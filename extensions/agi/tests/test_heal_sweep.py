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

# ---------------------------------------------------------------------------
# Bring-home BEFORE the sweep judges condition (4)
# (hypothesis:l4-a-finished-rounds-session-dir-comes-home-before-the-sweep-judges-it)
#
# A leaseless, merged, clean, past-grace round whose session dir is NOT home is
# home'd via cli._session_complete (the sweep's ONE sanctioned caller), and
# only a round whose dir comes home is judged removable. session-complete's OWN
# guards (terminal records, target not non-empty, no live lease) stay the
# authority -- the sweep never bypasses them and never copies a session dir
# itself. The grace check moves AHEAD of the home step so a director's hand
# harvest inside the window is never raced.
# ---------------------------------------------------------------------------

def _snapshot(root: Path, ignore_top_level: tuple = ()) -> dict:
    """relative path -> bytes, for every file under `root`; an absent root
    snapshots to {} and any top-level entry whose name is in `ignore_top_level`
    is skipped (used to drop the transient `.spawn-budget` lock every budget
    reader touches -- it is a lease lock, not a migration target)."""
    out = {}
    if not root.exists():
        return out
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if rel.parts[0] in ignore_top_level:
            continue
        out[str(rel)] = p.read_bytes()
    return out


def _land(repo: Path, wt: Path, branch: str) -> None:
    """Commit a change in the worktree and land its loop branch into the base,
    so HEAD(wt) is an ancestor of `season/s2` (condition 2 passes). Writes the
    branch name as the file body so a second cut from the same base lands a
    DIFFERENT commit (its own nodeX, different bytes)."""
    (wt / "nodeX.md").write_text(f"{branch}: x\n")
    _sh("git", "-C", str(wt), "add", "-A")
    _sh("git", "-C", str(wt), "commit", "-q", "-m", branch)
    _sh("git", "-C", str(repo), "merge", "--no-ff", "-q", "-m",
        f"merge {branch}", branch)


def _stamp_complete_round(wt: Path, iter_name: str, agent_id: str,
                         base: str = "season/s2") -> None:
    """A round whose manifest + agent record are ALL TERMINAL (what
    cli._iteration_agents_complete accepts) -- unlike the `agents: []` shape
    `_stamp_round` writes, which is NOT complete and would refuse to home. Also
    carries the top-level dispatcher `agent.json` with `base_branch` (the same
    tuple season.py merge-up / the sweep's `_sweep_worktree_base` climb)."""
    it = wt / ".agi" / "sessions" / iter_name
    (it / agent_id).mkdir(parents=True, exist_ok=True)
    (it / agent_id / "agent.json").write_text(json.dumps(
        {"id": agent_id, "status": "done", "victory": True}))
    (it / "agent.json").write_text(json.dumps(
        {"id": agent_id, "status": "done", "base_branch": base}))
    (it / "manifest.json").write_text(json.dumps({
        "iter": iter_name, "timeout_seconds": 600,
        "agents": [{"id": agent_id, "status": "done"}]}))
    (it / "output.log").write_text("round output\n")
    (it / "context.md").write_text("# round context\n")


def test_sweep_bring_home_dry_run_then_live(repo_root, monkeypatch):
    """(a) A merged+clean+leaseless+past-grace round whose session dir is NOT
    home: the dry-run logs homed-would + removed(dry-run) and writes NOTHING
    under the main sessions dir; the live pass migrates byte-identical bytes
    home (accounts not session-complete's round-trip checks pass), removes the
    source from the worktree, removes the worktree, and keeps the loop branch."""
    repo = repo_root
    graph = _graph(repo)
    wt = _cut(repo, "a00-eeee55", "loop/e-E@2", "season/s2")
    _land(repo, wt, "loop/e-E@2")
    _stamp_complete_round(wt, "iter-501", "a00-eeee55")
    assert not (graph / "sessions" / "iter-501").is_dir(), \
        "fixture: the iter dir is NOT home"

    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    sess_before = _snapshot(graph / "sessions", ignore_top_level=(".spawn-budget",))

    # DRY-RUN: nothing written, homed-would + removed(dry-run) logged.
    removed, refused, kept = heal._sweep_finished_worktrees(graph,
                                                            dry_run=True)
    assert (removed, refused, kept) == (1, 0, 0)
    assert not (graph / "sessions" / "iter-501").is_dir(), \
        "dry-run writes nothing under the main sessions dir"
    assert _snapshot(graph / "sessions",
                     ignore_top_level=(".spawn-budget",)) == sess_before
    assert "[sweep] homed a00-eeee55 iter=iter-501" in log.read_text()
    assert "[sweep] removed a00-eeee55 iter=iter-501 base=season/s2 "
    "(dry-run)" in log.read_text()
    assert wt.exists(), "dry-run removes nothing"

    # LIVE: home'd bytes identical, source gone, worktree removed, branch kept.
    removed, refused, kept = heal._sweep_finished_worktrees(graph)
    assert (removed, refused, kept) == (1, 0, 0)
    target = graph / "sessions" / "iter-501"
    assert (target / "manifest.json").is_file()
    assert (target / "a00-eeee55" / "agent.json").is_file()
    assert (target / "output.log").read_text() == "round output\n"
    assert not (wt / ".agi" / "sessions" / "iter-501").exists(), \
        "source removed from the worktree after homing"
    assert not wt.exists(), "worktree removed"
    branches = subprocess.run(
        ["git", "-C", str(repo), "branch", "--list", "loop/e-E@2"],
        capture_output=True, text=True).stdout
    assert "loop/e-E@2" in branches, "the loop/ branch is the history, keep it"


def test_sweep_bring_home_refuses_non_terminal(repo_root, monkeypatch):
    """(b) One non-terminal agent record: refused `session dir not home`
    (non-terminal), nothing migrated, the worktree kept -- session-complete's
    completeness guard is the authority, never bypassed."""
    repo = repo_root
    graph = _graph(repo)
    wt = _cut(repo, "a00-ffff66", "loop/f-F@2", "season/s2")
    _land(repo, wt, "loop/f-F@2")
    it = wt / ".agi" / "sessions" / "iter-502"
    (it / "a00-ffff66").mkdir(parents=True, exist_ok=True)
    (it / "a00-ffff66" / "agent.json").write_text(json.dumps(
        {"id": "a00-ffff66", "status": "running"}))  # NOT terminal
    (it / "agent.json").write_text(json.dumps(
        {"id": "a00-ffff66", "status": "running",
         "base_branch": "season/s2"}))
    (it / "manifest.json").write_text(json.dumps({
        "iter": "iter-502",
        "agents": [{"id": "a00-ffff66", "status": "running"}]}))
    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    removed, refused, kept = heal._sweep_finished_worktrees(graph)
    assert (removed, refused, kept) == (0, 1, 0)
    assert not (graph / "sessions" / "iter-502").exists(), "nothing migrated"
    assert wt.exists(), "worktree kept"
    text = log.read_text()
    assert "[sweep] refused a00-ffff66: session dir not home" in text
    assert "non-terminal" in text


def test_sweep_bring_home_never_overwrites_foreign_target(repo_root):
    """(c) A pre-existing NON-EMPTY main target is NEVER overwritten by the
    sweep: session-complete (whose authority stays intact) refuses the
    collision and the foreign bytes are byte-identical after the pass. The
    sweep's OWN removal verdict here follows the baseline (f) contract 'an
    on-disk target is home' -- a source-present round with a target already on
    disk is reachable as home without a home attempt, so the worktree IS
    reaped (the claim's (c) `refused` expectation is a documented deviation,
    see the node thought). The foreign BYTES are preserved either way."""
    repo = repo_root
    graph = _graph(repo)
    wt = _cut(repo, "a00-1111aa", "loop/1-A@2", "season/s2")
    _land(repo, wt, "loop/1-A@2")
    _stamp_complete_round(wt, "iter-503", "a00-1111aa")
    tgt = graph / "sessions" / "iter-503"
    tgt.mkdir(parents=True, exist_ok=True)
    (tgt / "preexisting.txt").write_text("foreign\n")
    removed, refused, _ = heal._sweep_finished_worktrees(graph)
    # THE invariant the falsifier names: a non-empty target is never
    # overwritten (session-complete refused the collision).
    assert (tgt / "preexisting.txt").read_text() == "foreign\n", \
        "the foreign target bytes must survive the pass untouched"
    assert not wt.exists(), (
        "baseline (f) contract: an on-disk target is home, so the round's "
        "worktree is reaped; the claim's (c) refusal is not reachable while "
        "the homed-fixture (f) case must stay removable")


def test_sweep_bring_home_branch_round_calls_once(repo_root, monkeypatch):
    """(d) A `--branch` round holds its iter dir in TWO worktrees:
    session-complete is called ONCE for the iteration (the memo is asserted)
    and BOTH worktrees are removed in the same live pass."""
    repo = repo_root
    graph = _graph(repo)
    w1 = _cut(repo, "a00-2222bb", "loop/2-B@2", "season/s2")
    _land(repo, w1, "loop/2-B@2")
    w2 = _cut(repo, "a00-3333cc", "loop/3-C@2", "season/s2")
    _land(repo, w2, "loop/3-C@2")
    _stamp_complete_round(w1, "iter-504", "a00-2222bb")
    it2 = w2 / ".agi" / "sessions" / "iter-504"
    (it2 / "a00-3333cc").mkdir(parents=True, exist_ok=True)
    (it2 / "a00-3333cc" / "agent.json").write_text(json.dumps(
        {"id": "a00-3333cc", "status": "done"}))
    (it2 / "agent.json").write_text(json.dumps(
        {"id": "a00-3333cc", "status": "done",
         "base_branch": "season/s2"}))
    (it2 / "manifest.json").write_text(json.dumps({
        "iter": "iter-504",
        "agents": [{"id": "a00-3333cc", "status": "done"}]}))
    (it2 / "output.log").write_text("second tree's output\n")

    # Count session-complete invocations on the SAME module the helper calls.
    import cli as _cli
    real = _cli._session_complete
    calls = []

    def counting(*a, **k):
        calls.append(k.get("dry_run", False))
        return real(*a, **k)
    monkeypatch.setattr(_cli, "_session_complete", counting)

    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    removed, refused, kept = heal._sweep_finished_worktrees(graph)
    assert (removed, refused, kept) == (2, 0, 0)
    assert calls == [False], "ONE session-complete call for the shared iter"
    target = graph / "sessions" / "iter-504"
    assert (target / "a00-2222bb" / "agent.json").is_file()
    assert (target / "a00-3333cc" / "agent.json").is_file()
    assert not w1.exists() and not w2.exists(), "both worktrees removed"


def test_sweep_bring_home_branch_round_dry_run_counts_both(repo_root,
                                                            monkeypatch):
    """(harvest L4.255) The DRY-RUN twin of (d): with nothing written to disk
    the memoized would-home ("") must carry to the second tree of the round --
    both trees log `removed (dry-run)`, session-complete is called once, and
    no tree is refused with an empty `session dir not home ()` reason."""
    repo = repo_root
    graph = _graph(repo)
    w1 = _cut(repo, "a00-2222bb", "loop/2-B@2", "season/s2")
    _land(repo, w1, "loop/2-B@2")
    w2 = _cut(repo, "a00-3333cc", "loop/3-C@2", "season/s2")
    _land(repo, w2, "loop/3-C@2")
    _stamp_complete_round(w1, "iter-504", "a00-2222bb")
    it2 = w2 / ".agi" / "sessions" / "iter-504"
    (it2 / "a00-3333cc").mkdir(parents=True, exist_ok=True)
    (it2 / "a00-3333cc" / "agent.json").write_text(json.dumps(
        {"id": "a00-3333cc", "status": "done"}))
    (it2 / "agent.json").write_text(json.dumps(
        {"id": "a00-3333cc", "status": "done",
         "base_branch": "season/s2"}))
    (it2 / "manifest.json").write_text(json.dumps({
        "iter": "iter-504",
        "agents": [{"id": "a00-3333cc", "status": "done"}]}))

    import cli as _cli
    real = _cli._session_complete
    calls = []

    def counting(*a, **k):
        calls.append(k.get("dry_run", False))
        return real(*a, **k)
    monkeypatch.setattr(_cli, "_session_complete", counting)

    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    removed, refused, kept = heal._sweep_finished_worktrees(graph, dry_run=True)
    text = log.read_text()
    assert (removed, refused, kept) == (2, 0, 0), text
    assert calls == [True], "ONE dry-run session-complete call for the iter"
    assert "session dir not home" not in text
    assert not (graph / "sessions" / "iter-504").exists(), "dry-run wrote nothing"
    assert w1.exists() and w2.exists(), "dry-run removed nothing"


def test_sweep_bring_home_grace_keeps_not_homed(tmp_path):
    """(e) A complete-but-not-home round YOUNGER than the (large) grace is kept
    as `grace` and NOT homed: a director's hand harvest inside the window is
    never raced by the reaper."""
    repo = tmp_path / "repo"
    graph = repo / ".agi"
    (graph / "nodes").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps(
        {"reaper": {"worktree_grace_min": 100000}}))
    _sh("git", "init", "-b", "season/s2", str(repo))
    _sh("git", "-C", str(repo), "config", "user.email", "t@example.com")
    _sh("git", "-C", str(repo), "config", "user.name", "t")
    (repo / ".gitignore").write_text(".agi/sessions/\n.agi/worktrees/\n")
    (repo / "base.txt").write_text("base\n")
    _sh("git", "-C", str(repo), "add", "-A")
    _sh("git", "-C", str(repo), "commit", "-q", "-m", "init")
    wt = graph / "worktrees" / "a00-9999zz"
    _sh("git", "-C", str(repo), "worktree", "add", "-b", "loop/z-Z@2",
        str(wt), "season/s2")
    (wt / "node.md").write_text("n\n")
    _sh("git", "-C", str(wt), "add", "-A")
    _sh("git", "-C", str(wt), "commit", "-q", "-m", "round")
    _sh("git", "-C", str(repo), "merge", "--no-ff", "-q", "-m", "merge z",
        "loop/z-Z@2")
    _stamp_complete_round(wt, "iter-505", "a00-9999zz")
    removed, refused, kept = heal._sweep_finished_worktrees(graph)
    assert (removed, refused, kept) == (0, 0, 1)
    assert not (graph / "sessions" / "iter-505").exists(), "NOT homed"
    assert wt.exists(), "worktree kept"


def test_sweep_refusal_reason_names_every_live_refusal():
    """(harvest L4.298) `_sweep_refusal_reason` carries a needle for every
    LIVE refusal text session-complete can print, and the tag is the named
    reason the `[sweep] session dir not home (<reason>)` line shows. The
    matrix below pairs each real print (measured by grep, file:line in the
    experiment node) with the needle that must map it -- order first-wins."""
    h = heal._sweep_refusal_reason
    assert h("agent a00-x status=running is not terminal; round still running") \
        == "non-terminal"
    # a status-LESS manifest entry defaults to `running`, so session-complete
    # prints exactly the line above -- the correct refusal is the
    # is-not-terminal tag, NOT the no-manifest tag.
    assert h("agent a00-x status=running is not terminal") == "non-terminal"
    assert h("no manifest.json in any source for iteration L4.9; nothing to "
             "judge, nothing moves") == "no manifest"
    assert h("target already exists and is not empty; refusing to overwrite") \
        == "target exists"
    assert h("a live lease is active for iteration L4.9; round still running") \
        == "live lease"
    assert h("this source's own contribution did not verify; left intact at "
             "its worktree") == "verify failed"


def test_sweep_refusal_reason_dead_needle_removed():
    """(harvest L4.298) The old `not every agent record is terminal` needle
    matches NOTHING any live code prints (grep), so it is removed: the text
    now falls through to the generic `home failed` bucket instead of a named
    tag for a message that can no longer appear."""
    h = heal._sweep_refusal_reason
    assert h("not every agent record is terminal; round still running") \
        == "home failed", \
        "the dead needle must not get a named tag; only live refusals do"
