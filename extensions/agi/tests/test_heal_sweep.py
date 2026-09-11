"""Tests for hypothesis:l4-a-finished-rounds-worktree-is-removed-after-harvest.

`heal.py watch` gains a `_sweep_finished_worktrees(root)` pass, run once per
watch pass after the round reaping, that REMOVES an agent worktree under
`<main>/.agi/worktrees/a00-*` only when ALL hold:
  (1) no live spawn-budget lease names the agent (the lease dir is the
      liveness source, never ps by name);
  (2) the worktree's HEAD is an ancestor of the branch it was cut from
      (a round that never landed is NOT removed);
  (3) `git status --porcelain` is empty apart from `.agi/sessions/` paths
      (a dirty tree is REFUSED by name, never forced);
  (4) the round's session dir has come home to the main checkout, or the
      worktree carries no `iter-*` dir at all;
  (5) the worktree dir is older than the grace (`reaper.worktree_grace_min`,
      default 30; `.agi/config.json` is read, never edited).
Removal is `git -C <main> worktree remove <wt>` WITHOUT `--force`, then
`git worktree prune`; the `loop/...` BRANCH is kept. There is also a
`heal.py sweep --root <main> --dry-run` subcommand that prints the same
`[sweep]` lines and removes nothing, and `heal.py sweep -h` exits 0.

The fixture is a REAL git main repo (git is reachable, tmux/ps are never
touched): base branch `season/s2`, four agent worktrees cut as `loop/...`
branches — one merged-and-clean-and-homed (removed), one with a modified
node file (refused dirty), one with a live lease (kept), one whose HEAD never
landed (refused unmerged).
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, BIN / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


heal = _load("heal")
spawn_budget = _load("spawn_budget")


def _sh(*args: str) -> None:
    """Run a git command; raise with stderr on failure (a fixture that cannot
    set up is a test error, not a silent skip)."""
    out = subprocess.run(list(args), capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"{args}: {out.stderr}")


@pytest.fixture
def repo_root(tmp_path: Path) -> Path:
    """A real git main checkout with a minimal `.agi/` graph whose config sets
    a zero grace so freshly-cut fixture worktrees are immediately reapable."""
    repo = tmp_path / "repo"
    graph = repo / ".agi"
    (graph / "nodes").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"reaper": {"worktree_grace_min": 0}}))
    _sh("git", "init", "-b", "season/s2", str(repo))
    _sh("git", "-C", str(repo), "config", "user.email", "t@example.com")
    _sh("git", "-C", str(repo), "config", "user.name", "t")
    # Mirror the real repo's gitignore (hypothesis:l4-a-finished-rounds-
    # worktree-is-removed-after-harvest): `.agi/sessions/` and `.agi/worktrees/`
    # are IGNORED, which is what lets `git worktree remove` (no --force) free a
    # finished round's tree despite its per-worktree session residue -- without
    # the ignore those bytes are UNTRACKED and git refuses the removal.
    (repo / ".gitignore").write_text(".agi/sessions/\n.agi/worktrees/\n")
    (repo / "base.txt").write_text("base\n")
    (graph / "nodes" / "root.md").write_text("# root\n")
    _sh("git", "-C", str(repo), "add", "-A")
    _sh("git", "-C", str(repo), "commit", "-q", "-m", "init")
    return repo


def _graph(repo: Path) -> Path:
    return repo / ".agi"


def _cut(repo: Path, agent_id: str, branch: str,
         base: str = "season/s2") -> Path:
    """`git worktree add <graph>/worktrees/<agent> -b <branch> <base>`."""
    wt = _graph(repo) / "worktrees" / agent_id
    _sh("git", "-C", str(repo), "worktree", "add", "-b", branch,
        str(wt), base)
    return wt


def _stamp_round(wt: Path, iter_name: str, agent_id: str, base: str) -> None:
    """Write the round's session records into a worktree, the same shape
    dispatch writes them: a top-level `agent.json` carrying `base_branch`
    (the tuple season.py merge-up climbs) and a manifest with no running
    agents (so `_watch_round` over it is a pure no-op)."""
    it = wt / ".agi" / "sessions" / iter_name
    it.mkdir(parents=True, exist_ok=True)
    (it / "agent.json").write_text(json.dumps(
        {"id": agent_id, "status": "done", "base_branch": base}))
    (it / "manifest.json").write_text(json.dumps(
        {"timeout_seconds": 600, "agents": []}))


def _home(repo: Path, iter_name: str) -> None:
    """The round's session dir `come home` to the main checkout."""
    (_graph(repo) / "sessions" / iter_name).mkdir(parents=True, exist_ok=True)


def _lease(repo: Path, agent_id: str) -> None:
    """A fake live lease in the shared spawn-budget dir naming `agent_id`.
    `holder_pid` is this test process, so `_lease_is_live` (os.kill(pid,0))
    sees it as genuinely live -- liveness is the lease dir, never ps by name."""
    budget = _graph(repo) / "sessions" / ".spawn-budget"
    budget.mkdir(parents=True, exist_ok=True)
    (budget / f"{agent_id}.lease").write_text(json.dumps(
        {"agent_id": agent_id, "holder_pid": os.getpid(),
         "agent_pid": os.getpid(), "iter": 1, "status": "running"}))


@pytest.fixture
def four_worktrees(repo_root: Path):
    """A released (merged+clean+homed), a dirty, a live and an unlanded agent
    worktree, returned as a dict of `agent_id -> wt Path`."""
    repo = repo_root
    graph = _graph(repo)
    # A — the round LANDED (HEAD is now the base tip) and came home.
    wt_a = _cut(repo, "a00-aaaa11", "loop/n-A@2", "season/s2")
    (wt_a / "nodeA.md").write_text("a\n")
    _sh("git", "-C", str(wt_a), "add", "-A")
    _sh("git", "-C", str(wt_a), "commit", "-q", "-m", "round A")
    # The round LANDED: merge the loop branch into its base, so HEAD(A) is an
    # ancestor of `season/s2` (a real merge, not a forced ref move -- the base
    # branch is checked out in the main repo, so `git branch -f` is refused).
    _sh("git", "-C", str(repo), "merge", "--no-ff", "-q", "-m",
        "merge A", "loop/n-A@2")
    _stamp_round(wt_a, "iter-001", "a00-aaaa11", "season/s2")
    _home(repo, "iter-001")
    # B, C, D cut from the now-merged base.
    wt_b = _cut(repo, "a00-bbbb22", "loop/b-B@2", "season/s2")
    (wt_b / "base.txt").write_text("base\nmodified\n")  # tracked change
    _stamp_round(wt_b, "iter-002", "a00-bbbb22", "season/s2")
    _home(repo, "iter-002")
    wt_c = _cut(repo, "a00-cccc33", "loop/c-C@2", "season/s2")
    _stamp_round(wt_c, "iter-003", "a00-cccc33", "season/s2")
    _home(repo, "iter-003")
    _lease(repo, "a00-cccc33")  # live lease -> kept
    wt_d = _cut(repo, "a00-dddd44", "loop/d-D@2", "season/s2")
    (wt_d / "nodeD.md").write_text("d\n")
    _sh("git", "-C", str(wt_d), "add", "-A")
    _sh("git", "-C", str(wt_d), "commit", "-q", "-m", "round D")
    _stamp_round(wt_d, "iter-004", "a00-dddd44", "season/s2")
    _home(repo, "iter-004")
    return {"a00-aaaa11": wt_a, "a00-bbbb22": wt_b,
            "a00-cccc33": wt_c, "a00-dddd44": wt_d}


def test_sweep_removes_merged_clean_homed_and_refuses_others(
        repo_root, four_worktrees, monkeypatch):
    """A finished round's (merged, clean, homed) worktree is removed and its
    loop branch survives; the dirty / live / unlanded ones are refused by
    name, never forced, their bytes untouched."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    removed, refused, kept = heal._sweep_finished_worktrees(_graph(repo_root))
    assert removed == 1
    assert refused == 2   # dirty (B) + unmerged (D); live (C) is kept, not refused
    assert kept == 1      # the live worktree

    # A removed, its loop BRANCH kept.
    assert not four_worktrees["a00-aaaa11"].exists()
    branches = subprocess.run(
        ["git", "-C", str(repo_root), "branch", "--list", "loop/n-A@2"],
        capture_output=True, text=True).stdout
    assert "loop/n-A@2" in branches, "the loop/ branch is the history, keep it"

    # B refused dirty: dir still there, modified node bytes untouched.
    assert four_worktrees["a00-bbbb22"].exists()
    assert "modified" in four_worktrees["a00-bbbb22"].joinpath(
        "base.txt").read_text()

    # C kept live; D kept unmerged.
    assert four_worktrees["a00-cccc33"].exists()
    assert four_worktrees["a00-dddd44"].exists()

    text = log.read_text()
    assert "[sweep] removed a00-aaaa11 iter=iter-001 base=season/s2" in text
    assert "[sweep] refused a00-bbbb22: dirty (1 paths)" in text
    assert "[sweep] kept a00-cccc33: live" in text
    assert "[sweep] refused a00-dddd44: unmerged" in text
    assert "sweep: removed=1 refused=2 kept-live=1" in text


def _raise_budget(*args, **kwargs):
    raise RuntimeError("budget dir unreadable (simulated)")


def test_sweep_unreadable_budget_fails_closed(repo_root, four_worktrees,
                                              monkeypatch):
    """An unreadable spawn-budget must SKIP the whole sweep, never treat every
    agent as dead: the merged+clean+homed worktree `a00-aaaa11` (which a normal
    pass would remove) is STILL PRESENT with its branch still existing."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    # heal bound `spawn_budget` at its own import time; patch THAT module object
    # (the one the sweep calls), not the test's separately-loaded copy, so the
    # sweep really sees the raise.
    monkeypatch.setattr(heal.spawn_budget, "live_agents", _raise_budget)

    removed, refused, kept = heal._sweep_finished_worktrees(_graph(repo_root))
    assert (removed, refused, kept) == (0, 0, 0)

    # Fail-closed: the reapable worktree survives, its branch still exists.
    assert four_worktrees["a00-aaaa11"].exists()
    branches = subprocess.run(
        ["git", "-C", str(repo_root), "branch", "--list", "loop/n-A@2"],
        capture_output=True, text=True).stdout
    assert "loop/n-A@2" in branches

    # The skip is visible in the log.
    assert "[sweep] skipped: budget unreadable (" in log.read_text()


def test_sweep_dry_run_removes_nothing_but_logs(repo_root, four_worktrees,
                                                monkeypatch):
    """`--dry-run` prints the same `[sweep] removed` line and removes none."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    removed, _, _ = heal._sweep_finished_worktrees(_graph(repo_root),
                                                   dry_run=True)
    assert removed == 1
    assert four_worktrees["a00-aaaa11"].exists(), "dry-run removes nothing"
    assert "removed a00-aaaa11 iter=iter-001 base=season/s2 (dry-run)" in \
        log.read_text()


def test_sweep_help_exits_zero(repo_root):
    """`heal.py sweep -h` exits 0 (claimed surface, and a `sweep` subcommand
    is reachable on the same binary as `watch`)."""
    out = subprocess.run([sys.executable, str(BIN / "heal.py"), "sweep", "-h"],
                         capture_output=True, text=True)
    assert out.returncode == 0
    assert "--dry-run" in out.stdout


def test_watch_once_calls_sweep_exactly_once(repo_root, four_worktrees,
                                             monkeypatch):
    """A `heal.py watch --once` pass runs the sweep exactly once: the
    released (merged+clean+homed) worktree is gone after the single pass, the
    refused ones still stand."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(_graph(repo_root)),
                         "--once"])
    assert heal.main() == 0
    assert not four_worktrees["a00-aaaa11"].exists()
    assert four_worktrees["a00-bbbb22"].exists()
    assert four_worktrees["a00-cccc33"].exists()
    assert four_worktrees["a00-dddd44"].exists()
    # one summary line => the sweep ran once.
    assert log.read_text().count("sweep: removed=") == 1