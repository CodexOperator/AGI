"""goal:g7.28.2 -- the regression falsifier for `goal:g7.28` (persistent dispatch).

`goal:g7.28.1` added an OPT-IN `--persistent` seat hold to
`extensions/agi/bin/dispatch.py`. The claim under test here is the negative:
**absent `--persistent`, the non-persistent kid/parent spawn path is
UNCHANGED** -- argv + env byte-equal to the pre-persistent merge base, exactly
ONE child process, no `_supervise_persistent` call, the inline reaper still
armed (config `agent_dispatch.inline_reaper` default True), and no
`persistent` / `restart_count` keys on the agent record -- for BOTH
`--tier kid` and `--tier parent`.

Three independent instruments:

  1. **Dry-run parity vs the merge base.** The pre-persistent base
     `dispatch.py` is materialised from git (the parent of the commit that
     first introduced `_PERSIST_STOP_ENV`), loaded in-process with
     `child_engine_paths` pinned to HEAD's so the ONLY variable is the
     persistent feature, and both render the same `--dry-run` command + env
     for the same project. Compared after normalising the two intentionally
     random values (agent id, session tmp dir). No spawn.
  2. **Live lifecycle, real Popen.** A fake harness binary counts its own
     launches, so the process count is measured by the child, not asserted
     about a stubbed `Popen` (`subprocess.Popen` is NEVER patched here).
  3. **A `--persistent` control**, so instruments 1-2 are not vacuous: with
     the flag the supervisor IS called and the reaper is NOT.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

_PATH = "extensions/agi/bin/dispatch.py"
_MARKER = "_PERSIST_STOP_ENV"


def _load_dispatch(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch(BIN / "dispatch.py", "agi_dispatch_parity")


def _git(*args: str) -> str | None:
    """Read-only git; None when git or the history is unavailable."""
    try:
        r = subprocess.run(["git", *args], cwd=REPO, capture_output=True,
                           text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return r.stdout


def _pre_persistent_source() -> str | None:
    """The dispatch.py of the commit BEFORE `--persistent` landed."""
    log = _git("log", "--format=%H", "-S", _MARKER, "--", _PATH)
    if not log or not log.split():
        return None
    introduced = log.split()[-1]  # git log is newest-first
    return _git("show", f"{introduced}^:{_PATH}")


# ------------------------------------------------------------------ scratch


class _Scratch:
    def __init__(self, tmp_path: Path):
        self.project = tmp_path / "proj"
        self.out = tmp_path / "out"
        self.out.mkdir(parents=True)
        self.fake = self.out / "fake_harness.sh"
        self.fake.write_text(
            "#!/bin/sh\n"
            f'printf "LAUNCH\\n" >> "{self.out}/launches"\n'
            "exit 0\n")
        self.fake.chmod(0o755)
        g = self.project / ".agi"
        (g / "nodes" / ".geometry").mkdir(parents=True)
        (g / "nodes" / "hypothesis").mkdir(parents=True)
        (g / "nodes" / "goal").mkdir(parents=True)
        (g / "config.json").write_text(json.dumps({
            "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                                 "bin": str(self.fake),
                                 "models": {"kid": "deepseek-v4",
                                            "parent": "glm-flash"}}},
            "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
            # inline_reaper deliberately ABSENT -> the config default (True)
            # is the value under test, never an override.
        }))
        (g / "nodes" / ".geometry" / "ladder.md").write_text(
            "---\ncurrent_season: 2\nroles:\n"
            "  - {tier: 1, role: parent, harness: pi, model: glm-flash}\n"
            "  - {tier: 0, role: kid, harness: pi, model: deepseek-v4}\n"
            "---\nbody")
        (g / "nodes" / ".geometry" / "secrets.md").write_text(
            "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
        (g / "nodes" / "goal" / "g15.md").write_text(
            "---\nid: goal:g15\ntype: goal\n---\nbody\n")
        (g / "nodes" / "hypothesis" / "x.md").write_text(
            "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n"
            "  - goal:g15\n---\nbody\n")

    def argv(self, *extra: str) -> list[str]:
        return [str(BIN / "dispatch.py"), str(self.project), "1",
                "--level", "small", "--harness", "pi", *extra,
                "--target", "hypothesis:x"]

    def launches(self) -> int:
        f = self.out / "launches"
        deadline = time.time() + 15
        while not f.exists() and time.time() < deadline:
            time.sleep(0.05)
        return len(f.read_text().splitlines()) if f.exists() else 0

    def record(self) -> dict:
        for p in (self.project / ".agi" / "sessions").rglob("agent.json"):
            return json.loads(p.read_text())
        raise AssertionError("no agent.json written")


@pytest.fixture()
def scratch(tmp_path, monkeypatch) -> _Scratch:
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR"):
        monkeypatch.delenv(k, raising=False)
    return _Scratch(tmp_path)


def _tier_args(tier: str, extra=()) -> list[str]:
    args = ["--tier", tier]
    if tier == "parent":
        args += ["--role", "parent"]
    return args + list(extra)


# ------------------------------------------------------- 1. argv/env parity


def _normalise(line: str) -> str:
    line = re.sub(r"dry\d\d-[0-9a-f]{8}", "dryNN-AGENTID", line)
    return re.sub(r"/tmp/[A-Za-z0-9_./-]+", "/tmp/TMPPATH", line)


def _report_lines(text: str) -> list[str]:
    return [_normalise(l.strip()) for l in text.splitlines()
            if "command:" in l or l.strip().startswith("env:")]


def _render(mod, argv: list[str]) -> tuple[int, str]:
    old = sys.argv
    sys.argv = argv
    buf = io.StringIO()
    try:
        with redirect_stdout(buf):
            rc = mod.main()
    finally:
        sys.argv = old
    return rc, buf.getvalue()


def _run_main(argv: list[str]) -> int:
    old = sys.argv
    sys.argv = argv
    try:
        return dispatch.main()
    finally:
        sys.argv = old


@pytest.mark.parametrize("tier", ["kid", "parent"])
def test_nonpersistent_argv_and_env_match_the_pre_persistent_base(
        scratch, tmp_path, tier):
    """Conjunct 1+3: with `--persistent` absent, the rendered command and env
    are identical to the merge base for kid AND parent -- the persistent
    commit changed the non-persistent bytes in no way."""
    base_src = _pre_persistent_source()
    if base_src is None:
        pytest.skip("git history unavailable: cannot materialise the base")
    base_path = tmp_path / "dispatch_base.py"
    base_path.write_text(base_src)
    base = _load_dispatch(base_path, f"agi_dispatch_base_{tier}")
    # Pin engine paths to HEAD's, so file location is not a variable.
    base.child_engine_paths = dispatch.child_engine_paths

    argv = scratch.argv(*_tier_args(tier), "--dry-run")
    rc_b, out_b = _render(base, argv)
    rc_h, out_h = _render(dispatch, argv)
    assert (rc_b, rc_h) == (0, 0), (rc_b, rc_h)
    assert _report_lines(out_b) == _report_lines(out_h), (
        f"tier={tier} non-persistent argv/env drifted from the merge base:\n"
        f"BASE {_report_lines(out_b)}\nHEAD {_report_lines(out_h)}")


# ------------------------------------------------------- 2. live lifecycle


@pytest.mark.parametrize("tier", ["kid", "parent"])
def test_nonpersistent_lifecycle_is_one_real_process_no_supervisor(
        scratch, monkeypatch, tier):
    """Conjunct 2+3 with REAL Popen: one child, no supervisor, inline reaper
    still armed (config default True), no persistent keys on the record."""
    calls = {"reaper": 0, "supervise": 0}
    monkeypatch.setattr(dispatch, "_reaper_phase",
                        lambda **k: calls.__setitem__("reaper",
                                                      calls["reaper"] + 1))
    monkeypatch.setattr(dispatch, "_supervise_persistent",
                        lambda *a, **k: calls.__setitem__(
                            "supervise", calls["supervise"] + 1))
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)

    argv = scratch.argv(*_tier_args(tier))
    assert _run_main(argv) == 0, argv
    assert scratch.launches() == 1, (
        f"tier={tier}: fire-and-forget must be exactly one process")
    assert calls == {"reaper": 1, "supervise": 0}, calls
    rec = scratch.record()
    assert "persistent" not in rec and "restart_count" not in rec, rec


def test_persistent_control_calls_the_supervisor_not_the_reaper(
        scratch, monkeypatch):
    """Non-vacuity guard for the two tests above: WITH `--persistent` the
    supervisor runs and the inline reaper is off -- so instrument 2 can
    distinguish the two paths."""
    calls = {"reaper": 0, "supervise": 0}
    monkeypatch.setattr(dispatch, "_reaper_phase",
                        lambda **k: calls.__setitem__("reaper",
                                                      calls["reaper"] + 1))
    monkeypatch.setattr(dispatch, "_supervise_persistent",
                        lambda *a, **k: calls.__setitem__(
                            "supervise", calls["supervise"] + 1))
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)

    argv = scratch.argv(*_tier_args("kid"), "--persistent")
    assert _run_main(argv) == 0, argv
    assert calls == {"reaper": 0, "supervise": 1}, calls
