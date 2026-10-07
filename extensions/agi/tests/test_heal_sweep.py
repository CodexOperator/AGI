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
import shutil
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
_REAL_PRESSURE_OK = heal._sweep_pressure_ok   # the autouse stub below hides it from every other row


@pytest.fixture(autouse=True)
def _no_box_pressure(monkeypatch):
    """goal:g7.16.1.5.3: the sweep defers under real box memory/io PSI; a
    test judges the sweep, never the box it happens to run on."""
    monkeypatch.setattr(heal, "_sweep_pressure_ok", lambda root: (True, "test"))
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


def _home(repo: Path, wt: Path, iter_name: str) -> None:
    """Bring the round's session dir `home` to the main checkout as
    session-complete leaves it: every source file under the worktree's iter
    dir present in the main target with EQUAL BYTES. A REAL byte copy
    (copytree), never a bare empty mkdir -- the sweep's condition (4) is
    per-source and byte-exact (_sweep_iter_home), so an empty placeholder no
    longer counts as home (hyp:l4-a-finished-rounds-worktree-is-removed-after-
    harvest, L4.257)."""
    src = wt / ".agi" / "sessions" / iter_name
    target = _graph(repo) / "sessions" / iter_name
    shutil.copytree(src, target)


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
    _home(repo, wt_a, "iter-001")
    # B, C, D cut from the now-merged base.
    wt_b = _cut(repo, "a00-bbbb22", "loop/b-B@2", "season/s2")
    (wt_b / "base.txt").write_text("base\nmodified\n")  # tracked change
    _stamp_round(wt_b, "iter-002", "a00-bbbb22", "season/s2")
    _home(repo, wt_b, "iter-002")
    wt_c = _cut(repo, "a00-cccc33", "loop/c-C@2", "season/s2")
    _stamp_round(wt_c, "iter-003", "a00-cccc33", "season/s2")
    _home(repo, wt_c, "iter-003")
    _lease(repo, "a00-cccc33")  # live lease -> kept
    wt_d = _cut(repo, "a00-dddd44", "loop/d-D@2", "season/s2")
    (wt_d / "nodeD.md").write_text("d\n")
    _sh("git", "-C", str(wt_d), "add", "-A")
    _sh("git", "-C", str(wt_d), "commit", "-q", "-m", "round D")
    _stamp_round(wt_d, "iter-004", "a00-dddd44", "season/s2")
    _home(repo, wt_d, "iter-004")
    return {"a00-aaaa11": wt_a, "a00-bbbb22": wt_b,
            "a00-cccc33": wt_c, "a00-dddd44": wt_d}


def _ref(repo, ref):
    r = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "-q", ref],
                       capture_output=True, text=True)
    return r.stdout.strip()


def test_sweep_archives_then_removes_unmerged_and_dirty(
        repo_root, four_worktrees, monkeypatch):
    """goal:g7.16.1.5.3 -- "unmerged" / "dirty" are no longer terminal: the
    merged+clean tree (A) is removed as before; the dirty one (B) and the
    unlanded one (D) are ARCHIVED first (refs/archive/worktrees/<name>, B's
    uncommitted bytes on <name>-dirty) and then removed; the live one (C) is
    kept. Every loop branch survives; no byte is lost."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    d_head = _ref(four_worktrees["a00-dddd44"], "HEAD")
    removed, refused, kept = heal._sweep_finished_worktrees(_graph(repo_root))
    assert (removed, refused, kept) == (3, 0, 1)

    assert not four_worktrees["a00-aaaa11"].exists()
    assert not four_worktrees["a00-bbbb22"].exists()
    assert not four_worktrees["a00-dddd44"].exists()
    assert four_worktrees["a00-cccc33"].exists(), "a live round is never touched"
    branches = subprocess.run(
        ["git", "-C", str(repo_root), "branch", "--list", "loop/n-A@2"],
        capture_output=True, text=True).stdout
    assert "loop/n-A@2" in branches, "the loop/ branch is the history, keep it"

    # A merged+clean needs no archive; D pinned at its HEAD; B's dirty bytes kept.
    assert _ref(repo_root, "refs/archive/worktrees/a00-aaaa11") == ""
    assert _ref(repo_root, "refs/archive/worktrees/a00-dddd44") == d_head
    b_dirty = _ref(repo_root, "refs/archive/worktrees/a00-bbbb22-dirty")
    assert b_dirty
    assert "modified" in subprocess.run(
        ["git", "-C", str(repo_root), "show", f"{b_dirty}:base.txt"],
        capture_output=True, text=True).stdout

    text = log.read_text()
    assert "[sweep] removed a00-aaaa11 iter=iter-001 base=season/s2" in text
    assert "[sweep] archived a00-bbbb22 (dirty 1) ref=refs/archive/worktrees/a00-bbbb22 +dirty" in text
    assert "[sweep] archived a00-dddd44 (unmerged) ref=refs/archive/worktrees/a00-dddd44" in text
    assert "[sweep] kept a00-cccc33: live" in text
    assert "refused a00-dddd44: unmerged" not in text
    assert "sweep: removed=3 archived=2 refused=0 kept-live=1" in text


def _fake_cgroup(tmp_path: Path, monkeypatch, file_mib: int, slab_mib: int) -> Path:
    """goal:g7.16.1.5.3.1 -- a fake /proc/self/cgroup + cgroup v2 dir; the
    test process's REAL cgroup is never written."""
    proc = tmp_path / "proc-cgroup"
    proc.write_text("0::/user.slice/fake.service\n")
    cg = tmp_path / "cgfs" / "user.slice" / "fake.service"
    cg.mkdir(parents=True)
    (cg / "memory.stat").write_text(
        f"anon 999999999\nfile {(file_mib + 700) << 20}\nshmem {700 << 20}\n"
        f"slab_reclaimable {slab_mib << 20}\n")
    monkeypatch.setattr(heal, "SWEEP_PROC_CGROUP", proc)
    monkeypatch.setattr(heal, "SWEEP_CGROUP_FS", tmp_path / "cgfs")
    return cg


def test_sweep_reclaim_asks_own_cgroup_for_file_plus_slab_capped(tmp_path, monkeypatch):
    """goal:g7.16.1.5.3.1 -- the ask is file - shmem + slab_reclaimable of OUR
    cgroup (never anon, never tmpfs: 700 MiB of shmem is in every fixture),
    capped by the cell, swappiness=0; under 16 MiB nothing is written; no
    cgroup v2 line = nothing asked."""
    cg = _fake_cgroup(tmp_path, monkeypatch, file_mib=300, slab_mib=100)
    assert heal._sweep_reclaim(256) == 256
    assert (cg / "memory.reclaim").read_text() == "256M swappiness=0"
    assert heal._sweep_reclaim(4096) == 400
    assert (cg / "memory.reclaim").read_text() == "400M swappiness=0"
    assert heal._sweep_reclaim(0) == 0
    (cg / "memory.reclaim").unlink()
    (cg / "memory.stat").write_text(f"anon 999999999\nfile {701 << 20}\nshmem {700 << 20}\nslab_reclaimable 0\n")
    assert heal._sweep_reclaim(256) == 0
    assert not (cg / "memory.reclaim").exists(), "under 16 MiB: nothing written"
    (tmp_path / "proc-cgroup").write_text("12:memory:/legacy\n")
    assert heal._sweep_reclaim(256) == 0


def test_sweep_reclaim_refusal_logs_one_line_and_never_raises(tmp_path, monkeypatch):
    cg = _fake_cgroup(tmp_path, monkeypatch, file_mib=300, slab_mib=0)
    (cg / "memory.reclaim").mkdir()  # a write that fails with an OSError
    log = tmp_path / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    assert heal._sweep_reclaim(256) == 0
    assert log.read_text().count("[sweep] reclaim refused") == 1


def test_sweep_reclaims_on_cadence_and_decides_the_same(
        repo_root, four_worktrees, tmp_path, monkeypatch):
    """goal:g7.16.1.5.3.1 -- with the cells on, the walk asks every
    `sweep_reclaim_every` trees and once at pass end, and every removal /
    archive / keep decision is exactly the cells-off one."""
    graph = _graph(repo_root)
    cfg = json.loads((graph / "config.json").read_text())
    cfg["reaper"].update(sweep_reclaim_max_mib=64, sweep_reclaim_every=2)
    (graph / "config.json").write_text(json.dumps(cfg))
    cg = _fake_cgroup(tmp_path, monkeypatch, file_mib=300, slab_mib=0)
    asks = []
    real = heal._sweep_reclaim
    monkeypatch.setattr(heal, "_sweep_reclaim", lambda m: asks.append(m) or real(m))
    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    assert heal._sweep_finished_worktrees(graph) == (3, 0, 1)
    # 4 trees x 2 walks = 8 steps -> 4 cadence asks + 1 after each of the
    # 2 archives (B dirty, D unmerged) + 1 at pass end
    assert asks == [64] * 7
    assert (cg / "memory.reclaim").read_text() == "64M swappiness=0"
    text = log.read_text()
    assert "[sweep] reclaimed own cgroup: 7 ask(s), 448 MiB asked over 8 tree steps" in text
    assert "sweep: removed=3 archived=2 refused=0 kept-live=1" in text


def test_sweep_reclaim_writes_only_its_own_cgroup():
    """goal:g7.16.1.5.3.1 Falsifier 2: ONE memory.reclaim write in heal, and
    its cgroup comes from /proc/self/cgroup only."""
    src = (BIN / "heal.py").read_text()
    assert src.count('"memory.reclaim"') == 1
    assert 'SWEEP_PROC_CGROUP = Path("/proc/self/cgroup")' in src


def test_sweep_deferred_under_pressure_removes_nothing(
        repo_root, four_worktrees, monkeypatch):
    """goal:g7.16.1.5.3 -- a pass under memory/io PSI (or a blind read) is
    deferred WHOLE: nothing archived, nothing removed, one line says why."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    monkeypatch.setattr(heal, "_sweep_pressure_ok",
                        lambda root: (False, "io psi some.avg10 55 >= 40"))
    assert heal._sweep_finished_worktrees(_graph(repo_root)) == (0, 0, 0)
    assert all(w.exists() for w in four_worktrees.values())
    assert "[sweep] deferred: io psi some.avg10 55 >= 40" in log.read_text()


def _pressure_root(tmp_path, cells=None):
    graph = tmp_path / ".agi"
    graph.mkdir()
    (graph / "config.json").write_text(json.dumps({"reaper": cells or {}}))
    return graph


def _pressure_box(monkeypatch, mem, io):
    """memory_alarm.read_psi (the ONE reader) answers per path; a number is the
    `some.avg10`, a dict is returned as is ({} = an unreadable file)."""
    import memory_alarm
    table = {str(memory_alarm.BOX_PSI): mem, "/proc/pressure/io": io}
    monkeypatch.setattr(memory_alarm, "read_psi", lambda path: (
        {"some": {"avg10": table[str(path)]}}
        if isinstance(table[str(path)], (int, float)) else table[str(path)]))


@pytest.mark.parametrize("mem,io,cells,ok,why", [
    (3.0, 2.0, None, True, "pressure under both lines"),
    (39.99, 39.99, None, True, "pressure under both lines"),
    (40.0, 1.0, None, False, "memory psi some.avg10 40 >= 40"),
    (1.0, 40.0, None, False, "io psi some.avg10 40 >= 40"),
    (55.0, 1.0, None, False, "memory psi some.avg10 55 >= 40"),
    (60.0, 70.0, None, False, "memory psi some.avg10 60 >= 40"),
    (15.0, 1.0, {"sweep_mem_psi_max_pct": 10}, False, "memory psi some.avg10 15 >= 10"),
    (1.0, 55.0, {"sweep_io_psi_max_pct": 90}, True, "pressure under both lines"),
    (1.0, 55.0, {"sweep_io_psi_max_pct": "50"}, False, "io psi some.avg10 55 >= 50"),
    (45.0, 1.0, {"sweep_mem_psi_max_pct": 0}, False, "memory psi some.avg10 45 >= 40"),
    (45.0, 1.0, {"sweep_mem_psi_max_pct": 101}, False, "memory psi some.avg10 45 >= 40"),
    (45.0, 1.0, {"sweep_mem_psi_max_pct": "x"}, False, "memory psi some.avg10 45 >= 40"),
    ({}, 1.0, None, False, "memory psi unreadable (no some.avg10): fails closed"),
    ({"some": {}}, 1.0, None, False, "memory psi unreadable (no some.avg10): fails closed"),
    (1.0, {}, None, False, "io psi unreadable (no some.avg10): fails closed"),
    (1.0, {"full": {"avg10": 1.0}}, None, False, "io psi unreadable (no some.avg10): fails closed"),
])
def test_the_real_pressure_gate_reads_both_psi_lines_and_fails_closed(
        tmp_path, monkeypatch, mem, io, cells, ok, why):
    """goal:g7.16.1.5.3 (g1.41 PASS B4 residue: every other row here stubs the
    gate away) -- the REAL `_sweep_pressure_ok`: a line is the cell when it is a
    number in (0, 100], else 40; AT the line refuses; memory is read before io;
    a blind read of either file fails closed by name."""
    _pressure_box(monkeypatch, mem, io)
    assert _REAL_PRESSURE_OK(_pressure_root(tmp_path, cells)) == (ok, why)


def test_sweep_failed_archive_never_removes(repo_root, four_worktrees,
                                            monkeypatch):
    """goal:g7.16.1.5.3 invariant: a tree that needs an archive is never
    removed unless the archive verified -- a failed archive refuses by name."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    monkeypatch.setattr(heal, "_sweep_archive", lambda *a, **k: "update-ref failed")
    removed, refused, kept = heal._sweep_finished_worktrees(_graph(repo_root))
    assert (removed, refused, kept) == (1, 2, 1)   # only merged+clean A goes
    assert four_worktrees["a00-bbbb22"].exists()
    assert four_worktrees["a00-dddd44"].exists()
    assert "[sweep] refused a00-dddd44: archive failed (update-ref failed)" in log.read_text()


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
    assert removed == 3
    assert all(w.exists() for w in four_worktrees.values()), "dry-run removes nothing"
    assert _ref(repo_root, "refs/archive/worktrees/a00-dddd44") == "", "dry-run writes no ref"
    assert "archived a00-dddd44 (unmerged) ref=refs/archive/worktrees/a00-dddd44 (dry-run)" in \
        log.read_text()
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
                                             monkeypatch, tmp_path):
    """A `heal.py watch --once` pass runs the sweep exactly once: the
    released (merged+clean+homed) worktree is gone after the single pass, the
    refused ones still stand. Defence-in-depth: the seat scan reads a real
    window file (AGI_WINDOW_PATH) and never a tmux subprocess, so this test
    cannot reach the live session even if the conftest guard is lost."""
    log = _graph(repo_root) / "reaper.log"
    # Name an empty window file so `_all_windows` reads it, never `tmux
    # list-windows -a` / `tmux new-window` (see heal.WINDOW_PATH_ENV seam).
    _wins = tmp_path / "windows"
    _wins.write_text("@1 nobody\n")
    monkeypatch.setenv("AGI_WINDOW_PATH", str(_wins))
    assert heal._all_windows() == [("@1", "nobody")]
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    monkeypatch.setattr(sys, "argv",
                        ["heal.py", "watch", "--root", str(_graph(repo_root)),
                         "--once"])
    assert heal.main() == 0
    assert not four_worktrees["a00-aaaa11"].exists()
    assert not four_worktrees["a00-bbbb22"].exists()   # archived, then removed
    assert four_worktrees["a00-cccc33"].exists()
    assert not four_worktrees["a00-dddd44"].exists()   # archived, then removed
    assert _ref(repo_root, "refs/archive/worktrees/a00-dddd44")
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


def _archived(repo: Path, ref: str, prefix: str) -> dict:
    """relative path (under `prefix`) -> bytes, for every file the archive
    ref's tree holds below `prefix` (the same shape as `_snapshot`)."""
    names = subprocess.run(
        ["git", "-C", str(repo), "ls-tree", "-r", "--name-only", ref, "--", prefix],
        capture_output=True, text=True, check=True).stdout.split()
    return {n[len(prefix) + 1:]: subprocess.run(
        ["git", "-C", str(repo), "show", f"{ref}:{n}"],
        capture_output=True, check=True).stdout for n in names}


def test_sweep_bring_home_never_overwrites_foreign_target(repo_root,
                                                           monkeypatch):
    """(c, RE-PINNED goal:g7.16.1.5.3) A pre-existing NON-EMPTY main target is
    never overwritten by the sweep: the bring-home IS attempted, session-
    complete (whose authority stays intact) refuses the collision ("target
    exists"). That refusal is TERMINAL -- the round is over -- so it no longer
    holds the tree forever (4287 of 4291 not-home refusals, 09-30): the tree's
    OWN records ride into refs/archive/worktrees/<name>-dirty (byte-verified
    here), THEN the tree is removed. No byte is lost on either side."""
    repo = repo_root
    graph = _graph(repo)
    wt = _cut(repo, "a00-1111aa", "loop/1-A@2", "season/s2")
    _land(repo, wt, "loop/1-A@2")
    _stamp_complete_round(wt, "iter-503", "a00-1111aa")
    tgt = graph / "sessions" / "iter-503"
    tgt.mkdir(parents=True, exist_ok=True)
    (tgt / "preexisting.txt").write_text("foreign\n")
    src_before = _snapshot(wt / ".agi" / "sessions" / "iter-503")
    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    removed, refused, _ = heal._sweep_finished_worktrees(graph)
    # THE invariant the falsifier names: a non-empty target is never
    # overwritten (session-complete refused the collision).
    assert (tgt / "preexisting.txt").read_text() == "foreign\n", \
        "the foreign target bytes must survive the pass untouched"
    assert (removed, refused) == (1, 0)
    assert not wt.exists(), "archived, then removed"
    assert _archived(repo, "refs/archive/worktrees/a00-1111aa-dirty",
                     ".agi/sessions/iter-503") == src_before, \
        "the tree's own unmigrated records are byte-equal in the archive"
    text = log.read_text()
    assert "[sweep] archived a00-1111aa (sessions 1) ref=refs/archive/worktrees/a00-1111aa +dirty" in text
    assert "session dir not home" not in text


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


# ---------------------------------------------------------------------------
# L4.257 — the empty/foreign-clicktive-placeholder DATA-LOSS defect
# (hypothesis:l4-a-finished-rounds-worktree-is-removed-after-harvest)
#
# Condition (4) used to prove 'the session dir came home' with a bare is_dir()
# on the main target. An EMPTY pre-created placeholder (dispatch pre-creates
# one) or a FOREIGN non-empty dir (the OTHER tree's half of a --branch round,
# or a hand-made dir) both satisfied it, so the bring-home was never attempted
# and `git worktree remove` reaped the tree WITH ITS OWN UNMIGRATED RECORDS.
# `home` is now per-source and byte-exact (_sweep_iter_home), so an absent or
# empty target, or any missing/unequal file, is NOT home and the bring-home
# runs (session-complete's own guards stay the authority).
# ---------------------------------------------------------------------------

def _stamp_plain_round(wt: Path, iter_name: str, agent_id: str) -> None:
    """A round whose manifest has `agents: []` -- session-complete's 'no
    agents in manifest' REFUSE (un-homeable). Carries the top-level
    dispatcher agent.json with `base_branch` (the tuple _sweep_worktree_base
    climbs)."""
    it = wt / ".agi" / "sessions" / iter_name
    it.mkdir(parents=True, exist_ok=True)
    (it / "agent.json").write_text(json.dumps(
        {"id": agent_id, "status": "done", "base_branch": "season/s2"}))
    (it / "manifest.json").write_text(json.dumps(
        {"iter": iter_name, "agents": []}))
    (it / "output.log").write_text("precious records\n")


def test_sweep_empty_target_is_not_home(repo_root, monkeypatch):
    """(a, FALSIFIER) A merged+clean+past-grace round with an EMPTY main target dir
    (a pre-created placeholder), whose source is UN-HOMEABLE: NOT home. The
    bring-home is attempted, session-complete refuses (non-terminal /
    'no agents in manifest'), the worktree is REFUSED and its records are
    byte-intact; the empty target is left alone. THE regressed failure: the
    old bare-is_dir() proof would have reaped this tree with its own
    unmigrated records."""
    repo = repo_root
    graph = _graph(repo)
    wt = _cut(repo, "a00-eeee55", "loop/e-E@2", "season/s2")
    _land(repo, wt, "loop/e-E@2")
    _stamp_plain_round(wt, "iter-601", "a00-eeee55")
    # main target = an EMPTY pre-created placeholder.
    tgt = graph / "sessions" / "iter-601"
    tgt.mkdir(parents=True, exist_ok=True)
    assert not any(tgt.iterdir()), "fixture: the placeholder is EMPTY"

    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    src_before = _snapshot(wt / ".agi" / "sessions" / "iter-601")

    removed, refused, kept = heal._sweep_finished_worktrees(graph)
    assert (removed, refused, kept) == (0, 1, 0)
    assert wt.exists(), "the source-holding tree is NOT reaped on an empty hit"
    assert _snapshot(wt / ".agi" / "sessions" / "iter-601") == src_before, \
        "the worktree's own records are byte-intact"
    assert any(tgt.iterdir()) is False, "the empty placeholder is left alone"
    text = log.read_text()
    assert "[sweep] refused a00-eeee55: session dir not home" in text
    assert "non-terminal" in text


def test_sweep_empty_target_homes_content_before_removal(repo_root, monkeypatch):
    """(b) A merged+clean+past-grace round with an EMPTY main target dir but a
    HOMEABLE source: the dry-run logs homed-would + removed(dry-run), writes
    NOTHING (target stays empty, worktree stays); the live pass brings the
    content home byte-equal, removes the source, then removes the worktree,
    keeping the loop branch."""
    repo = repo_root
    graph = _graph(repo)
    wt = _cut(repo, "a00-ffff66", "loop/f-F@2", "season/s2")
    _land(repo, wt, "loop/f-F@2")
    _stamp_complete_round(wt, "iter-602", "a00-ffff66")
    tgt = graph / "sessions" / "iter-602"
    tgt.mkdir(parents=True, exist_ok=True)  # EMPTY placeholder
    assert not any(tgt.iterdir()), "fixture: the placeholder is EMPTY"

    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))

    # DRY-RUN: nothing written, would-home + removed(dry-run) logged.
    removed, refused, kept = heal._sweep_finished_worktrees(graph, dry_run=True)
    assert (removed, refused, kept) == (1, 0, 0)
    assert not any(tgt.iterdir()), "dry-run writes nothing under the target"
    assert wt.exists(), "dry-run removes nothing"
    assert "[sweep] homed a00-ffff66 iter=iter-602" in log.read_text()

    # LIVE: content comes home byte-equal, source gone, worktree removed.
    removed, refused, kept = heal._sweep_finished_worktrees(graph)
    assert (removed, refused, kept) == (1, 0, 0)
    assert (tgt / "manifest.json").is_file()
    assert (tgt / "a00-ffff66" / "agent.json").is_file()
    assert (tgt / "output.log").read_text() == "round output\n"
    assert not (wt / ".agi" / "sessions" / "iter-602").exists(), \
        "source removed from the worktree after homing"
    assert not wt.exists(), "worktree removed"
    text = log.read_text()
    assert "[sweep] homed a00-ffff66 iter=iter-602" in text
    assert "[sweep] removed a00-ffff66 iter=iter-602 base=season/s2" in text
    branches = subprocess.run(
        ["git", "-C", str(repo), "branch", "--list", "loop/f-F@2"],
        capture_output=True, text=True).stdout
    assert "loop/f-F@2" in branches, "the loop/ branch is the history, keep it"


def _cold_cell(repo: Path, tmp_path: Path, monkeypatch) -> Path:
    """goal:g7.16.1.5.2.1 -- config:guard names a cold sessions home for a
    fixture box (the goal:g7.16.1.5.2 cell), under tmp."""
    cold = tmp_path / "cold-sessions"
    geo = _graph(repo) / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "guard.md").write_text(
        "# guard\n```sh guard.env\n"
        f"GUARD_AGI_SESSIONS_ARCHIVE_fixturebox={cold}\n```\n")
    monkeypatch.setenv("GUARD_BOX", "fixturebox")
    return cold


def test_sweep_homes_onto_the_cold_home_never_the_ram_disk(repo_root, tmp_path,
                                                           monkeypatch):
    """goal:g7.16.1.5.2.1 -- with the cold-home cell set and no MAIN entry,
    the homed bytes land in <cold>/<iter> and MAIN keeps ONLY a symlink (no
    real dir is ever created under MAIN's sessions); byte-equal, the source
    and the tree removed."""
    repo = repo_root
    graph = _graph(repo)
    cold = _cold_cell(repo, tmp_path, monkeypatch)
    wt = _cut(repo, "a00-c01d77", "loop/c-C@2", "season/s2")
    _land(repo, wt, "loop/c-C@2")
    _stamp_complete_round(wt, "iter-801", "a00-c01d77")
    src = _snapshot(wt / ".agi" / "sessions" / "iter-801")
    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    assert heal._sweep_finished_worktrees(graph) == (1, 0, 0)
    link = graph / "sessions" / "iter-801"
    assert link.is_symlink() and link.resolve() == (cold / "iter-801").resolve()
    assert _snapshot(cold / "iter-801") == src, "the homed bytes are on the cold home"
    assert not wt.exists()
    assert "[sweep] homed a00-c01d77 iter=iter-801" in log.read_text()


def test_sweep_cold_link_rolls_back_a_refused_homing(repo_root, tmp_path, monkeypatch):
    """goal:g7.16.1.5.2.1 -- a homing session-complete refuses (a non-terminal
    round) leaves no empty cold dir and no dangling link; the tree stands."""
    repo = repo_root
    graph = _graph(repo)
    cold = _cold_cell(repo, tmp_path, monkeypatch)
    wt = _cut(repo, "a00-c02d88", "loop/d-D@2", "season/s2")
    _land(repo, wt, "loop/d-D@2")
    _stamp_plain_round(wt, "iter-802", "a00-c02d88")
    monkeypatch.setenv("AGI_REAPER_LOG", str(graph / "reaper.log"))
    made = []
    real_link = heal._sweep_cold_link
    monkeypatch.setattr(heal, "_sweep_cold_link",
                        lambda *a: made.append(real_link(*a)) or made[-1])
    removed, refused, _ = heal._sweep_finished_worktrees(graph)
    assert any(made), "the cold link WAS made (the rollback is exercised)"
    assert (removed, refused) == (0, 1)
    assert not (graph / "sessions" / "iter-802").is_symlink()
    assert not (graph / "sessions" / "iter-802").exists()
    assert not (cold / "iter-802").exists()
    assert wt.exists()


def test_sweep_copy_failure_through_the_cold_link_leaves_no_partial(repo_root, tmp_path,
                                                                    monkeypatch):
    """SM residue 156: session-complete's copy FAILS mid-way through heal's
    cold link. The partial copy is discarded THROUGH the link (rmtree alone
    refuses a symlink and kept it), so the rollback finds the cold dir empty
    and removes it and the link; the tree's own records ride its archive."""
    import shutil as _shutil
    repo = repo_root
    graph = _graph(repo)
    cold = _cold_cell(repo, tmp_path, monkeypatch)
    wt = _cut(repo, "a00-c03d99", "loop/e-E@3", "season/s2")
    _land(repo, wt, "loop/e-E@3")
    _stamp_complete_round(wt, "iter-803", "a00-c03d99")
    src = _snapshot(wt / ".agi" / "sessions" / "iter-803")
    calls = []
    real_copy = _shutil.copy2

    def copy_then_fail(a, b, *k, **kw):
        calls.append(b)
        if len(calls) > 1:
            raise OSError(28, "No space left on device (fixture)")
        return real_copy(a, b, *k, **kw)
    monkeypatch.setattr(_shutil, "copy2", copy_then_fail)
    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    removed, refused, _ = heal._sweep_finished_worktrees(graph)
    assert len(calls) >= 2, "the copy really failed mid-way through the link"
    assert not (graph / "sessions" / "iter-803").is_symlink(), "no link left"
    assert not (cold / "iter-803").exists(), "no partial copy left on the cold home"
    assert (removed, refused) == (1, 0), "home failed -> archived, then removed"
    assert _archived(repo, "refs/archive/worktrees/a00-c03d99-dirty",
                     ".agi/sessions/iter-803") == src, "no byte lost"


def test_sweep_cold_link_keeps_a_dir_holding_bytes(tmp_path):
    """The rollback removes ONLY an empty cold dir: one byte may be a
    source's verified contribution, so the dir and its link stay."""
    dest = tmp_path / "cold" / "iter-9"
    dest.mkdir(parents=True)
    (dest / "x").write_text("landed\n")
    link = tmp_path / "main" / "iter-9"
    link.parent.mkdir()
    link.symlink_to(dest)
    heal._sweep_cold_unlink((link, dest))
    assert link.is_symlink() and (dest / "x").read_text() == "landed\n"
    (dest / "x").unlink()
    heal._sweep_cold_unlink((link, dest))
    assert not link.is_symlink() and not dest.exists()


def test_sweep_byte_equal_copy_is_home(repo_root, monkeypatch):
    """(d) A target holding a BYTE-EQUAL copy of the source (hand-copied,
    no session-complete) IS home: the worktree is removed. A target that
    differs by one byte is NOT home: the bring-home is attempted and refused
    (non-empty target), so its records are archived before the tree goes
    (goal:g7.16.1.5.3)."""
    repo = repo_root
    graph = _graph(repo)
    # -- home twin: byte-equal copy --
    wt_a = _cut(repo, "a00-3333cc", "loop/3-C@2", "season/s2")
    _land(repo, wt_a, "loop/3-C@2")
    _stamp_complete_round(wt_a, "iter-701", "a00-3333cc")
    shutil.copytree(wt_a / ".agi" / "sessions" / "iter-701",
                    graph / "sessions" / "iter-701")
    # -- foreign twin: one byte differs --
    wt_b = _cut(repo, "a00-4444dd", "loop/4-D@2", "season/s2")
    _land(repo, wt_b, "loop/4-D@2")
    _stamp_complete_round(wt_b, "iter-702", "a00-4444dd")
    tgt_b = graph / "sessions" / "iter-702"
    shutil.copytree(wt_b / ".agi" / "sessions" / "iter-702", tgt_b)
    (tgt_b / "output.log").write_text("foreign byte differs\n")

    src_b = _snapshot(wt_b / ".agi" / "sessions" / "iter-702")
    log = graph / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    removed, refused, kept = heal._sweep_finished_worktrees(graph)
    assert (removed, refused, kept) == (2, 0, 0)
    assert not wt_a.exists(), "byte-equal copy is home -> removed"
    assert _ref(repo, "refs/archive/worktrees/a00-3333cc-dirty") == "", \
        "a home tree needs no archive"
    assert not wt_b.exists(), "not home (target exists) -> archived, removed"
    assert _archived(repo, "refs/archive/worktrees/a00-4444dd-dirty",
                     ".agi/sessions/iter-702") == src_b
    assert (tgt_b / "output.log").read_text() == "foreign byte differs\n", \
        "the differing foreign bytes survive untouched"
    text = log.read_text()
    assert "removed a00-3333cc iter=iter-701" in text
    assert "archived a00-4444dd (sessions 1)" in text


# ---------------------------------------------------------------------------
# hypothesis:l5-the-sweep-fails-closed-on-a-staged-rename-or-copy-entry
#
# `_sweep_dirty_paths` must return the DESTINATION path of a porcelain v1
# rename/copy entry, not the literal non-path string `ORIG -> DEST`. The
# pre-fix `ln[3:].strip().strip('"')` produced the arrow literal, which
# `_sweep_park_leftovers`' `(wt / rel).is_file()` filter then dropped
# silently (0 files copied, not the fail-closed -1). Exercised against REAL
# git bytes wherever git can emit the shape; a `C` entry git-status does not
# emit here is covered by a hand-written line.
# ---------------------------------------------------------------------------
def _rename_repo(tmp_path):
    """A throwaway repo with one committed file — the fixture the rename
    shapes are read from as real `git status --porcelain` bytes."""
    repo = tmp_path / "rename-repo"
    repo.mkdir()
    _sh("git", "-C", str(repo), "init", "-q", ".")
    _sh("git", "-C", str(repo), "config", "user.email", "t@e.st")
    _sh("git", "-C", str(repo), "config", "user.name", "t")
    (repo / "old.txt").write_text("one\n")
    _sh("git", "-C", str(repo), "add", "-A")
    _sh("git", "-C", str(repo), "commit", "-qm", "init")
    return repo


def _porcelain(repo):
    out = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"],
                         capture_output=True, text=True, check=True)
    return out.stdout.splitlines()


def test_sweep_dirty_paths_rename_takes_destination(tmp_path):
    """Real `git mv`: the porcelain line is `R  old.txt -> new.txt`; the
    function must return the DESTINATION, not the arrow literal."""
    repo = _rename_repo(tmp_path)
    _sh("git", "-C", str(repo), "mv", "old.txt", "new.txt")
    lines = _porcelain(repo)
    assert lines == ["R  old.txt -> new.txt"], lines
    got = heal._sweep_dirty_paths(lines)
    assert got == ["new.txt"], got
    assert "old.txt -> new.txt" not in got, "the pre-fix arrow literal leaked"


def test_sweep_dirty_paths_rename_with_spaces_quotes_destination(tmp_path):
    """Git quotes each side separately: `RM old.txt -> "new name.txt"`. The
    destination keeps its spaces and loses its quotes."""
    repo = _rename_repo(tmp_path)
    _sh("git", "-C", str(repo), "mv", "old.txt", "new name.txt")
    (repo / "new name.txt").write_text("one\ntwo\n")
    lines = _porcelain(repo)
    assert lines == ['RM old.txt -> "new name.txt"'], lines
    assert heal._sweep_dirty_paths(lines) == ["new name.txt"]


def test_sweep_dirty_paths_rename_into_sessions_is_still_filtered(tmp_path):
    """The `.agi/sessions/` filter must apply to the DESTINATION: a rename
    INTO the tolerated scratch dir is dropped, not parked."""
    repo = _rename_repo(tmp_path)
    (repo / ".agi" / "sessions").mkdir(parents=True)
    _sh("git", "-C", str(repo), "mv", "old.txt", ".agi/sessions/keep.txt")
    lines = _porcelain(repo)
    assert lines == ["R  old.txt -> .agi/sessions/keep.txt"], lines
    assert heal._sweep_dirty_paths(lines) == []


def test_sweep_dirty_paths_rename_dest_containing_arrow(tmp_path):
    """THE case that must never regress: a destination that itself contains
    ` -> ` is C-quoted by git, so `split(" -> ")`/`parts[-1]` tears it and
    yields a path that does not exist — the silent drop this node exists to
    kill. Real git bytes, real `git mv`."""
    repo = _rename_repo(tmp_path)
    _sh("git", "-C", str(repo), "mv", "old.txt", "b -> c.txt")
    lines = _porcelain(repo)
    assert lines == ['R  old.txt -> "b -> c.txt"'], lines
    got = heal._sweep_dirty_paths(lines)
    assert got == ["b -> c.txt"], got
    assert (repo / got[0]).is_file(), "the returned path must exist"


def test_sweep_dirty_paths_quoted_orig_containing_arrow(tmp_path):
    """Both sides quoted, both containing the separator: the ORIG side must
    be consumed quote-awarely or the split tears the destination too."""
    repo = _rename_repo(tmp_path)
    (repo / "a -> b.txt").write_text("x\n")
    _sh("git", "-C", str(repo), "add", "-A")
    _sh("git", "-C", str(repo), "commit", "-qm", "add")
    _sh("git", "-C", str(repo), "mv", "a -> b.txt", "c -> d.txt")
    lines = _porcelain(repo)
    assert lines == ['R  "a -> b.txt" -> "c -> d.txt"'], lines
    assert heal._sweep_dirty_paths(lines) == ["c -> d.txt"]
    assert (repo / "c -> d.txt").is_file()


def test_sweep_dirty_paths_rename_dest_with_escaped_quote(tmp_path):
    """A `"` in the destination is escaped (`\\"`) inside the C-quoted side;
    unquoting must resolve the escape, not leave the backslash in the path."""
    repo = _rename_repo(tmp_path)
    _sh("git", "-C", str(repo), "mv", "old.txt", 'quote"name.txt')
    lines = _porcelain(repo)
    assert lines == ['R  old.txt -> "quote\\"name.txt"'], lines
    assert heal._sweep_dirty_paths(lines) == ['quote"name.txt']


def test_sweep_dirty_paths_ordinary_entries_unchanged():
    """Non-rename entries keep their existing meaning — a copy entry takes
    the destination, an ordinary modification keeps the whole path."""
    lines = [" M src/a.py", "?? notes.txt",
             'R  "old a.txt" -> "new a.txt"',
             "C  src/base.py -> src/copied.py",
             "R  malformed-no-arrow"]
    got = heal._sweep_dirty_paths(lines)
    assert got == ["src/a.py", "notes.txt", "new a.txt",
                   "src/copied.py", "malformed-no-arrow"], got
    assert not any(" -> " in p for p in got), \
        "no arrow literal may survive as a path"


def test_sweep_dirty_paths_rename_nonascii_dest_round_trips(tmp_path):
    """git C-quotes every byte >= 0x80 as an octal escape, so `git mv old.txt
    'é.txt'` yields `R  old.txt -> "\\303\\251.txt"`. The unquote must resolve
    the octal escapes back to the on-disk bytes; assert the PATH exists, not a
    spelling, so this proves the path rather than the escape."""
    repo = _rename_repo(tmp_path)
    _sh("git", "-C", str(repo), "mv", "old.txt", "é.txt")
    lines = _porcelain(repo)
    assert lines == ['R  old.txt -> "\\303\\251.txt"'], lines
    got = heal._sweep_dirty_paths(lines)
    assert len(got) == 1, got
    assert (repo / got[0]).is_file(), \
        f"returned {got[0]!r} is not a file on disk"
    assert (repo / got[0]).read_text() == "one\n"


def test_sweep_dirty_paths_ordinary_nonascii_entry_round_trips(tmp_path):
    """A plain untracked non-ASCII entry (`?? "\\303\\251.txt"`) takes the
    non-rename branch and must also resolve to a path that is_file()."""
    repo = _rename_repo(tmp_path)
    (repo / "é.txt").write_text("hi\n")
    lines = _porcelain(repo)
    assert lines == ['?? "\\303\\251.txt"'], lines
    got = heal._sweep_dirty_paths(lines)
    assert len(got) == 1, got
    assert (repo / got[0]).is_file(), \
        f"returned {got[0]!r} is not a file on disk"


def test_porcelain_unquote_full_escape_set_round_trips():
    """The whole C escape set git can emit in one quoted field: the letter
    escapes, the octal byte escapes (UTF-8 and an invalid byte), a literal
    backslash and an escaped quote."""
    # "\303\251" -> é (UTF-8), "\377" -> a raw 0xFF byte (surrogateescape).
    field = '"a\\tb\\nc\\"d\\\\e\\303\\251\\377.txt"'
    got = heal._porcelain_unquote(field)
    expected = ("a\tb\nc\"d\\e" "é" "\udcff" ".txt")
    assert got == expected, (got, expected)
    # and it survives a UTF-8 re-encode as the original bytes
    assert got.encode("utf-8", "surrogateescape") == \
        b"a\tb\nc\"d\\e\xc3\xa9\xff.txt"


def test_sweep_does_not_rearchive_a_locked_tree_until_its_state_changes(
        repo_root, four_worktrees, monkeypatch):
    """SM-1: a locked dirty tree cannot be removed (no second --force). Pass 1
    archives it once and refuses WITH git's reason; pass 2 (same bytes) writes
    no second archive and never removes it; one new byte in the already-
    modified file (status lines unchanged) is archived again."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    wt, ref = four_worktrees["a00-bbbb22"], "refs/archive/worktrees/a00-bbbb22-dirty"
    _sh("git", "-C", str(repo_root), "worktree", "lock", str(wt))
    n = lambda: log.read_text().count("[sweep] archived a00-bbbb22")
    heal._sweep_finished_worktrees(_graph(repo_root))
    first = _ref(repo_root, ref)
    assert first and n() == 1
    assert "[sweep] refused a00-bbbb22: remove failed (" in log.read_text()
    assert "locked" in log.read_text().split("[sweep] refused a00-bbbb22")[1]
    heal._sweep_finished_worktrees(_graph(repo_root))
    assert n() == 1 and _ref(repo_root, ref) == first, "same state: not re-archived"
    assert wt.exists(), "a locked tree is never removed"
    (wt / "base.txt").write_text("base\nmodified\nmore\n")
    heal._sweep_finished_worktrees(_graph(repo_root))
    assert n() == 2 and _ref(repo_root, ref) != first, "changed state: archived again"
    assert wt.exists()


@pytest.mark.parametrize("name,change", [
    ("a00-bbbb22", "untracked"), ("a00-bbbb22", "head_move"),
    ("a00-dddd44", None)])
def test_sweep_locked_tree_rearchived_only_when_changed_beyond_archive(
        repo_root, four_worktrees, monkeypatch, name, change):
    """SM-1b: a locked tree matching its archive is re-archived for a NEW
    untracked file or a HEAD move; a CLEAN one (no -dirty ref) writes once."""
    log, wt = _graph(repo_root) / "reaper.log", four_worktrees[name]
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    _sh("git", "-C", str(repo_root), "worktree", "lock", str(wt))
    sweep = lambda: heal._sweep_finished_worktrees(_graph(repo_root))
    n = lambda: log.read_text().count(f"[sweep] archived {name}")
    sweep(), sweep()
    assert n() == 1
    if change:
        (wt / "new.txt").write_text("x\n")
    if change == "head_move":
        _sh("git", "-C", str(wt), "add", "new.txt")
        _sh("git", "-C", str(wt), "commit", "-q", "-m", "more")
    sweep()
    assert n() == (2 if change else 1) and wt.exists()
    assert bool(_ref(repo_root, f"refs/archive/worktrees/{name}-dirty")) == (name == "a00-bbbb22")


def test_sweep_refuses_an_orphan_tree_once_by_name(repo_root, monkeypatch):
    """DG2.C1: a tree whose admin dir under .git/worktrees is gone has no
    HEAD; it is refused BY NAME, never logged "archived" (no ref was written),
    and the next pass does not try it again."""
    log = _graph(repo_root) / "reaper.log"
    monkeypatch.setenv("AGI_REAPER_LOG", str(log))
    wt = _cut(repo_root, "a00-orph99", "loop/o-O@2")
    (wt / "stray.txt").write_text("bytes\n")
    shutil.rmtree(repo_root / ".git" / "worktrees" / "a00-orph99")
    assert wt.is_dir() and "a00-orph99" not in subprocess.run(
        ["git", "-C", str(repo_root), "worktree", "list"],
        capture_output=True, text=True).stdout
    sweep = lambda: heal._sweep_finished_worktrees(_graph(repo_root))
    removed, refused, _ = sweep()
    text = log.read_text()
    assert (removed, refused) == (0, 1)
    refusal = [l for l in text.splitlines() if "refused a00-orph99" in l]
    assert len(refusal) == 1 and "orphan" in refusal[0] and "gitdir gone" in refusal[0]
    assert "archived a00-orph99" not in text
    assert not _ref(repo_root, "refs/archive/worktrees/a00-orph99")
    sweep()
    after = log.read_text()
    assert after.count("a00-orph99") == 1 and "archived a00-orph99" not in after
    assert (wt / "stray.txt").exists(), "an orphan's bytes are never removed"
