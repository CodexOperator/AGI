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
                        kid_sessions: bool = True,
                        base_branch: str = SEAT_REF) -> None:
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
            "base_branch": base_branch,
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


def test_merged_round_reports_dash_no_own_commits(tmp_path: Path) -> None:
    """A round already MERGED into the seat branch has every commit reachable
    from the seat, so it owns nothing of its own: rev-list `<round> ^<seat>` is
    empty and the row reports `-` with no kids — never the seat's commit or a
    stale `<round_branch>^` changeset (hypothesis:
    l4-harvest-table-attributes-only-the-rounds-own-commits). The old
    `_harvest_diffstat` recovered the changeset from `<branch>^..<branch>`,
    which on a ZERO-commit round attributed the SEAT's commit to the round —
    the over-attribution this hypothesis removes. Once the round's work is
    merged into the seat there is nothing PENDING on the branch to harvest,
    so `-` is the honest row.

    RED on the pre-fix code: `_harvest_diffstat` diffs `mb..<branch>`, which is
    empty for a merged round, then falls into the `<branch>^..<branch>`
    recovery and reports the (seat-merged) changeset.
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
    row = [ln for ln in out.splitlines() if ln.startswith("iter-91")][0]
    assert row.split("|")[4].strip() == "-"       # diffstat-vs-merge-base
    assert row.split("|")[5].strip() == "-"       # kids column
    assert "experiment:a00-kid" not in out


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

# --- over-attribution guard (hypothesis:l4-harvest-...) ---------------------
def test_zero_commit_round_reports_dash_not_the_seat_commit(tmp_path: Path) -> None:
    """A round whose branch tip IS the seat commit it was cut from (the round
    added nothing of its own) must report `-` for diffstat and `-` for kids —
    NEVER the seat commit's file. The old `_harvest_diffstat` fallback
    `<branch>^..<branch>` on a zero-commit branch attributed the SEAT's
    previous commit to the round (the L4.2xx over-attribution this
    hypothesis fixes). FALSIFIER: a zero-commit fixture round whose row names
    a file the seat commit touched.
    """
    repo = make_project_repo(tmp_path)
    wt = make_round_worktree(repo)
    # move the SEAT: create the seat ref at master, add a file to it (a seat
    # commit), then re-cut the round branch AT the seat tip — so the round
    # branch tip IS the seat commit (a zero-commit round that owns nothing).
    _git(repo, "branch", SEAT_REF, "master")
    _git(repo, "checkout", SEAT_REF)
    (repo / ".agi" / "seat-file").write_text("touched by the seat",
                                               encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "-c", "core.hooksPath=/dev/null", "commit",
         "-m", "seat commit touching a file")
    _git(repo, "checkout", "master")
    # re-cut the round branch at the seat ref (== the seat commit) with NO
    # own commits.
    _git(repo, "worktree", "remove", "--force", str(wt))
    _git(repo, "branch", "-D", BRANCH)
    wt = repo / ".agi" / "worktrees" / PARENT
    _git(repo, "worktree", "add", "-b", BRANCH, str(wt), SEAT_REF)
    wt_branch_tip = _git(repo, "rev-parse", BRANCH).stdout.strip()
    seat_tip = _git(repo, "rev-parse", SEAT_REF).stdout.strip()
    assert wt_branch_tip == seat_tip   # zero-commit round fixture
    write_seat_manifest(repo, "92", status="done")

    res = run_harvest(repo, "--seat", SEAT, "--round", "92")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    row = [ln for ln in out.splitlines() if ln.startswith("iter-92")][0]
    assert row.split("|")[4].strip() == "-"      # diffstat: nothing of the round
    assert row.split("|")[5].strip() == "-"      # kids: none
    assert ".agi/seat-file" not in out           # NEVER the seat commit's file
    assert ".agi/nodes/experiment/a00-kid.md" not in row  # not even the disk kid


def test_seat_moved_after_dispatch_excludes_the_later_seat_commit(
        tmp_path: Path) -> None:
    """A fixture where the SEAT moved after dispatch: the seat's LATER commit
    must NOT appear in the round's row. The round was cut at the older seat
    state, so its own commits exclude anything the seat added afterwards —
    rev-list `<round> ^<seat>` re-derives the round's changes against the
    seat's current tip, and the later seat file is not reachable from the
    round and not part of `<first_own>^..<round>`.
    """
    repo = make_project_repo(tmp_path)
    wt = make_round_worktree(repo)
    commit_kid_node(wt)
    # move the seat after dispatch: touch a NEW file on the seat ref.
    _git(repo, "branch", SEAT_REF, "master")
    _git(repo, "checkout", SEAT_REF)
    (repo / ".agi" / "seat-after-dispatch").write_text(
        "added by the seat AFTER the round was cut", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "-c", "core.hooksPath=/dev/null", "commit",
         "-m", "seat moved after dispatch")
    _git(repo, "checkout", "master")
    write_seat_manifest(repo, "93", status="done")

    res = run_harvest(repo, "--seat", SEAT, "--round", "93")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert "experiment:a00-kid" in out                  # round's own kid present
    assert ".agi/nodes/experiment/a00-kid.md" in out
    assert ".agi/seat-after-dispatch" not in out        # later seat commit absent


def test_two_commit_round_reports_both_commits_files(tmp_path: Path) -> None:
    """A round with several commits (kid commit + a parent `done:` commit, or
    a director fix-up) must report BOTH commits' files. The old
    `<round_branch>^..<round_branch>` recovery on a multi-commit branch
    reported only the TIP commit's changeset (the under-attribution half of
    the bug). FALSIFIER: a two-commit fixture whose row misses the first
    commit's file.
    """
    repo = make_project_repo(tmp_path)
    wt = make_round_worktree(repo)
    commit_kid_node(wt, name="a00-kid1.md", node_id="experiment:a00-kid1")
    # a second own commit on the branch (e.g. the parent's `done:` stamp).
    n = wt / ".agi" / "nodes" / "experiment"
    p = n / "a00-kid2.md"
    p.write_text("---\nid: experiment:a00-kid2\ntype: experiment\n"
                 "verdict: proved\n---\n\nsecond round commit\n",
                 encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "-c", "core.hooksPath=/dev/null", "commit", "-m", "done: stamp")
    write_seat_manifest(repo, "94", status="done")

    res = run_harvest(repo, "--seat", SEAT, "--round", "94")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert "experiment:a00-kid1" in out   # FIRST commit's file (the old bug)
    assert "experiment:a00-kid2" in out   # TIP commit's file
    assert ".agi/nodes/experiment/a00-kid1.md" in out
    assert ".agi/nodes/experiment/a00-kid2.md" in out


def test_season_resolved_seat_ref_is_the_diff_base(tmp_path: Path) -> None:
    """The seasonal seat ref `seat/<S>@s<N>` is the round's diff base.

    Hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits.
    The `@s<N>` segment must be built as `@s{season}` -- a `@2`-style literal
    (int season interpolated raw) builds `seat/<S>@2`, which NO `seat/` ref in
    this repo matches (the real refs are `seat/<S>@s2`), so rev-parse fails and
    `seat_base` collapses to "". The round is then diffed against the
    manifest's base_branch instead -- which here is a DELIBERATELY wrong,
    ancestor base (master) that sits BEFORE the seat's own commit. Only the
    season-resolved `seat/<S>@s2` can separate the round's own kid commit from
    the seat's own file.

    FALSIFIER: a round genuinely CUT from the seat ref whose manifest lies
    that base_branch is an ancestor (master). On the malformed ref the seat's
    OWN file leaks into the round's diffstat; on the fix only the round's kid
    shows and the seat's file is excluded.
    """
    repo = make_project_repo(tmp_path)
    # Give the seat ref an OWN commit (a file only the seat owns), then cut
    # the round branch FROM the seat tip -- so the round derives from the
    # seat, not from master. A wrong base_branch of master (an ancestor of
    # everything) can only be rescued by the season-resolved seat ref.
    _git(repo, "branch", SEAT_REF, "master")
    _git(repo, "checkout", SEAT_REF)
    (repo / ".agi" / "seat-owned.txt").write_text("only the seat owns this",
                                                  encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "-c", "core.hooksPath=/dev/null", "commit",
         "-m", "seat own commit")
    _git(repo, "checkout", "master")
    # round worktree is the parent's, cut from the seat tip
    wt = repo / ".agi" / "worktrees" / PARENT
    _git(repo, "worktree", "add", "-b", BRANCH, str(wt), SEAT_REF)
    commit_kid_node(wt)
    # base_branch is a lie: master is an ancestor, not the round's real base.
    # Only the season-resolved `seat/<S>@s2` names the true base.
    write_seat_manifest(repo, "95", status="done", base_branch="master")

    res = run_harvest(repo, "--seat", SEAT, "--round", "95")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert BRANCH in out
    assert "experiment:a00-kid" in out   # the round's OWN kid is present
    assert ".agi/nodes/experiment/a00-kid.md" in out  # git-diff names the node
    assert "seat-owned.txt" not in out   # the seat's own file NEVER leaks in


def test_canonical_round_branch_is_attributed(tmp_path: Path) -> None:
    """hypothesis:l4-branches-follow-the-season-grammar — a round cut on the
    canonical `season2/loops/<slug>-<parent-id>` spelling (what dispatch.py
    mints today) must be attribute-able by harvest-table. The old
    `for-each-ref refs/heads/loop` glob + `^.*-(a00-<hex>)@s<N>` regex
    never saw the canonical spelling, so the branch fact and the season
    fallback (`max` over the discovered loop seasons) were blind to it. RED
    on the pre-fix code: the canonical branch is not discovered, the season
    resolves to nothing, and the row cannot separate the round's own kid
    from the manifest base."""
    repo = make_project_repo(tmp_path)
    cbranch = "season2/loops/hypothesis-branches-follow-the-seas-a00-feedbeef"
    wt = repo / ".agi" / "worktrees" / PARENT
    _git(repo, "worktree", "add", "-b", cbranch, str(wt), "master")
    commit_kid_node(wt)
    write_seat_manifest(repo, "96", status="done", branch=cbranch)
    # sanity: git resolves the canonical branch, and the parsed loop carries
    # the parent agent (so the manifest-join / branch fact agree with git).
    assert _git(repo, "rev-parse", "--verify", "--quiet",
                cbranch).stdout.strip() != ""

    res = run_harvest(repo, "--seat", SEAT, "--round", "96")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert cbranch in out                     # canonical branch fact
    assert "experiment:a00-kid" in out        # kid node id fact
    assert ".agi/nodes/experiment/a00-kid.md" in out  # diffstat names the node


def test_post_seat_ref_is_the_diff_base(tmp_path: Path) -> None:
    """hypothesis:l4-a-seat-is-a-post-everywhere — the seasonal seat ref,
    once renamed to a POST, is still resolved as the round's diff base. The
    seat ref is created as `post/<S>@s2` (the seat- spelling is the deprecated
    alias); the diff-base resolver must find the ACTUAL `post/` spelling and
    never fall back to a wrong ancestor base_branch."""
    repo = make_project_repo(tmp_path)
    post_ref = f"post/{SEAT}@s2"
    _git(repo, "branch", post_ref, "master")
    _git(repo, "checkout", post_ref)
    (repo / ".agi" / "seat-owned.txt").write_text(
        "only the seat owns this", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "-c", "core.hooksPath=/dev/null", "commit",
         "-m", "seat own commit")
    _git(repo, "checkout", "master")
    wt = repo / ".agi" / "worktrees" / PARENT
    _git(repo, "worktree", "add", "-b", BRANCH, str(wt), post_ref)
    commit_kid_node(wt)
    # base_branch is a lie: master is an ancestor, not the round's real base.
    # Only the post/ spelling of the seat ref names the true base.
    write_seat_manifest(repo, "95", status="done", base_branch=post_ref)

    res = run_harvest(repo, "--seat", SEAT, "--round", "95")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert BRANCH in out
    assert "experiment:a00-kid" in out
    assert ".agi/nodes/experiment/a00-kid.md" in out
    assert "seat-owned.txt" not in out   # the seat's own file NEVER leaks in
