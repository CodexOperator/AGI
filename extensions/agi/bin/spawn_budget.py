#!/usr/bin/env python3
"""spawn_budget.py — a concurrency bound that survives a tier (goal:g4.8 item 3).

`spawn.parallel` bounds how many slots ONE `dispatch.py` invocation opens. It
does not bound grandchildren: a parent spawned by dispatch runs dispatch again
to get its own kids, and that second invocation reads the same `parallel` and
opens a fresh, unbounded population. N parents at M kids each is N*M processes
against one working tree, and `experiment:a00-763e629b-5c04ad` measured exactly
that.

The bound therefore cannot live in a number each invocation reads for itself.
It has to live in **shared state every spawner mutates**, enforced at the one
place a process is actually created. That is this module: a lease directory
under the project root, one file per live agent, taken before `Popen` and
reclaimed by liveness rather than by cleanup.

Three properties, each of which the manifest race (`goal:s28`) taught:

- **The count is re-read under the lock, never cached.** An invocation's view
  of how many agents are live is stale the moment another spawner starts.
- **Reclamation is lazy and liveness-based.** No release path can leak a lease,
  because a lease is only ever *believed* while its holder is alive. A killed
  agent, a killed dispatcher, and a machine reboot all free their leases
  without anyone running a cleanup step.
- **Admission is non-blocking.** A refused slot is skipped and reported, never
  waited on. Waiting would deadlock the exact topology this bounds: parents
  holding every lease, each blocked on kids that can never be admitted.
"""
from __future__ import annotations

import errno
import fcntl
import json
import os
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

import locations  # NOQA: E402

#: THE ONE definition of a terminal agent status (hypothesis:l4-one-definition-
#: of-terminal). `done-unreported` is what the reaper writes when a round
#: landed and only the report was lost -- the most common ending for a
#: `--branch` parent, and behaviourally terminal. It used to be omitted and
#: `dispatch.py` and `heal.py` only survived the omission on a second guard
#: (`if status != "running": continue`). This lives here because every reader
#: already imports `spawn_budget` (`dispatch.py`, `cli.py`) or imports a module
#: that does (`heal.py` -> dispatch), and `spawn_budget` imports only
#: `locations`, so nothing can cycle. Every reader imports THIS set; none
#: re-declares it.
TERMINAL = {"done", "done-unreported", "pending", "hung-healed", "failed"}

#: Fallback when neither `spawn.max_live` nor `spawn.parallel` is configured.
DEFAULT_MAX_LIVE = 1

#: How long `status --iter` sleeps sampling CPU ticks before judging a round
#: stalled. The director's stall definition (8 s) — a module constant, not a
#: bare literal, so a test can read it and shrink it.
TICK_SAMPLE_SECONDS = 8

#: Overridable sample window for the tick measurement. Defaults to
#: TICK_SAMPLE_SECONDS; tests monkeypatch this down so the falsifier does not
#: sleep 8 real seconds against live processes.
_STATUS_SAMPLE_SECONDS = TICK_SAMPLE_SECONDS


def budget_dir(root: Path) -> Path:
    """Where leases live: one directory per MAIN checkout.

    Under `sessions/` because it is session scratch and already gitignored,
    and *not* under an iteration directory because the population being
    bounded spans iterations — a parent dispatched into iter-107 may spawn
    kids into iter-107 too, but nothing guarantees it.

    **Resolves to the main checkout, never a per-worktree dir
    (`hypothesis:l3w4-parent-branch-merge-up`).** A parent spawned with
    `--branch` runs in its own git worktree, so `root` here may be a worktree
    root; the budget must stay the ONE directory every spawner mutates, or
    the tree-wide bound silently splits per worktree. `git_common_root`
    answers that via `git rev-parse --git-common-dir`, identity when the
    caller is already in the main checkout (or outside any git repo).

    **Keeps the graph-dir segment (`hypothesis:l3-budget-dir-dropped-agi`).**
    Under G11 the graph root is `<repo>/.agi`, and `git_common_root` returns
    the repo root — naively joining `main/sessions` would DROP the `.agi`
    segment and write leases into a stray `<repo>/sessions/`. So the main
    checkout's graph root is re-derived (`find_project_root(main)`, the same
    re-root `send.py` and `rotate.py` use) and the budget lives under IT:
    `<repo>/.agi/sessions/.spawn-budget`, shared by every worktree. In the
    legacy layout the graph root IS the repo root, so this is the identity
    and the budget keeps resolving to `<repo>/sessions/.spawn-budget`.
    """
    graph = locations.find_project_root(root) or root
    main = locations.git_common_root(graph)
    main_graph = locations.find_project_root(main) if main else None
    base = main_graph or graph
    return base / locations.SESSIONS_DIR_NAME / ".spawn-budget"


def _pause_flag_path(root: Path) -> Path:
    """Where the pause flag lives — inside `budget_dir`, so it resolves to
    the same main-checkout directory every worktree-based caller already
    reaches for a lease (`hypothesis:l3-reaper-restarts-through-stop`). A
    worktree-scoped pause flag would be invisible from the main tree for
    exactly the reason a worktree-scoped seat-pin was invisible from it
    earlier the same day — reusing `budget_dir`'s anchor avoids a second
    instance of that bug rather than re-deriving the fix.
    """
    return budget_dir(root) / ".paused"


def is_paused(root: Path) -> dict | None:
    """The active pause record, or `None` if dispatch is not paused.

    Checked by `acquire()` (refuses every new spawn) and by dispatch.py's
    inline reaper (refuses to restart a dead agent) — the two chokepoints
    that together make an owner stop order a structural refusal instead of
    a broadcast every seat has to separately remember not to violate.
    Record shape: `{paused: True, reason: str, actor: str, paused_at: int}`.
    """
    try:
        rec = json.loads(_pause_flag_path(root).read_text())
    except (OSError, json.JSONDecodeError):
        return None
    return rec if rec.get("paused") else None


def pause(root: Path, reason: str = "", actor: str = "") -> None:
    """Set the pause flag. Every `acquire()` and every reaper restart is
    refused until `resume()` clears it."""
    path = _pause_flag_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(path, {
        "paused": True, "reason": reason, "actor": actor,
        "paused_at": int(time.time()),
    })


def resume(root: Path) -> dict | None:
    """Clear the pause flag. Returns the cleared record, or `None` if it
    was not set."""
    prev = is_paused(root)
    _pause_flag_path(root).unlink(missing_ok=True)
    return prev


def max_live(cfg: dict, default: int = DEFAULT_MAX_LIVE) -> int:
    """The declared bound. `spawn.max_live` wins; `spawn.parallel` is the floor.

    A project that set `spawn.parallel` and never heard of this module gets a
    bound equal to its own slot count, which is what it already believed it
    was running. That makes the bound a tightening for existing projects and
    never a surprise loosening.
    """
    spawn = cfg.get("spawn") or {}
    if "max_live" in spawn:
        return int(spawn["max_live"])
    if "parallel" in spawn:
        return int(spawn["parallel"])
    legacy = cfg.get("agent_dispatch") or {}
    return int(legacy.get("claude_max_parallel", default))


def parent_max_kids(cfg: dict, default: int = 4) -> int:
    """The per-dispatch kid ceiling a parent's brief must name
    (hypothesis:l3-parent-never-told-to-iterate).

    A parent that iterates AND fans out is the first thing in this system
    capable of multiplying agents without a human in the loop, so the
    multiplicative bound needs its own knob rather than being silently equal
    to max_live. `spawn.parent_max_kids` wins; otherwise the ceiling is a
    small constant, never the whole tree's capacity. The ceiling is
    advisory-in-brief -- a hard, visible number the parent plans around --
    not an admission lease: `max_live` leases still bound the LIVE population
    and ``unadmitted`` refusals are unchanged.
    """
    spawn = cfg.get("spawn") or {}
    if "parent_max_kids" in spawn:
        return int(spawn["parent_max_kids"])
    return int(default)


@dataclass
class Lease:
    """One admitted agent's claim on the budget."""

    path: Path
    agent_id: str
    holder_pid: int
    agent_pid: int | None = None
    #: Hash of the credential minted for this slot, if any (`goal:g1.11`).
    #: The hash, never the secret — see `attach_credential`.
    key_hash: str | None = None


@contextmanager
def _budget_lock(root: Path):
    """Exclusive lock over the whole budget directory.

    The lock file is separate from the lease files so that sweeping, counting
    and creating a lease are one atomic step. Holding it across those three is
    the point: a count taken outside the lock is a count that was true once.
    """
    d = budget_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    lock_path = d / ".lock"
    with open(lock_path, "w") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def _pid_alive(pid: int) -> bool:
    """Whether `pid` names a live process.

    `EPERM` counts as alive: the process exists and is owned by someone else,
    which is still a process holding resources against this tree. Treating it
    as dead would free a lease for a process that is very much running.

    A zombie (state `Z` in `/proc/<pid>/stat`) counts as dead
    (`hypothesis:l3-cc-adapter-zombie-lease`): a defunct child is gone \u2014 its
    code has exited and only its reaping by a parent is outstanding. Its pid
    still answers `os.kill(pid, 0)`, so signal-existence alone would hold a
    lease forever behind an unreaped child. The process-table state is what
    the lease is about, so that is what liveness reads.
    """
    if pid <= 0:
        return False
    try:
        stat = open(f"/proc/{pid}/stat")
    except OSError:
        # Not on Linux, or the pid raced out of the table between checks.
        # Fall back to signal-existence rather than guess wrong.
        pass
    else:
        with stat:
            try:
                # State is field 3, after `pid (comm)`; comm can contain
                # spaces/parens, so split from the right on `) `.
                state = stat.read().rsplit(") ", 1)[1].split()[0]
            except (IndexError, ValueError):
                state = "?"
        if state == "Z":
            return False
    try:
        os.kill(pid, 0)
    except OSError as exc:
        return exc.errno == errno.EPERM
    return True


def _lease_is_live(rec: dict) -> bool:
    """A lease is live while the process it stands for is.

    Two holders, in order. Once the child exists, the child's pid is what the
    lease is about. Before that, the dispatcher that reserved it holds it —
    which is what closes the window between reserving a slot and `Popen`
    returning a pid. A dispatcher that dies inside that window frees its own
    reservation without anyone noticing it was ever taken.
    """
    agent_pid = rec.get("agent_pid")
    if agent_pid:
        return _pid_alive(int(agent_pid))
    holder = rec.get("holder_pid")
    return _pid_alive(int(holder)) if holder else False


def _read_leases(root: Path) -> list[tuple[Path, dict]]:
    out: list[tuple[Path, dict]] = []
    d = budget_dir(root)
    if not d.exists():
        return out
    for p in sorted(d.glob("*.lease")):
        try:
            out.append((p, json.loads(p.read_text())))
        except (json.JSONDecodeError, OSError):
            # A half-written or unreadable lease is not evidence of a live
            # process. Drop it rather than letting one corrupt file wedge the
            # budget shut forever — the failure mode that would turn a safety
            # rail into an outage.
            out.append((p, {}))
    return out


def _sweep_locked(root: Path) -> tuple[list[dict], list[str]]:
    """Delete dead leases. Returns `(live, hashes_to_revoke)`.

    Caller holds the lock. The credential hashes of reclaimed leases are
    *returned* rather than revoked here, because revoking is a network call
    with a 30s timeout and doing it under this lock would block every other
    spawner in the tree behind one unreachable API (`goal:g1.11`).
    """
    live: list[dict] = []
    orphaned: list[str] = []
    for path, rec in _read_leases(root):
        if _lease_is_live(rec):
            live.append(rec)
        else:
            key_hash = rec.get("key_hash")
            if key_hash:
                orphaned.append(str(key_hash))
            path.unlink(missing_ok=True)
    return live, orphaned


def _revoke_all(root: Path, hashes: list[str]) -> None:
    """Revoke reclaimed credentials, outside the lock, never fatally.

    Import is local so `spawn_budget` keeps working — and keeps bounding — on
    a box with no provisioning key and no network. The TTL on every minted key
    is what makes a failure here survivable rather than a leak.
    """
    if not hashes:
        return
    try:
        import provisioning
    except Exception:
        return
    for key_hash in hashes:
        try:
            provisioning.revoke(key_hash, root)
        except Exception:
            pass


def live_iteration_ids(root: Path) -> set:
    """Iteration ids with at least one live lease, READ-ONLY -- no sweep, no
    revoke, no lock file.

    `live_agents` reclaims dead leases (an unlink under the lock), which is
    the right behaviour for a spawner but the wrong one for a reader that must
    itself touch nothing -- the session-complete migration's `--dry-run`
    proves it writes nothing, so its liveness signal has to be a read. A lease
    is live while the process it names is (per `_lease_is_live`); a lease that
    is mid-write here is, at worst, momentarily stale, which a migration gate
    tolerates (the iteration's agent records must be terminal too).
    """
    live: set = set()
    for _path, rec in _read_leases(root):
        if _lease_is_live(rec):
            it = rec.get("iter")
            if it is not None:
                live.add(it)
    return live


def live_agents(root: Path) -> list[dict]:
    """Live leases, after reclaiming dead ones. Takes the lock itself."""
    with _budget_lock(root):
        live, orphaned = _sweep_locked(root)
    _revoke_all(root, orphaned)
    return live


def live_count(root: Path) -> int:
    return len(live_agents(root))


def acquire(root: Path, cap: int, agent_id: str, tier: str = "kid",
            iter_n: int | None = None) -> Lease | None:
    """Reserve one slot, or return None if the tree is already at `cap`.

    Non-blocking on purpose — see the module docstring. A caller that is
    refused should skip that slot and say so, not wait.

    Refuses unconditionally while paused (`hypothesis:l3-reaper-restarts-
    through-stop`), before the cap is even consulted — an owner stop order
    means no new agent anywhere in the tree, not "no agent past the cap".
    """
    root = Path(root)
    paused = is_paused(root)
    if paused:
        reason = paused.get("reason") or "owner stop order"
        print(f"spawn_budget: refusing {agent_id} — dispatch paused "
              f"({reason}); spawn_budget.py resume to lift", file=sys.stderr)
        return None
    with _budget_lock(root):
        live, orphaned = _sweep_locked(root)
        if len(live) >= cap:
            admitted = None
        else:
            holder = os.getpid()
            rec = {
                "agent_id": agent_id,
                "tier": tier,
                "iter": iter_n,
                "holder_pid": holder,
                "agent_pid": None,
                "reserved_at": int(time.time()),
            }
            path = budget_dir(root) / f"{agent_id}.lease"
            _write_lease(path, rec)
            admitted = Lease(path=path, agent_id=agent_id, holder_pid=holder)
    # Outside the lock: a refused admission still pays back whatever the sweep
    # reclaimed, so a tree that filled up with dead agents cleans itself on the
    # very call that noticed.
    _revoke_all(root, orphaned)
    return admitted


def attach_credential(lease: Lease, key_hash: str) -> None:
    """Record which minted credential this lease owns (`goal:g1.11`).

    The lease is already the object whose liveness governs the slot, so it is
    the right place to hang the key: reclaiming the slot and revoking the key
    become one event rather than two that can disagree. **Only the hash is
    stored — never the secret.** The lease file is ordinary session scratch,
    and a credential written there would outlive the process it was issued for,
    which is the whole thing this feature removes.
    """
    lease.key_hash = key_hash
    try:
        rec = json.loads(lease.path.read_text())
    except (json.JSONDecodeError, OSError):
        rec = {"agent_id": lease.agent_id, "holder_pid": lease.holder_pid}
    rec["key_hash"] = key_hash
    _write_lease(lease.path, rec)


def attach_branch(lease: Lease, branch_ref: dict) -> None:
    """Record which branch/base/worktree this lease's agent runs on.

    `hypothesis:l3w4-parent-branch-merge-up`. A `--branch` spawn cuts its
    own git worktree off the SPAWNER's branch; the lease is the object whose
    liveness governs the slot, so it is the right place to hang the target of
    the eventual `season.py merge-up` — a lease that lingers past the agent
    still says where its branch belongs, and `merge-up --record <lease>` can
    climb it into the recorded base. `branch`/`base_branch`/`worktree` are
    recorded verbatim (never the secret, never a path that later proves
    wrong); the same tuple is also written to the agent record by dispatch.
    """
    try:
        rec = json.loads(lease.path.read_text())
    except (json.JSONDecodeError, OSError):
        rec = {"agent_id": lease.agent_id, "holder_pid": lease.holder_pid}
    for key in ("branch", "base_branch", "worktree"):
        if branch_ref.get(key):
            rec[key] = branch_ref[key]
    _write_lease(lease.path, rec)


def commit(lease: Lease, agent_pid: int) -> None:
    """Hand the lease over to the spawned process once it has a pid."""
    lease.agent_pid = int(agent_pid)
    try:
        rec = json.loads(lease.path.read_text())
    except (json.JSONDecodeError, OSError):
        rec = {"agent_id": lease.agent_id, "holder_pid": lease.holder_pid}
    rec["agent_pid"] = int(agent_pid)
    rec["spawned_at"] = int(time.time())
    _write_lease(lease.path, rec)


def release(lease: Lease) -> None:
    """Give a slot back explicitly, revoking its credential if it has one.

    Only needed when a reservation is abandoned without a process ever being
    started — a zoom failure, a config error, a raised adapter. Everything
    else is reclaimed by liveness, so this is an optimisation, never a
    correctness requirement. The credential is revoked here rather than left to
    the next sweep, because an abandoned slot's key was issued and never used,
    and that is the cheapest possible moment to take it back.
    """
    lease.path.unlink(missing_ok=True)
    if lease.key_hash:
        # budget_dir is <root>/sessions/.spawn-budget, so the project root is
        # two levels up from the lease file's directory.
        _revoke_all(lease.path.parent.parent.parent, [lease.key_hash])


def _write_lease(path: Path, rec: dict) -> None:
    """Write a lease atomically, so a reader never sees half of one."""
    _atomic_write_json(path, rec)


def _atomic_write_json(path: Path, rec: dict) -> None:
    """Write `rec` as JSON to `path` atomically (tmp file + rename), so a
    reader never sees a half-written file. Shared by lease writes and the
    pause flag — same requirement, same fix, one helper."""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".tmp.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(rec, fh)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _pid_ticks(pid: int) -> int:
    """CPU ticks (utime+stime) consumed by `pid`, or 0 if unreadable."""
    try:
        with open(f"/proc/{pid}/stat") as fh:
            # comm (field 2) can contain spaces/parens; fields after `) ` are
            # 1-indexed with utime=14, stime=15.
            parts = fh.read().rsplit(") ", 1)[1].split()
            return int(parts[12]) + int(parts[13])
    except (OSError, IndexError, ValueError):
        return 0


def _pid_sockets(pid: int) -> int:
    """Every socket inode held by `pid` — TCP in ANY state plus unix sockets.

    The old `_pid_established_sockets` counted only ESTABLISHED (state 01)
    TCP. A parent mid-review between two API calls holds a LISTEN/CLOSE port
    or a unix control socket and reads as `sockets=0` — a false
    STALL-CANDIDATE. This reads the pid's fd table for `socket:[inode]`
    targets, then intersects those inodes with the inode sets of
    /proc/net/tcp, /proc/net/tcp6 (any state) and /proc/net/unix. Count is
    len(intersection); 0 on any unreadable edge.

    inode column: index 9 in tcp/tcp6 (10th column), index 6 in unix (a
    trailing Path may contain spaces, so it is never `cols[-1]`).
    """
    try:
        fds = Path(f"/proc/{pid}/fd").iterdir()
    except OSError:
        return 0
    inodes = set()
    for fd in fds:
        try:
            target = str(fd.readlink())
        except OSError:
            continue
        if target.startswith("socket:[") and target.endswith("]"):
            inodes.add(target[len("socket:["):-1])
    if not inodes:
        return 0
    table = set()
    for path in ("/proc/net/tcp", "/proc/net/tcp6"):
        try:
            lines = Path(path).read_text().splitlines()[1:]
        except OSError:
            continue
        for line in lines:
            cols = line.split()
            # any TCP state counts, not just ESTABLISHED (01)
            if len(cols) >= 10 and cols[9].isdigit():
                table.add(cols[9])
    try:
        lines = Path("/proc/net/unix").read_text().splitlines()[1:]
    except OSError:
        lines = []
    for line in lines:
        cols = line.split()
        if len(cols) >= 7 and cols[6].isdigit():
            table.add(cols[6])
    return len(inodes & table)


def _iter_num(iter_str: str) -> int | None:
    """Normalise `--iter L4.140` or `--iter 140` to the int the lease stores."""
    s = iter_str.strip()
    if "." in s:
        s = s.rsplit(".", 1)[1]
    try:
        return int(s)
    except ValueError:
        return None


def _agent_status(root: Path, agent_id: str, iter_val, worktree=None) -> tuple[str, str | None]:
    """The agent.json `status` for this agent, if a record exists, plus which
    sessions root answered (`"main"`, `"seat:<name>"`, `"wt:<parent-id>"`, or
    None for none). The `worktree` hint is accepted for call-signature
    compatibility but is no longer authoritative: the search is a plain glob.

    `iter_val` is the lease's own `iter` field, which is the round's genuine
    id string (`L4.167`) — never `f"iter-L{int}"`. The real sessions dir is
    `iter-L4.167`, so building it from an int alone (`iter-L167`) misses every
    live round. `locations.iteration_dirname` turns the lease value into the
    exact dir name for both schemes: `L4.167` -> `iter-L4.167`, `140` ->
    `iter-140`.

    The record layout is NOT "the round's own worktree" (hypothesis:l4-spawn-
    budget-iter-reads-the-rounds-own-sessions-dir, measured 2026-09-11): a
    PARENT's agent.json is written by the DISPATCHER into the DISPATCHING
    tree's sessions dir — a seat worktree
    (`<main>/.agi/worktrees/seat-<name>/.agi/sessions`) or MAIN itself; a KID's
    agent.json is written by its PARENT into the PARENT's worktree
    (`<main>/.agi/worktrees/<parent-id>/.agi/sessions`). So the old probe of
    the agent's OWN `worktrees/<agent_id>` dir could never find a record — it
    holds the agent's KIDS, never itself — and every worktree-spawned row
    printed `(no agent.json)` while the record was live on disk.

    The lookup therefore searches `<iter dir>/<agent_id>/agent.json` under
    EVERY sessions root the tree can name, in order:
      1. the invoking root's own graph sessions dir,
      2. MAIN's graph sessions dir (`budget_dir(root).parent`, as before),
      3. every `<main>/.agi/worktrees/*/.agi/sessions` — ONE glob over the
         worktree dir (~150 siblings is cheap), sorted so the answer is
         deterministic.
    The label names the answering root: `"main"` for MAIN, `"seat:<name>"`
    for a worktree named `seat-<name>`, `"wt:<parent-id>"` for any other work
    worktree. `(no agent.json)` is returned only when NO root holds a record.
    """
    try:
        dirname = locations.iteration_dirname(iter_val)
    except ValueError:
        return "(no agent.json)", None

    graph = locations.find_project_root(root) or root
    main = locations.git_common_root(graph)
    main_graph = locations.find_project_root(main) if main else None

    def wt_label(wt_root: Path) -> str:
        """`seat-sanctuary-director` -> `seat:sanctuary-director`; any other
        worktree root (`a00-06c44930`) -> `wt:<parent-id>`."""
        name = wt_root.name
        if name.startswith("seat-"):
            return f"seat:{name[5:]}"
        return f"wt:{name}"

    # (graph dir, label) candidates in precedence order, deduplicated by path.
    cands: list[tuple[Path, str]] = []
    seen: set[Path] = set()

    own = graph
    if own not in seen:
        cands.append((own, "main" if own == main_graph else wt_label(own)))
        seen.add(own)
    if main_graph and main_graph not in seen:
        cands.append((main_graph, "main"))
        seen.add(main_graph)
    if main_graph:
        for wt in sorted(main_graph.glob("worktrees/*")):
            wt_graph = locations.find_project_root(wt) or wt
            # Never bleed upward: when a worktree root has no graph of its own,
            # `find_project_root` resolves an ANCESTOR's graph (the MAIN one)
            # and a main-tree record would get mislabeled as a worktree record.
            # Only accept a graph at or below the candidate worktree root.
            if not (wt_graph == wt or wt in wt_graph.parents):
                continue
            if wt_graph in seen:
                continue
            cands.append((wt_graph, wt_label(wt)))
            seen.add(wt_graph)

    for cand, src in cands:
        p = cand / locations.SESSIONS_DIR_NAME / dirname / agent_id / "agent.json"
        try:
            rec = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        return rec.get("status") or "(no status)", src
    return "(no agent.json)", None


def _round_status(root: Path, iter_str: str) -> int:
    """`status --iter NNN`: the whole round's live rows + one verdict line."""
    nnn = _iter_num(iter_str)
    if nnn is None:
        print(f"spawn_budget: unknown iteration {iter_str!r} "
              f"(expected L4.NNN or NNN)", file=sys.stderr)
        return 1
    rows = [rec for _, rec in _read_leases(root)
            if _lease_is_live(rec)
            and _iter_num(str(rec.get("iter"))) == nnn]
    if not rows:
        print(f"spawn_budget: no live agents in iteration L{nnn} "
              f"(dir={budget_dir(root)})", file=sys.stderr)
        return 1
    kids = 0
    total_ticks = 0
    total_socks = 0
    done = False
    # Sample EVERY row's starting tick count first, sleep the ONE shared
    # window, then re-read every row. Net wall time is one window regardless
    # of round size, yet every pid still sits under the full window. The
    # pre-fix loop slept INSIDE the per-row loop, so a 5-row round cost 5
    # windows — and `status --iter` is exactly the command the director runs
    # when a round may be stalled.
    pids = [int(rec.get("agent_pid") or rec.get("holder_pid") or 0)
            for rec in rows]
    t0s = [_pid_ticks(pid) for pid in pids]
    time.sleep(_STATUS_SAMPLE_SECONDS)
    deltas = [max(0, _pid_ticks(pid) - t0) for pid, t0 in zip(pids, t0s)]
    for rec, pid, ticks in zip(rows, pids, deltas):
        tier = rec.get("tier") or "?"
        started = int(rec.get("spawned_at") or rec.get("reserved_at") or time.time())
        elapsed = max(0, int(time.time()) - started)
        socks = _pid_sockets(pid)
        status, src = _agent_status(root, rec.get("agent_id", "?"),
                                    rec.get("iter"), rec.get("worktree"))
        total_ticks += ticks
        total_socks += socks
        if tier == "kid":
            kids += 1
        if status in TERMINAL:
            done = True
        # `@...` names the sessions root that answered: `@main`, `@seat:<name>`
        # for a seat worktree, `@wt:<parent-id>` for any other worktree
        # (hypothesis:l4-spawn-budget-iter-reads-the-rounds-own-sessions-dir).
        # Nothing when src is None — `(no agent.json)` already names that case.
        suffix = f"@{src}" if src else ""
        print(f"  {rec.get('agent_id')} tier={tier} pid={pid} "
              f"elapsed={elapsed}s ticks={ticks} sockets={socks} "
              f"agent={status}{suffix}")
    if kids >= 1:
        print(f"round L{nnn}: parent alive, {kids} live kid(s)")
        return 0
    # STALL-CANDIDATE only when EVERY signal says stalled: 0 ticks over the
    # sample, 0 sockets, 0 live kids, no terminal agent.json status. A parent
    # mid-review holds a socket or burns CPU and must not be called stalled.
    if total_ticks == 0 and total_socks == 0 and not done:
        print(f"STALL-CANDIDATE: parent alive, 0 live kids, 0 ticks, "
              f"0 sockets, no done")
        return 0
    print(f"round L{nnn}: parent alive, reviewing "
          f"(ticks={total_ticks}, sockets={total_socks})")
    return 0


def main(argv: list[str] | None = None) -> int:
    """`spawn_budget.py [--root R] status|sweep|pause|resume`.

    `status` (default) inspects the live population, `sweep` reclaims dead
    leases. `pause [--reason R] [--actor A]` refuses every new spawn and
    every reaper restart tree-wide until `resume` clears it — the
    structural form of an owner stop order
    (`hypothesis:l3-reaper-restarts-through-stop`).
    """
    import argparse
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import locations  # noqa: E402

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=["status", "sweep", "pause", "resume"],
                     nargs="?", default="status")
    ap.add_argument("--root", default=".", help="Any path inside the project")
    ap.add_argument("--reason", default="", help="with pause: why (recorded, shown on every refusal)")
    ap.add_argument("--actor", default="", help="with pause: who paused it")
    ap.add_argument("--iter", default="",
                    help="status: restrict to one iteration (L4.NNN or NNN) "
                         "and emit the round verdict")
    args = ap.parse_args(argv)

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    if args.action == "pause":
        pause(root, reason=args.reason, actor=args.actor)
        who = f" by {args.actor}" if args.actor else ""
        why = f": {args.reason}" if args.reason else ""
        print(f"paused{who}{why} — every acquire() and reaper restart "
              f"refuses until resume")
        return 0
    if args.action == "resume":
        prev = resume(root)
        if prev is None:
            print("not paused — nothing to resume")
        else:
            print(f"resumed (was paused since "
                  f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(prev.get('paused_at', 0)))}"
                  f"{': ' + prev['reason'] if prev.get('reason') else ''})")
        return 0

    cfg_path = locations.config_path(root)
    if args.iter:
        return _round_status(root, args.iter)

    cfg = json.loads(cfg_path.read_text()) if cfg_path else {}
    cap = max_live(cfg)
    live = live_agents(root)
    paused = is_paused(root)
    if paused:
        who = f" by {paused['actor']}" if paused.get("actor") else ""
        why = f": {paused['reason']}" if paused.get("reason") else ""
        print(f"🔴 PAUSED{who}{why} — acquire() and reaper restarts are "
              f"refused; `spawn_budget.py resume` to lift")
    print(f"budget: {len(live)}/{cap} live  dir={budget_dir(root)}")
    for rec in live:
        it = rec.get("iter")
        # hypothesis:l3-killed-agent-restarts-unattributed — a live lease with
        # no iteration is invisible to the round it belongs to, so it can hold
        # that round open forever (mirror of the workflow-spawn no-lease
        # defect: there the count was too low, here the attribution is
        # missing). Every spawner in the tree passes iter_n, so `None` here is
        # a defect, not a state — make it loud rather than a silent count.
        loud = ("   <-- UNATTRIBUTED: iter is None (restarted lease "
                "lost its round)\n" if it is None else "")
        print(f"  {rec.get('agent_id')} tier={rec.get('tier')} "
              f"iter={it} pid={rec.get('agent_pid') or rec.get('holder_pid')}{loud}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
