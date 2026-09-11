"""Targeted tests for hypothesis:harvest-table-subcommand.

`rotate.py harvest-table --seat S [--round N | --all-live]` prints one row per
ROUND giving the five facts the director still discovers by hand:

  1. branch   — `loop/<slug>-<parent-id>@s<N>`, named after the PARENT-tier
                agent (dispatch names the round branch after the parent, and
                the row is one-per-round, kids in the kids column),
  2. worktree — the parent's `.agi/worktrees/<parent-id>/` (or `-` once gone),
  3. diffstat against the merge-base with the seat branch (a moved seat tip
                never shifts the base; a FULLY-MERGED round recovers its own
                changeset from the branch),
  4. the round's kid experiment node ids (added on the branch, under
                `.agi/nodes/experiment/`),
  5. each kid's `verdict`.

A round's authoritative manifest is the SEAT's — the record whose agent is
`tier == "parent"` names the branch — and it lives in the seat worktree at
`.agi/worktrees/seat-<S>/.agi/sessions/iter-*/` (the falsifier of the L4.236 /
L4.243 rounds: the scanner keyed rows by KID id and read the KID's worktree
manifest, which has no branch, while the branch is named after the parent).

Red-first. Builds a real git repo + a `--branch`-style worktree (the same
shape dispatch.py/loop_branch_name produces) with a session manifest, and
drives `rotate.main(['harvest-table', ...])`.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402

PARENT = "a00-feedbeef"          # parent-tier agent: names the round branch
KID = "a00-deadc0de"             # kid agent id (a worktree manifest's record)
BRANCH = "loop/hypothesis-harvest-table-subc-a00-feedbeef@s2"
SEAT = "test-seat"
SEAT_REF = f"seat/{SEAT}@s2"


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True)


def make_project_repo(tmp_path: Path) -> Path:
    """A real git repo on `master` with a committed `.agi/` graph dir and a
    `.gitignore` that ignores sessions/ (as the real repo does)."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x")
    (repo / ".gitignore").write_text("sessions/\n.agi/sessions/\n")
    graph = repo / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text('{"metric_primary": "outcome_coverage"}')
    (graph / "nodes").mkdir(exist_ok=True)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init with graph dir + gitignore")
    return repo


def make_round_worktree(repo: Path) -> Path:
    """The round's worktree + branch, named after the PARENT-tier agent (the
    shape dispatch.py cuts: `loop/<slug>-<parent-id>@s<N>`)."""
    wt = repo / ".agi" / "worktrees" / PARENT
    _git(repo, "worktree", "add", "-b", BRANCH, str(wt), "master")
    return wt


def commit_kid_node(wt: Path, name: str = "a00-kid.md",
                    node_id: str = "experiment:a00-kid",
                    verdict: str = "inconclusive_lean_proved:50") -> Path:
    """Write + commit one experiment kid node on the round branch."""
    n = wt / ".agi" / "nodes" / "experiment"
    n.mkdir(parents=True, exist_ok=True)
    p = n / name
    p.write_text(
        f"---\nid: {node_id}\ntype: experiment\n"
        f"verdict: {verdict}\n---\n\nround kid node\n",
        encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-m", f"kid node {node_id}")
    return p


def write_seat_manifest(repo: Path, iter_id: str, *,
                        status: str = "done", branch: str = BRANCH,
                        dispatched_by: str = SEAT, parent: str = PARENT,
                        kid_sessions: bool = True) -> None:
    """Write the round's authoritative manifest under the SEAT worktree
    (`.agi/worktrees/seat-<S>/.agi/sessions/iter-*`), carrying the PARENT-tier
    record that names the branch. Also drops a KID-only manifest under the
    parent's worktree, mirroring dispatch: the parent's own worktree session
    dir lists only the kids, never the branch."""
    seat_sess = repo / ".agi" / "worktrees" / f"seat-{SEAT}" / ".agi" / \
        "sessions" / f"iter-{iter_id}"
    seat_sess.mkdir(parents=True, exist_ok=True)
    # The seat ref the manifest records as base_branch must exist (as it does
    # for a real seat), or the merge-base with it cannot resolve.
    if not _git(repo, "rev-parse", "--verify", "--quiet",
                SEAT_REF).stdout.strip():
        _git(repo, "branch", SEAT_REF, "master")
    mf = {
        "iter": iter_id,
        "agents": [{
            "id": parent, "tier": "parent", "status": status,
            "dispatched_by": dispatched_by, "branch": branch,
            "base_branch": SEAT_REF,
            "target": "hypothesis:harvest-table-subcommand",
            "worktree": str(repo / ".agi" / "worktrees" / parent),
        }],
    }
    (seat_sess / "manifest.json").write_text(
        json.dumps(mf), encoding="utf-8")

    if kid_sessions:
        pwt = repo / ".agi" / "worktrees" / parent / ".agi" / "sessions" / \
            f"iter-{iter_id}"
        pwt.mkdir(parents=True, exist_ok=True)
        (pwt / "manifest.json").write_text(json.dumps({
            "iter": iter_id,
            "agents": [{"id": KID, "tier": "kid", "status": status,
                        "dispatched_by": dispatched_by,
                        "target": "hypothesis:harvest-table-subcommand"}],
        }), encoding="utf-8")


def run_harvest(main: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "bin" / "rotate.py"),
         "harvest-table", "--root", str(main), *flags],
        capture_output=True, text=True)


def test_parent_named_round_reports_branch_kids_verdict(tmp_path: Path) -> None:
    """The falsifier of L4.236/L4.243: the authoritative manifest lives under
    the SEAT worktree (`.agi/worktrees/seat-x/.agi/sessions/`), carries the
    PARENT-tier record, and the round branch is named after the parent — while
    the parent's OWN worktree session dir lists only the kid. The table must
    report the branch/kid/verdict from the seat record + git.

    RED on the pre-fix code: the scanner reads the parent-worktree KID-only
    manifest (a00-* sorts before seat-*), keys rows by kid id, and finds no
    loop branch named after the kid -> an all-dashes row.
    """
    repo = make_project_repo(tmp_path)
    wt = make_round_worktree(repo)
    commit_kid_node(wt)
    write_seat_manifest(repo, "90", status="done")

    res = run_harvest(repo, "--seat", SEAT, "--round", "90")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert "iter-90" in out
    assert BRANCH in out                     # parent-named branch fact
    assert str(wt) in out                    # worktree path fact
    assert "experiment:a00-kid" in out       # kid node id fact
    assert "inconclusive_lean_proved:50" in out  # verdict fact
    # one row for the round, not one per agent
    assert out.count("iter-90") == 1
    assert ".agi/nodes/experiment/a00-kid.md" in out   # diffstat names the node


def test_worktree_removed_still_reports_branch_and_kids(tmp_path: Path) -> None:
    """The branch + diffstat + kids come from git alone once the worktree is
    removed (the durable path the hypothesis names)."""
    repo = make_project_repo(tmp_path)
    wt = make_round_worktree(repo)
    commit_kid_node(wt)
    _git(repo, "worktree", "remove", "--force", str(wt))
    write_seat_manifest(repo, "78", status="done", kid_sessions=False)

    res = run_harvest(repo, "--seat", SEAT, "--round", "78")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert BRANCH in out  # branch discovered from git
    row = [ln for ln in out.splitlines() if ln.startswith("iter-78")][0]
    assert row.split("|")[3].strip() == "-"          # worktree path is a dash
    assert "experiment:a00-kid" in out               # kids read via `git show`
    assert ".agi/nodes/experiment/a00-kid.md" in out


def test_merged_round_recovers_own_changeset(tmp_path: Path) -> None:
    """A round already MERGED into the seat branch has merge-base == its own
    branch tip, so `mb..<branch>` is empty. The table must recover the round's
    OWN changeset from the branch (`<branch>^..<branch>` for a single-commit
    round) and still report kids + a non-empty diffstat naming the round's
    files.

    RED on the pre-fix code: `_harvest_diffstat` diffs `mb..<branch>`, which
    is empty for a merged round -> kids `-` and diffstat `-`.
    """
    repo = make_project_repo(tmp_path)
    wt = make_round_worktree(repo)
    commit_kid_node(wt)
    # create the seat branch at master and merge the round branch into it.
    _git(repo, "branch", SEAT_REF, "master")
    _git(repo, "checkout", SEAT_REF)
    _git(repo, "merge", "--no-ff", BRANCH, "-m", f"merge {BRANCH}")
    _git(repo, "checkout", "master")
    assert _git(repo, "merge-base", SEAT_REF, BRANCH).stdout.strip() == \
        _git(repo, "rev-parse", BRANCH).stdout.strip()
    write_seat_manifest(repo, "91", status="done", kid_sessions=False)

    res = run_harvest(repo, "--seat", SEAT, "--round", "91")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert BRANCH in out
    assert "experiment:a00-kid" in out
    assert ".agi/nodes/experiment/a00-kid.md" in out  # OWN changeset, not empty


def test_live_worktree_round_all_live_filter(tmp_path: Path) -> None:
    """--all-live returns a running round and skips a done round."""
    repo = make_project_repo(tmp_path)
    wt = make_round_worktree(repo)
    commit_kid_node(wt)
    write_seat_manifest(repo, "79", status="running", kid_sessions=False)
    write_seat_manifest(repo, "80", status="done", kid_sessions=False)

    res = run_harvest(repo, "--seat", SEAT, "--all-live")
    assert res.returncode == 0, res.stderr
    assert "iter-79" in res.stdout     # the running round
    assert "iter-80" not in res.stdout  # the done round is filtered out


def test_seat_filter(tmp_path: Path) -> None:
    """--seat keeps only rounds dispatched_by that seat."""
    repo = make_project_repo(tmp_path)
    wt = make_round_worktree(repo)
    commit_kid_node(wt)
    write_seat_manifest(repo, "81", status="done")

    hit = run_harvest(repo, "--seat", SEAT)
    assert "iter-81" in hit.stdout
    miss = run_harvest(repo, "--seat", "other-seat")
    assert "iter-81" not in miss.stdout
    assert "0 rows" in miss.stderr