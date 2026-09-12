#!/usr/bin/env python3
"""mail_alert.py — one shared side-channel alert for unread agent mail.

hypothesis:l3w4-shared-mail-alert. A seat (agent) should never have to spend
a turn polling its own inboxes: the loop already visits a per-turn seam
(UserPromptSubmit), and this module is the logic a hook registered on that
seam calls. It unifies three unread surfaces under ONE mechanism
(constraint 5):

  * dm    — pairwise conversations under comms/dm/            (send.py rooms())
  * room  — standing quorum/director rooms under comms/room/ (send.py rooms())
  * inbox — the plain per-recipient inbox under sessions/inbox/ (send.py)

When anything is unread it returns a single system-reminder-tagged block
(distinguishable from the owner — constraint 3) naming the room/sender and
how long it has waited, and stamps an `alerted_at` record per seat+thread so
"never got it" and "ignored it" stay distinguishable failures (constraint 4).
It never spends a turn of the agent's own: it is invoked by the harness hook,
the agent does zero work (constraint 1), and if the seam is busy it simply
fires at the next one (constraint 2).

Reuses send.py read-only — no writes to its conversation files, no changes
to send.py needed.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))

import send  # noqa: E402  (reuse rooms(), _scan_messages, comms_root)

#: State lives under the comms root: `<comms>/mail-alert/alerts.json`, keyed
#: seat -> thread -> {count, alerted_at}.
STATE_SUBDIR = "mail-alert"
STATE_FILE = "alerts.json"

#: Marker line used by CC hooks so the injected context block is visually and
#: programmatically distinct from the owner's own words.
INJECT_TAG = "agi_mail_alert"


def _age_minutes(ts: str) -> int | None:
    """Whole minutes since the given ISO ts (UTC), else None if unparsable."""
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        return max(0, int((datetime.now(timezone.utc) - dt).total_seconds() // 60))
    except Exception:
        return None


def _last_meta(croot: Path, kind: str, name: str) -> tuple[str, int | None]:
    """(sender, age_minutes) of the most recent block in a dm/room/file."""
    if kind == "room":
        blocks = send._read_conv(send._room_path(croot, name))
    elif kind == "dm":
        blocks = send._read_conv(send._dm_path(croot, *name.split("--", 1)))
    else:
        return "", None
    if not blocks:
        return "", None
    last = blocks[-1]
    return last.get("from", ""), _age_minutes(last.get("ts", ""))


def _inbox_unread(root: Path, me: str) -> int:
    """Unread block count in the plain per-recipient inbox (sessions/inbox/).

    Reuses `send._inbox_path`, which resolves to the SHARED sessions dir, so
    mail a seat in a worktree sent is counted by the main checkout's alert
    and vice versa (the inbox is ONE room across worktrees)."""
    blocks, _ = send._scan_messages(send._inbox_path(root, me))
    return len(blocks)


def collect_unread(croot: Path, root: Path, me: str) -> list[dict]:
    """All unread mail for `me`, unified across dm, room and inbox.

    Each item: {kind, name, count, last_from, age_minutes}. Sorted so the
    oldest-waiting thread is named first (a tired seat reads the top line).
    """
    items: list[dict] = []
    for kind, name, count in send.rooms(croot, me):
        if count > 0:
            last_from, age = _last_meta(croot, kind, name)
            items.append({"kind": kind, "name": name, "count": count,
                          "last_from": last_from, "age_minutes": age})
    inbox_unread = _inbox_unread(root, me)
    if inbox_unread > 0:
        items.append({"kind": "inbox", "name": "inbox", "count": inbox_unread,
                      "last_from": "", "age_minutes": None})
    items.sort(key=lambda i: (
        -(i["age_minutes"] if i["age_minutes"] is not None else 10 ** 9)))
    return items


def _load_state(croot: Path) -> dict:
    p = croot / STATE_SUBDIR / STATE_FILE
    if p.is_file():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def _save_state(croot: Path, state: dict) -> None:
    d = croot / STATE_SUBDIR
    d.mkdir(parents=True, exist_ok=True)
    (d / STATE_FILE).write_text(json.dumps(state))


def _thread_id(item: dict) -> str:
    return f"{item['kind']}:{item['name']}"


def should_alert(prev: dict | None, count: int) -> bool:
    """Raise on first sight of an unread thread and whenever NEW mail lands;
    stay silent on an unchanged backlog so an ignored message doesn't nag on
    every turn (the alerted_at record still shows it was raised)."""
    if prev is None:
        return True
    return count > int(prev.get("count", 0))


def build_alert(root: Path, me: str,
                comms_override: str | None = None) -> str | None:
    """Return the injection block for `me`, or None when nothing needs mail.

    Also stamps the alerted_at record for every thread being alerted. Pure
    and side-effect-visible: safe for a hook to call every seam.
    """
    if not me:
        return None
    croot = send.comms_root(root, comms_override)
    items = collect_unread(croot, root, me)
    if not items:
        return None

    state = _load_state(croot)
    seat = state.setdefault(me, {})
    now = send._now()
    wanted: list[dict] = []
    for item in items:
        tid = _thread_id(item)
        if should_alert(seat.get(tid), item["count"]):
            wanted.append(item)
            seat[tid] = {"count": item["count"], "alerted_at": now}
    if not wanted:
        return None
    _save_state(croot, state)

    lines = [f"<{INJECT_TAG}>"]
    lines.append(f"<summary>Unread mail for {me} ({len(wanted)} "
                 f"thread{'s' if len(wanted) != 1 else ''}):</summary>")
    for item in wanted:
        where = f"{item['kind']} {item['name']}"
        by = f" from {item['last_from']}" if item["last_from"] else ""
        age = (f", waiting ~{item['age_minutes']} min"
               if item["age_minutes"] is not None else "")
        lines.append(f"- {where}: {item['count']} unread{by}{age}")
    lines.append(f"<raised_at>{now}</raised_at>")
    lines.append(f"</{INJECT_TAG}>")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="emit a mail alert for a seat")
    ap.add_argument("--seat", "--post", default="",
                    help="recipient id (default: AGI_AGENT_ID)")
    ap.add_argument("--comms-root", dest="comms_root", default=None,
                    help="override comms root (tests)")
    ap.add_argument("--root", default=None, help="project root (default: cwd)")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path.cwd().resolve()
    seat = args.seat or send._detect_sender(None)
    try:
        alert = build_alert(root, seat, args.comms_root)
    except Exception as exc:  # a hook must never crash the session
        print(f"<!-- {INJECT_TAG}: error {exc} -->", file=sys.stderr)
        return 0
    if alert:
        print(alert, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
