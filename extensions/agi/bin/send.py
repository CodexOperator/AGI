#!/usr/bin/env python3
"""send.py — one-verb comms between agents, roles, and councils.

Transport is an append-only inbox file per recipient under
`.agi/sessions/inbox/<recipient>.md`. Each message is one YAML-style block
with `ts`, `from`, `to`, and `text`.

Usage:
    send.py send <to> <text>      — append a message, print the inbox path
    send.py read <me>             — print unread blocks and mark them read
    send.py peek <me>             — print unread blocks without marking

Rooms (hypothesis:l3w0-send-rooms) — conversations as files under
`sessions/<iter>/comms/`, rendered back as a chat transcript:

    send.py send --to X TEXT        — pairwise dm (comms/dm/<a>--<b>.md, sorted)
    send.py send --room R TEXT      — quorum message (comms/room/<name>.md)
    send.py read --room R [--since TS] — transcript; mark read
    send.py read --dm X             — dm transcript; mark read
    send.py peek --room R / --dm X  — transcript; do not mark read
    send.py rooms [--me X]          — list rooms/dm with unread counts
    send.py audience prime --reason TEXT [--morals] — the only way to reach prime

The room verbs keep the same append-only block shape as the inbox, so reading
a room prints **sender** HH:MM — text, like a chat channel to a model. A room
may never address the prime (the prime is inbox-only); the `audience` verb is
the gated path in. The comms root defaults to `<graph_root>/comms/season-<N>/`
(season read from the ladder node) and honours `locations.comms_root` in the
project config so a project may point it at tmpfs. `read --all` (and
`peek --all`) render the whole transcript without advancing the cursor.

Options:
    --from <sender>    override sender (default: AGI_AGENT_ID, then --from,
                       then "unknown"; a seat/tmux window name is never
                       used as an identity)
    --comms-root <dir> override the comms root (else config, else default)

Design source: .agi/context/l3-command-ladder-brief.md §2.3 (Comms).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import spawn_gate  # noqa: E402


#: Subdirectory under sessions/ for per-recipient inbox files.
INBOX_DIR = "inbox"

#: Separator between messages in the inbox file.
MSG_SEP = "---\n"

#: Marker line placed after the last read message. Everything before this line
#: has been "read"; everything after is "unread".
READ_MARKER = "# read up to here\n"

#: Comms root defaults to `<graph_root>/comms/season-<N>/`; config key override.
COMMS_SUBDIR = "comms"
SEASON_DIR_PREFIX = "season-"
#: Directory of graph nodes inside the graph root (holds .geometry/ladder.md).
NODES_DIR = "nodes"

#: Standing rooms — one free-horizontal-comms channel per ladder level. A room
#: may never address the prime.
STANDING_ROOMS = (
    "tier3-quorum",     # the prime's parents, always open
    "tier2-directors",
    "tier2-parents",
    "tier1-directors",
    "tier1-parents",
    "tier0-parents",
)

#: The prime director is inbox-only; rooms may not address it.
PRIME = "prime"

#: Sidecar suffix for per-participant read positions (JSON, participant -> ts).
STATE_SUFFIX = ".state.json"


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
    """Sender: AGI_AGENT_ID env, then the --from flag, then "unknown".

    The agent's own id (AGI_AGENT_ID, exported by dispatch) signs a message
    even when the caller forgot a flag; an explicit --from beats the
    fallback (hypothesis:l3-send-comms-root). No seat/terminal name is
    ever used as an identity: a tmux window name is a seat, not an agent,
    and signing one was exactly the false-identity hazard this became
    (hypothesis:l3-agent-id-never-exported). When no id and no flag are
    present the message is signed "unknown" — an honest absence, not a
    confident wrong name.
    """
    env = os.environ.get("AGI_AGENT_ID", "").strip()
    if env:
        return env
    if from_flag:
        return from_flag
    return "unknown"


# ── comms root ─────────────────────────────────────────────────────────────


def _default_comms_root(root: Path) -> Path:
    """`<graph_root>/comms/season-<N>/` — a declared, season-level root whose
    path does not change when a new iteration dir is minted.

    Season from the ladder node's `current_season`, failing open to 1 (a
    missing ladder must never scatter comms). Never the newest iteration dir: a
    per-iteration root would RESET the standing rooms on every loop.
    """
    graph = locations.find_project_root(root) or root
    season = 1
    try:
        s = spawn_gate.read_ladder_season(graph / NODES_DIR)
        if s is not None:
            season = s
    except Exception:
        pass
    return graph / COMMS_SUBDIR / f"{SEASON_DIR_PREFIX}{season}"


def comms_root(root: Path, override: str | None = None) -> Path:
    """The comms root: --comms-root flag > config `locations.comms_root` >
    default `sessions/<iter>/comms`. Config is read from the nearest graph
    root (.agi/); a config value absolute is used as-is, relative resolved
    against the graph root, so a project may point it at tmpfs."""
    if override:
        p = Path(override).expanduser()
        return p.resolve() if p.is_absolute() else (root / p).resolve()
    graph = locations.find_project_root(root) or root
    cfg = locations.load_config(graph)
    declared = (cfg.get("locations") or {}).get("comms_root")
    if isinstance(declared, str) and declared.strip():
        p = Path(declared.strip()).expanduser()
        return p.resolve() if p.is_absolute() else (graph / p).resolve()
    return _default_comms_root(root)


def _dm_pair(a: str, b: str) -> tuple[str, str, str]:
    """(a, b) sorted by code point; filename `<a>--<b>.md`; id string."""
    a, b = sorted((a, b))
    return a, b, f"{a}--{b}"


def _room_path(croot: Path, room: str) -> Path:
    return croot / "room" / f"{room}.md"


def _dm_path(croot: Path, a: str, b: str) -> Path:
    _, _, name = _dm_pair(a, b)
    return croot / "dm" / f"{name}.md"


def _block(ts: str, from_id: str, to: str, text: str) -> str:
    return f"{MSG_SEP}ts: {ts}\nfrom: {from_id}\nto: {to}\n\n{text}\n"


def _parse_blocks(text: str) -> list[dict]:
    """Parse an append-only conversation file into a list of message dicts.

    Each block: header lines (`ts:`, `from:`, `to:`) then a blank line then the
    free-text body. Returns [{ts, from, to, text}] in file order.
    """
    out: list[dict] = []
    for b in text.split(MSG_SEP):
        b = b.strip().lstrip("#").strip()
        if not b:
            continue
        lines = b.splitlines()
        meta: dict[str, str] = {}
        body_lines: list[str] = []
        in_body = False
        for ln in lines:
            stripped = ln.strip()
            if not in_body and stripped and ":" in stripped and not ln.startswith(" "):
                key, _, val = stripped.partition(":")
                meta[key.strip()] = val.strip()
            else:
                in_body = True
                body_lines.append(ln)
        meta["text"] = "\n".join(body_lines).strip()
        if "ts" in meta:
            out.append({"ts": meta.get("ts", ""),
                        "from": meta.get("from", ""),
                        "to": meta.get("to", ""),
                        "text": meta.get("text", "")})
    return out


def _read_conv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return _parse_blocks(path.read_text())


def render_transcript(blocks: list[dict]) -> list[str]:
    """Render messages as a chat transcript: `**sender** HH:MM — text`."""
    lines: list[str] = []
    for b in blocks:
        sender = b.get("from", "?")
        text = b.get("text", "")
        hhmm = "??:??"
        try:
            ts = b.get("ts", "")
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            hhmm = dt.astimezone().strftime("%H:%M")
        except Exception:
            pass
        lines.append(f"**{sender}** {hhmm} — {text}")
    return lines


def _load_state(path: Path) -> dict:
    sp = Path(str(path) + STATE_SUFFIX)
    if sp.is_file():
        try:
            return json.loads(sp.read_text())
        except Exception:
            return {}
    return {}


def _save_state(path: Path, state: dict) -> None:
    Path(str(path) + STATE_SUFFIX).write_text(json.dumps(state))


def _past(blocks: list[dict], since: str | None, read_count: int,
          participant: str, path: Path, commit: bool,
          all_: bool = False) -> list[dict]:
    """Blocks to show.

    With `all_`: the whole transcript, and the cursor is never advanced even
    when `commit` is true (read --all). With an explicit `since` ts: every
    block at/after it. Otherwise: the blocks after the participant's stored
    read position (a message *count*, so it is exact even when two messages
    share a microsecond). If `commit`, the read position advances to the end
    of what was shown.
    """
    shown: list[dict]
    if all_:
        shown = list(blocks)
        commit = False
    elif since is not None:
        shown = [b for b in blocks if _after_or_eq(b["ts"], since)]
    else:
        shown = blocks[read_count:]
    if commit and shown:
        state = _load_state(path)
        end_index = len(blocks)
        state[participant] = end_index
        _save_state(path, state)
    return shown


def _after_or_eq(a: str, b: str) -> bool:
    """ISO strings compare lexicographically when normalized to UTC `Z`."""
    try:
        return _norm(a) >= _norm(b)
    except Exception:
        return a >= b


def _norm(ts: str) -> str:
    if ts.endswith("Z"):
        return ts
    # normalize offset forms to UTC with Z for consistent comparison
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    except Exception:
        return ts


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


# ── rooms (hypothesis:l3w0-send-rooms) ────────────────────────────────────


def send_dm(croot: Path, me: str, other: str, text: str,
            sender: str | None) -> Path:
    """Append a message to the pairwise dm file `<a>--<b>.md`, names sorted."""
    a, b, _ = _dm_pair(me, other)
    path = _dm_path(croot, me, other)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(_block(_now(), _detect_sender(sender), other, text))
    return path


def send_room(croot: Path, room: str, text: str, sender: str | None) -> Path:
    """Append a message to a room. A room may never address the prime."""
    if room == PRIME or room.startswith(PRIME + "-"):
        print(f"ERR: {room!r} may not address the prime — the prime is "
              f"inbox-only; use `audience prime` instead", file=sys.stderr)
        raise SystemExit(1)
    path = _room_path(croot, room)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(_block(_now(), _detect_sender(sender), room, text))
    return path


def _conv_blocks(path: Path) -> list[dict]:
    return _read_conv(path)


def read_dm(croot: Path, me: str, other: str, since: str | None,
            sender: str | None, all_: bool = False) -> list[str]:
    """Render a dm transcript after `since` (or the reader's read position),
    and mark the latest shown message read. `all_` shows the whole transcript
    without advancing the cursor."""
    path = _dm_path(croot, me, other)
    blocks = _conv_blocks(path)
    state = _load_state(path)
    shown = _past(blocks, since, state.get(me, 0), me, path, commit=True,
                  all_=all_)
    return render_transcript(shown)


def peek_dm(croot: Path, me: str, other: str, since: str | None,
            all_: bool = False) -> list[str]:
    path = _dm_path(croot, me, other)
    blocks = _conv_blocks(path)
    state = _load_state(path)
    shown = _past(blocks, since, state.get(me, 0), me, path, commit=False,
                  all_=all_)
    return render_transcript(shown)


def read_room(croot: Path, room: str, participant: str, since: str | None,
              sender: str | None, all_: bool = False) -> list[str]:
    path = _room_path(croot, room)
    blocks = _conv_blocks(path)
    state = _load_state(path)
    shown = _past(blocks, since, state.get(participant, 0), participant, path,
                  commit=True, all_=all_)
    return render_transcript(shown)


def peek_room(croot: Path, room: str, participant: str, since: str | None,
              all_: bool = False) -> list[str]:
    path = _room_path(croot, room)
    blocks = _conv_blocks(path)
    state = _load_state(path)
    shown = _past(blocks, since, state.get(participant, 0), participant, path,
                  commit=False, all_=all_)
    return render_transcript(shown)


def rooms(croot: Path, me: str) -> list[tuple[str, str, int]]:
    """List (kind, name, unread_count) for every room and every dm `me` is in.

    Unread = messages after `me`'s stored read position in that conversation.
    Standing rooms a participant has never written/read are listed with 0
    only if they exist on disk."""
    out: list[tuple[str, str, int]] = []

    room_dir = croot / "room"
    if room_dir.is_dir():
        for f in sorted(room_dir.glob("*.md")):
            name = f.stem
            blocks = _conv_blocks(f)
            count = int(_load_state(f).get(me, 0) or 0)
            unread = max(0, len(blocks) - count)
            out.append(("room", name, unread))

    dm_dir = croot / "dm"
    if dm_dir.is_dir():
        for f in sorted(dm_dir.glob("*.md")):
            name = f.stem
            if me not in name.split("--"):
                continue
            blocks = _conv_blocks(f)
            count = int(_load_state(f).get(me, 0) or 0)
            unread = max(0, len(blocks) - count)
            out.append(("dm", name, unread))

    return out


def audience_prime(croot: Path, root: Path, reason: str,
                   sender: str | None, morals: bool) -> None:
    """Request an audience with the prime — the only path into the prime.

    Writes the reason to the prime's inbox file (`sessions/inbox/prime.md`)
    and records the audience so a sender may ask once per rotation unless the
    morals are at stake. The rule is printed back."""
    sender_id = _detect_sender(sender)
    rotation = os.environ.get("AGI_LOOP", "default")

    # one audience per sender per rotation, unless --morals
    if not morals:
        state_dir = croot / "audience"
        state_file = state_dir / "audiences.json"
        state: dict = {}
        if state_file.is_file():
            try:
                state = json.loads(state_file.read_text())
            except Exception:
                state = {}
        key = f"{sender_id}@{rotation}"
        if state.get(key):
            print(f"ERR: {sender_id} already had an audience with the prime "
                  f"this rotation ({rotation}). One audience per sender per "
                  f"rotation unless the morals are at stake (--morals).",
                  file=sys.stderr)
            raise SystemExit(1)
        state_dir.mkdir(parents=True, exist_ok=True)
        state[key] = True
        state_file.write_text(json.dumps(state))

    # deliver into the prime's inbox
    send(root, PRIME, f"[audience request] {reason}", sender_id)
    print(f"audience requested of the prime by {sender_id}: {reason!r}")
    print("rule: the prime is inbox-only; one audience per sender per rotation "
          "unless the morals are at stake (--morals).")


# ── CLI ────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="one-verb agent comms")
    # shared options on every subparser (and on the main parser) so the flags
    # work whether they precede or follow the subcommand
    # The parent parser's flags use default=argparse.SUPPRESS so that a flag
    # placed BEFORE the subcommand (parsed by the main parser) is not clobbered
    # by the subparser's own (absent) default. With SUPPRESS, an absent flag
    # leaves the namespace untouched and the main-parser value survives.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--from", dest="from_id", default=argparse.SUPPRESS,
                        help="override sender id (default: AGI_AGENT_ID or unknown)")
    common.add_argument("--comms-root", dest="comms_root",
                        default=argparse.SUPPRESS,
                        help="override the comms root for room/dm verbs")
    ap.add_argument("--from", dest="from_id", default=None,
                    help="override sender id (default: AGI_AGENT_ID or unknown)")
    ap.add_argument("--comms-root", dest="comms_root", default=None,
                    help="override the comms root for room/dm verbs")
    sub = ap.add_subparsers(dest="verb", required=True)

    # existing inbox verbs, unchanged surface
    p_send = sub.add_parser("send", parents=[common],
                            help="send a message (inbox, dm, or room)")
    p_send.add_argument("text", nargs="*", help="message text")
    p_send.add_argument("--to", dest="dm_to", default=None,
                        help="pairwise dm recipient (comms/dm/<a>--<b>.md)")
    p_send.add_argument("--room", dest="room", default=None,
                        help="quorum room (comms/room/<name>.md)")
    p_send.add_argument("target", nargs="?", default=None,
                        help="inbox recipient (positional, unchanged)")

    p_read = sub.add_parser("read", parents=[common],
                            help="read a conversation / inbox")
    p_read.add_argument("target", nargs="?", default=None,
                        help="inbox self (positional, unchanged)")
    p_read.add_argument("--room", dest="room", default=None,
                        help="room to read")
    p_read.add_argument("--dm", dest="dm", default=None,
                        help="dm partner to read")
    p_read.add_argument("--since", default=None, help="only after this ts (ISO)")
    p_read.add_argument("--all", dest="all_", action="store_true",
                        help="show the whole transcript without advancing the cursor")
    p_read.add_argument("--me", default=None,
                        help="participant id for read positions (default: sender)")

    p_peek = sub.add_parser("peek", parents=[common], help="peek without marking read")
    p_peek.add_argument("target", nargs="?", default=None,
                        help="inbox self (positional, unchanged)")
    p_peek.add_argument("--room", dest="room", default=None, help="room to peek")
    p_peek.add_argument("--dm", dest="dm", default=None, help="dm to peek")
    p_peek.add_argument("--since", default=None, help="only after this ts (ISO)")
    p_peek.add_argument("--all", dest="all_", action="store_true",
                        help="show the whole transcript without advancing the cursor")
    p_peek.add_argument("--me", default=None,
                        help="participant id (default: sender)")

    p_rooms = sub.add_parser("rooms", parents=[common],
                             help="list rooms and dms with unread")
    p_rooms.add_argument("--me", default=None,
                         help="participant id (default: sender)")

    p_aud = sub.add_parser("audience", parents=[common],
                           help="request an audience with the prime")
    p_aud.add_argument("target", help="must be `prime`")
    p_aud.add_argument("--reason", default="", help="why you need the prime")
    p_aud.add_argument("--morals", action="store_true",
                       help="bypass one-per-rotation gate (morals at stake)")

    args = ap.parse_args(argv)

    root = _project_root()
    croot = comms_root(root, args.comms_root)
    sender = args.from_id

    if args.verb == "send":
        text = " ".join(args.text) if args.text else ""
        if args.room is not None:
            if not text:
                print("ERR: message text is required for send --room",
                      file=sys.stderr)
                return 1
            print(send_room(croot, args.room, text, sender).resolve())
            return 0
        if args.dm_to is not None:
            if not text:
                print("ERR: message text is required for send --to",
                      file=sys.stderr)
                return 1
            print(send_dm(croot, _detect_sender(sender), args.dm_to, text,
                          sender).resolve())
            return 0
        # unchanged: inbox send, positional target
        if not args.target:
            print("ERR: send needs a target (inbox) or --room/--to",
                  file=sys.stderr)
            return 1
        if not text:
            print("ERR: message text is required for send", file=sys.stderr)
            return 1
        send(root, args.target, text, sender)
        return 0

    if args.verb == "read":
        me = args.me or _detect_sender(sender)
        all_ = getattr(args, "all_", False)
        if args.room is not None:
            for line in read_room(croot, args.room, me, args.since, sender,
                                  all_):
                print(line)
            return 0
        if args.dm is not None:
            for line in read_dm(croot, me, args.dm, args.since, sender, all_):
                print(line)
            return 0
        if not args.target:
            print("ERR: read needs a target (inbox) or --room/--dm",
                  file=sys.stderr)
            return 1
        read(root, args.target, sender)
        return 0

    if args.verb == "peek":
        me = args.me or _detect_sender(sender)
        all_ = getattr(args, "all_", False)
        if args.room is not None:
            for line in peek_room(croot, args.room, me, args.since, all_):
                print(line)
            return 0
        if args.dm is not None:
            for line in peek_dm(croot, me, args.dm, args.since, all_):
                print(line)
            return 0
        if not args.target:
            print("ERR: peek needs a target (inbox) or --room/--dm",
                  file=sys.stderr)
            return 1
        peek(root, args.target)
        return 0

    if args.verb == "rooms":
        me = args.me or _detect_sender(sender)
        rows = rooms(croot, me)
        if not rows:
            print(f"no rooms or dms for {me}")
            return 0
        for kind, name, unread in rows:
            print(f"{kind:5s} {name:<30s} {unread} unread")
        return 0

    if args.verb == "audience":
        if args.target != PRIME:
            print(f"ERR: audience targets the prime only, got {args.target!r}",
                  file=sys.stderr)
            return 1
        audience_prime(croot, root, args.reason, sender, args.morals)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
