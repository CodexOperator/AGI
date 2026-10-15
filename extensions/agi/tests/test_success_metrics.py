"""success_metrics.py — shared, not forked (hypothesis:l4-residue-that-is-
recorded-is-still-residue, SITE A).

`record_path` is "The ONE recorded place for a season's success metrics"
(docstring), and the write-log it reads is the same shared room. The
falsifier is PATH EQUALITY: a seat's graph root and the main checkout's graph
root must resolve the SAME success-metrics record path — not merely that each
read succeeds. A seat in a linked git worktree must read/write the season's
durable record on the MAIN checkout, never a per-worktree fork.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

BIN_DIR = Path(__file__).resolve().parents[1] / "bin"
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import success_metrics  # noqa: E402


def _git(cwd: Path, *args: str):
    subprocess.run(["git", "-C", str(cwd), *args], check=True,
                   capture_output=True, text=True)


def _make_project_repo(tmp_path: Path) -> Path:
    """A real git repo with a committed `.agi/` graph dir, on `master`."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    _git(repo, "init", "-b", "master")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    (repo / "README").write_text("x")
    graph = repo / ".agi"
    graph.mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({"metric_primary": "x"}))
    (graph / "nodes").mkdir()
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "init with graph dir")
    return repo


def test_record_path_is_the_same_room_for_seat_and_main(tmp_path):
    """FALSIFIER (SITE A): a seat's groot and the main groot resolve the SAME
    success-metrics record path — path EQUALITY. Under the pre-fix plain
    `Path(root) / "sessions"` join these diverged; through
    `locations.shared_sessions_dir` they meet on the main checkout."""
    repo = _make_project_repo(tmp_path)
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "-b", "loop/slug@s2", str(wt), "master")
    wt_graph = (wt / ".agi").resolve()       # the fork a seat edits
    main_graph = (repo / ".agi").resolve()   # the one shared body
    assert wt_graph != main_graph            # the fork is real

    from locations import find_project_root  # noqa: E402

    assert find_project_root(wt) == wt_graph
    assert find_project_root(repo) == main_graph

    season = 3
    seat_path = success_metrics.record_path(wt_graph, season)
    main_path = success_metrics.record_path(main_graph, season)
    assert seat_path == main_path            # THE falsifier: one room, one path
    # The unified path is the MAIN checkout's room, not the seat's fork.
    assert str(seat_path) == str(main_graph / "sessions" / f"success-metrics-{season}.json")
    assert seat_path != wt_graph / "sessions" / f"success-metrics-{season}.json"