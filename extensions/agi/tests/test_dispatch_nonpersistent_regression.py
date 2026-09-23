"""goal:g7.28.2 (hypothesis:a00-e61f6143-e142a1) -- the non-persistent
regression: adding `--persistent` must leave the default kid/parent spawn
byte-for-byte alone.

Three residuals the g7.28.1 suite does not cover:

1. **argv parity.** The default path still renders its argv through the ONE
   adapter/template seam, once -- and the `--persistent` run renders the SAME
   seam inputs and the SAME env, so the opt-in flag changed nothing.
2. **Non-vacuous absence.** `persistent`/`restart_count` are absent from a
   default record *because the default path never enters that branch*, not
   because nothing ever writes them: the SAME assertions invert under
   `--persistent`.
3. **Dry-run parity.** `--dry-run` resolves the same command line with and
   without `--persistent`, and no persistent bookkeeping leaks into it.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load_dispatch():
    spec = importlib.util.spec_from_file_location(
        "agi_dispatch", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()


def _make_project(base: Path) -> Path:
    graph = base / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                             "models": {"kid": "deepseek-v4"}}},
        "spawn": {"harness": "pi", "parallel": 1, "max_live": 25},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 0, role: kid, "
        "harness: pi, model: deepseek-v4}\n---\nbody")
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR", dispatch._PERSIST_STOP_ENV):
        os.environ.pop(k, None)
    return base


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    return _make_project(tmp_path)


class _StubProc:
    def __init__(self, pid, rc, left):
        self.pid = pid
        self._rc = rc
        self._left = left
        self.returncode = None

    def poll(self):
        if self._left <= 0:
            if self._rc is not None:
                self.returncode = self._rc
            return self.returncode
        self._left -= 1
        return None


def _fake_spawn(monkeypatch, stop_after=None):
    """Every child lives forever; `stop_after=N` sets the clean-stop env
    once N children exist so a `--persistent` hold still ends."""
    spawned = []
    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if not kwargs.get("start_new_session"):
            return real_popen(argv, **kwargs)
        f = kwargs.get("stdout")
        if f is not None:
            f.write(b"# fake child\n")
            f.flush()
        proc = _StubProc(2000 + len(spawned), None, 0)
        spawned.append((list(argv), kwargs.get("env"), proc))
        if stop_after is not None and len(spawned) >= stop_after:
            os.environ[dispatch._PERSIST_STOP_ENV] = "1"
        return proc

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", lambda s: None)
    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    return spawned


def _count_build_command(monkeypatch) -> list:
    """Record every `build_command` call's kwargs, in order."""
    calls: list = []
    real_load = dispatch.adapters.load
    wrapped: set = set()

    def _load(name):
        mod = real_load(name)
        if id(mod) not in wrapped:
            wrapped.add(id(mod))
            orig = mod.build_command

            def _bc(*a, **k):
                calls.append(dict(k))
                return orig(*a, **k)

            mod.build_command = _bc
        return mod

    monkeypatch.setattr(dispatch.adapters, "load", _load)
    return calls


def _argv(root: Path, *extra):
    return [str(BIN / "dispatch.py"), str(root), "1",
            "--level", "small", "--harness", "pi", "--tier", "kid",
            "--target", "hypothesis:x", *extra]


def _manifest(root: Path) -> list[dict]:
    path = sorted(root.glob(".agi/sessions/**/manifest.json"))[0]
    return json.loads(path.read_text())["agents"]


# Path/identity keys the two runs legitimately differ on. They are the
# PLACEHOLDERS of the seam, not its inputs: the claim is that the routing
# inputs (tier, role, model, effort, level) are untouched.
_PATH_KEYS = {"context_file", "agent_id", "sess_dir", "scaffold"}
# Random per-run identity exports, not routing.
_ENV_DROP = {"AGI_AGENT_ID", "AGI_ACTOR"}


def test_default_and_persistent_render_the_same_seam_args(
        project, monkeypatch):
    """Residual 1: `--persistent` is inert on the adapter/template seam --
    same routing kwargs, same env, and `build_command` runs exactly once on
    each path (a second argv path would double it)."""
    spawned = _fake_spawn(monkeypatch, stop_after=1)
    builds = _count_build_command(monkeypatch)

    monkeypatch.setattr(sys, "argv", _argv(project))
    assert dispatch.main() == 0
    assert len(spawned) == 1, "default must spawn exactly once"
    assert len(builds) == 1, "default rebuilt its argv"
    default_kwargs = builds[0]
    default_env = spawned[0][1]

    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    spawned.clear()
    builds.clear()
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))
    assert dispatch.main() == 0
    assert len(spawned) == 1, "a live persistent seat holds, never restarts"
    assert len(builds) == 1, "persistent path rebuilt its argv"
    persistent_kwargs = builds[0]
    persistent_env = spawned[0][1]

    assert {k: v for k, v in default_kwargs.items()
            if k not in _PATH_KEYS} == \
           {k: v for k, v in persistent_kwargs.items()
            if k not in _PATH_KEYS}, "the seam inputs changed under --persistent"
    assert {k: v for k, v in default_env.items() if k not in _ENV_DROP} == \
           {k: v for k, v in persistent_env.items()
            if k not in _ENV_DROP}, "the child env changed under --persistent"


def test_absence_of_persistent_bookkeeping_is_not_vacuous(
        project, monkeypatch):
    """Residual 2: the default record's LACK of `persistent`/`restart_count`
    is a real signal -- the same probe inverts once `--persistent` is set."""
    _fake_spawn(monkeypatch, stop_after=1)

    monkeypatch.setattr(sys, "argv", _argv(project))
    assert dispatch.main() == 0
    default_rec = _manifest(project)[0]

    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))
    assert dispatch.main() == 0
    persistent_rec = [a for a in _manifest(project)
                      if a["id"] != default_rec["id"]][0]

    # The default-path assertions (the very ones in the g7.28.1 suite)...
    assert "persistent" not in default_rec, default_rec
    assert "restart_count" not in default_rec, default_rec
    # ...are not vacuous: the same keys DO appear under --persistent.
    assert persistent_rec["persistent"] is True, persistent_rec
    assert persistent_rec["restart_count"] == 0, persistent_rec


def _norm_dry(text: str) -> str:
    text = re.sub(r"dry\d\d-[0-9a-f]{8}", "DRYID", text)
    text = re.sub(r"/tmp/[^\s\"']+\.jsonl", "TRAJ", text)
    text = re.sub(r"/tmp/[^\s\"']+\.md", "CTX", text)
    text = re.sub(r"/tmp/tmp[^\s\"']+", "TMP", text)
    return text


def test_dry_run_is_unchanged_and_leaks_no_persistent_bookkeeping(
        project, monkeypatch, capsys):
    """Residual 3: `--dry-run` resolves the identical command line with and
    without `--persistent`, and prints no persistent bookkeeping."""
    monkeypatch.setattr(sys, "argv", _argv(project, "--dry-run"))
    assert dispatch.main() == 0
    base = capsys.readouterr().out
    assert "persistent" not in base, "persistent bookkeeping leaked to dry-run"

    monkeypatch.setattr(sys, "argv", _argv(project, "--dry-run", "--persistent"))
    assert dispatch.main() == 0
    flagged = capsys.readouterr().out
    assert "persistent" not in flagged, \
        "--persistent leaked bookkeeping into --dry-run"

    def commands(text):
        return [l.strip() for l in text.splitlines()
                if l.strip().startswith("command:")]

    assert commands(_norm_dry(base)) == commands(_norm_dry(flagged)), (
        "the dry-run command line changed under --persistent")
    assert len(commands(base)) == 1, "expected exactly one resolved slot"
    # A dry run is a read: no session dir, no manifest.
    assert not list(project.glob(".agi/sessions/**/manifest.json"))
