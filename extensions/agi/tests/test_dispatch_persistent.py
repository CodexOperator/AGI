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


def _argv(tmp_path: Path, *extra):
    return [str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--level", "small", "--harness", "pi", "--tier", "kid",
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


def test_record_carries_persistent_state_and_live_pid_at_end(
        project, monkeypatch, capsys):
    """Conjunct (c) + occupation honesty: while the hold runs the record
    names the CURRENT (restarted) pid; when the hold ends with the child
    still ALIVE the record keeps that live pid (state `released`) rather
    than erasing a running occupant."""
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
    assert rec["persistent_state"] == "released", rec
    assert rec["pid"] == spawned[1][1].pid, rec
    # the manifest and the session agent.json are the same bytes: both name
    # the live occupant, neither erases it.
    sess = json.loads(sorted((project / ".agi" / "sessions").glob(
        f"**/{rec['id']}/agent.json"))[0].read_text())
    assert sess["persistent_state"] == "released", sess
    assert sess["pid"] == spawned[1][1].pid, sess


def _record():
    return {"id": "a", "persistent": True, "restart_count": 0, "pid": 111}


def test_zero_restarts_dead_child_marks_ended(tmp_path, monkeypatch):
    """Gate: max_restarts=0 with a dead child -> no restart, record marked
    ended (not running) with no live pid asserted."""
    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    session = tmp_path / "sess"
    session.mkdir()
    rec = _record()
    reopens: list = []

    def reopen(mode):
        reopens.append(mode)
        return _StubProc(222, None, 999)

    dispatch._supervise_persistent(
        _StubProc(111, 1, 0), reopen, iter_dir=tmp_path, agent_id="a",
        record=rec, session=session, max_restarts=0)
    assert reopens == [], "a zero-restart hold must not re-open"
    assert rec["persistent_state"] == "exhausted", rec
    assert rec["pid"] is None, rec
    on_disk = json.loads((session / "agent.json").read_text())
    assert on_disk["persistent_state"] == "exhausted", on_disk
    assert on_disk["pid"] is None, on_disk


def test_stop_env_keeps_a_live_occupant_released(tmp_path, monkeypatch):
    """Wire (the case the parent's probe D FAILED): AGI_PERSISTENT_STOP=1
    while the child's `poll()` is None (ALIVE) -> the persisted record's
    `pid` IS that live child's pid, and the state is not `running`. The
    hold ending must never be reported as the occupant being gone."""
    session = tmp_path / "sess"
    session.mkdir()
    rec = _record()
    reopens: list = []
    monkeypatch.setenv(dispatch._PERSIST_STOP_ENV, "1")

    def reopen(mode):
        reopens.append(mode)
        return _StubProc(222, None, 999)

    live = _StubProc(111, None, 999)
    dispatch._supervise_persistent(
        live, reopen, iter_dir=tmp_path, agent_id="a",
        record=rec, session=session, max_restarts=2)
    assert reopens == [], "a stopped hold must not re-open"
    assert rec["persistent_state"] != "running", rec
    assert rec["persistent_state"] == "released", rec
    assert rec["pid"] == live.pid, rec
    on_disk = json.loads((session / "agent.json").read_text())
    assert on_disk["persistent_state"] == "released", on_disk
    assert on_disk["pid"] == live.pid, on_disk


def test_stop_env_marks_stopped_when_child_is_dead(tmp_path, monkeypatch):
    """Gate: AGI_PERSISTENT_STOP=1 with a DEAD child -> no restart, state
    `stopped`, pid None (the original honesty case must still hold)."""
    session = tmp_path / "sess"
    session.mkdir()
    rec = _record()
    reopens: list = []
    monkeypatch.setenv(dispatch._PERSIST_STOP_ENV, "1")

    def reopen(mode):
        reopens.append(mode)
        return _StubProc(222, None, 999)

    dispatch._supervise_persistent(
        _StubProc(111, 1, 0), reopen, iter_dir=tmp_path, agent_id="a",
        record=rec, session=session, max_restarts=2)
    assert reopens == [], "a stopped hold must not re-open"
    assert rec["persistent_state"] == "stopped", rec
    assert rec["pid"] is None, rec


def test_instantly_dead_reopen_is_not_named_as_the_occupant(tmp_path,
                                                           monkeypatch):
    """Wire (the case the prior round's probe C FAILED): max_restarts=2 with
    an instantly-dead `reopen` -> the persisted record's `persistent_state`
    is not `running`, and its `pid` is not any re-opened child's pid."""
    monkeypatch.delenv(dispatch._PERSIST_STOP_ENV, raising=False)
    session = tmp_path / "sess"
    session.mkdir()
    rec = _record()
    dead_pids: list = []
    calls = {"n": 0}

    def reopen(mode):
        calls["n"] += 1
        pid = 9000 + calls["n"]
        dead_pids.append(pid)
        return _StubProc(pid, 1, 0)  # instantly dead

    dispatch._supervise_persistent(
        _StubProc(111, 1, 0), reopen, iter_dir=tmp_path, agent_id="a",
        record=rec, session=session, max_restarts=2)
    assert calls["n"] == 2, calls
    assert rec["persistent_state"] != "running", rec
    assert rec["persistent_state"] == "exhausted", rec
    assert rec["pid"] not in dead_pids and rec["pid"] is None, rec
    on_disk = json.loads((session / "agent.json").read_text())
    assert on_disk["persistent_state"] != "running", on_disk
    assert on_disk["pid"] not in dead_pids and on_disk["pid"] is None, on_disk
