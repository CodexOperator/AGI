"""Tests for hypothesis:l4-the-reaper-is-one-persistent-service part 2.

The persistent watcher (`heal.py watch`) discovers every live round under a
main checkout, runs the SAME `_reap_pass` dispatch.py's inline reaper uses,
and — for any agent still `running` past its manifest `timeout_seconds` —
marks it `timeout` in BOTH the agent record and the manifest it was found in,
plus exactly ONE dm to the stamped `dispatched_by` through the L4.113 path.

The claim fixture (in the hypothesis): a main checkout with TWO rounds whose
parents outlive their nominal timeout -> BOTH marked `timeout`, BOTH
dispatchers get exactly ONE dm, the watcher process pid unchanged across
both, and `heal.py watch --once` runs one pass and exits.

Test-side safety, matching the merge-up traps: `AGI_REAPER_LOG` is pointed at
a tmp file so no test ever touches ~/logs; a second `--once` pass is proven
idempotent (still exactly one dm each) so the watcher never double-sends.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
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
heal = _load("heal")


@pytest.fixture
def graph_project(tmp_path: Path) -> Path:
    """A project whose graph root (repo/.agi) carries nodes + config so the
    shared-inbox resolver lands dms in graph/sessions/inbox."""
    graph = tmp_path / "repo" / ".agi"
    (graph / "nodes").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    return graph


def _round(graph: Path, name: str, agent_id: str, timeout_s: int) -> None:
    """Two rounds whose owner outlives the nominal timeout."""
    it = graph / "sessions" / f"iter-{name}"
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({
        "timeout_seconds": timeout_s,
        "agents": [{"id": agent_id, "status": "running",
                    "dispatched_by": "director"}],
    }, indent=2))
    adir = it / agent_id
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "agent.json").write_text(json.dumps({
        "id": agent_id, "status": "running", "dispatched_by": "director",
        "started_at": int(time.time()) - 5,  # already past the 1s timeout
        "pid": 0,  # 0 -> no death-reap path; isolate the timeout mark
    }, indent=2))


def _inbox(graph: Path, who: str) -> Path:
    return cli.locations.shared_sessions_dir(graph) / "inbox" / f"{who}.md"


def _manifest_status(graph: Path, name: str, agent_id: str) -> str:
    m = json.loads((graph / "sessions" / f"iter-{name}" / "manifest.json")
                   .read_text())
    for e in m["agents"]:
        if e["id"] == agent_id:
            return e["status"]
    return "absent"


def test_watch_once_marks_two_timeouts_two_dms_one_log_event_each(
        graph_project, monkeypatch):
    """Two rounds whose owners outlived the deadline: both marked `timeout`,
    both dispatchers get exactly ONE dm, one log line per event, and the
    watcher's pid is unchanged across both rounds."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _round(graph_project, "A", "kid-a", 1)
    _round(graph_project, "B", "kid-b", 1)

    pid_before = os.getpid()
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    rc = heal.main()
    assert rc == 0  # --once runs one pass and exits
    assert os.getpid() == pid_before  # the SAME watcher did both rounds

    assert _manifest_status(graph_project, "A", "kid-a") == "timeout"
    assert _manifest_status(graph_project, "B", "kid-b") == "timeout"

    inbox_a = _inbox(graph_project, "director")
    text = inbox_a.read_text()
    # ONE dm per round, both to the same stamped dispatcher, in ONE inbox.
    assert text.count("from:") == 2, "exactly one dm per terminal round"
    assert text.count("reason=timeout") == 2
    assert "iter=iter-A agent=kid-a" in text
    assert "iter=iter-B agent=kid-b" in text

    log_text = log.read_text()
    assert "marked timeout" in log_text
    assert log_text.count("marked timeout") == 2  # ONE log line per event
    assert "iter-iter-A" in log_text or "iter-A" in log_text


def test_watch_second_pass_is_idempotent_no_double_dm(graph_project, monkeypatch):
    """A second `--once` pass over an already-marked round must not mark again
    nor re-send the dm — exactly one dm survives both passes."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _round(graph_project, "C", "kid-c", 1)

    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0
    assert heal.main() == 0  # second pass

    text = _inbox(graph_project, "director").read_text()
    assert text.count("from:") == 1, "second pass must not re-send the dm"


def test_watch_round_with_no_dispatcher_still_marks_and_logs(
        graph_project, monkeypatch, capsys):
    """A round with NO `dispatched_by` stamp is marked `timeout` and logs the
    mark; the dm is skipped but there is never silence."""
    it = graph_project / "sessions" / "iter-D"
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({
        "timeout_seconds": 1,
        "agents": [{"id": "kid-d", "status": "running"}],
    }, indent=2))
    adir = it / "kid-d"
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "agent.json").write_text(json.dumps({
        "id": "kid-d", "status": "running",
        "started_at": int(time.time()) - 5, "pid": 0,
    }, indent=2))

    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "r2.log"))
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0

    assert _manifest_status(graph_project, "D", "kid-d") == "timeout"
    # dm goes nowhere (no stamp) but a warn line is emitted — never silence
    assert "no dispatcher stamp" in capsys.readouterr().err

def _dead_pid() -> int:
    """A genuinely-dead pid (a short-lived process that has already exited)."""
    import subprocess
    p = subprocess.Popen([sys.executable, "-c", "pass"])
    p.wait()
    return p.pid


def _round_dead(graph: Path, name: str, agent_id: str, timeout_s: int,
                started_ago: int, pid: int) -> None:
    """A round whose agent pid is DEAD — the service DEATH path."""
    it = graph / "sessions" / f"iter-{name}"
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({
        "timeout_seconds": timeout_s,
        "agents": [{"id": agent_id, "status": "running",
                    "dispatched_by": "director", "pid": pid}],
    }, indent=2))
    adir = it / agent_id
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "agent.json").write_text(json.dumps({
        "id": agent_id, "status": "running", "dispatched_by": "director",
        "started_at": int(time.time()) - started_ago, "pid": pid,
    }, indent=2))


def test_watch_dead_pid_within_deadline_is_a_death_with_one_dm(
        graph_project, monkeypatch):
    """Residue (a): a dead pid WITHIN its deadline is recorded as a DEATH
    (status failed, honest 'pid N died' reason — NOT the bogus 'restart
    unavailable') with exactly ONE death dm, one log line."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _round_dead(graph_project, "E", "kid-e", timeout_s=1000, started_ago=5,
                pid=_dead_pid())
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0

    assert _manifest_status(graph_project, "E", "kid-e") == "failed"
    rec = json.loads((graph_project / "sessions" / "iter-E" / "kid-e"
                      / "agent.json").read_text())
    assert rec["status"] == "failed"
    assert "died" in rec["fail_reason"], rec["fail_reason"]
    assert "restart unavailable" not in rec["fail_reason"]

    text = _inbox(graph_project, "director").read_text()
    assert text.count("from:") == 1, "exactly one death dm"
    assert "reason=death" in text
    assert "reason=timeout" not in text
    assert _manifest_status(graph_project, "E", "kid-e") == "failed"


def test_watch_dead_pid_past_deadline_is_a_death_not_timeout(
        graph_project, monkeypatch):
    """Residue (a): a dead pid PAST its deadline is a DEATH, never overwritten
    to `timeout` — one status, one dm, distinguishable in the dm text."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _round_dead(graph_project, "F", "kid-f", timeout_s=1, started_ago=5,
                pid=_dead_pid())
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0

    assert _manifest_status(graph_project, "F", "kid-f") == "failed"
    rec = json.loads((graph_project / "sessions" / "iter-F" / "kid-f"
                      / "agent.json").read_text())
    assert rec["status"] == "failed"
    assert "died" in rec["fail_reason"]
    assert "past manifest timeout_seconds" not in rec["fail_reason"]

    text = _inbox(graph_project, "director").read_text()
    assert text.count("from:") == 1, "exactly one death dm, not a timeout dm"
    assert "reason=death" in text
    assert "reason=timeout" not in text


def test_watch_death_not_double_dm_on_second_pass(graph_project, monkeypatch):
    """A second `--once` pass over an already-recorded death must not re-send
    the death dm — the watcher stays idempotent across passes."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _round_dead(graph_project, "G", "kid-g", timeout_s=1000, started_ago=5,
                pid=_dead_pid())
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0
    assert heal.main() == 0  # second pass
    text = _inbox(graph_project, "director").read_text()
    assert text.count("from:") == 1, "second pass must not re-send the dm"


class _FlipFlopAdapter:
    """Exercises EXACTLY the transition the other dead-pid tests never reach
    (hypothesis:l4-heal-death-past-deadline-branch-has-a-test). is_alive
    returns True on the FIRST call for a pid — so `_reap_pass` sees the agent
    alive and leaves it in `outcome["still"]` — and False on every call after
    — so the watcher's own timeout check (heal.py:320) sees it dead and
    records a DEATH, not a timeout."""

    def __init__(self):
        self._calls = {}

    def is_alive(self, pid: int) -> bool:
        n = self._calls.get(pid, 0)
        self._calls[pid] = n + 1
        return n == 0


def _round_alive_then_dead(graph: Path, name: str, agent_id: str,
                           timeout_s: int, started_ago: int, pid: int) -> None:
    """A round whose agent is ALIVE at the reap pass and DEAD by the watcher's
    own deadline check — the death-past-deadline transition under test."""
    it = graph / "sessions" / f"iter-{name}"
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({
        "timeout_seconds": timeout_s,
        "agents": [{"id": agent_id, "status": "running",
                    "dispatched_by": "director", "pid": pid}],
    }, indent=2))
    adir = it / agent_id
    adir.mkdir(parents=True, exist_ok=True)
    (adir / "agent.json").write_text(json.dumps({
        "id": agent_id, "status": "running", "dispatched_by": "director",
        "started_at": int(time.time()) - started_ago, "pid": pid,
    }, indent=2))


def test_watch_dead_past_deadline_alive_at_reap_then_dead(graph_project,
                                                          monkeypatch):
    """The transition: pid ALIVE at the reap pass (left in `still`), DEAD by
    the timeout check -> a DEATH is recorded (never a timeout): agent.json
    status failed + 'pid N died (detected by reaper)' + finished_at set, the
    manifest updated, EXACTLY ONE death dm, NO timeout dm, and the watch log
    carries 'marked DEAD past deadline'."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    monkeypatch.setattr(heal, "_WatcherAdapter", _FlipFlopAdapter)
    _round_alive_then_dead(graph_project, "H", "kid-h", timeout_s=1,
                           started_ago=5, pid=424242)
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0

    # agent.json: honest death, NOT a timeout overwrite.
    rec = json.loads((graph_project / "sessions" / "iter-H" / "kid-h"
                      / "agent.json").read_text())
    assert rec["status"] == "failed", rec["status"]
    assert rec["fail_reason"] == "pid 424242 died (detected by reaper)", \
        rec["fail_reason"]
    assert rec.get("finished_at"), "finished_at must be set"
    assert "timeout_reason" not in rec

    # manifest entry updated in lockstep.
    man = json.loads((graph_project / "sessions" / "iter-H"
                      / "manifest.json").read_text())
    entry = next(e for e in man["agents"] if e["id"] == "kid-h")
    assert entry["status"] == "failed"
    assert entry["finished_at"] == rec["finished_at"]
    assert entry["fail_reason"] == rec["fail_reason"]

    # EXACTLY ONE dm, reason=death, never timeout.
    text = _inbox(graph_project, "director").read_text()
    assert text.count("from:") == 1, "exactly one death dm"
    assert "reason=death" in text
    assert "reason=timeout" not in text

    # watch log line for the death-past-deadline mark.
    ltext = log.read_text()
    assert "marked DEAD past deadline" in ltext
    assert "marked timeout" not in ltext


def test_watch_dead_past_deadline_no_double_dm_on_second_pass(
        graph_project, monkeypatch):
    """A second pass over the already-recorded death-past-deadline must not
    re-dm — the L4.123 double-dm guard holds for this branch too."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    monkeypatch.setattr(heal, "_WatcherAdapter", _FlipFlopAdapter)
    _round_alive_then_dead(graph_project, "I", "kid-i", timeout_s=1,
                           started_ago=5, pid=424243)
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0
    assert heal.main() == 0  # second pass
    text = _inbox(graph_project, "director").read_text()
    assert text.count("from:") == 1, "second pass must not re-send the dm"


class _AlwaysAliveAdapter:
    """is_alive always True — the sibling path: a live pid past its deadline
    is STILL a timeout, not a death. Guards the :320 branch's condition, so
    an over-eager death detector here is caught."""
    def is_alive(self, pid: int) -> bool:
        return True


def test_watch_alive_past_deadline_still_timeout_not_death(graph_project,
                                                           monkeypatch):
    """Sibling path (untouched): pid alive at BOTH checks still records the
    TIMEOUT, never a death — the death branch must not fire when is_alive is
    true."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    monkeypatch.setattr(heal, "_WatcherAdapter", _AlwaysAliveAdapter)
    _round_alive_then_dead(graph_project, "J", "kid-j", timeout_s=1,
                           started_ago=5, pid=424244)
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0

    assert _manifest_status(graph_project, "J", "kid-j") == "timeout"
    rec = json.loads((graph_project / "sessions" / "iter-J" / "kid-j"
                      / "agent.json").read_text())
    assert rec["status"] == "timeout", rec["status"]
    assert rec.get("fail_reason") != "pid 424244 died (detected by reaper"
    assert "timeout_reason" in rec, "timeout sets timeout_reason, not a death"
    text = _inbox(graph_project, "director").read_text()
    assert "reason=timeout" in text
    assert "reason=death" not in text
