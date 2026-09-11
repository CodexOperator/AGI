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


@pytest.fixture()
def fast_tick_sample(monkeypatch):
    """`status --iter` samples CPU over TICK_SAMPLE_SECONDS (8 s). Tests must
    not sleep 8 real seconds each, so shrink the module seam to nearly
    nothing. The seam is `spawn_budget._STATUS_SAMPLE_SECONDS` — a test that
    reads the documented constant instead of monkeypatching it back into a
    bare literal keeps both the definition and the seam honest."""
    assert spawn_budget.TICK_SAMPLE_SECONDS == 8
    monkeypatch.setattr(spawn_budget, "_STATUS_SAMPLE_SECONDS", 0.01)
    yield spawn_budget


def _mk_project(root: Path) -> None:
    (root / ".agi").mkdir(exist_ok=True)
    (root / ".agi" / "config.json").write_text('{}')


def test_status_iter_parent_with_live_kid_is_never_a_stall_candidate(root, capsys, fast_tick_sample):
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


def test_status_iter_parent_alone_idle_is_a_stall_candidate(root, capsys, fast_tick_sample):
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


def test_status_iter_string_iter_lease_matches_and_reads_agent_json(root, capsys, fast_tick_sample):
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


def test_status_iter_prints_running_overdue_for_a_live_past_deadline_kid(root, capsys, fast_tick_sample):
    """hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-
    print-it — heal.py keeps a live past-deadline agent's status `running`
    and adds `overdue_since`/`overdue_reason`; it NEVER sets status=overdue.
    So the parent brief must not tell a parent to read a `status reads
    overdue` word that nothing emits, and THIS reader must print
    `agent=running(overdue)` — the word the brief now names. A record with
    `status: running` + `overdue_since` must therefore print `running(overdue)`, and
    a plain running record must stay `agent=running` with no suffix."""
    _mk_project(root)
    parent = _sleeping()
    overdue = _sleeping()
    plain = _sleeping()
    p_lease = spawn_budget.acquire(root, 3, "parent-0", tier="parent", iter_n="L4.168")
    spawn_budget.commit(p_lease, parent.pid)
    o_lease = spawn_budget.acquire(root, 3, "kid-overdue", tier="kid", iter_n="L4.168")
    spawn_budget.commit(o_lease, overdue.pid)
    k_lease = spawn_budget.acquire(root, 3, "kid-plain", tier="kid", iter_n="L4.168")
    spawn_budget.commit(k_lease, plain.pid)
    for leaf, body in (("parent-0", '{"status": "running"}'),
                       ("kid-overdue", '{"status": "running", "overdue_since": 1700000000, "overdue_reason": "past manifest timeout_seconds=3600"}'),
                       ("kid-plain", '{"status": "running"}')):
        ajson = root / ".agi" / "sessions" / "iter-L4.168" / leaf / "agent.json"
        ajson.parent.mkdir(parents=True)
        ajson.write_text(body)
    try:
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.168"])
        out = capsys.readouterr().out
        assert rc == 0, out
        assert "agent=running(overdue)" in out, out
        assert out.count("agent=running") == 3, out
    finally:
        for p in (parent, overdue, plain):
            p.kill(); p.wait()


def test_status_iter_unparseable_iter_lease_prints_row_not_traceback(root, capsys, fast_tick_sample):
    """hypothesis:l4-agent-status-returns-three-on-every-path — a live lease
    whose `iter` field `_iter_num` matches but `locations.iteration_dirname`
    rejects drives `status --iter` INTO `_agent_status`'s `except ValueError`
    branch. That branch was a stale 2-TUPLE return (`"(no agent.json)", None`)
    after L4.232 made the contract a 3-tuple, so the caller's
    `status, src, overdue = _agent_status(...)` raised
    `ValueError: not enough values to unpack` — a crash in `status --iter`
    for a lease whose iter field does not parse. The row must PRINT, never
    traceback. The corrupt value is `"9.140"`: `_iter_num` strips it to 140
    (so the round matches `--iter L4.140`) but `iteration_id("9.140")` raises
    ValueError because a loop label must start with a letter."""
    _mk_project(root)
    parent = _sleeping()
    p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent", iter_n="L4.170")
    spawn_budget.commit(p_lease, parent.pid)
    rec = json.loads(p_lease.path.read_text())
    rec["iter"] = "9.140"
    p_lease.path.write_text(json.dumps(rec))
    try:
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.140"])
        out = capsys.readouterr().out
        assert rc == 0, out
        assert "parent-0 tier=" in out, out
        assert "(no agent.json)" in out, out
        assert "Traceback" not in out, out
    finally:
        parent.kill(); parent.wait()


def test_agent_status_finds_parent_record_under_a_seat_worktree(root: Path):
    """hypothesis:l4-spawn-budget-iter-reads-the-rounds-own-sessions-dir,
    MEASURED layout: a PARENT agent.json is written by the DISPATCHER into
    the DISPATCHING seat's worktree sessions dir
    (`<main>/.agi/worktrees/seat-sanctuary-director/.agi/sessions`). The
    lookup must find it there and name the root `seat:sanctuary-director`."""
    _mk_project(root)
    main_graph = root / ".agi"
    wt_graph = main_graph / "worktrees" / "seat-sanctuary-director" / ".agi"
    wt_graph.mkdir(parents=True, exist_ok=True)
    (wt_graph / "config.json").write_text("{}")
    ajson = wt_graph / "sessions" / "iter-L4.193" / "a00-06c44930" / "agent.json"
    ajson.parent.mkdir(parents=True)
    ajson.write_text('{"status": "running"}')
    status, src, overdue = spawn_budget._agent_status(root, "a00-06c44930", "L4.193")
    assert status == "running", status
    assert src == "seat:sanctuary-director", src


def test_agent_status_finds_kid_record_under_parents_worktree(root: Path):
    """MEASURED layout: a KID agent.json is written by its PARENT into the
    PARENT's worktree (`<main>/.agi/worktrees/<parent-id>/.agi/sessions`). The
    lookup must find it there and name the root `wt:<parent-id>`."""
    _mk_project(root)
    main_graph = root / ".agi"
    wt_graph = main_graph / "worktrees" / "a00-06c44930" / ".agi"
    wt_graph.mkdir(parents=True, exist_ok=True)
    (wt_graph / "config.json").write_text("{}")
    ajson = wt_graph / "sessions" / "iter-L4.193" / "a00-71de766d" / "agent.json"
    ajson.parent.mkdir(parents=True)
    ajson.write_text('{"status": "running"}')
    status, src, overdue = spawn_budget._agent_status(root, "a00-71de766d", "L4.193")
    assert status == "running", status
    assert src == "wt:a00-06c44930", src


def test_agent_status_finds_main_tree_record(root: Path):
    """A record under only MAIN's sessions dir is found and named `main`."""
    _mk_project(root)
    main_graph = root / ".agi"
    ajson = main_graph / "sessions" / "iter-L4.193" / "a0" / "agent.json"
    ajson.parent.mkdir(parents=True)
    ajson.write_text('{"status": "done"}')
    status, src, overdue = spawn_budget._agent_status(root, "a0", "L4.193")
    assert status == "done", status
    assert src == "main", src


def test_agent_status_own_candidate_from_its_own_seat_labels_seat_not_wt_agi(
        root: Path, monkeypatch):
    """hypothesis:l4-status-iter-labels-every-root-by-its-worktree-name —
    the FALSIFIER. Invoking `_agent_status` FROM a non-main worktree makes the
    record's OWN candidate the seat's own graph dir. The own candidate used to
    be labeled `wt_label(own)` where `own` is the GRAPH dir
    (`<worktree>/.agi`), whose `.name` is always `.agi` — so every record
    answered from its own root printed `@wt:.agi` (the label depended on where
    you stood: the same record printed `@seat:sanctuary-director` when reached
    through another tree's glob). The label must now derive from the WORKTREE
    directory (the graph dir's parent when the graph dir is `.agi`, else the
    graph dir itself), identically for the own and the glob candidates, so
    `@seat:sanctuary-director` prints from any tree.

    `git_common_root` is stubbed to the tmp main because a tmp tree has no real
    common git dir (in production it resolves the main checkout); the seat
    graph is a distinct path from it, which is what makes `own` non-main."""
    _mk_project(root)
    main_graph = root / ".agi"
    seat_graph = main_graph / "worktrees" / "seat-sanctuary-director" / ".agi"
    seat_graph.mkdir(parents=True, exist_ok=True)
    (seat_graph / "config.json").write_text("{}")
    ajson = seat_graph / "sessions" / "iter-L4.193" / "a00-06c44930" / "agent.json"
    ajson.parent.mkdir(parents=True)
    ajson.write_text('{"status": "running"}')
    monkeypatch.setattr(spawn_budget.locations, "git_common_root",
                        lambda g: root)
    status, src, overdue = spawn_budget._agent_status(
        root / ".agi" / "worktrees" / "seat-sanctuary-director",
        "a00-06c44930", "L4.193")
    assert status == "running", status
    assert src == "seat:sanctuary-director", src
    assert "wt:.agi" not in src, src


def test_agent_status_no_record_anywhere_is_no_agent_json(root: Path):
    """`(no agent.json)` is returned only when NOTHING holds the record —
    MAIN empty, no worktree, no seat — and then src is None."""
    _mk_project(root)
    # a seat and a parent worktree both exist but hold no record for `a0`
    for wt_name in ("seat-sanctuary-director", "a00-06c44930"):
        wt_graph = root / ".agi" / "worktrees" / wt_name / ".agi"
        wt_graph.mkdir(parents=True, exist_ok=True)
        (wt_graph / "config.json").write_text("{}")
    status, src, overdue = spawn_budget._agent_status(root, "a0", "L4.193")
    assert status == "(no agent.json)", status
    assert src is None, src


def test_status_iter_worktree_round_is_no_longer_a_false_negative(root, capsys, fast_tick_sample):
    """FALSIFIER of hypothesis:l4-spawn-budget-iter-reads-the-rounds-own-
    sessions-dir with the MEASURED layout. A parent dispatched from a seat
    keeps its agent.json in the seat worktree; its kid keeps its own in the
    parent's worktree. Before the fix both live rows printed `(no agent.json)`
    while both records sat on disk; now each is found and the column names
    the root as `@seat:<name>` / `@wt:<parent-id>`."""
    _mk_project(root)
    main_graph = root / ".agi"
    # seat worktree holds the PARENT record
    seat_graph = main_graph / "worktrees" / "seat-sanctuary-director" / ".agi"
    seat_graph.mkdir(parents=True, exist_ok=True)
    (seat_graph / "config.json").write_text("{}")
    (seat_graph / "sessions" / "iter-L4.193" / "parent-0").mkdir(parents=True)
    (seat_graph / "sessions" / "iter-L4.193" / "parent-0" / "agent.json").write_text(
        '{"status": "running"}')
    # parent's worktree holds the KID record
    parent_graph = main_graph / "worktrees" / "parent-0" / ".agi"
    parent_graph.mkdir(parents=True, exist_ok=True)
    (parent_graph / "config.json").write_text("{}")
    (parent_graph / "sessions" / "iter-L4.193" / "kid-0").mkdir(parents=True)
    (parent_graph / "sessions" / "iter-L4.193" / "kid-0" / "agent.json").write_text(
        '{"status": "running"}')
    parent = _sleeping()
    kid = _sleeping()
    try:
        p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent",
                                       iter_n="L4.193")
        spawn_budget.commit(p_lease, parent.pid)
        k_lease = spawn_budget.acquire(root, 2, "kid-0", tier="kid",
                                       iter_n="L4.193")
        spawn_budget.commit(k_lease, kid.pid)
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.193"])
        out = capsys.readouterr().out
        assert rc == 0, out
        assert "STALL-CANDIDATE" not in out, out
        assert "1 live kid(s)" in out, out
        assert "agent=running@seat:sanctuary-director" in out, out
        assert "agent=running@wt:parent-0" in out, out
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


# --------------------------------------------------------------------------
# hypothesis:l4-stall-candidate-measures-an-api-bound-parent-honestly — the
# verdict line must carry the numbers it measured, and STALL-CANDIDATE must
# fire ONLY when ticks AND sockets AND kids AND done all say stalled
# --------------------------------------------------------------------------

class _FakeSampler:
    """Injects the tick/socket samplers so the falsifier needs no real sockets
    and no 8 s wall clock. `_round_status` calls the module globals
    `_pid_ticks`/`_pid_sockets`, so monkeypatching them IS the seam."""

    def __init__(self, ticks_steps=(0, 0), sockets=0):
        self._steps = list(ticks_steps)
        self._sockets = sockets
        self._samples = []

    def ticks(self, pid):
        # sampled twice per pid (t0 then t1); the delta is what matters
        return self._steps.pop(0) if self._steps else 0

    def sockets(self, pid):
        return self._sockets


def test_status_iter_parent_with_ticks_but_no_sockets_is_reviewing_not_candidate(
        root, capsys, fast_tick_sample, monkeypatch):
    """THE FALSIFIER: a parent that consumed CPU over the sample (ticks > 0,
    0 sockets) must print `reviewing` and MUST NOT print STALL-CANDIDATE. The
    pre-fix code judged only on ticks and sockets from real /proc state over a
    2 s sample, so an API-bound parent could read 0/0 and be called stalled
    while alive. A fixture with ticks then positive proves the verdict path
    keeps the evidence it measured."""
    _mk_project(root)
    parent = _sleeping()
    p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent", iter_n="L4.170")
    spawn_budget.commit(p_lease, parent.pid)
    fake = _FakeSampler(ticks_steps=(0, 500), sockets=0)
    monkeypatch.setattr(spawn_budget, "_pid_ticks", fake.ticks)
    monkeypatch.setattr(spawn_budget, "_pid_sockets", fake.sockets)
    try:
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.170"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "STALL-CANDIDATE" not in out, out
        assert "reviewing" in out, out
        assert "ticks=500" in out, out
        assert "sockets=0" in out, out
    finally:
        parent.kill(); parent.wait()


def test_status_iter_parent_with_sockets_but_no_ticks_is_reviewing_not_candidate(
        root, capsys, fast_tick_sample, monkeypatch):
    """The mirror falsifier: a parent holding 3 sockets but 0 CPU ticks over
    the sample (mid-review between API calls, waiting on a control socket) must
    be `reviewing`, never STALL-CANDIDATE. The pre-fix helper counted only
    ESTABLISHED TCP (state 01), so a unix/LISTEN-holding parent read
    `sockets=0` and was falsely flagged."""
    _mk_project(root)
    parent = _sleeping()
    p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent", iter_n="L4.172")
    spawn_budget.commit(p_lease, parent.pid)
    fake = _FakeSampler(ticks_steps=(0, 0), sockets=3)
    monkeypatch.setattr(spawn_budget, "_pid_ticks", fake.ticks)
    monkeypatch.setattr(spawn_budget, "_pid_sockets", fake.sockets)
    try:
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.172"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "STALL-CANDIDATE" not in out, out
        assert "reviewing" in out, out
        assert "sockets=3" in out, out
        assert "ticks=0" in out, out
    finally:
        parent.kill(); parent.wait()


def test_status_iter_samples_tick_window_once_for_many_rows(root, capsys, monkeypatch):
    """The sample window is paid ONCE per round, not once per row. A round
    of 3+ live rows whose `status --iter` runs under a real (non-seam) window
    must finish in well under 3x that window. Per-row serial sleeps (the
    pre-fix shape) cost 3 windows and FAIL this assertion; concurrent
    sampling costs exactly one."""
    _mk_project(root)
    window = 0.2
    monkeypatch.setattr(spawn_budget, "_STATUS_SAMPLE_SECONDS", window)
    procs = [_sleeping() for _ in range(3)]
    for i, p in enumerate(procs):
        lease = spawn_budget.acquire(root, 3, f"parent-{i}", tier="parent", iter_n="L4.175")
        assert lease is not None
        spawn_budget.commit(lease, p.pid)
    try:
        t0 = time.monotonic()
        rc = spawn_budget.main(["--root", str(root), "status", "--iter", "L4.175"])
        elapsed = time.monotonic() - t0
        assert rc == 0
        assert elapsed < 2 * window, (
            f"window paid {elapsed:.2f}s for 3 rows; expected < 2*{window}s "
            f"({2*window:.2f}s). Serial per-row sleeps cost 3*{window}s "
            f"({3*window:.2f}s).")
    finally:
        for p in procs:
            p.kill(); p.wait()


def test_pid_sockets_counts_any_tcp_state_and_unix(tmp_path, monkeypatch):
    """The rewritten helper must count every socket the pid holds, in any TCP
    state plus unix — not just ESTABLISHED (01). Verifies the /proc parsing
    against a synthetic /proc tree redirected from a tmp dir, so it needs no
    real sockets and touches no real /proc."""
    import pathlib
    import spawn_budget as sb

    proc = tmp_path / "proc"
    (proc / "net").mkdir(parents=True)
    # pid holds two socket links: LISTEN (0A) tcp6 inode 111 and a unix socket
    # inode 222; the anon_inode must NOT count.
    fd = proc / "123" / "fd"
    fd.mkdir(parents=True)
    (fd / "3").symlink_to("socket:[111]")
    (fd / "4").symlink_to("socket:[222]")
    (fd / "5").symlink_to("anon_inode:[eventpoll]")
    # tcp6 lines in the REAL 17-column /proc layout: inode is index 9. States
    # 0A (LISTEN) and 12 (CLOSE_WAIT) — neither is 01, so the old helper that
    # counted only ESTABLISHED would have missed the LISTEN socket entirely.
    (proc / "net" / "tcp").write_text(
        "sl local rem st tx rx tr tm retr uid timeout inode\n")
    (proc / "net" / "tcp6").write_text(
        "sl local rem st tx rx tr tm retr uid timeout inode\n"
        " 0: 0100007F:04D2 00000000:0000 0A 00:00 0:0 0 0 0 111 1 0000 100 0 0 10 0\n"
        " 1: 0100007F:04D3 00000000:0000 12 00:00 0:0 0 0 0 999 1 0000 100 0 0 10 0\n")
    (proc / "net" / "unix").write_text(
        "Num RefCount Protocol Flags Type St Inode Path\n"
        "0000: 00000003 00000000 00000000 0001 03 222 /run/x.sock\n"
        "0001: 00000003 00000000 00000000 0001 03 555\n")

    _real = pathlib.Path

    def _redirect(p):
        s = str(p)
        # only the /proc strings the helper reads get redirected to the fake;
        # everything else is a normal real path (pytest's own tmp handling)
        if s == f"/proc/{123}/fd" or s.startswith("/proc/net/"):
            return _real(s.replace("/proc/", str(proc) + "/"))
        return _real(s)

    # patch the module's Path alias, not pathlib globally, so pytest's own
    # tmp_path bookkeeping is untouched and nothing recurses
    monkeypatch.setattr(sb, "Path", lambda p: _redirect(_real(p)))
    # LISTEN(0A) tcp6 inode 111 + unix inode 222 = 2; CLOSE_WAIT 999 and the
    # path-less unix 555 are not held by the pid; anon_inode never counts.
    assert sb._pid_sockets(123) == 2


def test_pid_sockets_returns_0_when_fd_dir_exits_mid_scan(tmp_path, monkeypatch):
    """A pid whose fd dir vanishes after the first entry is yielded must
    return 0, NOT raise. iterdir() is lazy, so a pid that exits mid-read raises
    FileNotFoundError/ProcessLookupError out of the `for fd in fds:` loop; the
    whole walk (listing + readlinks) must sit in one guarded try, else the
    exception escapes the helper up into status().

    The bomb here targets the FIXTURE fd dir built under tmp_path -- never the
    host's /proc/123/fd -- so the walk really walks `socket:[111]` and then
    raises on the second next(). This test was a NON-FALSIFIER while the bomb
    resolved `_real(str(p))` to the host path: on a box where pid 123 is
    unreadable/absent the iteration is empty and `== 0` held on pre-fix bytes
    too. The counterfactual and mutation assertions below pin both the fixture
    walk and the guard's load-bearingness."""
    import pathlib
    import shutil
    import spawn_budget as sb

    proc = tmp_path / "proc"
    (proc / "net").mkdir(parents=True)
    fd = proc / "123" / "fd"
    fd.mkdir(parents=True)
    (fd / "3").symlink_to("socket:[111]")

    _real = pathlib.Path
    _flav = _real(str(fd))._flavour

    # The bomb RECORDS that it fired at TEST scope (L4.276 build order): the
    # counterfactual must be asserted, not just implied by a deleted dir.
    # `fired` below stays PER-ITERDIR so each iterdir() fires exactly once; the
    # recorded `bomb_fired` accumulates so the test can assert it and re-arm it
    # across the two walks (the mutant check, then the real helper).
    bomb_fired = False

    def _bomb_path():
        """A Path over the FIXTURE fd dir whose iterdir() yields one entry,
        deletes that fixture, then raises FileNotFoundError on the SECOND
        next() -- the process-exits-mid-read condition. Pointed at the fixture
        (closure `fd`), not the host path, so the walk really yields
        `socket:[111]` before the dir vanishes.

        The rmtree alone would NOT raise: on a plain tmp dir the open scandir
        fd survives the unlink and reads every buffered entry to StopIteration
        (probe 2026-09-11). Only a real /proc readdir fails once /proc/<pid>
        vanishes, so the generator raises explicitly to reproduce that failure
        deterministically; the rmtree is kept as the counterfactual signal that
        the fixture (not the host /proc) was walked."""

        class _BombPath(_real):
            _flavour = _flav

            def iterdir(self):
                it = super().iterdir()
                fired = False
                def _gen():
                    nonlocal fired, bomb_fired
                    for ent in it:
                        yield ent
                        if not fired:
                            fired = True
                            bomb_fired = True
                            shutil.rmtree(fd, ignore_errors=True)
                            raise FileNotFoundError(f"{fd}")
                return _gen()

        return _BombPath(str(fd))

    def _redirect(p):
        s = str(p)
        if s == f"/proc/{123}/fd":
            return _bomb_path()
        if s.startswith("/proc/net/"):
            return _real(s.replace("/proc/", str(proc) + "/"))
        return _real(s)

    monkeypatch.setattr(sb, "Path", lambda p: _redirect(_real(p)))

    # MUTATION CHECK: with the guard's try narrowed to the readlink only -- the
    # PRE-FIX shape, where the lazy listing runs in the `for` loop OUTSIDE the
    # try -- the SAME fixture raises FileNotFoundError out of the walk. This is
    # what proves the guard (the whole walk inside one try) is load-bearing:
    # the rewritten test is RED on the pre-fix shape and GREEN only on the
    # fixed helper, so it is a real falsifier of the vanish-mid-read bug.
    def _mutant_sockets_pre_fix(pid):
        try:
            fds = sb.Path(f"/proc/{pid}/fd").iterdir()
        except OSError:
            return 0
        inodes = set()
        for fdes in fds:  # <- OUTSIDE the try: a vanished dir raises here
            target = str(fdes.readlink())
            if target.startswith("socket:[") and target.endswith("]"):
                inodes.add(target[len("socket:["):-1])
        return len(inodes)

    with pytest.raises(FileNotFoundError):
        _mutant_sockets_pre_fix(123)
    # THE BOMB RECORDED IT FIRED (L4.276): the redirect raised after yielding
    # the entry; a vacuous walk that never touched the fixture leaves this flag
    # False and fires red here.
    assert bomb_fired, \
        "the bomb never raised in the mutant walk: it did not touch the fixture"

    # the mutant consumed the fixture; rebuild it for the real helper
    fd.mkdir(parents=True)
    (fd / "3").symlink_to("socket:[111]")

    # THE EXISTS-BEFORE FALSIFIER (L4.276 build order): the fixture fd dir
    # must EXIST immediately before the real helper call. With the two rebuild
    # lines above commented out (the MUTATION), this assertion fires RED -- the
    # mutant consumed the only copy and nothing rebuilt it, so a walk over the
    # missing dir is the vacuous non-falsifier (missing dir -> trivially 0)
    # the round demoted. Comment those two lines and this test goes red HERE.
    bomb_fired = False   # re-arm: the REAL call must fire the bomb too, else
                         # it walked the host /proc, not this fixture
    assert fd.exists(), \
        "fixture fd dir absent before the real helper call: walk would be vacuous"

    # the fixed helper survives the vanish: the guarded walk collapses to the
    # documented 0, and no OSError escapes.
    assert sb._pid_sockets(123) == 0
    # the bomb fired (and was recorded) inside the real, guarded walk
    assert bomb_fired, "the real helper did not walk the fixture"
    # COUNTERFACTUAL: the fixture fd dir is gone after the walk. Had the walk
    # iterated the host's /proc instead of the fixture (the non-falsifier
    # shape), this dir would still exist.
    assert not fd.exists(), "the fixture survived the real walk: it was not consumed"


# --------------------------------------------------------------------------
# hypothesis:l4-spawn-budget-status-waits-for-the-parent — `status --iter
# --wait [--timeout S]` blocks until the round's PARENT lease is gone
# --------------------------------------------------------------------------

def test_wait_already_finished_round_exits_0_without_sleep(monkeypatch, root, capsys):
    """(a) FALSIFIER of the claim's no-sleep clause. A round whose parent
    lease is already gone but whose session dir exists is already-finished:
    `--wait` must return 0 on the FIRST read and MUST NOT sleep. The
    session dir is what separates already-finished (exit 0) from unknown
    (exit 3).

    `time.sleep` is monkeypatched to raise, so any wait that sleeps on an
    already-finished round fails red instead of just running slow."""
    _mk_project(root)
    sdir = root / ".agi" / "sessions" / "iter-L4.244"
    sdir.mkdir(parents=True)
    monkeypatch.setattr(
        spawn_budget.time, "sleep",
        lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("--wait slept on an already-finished round")))
    rc = spawn_budget.main(["--root", str(root), "status",
                            "--iter", "L4.244", "--wait"])
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "already finished" in out, out


def test_wait_parent_removed_returns_0_after_removal(root, capsys):
    """(b) A parent lease removed by a background thread 0.3 s in:
    `--wait --timeout 10` returns 0 after the removal with the final view
    printed. The wait is on the lease view, so the removal (whatever the kid
    does) is what unblocks it."""
    import threading
    _mk_project(root)
    parent = _sleeping()
    p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent",
                                   iter_n="L4.245")
    assert p_lease is not None
    spawn_budget.commit(p_lease, parent.pid)

    def _drop():
        time.sleep(0.3)
        p_lease.path.unlink(missing_ok=True)
    t = threading.Thread(target=_drop)
    t.start()
    try:
        t0 = time.monotonic()
        rc = spawn_budget.main(["--root", str(root), "status",
                                "--iter", "L4.245", "--wait", "--timeout", "10"])
        elapsed = time.monotonic() - t0
        out = capsys.readouterr().out
        assert rc == 0, out
        assert elapsed < 9, f"waited {elapsed:.2f}s; expected well under timeout 10"
        assert "parent done" in out, out
    finally:
        t.join(timeout=2)
        parent.kill(); parent.wait()


def test_wait_parent_never_goes_times_out_exit_2(root, capsys):
    """(c) A parent lease that never goes with `--timeout 1` exits 2, prints
    the last-seen view (the live parent row) to stdout AND `ERR: ... parent
    still live after Ns` to stderr, naming the round. The last-seen view is
    the clause the parent review found overclaimed (hypothesis
    `l4-spawn-budget-status-waits-for-the-parent`): the code went straight to
    the ERR print with no `_print_remaining_rows`."""
    _mk_project(root)
    parent = _sleeping()
    p_lease = spawn_budget.acquire(root, 2, "parent-0", tier="parent",
                                   iter_n="L4.246")
    assert p_lease is not None
    spawn_budget.commit(p_lease, parent.pid)
    try:
        rc = spawn_budget.main(["--root", str(root), "status",
                                "--iter", "L4.246", "--wait", "--timeout", "1"])
        cap = capsys.readouterr()
        out, err = cap.out, cap.err
        assert rc == 2, out
        # last-seen view: the still-live parent row is printed (stdout)
        assert "parent-0" in out, out
        assert "parent still live" in err, err
        assert "L4.246" in err, err
    finally:
        parent.kill(); parent.wait()


def test_wait_unknown_round_exit_3(root, capsys):
    """(d) An id with neither a lease nor a session dir -> exit 3 with
    `ERR: unknown round`."""
    _mk_project(root)
    rc = spawn_budget.main(["--root", str(root), "status",
                            "--iter", "L4.99997", "--wait"])
    err = capsys.readouterr().err
    assert rc == 3, err
    assert "unknown round" in err, err


def test_wait_without_iter_is_an_argparse_error(root, capsys):
    """(e) `--wait` without `--iter` is an argparse error, exit 2."""
    _mk_project(root)
    rc = spawn_budget.main(["--root", str(root), "status", "--wait"])
    err = capsys.readouterr().err
    assert rc == 2, err
    assert "--wait requires --iter" in err, err

