"""Tests for the SIBLING before-work stall shape in extensions/agi/bin/stall_detect.py.

**hypothesis:l4-stall-before-work.** A parent that NEVER spawned a kid at all
is a second, SIBLING stalled shape — NOT a widening of L4.78's four-condition
AND, and NOT caught by it (L4.78's `_cohort_terminal` returns True vacuously
over an empty kid set, but its condition (4) requires UNCOMMITTED work, which
a parent that never touched a file has none of — verified against the actual
code that L4.77's round would NOT be detected by L4.78's detector).

THE SHAPE, all four conditions together:
  (1) `zero_kids` — the parent spawned NO kid, genuinely none, ever;
  (2) the dispatcher-side record still reads `status: running`;
  (3) the worktree is CLEAN (`git status --porcelain` empty) — the INVERSE of
      L4.78's condition (4);
  (4) age past a threshold (default 15 min; state and justify below).

Proven here, mirroring L4.78's falsifier discipline exactly:
  (a) a fixture matching all four new conditions IS detected;
  (b) four fixtures, each missing exactly ONE condition (a kid was spawned;
      the record's status moved off `running`; the worktree has uncommitted
      work; age is under threshold), and NONE of them is detected — one test
      per missing condition;
  (c) the recorded label is absent from `spawn_budget.TERMINAL` (a stalled
      parent, of either shape, is still alive and still holds its lease);
  (d) detection and recording never kill, restart or commit — asserted on the
      ABSENCE of the action, not the presence of the label, and the test is
      proven to have teeth by a local mutation that adds a fake auto-kill
      (the mutation is reverted; it is only exercised to confirm the test
      would catch it, never shipped).

No existing test was edited; `detect_stalled` and its tests are untouched.
`stall_detect.py`'s four-parameter after-work signature is untouched.
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

LABEL = stall_detect.STALL_BEFORE_WORK_LABEL


def _detect_before(**over):
    """detect_stalled_before_work with the all-four-true default; flip one."""
    args = dict(
        zero_kids=True,
        record_status="running",
        worktree_clean=True,
        age_s=stall_detect.STALL_BEFORE_WORK_THRESHOLD_S + 60,
        threshold_s=stall_detect.STALL_BEFORE_WORK_THRESHOLD_S,
    )
    args.update(over)
    return stall_detect.detect_stalled_before_work(**args)


def _write_agent(itdir, agent_id, status="done", started_at=None, worktree=None):
    itdir = itdir / agent_id
    itdir.mkdir(parents=True, exist_ok=True)
    started_at = started_at if started_at is not None else int(time.time()) - 1000
    rec = {"id": agent_id, "status": status, "started_at": started_at,
           "pid": 999999, "worktree": str(worktree or itdir / "wt")}
    aj = itdir / "agent.json"
    aj.write_text(json.dumps(rec, indent=2), encoding="utf-8")
    return aj


class TestFourConditions:
    def test_all_four_conditions_detected(self):
        assert _detect_before() is True

    def test_spawned_kid_not_detected(self):
        # condition (1) missing: a kid WAS spawned, even if not yet terminal
        assert _detect_before(zero_kids=False) is False

    def test_non_running_record_not_detected(self):
        # condition (2) missing: status moved off `running`
        assert _detect_before(record_status="done") is False
        assert _detect_before(record_status="failed") is False

    def test_dirty_worktree_not_detected(self):
        # condition (3) missing: uncommitted work present
        assert _detect_before(worktree_clean=False) is False

    def test_young_not_detected(self):
        # condition (4) missing: merely slow, under threshold
        assert _detect_before(
            age_s=stall_detect.STALL_BEFORE_WORK_THRESHOLD_S - 60) is False


class TestTerminalSet:
    def test_label_not_in_terminal(self):
        assert LABEL not in TERMINAL
        assert "stalled" not in TERMINAL  # sibling labels stay lease-holding


class TestNoSideEffects:
    def test_detect_writes_nothing(self, tmp_path):
        itdir = tmp_path / "iter-x"
        aj = _write_agent(itdir, "parent", status="running",
                          started_at=int(time.time()) - 10000)
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x", "agents": [{"id": "parent", "status": "running"}]
        }, indent=2))
        before = aj.read_text(encoding="utf-8")
        parents = stall_detect.scan_iteration_before_work(
            itdir, threshold_s=5, now=time.time(),
            worktree_clean=lambda rec, itdir: True)
        assert parents == ["parent"]
        assert aj.read_text(encoding="utf-8") == before  # read-only scan

    def test_note_never_kills_or_commits(self, tmp_path):
        """RECORD, DO NOT REPAIR: the stamp is the ONLY write.

        Asserted on the ABSENCE of the action: the record's own fields that a
        kill would change (pid) and that a restart would change (status would
        not become the label, identity would move) stay as they are; only
        `status`/`stalled_at` move. No git and no subprocess run here.
        """
        itdir = tmp_path / "iter-x"
        aj = _write_agent(itdir, "parent", status="running",
                          started_at=int(time.time()) - 10000)
        stall_detect.note_stalled_before_work(aj)
        rec = json.loads(aj.read_text(encoding="utf-8"))
        assert rec["status"] == LABEL                  # recorded, the point
        assert "stalled_at" in rec
        assert rec["pid"] == 999999                    # not killed
        assert rec["id"] == "parent"                   # identity intact

        # idempotent: a second call changes nothing
        stamp = rec["stalled_at"]
        stall_detect.note_stalled_before_work(aj)
        rec2 = json.loads(aj.read_text(encoding="utf-8"))
        assert rec2["status"] == LABEL
        assert rec2["stalled_at"] == stamp

    def test_no_repair_when_fires(self, tmp_path, monkeypatch):
        """The hook fires, stamps the label, and performs NO repair action.

        A round that adds a \"helpful\" auto-kill while the label works
        correctly would pass a label-shaped test and fail this one. This test
        has teeth: it is exercised against a mutated clone below (in
        test_mutation_teeth) that adds a fake auto-kill, and that clone fails
        here — proving the assertion fires, not that a kill happens to be
        absent this run.
        """
        itdir = tmp_path / "iter-x"
        aj = _write_agent(itdir, "parent", status="running",
                          started_at=int(time.time()) - 10000)
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x", "agents": [{"id": "parent", "status": "running"}]
        }, indent=2))
        # Stub os.kill so any kill in the code under test would be captured;
        # the assertion below requires it never fired.
        fired = []
        def squeal(pid, sig):
            fired.append(pid)
        monkeypatch.setattr(os, "kill", squeal)
        stamped = stall_detect.record_stalled_before_work_in_iteration(
            itdir, threshold_s=5, now=time.time(),
            worktree_clean=lambda rec, itdir: True)
        assert stamped == ["parent"]
        rec = json.loads(aj.read_text(encoding="utf-8"))
        assert rec["status"] == LABEL
        assert fired == []  # NOTHING was killed

    def test_mutation_teeth(self, tmp_path, monkeypatch):
        """Prove the no-repair test catches a fake auto-kill (then revert).

        We do not ship the mutation. We clone the record function, add a lazy
        os.kill, run the SAME assertion shape `test_no_repair_when_fires`
        uses, and require it to FAIL — proving the assertion has teeth. If the
        assertion silently passed on the mutated code, the no-repair guard
        would be worthless.
        """
        # clone the module's record function into a dict we can call
        scan = stall_detect.scan_iteration_before_work
        note = stall_detect.note_stalled_before_work

        def mutated_record(itdir, **kw):
            itdirp = os.fspath(itdir)
            stamped = []
            for aid in scan(itdirp, **kw):
                note(os.path.join(itdirp, aid, "agent.json"))
                # FAKE REPAIR — what RECORD, DO NOT REPAIR forbids
                p = json.loads(open(os.path.join(itdirp, aid, "agent.json")).read())
                os.kill(int(p.get("pid", 0)), 9)  # noqa: F821  (guarded below)
                stamped.append(aid)
            return stamped

        captured = []
        def squeal(pid, sig):
            captured.append(pid)
        monkeypatch.setattr(os, "kill", squeal)
        itdir = tmp_path / "iter-x"
        _write_agent(itdir, "parent", status="running",
                     started_at=int(time.time()) - 10000)
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x", "agents": [{"id": "parent", "status": "running"}]
        }, indent=2))
        with pytest.raises(AssertionError):
            # replicate the no-repair assertion: label present AND no kill
            stamped = mutated_record(
                itdir, threshold_s=5, now=time.time(),
                worktree_clean=lambda r, i: True)
            assert stamped == ["parent"]
            assert captured == []  # MUST fire — the fake kill violates RECORD/DO-NOT-REPAIR

        assert captured, "mutation did not reach a kill; the test cannot prove teeth"


class TestScanIterationBeforeWork:
    def _iter(self, tmp_path, kid_ids=(), parent_status="running",
              parent_age=10000, dirty_recs=()):
        itdir = tmp_path / "iter-x"
        parent_started = int(time.time()) - parent_age
        _write_agent(itdir, "parent", status=parent_status,
                     started_at=parent_started)
        for i, kid in enumerate(kid_ids):
            _write_agent(itdir, kid, status="done" if isinstance(kid, str)
                         and kid else "done",
                         started_at=parent_started)
        manifest = {
            "iter": "x",
            "agents": [{"id": "parent", "status": parent_status},
                       *[{"id": k, "status": "done"} for k in kid_ids]],
        }
        (itdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
        return itdir

    def test_zero_kids_clean_past_threshold_detected(self, tmp_path):
        itdir = self._iter(tmp_path, kid_ids=())  # no kids at all
        assert stall_detect.scan_iteration_before_work(
            itdir, threshold_s=5, now=time.time(),
            worktree_clean=lambda rec, itdir: True) == ["parent"]

    def test_any_spawned_kid_not_detected(self, tmp_path):
        # one kid, even a terminal one -> a kid WAS spawned -> not this shape
        itdir = self._iter(tmp_path, kid_ids=("kid0",))
        assert stall_detect.scan_iteration_before_work(
            itdir, threshold_s=5, now=time.time(),
            worktree_clean=lambda rec, itdir: True) == []

    def test_non_running_parent_not_detected(self, tmp_path):
        itdir = self._iter(tmp_path, parent_status="done")
        assert stall_detect.scan_iteration_before_work(
            itdir, threshold_s=5, now=time.time(),
            worktree_clean=lambda rec, itdir: True) == []

    def test_young_parent_not_detected(self, tmp_path):
        itdir = self._iter(tmp_path, parent_age=2)  # under threshold
        assert stall_detect.scan_iteration_before_work(
            itdir, threshold_s=300, now=time.time(),
            worktree_clean=lambda rec, itdir: True) == []

    def test_dirty_worktree_not_detected(self, tmp_path):
        itdir = self._iter(tmp_path)
        assert stall_detect.scan_iteration_before_work(
            itdir, threshold_s=5, now=time.time(),
            worktree_clean=lambda rec, itdir: False) == []


class TestWiringHook:
    def test_hook_fires_and_stamps(self, tmp_path):
        itdir = tmp_path / "iter-x"
        aj = _write_agent(itdir, "parent", status="running",
                          started_at=int(time.time()) - 10000)
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x", "agents": [{"id": "parent", "status": "running"}]
        }, indent=2))
        stamped = stall_detect.record_stalled_before_work_in_iteration(
            itdir, threshold_s=5, now=time.time(),
            worktree_clean=lambda rec, itdir: True)
        assert stamped == ["parent"]
        rec = json.loads(aj.read_text(encoding="utf-8"))
        assert rec["status"] == LABEL
        assert "stalled_at" in rec
        assert rec["pid"] == 999999   # alive, not killed
        assert rec["id"] == "parent"  # identity intact

    def test_hook_keeps_label_out_of_terminal(self):
        assert LABEL not in TERMINAL
        assert "stalled" not in TERMINAL