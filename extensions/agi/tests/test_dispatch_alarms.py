"""Tests for hypothesis:l4-a-round-alarms-its-dispatcher-by-default.

The load-bearing links tested here: (1) the `dispatched_by` stamp dispatch.py
writes into each agent record at spawn, and (2) the completion dm cli.py's
`done` path sends to that stamp. The fixture runs the helper directly against
a scratch project (a real cli.py `done` needs a live spawn); a dm that would
be sent from a worktree lands in the ONE shared inbox via send.py's
shared-sessions resolver, which is exactly what this asserts.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

cli = _load("cli")


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A minimal agi project so the shared-inbox resolver has a graph root."""
    root = tmp_path / "project"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    return root


def _write_manifest(root: Path, iter_n: str, agent_id: str,
                    dispatched_by) -> None:
    it = cli.locations.iteration_dir(root, iter_n)
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({"agents": [{
        "id": agent_id,
        "status": "running",
        "dispatched_by": dispatched_by,
    }]}, indent=2))


def _inbox(root: Path, who: str) -> Path:
    return cli.locations.shared_sessions_dir(root) / "inbox" / f"{who}.md"


def test_completion_dm_lands_exactly_once(project: Path, monkeypatch, capsys):
    """A round with a dispatcher stamp finishes -> ONE dm in the shared inbox."""
    iter_n, agent_id, dispatcher = "L4.999", "kid-alarm", "director"
    _write_manifest(project, iter_n, agent_id, dispatcher)
    monkeypatch.setattr(cli, "_session_root", lambda: project)

    cli._alarm_dispatcher_on_done(project, iter_n, agent_id,
                                  "experiment:alarm-x", "proved")

    inbox = _inbox(project, dispatcher)
    assert inbox.is_file(), f"no inbox at {inbox}"
    text = inbox.read_text()
    # exactly ONE message block (the MSG_SEP begins every block)
    assert text.count("from:") == 1
    assert "iter=L4.999" in text
    assert "agent=kid-alarm" in text
    assert "node=experiment:alarm-x" in text
    assert "verdict=proved" in text
    assert "to: director" in text
    # the dispatcher's OUTBOX/DM pairing is not how send works; block is inbox-side
    capsys.readouterr()  # swallow the printed inbox path


def test_absent_dispatcher_is_a_stderr_line_not_a_crash(project, monkeypatch, capsys):
    """No dispatcher stamp -> one stderr line, no dm, no exception."""
    iter_n, agent_id = "L4.998", "kid-solo"
    _write_manifest(project, iter_n, agent_id, None)
    monkeypatch.setattr(cli, "_session_root", lambda: project)

    rc = cli._alarm_dispatcher_on_done(project, iter_n, agent_id,
                                       "experiment:solo-x", "pending")
    assert rc is None  # never fatal
    err = capsys.readouterr().err
    assert "no dispatcher stamp" in err
    assert err.count("warn: no dispatcher stamp") == 1
    assert not _inbox(project, "kid-solo").exists()
    # and no inbox for a guessed name either (we never invent identity)
    assert not _inbox(project, "director").exists()


def test_missing_manifest_silently_skips(project, monkeypatch, capsys):
    monkeypatch.setattr(cli, "_session_root", lambda: project)
    rc = cli._alarm_dispatcher_on_done(project, "L4.997", "ghost",
                                       "experiment:g-x", "pending")
    assert rc is None
    assert capsys.readouterr().err == ""

import time  # noqa: E402 (used by the heal fixtures below)


# --- heal.py: death / timeout events (the round's OTHER terminal events) ---
# These drive heal.main()'s real poll loop against a fixture manifest with a
# `dispatched_by` stamp, patching only the side-effects that would spawn a
# real pi process or sleep the test — the event alarm itself runs untouched.

heal = _load("heal")


def _graph_project(repo: Path) -> Path:
    """A project whose graph root (repo/.agi) carries nodes + config, so
    send.py's shared-inbox resolver (_inbox_dir -> shared_sessions_dir)
    lands the dm in graph/sessions/inbox regardless of worktree."""
    graph = repo / ".agi"
    (graph / "nodes").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    return graph


def _heal_fixture(graph: Path, iter_n: str, agent_id: str, dispatched_by,
                  started_at: float, pid: int) -> None:
    it = cli.locations.iteration_dir(graph, iter_n)
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({
        "timeout_seconds": 600,
        "agents": [{"id": agent_id, "status": "running",
                    "dispatched_by": dispatched_by}],
    }, indent=2))
    adir = it / agent_id
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "agent.json").write_text(json.dumps({
        "id": agent_id, "status": "running", "dispatched_by": dispatched_by,
        "started_at": int(started_at), "pid": pid,
    }, indent=2))


def test_heal_timeout_sends_one_dm_to_the_dispatcher(tmp_path, monkeypatch):
    """A round that TIMES OUT -> the dispatch stamp gets exactly ONE dm
    naming the timeout, measured from the one shared inbox."""
    graph = _graph_project(tmp_path)
    iter_n, agent_id, dispatcher = "L4.901", "kid-hung", "director"
    _heal_fixture(graph, iter_n, agent_id, dispatcher,
                  started_at=time.time() - 100000, pid=4242)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(graph), iter_n])
    monkeypatch.setattr("time.sleep", lambda *a, **k: None)

    def fake_heal(root, it, aid, rec):
        rec["status"] = "hung-healed"
        rec["finished_at"] = 1
        (cli.locations.iteration_dir(root, it) / aid / "agent.json").write_text(
            json.dumps(rec, indent=2))
    monkeypatch.setattr(heal, "_heal", fake_heal)

    rc = heal.main()
    assert rc == 0
    inbox = _inbox(graph, dispatcher)
    assert inbox.is_file(), f"no dm inbox at {inbox}"
    text = inbox.read_text()
    assert text.count("from:") == 1, f"expected exactly ONE dm, got:\n{text}"
    assert f"agent={agent_id}" in text
    assert "reason=timeout" in text


def test_heal_death_sends_one_dm_to_the_dispatcher(tmp_path, monkeypatch):
    """A round whose pid disappears -> exactly ONE dm naming the death."""
    graph = _graph_project(tmp_path)
    iter_n, agent_id, dispatcher = "L4.902", "kid-died", "director"
    _heal_fixture(graph, iter_n, agent_id, dispatcher,
                  started_at=time.time(), pid=4242)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(graph), iter_n])
    monkeypatch.setattr("time.sleep", lambda *a, **k: None)
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: False)

    rc = heal.main()
    assert rc == 0
    inbox = _inbox(graph, dispatcher)
    assert inbox.is_file(), f"no dm inbox at {inbox}"
    text = inbox.read_text()
    assert text.count("from:") == 1, f"expected exactly ONE dm, got:\n{text}"
    assert f"agent={agent_id}" in text
    assert "reason=death" in text


def test_heal_absent_dispatcher_still_finishes(tmp_path, monkeypatch, capsys):
    """A stamp-less round that times out sends no dm and no crash — healing
    still closes the agent out (the alarm must never break the heal)."""
    graph = _graph_project(tmp_path)
    iter_n, agent_id = "L4.903", "kid-solo-hung"
    _heal_fixture(graph, iter_n, agent_id, None,
                  started_at=time.time() - 100000, pid=4242)
    monkeypatch.setattr(sys, "argv", ["heal.py", str(graph), iter_n])
    monkeypatch.setattr("time.sleep", lambda *a, **k: None)
    monkeypatch.setattr(heal, "_pid_alive", lambda pid: True)

    def fake_heal(root, it, aid, rec):
        rec["status"] = "hung-healed"
        rec["finished_at"] = 1
        (cli.locations.iteration_dir(root, it) / aid / "agent.json").write_text(
            json.dumps(rec, indent=2))
    monkeypatch.setattr(heal, "_heal", fake_heal)

    rc = heal.main()
    assert rc == 0
    assert not _inbox(graph, agent_id).exists()
    assert not _inbox(graph, "director").exists()
    assert "no dispatcher stamp" in capsys.readouterr().err


# --- dispatcher's reaper give-up (dispatch.py _reaper_phase: finished:) ----
# Exercises the real give-up site (not a hand-unrolled copy): a manifest with
# a still-running agent past the deadline -> each stamp gets one dm naming who
# was still running.

dispatch = _load("dispatch")


def test_reaper_give_up_alarms_each_still_running_dispatchers(tmp_path, monkeypatch):
    graph = _graph_project(tmp_path)
    iter_n = "L4.904"
    it = cli.locations.iteration_dir(graph, iter_n)
    it.mkdir(parents=True, exist_ok=True)
    manifest = {"timeout_seconds": 600, "agents": [
        {"id": "kid-a", "status": "running", "dispatched_by": "seat-a"},
        {"id": "kid-b", "status": "done", "dispatched_by": "seat-b"},
        {"id": "kid-c", "status": "failed", "dispatched_by": "seat-c"},
    ]}
    (it / "manifest.json").write_text(json.dumps(manifest, indent=2))
    for aid in ("kid-a", "kid-b", "kid-c"):
        adir = it / aid
        adir.mkdir(parents=True, exist_ok=True)
        (adir / "agent.json").write_text(
            json.dumps({"id": aid, "status": "running", "pid": 0}))

    class FakeAdapter:
        def is_alive(self, pid):
            return True

    import time as _time
    monkeypatch.setattr(_time, "sleep", lambda *a, **k: None)
    dispatch.stall_detect.record_stalled_in_iteration = lambda d: None
    dispatch._reaper_phase(graph, it, FakeAdapter(), timeout_s=600,
                           max_wait_s=1, cap=1, cfg={})

    inbox_a = _inbox(graph, "seat-a")
    assert inbox_a.is_file(), "still-running kid-a should alarm seat-a"
    text = inbox_a.read_text()
    assert text.count("from:") == 1
    assert "still-running=kid-a" in text
    # terminal agents never alarm their dispatcher on give-up
    assert not _inbox(graph, "seat-b").exists()
    assert not _inbox(graph, "seat-c").exists()

