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
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

#: Fallback when neither `spawn.max_live` nor `spawn.parallel` is configured.
DEFAULT_MAX_LIVE = 1


def budget_dir(root: Path) -> Path:
    """Where leases live: one directory per project tree.

    Under `sessions/` because it is session scratch and already gitignored,
    and *not* under an iteration directory because the population being
    bounded spans iterations — a parent dispatched into iter-107 may spawn
    kids into iter-107 too, but nothing guarantees it.
    """
    return Path(root) / "sessions" / ".spawn-budget"


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
    """
    if pid <= 0:
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
    """
    root = Path(root)
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
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".lease.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(rec, fh)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def main(argv: list[str] | None = None) -> int:
    """`spawn_budget.py [--root R] status|sweep` — inspect the live population."""
    import argparse
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import locations  # noqa: E402

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("action", choices=["status", "sweep"], nargs="?", default="status")
    ap.add_argument("--root", default=".", help="Any path inside the project")
    args = ap.parse_args(argv)

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1
    cfg_path = locations.config_path(root)
    cfg = json.loads(cfg_path.read_text()) if cfg_path else {}
    cap = max_live(cfg)
    live = live_agents(root)
    print(f"budget: {len(live)}/{cap} live  dir={budget_dir(root)}")
    for rec in live:
        print(f"  {rec.get('agent_id')} tier={rec.get('tier')} "
              f"iter={rec.get('iter')} pid={rec.get('agent_pid') or rec.get('holder_pid')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
