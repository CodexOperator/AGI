#!/usr/bin/env python3
"""send.py — one-verb comms between agents, roles, and councils.

Transport is an append-only inbox file per recipient under
`.agi/sessions/inbox/<recipient>.md`. Each message is one YAML-style block
with `ts`, `from`, `to`, and `text`.

Usage:
    send.py send <to> <text>      — append a message, print the inbox path
    send.py read <me>             — print unread blocks and mark them read
    send.py peek <me>             — print unread blocks without marking

Options:
    --from <sender>    override sender (default: AGI_AGENT_ID env or "unknown")

Design source: .agi/context/season-ladder-and-morals-brief.md §2 (Comms).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402


#: Subdirectory under sessions/ for per-recipient inbox files.
INBOX_DIR = "inbox"

#: Separator between messages in the inbox file.
MSG_SEP = "---\n"

#: Marker line placed after the last read message. Everything before this line
#: has been "read"; everything after is "unread".
READ_MARKER = "# read up to here\n"


def _project_root() -> Path:
    """Resolve the nearest enclosing agi project root."""
    root = locations.find_project_root(Path.cwd())
    if root is None:
        print("ERR: not inside an agi project", file=sys.stderr)
        sys.exit(1)
    return root


def _inbox_dir(root: Path) -> Path:
    """`<root>/sessions/inbox/` — where per-recipient inbox files live."""
    return root / "sessions" / INBOX_DIR


def _inbox_path(root: Path, recipient: str) -> Path:
    """The inbox file for one recipient."""
    return _inbox_dir(root) / f"{recipient}.md"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _detect_sender(from_flag: str | None) -> str:
    """Sender from --from flag, AGI_AGENT_ID env, or fallback."""
    if from_flag:
        return from_flag
    env = os.environ.get("AGI_AGENT_ID", "")
    if env:
        return env
    return "unknown"


# ── verbs ─────────────────────────────────────────────────────────────────


def send(root: Path, to: str, text: str, sender: str | None) -> None:
    """Append one message block to the recipient's inbox."""
    inbox = _inbox_path(root, to)
    inbox.parent.mkdir(parents=True, exist_ok=True)

    ts = _now()
    from_id = _detect_sender(sender)
    block = f"{MSG_SEP}ts: {ts}\nfrom: {from_id}\nto: {to}\n\n{text}\n"

    with open(inbox, "a") as f:
        f.write(block)

    print(inbox.resolve())


def _scan_messages(inbox: Path) -> tuple[list[str], int]:
    """Read an inbox file and return (unread_blocks, read_marker_line).

    The read marker (`# read up to here`) divides read from unread.
    Everything before the marker (exclusive) is read; everything after is
    unread. Lines before the first block separator are the header and are
    counted as read.
    """
    if not inbox.is_file():
        return [], 0

    text = inbox.read_text()
    lines = text.splitlines(keepends=True)
    marker_index = -1
    for i, line in enumerate(lines):
        if line == READ_MARKER:
            marker_index = i
            break

    # Everything after the marker (or the whole file if no marker) is unread.
    if marker_index >= 0:
        unread_text = "".join(lines[marker_index + 1:])
    else:
        unread_text = text

    # Split into blocks by the message separator.
    blocks = [b for b in unread_text.split(MSG_SEP) if b.strip()]
    return blocks, marker_index


def read(root: Path, me: str, sender: str | None) -> None:
    """Print unread blocks and mark them read."""
    inbox = _inbox_path(root, me)
    blocks, marker_index = _scan_messages(inbox)

    if not blocks:
        print(f"inbox for {me}: empty")
        return

    # Print blocks.
    for i, block in enumerate(blocks):
        if i > 0:
            print(MSG_SEP, end="")
        print(block, end="")

    # Mark read: find the current last line and add a marker after it.
    # If marker already existed, move it past the blocks we just printed.
    if inbox.is_file():
        text = inbox.read_text()
        lines = text.splitlines(keepends=True)
        if marker_index >= 0:
            # Remove old marker; re-insert at end.
            lines = [l for l in lines if l != READ_MARKER]
        # Strip trailing whitespace, then add marker + trailing newline.
        content = "".join(lines).rstrip("\n")
        inbox.write_text(content + "\n" + READ_MARKER)


def peek(root: Path, me: str) -> None:
    """Print unread blocks without marking them read."""
    inbox = _inbox_path(root, me)
    blocks, _ = _scan_messages(inbox)

    if not blocks:
        print(f"inbox for {me}: empty")
        return

    for i, block in enumerate(blocks):
        if i > 0:
            print(MSG_SEP, end="")
        print(block, end="")


# ── CLI ────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="one-verb agent comms")
    ap.add_argument("verb", choices=["send", "read", "peek"],
                    help="send a message, read (and mark read), or peek (no mark)")
    ap.add_argument("target", help="recipient (send) or self (read/peek)")
    ap.add_argument("text", nargs="*", help="message text (send only)")
    ap.add_argument("--from", dest="from_id", default=None,
                    help="override sender id (default: AGI_AGENT_ID or unknown)")
    args = ap.parse_args(argv)

    root = _project_root()

    if args.verb == "send":
        text = " ".join(args.text) if args.text else ""
        if not text:
            print("ERR: message text is required for send", file=sys.stderr)
            return 1
        send(root, args.target, text, args.from_id)
        return 0

    if args.verb == "read":
        read(root, args.target, args.from_id)
        return 0

    if args.verb == "peek":
        peek(root, args.target)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())