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
    send.py audience quorum --reason TEXT — ask the quorum for a ruling (any
        caller); a quorum member answers with
        send.py report --room quorum-requests --ref TS TEXT (quorum-only)

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
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(_BIN))
sys.path.insert(0, str(_BIN.parent / "src"))
import locations  # noqa: E402
import spawn_gate  # noqa: E402
from graph_core.persistence import frontmatter as _fm  # noqa: E402


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

#: The door for anyone outside the quorum (master-sensei, an advisor, even
#: the prime) to ask the quorum for a ruling (hypothesis:l3w4-quorum-request-
#: path). The quorum's own room ("quorum") is closed to everyone else by
#: owner ruling 2026-09-08; this room is the sanctioned way in. `audience
#: quorum --reason TEXT` asks; `report --room QUORUM_REQUEST_ROOM --ref TS
#: TEXT` (quorum-only) answers in the same thread.
QUORUM_REQUEST_ROOM = "quorum-requests"

#: The three advisor visions, one vote each in a complete quorum
#: (hypothesis:l3w4-quorum-reviews). A tally needs all three.
VISIONS = ("alive", "all-is-one", "self-perpetuating")

#: The alignment enum a quorum vote may carry (mirrors the `alignment`
#: field on report nodes and the `schemas/[outcome].md` enum).
ALIGNMENTS = ("aligned", "adjust", "unknown")

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


def _quorum_caller() -> bool:
    """True when the caller is a tier-3 parent (the quorum) — the only role
    that may reach the prime without the morals override
    (hypothesis:l3w4-quorum-reviews: "The quorum IS Belam to anyone else")."""
    role = os.environ.get("AGI_ROLE", "").strip()
    tier = os.environ.get("AGI_LADDER_TIER", "").strip()
    return role == "parent" and tier == "3"


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


def _main_graph_root(root: Path) -> Path:
    """The graph root of the MAIN checkout, from any depth (worktree or main).

    `hypothesis:l3w4-parent-branch-merge-up` — a `--branch` kid runs in its
    own git worktree, which carries its own `.agi/`; comms must stay the ONE
    shared directory for a season, so we resolve the main checkout through
    `locations.git_common_root` and re-apply graph discovery from there. In
    the main checkout this is the identity (same `.agi/` comes back), so the
    default comms location never moves for non-worktree callers.
    """
    graph = locations.find_project_root(root) or root
    main = locations.git_common_root(graph)
    main_graph = locations.find_project_root(main) if main else None
    return main_graph or graph


def _default_comms_root(root: Path) -> Path:
    """`<graph_root>/comms/season-<N>/` — a declared, season-level root whose
    path does not change when a new iteration dir is minted.

    Season from the ladder node's `current_season`, failing open to 1 (a
    missing ladder must never scatter comms). Never the newest iteration dir: a
    per-iteration root would RESET the standing rooms on every loop.
    """
    graph = _main_graph_root(root)
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
    against the MAIN checkout's graph root (`_main_graph_root`), so under a
    `--branch` kid the comms dir stays the main checkout's — one room per
    season, never one per worktree."""
    if override:
        p = Path(override).expanduser()
        return p.resolve() if p.is_absolute() else (root / p).resolve()
    graph = _main_graph_root(root)
    cfg = locations.load_config(graph)
    declared = (cfg.get("locations") or {}).get("comms_root")
    if isinstance(declared, str) and declared.strip():
        p = Path(declared.strip()).expanduser()
        return p.resolve() if p.is_absolute() else (graph / p).resolve()
    return _default_comms_root(graph)


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


def _nudge_window(tmux_session: str | None, window: str, text: str) -> bool:
    """Best-effort `tmux send-keys` nudge into a perpetual seat's window
    (hypothesis:l3w4-seat-transport).

    Types `text Enter` into the window literally named `window` in the tmux
    session; fires only when that window exists and silently returns False
    otherwise — windowless (ephemeral/fire-and-forget) recipients are
    untouched. Never raises: tmux missing, a missing session/window, or a
    timeout is a no-op.
    """
    if not window:
        return False
    if tmux_session is None:
        import rotate  # lazy: same bin dir, DEFAULT_TMUX_SESSION lives there
        tmux_session = rotate.DEFAULT_TMUX_SESSION
    try:
        listing = subprocess.run(
            ["tmux", "list-windows", "-t", tmux_session,
             "-F", "#{window_name}"],
            capture_output=True, text=True, timeout=5,
        )
        if listing.returncode != 0:
            return False
        names = [ln.strip() for ln in listing.stdout.strip().splitlines()
                 if ln.strip()]
        if window not in names:
            return False
        subprocess.run(
            ["tmux", "send-keys", "-t", f"{tmux_session}:{window}",
             text, "Enter"],
            capture_output=True, text=True, timeout=5,
        )
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


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

    # Best-effort nudge into a perpetual seat's window; a no-op for
    # windowless (ephemeral) recipients (hypothesis:l3w4-seat-transport).
    _nudge_window(None, to, text)

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
    """Append a message to the pairwise dm file `<a>--<b>.md`, names sorted.

    A dm may never address or originate from the prime, like a room
    (hypothesis:l3w4-quorum-reviews): the prime is inbox-only, reached only
    through the gated `audience` path.
    """
    if other == PRIME or me == PRIME or other.startswith(PRIME + "-"):
        print(f"ERR: the prime is inbox-only; a dm may not address or "
              f"originate from the prime — use `audience prime` instead",
              file=sys.stderr)
        raise SystemExit(1)
    a, b, _ = _dm_pair(me, other)
    path = _dm_path(croot, me, other)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(_block(_now(), _detect_sender(sender), other, text))
    # Nudge the other party's tmux window when it exists (silent no-op
    # otherwise) — hypothesis:l3w4-seat-transport.
    _nudge_window(None, other, text)
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


# ── master comms and escalation (hypothesis:l3w4-masters-comms-and-escalation)


def ask(croot: Path, root: Path, me: str, to: str, text: str,
        sender: str | None) -> Path:
    """`ask --to NAME`: dm a Master (a `-master` seat), tagged `[ask]`.

    `to` must end `-master` and, when the seat registry is readable, be a
    registered row in it (fail-closed on a present-but-unknown name);
    fail-open to the suffix check alone when `seats.md` is absent/unreadable
    (spawn_gate.read_seat_registry's own contract).
    """
    if not to.endswith("-master"):
        print(f"ERR: {to!r} is not a -master seat", file=sys.stderr)
        raise SystemExit(1)
    seats = spawn_gate.read_seat_registry(root / "nodes")
    if seats is not None and not any(row.get("name") == to for row in seats):
        print(f"ERR: {to!r} is not a registered -master seat", file=sys.stderr)
        raise SystemExit(1)
    return send_dm(croot, me, to, f"[ask] {text}", sender)


def report(croot: Path, me: str, asker: str | None, ref: str, text: str,
           sender: str | None, room: str | None = None) -> Path:
    """`report --to ASKER --ref TS`: reply only inside a matching `[ask]`.

    Requires a block in the `<me>--<asker>.md` dm with `ts == ref` and
    `from == asker` whose text starts `[ask]`; else refuses and writes
    nothing.

    `report --room R --ref TS` (hypothesis:l3w4-quorum-request-path) is the
    same contract against a ROOM instead of a dm: any `[ask]` at that `ts` in
    room `R` qualifies (a room has no single fixed asker), and the reply
    posts back into the same room as `[report ref=TS]`, so the question and
    the ruling live in one file. Replying inside QUORUM_REQUEST_ROOM is
    quorum-only (mirrors `audience_prime`'s gate to the prime): a ruling
    anyone could forge is not a ruling.
    """
    if room:
        if room == QUORUM_REQUEST_ROOM and not _quorum_caller():
            print(f"ERR: replying in {QUORUM_REQUEST_ROOM!r} is quorum-only "
                  f"-- AGI_ROLE=parent + AGI_LADDER_TIER=3 required.",
                  file=sys.stderr)
            raise SystemExit(1)
        blocks = _conv_blocks(_room_path(croot, room))
        matched = any(
            _norm(b.get("ts", "")) == _norm(ref)
            and b.get("text", "").lstrip().startswith("[ask]")
            for b in blocks
        )
        if not matched:
            print(f"ERR: no [ask] at {ref} in room {room!r}", file=sys.stderr)
            raise SystemExit(1)
        return send_room(croot, room, f"[report ref={ref}] {text}", sender)

    blocks = _conv_blocks(_dm_path(croot, me, asker))
    matched = any(
        _norm(b.get("ts", "")) == _norm(ref)
        and b.get("from") == asker
        and b.get("text", "").lstrip().startswith("[ask]")
        for b in blocks
    )
    if not matched:
        print(f"ERR: no [ask] from {asker} at {ref}", file=sys.stderr)
        raise SystemExit(1)
    return send_dm(croot, me, asker, f"[report ref={ref}] {text}", sender)


def escalate(croot: Path, text: str, to: str | None, concern: str,
             sender: str | None) -> Path:
    """`escalate [--to owner] [--concern V] TEXT`.

    No `--to`: posts `[concern:V]` into room `tier3-quorum`. `--to owner`:
    dms `liaison` (never `prime`), gated to a parent at ladder tier 3.
    """
    if to == "owner":
        if (os.environ.get("AGI_ROLE") != "parent"
                or os.environ.get("AGI_LADDER_TIER") != "3"):
            print("ERR: escalate --to owner requires AGI_ROLE=parent and "
                  "AGI_LADDER_TIER=3", file=sys.stderr)
            raise SystemExit(1)
        return send_dm(croot, _detect_sender(sender), "liaison",
                       f"[owner-decision] {text}", sender)
    return send_room(croot, "tier3-quorum", f"[concern:{concern}] {text}",
                     sender)


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

    # quorum-only gate to the prime; only --morals bypasses it
    if not morals and not _quorum_caller():
        print(f"ERR: an audience with the prime is quorum-only — "
              f"AGI_ROLE=parent + AGI_LADDER_TIER=3 required, or --morals "
              f"(morality outranks the quorum).", file=sys.stderr)
        raise SystemExit(1)

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


def audience_quorum(croot: Path, reason: str, sender: str | None) -> Path:
    """`audience quorum --reason TEXT`: ask the quorum for a ruling.

    hypothesis:l3w4-quorum-request-path. The quorum's own room ("quorum") is
    closed to everyone but the three vision seats (owner, 2026-09-08); this
    is the sanctioned door for master-sensei, an advisor, or the prime to ask
    it something. Posts `[ask] TEXT` into QUORUM_REQUEST_ROOM, open to any
    caller -- no quorum-only gate here, that gate belongs on the ANSWER
    (`report --room QUORUM_REQUEST_ROOM`, see `report`). A quorum member
    replies in the same room, so the question and the ruling live in one
    file: a ruling that leaves no trace is not a ruling.
    """
    sender_id = _detect_sender(sender)
    path = send_room(croot, QUORUM_REQUEST_ROOM, f"[ask] {reason}", sender_id)
    print(f"quorum audience requested by {sender_id}: {reason!r}")
    print(f"rule: a quorum member answers with `send.py report --room "
          f"{QUORUM_REQUEST_ROOM} --ref <ts-of-this-message> TEXT`.")
    return path


# ── quorum review (hypothesis:l3w4-quorum-reviews) ──────────────────────


def vote(croot: Path, room: str, target: str, vision: str, alignment: str,
         sender: str | None, morals: bool, reason: str,
         round_: str) -> Path:
    """Post one advisor's `VOTE` line into a quorum room, via `send_room`
    (which keeps the room prime-free). Every vote carries the round, the
    judgement target, the advisor's vision, its alignment, the reason, and a
    morals flag. `tally_votes` reads exactly this shape back."""
    if vision not in VISIONS:
        print(f"ERR: vision must be one of {', '.join(VISIONS)}, got {vision!r}",
              file=sys.stderr)
        raise SystemExit(1)
    if alignment not in ALIGNMENTS:
        print(f"ERR: alignment must be one of {', '.join(ALIGNMENTS)}, "
              f"got {alignment!r}", file=sys.stderr)
        raise SystemExit(1)
    if not target:
        print("ERR: vote needs --target", file=sys.stderr)
        raise SystemExit(1)
    round_ = round_ or os.environ.get("AGI_LOOP", "default")
    line = (f"VOTE | round={round_} | target={target} | vision={vision} "
            f"| alignment={alignment} | reason={reason} "
            f"| morals={1 if morals else 0}")
    return send_room(croot, room, line, sender)


def _parse_vote(text: str) -> dict | None:
    """Parse a `VOTE | key=val | ...` room line into a dict. Returns None for
    non-vote lines (ordinary chatter) or a line with an unknown vision."""
    if not text.strip().startswith("VOTE"):
        return None
    d: dict[str, str | bool] = {}
    for tok in text.strip()[4:].split("|"):
        tok = tok.strip()
        if "=" in tok:
            k, _, v = tok.partition("=")
            d[k.strip()] = v.strip()
    if d.get("vision") not in VISIONS:
        return None
    d["morals"] = str(d.get("morals")) == "1"
    return d


def tally_votes(croot: Path, room: str, target: str, round_: str) -> dict:
    """Tally the quorum's votes in `room` for one `target` and `round`.

    Groups by vision (one advisor per vision); for a vision voted twice the
    LAST write wins. Requires all three visions present, else ERR "incomplete
    quorum" and exits 1. Returns {vision: {alignment, reason, morals, from}}.
    """
    path = _room_path(croot, room)
    by_vision: dict = {}
    for b in _read_conv(path):
        parsed = _parse_vote(b.get("text", ""))
        if not parsed:
            continue
        if parsed.get("target") != target:
            continue
        if parsed.get("round") != round_:
            continue
        parsed["from"] = b.get("from", "")
        by_vision[str(parsed["vision"])] = parsed  # last write wins
    missing = [v for v in VISIONS if v not in by_vision]
    if missing:
        print(f"ERR: incomplete quorum in room {room!r} for {target} round "
              f"{round_}: missing vision(s) {', '.join(missing)}",
              file=sys.stderr)
        raise SystemExit(1)
    return by_vision


#: Filenames for the audience-exit sidecar and audience state, under
#: `<croot>/audience/`.
EXITED_STATE = "exited.json"
AUDIENCE_STATE = "state.json"


def audience_close(croot: Path, round_: str, decision: str = "") -> None:
    """Close an audience with the prime for one round: the prime is excluded
    from further group traffic that rotation (`exited.json[prime][round]=true`)
    and the {opened,closed,decision} record is kept in `state.json`.
    """
    state_dir = croot / "audience"
    state_dir.mkdir(parents=True, exist_ok=True)
    ts = _now()

    exited: dict = {}
    ep = state_dir / EXITED_STATE
    if ep.is_file():
        try:
            exited = json.loads(ep.read_text())
        except Exception:
            exited = {}
    exited.setdefault(PRIME, {})[round_] = True
    ep.write_text(json.dumps(exited))

    state: dict = {}
    sp = state_dir / AUDIENCE_STATE
    if sp.is_file():
        try:
            state = json.loads(sp.read_text())
        except Exception:
            state = {}
    rec = state.setdefault(PRIME, {}).setdefault(round_, {"opened": ts})
    rec["closed"] = ts
    if decision:
        rec["decision"] = decision
    sp.write_text(json.dumps(state))
    print(f"audience with the prime closed; prime excluded from group "
          f"traffic for round {round_}")


def prime_excluded(croot: Path, round_: str) -> int:
    """Exit 0 when the prime is excluded for `round_`, else exit 1 — a probe
    a rotation-loop alarm reads to know Belam has left the room
    (hypothesis:l3w4-seat-rotation-loops)."""
    ep = croot / "audience" / EXITED_STATE
    if ep.is_file():
        try:
            exited = json.loads(ep.read_text())
            if exited.get(PRIME, {}).get(round_):
                print(f"prime excluded for round {round_}")
                return 0
        except Exception:
            pass
    print(f"prime NOT excluded for round {round_}", file=sys.stderr)
    return 1


# ── CLI ────────────────────────────────────────────────────────────────────


# --------------------------------------------------------------------------- #
# whois — authority verified against the graph, never against the message
# (hypothesis:l4-authority-verified-against-the-graph-not-the-message)
#
# A named sender offers a session_ref as proof of identity. The only
# authoritative registry is config:seats, and the only trustworthy copy of it
# is the PUSHED ref, not the working tree — a working-tree file is exactly what
# an impersonator benefits from and what a stale worktree gets wrong. Read it
# with `git show <pushed-ref>:<path>`, parse it with the SAME node-loader the
# engine already uses (graph_core frontmatter, the path hierarchy.load_seats
# takes — never a new hand-rolled parser), and label every answer:
#   * VERIFIED + the commit sha the answer came from, when the pushed ref is
#     reachable (provenance IN the answer, always);
#   * UNVERIFIED + non-zero exit, when it is not — never a silent success.
# --------------------------------------------------------------------------- #

#: The pushed branch that carries config:seats (`.agi/nodes/.geometry/seats.md`).
#: The prime updates and pushes it at every rotation, so its HEAD is the
#: authoritative answer after a fetch — never the local working tree.
_PUSHED_SEATS = "origin/season/s2"
_SEATS_REPO_PATH = ".agi/nodes/.geometry/seats.md"


def _load_seats_rows(content: str) -> list:
    """Parse a seats.md byte-string with the engine's node-loader (the same
    path hierarchy.load_seats uses) — reusing the ONE parse, never adding a
    sixth hand-rolled reader."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as tf:
        tf.write(content)
        tmp = Path(tf.name)
    try:
        nf = _fm.load_node_file(tmp)
        return [dict(r) for r in ((nf.frontmatter or {}).get("seats") or [])
                if isinstance(r, dict)]
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass


def _run_git(root: Path, args: list):
    """Run a git READ from the project root; None on any failure."""
    try:
        return subprocess.run(["git", *args], cwd=str(root),
                              capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, OSError):
        return None


def _pushed_seats(root: Path, ref: str, do_fetch: bool):
    """Return (rows, commit_sha) read from the PUSHED ref, or None if the
    pushed authority cannot be reached. Fetches first (unless disabled), then
    `git rev-parse` for the provenance sha and `git show` for the file."""
    if do_fetch:
        fetch = _run_git(root, ["fetch", "origin", "season/s2"])
        if fetch is None or fetch.returncode != 0:
            return None
    sha = _run_git(root, ["rev-parse", ref])
    if sha is None or sha.returncode != 0:
        return None
    shown = _run_git(root, ["show", f"{ref}:{_SEATS_REPO_PATH}"])
    if shown is None or shown.returncode != 0:
        return None
    return _load_seats_rows(shown.stdout), sha.stdout.strip()


def _locally_loaded_rows(root: Path) -> list:
    """Fallback rows from the WORKING-TREE file, used only for the UNVERIFIED
    fallback path — never the authority, always clearly labelled so."""
    p = root / "nodes" / ".geometry" / "seats.md"
    if not p.is_file():
        return []
    try:
        return _load_seats_rows(p.read_text())
    except Exception:                                            # noqa: BLE001
        return []


#: whois exit codes. 🔴 A NEGATIVE ANSWER MUST NOT EXIT 0. This check exists
#: to be USED -- `send.py whois <ref> --claim <role> && trust_them` is the
#: whole point -- and a refusal that returns success is the failure this repo
#: has now paid for three times in one day: a spawn gate printing UNVERIFIED
#: and returning success while writing a real node, a meter printing a
#: confident fraction for a transcript it could not attribute, and a floor
#: whose printed remedy did not clear the floor. Distinct codes so a caller
#: can tell "not who they claim" from "not in the table at all" from "I could
#: not reach the authority".
WHOIS_OK = 0                #: verified AND the answer is affirmative
WHOIS_UNVERIFIED = 1        #: pushed authority unreachable -- unproven
WHOIS_NOT_AUTHORIZED = 2    #: ref is real but is NOT the claimed seat/role
WHOIS_NO_MATCH = 3          #: ref belongs to no seat row at all


def _resolve_rows(rows: list, session_ref: str,
                  claim: str | None) -> tuple[int, str]:
    """Answer the is-this-who-they-say question for one ref. Two directions:
    with no --claim, name the seat + role the ref belongs to; with
    --claim NAME, answer whether this ref IS that row (a ref present in the
    table but under a DIFFERENT name/role answers NO — the impersonation case)."""
    hits = [r for r in rows if r.get("session_ref") == session_ref]
    if not hits:
        return WHOIS_NO_MATCH, f"NO-MATCH: {session_ref} belongs to no seat row"
    who = hits[0]
    name = who.get("name", "?")
    role = who.get("role", "?")
    if claim:
        ok = (claim == name) or (claim == role)
        verdict = "IS-AUTHORIZED" if ok else "IS-NOT-AUTHORIZED"
        return ((WHOIS_OK if ok else WHOIS_NOT_AUTHORIZED),
                f"{verdict}: {session_ref} vs claim {claim!r} "
                f"-> actual seat {name}, role {role}")
    return WHOIS_OK, f"SEAT: {session_ref} -> seat {name}, role {role}"


def whois(root: Path, session_ref: str, claim: str | None,
          source: str = _PUSHED_SEATS, do_fetch: bool = True):
    """Resolve session_ref against the PUSHED config:seats.

    Returns `(exit, text)` using the WHOIS_* codes: 0 only when the answer is
    both authoritative AND affirmative, 1 UNVERIFIED, 2 NOT-AUTHORIZED,
    3 NO-MATCH. Provenance (source ref + commit sha) is in every verified
    answer."""
    seeded = _pushed_seats(root, source, do_fetch)
    if seeded is None:
        # Pushed authority unreachable. Do NOT silently answer from the working
        # tree: answer, but label it UNVERIFIED and exit non-zero. An
        # unauthoritative answer must never exit 0.
        _code, answer = _resolve_rows(_locally_loaded_rows(root), session_ref,
                                      claim)
        text = (f"UNVERIFIED {session_ref}: pushed ref {source!r} unreachable; "
                f"reading working tree, NOT authoritative — treat as unproven\n"
                + answer)
        # UNVERIFIED outranks whatever the working tree happened to say: the
        # caller must not act on an answer we could not authenticate, even a
        # negative one.
        return WHOIS_UNVERIFIED, text
    rows, sha = seeded
    code, answer = _resolve_rows(rows, session_ref, claim)
    return code, f"{answer}  (verified against {source} @ {sha})"


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
    # ONE positional list, split in code (hypothesis:l3w4-quorum-request-
    # path) -- a separate `target` (nargs='?') + `text` (nargs='*') positional
    # pair is ambiguous by construction and breaks one direction whichever
    # order they're declared in: target-first (L3.43's own fix, immediately
    # prior to this one) swallows the first token of `--room`/`--to` text
    # into target and leaves text empty ("message text is required" on EVERY
    # --room/--to send); text-first swallows the inbox target instead ("send
    # needs a target" on every plain send, the bug L3.43 was fixing). Neither
    # order can satisfy both `send TARGET TEXT...` and `send --room R TEXT...`
    # -- argparse's nargs matching has no way to know which positional a
    # trailing token belongs to until --room/--to's presence is checked, and
    # that check can only happen after parsing. So: one bucket, no nargs
    # ambiguity, and the split happens where the information actually is.
    p_send.add_argument("send_args", nargs="*",
                        help="inbox: TARGET TEXT...; with --room/--to: TEXT...")
    p_send.add_argument("--to", dest="dm_to", default=None,
                        help="pairwise dm recipient (comms/dm/<a>--<b>.md)")
    p_send.add_argument("--room", dest="room", default=None,
                        help="quorum room (comms/room/<name>.md)")

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
                           help="request an audience with the prime or quorum")
    p_aud.add_argument("target", help="`prime`, `quorum`, or `close`")
    p_aud.add_argument("--reason", default="", help="why you need the prime/quorum")
    p_aud.add_argument("--morals", action="store_true",
                       help="bypass one-per-rotation gate (morals at stake)")
    p_aud.add_argument("--round", dest="aud_round", default="",
                       help="round to close/exclude (audience close)")
    p_aud.add_argument("--decision", default="",
                       help="decision record (audience close)")

    p_vote = sub.add_parser("vote", parents=[common],
                  help="post one advisor quorum vote into a room")
    p_vote.add_argument("--room", default="tier3-quorum",
                        help="room to post the vote into")
    p_vote.add_argument("--target", required=True,
                        help="node id the vote judges")
    p_vote.add_argument("--vision", required=True,
                        help="your vision: " + ",".join(VISIONS))
    p_vote.add_argument("--alignment", required=True,
                        help="your alignment: " + ",".join(ALIGNMENTS))
    p_vote.add_argument("--reason", default="", help="one-line why")
    p_vote.add_argument("--morals", action="store_true",
                        help="morals at stake: forces audience not stamp")
    p_vote.add_argument("--round", dest="v_round", default="",
                        help="round (default: AGI_LOOP)")

    p_pe = sub.add_parser("prime-excluded", parents=[common],
                  help="exit 0 if the prime is excluded for a round, else 1")
    p_pe.add_argument("--round", required=True)

    p_ask = sub.add_parser("ask", parents=[common],
                  help="dm a Master seat, tagged [ask]")
    p_ask.add_argument("--to", required=True, help="a -master seat")
    p_ask.add_argument("text", nargs="*", help="message text")

    p_report = sub.add_parser("report", parents=[common],
                  help="reply to a matching [ask] (dm or --room)")
    p_report.add_argument("--to", dest="asker", default=None,
                          help="the asker to reply to (dm; exactly one of "
                               "--to/--room)")
    p_report.add_argument("--room", dest="report_room", default=None,
                          help="room to reply in, e.g. quorum-requests "
                               "(exactly one of --to/--room)")
    p_report.add_argument("--ref", required=True,
                          help="ts of the [ask] block being answered")
    p_report.add_argument("text", nargs="*", help="message text")

    p_whois = sub.add_parser(
        "whois", parents=[common],
        help="resolve a claimed session_ref against the PUSHED config:seats "
             "(authority is the graph, never the message; hypothesis:l4-"
             "authority-verified-against-the-graph-not-the-message)")
    p_whois.add_argument("session_ref",
                         help="the session_ref (e.g. 7902ac) to verify")
    p_whois.add_argument("--claim", default=None,
                         help="claimed seat name or role; answer whether this "
                              "ref IS that row (impersonation check)")
    p_whois.add_argument("--source", default=_PUSHED_SEATS,
                         help="git ref to read seats from (default: pushed "
                              "origin/season/s2)")
    p_whois.add_argument("--no-fetch", dest="no_fetch", action="store_true",
                         help="skip the `git fetch` before reading")

    p_esc = sub.add_parser("escalate", parents=[common],
                  help="post a concern, or escalate to owner via liaison")
    p_esc.add_argument("--to", default=None, help="'owner' or omit")
    p_esc.add_argument("--concern", default="vision",
                       help="concern tag when --to is omitted")
    p_esc.add_argument("text", nargs="*", help="message text")

    args = ap.parse_args(argv)

    root = _project_root()
    croot = comms_root(root, args.comms_root)
    sender = args.from_id

    if args.verb == "send":
        # --room/--to: the whole positional bucket is text, nothing is a
        # target. Split by MODE, not by argparse nargs (see p_send comment).
        if args.room is not None:
            text = " ".join(args.send_args)
            if not text:
                print("ERR: message text is required for send --room",
                      file=sys.stderr)
                return 1
            print(send_room(croot, args.room, text, sender).resolve())
            return 0
        if args.dm_to is not None:
            text = " ".join(args.send_args)
            if not text:
                print("ERR: message text is required for send --to",
                      file=sys.stderr)
                return 1
            print(send_dm(croot, _detect_sender(sender), args.dm_to, text,
                          sender).resolve())
            return 0
        # unchanged: inbox send -- first token is the target, the rest is text
        if not args.send_args:
            print("ERR: send needs a target (inbox) or --room/--to",
                  file=sys.stderr)
            return 1
        target, *rest = args.send_args
        text = " ".join(rest)
        if not text:
            print("ERR: message text is required for send", file=sys.stderr)
            return 1
        send(root, target, text, sender)
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
        if args.target == "close":
            if not args.aud_round:
                print("ERR: audience close needs --round", file=sys.stderr)
                return 1
            audience_close(croot, args.aud_round, args.decision)
            return 0
        if args.target == "quorum":
            audience_quorum(croot, args.reason, sender)
            return 0
        if args.target != PRIME:
            print(f"ERR: audience targets 'prime', 'quorum', or 'close', "
                  f"got {args.target!r}", file=sys.stderr)
            return 1
        audience_prime(croot, root, args.reason, sender, args.morals)
        return 0

    if args.verb == "vote":
        round_ = args.v_round or os.environ.get("AGI_LOOP", "default")
        print(vote(croot, args.room, args.target, args.vision,
                   args.alignment, sender, args.morals, args.reason,
                   round_))
        return 0

    if args.verb == "prime-excluded":
        return prime_excluded(croot, args.round)

    if args.verb == "ask":
        text = " ".join(args.text) if args.text else ""
        if not text:
            print("ERR: message text is required for ask", file=sys.stderr)
            return 1
        print(ask(croot, root, _detect_sender(sender), args.to, text,
                  sender).resolve())
        return 0

    if args.verb == "report":
        text = " ".join(args.text) if args.text else ""
        if not text:
            print("ERR: message text is required for report", file=sys.stderr)
            return 1
        if bool(args.asker) == bool(args.report_room):
            print("ERR: report needs exactly one of --to or --room",
                  file=sys.stderr)
            return 1
        print(report(croot, _detect_sender(sender), args.asker, args.ref,
                     text, sender, room=args.report_room).resolve())
        return 0

    if args.verb == "whois":
        rc, text = whois(root, args.session_ref, args.claim, args.source,
                         not args.no_fetch)
        print(text)
        return rc

    if args.verb == "escalate":
        text = " ".join(args.text) if args.text else ""
        if not text:
            print("ERR: message text is required for escalate", file=sys.stderr)
            return 1
        print(escalate(croot, text, args.to, args.concern, sender).resolve())
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
