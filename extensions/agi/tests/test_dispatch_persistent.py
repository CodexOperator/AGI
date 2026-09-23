"""goal:g7.28.1 (hypothesis:a00-c3a24084-4190b2) -- falsifiers 1 and 3.

A `--persistent` dispatch HOLDS its seat and, when the child dies, re-opens
it through the SAME `_open_round` seam -- hence the SAME rendered
`spawn_args`/`spawn_env`, no second argv path, no re-render. And the seat's
record shows the occupation (persistent / live pid / restart_count).

No live model, no network, no real sleep: `subprocess.Popen` is faked for the
spawn path and `dispatch._PERSIST_SLEEP` is a no-op.
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


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                             "models": {"kid": "deepseek-v4",
                                        "parent": "deepseek-v4"}}},
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
    return tmp_path


class _StubProc:
    """A fake child: `poll()` returns None `left` times, then `rc` forever."""

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


def _fake_spawn(monkeypatch, plans, stop_after=None):
    """Patch the spawn Popen; `stop_after=N` sets the clean-stop env once N
    children have been opened, so a live persistent seat still ends."""
    spawned = []
    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if not kwargs.get("start_new_session"):
            return real_popen(argv, **kwargs)
        plan = plans[len(spawned)] if len(spawned) < len(plans) else plans[-1]
        f = kwargs.get("stdout")
        if f is not None and plan.get("bytes"):
            f.write(plan["bytes"])
            f.flush()
        proc = _StubProc(1000 + len(spawned), plan.get("rc"),
                         plan.get("left", 0))
        spawned.append((argv, proc))
        if stop_after is not None and len(spawned) >= stop_after:
            os.environ[dispatch._PERSIST_STOP_ENV] = "1"
        return proc

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda s: None)
    monkeypatch.setattr(dispatch, "_PERSIST_SLEEP", lambda s: None)
    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    return spawned


def _argv(tmp_path: Path, *extra, tier: str = "kid"):
    return [str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--level", "small", "--harness", "pi", "--tier", tier,
            "--target", "hypothesis:x", *extra]


def _count_build_command(monkeypatch) -> list:
    """Count adapter.build_command calls: a restart that rebuilt argv would
    call it a second time."""
    calls: list = []
    real_load = dispatch.adapters.load
    wrapped: set = set()

    def _load(name):
        mod = real_load(name)
        if id(mod) not in wrapped:
            wrapped.add(id(mod))
            orig = mod.build_command

            def _bc(*a, **k):
                calls.append(1)
                return orig(*a, **k)

            mod.build_command = _bc
        return mod

    monkeypatch.setattr(dispatch.adapters, "load", _load)
    return calls


def _manifest(root: Path) -> list[dict]:
    path = sorted(root.glob(".agi/sessions/**/manifest.json"))[0]
    return json.loads(path.read_text())["agents"]


def test_persistent_restart_reuses_the_very_same_argv(
        project, monkeypatch, capsys):
    """Falsifiers 1+3: the child dies, the supervisor restarts it, and the
    re-opened argv is the IDENTICAL list object the first spawn used -- the
    seam never rebuilt it (`mem_cap.wrap_argv` returns the same list when no
    cap is set, so `is` is the honest proof)."""
    spawned = _fake_spawn(monkeypatch, [
        {"left": 14, "rc": 1},
        {"left": 999, "rc": None},
    ], stop_after=2)
    builds = _count_build_command(monkeypatch)
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))

    assert dispatch.main() == 0
    assert len(spawned) == 2, f"expected one restart, got {len(spawned)}"
    # Same rendered argv: byte-identical, and the builder that renders it ran
    # exactly ONCE -- a restart through a second argv path would rebuild it.
    assert spawned[0][0] == spawned[1][0]
    assert len(builds) == 1, f"argv was rebuilt: build_command x{len(builds)}"


def test_fire_and_forget_default_spawns_no_supervisor(
        project, monkeypatch, capsys):
    """`--persistent` absent: exactly one spawn, no restart bookkeeping, and
    no supervisor in the path (the default must be unchanged)."""
    spawned = _fake_spawn(monkeypatch, [{"left": 999, "rc": None}])
    monkeypatch.setattr(sys, "argv", _argv(project))

    assert dispatch.main() == 0
    assert len(spawned) == 1, f"default path must not restart: {len(spawned)}"
    agents = _manifest(project)
    assert agents and "persistent" not in agents[0], agents
    assert "restart_count" not in agents[0], agents


def test_record_carries_persistent_live_pid_and_restart_count(
        project, monkeypatch, capsys):
    """Conjunct (c): the seat's own record shows the occupation -- persistent
    true, the CURRENT (restarted) pid, and the restart count."""
    spawned = _fake_spawn(monkeypatch, [
        {"left": 14, "rc": 1},
        {"left": 999, "rc": None},
    ], stop_after=2)
    monkeypatch.setattr(sys, "argv", _argv(project, "--persistent"))

    assert dispatch.main() == 0
    agents = _manifest(project)
    assert len(agents) == 1, agents
    rec = agents[0]
    assert rec["persistent"] is True, rec
    assert rec["restart_count"] == 1, rec
    assert rec["pid"] == spawned[1][1].pid, (
        f"record pid {rec['pid']} is not the live child "
        f"{spawned[1][1].pid}")


# The minted agent identity: `a00-<8 hex>`, and the scaffold slug that embeds
# it plus the writer's per-mint `uuid4().hex[:6]` suffix (`a00-<8hex>-<6hex>`).
_AGENT_RE = re.compile(r"a00-[0-9a-f]{8}(?:-[0-9a-f]{6})?")


def _norm_argv(argv: list[str], sessions: Path) -> list[str]:
    """The ONLY two nondeterministic fields, normalized in this order: the
    per-run session dir, then the minted agent identity -- the agent id and
    the scaffold node id/ slug derived from it (`experiment:<agent>`), which
    is what appears in the brief and the closing line."""
    return [_AGENT_RE.sub("<AGENT>", arg.replace(str(sessions), "<SESSIONS>"))
            for arg in argv]


@pytest.mark.parametrize("tier", ["kid", "parent"])
def test_goal_g7_28_2_persistent_is_opt_in_on_supervision_only(
        project, monkeypatch, capsys, tier):
    """goal:g7.28.2 -- the regression the `--persistent` feature could have
    caused: with the flag ABSENT the spawn path stays fire-and-forget.

    Same target, same harness, once WITHOUT `--persistent` and once WITH,
    for BOTH tier=kid and tier=parent. The two child argv lists are EQUAL
    after exactly two normalizations (session dir, agent id) -- the flag is
    opt-in on supervision only, never a second argv path. Non-persistent:
    exactly ONE Popen, the supervisor never entered, and the manifest record
    carries neither `persistent` nor `restart_count`. Control: with the flag
    the supervisor IS entered exactly once and the record IS stamped -- so
    this test cannot go green by the feature being deleted.
    """
    supervisor_calls: list = []
    monkeypatch.setattr(dispatch, "_supervise_persistent",
                        lambda *a, **k: supervisor_calls.append((a, k)) or 0)

    # --- run 1: WITHOUT --persistent (the invariant under test) ---
    spawned = _fake_spawn(monkeypatch, [{"left": 999, "rc": None}])
    monkeypatch.setattr(sys, "argv", _argv(project, tier=tier))
    assert dispatch.main() == 0
    assert len(spawned) == 1, f"non-persistent must Popen once: {len(spawned)}"
    assert supervisor_calls == [], (
        "fire-and-forget entered _supervise_persistent: "
        f"{supervisor_calls}")
    rec1 = _manifest(project)[0]
    argv_plain = _norm_argv(spawned[0][0], project / ".agi" / "sessions")
    assert "persistent" not in rec1 and "restart_count" not in rec1, rec1

    # --- run 2: WITH --persistent (control; same argv expected) ---
    supervisor_calls.clear()
    spawned_p = _fake_spawn(monkeypatch, [{"left": 999, "rc": None}])
    monkeypatch.setattr(sys, "argv",
                        _argv(project, "--persistent", tier=tier))
    assert dispatch.main() == 0
    assert len(spawned_p) == 1, len(spawned_p)
    assert len(supervisor_calls) == 1, (
        f"--persistent must enter the supervisor exactly once: "
        f"{len(supervisor_calls)}")
    rec2 = [r for r in _manifest(project) if r["id"] != rec1["id"]][-1]
    assert rec2["persistent"] is True, rec2
    assert rec2["restart_count"] == 0, rec2
    argv_persistent = _norm_argv(spawned_p[0][0],
                                 project / ".agi" / "sessions")

    # ARGV PARITY: FULL lists, two normalizations, no substring match.
    assert argv_plain == argv_persistent, (
        "the --persistent flag changed the non-persistent child argv:\n"
        f"  plain:      {argv_plain}\n  persistent: {argv_persistent}")
