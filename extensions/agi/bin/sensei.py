#!/usr/bin/env python3
"""sensei.py — the Master Sensei of the seat system (hypothesis:l3w4-master-sensei).

A training/tuning role. It keeps track of where agents fail, proposes a
harness/seat change to the failing role and its direct supervisor, and
applies it once both have replied after the proposal timestamp. It never
touches Belam or his advisors (tier-3 parents) without explicit owner
approval; for those it drafts a file and dms the liaison instead.

Two axes, deliberately non-circular: sanctuary-master rotates every Master
including the Sensei; the Sensei improves every Master including
sanctuary-master (safe because sanctuary-master's own `rotated_by` is
`quorum`, not the Sensei).

Usage (all read config:seats from the nearest graph root):

    sensei.py pick_worst --ledger PATH          # pure: worst row(s)
    sensei.py propose --target SEAT --change TX # dm seat + supervisor
    sensei.py   apply --target SEAT --node-id N --change TX --since TS \\
                      [--supervisor SEAT] [--owner-approved] [--dry-run]

The `ts` a `propose` prints is the `--since` handle for a matching `apply`.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

try:  # runs from extensions/agi/bin/ as part of the package
    from . import locations, node_writer, send as _send
except ImportError:  # runs as a plain script from a checkout
    import locations  # type: ignore
    import node_writer  # type: ignore
    import send as _send  # type: ignore

SENSEI = "master-sensei"
ROOM_QUORUM = "tier3-quorum"  # the one room that reaches the prime's seat
LIAISON = "liaison"
DRAFTS_DIR = "sessions/sensei/drafts"  # relative to the GRAPH root (.agi/), like .agi/sessions/
MSG_PREFIX = "[sensei #propose] "

# Roles the Sensei may never change on its own authority. Belam is the
# prime; the advisors are the tier-3 parents embodying the visions. Both need
# the owner's explicit `--owner-approved` flag (owner 9).
PROTECTED_ROLES = {"prime_director", "parent"}


# ── seats loading ────────────────────────────────────────────────────────


def load_seats(root: Path) -> list[dict]:
    """Parse the `seats:` list out of config:seats's frontmatter.

    Uses node_writer.find_node_file so the row file is located exactly the
    way every other reader locates it, then a minimal YAML list parse (the
    seats schema is flat JSON objects on lines, so a document split of the
    `seats:` block is enough).
    """
    nf = node_writer.find_node_file(root, "config:seats")
    if nf is None:
        return []
    text = nf.read_text(encoding="utf-8")
    fm = text.split("---", 2)[1] if text.startswith("---") else ""
    in_seats = False
    rows: list[dict] = []
    for line in fm.splitlines():
        if line.strip().startswith("seats:"):
            in_seats = True
            continue
        if in_seats:
            if line.strip().startswith("-"):
                import json as _json

                payload = line.strip()[1:].strip()
                try:
                    rows.append(_json.loads(payload))
                except Exception:
                    continue
            elif line.strip() and not line.startswith((" ", "-")):
                break  # next frontmatter key
        elif line.strip().startswith(("locations:", "edited_by:", "thought")):
            pass
    return rows


def seat_row(rows: list[dict], name: str) -> dict | None:
    for r in rows:
        if (r.get("name") or "").strip() == name:
            return r
    return None


# ── supervisor resolution ────────────────────────────────────────────────


def _direct_supervisor(row: dict) -> tuple[str, str] | None:
    """Which thread the seat's direct supervisor lives on.

    `rotated_by in {quorum, advisor, prime}` reaches the prime's seat through
    the one room (owner 4: no seat but the quorum reaches Belam) — returns
    `("room", "tier3-quorum")`. Any other named `rotated_by` is a dm to that
    seat — `("dm", <name>)`. No `rotated_by` means no supervisor thread.
    """
    rotated_by = (row.get("rotated_by") or "").strip()
    if rotated_by in ("quorum", "advisor", "prime"):
        return ("room", ROOM_QUORUM)
    if rotated_by:
        return ("dm", rotated_by)
    return None


def _required_threads(row: dict | None, target: str,
                      supervisor_flag: str | None) -> list[tuple[str, str]]:
    """The threads that must show a reply before an apply proceeds.

    A seat row contributes its own dm plus its supervisor thread; an
    ephemeral target (no row in config:seats) contributes only the supervisor
    thread, which must come from `--supervisor` (there is no role dm to ping).
    """
    if row is None:
        if not supervisor_flag:
            raise ValueError(
                f"ephemeral target {target!r} has no seat row; "
                f"--supervisor SEAT is required")
        return [("dm", supervisor_flag)]
    threads: list[tuple[str, str]] = [("dm", target)]
    sup = _direct_supervisor(row)
    if sup is not None:
        threads.append(sup)
    return threads


# ── pick_worst ───────────────────────────────────────────────────────────


def pick_worst(rows: list[dict]) -> dict | None:
    """The worst `(seat_or_role, model)` group from the failure ledger.

    Pure. Each input row is a ledger row with `seat_or_role`, `model`,
    `fail_rate` and `failed` keys. Groups by `(seat_or_role, model)`; the
    worst fail rate wins; ties break by higher failure count, then by seat
    name for a stable answer. Returns one representative row, or None for no
    rows.
    """
    best: dict | None = None
    for r in rows:
        rate = r.get("fail_rate", 0.0) or 0.0
        if best is None:
            best = dict(r)
            continue
        if rate > (best.get("fail_rate", 0.0) or 0.0):
            best = dict(r)
        elif rate == (best.get("fail_rate", 0.0) or 0.0):
            b_count = best.get("failed", 0) or 0
            if (r.get("failed", 0) or 0) > b_count:
                best = dict(r)
            elif (r.get("failed", 0) or 0) == b_count:
                if (r.get("seat_or_role", "") or "") < (
                        best.get("seat_or_role", "") or ""):
                    best = dict(r)
    return best


# ── reply checking / timestamps ──────────────────────────────────────────


def _normts(ts: str) -> str:
    ts = (ts or "").strip()
    return ts.replace("Z", "+00:00") if ts.endswith(("Z", "z")) else ts


def _after(block_ts: str, since: str) -> bool:
    """True when block_ts is strictly after `since`. Both ISO; lexicographic
    compare after a Z→+00:00 normalisation keeps pure-UTC stamps aligned."""
    return bool(_normts(block_ts) > _normts(since))


def _has_reply(croot: Path, thread: tuple[str, str], since: str, *,
               me: str = SENSEI) -> bool:
    """A block after `since` sent by someone other than the Sensei himself."""
    kind, name = thread
    if kind == "room":
        path = _send._room_path(croot, name)
    else:
        a, b, _ = _send._dm_pair(me, name)
        path = _send._dm_path(croot, me, name)
    for b in _send._read_conv(path):
        if not _after(b.get("ts", ""), since):
            continue
        sender = (b.get("from") or "").strip()
        if sender not in ("", me):
            return True
    return False


# ── apply_note (the one place write.py can be reached from) ──────────────


def apply_note(root: Path, node_id: str, change: str) -> str:
    """`write.py <node> "note SENSEI: <change>"` — the exact once-only write."""
    proc = subprocess.run(
        [sys.executable, str(Path(__file__).resolve().parent / "write.py"),
         node_id, f"note SENSEI: {change}", "--root", str(root)],
        capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(
            f"write.py failed ({proc.returncode}): "
            f"{proc.stderr.strip() or proc.stdout.strip()}")
    return (proc.stdout.strip() or proc.stderr.strip())


# ── subcommand bodies ────────────────────────────────────────────────────


def cmd_propose(root: Path, croot: Path, args) -> int:
    rows = load_seats(root)
    row = seat_row(rows, args.target)
    if args.change is None or not args.change.strip():
        print("ERR: --change TEXT is required", file=sys.stderr)
        return 2
    if row is None and not args.supervisor:
        print(f"ERR: no seat row for {args.target!r} and no --supervisor "
              f"given; nothing to propose against", file=sys.stderr)
        return 2
    threads = _required_threads(row, args.target, args.supervisor)
    text = f"{MSG_PREFIX}{args.change.strip()}"
    import datetime as _dt
    ts = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for kind, name in threads:
        if kind == "room":
            _send.send_room(croot, name, text, SENSEI)
        else:
            _send.send_dm(croot, SENSEI, name, text, SENSEI)
        print(f"  proposed -> {kind} {name}")
    print(ts)
    return 0


def cmd_apply(root: Path, croot: Path, args) -> int:
    rows = load_seats(root)
    row = seat_row(rows, args.target)
    if row is None and not args.supervisor:
        print(f"ERR: no seat row for {args.target!r} and no --supervisor "
              f"given", file=sys.stderr)
        return 2
    if row is None and not args.node_id:
        print("ERR: ephemeral apply needs --node-id to write its note into",
              file=sys.stderr)
        return 2
    if not args.since:
        print("ERR: --since TS is required (the ts a propose printed)",
              file=sys.stderr)
        return 2
    if args.change is None or not args.change.strip():
        print("ERR: --change TEXT is required", file=sys.stderr)
        return 2

    threads = _required_threads(row, args.target, args.supervisor)
    missing = [f"{k}:{n}" for k, n in threads
               if not _has_reply(croot, (k, n), args.since)]
    if missing:
        print("REFUSED: no reply after since on: " + ", ".join(missing),
              file=sys.stderr)
        return 3

    protected = row is not None and (
        (row.get("role") or "").strip() in PROTECTED_ROLES
        or int(row.get("tier", 0) or 0) >= 3)
    if protected and not args.owner_approved:
        return _draft_for_owner(root, croot, args, threads)
    node_id = args.node_id or (row.get("owning_goal") or "") or args.target
    if args.dry_run:
        print(f"[dry-run] write.py {node_id} 'note SENSEI: {args.change}'")
        return 0
    out = apply_note(root, node_id, args.change)
    print(f"APPLIED: {node_id} <- SENSEI note")
    for ln in out.splitlines():
        print(f"  {ln}")
    return 0


def _draft_for_owner(root: Path, croot: Path, args,
                     threads: list[tuple[str, str]]) -> int:
    """Protected target without --owner-approved: draft a file, dm liaison."""
    drafts = Path(root) / DRAFTS_DIR
    drafts.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in args.target)
    path = drafts / f"{safe}.md"
    body = (f"# sensei draft — {args.target}\n\n"
            f"change: {args.change}\n"
            f"since:  {args.since}\n"
            f"threads: {', '.join(f'{k}:{n}' for k, n in threads)}\n"
            f"status: awaiting-owner-approval\n")
    path.write_text(body, encoding="utf-8")
    _send.send_dm(croot, SENSEI, LIAISON,
                  f"[sensei #draft] {args.target}: {args.change} (see {path})",
                  SENSEI)
    print(f"DRAFTED: {path}")
    print(f"DM → liaison (owner approval required: rerun with --owner-approved)")
    return 0


# ── CLI ──────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    root = locations.find_project_root(Path.cwd().resolve())
    if root is None:
        print("ERR: not inside an agi project", file=sys.stderr)
        return 1
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(root),
                    help="any path inside the project (default cwd)")
    ap.add_argument("--dry-run", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pick_worst", help="worst ledger row(s)")
    p.add_argument("--ledger", default=None,
                   help="path to the failure-ledger rows file")
    p.add_argument("--rows", default=None, nargs="*",
                   help="inline JSON rows (for tests / tooling)")

    p = sub.add_parser("propose", help="ping a seat + its supervisor")
    p.add_argument("--target", required=True)
    p.add_argument("--change", default=None)
    p.add_argument("--supervisor", default=None)

    p = sub.add_parser("apply", help="apply once both threads reply")
    p.add_argument("--target", required=True)
    p.add_argument("--node-id", default=None,
                   help="build node to write the SENSEI note into")
    p.add_argument("--change", default=None)
    p.add_argument("--since", default=None)
    p.add_argument("--supervisor", default=None)
    p.add_argument("--owner-approved", action="store_true")

    args = ap.parse_args(argv)
    root = locations.find_project_root(Path(args.root).resolve()) or root
    croot = _send.comms_root(root)

    if args.cmd == "pick_worst":
        rows: list[dict] = []
        import json as _json
        for s in (args.rows or []):
            try:
                rows.append(_json.loads(s))
            except Exception:
                continue
        if args.ledger and Path(args.ledger).is_file():
            with open(args.ledger, encoding="utf-8") as f:
                rows = [_json.loads(ln) for ln in f if ln.strip()]
        worst = pick_worst(rows)
        if worst is None:
            print("no rows; nothing to pick")
            return 0
        print(_json.dumps(worst, sort_keys=True))
        return 0
    if args.cmd == "propose":
        return cmd_propose(root, croot, args)
    if args.cmd == "apply":
        return cmd_apply(root, croot, args)
    return 2


if __name__ == "__main__":
    sys.exit(main())