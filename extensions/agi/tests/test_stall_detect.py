"""Tests for extensions/agi/bin/stall_detect.py — DETECTION ONLY, no repair.

**hypothesis:l4-stalled-is-a-state-the-harness-can-see.** Proven here:
  (a) the four-condition fixture (all kids terminal, record `running` with an
      mtime unchanged since spawn, uncommitted worktree, age past T) is
      detected as `stalled`;
  (b) one fixture per missing condition is NOT stalled — because a detector
      that fires on three of four is a false-alarm generator, and a false
      alarm on an agent's liveness teaches the operator to ignore the signal;
  (c) `stalled` is absent from `spawn_budget.TERMINAL` (a stalled parent is
      still alive and still holds its lease);
  (d) detection and recording never kill, restart or commit — asserted on the
      absence of the action, not the presence of the label.

No existing test was edited. `stall_detect.py` never touches the reaper's
commit-based completion check.
"""
from __future__ import annotations

import json
import os
import sys
import time

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO_ROOT, "extensions", "agi", "bin"))
import stall_detect  # noqa: E402
from spawn_budget import TERMINAL  # noqa: E402


def _detect(**over):
    """detect_stalled with the all-four-true default; flip one to test it."""
    args = dict(
        kids_terminal=True,
        record_status="running",
        record_mtime_unchanged=True,
        worktree_has_uncommitted=True,
        age_s=stall_detect.STALL_THRESHOLD_S + 60,
        threshold_s=stall_detect.STALL_THRESHOLD_S,
    )
    args.update(over)
    return stall_detect.detect_stalled(**args)


def _write_agent(itdir, agent_id, status="done", started_at=None):
    itdir = itdir / agent_id
    itdir.mkdir(parents=True, exist_ok=True)
    started_at = started_at if started_at is not None else int(time.time()) - 1000
    rec = {"id": agent_id, "status": status, "started_at": started_at,
           "pid": 999999, "worktree": str(itdir / "wt")}
    aj = itdir / "agent.json"
    aj.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    os.utime(aj, (started_at, started_at))
    return aj, itdir / "wt"


class TestFourConditions:
    def test_all_four_conditions_stalled(self):
        assert _detect() is True

    def test_live_kid_not_stalled(self):
        assert _detect(kids_terminal=False) is False

    def test_terminal_record_not_stalled(self):
        assert _detect(record_status="done") is False
        assert _detect(record_status="failed") is False

    def test_moved_mtime_not_stalled(self):
        assert _detect(record_mtime_unchanged=False) is False

    def test_clean_worktree_not_stalled(self):
        assert _detect(worktree_has_uncommitted=False) is False

    def test_young_not_stalled(self):
        # merely slow, under T -> not stalled
        assert _detect(age_s=stall_detect.STALL_THRESHOLD_S - 60) is False


class TestTerminalSet:
    def test_stalled_not_in_terminal(self):
        assert "stalled" not in TERMINAL


class TestNoSideEffects:
    def test_detect_returns_bool_writes_nothing(self, tmp_path):
        # detection on a real record must not alter the record on disk
        itdir = tmp_path / "iter-x"
        aj, _ = _write_agent(itdir, "parent", status="running",
                             started_at=int(time.time()) - 10000)
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x", "agents": [{"id": "parent", "status": "running"}]
        }, indent=2))
        before = aj.read_text(encoding="utf-8")
        parents = stall_detect.scan_iteration(
            itdir, threshold_s=5, now=time.time(),
            worktree_dirty=lambda rec, itdir: True)
        assert parents == ["parent"]
        assert aj.read_text(encoding="utf-8") == before  # read-only scan

    def test_note_stalled_never_kills_or_commits(self, tmp_path):
        # recording stamps the label; nothing is killed, restarted or
        # committed — the pid is untouched, no git ran, no process spawned.
        itdir = tmp_path / "iter-x"
        aj, _ = _write_agent(itdir, "parent", status="running",
                             started_at=int(time.time()) - 10000)
        stall_detect.note_stalled(aj)
        rec = json.loads(aj.read_text(encoding="utf-8"))
        assert rec["status"] == "stalled"
        assert "stalled_at" in rec
        assert rec["pid"] == 999999            # not killed
        assert rec["started_at"] == rec.get("started_at")  # identity kept

        # idempotent: a second call changes nothing
        stamp = rec["stalled_at"]
        stall_detect.note_stalled(aj)
        rec2 = json.loads(aj.read_text(encoding="utf-8"))
        assert rec2["status"] == "stalled"
        assert rec2["stalled_at"] == stamp


class TestScanIteration:
    def _cohort(self, tmp_path, kid_statuses):
        itdir = tmp_path / "iter-x"
        parent_started = int(time.time()) - 10000
        _write_agent(itdir, "parent", status="running", started_at=parent_started)
        for i, st in enumerate(kid_statuses):
            _write_agent(itdir, f"kid{i}", status=st,
                         started_at=parent_started)
        manifest = {
            "iter": "x",
            "agents": [
                {"id": "parent", "status": "running"},
                *[{"id": f"kid{i}", "status": st}
                  for i, st in enumerate(kid_statuses)],
            ],
        }
        (itdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
        return itdir

    def test_stalled_parent_detected(self, tmp_path):
        itdir = self._cohort(tmp_path, ["done", "failed"])  # both terminal
        assert stall_detect.scan_iteration(
            itdir, threshold_s=5, now=time.time(),
            worktree_dirty=lambda rec, itdir: True) == ["parent"]

    def test_live_kid_means_none_stalled(self, tmp_path):
        itdir = self._cohort(tmp_path, ["done", "running"])  # one live kid
        assert stall_detect.scan_iteration(
            itdir, threshold_s=5, now=time.time(),
            worktree_dirty=lambda rec, itdir: True) == []

    def test_young_parent_not_stalled(self, tmp_path):
        itdir = self._cohort(tmp_path, ["done"])  # kids terminal
        # parent is young (threshold not passed) -> not stalled
        parent_rec = json.loads(
            (itdir / "parent" / "agent.json").read_text(encoding="utf-8"))
        parent_rec["started_at"] = int(time.time()) - 2
        (itdir / "parent" / "agent.json").write_text(
            json.dumps(parent_rec, indent=2), encoding="utf-8")
        assert stall_detect.scan_iteration(
            itdir, threshold_s=5, now=time.time(),
            worktree_dirty=lambda rec, itdir: True) == []


class TestRecordMtime:
    def test_mtime_unchanged_true(self, tmp_path):
        aj, _ = _write_agent(tmp_path, "a", status="running",
                             started_at=int(time.time()) - 10000)
        assert stall_detect.record_mtime_unchanged(aj, int(time.time()) - 10000) is True

    def test_mtime_moved_false(self, tmp_path):
        aj, _ = _write_agent(tmp_path, "a", status="running",
                             started_at=int(time.time()) - 10000)
        # touch the record (as a late `done` write would)
        os.utime(aj, (time.time(), time.time()))
        assert stall_detect.record_mtime_unchanged(aj, int(time.time()) - 10000) is False


class TestWiringHook:
    """The harvest-path hook: `record_stalled_in_iteration` = scan + stamp.

    Measures the intent of the dispatch wiring without running the reaper
    loop: the hook is the exact call the reaper makes each pass, so a fixture
    iter dir shaped like the L4.65/L4.70 case must end with the parent's live
    record bearing `status: stalled`, a healthy or young parent must be left
    untouched, and `stalled` must remain absent from `TERMINAL`.
    """

    def test_hook_fires_and_stamps_record(self, tmp_path):
        # four-condition parent (kids terminal, dirty worktree, past T) -> the
        # hook fires once and stamps the live record, leaving identity whole.
        itdir = tmp_path / "iter-x"
        aj, _ = _write_agent(itdir, "parent", status="running",
                             started_at=int(time.time()) - 10000)
        _write_agent(itdir, "kid0", status="done")
        _write_agent(itdir, "kid1", status="failed")
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x",
            "agents": [
                {"id": "parent", "status": "running"},
                {"id": "kid0", "status": "done"},
                {"id": "kid1", "status": "failed"},
            ],
        }, indent=2))
        stamped = stall_detect.record_stalled_in_iteration(
            itdir, threshold_s=5, now=time.time(),
            worktree_dirty=lambda rec, itdir: True)
        assert stamped == ["parent"]
        rec = json.loads(aj.read_text(encoding="utf-8"))
        assert rec["status"] == "stalled"
        assert "stalled_at" in rec
        assert rec["pid"] == 999999            # alive, not killed
        assert rec["id"] == "parent"          # identity intact

    def test_hook_noop_on_healthy_parent(self, tmp_path):
        # one live kid -> parent is not stalled; the hook scans, stamps
        # nothing, and leaves every record untouched.
        itdir = tmp_path / "iter-x"
        aj, _ = _write_agent(itdir, "parent", status="running",
                             started_at=int(time.time()) - 10000)
        _write_agent(itdir, "kid0", status="running")  # live kid
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x",
            "agents": [
                {"id": "parent", "status": "running"},
                {"id": "kid0", "status": "running"},
            ],
        }, indent=2))
        stamped = stall_detect.record_stalled_in_iteration(
            itdir, threshold_s=5, now=time.time(),
            worktree_dirty=lambda rec, itdir: True)
        assert stamped == []
        rec = json.loads(aj.read_text(encoding="utf-8"))
        assert rec["status"] == "running"      # untouched
        assert "stalled_at" not in rec

    def test_hook_noop_on_young_parent(self, tmp_path):
        # kids terminal but the parent is younger than T -> merely slow, so
        # the hook must not brand it stalled.
        itdir = tmp_path / "iter-x"
        aj, _ = _write_agent(itdir, "parent", status="running",
                             started_at=int(time.time()) - 2)  # young
        _write_agent(itdir, "kid0", status="done")
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x",
            "agents": [
                {"id": "parent", "status": "running"},
                {"id": "kid0", "status": "done"},
            ],
        }, indent=2))
        stamped = stall_detect.record_stalled_in_iteration(
            itdir, threshold_s=300, now=time.time(),
            worktree_dirty=lambda rec, itdir: True)
        assert stamped == []
        rec = json.loads(aj.read_text(encoding="utf-8"))
        assert rec["status"] == "running"

    def test_hook_keeps_stalled_out_of_terminal(self):
        # wiring must never let a recorded stalled parent join TERMINAL;
        # spawn_budget still leases it.
        assert "stalled" not in TERMINAL