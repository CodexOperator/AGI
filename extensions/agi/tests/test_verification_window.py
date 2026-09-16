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
import re
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


# ---------------------------------------------------------------------------
# The lock line names WHO holds it. Measured cost: the master-sensei spent 17
# calls before the first (d) on belam 181151Z -- 5 of them hand calls after
# `window` on a HELD lock printed only `lock: held by <pid> since <ts>`, to
# learn who that pid was. One line now carries pid, age, tree, command head,
# and -- when any pid on the holder's ppid chain is a registered spawn-budget
# runner -- that runner's agent id, tier and iter. A dead or unreadable
# `/proc` entry degrades to `unresolved`; `lock: free` is untouched.
#
# The process table is a FAKE `PROC` (module constant), so none of this
# depends on the box's real `proc` or a real spawned process.

import spawn_budget  # noqa: E402


def _fake_proc(tmp_path: Path, pid: int, *, cwd=None, ppid=None, cmd=None) -> Path:
    """A minimal fake process table: `PROC/<pid>/{cwd,status,cmdline}`."""
    proc = tmp_path / "proc"
    d = proc / str(pid)
    d.mkdir(parents=True, exist_ok=True)
    if cwd is not None:
        (d / "cwd").symlink_to(cwd)
    if ppid is not None:
        (d / "status").write_text(f"Name:\tx\nPPid:\t{ppid}\n", encoding="utf-8")
    if cmd is not None:
        (d / "cmdline").write_bytes(cmd)
    return proc


def _held(tmp_path, monkeypatch, pid):
    """A fixture groot whose lock names the (live) `pid`, with `PROC` faked."""
    _make_groot(tmp_path, lock=True)
    lock = tmp_path / "sessions" / verification.SUITE_LOCK
    lock.write_text(str(pid), encoding="utf-8")
    return tmp_path


def test_window_names_tree_age_and_command_of_a_worktree_holder(tmp_path, monkeypatch):
    """A live holder whose cwd is inside `.agi/worktrees/<name>` -> the post
    name, an age in seconds, and the cmdline head, all on the one lock line."""
    pid = os.getppid()                       # alive, and != os.getpid()
    wt = tmp_path / ".agi" / "worktrees" / "a00-cafe1234"
    wt.mkdir(parents=True)
    proc = _fake_proc(tmp_path, pid, cwd=wt, ppid=1,
                      cmd=b"python3\x00-m\x00pytest\x00extensions/agi/tests")
    groot = _held(tmp_path, monkeypatch, pid)
    monkeypatch.setattr(verification, "PROC", proc)
    line = [l for l in verification.render_window(groot).splitlines()
            if l.startswith("lock:")][0]
    assert f"lock: held by {pid} since " in line
    assert "tree a00-cafe1234" in line
    assert re.search(r"age \d+s", line)
    assert "cmd python3 -m pytest extensions/agi/tests" in line


def test_window_names_main_when_the_holder_sits_in_the_main_checkout(tmp_path, monkeypatch):
    """A holder whose cwd IS the main checkout prints `tree main`."""
    pid = os.getppid()
    proc = _fake_proc(tmp_path, pid, cwd=tmp_path, ppid=1, cmd=b"bash\x00run.sh")
    groot = _held(tmp_path, monkeypatch, pid)
    monkeypatch.setattr(verification, "PROC", proc)
    out = verification.render_window(groot)
    assert "tree main" in out


def test_window_names_the_registered_runner_behind_the_holder(tmp_path, monkeypatch):
    """A pid on the holder's ppid chain that matches a LIVE spawn-budget lease
    appends that runner's agent id, tier and iter -- read through the budget
    reader, not a second parse of the budget dir."""
    holder, runner, grandparent = os.getppid(), 1, 1
    # the holder's PARENT is the registered runner: 2 ppid hops from the pid
    proc = _fake_proc(tmp_path, holder, cwd=tmp_path, ppid=runner,
                      cmd=b"claude\x00--resume")
    _fake_proc(tmp_path, runner, ppid=grandparent)
    groot = _held(tmp_path, monkeypatch, holder)
    lease_dir = spawn_budget.budget_dir(groot)
    lease_dir.mkdir(parents=True, exist_ok=True)
    (lease_dir / "a00-deadbeef123456.lease").write_text(json.dumps({
        "agent_id": "a00-deadbeef123456", "tier": "kid", "iter": 7,
        "agent_pid": runner, "holder_pid": runner,
    }), encoding="utf-8")
    monkeypatch.setattr(verification, "PROC", proc)
    out = verification.render_window(groot)
    assert "runner a00-deadbeef123456 tier=kid iter=7" in out


def test_window_lock_line_degrades_and_free_is_byte_identical(tmp_path, monkeypatch):
    """An unreadable `/proc` entry degrades to `unresolved` and never raises;
    `lock: free` is byte-for-byte what it always was."""
    pid = os.getppid()
    groot = _held(tmp_path, monkeypatch, pid)
    monkeypatch.setattr(verification, "PROC", tmp_path / "proc")  # empty table
    out = verification.render_window(groot)   # must not raise
    assert f"lock: held by {pid} " in out
    assert "tree unresolved" in out and "cmd unresolved" in out
    free = tmp_path / "free"
    free.mkdir()
    _make_groot(free)
    assert [l for l in verification.render_window(free).splitlines()
            if l.startswith("lock:")] == ["lock: free"]
