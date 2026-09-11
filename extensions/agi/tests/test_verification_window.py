"""Tests for the `window` subcommand in `bin/verification.py` (step 3 of
hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps).

The point holds for a merge-up window (sanctuary-director.md §Merge-up step
2: "lock state + tip + baseline") before merging. `verification.py window`
PRINTS that reply from the REAL files — the suite/window lock under
`<groot>/sessions/` and the STATE_FILE baseline — and never sends, writes or
grants anything.

Fixture roots declare a ladder honouring `town_branches: {core: season/s2}`
so `_integration_branch` resolves; the tip line depends on the origin/HEAD
probes which a non-git tmp root leaves as `(no integration branch ... /
origin unresolved)`. The three facts this round asserts are lock-held, lock-
free, and the baseline sha. `--grant SEAT` just prefixes the seat name so the
line is paste-ready; the grant decision itself stays the Prime's.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import verification  # noqa: E402


def _make_groot(groot: Path, *, lock: bool = False) -> None:
    """A fixture project root: a ladder declaring the integration branch and a
    stamped baseline. Optionally a live lock file (our own pid, so `_pid_alive`
    reads it as a LIVE holder — not a stale dead-pid one)."""
    ladder = groot / "nodes" / ".geometry" / "ladder.md"
    ladder.parent.mkdir(parents=True, exist_ok=True)
    ladder.write_text(
        "---\ntype: config\ntown_branches:\n  core: season/s2\n---\n",
        encoding="utf-8")
    state = groot / "sessions" / verification.STATE_FILE
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(json.dumps({
        "active": 2096, "deprecated": 195, "total": 2291,
        "sha": "7c602379a", "stamped_at": time.time(),
        "reason": "kept (on season/s2, HEAD pushed)",
    }), encoding="utf-8")
    if lock:
        lock_path = groot / "sessions" / verification.SUITE_LOCK
        # a LIVE holder that is not our own process: the parent of this pytest
        # run is guaranteed alive and != os.getpid(), so the handler reads it
        # as a real held lock rather than a stale/dead-pid read.
        lock_path.write_text(str(os.getppid()), encoding="utf-8")


def test_window_lock_free_when_no_lock_file(tmp_path):
    _make_groot(tmp_path)
    out = verification.render_window(tmp_path)
    assert "lock: free" in out
    assert "7c602379a" in out  # fixture baseline sha


def test_window_lock_held_when_fixture_lock_exists(tmp_path):
    _make_groot(tmp_path, lock=True)
    out = verification.render_window(tmp_path)
    assert "lock: held by " in out
    assert str(os.getppid()) in out
    assert "since " in out
    assert "7c602379a" in out  # fixture baseline sha


def test_window_baseline_reports_stamping_sha_and_reason(tmp_path):
    _make_groot(tmp_path)
    out = verification.render_window(tmp_path)
    assert "baseline:" in out
    assert "active=2096" in out
    assert "deprecated=195" in out
    assert "total=2291" in out
    assert "stamped sha=7c602379a" in out
    assert "reason=kept (on season/s2, HEAD pushed)" in out


def test_window_no_baseline_reports_none(tmp_path):
    groot = tmp_path / "empty"
    groot.mkdir(parents=True)
    out = verification.render_window(groot)
    assert "baseline: none recorded" in out


# ---------------------------------------------------------------------------
# The worktree caveat the parent measured LIVE (SL1.04): two defects, both in
# `render_window`. (1) the baseline was read from the CALLER's per-worktree
# `<groot>/sessions/` (`none recorded` from a seat worktree) even though the
# never-lower baseline is stamped in MAIN; (2) the tip line named the CALLER's
# HEAD as "MAIN HEAD". Both route through `git_common_root` to the main
# checkout -- same rule `_suite_ts_path` already applies to the suite stamp.
#
# A real linked worktree is required: the shared-sessions routing only takes
# effect when `git rev-parse --git-common-dir` differs from the caller's own
# git dir. A nested plain tmp dir is the IDENTITY and would not exercise the
# fix at all. So this builds a genuine main repo with a linked worktree.


def _git(cwd: Path, *args: str) -> str:
    r = subprocess.run(["git", "-C", str(cwd), *args], check=True,
                       capture_output=True, text=True)
    return r.stdout.strip()


def _make_main_and_worktree(tmp_path: Path):
    """A real git main repo carrying the stamped baseline + a linked worktree
    whose own `.agi/sessions/` has NONE. Returns (main_graph, wt_graph, sha0,
    main_head, wt_head) where main_head != wt_head so the honest-MAIN-head
    claim is actually tested."""
    main = tmp_path / "main"
    main.mkdir(parents=True)
    _git(main, "init", "-b", "master")
    _git(main, "config", "user.email", "t@t")
    _git(main, "config", "user.name", "t")
    (main / "README").write_text("x")
    _git(main, "add", "-A")
    _git(main, "commit", "-m", "init")
    sha0 = _git(main, "rev-parse", "HEAD")
    # declare the integration branch and give it a REAL origin ref so the tip
    # line resolves without pushing (the ladder's `town_branches` needs
    # `rotate.load_ladder_field`, which the graph dir must carry).
    _git(main, "branch", "season/s2", sha0)
    _git(main, "update-ref", "refs/remotes/origin/season/s2", sha0)
    # a linked worktree, checked out at the same sha0, on a seat branch
    wt = tmp_path / "wt"
    _git(main, "worktree", "add", "-b", "loop/slug@s2", str(wt), "master")
    # MAIN advances past the worktree so the two heads genuinely differ -- the
    # phoney-label defect is only detectable when main != worktree HEAD.
    (main / "README").write_text("x2")
    _git(main, "add", "-A")
    _git(main, "commit", "-m", "advance main")
    main_head = _git(main, "rev-parse", "HEAD")
    wt_head = _git(wt, "rev-parse", "HEAD")
    assert main_head != wt_head
    # graph dir + ladder in BOTH trees (a real worktree carries `.agi/`); the
    # baseline lives ONLY in MAIN's sessions -- the whole point of the defect.
    for repo in (main, wt):
        gdir = repo / ".agi"
        gdir.mkdir(parents=True, exist_ok=True)
        (gdir / "config.json").write_text('{"metric_primary": "x"}',
                                           encoding="utf-8")
        ladder = gdir / "nodes" / ".geometry" / "ladder.md"
        ladder.parent.mkdir(parents=True, exist_ok=True)
        ladder.write_text(
            "---\ntype: config\ntown_branches:\n  core: season/s2\n---\n",
            encoding="utf-8")
    state = main / ".agi" / "sessions" / verification.STATE_FILE
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(json.dumps({
        "active": 2096, "deprecated": 195, "total": 2291,
        "sha": "7c602379a", "stamped_at": time.time(),
        "reason": "kept (on season/s2, HEAD pushed)",
    }), encoding="utf-8")
    return main / ".agi", wt / ".agi", sha0, main_head, wt_head


def test_window_reads_main_baseline_and_main_head_from_a_worktree(tmp_path):
    """The parent's live measurement, pinned as a red-first test: a `window`
    reply run from a seat WORKTREE must read MAIN's never-lower baseline (the
    shared sessions dir through `git_common_root`, exactly where the stamp
    lives) and must print MAIN's real HEAD -- never the worktree's own HEAD
    wearing the "MAIN HEAD" label."""
    main_graph, wt_graph, sha0, main_head, wt_head = \
        _make_main_and_worktree(tmp_path)
    out = verification.render_window(wt_graph)
    # baseline routed to MAIN, not the caller's freshly-absent per-worktree one
    assert "baseline: active=2096" in out
    assert "stamped sha=7c602379a" in out
    assert "none recorded" not in out
    # the tip line honestly names MAIN's HEAD (and !== the worktree head)
    assert f"MAIN HEAD {main_head}" in out
    assert f"MAIN HEAD {wt_head}" not in out
    # sanity: run from MAIN itself the SAME facts hold and sha0 is still the
    # declared tip
    out_main = verification.render_window(main_graph)
    assert f"MAIN HEAD {main_head}" in out_main
    assert f"{sha0}" in out_main
