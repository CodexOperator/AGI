"""Tests for hypothesis:l4-the-reaper-is-one-persistent-service part 2.

The persistent watcher (`heal.py watch`) discovers every live round under a
main checkout, runs the SAME `_reap_pass` dispatch.py's inline reaper uses,
and — for any agent still `running` past its manifest `timeout_seconds`
whose pid is genuinely DEAD — records the death (`failed`). A LIVE pid past
its deadline is never written a terminal word: it is marked `overdue`
(hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal) — status stays
`running`, `overdue_since`/`overdue_reason` set, EXACTLY ONE `overdue` dm
through the L4.113 path, never a second dm on a later pass.

The claim fixture (in the hypothesis): a main checkout with TWO rounds whose
parents outlive their nominal timeout -> BOTH marked `overdue` (status still
`running`), BOTH dispatchers get exactly ONE dm, the watcher process pid
unchanged across both, and `heal.py watch --once` runs one pass and exits.

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
    """Two rounds whose owners outlived the deadline: BOTH marked `overdue`
    (status stays `running`), both dispatchers get exactly ONE dm, one log
    line per event, and the watcher's pid is unchanged across both rounds."""
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

    assert _manifest_status(graph_project, "A", "kid-a") == "running"
    assert _manifest_status(graph_project, "B", "kid-b") == "running"

    # each agent gained the overdue mark, never a terminal word.
    for nm, aid in (("A", "kid-a"), ("B", "kid-b")):
        rec = json.loads((graph_project / "sessions" / f"iter-{nm}" / aid
                          / "agent.json").read_text())
        assert rec["status"] == "running", rec["status"]
        assert rec.get("overdue_since"), "overdue_since must be set"

    inbox_a = _inbox(graph_project, "director")
    text = inbox_a.read_text()
    # ONE dm per round, both to the same stamped dispatcher, in ONE inbox.
    assert text.count("from:") == 2, "exactly one dm per overdue round"
    assert text.count("reason=overdue") == 2
    assert "iter=iter-A agent=kid-a" in text
    assert "iter=iter-B agent=kid-b" in text

    log_text = log.read_text()
    assert "marked OVERDUE" in log_text
    assert log_text.count("marked OVERDUE") == 2  # ONE log line per event
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
    """A round with NO `dispatched_by` stamp that is past deadline and has a
    live (unknown — pid 0) pid is marked OVERDUE and logs the mark; the dm is
    skipped but there is never silence."""
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

    rec = json.loads((graph_project / "sessions" / "iter-D" / "kid-d"
                      / "agent.json").read_text())
    assert rec["status"] == "running"
    assert rec.get("overdue_since"), "overdue mark set without a stamp"
    assert _manifest_status(graph_project, "D", "kid-d") == "running"
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


def test_watch_repairs_a_stranded_seat_wake_in_one_pass(
        graph_project, monkeypatch):
    """hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter:
    the watch pass calls `send.wake` for every configured live seat row, with
    no operator, so a stranded rotation-alert wake is repaired within ONE
    `--once` pass. A row with no name is skipped; `send.wake` itself is a
    read-only no-op when there is nothing to deliver, so polling every row
    is safe."""
    import send as _send
    woke = []

    def _fake_wake(root, to, tmux_session=None):
        woke.append(to)
        return True

    monkeypatch.setattr(_send, "wake", _fake_wake)
    monkeypatch.setattr(
        _send, "_locally_loaded_rows",
        lambda root: [{"name": "sanctuary-director"},
                      {"name": "sanctuary-helper"},
                      {"name": ""}])          # the "" row is skipped
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0
    assert sorted(woke) == ["sanctuary-director", "sanctuary-helper"]


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


def test_watch_alive_past_deadline_is_overdue_not_timeout_not_death(
        graph_project, monkeypatch):
    """Sibling path: pid alive at BOTH checks records an OVERDUE, never a
    death and never a terminal timeout — status stays running, overdue_since
    is set, exactly one overdue dm. The death branch must not fire when
    is_alive is true (hypothesis:l4-a-timeout-mark-on-a-live-agent-is-
    not-terminal)."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    monkeypatch.setattr(heal, "_WatcherAdapter", _AlwaysAliveAdapter)
    _round_alive_then_dead(graph_project, "J", "kid-j", timeout_s=1,
                           started_ago=5, pid=424244)
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(graph_project),
                         "--once"])
    assert heal.main() == 0

    assert _manifest_status(graph_project, "J", "kid-j") == "running"
    rec = json.loads((graph_project / "sessions" / "iter-J" / "kid-j"
                      / "agent.json").read_text())
    assert rec["status"] == "running", rec["status"]
    assert rec.get("overdue_since"), "overdue_since must be set for a live pid"
    assert rec.get("overdue_reason"), "overdue_reason must be set"
    assert "timeout_reason" not in rec, "never a terminal timeout for a live pid"
    assert "overdue_since" in _entry(graph_project, "J", "kid-j"), \
        "manifest entry carries the overdue mark"
    text = _inbox(graph_project, "director").read_text()
    assert "reason=overdue" in text
    assert "reason=death" not in text
    assert "reason=timeout" not in text
    assert "marked OVERDUE" in log.read_text()


# --- hypothesis:l4-the-manifest-mirrors-terminal-agent-status --------------
# A TERMINAL agent.json (done/failed/timeout) whose manifest entry still reads
# `running` — an agent that finished its work and exited but whose manifest was
# never updated — must have the terminal truth MIRRORED onto the manifest entry
# by a clean `_watch_round`, with exactly ONE log line and NO dm (a clean `done`
# is not an alarm). This is a MIRROR, not a reap: the id never lands in
# `marked`/`still`/`died`, and a still-running agent is left untouched.
def _mirror_round(graph: Path, name: str, agent_id: str,
                  rec_status: str, rec_extra=None) -> None:
    """A round whose agent.json is TERMINAL (rec_status) but whose manifest
    entry still says `running` — the clean-mirror gap."""
    it = graph / "sessions" / f"iter-{name}"
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({
        "timeout_seconds": 600,
        "agents": [{"id": agent_id, "status": "running",
                    "dispatched_by": "director"}],
    }, indent=2))
    adir = it / agent_id
    adir.mkdir(parents=True, exist_ok=True)
    rec = {"id": agent_id, "status": rec_status,
           "dispatched_by": "director", "finished_at": 1234567890}
    if rec_extra:
        rec.update(rec_extra)
    (adir / "agent.json").write_text(json.dumps(rec, indent=2))


def _entry(graph: Path, name: str, agent_id: str):
    m = json.loads((graph / "sessions" / f"iter-{name}" / "manifest.json")
                   .read_text())
    for e in m["agents"]:
        if e["id"] == agent_id:
            return e
    return {}


def test_watch_mirrors_a_clean_done_onto_the_manifest(graph_project, monkeypatch):
    """agent.json `done` + manifest `running` -> after one `_watch_round` pass
    the manifest entry reads `done` with `finished_at` mirrored; ONE log line,
    NO dm."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _mirror_round(graph_project, "M", "kid-m", "done")

    iter_dir = graph_project / "sessions" / "iter-M"
    heal._watch_round(graph_project, iter_dir, heal._WatcherAdapter())

    assert _entry(graph_project, "M", "kid-m")["status"] == "done"
    assert _entry(graph_project, "M", "kid-m")["finished_at"] == 1234567890
    assert not _inbox(graph_project, "director").exists(), \
        "a clean done must NOT send a dm"

    log_text = log.read_text()
    assert log_text.count("MIRRORED") == 1, "exactly ONE log line per mirror"


def test_watch_mirror_is_idempotent_no_repeat_log_or_write(graph_project,
                                                           monkeypatch):
    """A second `_watch_round` pass over an already-mirrored entry adds no new
    log line and no new write (the manifest mtime is unchanged)."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _mirror_round(graph_project, "N", "kid-n", "done")
    iter_dir = graph_project / "sessions" / "iter-N"

    heal._watch_round(graph_project, iter_dir, heal._WatcherAdapter())
    mp = graph_project / "sessions" / "iter-N" / "manifest.json"
    mtime = mp.stat().st_mtime_ns
    log_len = len(log.read_text())

    heal._watch_round(graph_project, iter_dir, heal._WatcherAdapter())

    assert mp.stat().st_mtime_ns == mtime, "no rewrite on an already-consistent entry"
    assert len(log.read_text()) == log_len, "no new log line on a second pass"
    assert log.read_text().count("MIRRORED") == 1


def test_watch_mirror_and_running_agent_untouched(graph_project, monkeypatch):
    """Inside ONE pass: a terminal done is mirrored while a still-running
    agent (agent.json `running` + manifest `running`) is left exactly as-is —
    no finished_at, entry unchanged."""
    it = graph_project / "sessions" / "iter-O"
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({
        "timeout_seconds": 600,
        "agents": [
            {"id": "done-a", "status": "running", "dispatched_by": "director"},
            {"id": "live-b", "status": "running", "dispatched_by": "director"},
        ],
    }, indent=2))
    for aid in ("done-a", "live-b"):
        (it / aid).mkdir(parents=True, exist_ok=True)
    (it / "done-a" / "agent.json").write_text(json.dumps(
        {"id": "done-a", "status": "done", "dispatched_by": "director",
         "finished_at": 999}, indent=2))
    (it / "live-b" / "agent.json").write_text(json.dumps(
        {"id": "live-b", "status": "running", "dispatched_by": "director",
         "started_at": int(time.time())}, indent=2))

    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    heal._watch_round(graph_project, it, heal._WatcherAdapter())

    assert _entry(graph_project, "O", "done-a")["status"] == "done"
    assert _entry(graph_project, "O", "live-b")["status"] == "running"
    assert _entry(graph_project, "O", "live-b").get("finished_at") is None, \
        "a live agent must not gain finished_at"
    assert "live-b" not in _entry(graph_project, "O", "done-a")


def test_watch_mirrors_failed_and_timeout_agent_json_too(graph_project,
                                                         monkeypatch):
    """The mirror branch is not done-only: a `failed` and a `timeout`
    agent.json mirror onto the manifest the same way (with fail_reason)."""
    log = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _mirror_round(graph_project, "P", "kid-p", "failed",
                  {"fail_reason": "boom"})
    _mirror_round(graph_project, "Q", "kid-q", "timeout",
                  {"timeout_reason": "past deadline"})

    for it in (graph_project / "sessions" / "iter-P",
               graph_project / "sessions" / "iter-Q"):
        heal._watch_round(graph_project, it, heal._WatcherAdapter())

    assert _entry(graph_project, "P", "kid-p")["status"] == "failed"
    assert _entry(graph_project, "P", "kid-p")["fail_reason"] == "boom"
    assert _entry(graph_project, "Q", "kid-q")["status"] == "timeout"
    assert _entry(graph_project, "Q", "kid-q")["finished_at"] == 1234567890


def test_watch_mirror_falsifier_no_terminal_behind_running(graph_project,
                                                           monkeypatch):
    """FALSIFIER: after one pass over every mirror fixture, no manifest entry
    reads `running` whose own agent.json is terminal."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    _mirror_round(graph_project, "R", "done-z", "done")
    _mirror_round(graph_project, "S", "fail-z", "failed", {"fail_reason": "x"})
    it = graph_project / "sessions" / "iter-T"
    it.mkdir(parents=True, exist_ok=True)
    (it / "manifest.json").write_text(json.dumps({
        "timeout_seconds": 600,
        "agents": [{"id": "run-z", "status": "running",
                    "dispatched_by": "director"}],
    }, indent=2))
    (it / "run-z").mkdir(parents=True, exist_ok=True)
    (it / "run-z" / "agent.json").write_text(json.dumps(
        {"id": "run-z", "status": "running"}, indent=2))

    for nm in ("R", "S", "T"):
        heal._watch_round(graph_project, graph_project / "sessions" / f"iter-{nm}",
                          heal._WatcherAdapter())

    for nm in ("R", "S"):
        e = _entry(graph_project, nm, {"R": "done-z", "S": "fail-z"}[nm])
        assert e["status"] != "running", \
            f"iter-{nm} entry must not read running after one pass"


# --------------------------------------------------------------------------
# Round SL5.09 — clause 3 of hypothesis:l4-a-rotation-alert-lands-in-the-
# inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe:
# crash-recovery `detected` records DEDUPE per death (one record per
# seating, later polls update it IN PLACE — never a fresh stamp file per
# poll). The measured defect: a still-dead-and-unrecoverable seat, re-scanned
# every ~30 s, accumulated nine `result=detected` records for one death.
# A real-rotate shim stands in so the write path and the dedupe read both use
# the genuine record format.
# --------------------------------------------------------------------------

def _rot_shim(tmp_rot, rows=None):
    """A minimal `_rotate` stand-in whose records are real rotate.py-shape
    JSON under `tmp_rot`, exercising heal's own dedupe read + the same
    `.seating.json`-style naming the real writer uses. `rows`, when given, is
    the `_load_seats` result amplified out of the shim so `_watch_one_seat`
    re-reads the seat row it needs without a real geometry seats.md."""
    import datetime as _dt
    _ROWS = rows if rows is not None else []
    _LOAD = _ROWS if callable(_ROWS) else (lambda root: _ROWS)
    class _R:
        # SL2#10 seam: `_write_crash_recovery` reads the module constant for
        # the record's `tmux_session` cell (heal.py, landed by a00-a4f9327b
        # after this shim was written) -- the shim carries it so the record
        # shape stays the real writer's; nothing under test reads the value.
        DEFAULT_TMUX_SESSION = "agi-rc"
        @staticmethod
        def _load_seats(root):
            return _LOAD(root)
        @staticmethod
        def _sessions_dir(root):
            return Path(str(root)) / "sessions"
        @staticmethod
        def _rotations_dir(root):
            return tmp_rot
        @staticmethod
        def _rotation_record_files(root, seat):
            rot = _R._rotations_dir(root)
            if not rot.is_dir():
                return []
            out = []
            for p in sorted(rot.glob(f"{seat}.*.json"), key=lambda p: p.name):
                try:
                    rec = json.loads(p.read_text(encoding="utf-8"))
                except (OSError, ValueError):
                    out.append(p)
                    continue
                if isinstance(rec, dict) and rec.get("rotation") == "crash-recovery":
                    continue
                out.append(p)
            return out
        @staticmethod
        def _latest_rotation_record(root, seat):
            files = _R._rotation_record_files(root, seat)
            if not files:
                return None
            try:
                return json.loads(files[-1].read_text(encoding="utf-8"))
            except (OSError, ValueError):
                return None
        @staticmethod
        def _write_rotation_record(root, rec, path=None):
            tmp_rot.mkdir(parents=True, exist_ok=True)
            if path is None:
                # ns suffix: distinct fresh files even within one wall-clock
                # second, isolating the DEDUPE behaviour under test.
                stamp = _dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
                stamp += f"{time.time_ns() % 10**6:06d}"
                path = tmp_rot / f"{rec['seat']}.{stamp}.json"
            path.write_text(json.dumps(rec) + "\n", encoding="utf-8")
            return path
    return _R


def test_detected_recovery_records_dedupe_one_per_death(graph_project,
                                                        tmp_path, monkeypatch):
    """A death whose recovery never lands (outcome respawned=False) is
    re-scanned by the watcher every poll; each `detected` write must update
    the SAME record file in place, never mint a fresh stamp file. Three
    polls -> exactly ONE detected record. (The nine-record defect.)"""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    shim = _rot_shim(rot)
    now = time.time()
    cells = {"name": "solo", "role": "director", "pid": 4242,
             "window": "@9", "generation": 3}
    outcome = {"respawned": False, "name": "solo", "generation": 3,
               "reason": "launcher reported no successor process"}
    try:
        for _ in range(3):
            heal._write_crash_recovery(graph_project, "solo", "dead-pid",
                                       cells, shim, now, outcome)
    finally:
        pass
    detected = [p for p in rot.glob("solo.*.json")]
    assert len(detected) == 1, \
        f"expected ONE deduped detected record, got {len(detected)}: {detected}"
    rec = json.loads(detected[0].read_text())
    assert rec["result"] == "detected"
    assert rec["rotation"] == "crash-recovery"


def test_respawned_recovery_writes_fresh_file_per_outcome(graph_project,
                                                          tmp_path,
                                                          monkeypatch):
    """A `respawned` outcome is a distinct, terminal recovery: it is NEVER
    deduped. Two respawned recoveries -> two records (the dedupe key is the
    still-open death, so it must not suppress distinct healed recoveries)."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    shim = _rot_shim(rot)
    cells = {"name": "twice", "role": "director", "pid": 1,
             "window": "@1", "generation": 1}
    outcome = {"respawned": True, "name": "twice", "generation": 2,
               "pid": 55, "window": "@2", "reason": "", "row": "ok"}
    heal._write_crash_recovery(graph_project, "twice", "boom", cells,
                               shim, time.time(), outcome)
    heal._write_crash_recovery(graph_project, "twice", "boom", cells,
                               shim, time.time(), outcome)
    files = sorted(rot.glob("twice.*.json"))
    assert len(files) == 2, f"fresh respawned record expected, got {files}"
    for p in files:
        rec = json.loads(p.read_text())
        assert rec["result"] == "respawned"


# --------------------------------------------------------------------------
# hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-rotation-record-
# before-declaring-a-crash, clauses (2)/(3): a rotation that just FINISHED
# must not read as a crash. A SUCCESS rotation record newer than the row
# (gen_after > row generation, or landed inside SEAT_DEAD_WINDOW_S while the
# row pid is dead) means the row's pid/@id belong to the RETIRED predecessor
# -- the seat ROTATED, never DEAD. No crash-recovery record, no launcher,
# {} returned. The guard is never lowered: a genuinely dead seat with no
# newer success record is still detected.
# --------------------------------------------------------------------------

SEAT_DEAD_PLUS = heal.SEAT_DEAD_WINDOW_S + 60


def _write_started_record(rot: Path, seat: str, age_s: int) -> None:
    """A real rotate.py-shape `started` rotate-self record, `age_s` old."""
    rot.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time() - age_s))
    rec = {"rotation": "rotate-self", "seat": seat, "result": "started",
           "recorded_at": time.strftime(
               "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - age_s)),
           "steps_reached": ["spawn"]}
    (rot / f"{seat}.{stamp}.json").write_text(
        json.dumps(rec, indent=2) + "\n", encoding="utf-8")


def _mk_dead_row(name: str, gen: int, pid: int = 31337,
                 window: str = "@306") -> dict:
    """A pre-rotation row: dead pid, gone window @id, dead generation.
    `recover: False` keeps the counter-falsifier assertions at the DEAD-NAMING
    seam without pulling `_recover_seat` (and its rotate shim surface) in."""
    return {"name": name, "role": "director", "model": "x", "pid": pid,
            "window": window, "session_id": "sess-1", "generation": gen,
            "recover": False}


def _write_success_record(rot: Path, seat: str, gen_before: int,
                          gen_after: int, age_s: int) -> None:
    """A real rotate.py-shape `success` rotate-self record, `age_s` old."""
    rot.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time() - age_s))
    rec = {"rotation": "rotate-self", "seat": seat, "result": "success",
           "gen_before": gen_before, "gen_after": gen_after,
           "recorded_at": time.strftime(
               "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - age_s))}
    (rot / f"{seat}.{stamp}.json").write_text(
        json.dumps(rec, indent=2) + "\n", encoding="utf-8")


def _write_success_record_nested(rot: Path, seat: str, before: int,
                                 after: int, age_s: int) -> None:
    """A `success` record in the REAL INCIDENT shape: top-level gen fields
    absent/null, generation carried ONLY nested under
    `observations.b_generation.before/after` (cf.
    sensei-director.20260912T000346Z.json)."""
    rot.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time() - age_s))
    rec = {"rotation": "rotate-self", "seat": seat, "result": "success",
           "gen_before": None, "gen_after": None,
           "observations": {"b_generation": {"before": before,
                                               "after": after}},
           "recorded_at": time.strftime(
               "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - age_s))}
    (rot / f"{seat}.{stamp}.json").write_text(
        json.dumps(rec, indent=2) + "\n", encoding="utf-8")


def _write_success_record_identity(rot: Path, seat: str, *,
                                   chain_pids, own_window, join_pid,
                                   join_window, succ_window,
                                   gen_before, gen_after, age_s) -> None:
    """A real-rotate shape `success` record carrying the identity the dead-
    seat watcher decides by: `s12_self_reap.chain[*].pid` (the RETIRED
    predecessor's process chain) plus `handover.own_window.id` (the
    predecessor's window), `handover.join.{pid,window_id}` and
    `handover.successor_window.id` (the successor the rotate-self spawned and
    joined). `age_s` old."""
    rot.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(time.time() - age_s))
    rec = {"rotation": "rotate-self", "seat": seat, "result": "success",
           "gen_before": gen_before, "gen_after": gen_after,
           "recorded_at": time.strftime(
               "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - age_s)),
           "handover": {
               "own_window": {"name": f"{seat}.genX", "id": own_window},
               "successor_window": {"name": seat, "id": succ_window},
               "join": {"found": True, "window_id": join_window,
                          "pid": join_pid}},
           "s12_self_reap": {"order": "deepest-first", "planned": True,
                              "chain": [{"pid": p, "was_alive": True,
                                           "termd": True, "gone_after": True}
                                          for p in chain_pids]}}
    (rot / f"{seat}.{stamp}.json").write_text(
        json.dumps(rec, indent=2) + "\n", encoding="utf-8")


def test_success_rotation_suppresses_false_dead(graph_project, tmp_path,
                                                monkeypatch):
    """THE falsifier: a gen-4 row with a DEAD predecessor pid and gone @306,
    plus a success record gen 4 -> 5 inside the dead window, must NOT read as
    a crash. `_watch_one_seat` returns {} -- NAMED once as rotated, NO
    crash-recovery record written, launcher NEVER invoked."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("sensei-director", gen=4)
    shim = _rot_shim(rot, rows=[row])
    _write_success_record(rot, "sensei-director", 4, 5, age_s=21)
    launched: list = []
    summary = heal._watch_one_seat(
        graph_project, row, [], shim, now=time.time(),
        pid_alive=lambda p: False, window_path=None,
        launcher=lambda *a, **k: launched.append(a) or {},
        pin_table={}, seat_sessions=[], registry_dir=None)
    assert summary == {}, f"rotated seat must return {{}}, got {summary}"
    assert launched == [], "launcher must never be called for a rotated seat"
    crash = [p for p in rot.glob("sensei-director.*.json")]
    assert len(crash) == 1, \
        f"no crash-recovery may be written for a rotated seat, got: {crash}"


def test_dead_without_newer_success_still_dead(graph_project, tmp_path,
                                               monkeypatch):
    """COUNTER-falsifier: a genuinely dead seat (dead pid, gone @id) whose
    only success record is OLDER than the window with the SAME generation as
    the row must STILL be detected as DEAD -- the guard is never lowered."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("helo", gen=4)
    shim = _rot_shim(rot, rows=[row])
    # same generation as the row, OLDER than the window -> not rotated
    _write_success_record(rot, "helo", 3, 4, age_s=SEAT_DEAD_PLUS)
    summary = heal._watch_one_seat(
        graph_project, row, [], shim, now=time.time(),
        pid_alive=lambda p: False, window_path=None,
        launcher=lambda *a, **k: {}, pin_table={}, seat_sessions=[],
        registry_dir=None)
    assert summary != {}, "a genuinely dead seat must still be DEAD"
    assert summary.get("probable_cause") is not None


def test_dead_with_no_success_record_still_dead(graph_project, tmp_path,
                                                monkeypatch):
    """COUNTER-falsifier: no success record at all -> still DEAD."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("helo2", gen=4)
    shim = _rot_shim(rot, rows=[row])
    summary = heal._watch_one_seat(
        graph_project, row, [], shim, now=time.time(),
        pid_alive=lambda p: False, window_path=None,
        launcher=lambda *a, **k: {}, pin_table={}, seat_sessions=[],
        registry_dir=None)
    assert summary != {}, "no success record -> seat is still DEAD"


def test_old_success_new_gen_still_suppresses(graph_project, tmp_path,
                                              monkeypatch):
    """A success record whose gen_after EXCEEDS the row generation still
    proves the row is the RETIRED predecessor -- but ONLY through the record's
    IDENTITY. The pred-identity arm has NO age bound, so a lagging row
    carrying the predecessor's chain pid is still rotated even an hour later,
    never DEAD. A no-identity record that old has no identity to prove
    anything and must NOT suppress (unit case `d`)."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("oldrot", gen=2, pid=9001)
    shim = _rot_shim(rot, rows=[row])
    _write_success_record_identity(rot, "oldrot", chain_pids=[9001],
                                   own_window="@9", join_pid=9002,
                                   join_window="@10", succ_window="@10",
                                   gen_before=1, gen_after=5,
                                   age_s=SEAT_DEAD_PLUS)
    summary = heal._watch_one_seat(
        graph_project, row, [], shim, now=time.time(),
        pid_alive=lambda p: False, window_path=None,
        launcher=lambda *a, **k: {}, pin_table={}, seat_sessions=[],
        registry_dir=None)
    assert summary == {}, "pred-identity suppresses even outside the window"


def test_nested_generation_record_names_4_to_5(graph_project, tmp_path,
                                               monkeypatch):
    """BUGFIX (parent a00-fcdbdec1): the REAL INCIDENT shape -- a success
    record whose gen_before/gen_after are TOP-LEVEL NULL and whose generation
    lives ONLY nested under observations.b_generation -- must both suppress
    the false DEAD ({} returned) AND name "4 -> 5", not "None -> 5". The
    `_watch_one_seat` naming branch must read BEFORE and AFTER through the
    SAME nested-aware extraction as `_success_record_rotated`."""
    reaper = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(reaper))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("sensei-director", gen=4)
    shim = _rot_shim(rot, rows=[row])
    _write_success_record_nested(rot, "sensei-director", 4, 5, age_s=21)
    launched: list = []
    summary = heal._watch_one_seat(
        graph_project, row, [], shim, now=time.time(),
        pid_alive=lambda p: False, window_path=None,
        launcher=lambda *a, **k: launched.append(a) or {},
        pin_table={}, seat_sessions=[], registry_dir=None)
    assert summary == {}, f"nested-shape rotated seat must return {{}}, got {summary}"
    assert launched == [], "launcher must never be called for a rotated seat"
    log = reaper.read_text() if reaper.exists() else ""
    assert "4 -> 5" in log, \
        f"nested-shape record must name '4 -> 5', not 'None -> 5'; reaper:\n{log}"
    assert "None -> 5" not in log, \
        f"nested-shape record must NOT name 'None -> 5'; reaper:\n{log}"


def test_rotation_before_after_extraction(tmp_path):
    """Shared extraction prefers top-level gens and falls back to the nested
    incident shape; the two agree on the real record."""
    top = {"gen_before": 4, "gen_after": 5}
    assert heal._rotation_before_after(top) == (4, 5)
    nested = {"gen_before": None, "gen_after": None,
              "observations": {"b_generation": {"before": 4,
                                                  "after": 5}}}
    assert heal._rotation_before_after(nested) == (4, 5)
    mixed = {"gen_after": 5, "gen_before": None,
             "observations": {"b_generation": {"before": 4}}}
    assert heal._rotation_before_after(mixed) == (4, 5)


def test_success_record_rotated_unit(tmp_path):
    """`_success_record_rotated` decides by the record's IDENTITY first:
    pred-identity returns the record with NO age bound; succ-dead returns
    None so the successor's death is never masked; the gen/age fallbacks
    fire ONLY for records with no identity fields and ONLY inside the
    window. Returns `(record, arm)` -- arm names the deciding proof."""
    rot = tmp_path / "rotations"
    shim = _rot_shim(rot)

    def _mk(name, gen, pid=31337, window="@306"):
        return _mk_dead_row(name, gen, pid=pid, window=window)

    # pred-identity by CHAIN PID, record an HOUR old -> rotated, no age bound
    _write_success_record_identity(rot, "a", chain_pids=[111], own_window="@5",
                                   join_pid=222, join_window="@6",
                                   succ_window="@6", gen_before=3, gen_after=4,
                                   age_s=SEAT_DEAD_PLUS)
    got, arm = heal._success_record_rotated(tmp_path, "a",
                                            _mk("a", gen=3, pid=111), shim,
                                            time.time())
    assert got is not None and arm == "pred-identity" \
        and got.get("gen_after") == 4
    # pred-identity by own WINDOW, hour-old record -> rotated
    _write_success_record_identity(rot, "aw", chain_pids=[999], own_window="@5",
                                   join_pid=222, join_window="@6",
                                   succ_window="@6", gen_before=3, gen_after=4,
                                   age_s=SEAT_DEAD_PLUS)
    got, arm = heal._success_record_rotated(tmp_path, "aw",
                                            _mk("aw", gen=3, window="@5"),
                                            shim, time.time())
    assert got is not None and arm == "pred-identity"
    # succ-dead: row IS the successor (join pid), 60 s old -> None, never masked
    _write_success_record_identity(rot, "s", chain_pids=[111], own_window="@5",
                                   join_pid=222, join_window="@6",
                                   succ_window="@6", gen_before=3, gen_after=4,
                                   age_s=60)
    got, arm = heal._success_record_rotated(tmp_path, "s",
                                            _mk("s", gen=4, pid=222), shim,
                                            time.time())
    assert got is None and arm == "succ-dead"
    # succ-dead by successor WINDOW (60 s old) -> None
    _write_success_record_identity(rot, "sw", chain_pids=[111], own_window="@5",
                                   join_pid=222, join_window="@6",
                                   succ_window="@6", gen_before=3, gen_after=4,
                                   age_s=60)
    got, arm = heal._success_record_rotated(tmp_path, "sw",
                                            _mk("sw", gen=4, window="@6"),
                                            shim, time.time())
    assert got is None and arm == "succ-dead"
    # identity record matching NEITHER -> None (guard never lowered)
    _write_success_record_identity(rot, "u", chain_pids=[111], own_window="@5",
                                   join_pid=222, join_window="@6",
                                   succ_window="@6", gen_before=3, gen_after=4,
                                   age_s=21)
    got, arm = heal._success_record_rotated(tmp_path, "u",
                                            _mk("u", gen=4, pid=777), shim,
                                            time.time())
    assert got is None and arm is None
    # NO identity -> gen-fallback INSIDE the window (gen_after > row gen)
    _write_success_record(rot, "g", 4, 5, age_s=21)
    got, arm = heal._success_record_rotated(tmp_path, "g",
                                            _mk("g", gen=4), shim,
                                            time.time())
    assert got is not None and arm == "gen-fallback"
    # NO identity -> age-fallback INSIDE the window (any/same generation)
    _write_success_record(rot, "b", 4, 4, age_s=21)
    got, arm = heal._success_record_rotated(tmp_path, "b",
                                            _mk("b", gen=4), shim,
                                            time.time())
    assert got is not None and arm == "age-fallback"
    # NO identity, OLDER than window -> None even when gen_after > row gen
    _write_success_record(rot, "d", 3, 4, age_s=SEAT_DEAD_PLUS)
    got, arm = heal._success_record_rotated(tmp_path, "d",
                                            _mk("d", gen=4), shim,
                                            time.time())
    assert got is None and arm is None
    # a `started` record is never a success -> None
    _write_started_record(rot, "c", age_s=21)
    got, arm = heal._success_record_rotated(tmp_path, "c",
                                            _mk("c", gen=4), shim,
                                            time.time())
    assert got is None and arm is None
    # a record MISSING handover / s12_self_reap never raises (fallback path)
    _write_success_record(rot, "e", 4, 5, age_s=21)
    got, arm = heal._success_record_rotated(tmp_path, "e",
                                            _mk("e", gen=4), shim,
                                            time.time())
    assert got is not None and arm == "gen-fallback"


def test_rotation_in_flight_honours_success(graph_project, tmp_path):
    """Clause (3): `_rotation_in_flight` honours a SUCCESS rotation record as
    a rotation in flight (the seat already rotated), shared helper."""
    rot = tmp_path / "rotations"
    row = _mk_dead_row("flightsucc", gen=4)
    shim = _rot_shim(rot, rows=[row])
    _write_success_record(rot, "flightsucc", 4, 5, age_s=21)
    assert heal._rotation_in_flight(graph_project, "flightsucc", shim,
                                    time.time(), row=row) is True


def test_live_seat_row_takes_identity_from_main(monkeypatch, tmp_path):
    """Clause (1): `_live_seat_row` takes the IDENTITY cells (generation /
    pid etc.) from the MAIN checkout's copy, keeping non-identity cells
    live-first. Two geometry dirs that DIFFER: the worktree copy says gen 4,
    MAIN says gen 5 -- the row reads gen 5 (the ONE writer's file)."""
    main_dir = tmp_path / "main"
    wt_dir = tmp_path / "wt"
    wt_dir.mkdir(parents=True, exist_ok=True)
    main_dir.mkdir(parents=True, exist_ok=True)
    def _rows(root):
        if str(root) == str(main_dir):
            return [{"name": "dir", "generation": 5, "role": "director",
                     "session_ref": "main-sess"}]
        return [{"name": "dir", "generation": 4, "role": "director"}]
    shim = _rot_shim(tmp_path / "rotations", rows=_rows)
    monkeypatch.setattr(heal, "_main_graph_root", lambda gdir: main_dir)
    row = heal._live_seat_row(wt_dir, "dir", shim)
    assert row["generation"] == 5, \
        "IDENTITY cells must come from MAIN, not the worktree copy"


# --------------------------------------------------------------------------
# hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-never-
# by-gen-order-or-age (goal:g15.23 fix-only #4): the dead-seat watcher proves
# a rotation by the record's IDENTITY fields (predecessor chain pid / own
# window; successor join pid / successor window), never by gen ordering or
# record age alone. FALSIFIERS below.
# --------------------------------------------------------------------------

def test_successor_pid_dead_never_masked(graph_project, tmp_path, monkeypatch):
    """FALSE-preventer (the SL2.11 P2 residue): a seat that ROTATED cleanly
    and whose SUCCESSOR then died must be detected DEAD, not masked by the
    600 s window. A row carrying the record's SUCCESSOR pid -- dead, with a
    60 s old success record -- must STILL read DEAD (the record's succ-dead
    arm returns None; the 600 s window never masks the successor's death)."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("sensei-director", gen=5, pid=222)
    shim = _rot_shim(rot, rows=[row])
    _write_success_record_identity(rot, "sensei-director", chain_pids=[111],
                                   own_window="@5", join_pid=222,
                                   join_window="@6", succ_window="@6",
                                   gen_before=4, gen_after=5, age_s=60)
    summary = heal._watch_one_seat(
        graph_project, row, [], shim, now=time.time(),
        pid_alive=lambda p: False, window_path=None,
        launcher=lambda *a, **k: {}, pin_table={}, seat_sessions=[],
        registry_dir=None)
    assert summary != {}, \
        "successor death must NOT be masked by the 600 s window"
    assert summary.get("probable_cause") is not None


def test_successor_window_dead_never_masked(graph_project, tmp_path,
                                            monkeypatch):
    """Same false-preventer by WINDOW: a dead successor row carrying the
    record's successor window @id reads DEAD even with a 60 s old success
    record (succ-dead arm)."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("sensei-director", gen=5, window="@6")
    shim = _rot_shim(rot, rows=[row])
    _write_success_record_identity(rot, "sensei-director", chain_pids=[111],
                                   own_window="@5", join_pid=222,
                                   join_window="@6", succ_window="@6",
                                   gen_before=4, gen_after=5, age_s=60)
    summary = heal._watch_one_seat(
        graph_project, row, [], shim, now=time.time(),
        pid_alive=lambda p: False, window_path=None,
        launcher=lambda *a, **k: {}, pin_table={}, seat_sessions=[],
        registry_dir=None)
    assert summary != {}, \
        "successor-window death must NOT be masked by the 600 s window"
    assert summary.get("probable_cause") is not None


def test_lagging_chain_pid_row_still_rotated(graph_project, tmp_path,
                                             monkeypatch):
    """THE lagging-row protect: a stale row still carrying the RETIRED
    predecessor's chain pid, with a record AN HOUR OLD, must read ROTATED
    (pred-identity arm has NO age bound -- a lagging row is exactly what it
    protects), never DEAD."""
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph_project / "reaper.log"))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("sensei-director", gen=4, pid=111)
    shim = _rot_shim(rot, rows=[row])
    _write_success_record_identity(rot, "sensei-director", chain_pids=[111],
                                   own_window="@5", join_pid=222,
                                   join_window="@6", succ_window="@6",
                                   gen_before=3, gen_after=4,
                                   age_s=SEAT_DEAD_PLUS)
    launched: list = []
    summary = heal._watch_one_seat(
        graph_project, row, [], shim, now=time.time(),
        pid_alive=lambda p: False, window_path=None,
        launcher=lambda *a, **k: launched.append(a) or {},
        pin_table={}, seat_sessions=[], registry_dir=None)
    assert summary == {}, \
        "a lagging predecessor chain-pid row must read ROTATED, not DEAD"
    assert launched == []


def test_watch_log_names_deciding_arm(graph_project, tmp_path, monkeypatch):
    """Clause (4): the `rotated seat` reaper line names the DECIDING ARM
    (`arm=pred-identity|gen-fallback|age-fallback`), one word, so a reaper log
    reads which proof was used."""
    reaper = graph_project / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(reaper))
    rot = tmp_path / "rotations"
    row = _mk_dead_row("sensei-director", gen=4, pid=111)
    shim = _rot_shim(rot, rows=[row])
    _write_success_record_identity(rot, "sensei-director", chain_pids=[111],
                                   own_window="@5", join_pid=222,
                                   join_window="@6", succ_window="@6",
                                   gen_before=3, gen_after=4, age_s=21)
    heal._watch_one_seat(graph_project, row, [], shim, now=time.time(),
                         pid_alive=lambda p: False, window_path=None,
                         launcher=lambda *a, **k: {}, pin_table={},
                         seat_sessions=[], registry_dir=None)
    log = reaper.read_text() if reaper.exists() else ""
    assert "arm=pred-identity" in log, \
        f"rotate-seat line must name arm=pred-identity; reaper:\n{log}"
