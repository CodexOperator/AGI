"""Fixtures-only proof of `season.py merge-kids` (hypothesis:
l4-a-parent-cuts-five-and-merges-its-kids, half 2).

Every git operation happens inside a TEMP repo under tmp_path, never this
repo. The suite command in the fixtures is a trivial always-green shell one
liner (or an always-red one for the red fixtures) so the merge protocol is
proved without coupling to this repo's real pytest run.
"""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

BIN_DIR = Path(__file__).resolve().parents[1] / "bin"
SEASON_PY = BIN_DIR / "season.py"

GREEN_SUITE = "true"
RED_SUITE = "false"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path):
    """A temp project-shaped git repo: base branch carrying one node file and
    one source file, plus an always-green `--suite` command."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "round").check_returncode()
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test")
    # project marker so season.py's find_project_root resolves here
    (repo / ".agi").mkdir()
    (repo / ".agi" / "config.json").write_text("{}")
    # one node file
    node = repo / ".agi" / "nodes" / "hypothesis" / "h-merge.md"
    node.parent.mkdir(parents=True)
    node.write_text(_NODE_BASE)
    # one source file
    src = repo / "src.py"
    src.write_text("VALUE = 1\n")
    # a hideously real-ish multi-line source file for the clean branch
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "base").check_returncode()
    return repo


_NODE_BASE = """---
id: hypothesis:h-merge
type: hypothesis
verdict: pending
confidence: 0.5
---
# h-merge

## Agent Notes
base-note-a
base-note-b
"""


def _run_merge_kids(repo: Path, *branches: str, suite: str = GREEN_SUITE):
    return subprocess.run(
        [sys_executable(), SEASON_PY, "--root", str(repo), "merge-kids",
         *branches, "--suite", suite],
        capture_output=True, text=True)


def sys_executable():
    return shutil.which("python3") or "python3"


# -- branch helpers ----------------------------------------------------------

def _mkalias(repo: Path, branch: str):
    _git(repo, "checkout", "-b", branch).check_returncode()


def _splitbranch(repo: Path, base: str, branch: str):
    _git(repo, "checkout", "-b", branch, base).check_returncode()


def _commit_all(repo: Path, msg: str):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", msg).check_returncode()


def test_branch_a_clean_merges(repo):
    """Branch A (clean): adds an unrelated source line -> merges clean."""
    _mkalias(repo, "kid-A")
    src = repo / "src.py"
    src.write_text(src.read_text() + "CLEAN_A = True\n")
    _commit_all(repo, "kid A")
    _git(repo, "checkout", "round")

    r = _run_merge_kids(repo, "kid-A")
    assert r.returncode == 0, r.stderr
    assert "merged kid-A --no-ff into round" in r.stdout
    out = _git(repo, "log", "--oneline", "-3").stdout
    assert "kid A" in out
    # merge commit has two parents and both bytes are present
    assert "CLEAN_A = True" in (repo / "src.py").read_text()


def test_branch_b_node_conflict_union(repo):
    """Branch B (node-conflicting): edits the SAME node line AND drops its
    verdict/confidence. The current branch holds the higher-confidence
    verdict. The merged file must keep BOTH notes and the HIGHER-confidence
    verdict."""
    node = repo / ".agi" / "nodes" / "hypothesis" / "h-merge.md"

    def set_node(verdict, conf, note):
        return ("---\nid: hypothesis:h-merge\ntype: hypothesis\n"
                f"verdict: {verdict}\nconfidence: {conf}\n---\n"
                "# h-merge\n\n## Agent Notes\n" + note + "\n")

    # current branch (round) raises the verdict and selects its own note
    node.write_text(set_node("inconclusive_lean_proved:70", "0.7",
                             "round-selected-note"))
    _commit_all(repo, "round raises verdict")

    # kid B branches from base (round~1) with a lower-confidence verdict and
    # edits the SAME note line -> genuine same-line modify/modify conflict
    _git(repo, "checkout", "-b", "kid-B", "round~1")
    node.write_text(set_node("inconclusive_lean_proved:30", "0.3",
                             "kid-selected-note"))
    _commit_all(repo, "kid B")
    _git(repo, "checkout", "round")

    r = _run_merge_kids(repo, "kid-B")
    assert r.returncode == 0, r.stderr
    merged = node.read_text()
    # union keeps BOTH distinct note lines
    assert "round-selected-note" in merged
    assert "kid-selected-note" in merged
    # higher-confidence verdict/confidence kept (70/0.7, not 30/0.3)
    assert "verdict: inconclusive_lean_proved:70" in merged
    assert "confidence: 0.7" in merged
    assert "verdict: inconclusive_lean_proved:30" not in merged
    assert "confidence: 0.3" not in merged


def test_branch_b_node_union_keeps_consumers_stronger(repo):
    """Union must take the HIGHER-confidence verdict even when the KID (the
    merged branch) is the one holding it while the current branch is lower."""
    node = repo / ".agi" / "nodes" / "hypothesis" / "h-merge.md"

    def set_node(verdict, conf, note):
        return ("---\nid: hypothesis:h-merge\ntype: hypothesis\n"
                f"verdict: {verdict}\nconfidence: {conf}\n---\n"
                "# h-merge\n\n## Agent Notes\n" + note + "\n")

    # current branch (round) is the weak pending default with one note
    node.write_text(set_node("pending", "0.5", "round-note"))
    _commit_all(repo, "round pending")
    # kid B branches from base (round~1) and proves it, editing the SAME note
    _git(repo, "checkout", "-b", "kid-B", "round~1")
    node.write_text(set_node("proved", "0.9", "kid-proves-note"))
    _commit_all(repo, "kid B proves")
    _git(repo, "checkout", "round")

    r = _run_merge_kids(repo, "kid-B")
    assert r.returncode == 0, r.stderr
    merged = node.read_text()
    # the kid's decisive verdict wins, both notes kept
    assert "verdict: proved" in merged
    assert "confidence: 0.9" in merged
    assert "kid-proves-note" in merged
    assert "round-note" in merged


def test_branch_c_source_conflict_refuses_and_leaves_merge(repo):
    """Branch C (source-conflicting): both sides edit the same source line ->
    the verb refuses, names the path, leaves MERGE_HEAD present, commits
    nothing."""
    src = repo / "src.py"
    # current branch (round) edits the VALUE line
    src.write_text(src.read_text().replace("VALUE = 1", "VALUE = 2"))
    _commit_all(repo, "round touches source")
    # kid C branches from base (round~1) and edits the SAME line differently
    _git(repo, "checkout", "-b", "kid-C", "round~1")
    src.write_text(src.read_text().replace("VALUE = 1", "VALUE = 3"))
    _commit_all(repo, "kid C")
    _git(repo, "checkout", "round")

    before = _git(repo, "rev-parse", "HEAD").stdout.strip()
    r = _run_merge_kids(repo, "kid-C")
    assert r.returncode != 0
    assert "SOURCE conflict in kid-C" in r.stderr
    assert "src.py" in r.stderr
    # merge left in progress: MERGE_HEAD still present
    mh = _git(repo, "rev-parse", "--verify", "MERGE_HEAD")
    assert mh.returncode == 0, "merge should be left in progress"
    # nothing committed
    after = _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert after == before


def test_suite_red_aborts_and_commits_nothing(repo):
    """A branch whose suite fails causes `git merge --abort` and no merge
    commit."""
    _splitbranch(repo, "round", "kid-red")
    src = repo / "src.py"
    src.write_text(src.read_text() + "RED = True\n")
    _commit_all(repo, "kid red")
    _git(repo, "checkout", "round")

    before = _git(repo, "rev-parse", "HEAD").stdout.strip()
    r = _run_merge_kids(repo, "kid-red", suite=RED_SUITE)
    assert r.returncode != 0
    assert "suite red after merging kid-red" in r.stderr
    # merge aborted: no MERGE_HEAD and nothing committed
    mh = _git(repo, "rev-parse", "--verify", "MERGE_HEAD")
    assert mh.returncode != 0, "merge must be aborted"
    after = _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert after == before


def test_zero_ahead_branch_refused(repo):
    """A zero-commits-ahead branch is refused (no no-op green merge commit)."""
    _mkalias(repo, "kid-empty")
    _git(repo, "checkout", "round")
    before = _git(repo, "rev-parse", "HEAD").stdout.strip()
    r = _run_merge_kids(repo, "kid-empty")
    assert r.returncode != 0
    assert "zero commits ahead" in r.stderr
    after = _git(repo, "rev-parse", "HEAD").stdout.strip()
    assert after == before


def test_multiple_branches_merged_in_order(repo):
    """Two clean branches merge one at a time, in the order given, both suite-
    gated and both landed."""
    _mkalias(repo, "kid-1")
    (repo / "src.py").write_text((repo / "src.py").read_text() + "ONE\n")
    _commit_all(repo, "kid 1")
    _mkalias(repo, "kid-2")
    (repo / "src.py").write_text((repo / "src.py").read_text() + "TWO\n")
    _commit_all(repo, "kid 2")
    _git(repo, "checkout", "round")

    r = _run_merge_kids(repo, "kid-1", "kid-2")
    assert r.returncode == 0, r.stderr
    assert "merged kid-1 --no-ff into round" in r.stdout
    assert "merged kid-2 --no-ff into round" in r.stdout
    log = _git(repo, "log", "--oneline", "-4").stdout
    # three merge parents' content all present
    txt = (repo / "src.py").read_text()
    assert "ONE" in txt and "TWO" in txt


# -- the pure resolver is testable without git ------------------------------

@pytest.fixture(scope="module")
def season_module():
    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location(
        "season_under_test", SEASON_PY)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["season_under_test"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_pure_higher_confidence_verdict(season_module):
    _higher_confidence_verdict = season_module._higher_confidence_verdict
    a = ("inconclusive_lean_proved:70", "0.7")
    b = ("inconclusive_lean_proved:30", "0.3")
    assert _higher_confidence_verdict(a, b) == a  # tie -> ours
    b2 = ("inconclusive_lean_proved:80", "0.8")
    assert _higher_confidence_verdict(a, b2) == b2  # theirs stronger
    # a definitive state beats any inconclusive regardless of percent
    b3 = ("proved", "0.4")
    assert _higher_confidence_verdict(b2, b3) == b3


def test_pure_resolve_node_conflict_unions_and_keeps_strongest(season_module):
    _resolve_node_conflict = season_module._resolve_node_conflict
    sector = """---
id: hypothesis:h
verdict: inconclusive_lean_proved:70
confidence: 0.7
---
# h

## Agent Notes
base-note-a
<<<<<<< HEAD
curline-added
=======
kidline-added
>>>>>>> kid-B
"""
    resolved = _resolve_node_conflict(sector)
    assert "curline-added" in resolved
    assert "kidline-added" in resolved
    assert "verdict: inconclusive_lean_proved:70" in resolved
    assert "confidence: 0.7" in resolved
    # no markers remain
    assert "<<<<<<<" not in resolved
    assert "=======" not in resolved
    assert ">>>>>>>" not in resolved


def test_merge_kids_is_a_registered_subcommand():
    """Regression for the brief->verb wiring (kid 3 of the merge hypothesis):
    the branch-parent brief names `season.py merge-kids <kid-branch> ...` as
    the parent's ONE git operation. If `merge-kids` ever stops being a
    registered season.py subcommand, the brief's verb silently points at
    nothing — and the falsifier 'nothing names the verb' comes straight back.

    We read the PARSER only and never invoke git: `--help` on the subcommand
    makes argparse exit during parse_args (SystemExit 0) before any
    project-root resolution or git work, so a bogus `--root` is harmless here.
    """
    r = subprocess.run(
        [sys_executable(), SEASON_PY, "--root", "/nonexistent",
         "merge-kids", "--help"],
        capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout, r.stderr)
    help_text = r.stdout + r.stderr
    assert "merge-kids" in help_text, (
        "season.py must register merge-kids as a subcommand for the brief "
        "to name it")
    assert "branches" in help_text, (
        "merge-kids must still take its positional kid-branch list")
    # it is the merge verb over kid branches, not some unrelated subcommand
    assert "kid branches" in help_text.lower(), (
        "merge-kids positional help must describe the kid-branch merge it does")
