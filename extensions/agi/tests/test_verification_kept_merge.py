"""Experiment for hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-
a-kept-merge.

THE CLAIM: `verification.py` should record the never-lower node-count baseline
(`.agi/sessions/verify-count.json`) only when the run is on bytes that are
KEPT — the tree is `season/s2` AND HEAD is an ancestor-of/equal to the pushed
`origin/season/s2`, or an explicit `--stamp` is passed by the merge-up step
AFTER the push. A run on a worktree, a seat branch, or an unpushed MAIN read
compares but does NOT stamp (note says `baseline not stamped: <reason>`).

FALSIFIER: a red or dropped read that stamps.

THIS EXPERIMENT measures the CURRENT implementation, which predates the fix.
The question the run answers: does the current `compare_count` stamp the
baseline on every state-writing path regardless of git context? If yes, the
falsifier is LIVE in the current bytes — a dropped or worktree read writes
`verify-count.json` exactly as a kept merge would.

We test the CURRENT code under mock git-context conditions. Because the
current `compare_count` has NO git awareness at all (it never asks where HEAD
is, what branch, or what is pushed), we expect:
  (a) first run on a worktree groot stamps (unconditional `_write_state`)
  (b) a steady run on a seat-branch groot re-stamps/updates
  (c) there is no code path in the module that consults git for stamping
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import verification  # noqa: E402


def test_compare_count_has_no_git_context_in_module_source():
    """The falsifier's mechanism: the current compare_count consults NO git
    context when deciding to write the baseline. If the module source never
    reads the branch, HEAD ancestry, or a remote ref inside the node-count
    path, then EVERY state-writing read stamps — kept or dropped alike."""
    src = (BIN / "verification.py").read_text(encoding="utf-8")
    # Isolate just the two stamping functions, not the whole file tail (which
    # also holds the bin-freshness `_git_tracked` helper that legitimately
    # names git). Scope by function body between `def compare_count` and the
    # next top-level `def`.
    start = src.index("def compare_count")
    end = src.index("def _write_state", start)
    body = src[start:end]
    assert "git" not in body.lower(), (
        "compare_count already consults git — the fix is present")


def test_first_run_on_a_worktree_groot_stamps_the_baseline(tmp_path):
    """(a) Current first-run path: NO prior baseline + a read -> stamps,
    whatever the git context. On a seat-branch/worktree groot this is exactly
    the falsifier — bytes that would be dropped have just become the baseline."""
    groot = tmp_path / ".agi"   # simulate a worktree groot; no git here
    (groot / "sessions").mkdir(parents=True)
    current = {"active": 1707, "deprecated": 194, "total": 1901}
    r = verification.compare_count(groot, current)
    assert r.status == "PASS"
    assert "baseline recorded" in r.note
    state = json.loads((groot / "sessions" / "verify-count.json").read_text())
    assert state == current, "the worktree read stamped the baseline"


def test_steady_run_on_a_seat_groot_re_stamps(tmp_path):
    """(b) Current steady path: active >= baseline -> `_write_state` again,
    overwriting the baseline even though the read may be on droppable bytes."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / "verify-count.json").write_text(
        json.dumps({"active": 1707, "deprecated": 194, "total": 1901}))
    newer = {"active": 1710, "deprecated": 195, "total": 1905}
    r = verification.compare_count(groot, newer)
    assert r.status == "PASS"
    state = json.loads((groot / "sessions" / "verify-count.json").read_text())
    assert state == newer, "a larger read re-stamped the baseline unconditionally"


def test_drop_still_fails_but_never_stamps(tmp_path):
    """(c) A drop (active < baseline) already FAILs and does NOT write — the
    one half the current code gets right. The residual gap is the first-run
    and steady-update paths, which stamp with no kept-bytes check."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / "verify-count.json").write_text(
        json.dumps({"active": 9999, "deprecated": 0, "total": 0}))
    r = verification.compare_count(groot, {"active": 1707,
                                           "deprecated": 194, "total": 1901})
    assert r.status == "FAIL"
    state = json.loads((groot / "sessions" / "verify-count.json").read_text())
    assert state["active"] == 9999, "the drop read must not have overwritten"
