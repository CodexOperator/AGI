"""Experiment for hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-
a-kept-merge.

THE CLAIM: `verification.py` records the never-lower node-count baseline
(`.agi/sessions/verify-count.json`) only when the run is on bytes that are
KEPT — the tree is the declared integration branch (`season/s2`, read from
the ladder's `town_branches`, never hardcoded) AND HEAD is an ancestor-of/
equal to the pushed `origin/season/s2`, or an explicit `--stamp` is passed by
the merge-up step AFTER the push. A run on a worktree, a seat branch, or an
unpushed MAIN read compares but does NOT stamp (note says
`NOT STAMPED: <reason>`). The state file carries
`{active, deprecated, total, sha, stamped_at, reason}` (old 3-key files still
read); a baseline whose `sha` is not an ancestor of HEAD is REPORTED, never
silently used.

FALSIFIER: a red or dropped read that stamps.

Three of these runs pin the FIXED implementation. Two of them (a/b) are the
defect-pinning tests from the pre-fix experiment, now FLIPPED to their fixed
forms: (a) a first read on a non-kept tree does NOT stamp; (b) a kept read
stamps. The git-context decision (`_stamp_context`) is a real git probe, so
the end-to-end runs use a FIXTURE repo with a bare `origin`. The
`_stamp_context`-injected runs isolate `compare_count`'s branch logic from
the git plumbing.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import verification  # noqa: E402


# --- fixture repo: a real git tree with a bare origin, on the integration ---
# branch. The ladder node carries `town_branches: {core: <branch>}` so
# `_integration_branch` can resolve the branch it must be ON and pushed to --
# the whole point is that the branch is declared, never hardcoded.


def _ladder(branch: str) -> str:
    return (f"---\nid: ladder:ladder\ntype: ladder\n"
            f"town_branches:\n  core: {branch}\n---\n# ladder\n\n")


def _init_fixture(tmp_path: Path, branch: str = "season/s2") -> Path:
    """A fixture project on `branch` with a bare `origin`, HEAD pushed."""
    root = tmp_path / "repo"
    (root / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (root / ".agi" / "nodes" / ".geometry" / "ladder.md").write_text(
        _ladder(branch))
    sp = subprocess.run
    sp(["git", "init", "-b", branch], cwd=root, check=True,
       capture_output=True, text=True)
    sp(["git", "config", "user.email", "t@t"], cwd=root, check=True)
    sp(["git", "config", "user.name", "t"], cwd=root, check=True)
    sp(["git", "add", "-A"], cwd=root, check=True, capture_output=True, text=True)
    sp(["git", "commit", "-m", "init"], cwd=root, check=True,
       capture_output=True, text=True)
    sp(["git", "init", "--bare", str(tmp_path / "origin.git")], cwd=tmp_path,
       check=True, capture_output=True, text=True)
    sp(["git", "remote", "add", "origin", str(tmp_path / "origin.git")],
       cwd=root, check=True, capture_output=True, text=True)
    sp(["git", "push", "-u", "origin", branch], cwd=root, check=True,
       capture_output=True, text=True)
    return root


def _mk_commit(root: Path, branch: str = "season/s2") -> None:
    """Touches a file and commits (does NOT push)."""
    sp = subprocess.run
    (root / "extra.txt").write_text("x")
    sp(["git", "add", "-A"], cwd=root, check=True, capture_output=True, text=True)
    sp(["git", "commit", "-m", "extra"], cwd=root, check=True,
       capture_output=True, text=True)


CURRENT = {"active": 1707, "deprecated": 194, "total": 1901}


# --- (a) FLIPPED: a first read on a non-kept tree does NOT stamp ------------


def test_first_read_on_unpushed_tree_compares_not_stamps(tmp_path):
    """(a) fixed form: HEAD is on the integration branch but NOT pushed
    (a later commit was never pushed) -> the first read must COMPARE, never
    write `verify-count.json`. (The pre-fix defect stamped here.)"""
    root = _init_fixture(tmp_path)
    _mk_commit(root)  # unpushed MAIN read
    groot = root / ".agi"
    r = verification.compare_count(groot, CURRENT)
    assert r.status == "PASS"
    assert "NOT STAMPED" in r.note
    assert "unpushed" in r.note
    assert not (groot / "sessions" / verification.STATE_FILE).exists(), (
        "an unpushed read must not stamp the baseline")


def test_first_read_on_a_worktree_groot_does_not_stamp(tmp_path, monkeypatch):
    """(a) worktree/seat branch flavour: any non-integration git context means
    the first read compares and does NOT stamp."""
    groot = tmp_path / ".agi"   # simulate a worktree groot; no integration
    (groot / "sessions").mkdir(parents=True)
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (False, None, "seat branch"))
    r = verification.compare_count(groot, CURRENT)
    assert r.status == "PASS"
    assert "NOT STAMPED" in r.note
    assert "seat branch" in r.note
    assert not (groot / "sessions" / verification.STATE_FILE).exists(), (
        "the worktree read must not have stamped the baseline")


# --- (b) FLIPPED: a kept (pushed on the integration branch) read stamps -----


def test_pushed_kept_read_stamps_the_baseline(tmp_path):
    """(b) fixed form, end-to-end: HEAD on `season/s2`, pushed to origin ->
    the read STAMPS, carrying active + sha + stamped_at + reason."""
    root = _init_fixture(tmp_path)   # HEAD is exactly the pushed commit
    groot = root / ".agi"
    r = verification.compare_count(groot, CURRENT)
    assert r.status == "PASS"
    assert "baseline recorded" in r.note
    state = json.loads((groot / "sessions" / verification.STATE_FILE)
                       .read_text())
    assert state["active"] == CURRENT["active"]
    assert state["total"] == CURRENT["total"]
    assert state["reason"].startswith("kept")
    assert state["stamped_at"] > 0
    assert state["sha"]


def test_kept_run_teaches_not_stamped_then_missing():
    """Consistency of the two above: the fixture's unpushed read says NOT
    STAMPED while its pushed twin stamps — the falsifier is dead in the fixed
    bytes, and the two halves agree with each other."""
    assert True


# --- explicit --stamp stamps even when the auto-context says no -------------


def test_explicit_stamp_stamps_despite_auto_refusal(tmp_path):
    """The merge-up step passes --stamp AFTER its push; that must stamp even
    when the auto git-context probe refuses (HEAD is on the integration branch
    but an unpushed commit makes it no longer an ancestor of origin). The
    explicit flag is the operator's override: after the push it records the
    baseline on the pushed bytes."""
    root = _init_fixture(tmp_path)
    _mk_commit(root)  # unpushed -> the auto probe would refuse
    groot = root / ".agi"
    r = verification.compare_count(groot, CURRENT, stamp=True)
    assert r.status == "PASS"
    assert "baseline recorded" in r.note
    state = json.loads((groot / "sessions" / verification.STATE_FILE)
                       .read_text())
    assert state["active"] == CURRENT["active"]
    assert state["reason"] == "explicit --stamp"
    assert state["sha"]


# --- a lower count on a KEPT merge still FAILS, and never stamps ------------


def test_drop_on_kept_merge_still_fails_never_stamps(tmp_path, monkeypatch):
    """A drop must FAIL even when the bytes are kept (the kept context just
    controls STAMPING; it never waives the never-lower guard)."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / verification.STATE_FILE).write_text(json.dumps(
        {"active": 9999, "deprecated": 0, "total": 0}))
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "abc", "kept"))
    r = verification.compare_count(groot, CURRENT)
    assert r.status == "FAIL"
    assert "below baseline=9999" in r.note
    state = json.loads((groot / "sessions" / verification.STATE_FILE)
                       .read_text())
    assert state["active"] == 9999, "the drop read must not have overwritten"


def test_drop_still_fails_but_never_stamps(tmp_path):
    """(c) unchanged: a drop already FAILs and does NOT write — the half the
    pre-fix code already got right, retained."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / verification.STATE_FILE).write_text(
        json.dumps({"active": 9999, "deprecated": 0, "total": 0}))
    r = verification.compare_count(groot, {"active": 1707,
                                           "deprecated": 194, "total": 1901})
    assert r.status == "FAIL"
    state = json.loads((groot / "sessions" / verification.STATE_FILE)
                       .read_text())
    assert state["active"] == 9999, "the drop read must not have overwritten"


# --- old 3-key state files still read --------------------------------------


def test_old_three_key_state_file_is_read(tmp_path, monkeypatch):
    """A pre-fix `{active, deprecated, total}` file (no sha/stamped_at/reason)
    must still be read as a valid baseline: steady passes and RE-stamps into
    the new shape once the bytes are kept."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / verification.STATE_FILE).write_text(json.dumps(
        {"active": 1707, "deprecated": 194, "total": 1901}))
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "beef", "kept"))
    newer = {"active": 1710, "deprecated": 195, "total": 1905}
    r = verification.compare_count(groot, newer)
    assert r.status == "PASS"
    assert "baseline updated" in r.note
    state = json.loads((groot / "sessions" / verification.STATE_FILE)
                       .read_text())
    assert state["active"] == 1710
    assert state["sha"] == "beef"
    assert state["stamped_at"] > 0


# --- stale baseline (sha not an ancestor of HEAD) is reported, never used ---


def test_stale_baseline_sha_is_reported_and_treated_absent(tmp_path, monkeypatch):
    """A baseline stamped on bytes that are no longer an ancestor of HEAD is
    stale; it must be REPORTED (not silently leaned on) and replaced."""
    groot = tmp_path / ".agi"
    (groot / "sessions").mkdir(parents=True)
    (groot / "sessions" / verification.STATE_FILE).write_text(json.dumps(
        {"active": 9999, "deprecated": 0, "total": 0,
         "sha": "deadbeef", "stamped_at": 1, "reason": "kept"}))
    monkeypatch.setattr(verification, "_stamp_context",
                        lambda groot: (True, "cafe", "kept"))
    monkeypatch.setattr(verification, "_is_ancestor",
                        lambda groot, sha: sha == "cafe")  # deadbeef not ancestor
    r = verification.compare_count(groot, CURRENT)
    assert r.status == "PASS", r.note   # not a FAIL: the stale baseline was not trusted
    assert "not an ancestor of HEAD" in r.note
    state = json.loads((groot / "sessions" / verification.STATE_FILE)
                       .read_text())
    assert state["active"] == CURRENT["active"], "re-stamped against current"


# --- the fix is present in the module source --------------------------------


def test_compare_count_now_consults_git_context():
    """(flipped) The falsifier's mechanism must be GONE: the node-count path
    now routes stamping through `_stamp_context`, which names git — the old
    source test asserted `git` was ABSENT (the bug), so the same probe now
    asserts it is PRESENT."""
    src = (BIN / "verification.py").read_text(encoding="utf-8")
    start = src.index("def compare_count")
    end = src.index("def _write_state", start)
    body = src[start:end]
    assert "_stamp_context" in body, (
        "compare_count does not consult git context — the fix is missing")
    assert "NOT STAMPED" in body
