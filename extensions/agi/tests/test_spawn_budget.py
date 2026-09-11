"""goal:g4.8 item 3 — a concurrency bound that survives a tier.

`spawn.parallel` bounds one invocation's slots. These tests exercise the
property it does NOT have and the lease directory does: that a SECOND,
independent spawner — which is what a parent spawning its own kids is — counts
against the same budget as the first.

The population test is the falsifier itself, run for real: N spawners racing
through the same admission path against one tree, asserting the peak live count
never exceeds the declared bound. It is deliberately a concurrency test with
real processes rather than a unit test of the counter, because `goal:s28` is
the standing proof in this repo that a read-merge-write cycle can look correct
and lose 6 of 8 entries under exactly that load.
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import spawn_budget  # noqa: E402


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    (tmp_path / "sessions").mkdir()
    return tmp_path


# --------------------------------------------------------------------------
# The bound itself
# --------------------------------------------------------------------------

def test_acquire_admits_up_to_the_cap_and_then_refuses(root: Path):
    leases = [spawn_budget.acquire(root, 3, f"a{i}") for i in range(3)]
    assert all(l is not None for l in leases)
    assert spawn_budget.live_count(root) == 3
    assert spawn_budget.acquire(root, 3, "a3") is None, (
        "the fourth agent must be refused, not queued")


def test_acquire_refuses_while_paused_and_admits_once_resumed(root: Path):
    """hypothesis:l3-reaper-restarts-through-stop — the structural form of
    an owner stop order. Refuses even with the cap wide open; resumes
    cleanly once cleared."""
    assert spawn_budget.acquire(root, 25, "before-pause") is not None
    spawn_budget.pause(root, reason="owner: low on tokens", actor="belam")
    assert spawn_budget.acquire(root, 25, "during-pause") is None, (
        "acquire must refuse every new admission while paused, "
        "regardless of how much of the cap is free")
    assert spawn_budget.live_count(root) == 1, (
        "the refused acquire must not have written a lease")
    prev = spawn_budget.resume(root)
    assert prev is not None and prev["reason"] == "owner: low on tokens"
    assert spawn_budget.acquire(root, 25, "after-resume") is not None


def test_is_paused_reports_reason_and_actor(root: Path):
    assert spawn_budget.is_paused(root) is None
    spawn_budget.pause(root, reason="survival mode", actor="belam")
    rec = spawn_budget.is_paused(root)
    assert rec is not None
    assert rec["reason"] == "survival mode"
    assert rec["actor"] == "belam"
    assert rec["paused"] is True
    assert isinstance(rec["paused_at"], int)


def test_resume_without_a_prior_pause_is_a_no_op(root: Path):
    assert spawn_budget.resume(root) is None
    assert spawn_budget.is_paused(root) is None


def test_refusal_while_paused_is_not_a_wait(root: Path):
    """Same non-blocking guarantee the cap refusal already has (see
    `test_refusal_is_not_a_wait` below) — a paused refusal must not stall
    either."""
    spawn_budget.pause(root, reason="test")
    t0 = time.monotonic()
    assert spawn_budget.acquire(root, 25, "blocked-by-pause") is None
    assert time.monotonic() - t0 < 0.5


def test_refusal_is_not_a_wait(root: Path):
    """Admission returns immediately when full.

    Blocking is the tempting alternative and it deadlocks this exact topology:
    parents holding every lease, each blocked on a kid that cannot be admitted
    until a parent finishes. The bound must degrade to fewer agents, never to
    a stall.
    """
    spawn_budget.acquire(root, 1, "only")
    t0 = time.monotonic()
    assert spawn_budget.acquire(root, 1, "second") is None
    assert time.monotonic() - t0 < 0.5


def test_releasing_a_lease_frees_the_slot(root: Path):
    lease = spawn_budget.acquire(root, 1, "a0")
    assert spawn_budget.acquire(root, 1, "a1") is None
    spawn_budget.release(lease)
    assert spawn_budget.acquire(root, 1, "a1") is not None


# --------------------------------------------------------------------------
# Reclamation is by liveness, so no cleanup path can leak a slot
# --------------------------------------------------------------------------

def test_a_dead_agents_lease_is_reclaimed_without_anyone_releasing_it(root: Path):
    """A killed agent frees its slot with no cleanup step run anywhere.

    This is the property that makes the bound safe to enforce at all: if slots
    were freed only by an explicit release, one `kill -9` would shrink the
    budget permanently and the safety rail would become an outage.
    """
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    lease = spawn_budget.acquire(root, 1, "doomed")
    spawn_budget.commit(lease, proc.pid)
    assert spawn_budget.live_count(root) == 1

    proc.kill()
    proc.wait()
    assert spawn_budget.live_count(root) == 0, (
        "a dead agent must not keep holding a slot")
    assert spawn_budget.acquire(root, 1, "next") is not None


def test_a_reservation_is_held_by_the_dispatcher_until_a_pid_exists(root: Path):
    """The window between reserving and `Popen` returning is covered.

    Before `commit`, the lease is held by the reserving process. That is what
    stops two dispatchers from both counting the same free slot while neither
    has started a child yet.
    """
    lease = spawn_budget.acquire(root, 1, "reserved")
    rec = json.loads(lease.path.read_text())
    assert rec["agent_pid"] is None
    assert rec["holder_pid"] == os.getpid()
    assert spawn_budget.live_count(root) == 1, (
        "an uncommitted reservation still occupies its slot")


def test_a_lease_whose_holder_died_before_spawning_is_reclaimed(root: Path):
    """A dispatcher that dies between reserving and spawning leaks nothing."""
    d = spawn_budget.budget_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait()
    (d / "ghost.lease").write_text(json.dumps({
        "agent_id": "ghost", "holder_pid": dead.pid, "agent_pid": None,
    }))
    assert spawn_budget.live_count(root) == 0
    assert not (d / "ghost.lease").exists(), "a dead lease is swept, not kept"


def test_a_zombie_lease_is_reclaimed_hypothesis_l3_zombie(root: Path):
    """A defunct (state Z) child does not hold a slot.

    `hypothesis:l3-cc-adapter-zombie-lease`: an unreaped child still answers
    `os.kill(pid, 0)`, so signal-existence alone would hold every finished
    claude-code agent's lease forever. Liveness reads the process-table state:
    a zombie is dead and is swept.
    """
    pid = os.fork()
    if pid == 0:  # child exits; parent never waits before the sweep
        os._exit(0)
    try:
        time.sleep(0.2)  # let the child die and the defunct state settle
        state = open(f"/proc/{pid}/stat").read().rsplit(") ", 1)[1].split()[0]
        assert state == "Z", f"expected a zombie, got state {state!r}"
        assert not spawn_budget._pid_alive(pid), "a zombie is dead, not live"
        lease = spawn_budget.acquire(root, 1, "zombie-agent")
        assert lease is not None
        spawn_budget.commit(lease, pid)
        assert lease.path.exists(), "lease exists before the sweep that frees it"
        assert spawn_budget.live_count(root) == 0, "a zombie-held slot is freed"
        assert not lease.path.exists(), "the sweep removed the dead lease"
    finally:
        os.waitpid(pid, 0)


def test_a_corrupt_lease_cannot_wedge_the_budget_shut(root: Path):
    """An unparseable lease is dropped rather than believed forever."""
    d = spawn_budget.budget_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    (d / "half-written.lease").write_text("{not json")
    assert spawn_budget.live_count(root) == 0
    assert spawn_budget.acquire(root, 1, "a0") is not None


# --------------------------------------------------------------------------
# Config resolution
# --------------------------------------------------------------------------

def test_max_live_prefers_its_own_key_then_falls_back_to_parallel():
    assert spawn_budget.max_live({"spawn": {"max_live": 5, "parallel": 2}}) == 5
    assert spawn_budget.max_live({"spawn": {"parallel": 2}}) == 2, (
        "a project that never heard of this key gets a bound equal to the "
        "slot count it already believed it was running")
    assert spawn_budget.max_live({"agent_dispatch": {"claude_max_parallel": 3}}) == 3
    assert spawn_budget.max_live({}) == spawn_budget.DEFAULT_MAX_LIVE


# --------------------------------------------------------------------------
# The falsifier: the total live population never exceeds the bound
# --------------------------------------------------------------------------

def _grab(root_s: str, cap: int, n: int, idx: int, peaks) -> None:
    """One independent spawner: take slots, sample the population, drop them."""
    root = Path(root_s)
    held = []
    for i in range(n):
        lease = spawn_budget.acquire(root, cap, f"p{idx}-k{i}")
        if lease is None:
            continue
        spawn_budget.commit(lease, os.getpid())
        held.append(lease)
        peaks.append(spawn_budget.live_count(root))
        time.sleep(0.01)
    for lease in held:
        spawn_budget.release(lease)


@pytest.mark.parametrize("cap", [1, 3, 5])
def test_the_live_population_never_exceeds_the_bound_under_concurrency(root: Path, cap: int):
    """`goal:g4.8`'s falsifier clause, run rather than asserted.

    Five independent spawners, five slots each — the 5x5 shape the owner
    asked for — racing through one lease directory. Twenty-five would-be
    agents; the peak live count must never pass `cap`.

    `spawn.parallel` alone cannot make this pass at any cap below 25: each
    spawner reads the same number and opens its own population. That is the
    whole distinction this module exists for.
    """
    ctx = mp.get_context("fork")
    with ctx.Manager() as mgr:
        peaks = mgr.list()
        procs = [ctx.Process(target=_grab, args=(str(root), cap, 5, i, peaks))
                 for i in range(5)]
        for p in procs:
            p.start()
        for p in procs:
            p.join(timeout=60)
        observed = list(peaks)

    assert observed, "no spawner was admitted at all"
    assert max(observed) <= cap, (
        f"live population reached {max(observed)} against a declared bound of "
        f"{cap} — the grandchild hole is still open")


def test_a_second_independent_spawner_counts_against_the_first(root: Path):
    """The grandchild property, stated at its smallest.

    A parent runs `dispatch.py` again. That second invocation reads the same
    `spawn.parallel` the first one did, so nothing in the config can stop it
    opening a fresh population. Shared state can, and this is that state.
    """
    parent_lease = spawn_budget.acquire(root, 2, "parent-0")
    spawn_budget.commit(parent_lease, os.getpid())

    code = (
        "import sys; sys.path.insert(0, %r);\n"
        "import spawn_budget;\n"
        "a = spawn_budget.acquire(%r, 2, 'kid-0');\n"
        "b = spawn_budget.acquire(%r, 2, 'kid-1');\n"
        "print(int(a is not None), int(b is not None))\n"
        % (str(BIN), str(root), str(root))
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True,
                         text=True, check=True).stdout.split()
    assert out == ["1", "0"], (
        "the second spawner saw the first's lease and was cut off at the "
        "shared bound, not at its own")


# --------------------------------------------------------------------------
# The budget is ONE directory across worktrees (hypothesis:l3w4)
# --------------------------------------------------------------------------

def test_budget_dir_is_shared_across_a_linked_worktree(tmp_path: Path):
    """A lease taken from a worktree lands in the MAIN checkout's budget.

    `hypothesis:l3w4-parent-branch-merge-up`: a parent dispatched with
    `--branch` runs in its own git worktree; its kids edit only that worktree.
    The budget must NOT follow the worktree root or the tree-wide bound
    silently splits per worktree — the whole thing
    `spawn_budget.py` exists to enforce (goal:g4.8 item 3).

    `hypothesis:l3-budget-dir-dropped-agi`: under G11 the graph lives at
    `<repo>/.agi` and the budget must resolve to `<repo>/.agi/sessions/
    .spawn-budget` — never a stray `<repo>/sessions/` and never a
    per-worktree split. The exact `.agi` path is asserted so a regression
    that drops the graph-dir segment fails red on both the main checkout and
    the worktree.
    """
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "master"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / "README").write_text("x")
    # G11 layout: the graph root is a resolveable `.agi` dir with a config.
    graph = repo / ".agi"
    graph.mkdir()
    (graph / "config.json").write_text("{}")
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)

    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/slug@s2", str(wt), "master"],
                   check=True, capture_output=True)

    expected = repo / ".agi" / "sessions" / ".spawn-budget"
    assert spawn_budget.budget_dir(repo) == expected, (
        "the main checkout's budget must keep the .agi graph-dir segment: "
        "<repo>/.agi/sessions/.spawn-budget, not <repo>/sessions/.spawn-budget")
    assert spawn_budget.budget_dir(wt) == expected, (
        "a worktree's budget must be the MAIN checkout's `.agi` graph dir, "
        "never a per-worktree split and never a dropped `.agi` segment")
    assert spawn_budget.acquire(wt, 2, "wt-agent") is not None
    # The lease is visible from the main checkout and from the worktree alike.
    assert spawn_budget.live_count(repo) == 1
    assert spawn_budget.live_count(wt) == 1
    assert (expected / "wt-agent.lease").is_file(), (
        "the lease file lives in the main checkout's budget dir")


# --------------------------------------------------------------------------
# hypothesis:l3w4-parent-branch-merge-up — the lease records the branch
# --------------------------------------------------------------------------


def test_attach_branch_records_branch_base_and_worktree_on_the_lease(root):
    """A `--branch` spawn records where its branch belongs on the LEASE, so
    `season.py merge-up --record <lease>` (or the agent record) can climb the
    branch into its recorded base even after the agent has gone."""
    lease = spawn_budget.acquire(root, 2, "branch-agent")
    assert lease is not None
    spawn_budget.attach_branch(lease, {
        "branch": "loop/explore-a00-xy@s2",
        "base_branch": "season/s1",
        "worktree": "/tmp/main/.agi/worktrees/a00-xy",
    })
    rec = json.loads(lease.path.read_text())
    assert rec["branch"] == "loop/explore-a00-xy@s2"
    assert rec["base_branch"] == "season/s1"
    assert rec["worktree"] == "/tmp/main/.agi/worktrees/a00-xy"


def test_a_lease_without_an_iteration_is_loud_in_status(root, capsys):
    """hypothesis:l3-killed-agent-restarts-unattributed — `iter=None` on a live
    lease must be loud, not a silent count that holds a round open forever.
    Every spawner passes iter_n, so None here is a defect and status flags it.
    """
    (root / ".agi").mkdir()
    (root / ".agi" / "config.json").write_text('{}')
    lease = spawn_budget.acquire(root, 10, "a00-orphan-r1", tier="parent")  # no iter_n
    assert lease is not None
    spawn_budget.main(["--root", str(root), "status"])
    out = capsys.readouterr().out
    assert "UNATTRIBUTED" in out, out
    assert "iter=None" in out, out


def test_a_lease_recorded_with_an_iteration_is_attributed(root, capsys):
    """The attribution seam: a lease acquired with an iteration id renders it
    plainly in status, so a restart that inherits its round is visible to it.
    """
    (root / ".agi").mkdir()
    (root / ".agi" / "config.json").write_text('{}')
    lease = spawn_budget.acquire(root, 10, "a00-healthy-r1", tier="kid", iter_n=342)
    assert lease is not None
    spawn_budget.main(["--root", str(root), "status"])
    out = capsys.readouterr().out
    assert "iter=342" in out, out
    assert "UNATTRIBUTED" not in out, out


def test_attach_branch_ignores_empty_fields(root):
    """An attach with no branch fields must leave the lease unchanged except
    its mandatory keys — never write empty-string placeholders."""
    lease = spawn_budget.acquire(root, 2, "plain-agent")
    assert lease is not None
    spawn_budget.attach_branch(lease, {})
    rec = json.loads(lease.path.read_text())
    assert "branch" not in rec
    assert "base_branch" not in rec
    assert "worktree" not in rec
    assert rec["agent_id"] == "plain-agent"


# --------------------------------------------------------------------------
# The pause flag, CLI surface (hypothesis:l3-reaper-restarts-through-stop)
# --------------------------------------------------------------------------

def test_cli_pause_then_status_shows_the_banner_then_resume_clears_it(root, capsys):
    (root / ".agi").mkdir()
    (root / ".agi" / "config.json").write_text('{}')

    rc = spawn_budget.main(["--root", str(root), "pause",
                            "--reason", "owner: low on tokens", "--actor", "belam"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "paused" in out.lower()

    spawn_budget.main(["--root", str(root), "status"])
    out = capsys.readouterr().out
    assert "PAUSED" in out
    assert "owner: low on tokens" in out
    assert "belam" in out

    rc = spawn_budget.main(["--root", str(root), "resume"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "resumed" in out.lower()
    assert "owner: low on tokens" in out

    spawn_budget.main(["--root", str(root), "status"])
    out = capsys.readouterr().out
    assert "PAUSED" not in out


def test_cli_resume_with_nothing_to_resume_says_so(root, capsys):
    (root / ".agi").mkdir()
    (root / ".agi" / "config.json").write_text('{}')
    rc = spawn_budget.main(["--root", str(root), "resume"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "not paused" in out.lower()


# --------------------------------------------------------------------------
# hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled — `status --iter`
# --------------------------------------------------------------------------

def _sleeping():
    """A live, idle process (sleeping, 0 CPU ticks, 0 sockets)."""
    return subprocess.Popen([sys.executable, "-c",
                             "import time, signal; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(120)"])


def _mk_project(root: Path) -> None:
    (root / ".agi").mkdir(exist_ok=True)
    (root / ".agi" / "config.json").write_text('{}')


def test_status_iter_parent_with_live_kid_is_never_a_stall_candidate(root, capsys):
    """The falsifier, run for real: parent + live kid must NOT be a candidate."""
    _mk_project(root)
    parent = _sleeping()
    kid = _sleeping()
    p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent", iter_n=140)
    spawn_budget.commit(p_lease, parent.pid)
    k_lease = spawn_budget.acquire(root, 2, "kid-0", tier="kid", iter_n=140)
    spawn_budget.commit(k_lease, kid.pid)
    try:
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.140"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "STALL-CANDIDATE" not in out, out
        assert "1 live kid(s)" in out, out
        assert "round L140:" in out, out
    finally:
        for p in (parent, kid):
            p.kill(); p.wait()


def test_status_iter_parent_alone_idle_is_a_stall_candidate(root, capsys):
    """Parent alive but idle (0 ticks, 0 sockets, no done) and no kid → candidate."""
    _mk_project(root)
    parent = _sleeping()
    p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent", iter_n=141)
    spawn_budget.commit(p_lease, parent.pid)
    try:
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.141"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "STALL-CANDIDATE:" in out, out
        assert "0 live kids" in out, out
        assert "0 ticks" in out, out
        assert "0 sockets" in out, out
    finally:
        parent.kill(); parent.wait()


def test_status_iter_string_iter_lease_matches_and_reads_agent_json(root, capsys):
    """A REAL lease stores `iter` as the string 'L4.NNN' (locations.
    iteration_id), never an int. The old int-only comparison (`rec.get("iter")
    == nnn`) never matched a live round and `iter-L{int}` never found the
    agent.json. The parent+kid round with a STRING iter must be FOUND."""
    _mk_project(root)
    parent = _sleeping()
    kid = _sleeping()
    p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent", iter_n="L4.167")
    spawn_budget.commit(p_lease, parent.pid)
    k_lease = spawn_budget.acquire(root, 2, "kid-0", tier="kid", iter_n="L4.167")
    spawn_budget.commit(k_lease, kid.pid)
    # real agent.json lives in the sessions dir named from the genuine id
    for leaf in ("parent-0", "kid-0"):
        ajson = root / ".agi" / "sessions" / "iter-L4.167" / leaf / "agent.json"
        ajson.parent.mkdir(parents=True)
        ajson.write_text('{"status": "running"}')
    try:
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.167"])
        out = capsys.readouterr().out
        assert rc == 0, out
        assert "STALL-CANDIDATE" not in out, out
        assert "1 live kid(s)" in out, out
        assert out.count("agent=running") == 2, out
        assert "(no agent.json)" not in out, out
    finally:
        for p in (parent, kid):
            p.kill(); p.wait()


def test_status_iter_unknown_iteration_names_it_and_exits_1(root, capsys):
    """An unknown iteration is a NAMED message, exit 1 — never a silent 0."""
    _mk_project(root)
    rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.99999"])
    out = capsys.readouterr().err
    assert rc == 1
    assert "no live agents in iteration L99999" in out, out
    # bad format is also a named refusal
    rc2 = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.xyz"])
    out2 = capsys.readouterr().err
    assert rc2 == 1
    assert "unknown iteration" in out2, out2
