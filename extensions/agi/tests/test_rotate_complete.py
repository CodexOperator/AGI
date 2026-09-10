"""Targeted tests for hypothesis:l4-seat-session-iter-dirs, HALF (b).

SESSION-COMPLETE (`rotate.py complete`) retires a seat worktree:

  1. REFUSES unless the seat branch is already an ancestor of its parent
     branch (the merge-up prerequisite) — exit non-zero, REMOVE NOTHING.
  2. On an ancestor branch: COPIES the worktree's `.agi/sessions/iter-*` dirs
     into the MAIN checkout's `.agi/sessions/` (an explicit copy, because
     `sessions/` is gitignored so a merge carries nothing).
  3. NEVER overwrites an existing same-name dir in main — main's copy stays
     byte-for-byte intact and the command says it skipped.
  4. Only then removes the worktree (`git worktree remove`) and the branch.
     NO node is ever deleted: the seat's tracked content is already an
     ancestor of the parent branch, so removing the worktree + branch loses
     no graph object. Uncommitted work (a dirty worktree) is a REFUSAL.

Red-first. Builds a real git repo + a `--branch`-style worktree (the same
shape dispatch.py produces) and drives `rotate.main(['complete', ...])`.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True)


def _make_project_repo(tmp_path: Path) -> Path:
    """A real git repo with a committed `.agi/` graph dir and a `.gitignore`
    that ignores `sessions/` (as the real repo does) so a worktree holding
    only session dirs is not dirty. On branch `master`."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x")
    # sessions/ must be ignored: a worktree whose only untracked files are
    # ignored ones must read as CLEAN (and git worktree remove must succeed).
    (repo / ".gitignore").write_text("sessions/\n.agi/sessions/\n"
                                     "!.agi/sessions/rotations/\n")
    graph = repo / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text('{"metric_primary": "outcome_coverage"}')
    (graph / "nodes").mkdir(exist_ok=True)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init with graph dir + gitignore")
    return repo


def _make_worktree(repo: Path, tmp_path: Path, name: str = "wt",
                   branch: str = "loop/t-a00@1") -> Path:
    wt = tmp_path / name
    _git(repo, "worktree", "add", "-b", branch, str(wt), "master")
    return wt


def _write_session_iter(wt: Path, name: str = "iter-99") -> Path:
    d = wt / ".agi" / "sessions" / name
    d.mkdir(parents=True)
    (d / "agent.json").write_text('{"id": "a00-x", "status": "running"}')
    (d / "output.log").write_text("round log\n")
    return d


def _commit_node_on_seat_branch(wt: Path, content: str = "unique node body") -> None:
    n = wt / ".agi" / "nodes" / "experiment"
    n.mkdir(parents=True, exist_ok=True)
    (n / "round-node.md").write_text(
        f"---\nid: experiment:round-node\ntype: experiment\n---\n\n{content}\n",
        encoding="utf-8")
    _git(wt, "add", "-A")
    _git(wt, "commit", "-m", "seat round node")


def _merge_seat_into(repo: Path, branch: str, parent: str = "master") -> None:
    """Merge the seat branch into `parent` so the seat branch becomes an
    ancestor of it (the merge-up home). Runs from the main checkout."""
    _git(repo, "checkout", "-q", parent)
    _git(repo, "merge", "-q", "--no-ff", "-m", f"merge {branch}", branch)


# --- proof bar 1: refuses on a non-ancestor branch, removes NOTHING ---------


def test_refuses_on_non_ancestor_and_removes_nothing(tmp_path):
    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)
    # Seat does real work: a committed node AND a session iter dir — but the
    # branch is NOT merged into master, so it is not an ancestor.
    _commit_node_on_seat_branch(wt)
    sess = _write_session_iter(wt)

    assert _git(repo, "merge-base", "--is-ancestor",
                "loop/t-a00@1", "master").returncode != 0  # precondition

    rc = rotate.main(["complete", "--worktree", str(wt), "--parent", "master"])
    assert rc != 0
    # Nothing removed: worktree dir, branch, session dir all still present,
    # and main got NO session dir.
    assert wt.is_dir()
    assert sess.is_dir()
    assert "loop/t-a00@1" in _git(repo, "branch").stdout
    assert not (repo / ".agi" / "sessions" / "iter-99").exists()
    # The refusal names the missing merge-up.
    assert "not an ancestor" in rotate_last_stderr()


def test_refuses_on_dirty_worktree_even_when_ancestor(tmp_path):
    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)
    _commit_node_on_seat_branch(wt)
    _merge_seat_into(repo, "loop/t-a00@1")          # ancestor now
    # Uncommitted node file = a dirty worktree = session not complete.
    (wt / ".agi" / "nodes" / "experiment" / "uncommitted.md").write_text(
        "---\nid: experiment:uncommitted\ntype: experiment\n---\n\nuncommitted\n")
    # A session dir as well.
    _write_session_iter(wt)

    rc = rotate.main(["complete", "--worktree", str(wt), "--parent", "master"])
    assert rc != 0
    assert wt.is_dir()
    assert "loop/t-a00@1" in _git(repo, "branch").stdout
    assert not (repo / ".agi" / "sessions" / "iter-99").exists()
    assert "uncommitted" in rotate_last_stderr()


# --- proof bar 2: ancestor branch → iter dirs in main, worktree+branch gone --


def test_ancestor_branch_harvests_dirs_and_retires_seat(tmp_path):
    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)
    _commit_node_on_seat_branch(wt)
    sess = _write_session_iter(wt)
    sub = _write_session_iter(wt, name="iter-100")
    # Snapshot the source logs BEFORE the worktree is removed.
    sess_log = (sess / "output.log").read_text()
    sub_log = (sub / "output.log").read_text()
    _merge_seat_into(repo, "loop/t-a00@1")

    rc = rotate.main(["complete", "--worktree", str(wt), "--parent", "master"])
    assert rc == 0, rotate_last_stderr()

    # Both iter dirs now resident in main, byte-equal to the source.
    for name, log in (("iter-99", sess_log), ("iter-100", sub_log)):
        dst = repo / ".agi" / "sessions" / name
        assert (dst / "agent.json").is_file()
        assert (dst / "output.log").read_text() == log
    # Worktree and branch are gone.
    assert not wt.exists()
    assert "loop/t-a00@1" not in _git(repo, "branch").stdout
    # The seat's node is preserved in main's history (see proof bar 4).


# --- proof bar 3: an existing same-name dir in main is NEVER overwritten -----


def test_existing_same_name_dir_in_main_is_left_byte_for_byte(tmp_path):
    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)
    _commit_node_on_seat_branch(wt)
    # Main ALREADY owns iter-99 with distinct content; the seat also has one.
    pre = repo / ".agi" / "sessions" / "iter-99"
    pre.mkdir(parents=True)
    pre_file = pre / "agent.json"
    pre_file.write_text('{"id": "main-owned", "round": "pre-existing"}')
    pre_marker = pre / "sentinel.bin"
    pre_marker.write_bytes(b"\x00\x01\x02main-owned-mark")
    incoming = _write_session_iter(wt, name="iter-99")
    incoming_new = (incoming / "agent.json")
    incoming_new.write_text('{"id": "a00-x", "round": "incoming"}')
    _merge_seat_into(repo, "loop/t-a00@1")

    rc = rotate.main(["complete", "--worktree", str(wt), "--parent", "master"])
    assert rc == 0, rotate_last_stderr()
    assert "skip iter-99" in rotate_last_stdout()
    # Main's copy is byte-for-byte untouched.
    assert pre_file.read_text() == '{"id": "main-owned", "round": "pre-existing"}'
    assert pre_marker.read_bytes() == b"\x00\x01\x02main-owned-mark"
    # And nothing ELSE was planted under iter-99 by us.
    assert not (pre / "copied-by-complete.exe").exists()
    # Seat still retired despite the skip.
    assert not wt.exists()
    assert "loop/t-a00@1" not in _git(repo, "branch").stdout


# --- proof bar 4: no node deleted in any path -------------------------------


def test_no_node_deleted_after_retirement(tmp_path):
    repo = _make_project_repo(tmp_path)
    wt = _make_worktree(repo, tmp_path)
    body = "the one true node body"
    _commit_node_on_seat_branch(wt, content=body)
    _write_session_iter(wt)

    # The node first exists in the worktree fork and NOT in main (before any
    # merge carries it home).
    assert (wt / ".agi" / "nodes" / "experiment" / "round-node.md").is_file()
    assert not (repo / ".agi" / "nodes" / "experiment" / "round-node.md").exists()

    _merge_seat_into(repo, "loop/t-a00@1")
    # The merge-up carried the node home; complete must not lose it.
    assert (repo / ".agi" / "nodes" / "experiment" / "round-node.md").is_file()

    rc = rotate.main(["complete", "--worktree", str(wt), "--parent", "master"])
    assert rc == 0, rotate_last_stderr()

    # Worktree now gone — but the node's content is resident in main via the
    # merged parent branch: nothing was deleted from the graph, it moved home.
    assert not wt.exists()
    assert body in _git(repo, "show",
                       "master:.agi/nodes/experiment/round-node.md").stdout


# --- helpers for capturing output -------------------------------------------

_LAST_OUT: list[str] = []
_LAST_ERR: list[str] = []

_ORIG_MAIN = rotate.main


def rotate_last_stdout() -> str:
    return "\n".join(_LAST_OUT)


def rotate_last_stderr() -> str:
    return "\n".join(_LAST_ERR)


def _capture(argv: list[str]) -> int:
    import contextlib
    import io
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = _ORIG_MAIN(argv)
    _LAST_OUT[:] = [ln for ln in out.getvalue().splitlines()]
    _LAST_ERR[:] = [ln for ln in err.getvalue().splitlines()]
    return rc


# Patch rotate.main's return path: tests call `rotate.main(...)` directly and
# also need the captured stdout/stderr for the refusal/skip assertions.
rotate.main = _capture  # type: ignore[assignment]