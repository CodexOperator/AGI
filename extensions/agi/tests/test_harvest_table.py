"""Targeted tests for hypothesis:harvest-table-subcommand.

`rotate.py harvest-table --seat S [--round N | --all-live]` prints one row per
(round, kid agent) giving the five facts the director still discovers by hand:

  1. branch   — `loop/<slug>-<agent>@s<N>`, discovered from `git for-each-ref`
                (survives the worktree being removed),
  2. worktree — `.agi/worktrees/<agent>/` path (or `-` once removed),
  3. diffstat against the merge-base with the parent branch (a moved parent
                tip never shifts the base),
  4. the round's kid experiment node ids (added on the branch, under
                `.agi/nodes/experiment/`),
  5. each kid's `verdict`.

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

AGENT = "a00-11112222"
BRANCH = "loop/hypothesis-harvest-table-subc-a00-11112222@s2"
SEAT = "test-seat"


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


def make_worktree(repo: Path) -> Path:
    """The round's worktree + branch, the shape dispatch.py cuts."""
    wt = repo / ".agi" / "worktrees" / AGENT
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


def manifest(iter_id: str, *, dispatched_by: str = SEAT,
             status: str = "running", target: str = "hypothesis:harvest-table-subcommand") -> dict:
    return {
        "iter": iter_id,
        "agents": [{
            "id": AGENT,
            "target": target,
            "strategy": "extend_existing",
            "tier": "kid",
            "status": status,
            "dispatched_by": dispatched_by,
        }],
    }


def run_harvest(main: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "bin" / "rotate.py"),
         "harvest-table", "--root", str(main), *flags],
        capture_output=True, text=True)


def test_completed_round_reports_all_five_facts(tmp_path: Path) -> None:
    """A round harvested into main (manifest under main/.agi/sessions) reports
    branch + worktree + a diffstat from merge-base + the kid node id + the
    kid's verdict, all checked by hand against the fixture."""
    repo = make_project_repo(tmp_path)
    wt = make_worktree(repo)
    commit_kid_node(wt)
    # completed round: manifest harvested into main's sessions dir, worktree
    # still present.
    sess = repo / ".agi" / "sessions" / "iter-77"
    sess.mkdir(parents=True)
    (sess / "manifest.json").write_text(
        json.dumps(manifest("77", status="done")), encoding="utf-8")

    res = run_harvest(repo, "--round", "77")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert "iter-77" in out
    assert AGENT in out
    assert BRANCH in out
    assert str(wt) in out            # worktree path fact
    assert "experiment:a00-kid" in out   # kid node id fact
    assert "inconclusive_lean_proved:50" in out  # verdict fact
    # diffstat against the merge-base: exactly the one kid node file.
    assert ".agi/nodes/experiment/a00-kid.md" in out


def test_worktree_removed_still_reports_branch_and_kids(tmp_path: Path) -> None:
    """The branch + diffstat + kids come from git alone once the worktree is
    removed (the durable path the hypothesis names)."""
    repo = make_project_repo(tmp_path)
    wt = make_worktree(repo)
    commit_kid_node(wt)
    _git(repo, "worktree", "remove", "--force", str(wt))
    sess = repo / ".agi" / "sessions" / "iter-78"
    sess.mkdir(parents=True)
    (sess / "manifest.json").write_text(
        json.dumps(manifest("78", status="done")), encoding="utf-8")

    res = run_harvest(repo, "--round", "78")
    assert res.returncode == 0, res.stderr
    out = res.stdout
    assert BRANCH in out                     # branch discovered from git
    assert "worktrees/a00-11112222" not in out.split("|")[3] or \
        str(wt) not in out                   # worktree path is a dash
    row = [ln for ln in out.splitlines() if ln.startswith("iter-78")][0]
    worktree_field = row.split("|")[3].strip()
    assert worktree_field == "-"
    assert "experiment:a00-kid" in out       # kids read via `git show`
    assert ".agi/nodes/experiment/a00-kid.md" in out


def test_live_worktree_round_all_live_filter(tmp_path: Path) -> None:
    """A live round keeps its manifest inside the worktree's sessions dir;
    --all-live returns it, and --all-live skips a done round."""
    repo = make_project_repo(tmp_path)
    wt = make_worktree(repo)
    commit_kid_node(wt)
    # manifest for THIS live round lives under the worktree, not main.
    sess = wt / ".agi" / "sessions" / "iter-79"
    sess.mkdir(parents=True)
    (sess / "manifest.json").write_text(
        json.dumps(manifest("79", status="running")), encoding="utf-8")
    # a second, done round harvested into main.
    done = repo / ".agi" / "sessions" / "iter-80"
    done.mkdir(parents=True)
    (done / "manifest.json").write_text(
        json.dumps(manifest("80", status="done")), encoding="utf-8")

    res = run_harvest(repo, "--all-live")
    assert res.returncode == 0, res.stderr
    assert "iter-79" in res.stdout     # the live round (from the worktree)
    assert "iter-80" not in res.stdout  # the done round is filtered out


def test_seat_filter(tmp_path: Path) -> None:
    """--seat keeps only rounds dispatched_by that seat."""
    repo = make_project_repo(tmp_path)
    wt = make_worktree(repo)
    commit_kid_node(wt)
    sess = repo / ".agi" / "sessions" / "iter-81"
    sess.mkdir(parents=True)
    (sess / "manifest.json").write_text(
        json.dumps(manifest("81", status="done")), encoding="utf-8")

    hit = run_harvest(repo, "--seat", SEAT)
    assert "iter-81" in hit.stdout
    miss = run_harvest(repo, "--seat", "other-seat")
    assert "iter-81" not in miss.stdout
    assert "0 rows" in miss.stderr


def _commit_node(wt: Path, name: str, node_id: str, msg: str) -> None:
    """Write + commit one experiment kid node under wt/.agi/nodes."""
    n = wt / ".agi" / "nodes" / "experiment"
    n.mkdir(parents=True, exist_ok=True)
    p = n / name
    p.write_text(
        f"---\nid: {node_id}\ntype: experiment\nverdict: proved\n---\n\n{msg}\n",
        encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-m", msg)


def test_git_base_resolved_per_agent_prevents_cross_round_over_attribution(
        tmp_path: Path) -> None:
    """Round B branches from round A's branch; both worktrees present; main is
    left on master (NOT round A's branch). Each manifest records its agent's
    base_branch. `harvest-table --round B` must diff round B against ITS OWN
    manifest base_branch (round A's branch), so it lists kid B and NOT kid A.

    This is the live falsifier of hypothesis:harvest-table-subcommand: the
    main checkout's checked-out branch is not the round's base, and a stale
    single `parent` (main's branch) over-attributes earlier rounds' kids to a
    later round.

    RED-FIRST: on the pre-fix code (parent = main's current branch = master)
    round B's merge-base is master and `master..BRANCH_B` spans BOTH kid A and
    kid B, so the assertion that kid A is absent FAILS before the fix.
    """
    repo = make_project_repo(tmp_path)   # init'd on master, main stays there

    AGENT_A = "a00-11112222"
    AGENT_B = "a00-33334444"
    BRANCH_A = "loop/hypothesis-harvest-tbl-a-a00-11112222@s2"
    BRANCH_B = "loop/hypothesis-harvest-tbl-b-a00-33334444@s2"

    # round A: branch cut from master, commits kid A (its base_branch: master)
    wtA = repo / ".agi" / "worktrees" / AGENT_A
    _git(repo, "worktree", "add", "-b", BRANCH_A, str(wtA), "master")
    _commit_node(wtA, "a00-kidA.md", "experiment:a00-kidA", "kid A")

    # round B: branch cut from round A's branch, commits kid B
    # (its base_branch: round A's branch)
    wtB = repo / ".agi" / "worktrees" / AGENT_B
    _git(repo, "worktree", "add", "-b", BRANCH_B, str(wtB), BRANCH_A)
    _commit_node(wtB, "a00-kidB.md", "experiment:a00-kidB", "kid B")

    def manifest_agent(agent_id: str, base_branch: str, target: str) -> dict:
        return {
            "id": agent_id, "base_branch": base_branch, "target": target,
            "dispatched_by": SEAT, "status": "done",
        }

    sess_a = repo / ".agi" / "sessions" / "iter-A"
    sess_a.mkdir(parents=True)
    (sess_a / "manifest.json").write_text(json.dumps({"iter": "A", "agents": [
        manifest_agent(AGENT_A, "master", "hypothesis:harvest-table-subcommand")]}),
        encoding="utf-8")
    sess_b = repo / ".agi" / "sessions" / "iter-B"
    sess_b.mkdir(parents=True)
    (sess_b / "manifest.json").write_text(json.dumps({"iter": "B", "agents": [
        manifest_agent(AGENT_B, BRANCH_A, "hypothesis:harvest-table-subcommand")]}),
        encoding="utf-8")

    res_b = run_harvest(repo, "--round", "iter-B")
    assert res_b.returncode == 0, res_b.stderr
    assert BRANCH_B in res_b.stdout
    assert "experiment:a00-kidB" in res_b.stdout   # round B's own kid
    assert "experiment:a00-kidA" not in res_b.stdout  # NOT round A's kid

    res_a = run_harvest(repo, "--round", "iter-A")
    assert res_a.returncode == 0, res_a.stderr
    assert BRANCH_A in res_a.stdout
    assert "experiment:a00-kidA" in res_a.stdout   # round A's own kid