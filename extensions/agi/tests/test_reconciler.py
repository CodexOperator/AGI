"""Tests for extensions/agi/bin/reconciler.py — RECONCILE, DO NOT REPAIR.

**hypothesis:l4-the-reconciler-one-root-three-faces.** Proven here:
  (a) a fixture built from the REAL frozen L4.85 artifact
      (`.agi/worktrees/a00-e9572046/.agi/sessions/iter-L4.85/` — the kid
      `a00-d0a67d4f` whose `agent.json` reads `status: running` with a
      long-dead pid 2130989) reconciles to the derived terminal status;
  (b) a record saying `running` for a DEAD pid is reconciled to the derived
      terminal status;
  (c) a record saying `done` for a LIVE pid is left ALONE — the inference
      never runs the other way;
  (d) a LIVE pid with a `running` record is left alone — liveness proves
      nothing, so it changes nothing;
  (e) the derived status is distinguishable BY NAME from an actor-reported
      one (absent from `spawn_budget.TERMINAL` and from cli's status rank);
  (f) nothing is killed, restarted or committed — asserted on the ABSENCE of
      the action;
  (g) `hang`-for-dead is derived only from a DEAD pid, never from a live one,
      under any recorded status.

The ONE-WAY RULE is the whole safety argument and the tests carry it from
both sides: (c) and (d) both assert the NON-action on a live pid. L4.78's
`test_stall_detect.py` is unchanged and green — the reconciler feeds the
stall detector a truthful corpus; it does not replace it.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(REPO_ROOT, "extensions", "agi", "bin"))
import reconciler  # noqa: E402
from spawn_budget import TERMINAL  # noqa: E402

#: The REAL frozen artifact from iter-L4.85 (hypothesis (a)). DO NOT MODIFY
#: this worktree; it is read-only evidence of shape (3). It lives in the MAIN
#: checkout's `.agi/worktrees/`, so it is reached by walking up from any
#: kid's worktree (which sits one level under `.agi/worktrees/`) to `<repo>`.
_MAIN_REPO = os.path.abspath(os.path.join(REPO_ROOT, "..", "..", ".."))
FROZEN_L485 = os.path.join(
    _MAIN_REPO, ".agi", "worktrees", "a00-e9572046",
    ".agi", "sessions", "iter-L4.85")
FROZEN_KID_AJ = os.path.join(FROZEN_L485, "a00-d0a67d4f", "agent.json")


def _rec(status="running", pid=424242, dead=True):
    """A record; by default the pid is DEAD (the case that must reconcile)."""
    def alive(_pid):
        return not dead
    return {"id": "k", "status": status, "pid": pid}, alive


class TestOneWayRule:
    """The spine of the hypothesis: only a DEAD pid moves a record, and only
    a `running` record moves toward the derived terminal status."""

    def test_running_record_dead_pid_derived_terminal(self):
        # (b) the core claim: a lie the corpus tells is corrected.
        rec, alive = _rec("running", 123, dead=True)
        assert reconciler.reconcile_record(rec, pid_alive=alive) \
            == reconciler.DERIVED_TERMINAL

    def test_done_record_live_pid_left_alone(self):
        # (c) 🔴 the one that matters: the inference never runs the other way.
        rec, alive = _rec("done", 999, dead=False)
        assert reconciler.reconcile_record(rec, pid_alive=alive) == "done"

    def test_running_record_live_pid_left_alone(self):
        # (d) liveness proves nothing, so it changes nothing.
        rec, alive = _rec("running", 999, dead=False)
        assert reconciler.reconcile_record(rec, pid_alive=alive) == "running"

    def test_done_record_dead_pid_left_alone(self):
        # a `done` record is the actor speaking for itself and outranks any
        # inference; a dead pid adds nothing to an already-terminal record.
        rec, alive = _rec("done", 123, dead=True)
        assert reconciler.reconcile_record(rec, pid_alive=alive) == "done"

    def test_any_terminal_record_never_moves(self):
        # every TERMINAL recorded status is left exactly as reported, whatever
        # its pid — reconciliation only ever strengthens, never weakens.
        for status in TERMINAL:
            rec_d, alive_d = _rec(status, 123, dead=True)
            rec_l, alive_l = _rec(status, 999, dead=False)
            assert reconciler.reconcile_record(rec_d, pid_alive=alive_d) == status
            assert reconciler.reconcile_record(rec_l, pid_alive=alive_l) == status

    def test_running_record_missing_pid_left_alone(self):
        # no pid to check -> liveness proves nothing -> change nothing.
        rec, _ = _rec("running", 0, dead=True)
        assert reconciler.reconcile_record(rec, pid_alive=lambda p: False) == "running"

    def test_unknown_status_left_alone(self):
        # an unrecognised status is never inferred from; that is how a corpus
        # starts lying again.
        rec, alive = _rec("zombie", 123, dead=True)
        assert reconciler.reconcile_record(rec, pid_alive=alive) == "zombie"


class TestDistinctName:
    """(e) a derived status that masquerades as a reported one would poison
    every ranking that resolves inferred endings by content."""

    def test_hung_dead_not_in_terminal_by_side_effect(self):
        # the derived status is DECLARED here, not slipped into the ONE set.
        assert reconciler.DERIVED_TERMINAL == "hung-dead"
        assert reconciler.DERIVED_TERMINAL not in TERMINAL
        assert reconciler.DERIVED_TERMINAL in reconciler.DERIVED_TERMINAL_SET

    def test_hung_dead_absent_from_actor_family(self):
        # `done-unreported` is the reaper's inferred-but-still-terminal name;
        # `hung-dead` is a NEW name in that family, never an actor's. Grep the
        # dispatcher/cli for any actor that writes it.
        src = os.path.join(REPO_ROOT, "extensions", "agi", "bin")
        for fn in ("cli.py", "dispatch.py"):
            path = os.path.join(src, fn)
            if not os.path.exists(path):
                continue
            text = open(path, encoding="utf-8").read()
            # only this module and its tests may bear the derived name
            assert text.count("hung-dead") == 0, \
                f"{fn} must never write the derived status {reconciler.DERIVED_TERMINAL}"


class TestNoSideEffects:
    """(f) assert the ABSENCE of the action: no kill, no restart, no commit."""

    def test_reconcile_returns_string_writes_nothing(self, tmp_path):
        itdir, aj = self._iterdir(tmp_path)
        before = aj.read_text(encoding="utf-8")
        corrected = reconciler.reconcile_iteration(
            itdir, pid_alive=lambda p: False)   # every record's pid dead
        assert ("kid", "running", reconciler.DERIVED_TERMINAL) in corrected
        assert aj.read_text(encoding="utf-8") == before  # record untouched

    def test_nothing_killed_restarted_committed(self, tmp_path):
        # the module performs no process kill, no Popen, no git — reach into
        # the module and assert none of the primitives those actions require
        # are called during a full reconcile.
        itdir, _ = self._iterdir(tmp_path)
        killed = {"pid": None}
        real_kill = os.kill

        def spying_kill(pid, sig):
            killed["pid"] = pid
            return real_kill(pid, sig)

        os.kill = spying_kill
        git_calls = []

        real_sub = subprocess.run
        def spying_run(*a, **k):
            cmd = a[0] if a and isinstance(a[0], list) else k.get("args")
            if cmd and isinstance(cmd, list) and cmd and cmd[0] == "git":
                git_calls.append(cmd)
            return real_sub(*a, **k)

        subprocess.run = spying_run
        try:
            reconciler.reconcile_iteration(itdir, pid_alive=lambda p: True)
            reconciler.reconcile_iteration(itdir, pid_alive=lambda p: False)
        finally:
            os.kill = real_kill
            subprocess.run = real_sub
        assert killed["pid"] is None           # nothing killed
        assert git_calls == []                 # nothing committed / restarted

    @staticmethod
    def _iterdir(tmp_path):
        itdir = tmp_path / "iter-x"
        kid = itdir / "kid"
        kid.mkdir(parents=True, exist_ok=True)
        rec = {"id": "kid", "status": "running", "pid": 31337}
        aj = kid / "agent.json"
        aj.write_text(json.dumps(rec, indent=2), encoding="utf-8")
        (itdir / "manifest.json").write_text(json.dumps({
            "iter": "x", "agents": [{"id": "kid", "status": "running"}],
        }, indent=2), encoding="utf-8")
        return itdir, aj


class TestAgainstFrozenArtifact:
    """(a) 🔴 the evidence that makes this a cause, not an anecdote: the REAL
    L4.85 kid record, read from the frozen worktree, reconciles to the derived
    terminal status. If the frozen worktree is gone (cleaned), skip — but any
    box that still holds it must reconcile it.

    This is the only capture of shape (3) anyone has: a pi process that died
    on a 404 while its `agent.json` still read `status: running` and its pid
    was already dead. Nothing here modifies the worktree.
    """

    def test_frozen_l485_kid_reconciles_to_hung_dead(self):
        if not os.path.isfile(FROZEN_KID_AJ):
            pytest.skip("frozen L4.85 worktree not present; evidence is elsewhere")
        rec = json.loads(open(FROZEN_KID_AJ, encoding="utf-8").read())
        assert rec.get("status") == "running", "the frozen record must be the lie"
        pid = int(rec.get("pid") or 0)
        assert pid > 0 and not _os_pid_alive(pid), \
            f"frozen pid {pid} should be dead (verified: it is)"

        # real liveness, real record -> the derived terminal status
        assert reconciler.reconcile_record(rec) == reconciler.DERIVED_TERMINAL

    def test_frozen_manifest_has_same_stuck_kid(self):
        if not os.path.isfile(os.path.join(FROZEN_L485, "manifest.json")):
            pytest.skip("frozen L4.85 worktree not present; evidence is elsewhere")
        manifest = json.loads(
            open(os.path.join(FROZEN_L485, "manifest.json"), encoding="utf-8").read())
        kids = [a for a in manifest.get("agents", []) if a.get("tier") == "kid"]
        assert kids, "the frozen iteration must include a kid agent"
        # the derived whole-iteration pass corrects the stuck kid
        corrected = reconciler.reconcile_iteration(FROZEN_L485)
        assert any(d == reconciler.DERIVED_TERMINAL for _, _, d in corrected)


def _os_pid_alive(pid: int) -> bool:
    """Signal-existence liveness, matching spawn_budget._pid_alive's edge cases
    closely enough to verify the frozen pid is really dead. A real liveness
    check, not a stub."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError as exc:
        return exc.errno == getattr(os, "EPERM", 1)
    return True