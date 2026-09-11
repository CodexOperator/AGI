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
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

_BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(_BIN))
sys.path.insert(0, str(_BIN.parent / "src"))
import locations  # noqa: E402
import spawn_gate  # noqa: E402
import seatsig  # noqa: E402
from graph_core.persistence import frontmatter as _fm  # noqa: E402


#: Subdirectory under sessions/ for per-recipient inbox files.
INBOX_DIR = "inbox"

#: Subdirectory under sessions/ for per-seat signing-key files. Each key lives
#: under the SAME shared sessions dir as the inbox (a worktree kid shares the
#: main checkout's keys, exactly like the mail). The private seed is written
#: HERE and nowhere else: mode 0600, never printed, never logged, never under
#: the graph tree or in a commit (.agi/sessions/ is gitignored).
SEATS_DIR = "seats"
#: Mode for a seat key file. A 0600 private seed is the point -- readable by
#: the owning agent only.
SEAT_KEY_MODE = 0o600

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
    """`<sessions>/inbox/` — where per-recipient inbox files live.

    The mail must be ONE room across every git worktree, or a recipient who
    wrote/reads from the main checkout never sees mail a seat in a worktree
    sent (the boundary face: an inbox written to a root the recipient never
    reads). So this routes through the shared-sessions resolver, not the
    plain per-worktree join. A non-git root is the identity."""
    return locations.shared_sessions_dir(root) / INBOX_DIR


def _inbox_path(root: Path, recipient: str) -> Path:
    """The inbox file for one recipient."""
    return _inbox_dir(root) / f"{recipient}.md"


def _seats_dir(root: Path) -> Path:
    """`<sessions>/seats/` -- the ONE shared seat-key dir, like the inbox."""
    return locations.shared_sessions_dir(root) / SEATS_DIR


def _seat_key_path(root: Path, seat: str) -> Path:
    """The signing key file for one seat: `<sessions>/seats/<seat>.key`."""
    return _seats_dir(root) / f"{seat}.key"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_msg(ts: str, from_id: str, to: str, text: str) -> str:
    """The EXACT bytes a signature covers: ``ts\nfrom\nto\n\ntext``.

    Canonical form -- the values substituted for the placeholders, no `sig:`
    line, no prefix labels, no trailing newline beyond what the caller passes
    in ``text``. The signer and every verifier must reconstruct THIS string
    and nothing else, or a message cannot verify. A test asserts these exact
    bytes end-to-end.
    """
    return f"{ts}\n{from_id}\n{to}\n\n{text}"


def _sign_line(root: Path, from_id: str, ts: str, to: str,
               text: str) -> str | None:
    """The ``sig:`` header for one message, or None when unsigned.

    Signs only when ``<sessions>/seats/<from_id>.key`` exists (a seat that has
    generated a key). The line is ``sig: <scheme>:<fingerprint>:<sig_hex>`` --
    scheme name, the short fingerprint (first 16 hex of sha256 of the public
    key) for a human-readable handle, then the signature hex. The private seed
    is used only to sign, never printed or logged.
    """
    key_file = _seat_key_path(root, from_id)
    if not key_file.is_file():
        return None
    try:
        obj = json.loads(key_file.read_text())
    except (ValueError, OSError):
        return None
    scheme_name = obj.get("scheme")
    priv_hex = obj.get("priv_hex")
    if not scheme_name or not priv_hex:
        return None
    try:
        scheme = seatsig.get(scheme_name)
        priv = bytes.fromhex(priv_hex)
        pub = scheme.public_from_secret(priv)
        sig = scheme.sign(priv, _canonical_msg(ts, from_id, to, text).encode())
    except Exception:                                              # noqa: BLE001
        # A broken/mismatched key never takes a message down: fall back to
        # unsigned rather than crash a send (the reader then labels FORGED
        # with no forged sig -- a detectable absence, never a fabricated one).
        return None
    return f"sig: {scheme_name}:{seatsig.fingerprint(pub)}:{sig.hex()}"


def keygen(root: Path, seat: str, scheme_name: str = "ed25519") -> Path:
    """Mint a seat signing key under ``<sessions>/seats/<seat>.key``.

    Writes JSON {"scheme": ..., "priv_hex": ...} with mode 0600, creating the
    directory if needed. PRINTS the two seat-row cells someone must put into
    config:seats for this seat -- ``pubkey: <hex>`` and ``sig_scheme: <name>``
    -- and writes NO graph node (a seated role writes only its own row and
    only declared fields; the schema change adding pubkey + sig_scheme to the
    seat row is the prime's edit, not this command's). The PRIVATE seed is
    never printed, logged, or written outside sessions/.
    """
    scheme = seatsig.get(scheme_name)  # KeyError names the unknown scheme
    _priv, pub = scheme.keygen()
    d = _seats_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{seat}.key"
    payload = json.dumps({"scheme": scheme_name, "priv_hex": _priv.hex()})
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, SEAT_KEY_MODE)
    try:
        with os.fdopen(fd, "w") as f:
            f.write(payload)
    except BaseException:                                        # noqa: BLE001
        try:
            os.close(fd)
        except OSError:
            pass
        raise
    os.chmod(path, SEAT_KEY_MODE)
    # The two cells the row needs -- NEVER the private seed.
    print(f"pubkey: {pub.hex()}")
    print(f"sig_scheme: {scheme_name}")
    return path


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


#: One fixed machine-prefixed wake token. The only variable part is the
#: recipient seat name — never the sender, never the message body. The body
#: lives ONLY in the inbox/dm file; the token is a wake, not a message
#: (hypothesis:l4-a-nudge-is-a-wake-token-not-a-message, claim 1).
NUDGE_TOKEN_TEMPLATE = (
    "[agi-nudge] unread for {seat}:"
    " send.py read {seat}"
)

#: The token is SHORT on purpose (< 100 chars for every live seat name):
#: the prime pinned on a real Claude Code pane (nudge node 83fe8049c) that a
#: long chunk typed with its Enter in ONE send-keys call is taken for a paste
#: and stranded, and a token that wraps in the input box also defeats the
#: "already unsubmitted" capture-pane check. A seat name so long that the
#: full form would reach the cap gets the bare form instead (every brief
#: already carries the read command).
_NUDGE_TOKEN_MAX = 99
NUDGE_TOKEN_BARE_TEMPLATE = "[agi-nudge] unread for {seat}"

#: The pause between typing the literal token and the SEPARATE Enter call —
#: probe (D): `send-keys -l <text>`, sleep 0.3, then `send-keys Enter` as
#: its own call is queued and delivered; the two keys in one call are not.
_NUDGE_ENTER_DELAY_S = 0.3

#: At most ONE wake token per unread batch per seat. The per-seat nudge
#: marker (ts of the last token) absorbs a rapid succession of dms into a
#: single token; a later send re-issues the token when the marker is stale.
_NUDGE_COALESCE_WINDOW_S = 30.0


def _build_nudge_token(seat: str) -> str:
    """ONE fixed machine-prefixed wake token for one recipient seat, always
    shorter than `_NUDGE_TOKEN_MAX` (the bare form when the seat name is
    long enough to threaten the cap)."""
    token = NUDGE_TOKEN_TEMPLATE.format(seat=seat)
    if len(token) > _NUDGE_TOKEN_MAX:
        token = NUDGE_TOKEN_BARE_TEMPLATE.format(seat=seat)
    return token


#: Measured safe line length for a nudge typed with `-l` then Enter
#: (hypothesis:l4-the-nudge-carries-the-dm-body-inline). Derived from the
#: GEOMETRY of a REAL pane (`tmux capture-pane -p`), the committed fixture
#: extensions/agi/tests/fixtures/claude_pane_idle.txt (and _busy.txt): the
#: `─` separator row is 104 columns (sha256 3f28fc37.../c2928e9a... in the
#: fixture header). Claude's input box renders the typed line with a `❯ `
#: prefix (U+276F + space = 2 columns), so the line spans at most
#: 104 − 2 = 102 columns on ONE box row before it wraps. A token that wraps
#: in the input box defeats the "already unsubmitted" head check; the paste
#: heuristic (prime probe B, nudge node 83fe8049c) strands a one-call
#: `text Enter` chunk at ~100 chars (_FixturePane.PASTE_CHARS = 100). So:
#:   pane/separator width        104  (real capture)
#:   − input-box `❯ ` prefix      2
#:   = one-row line budget       102
#:   − margin under PASTE_CHARS  −7   (100 paste → 7 under)
#:   = _NUDGE_LINE_MAX            95
#: 95 < 102 (fits one visible box row) and 95 < 100 (under the paste
#: threshold, so even a hypothetical one-call `text Enter` chunk would not
#: strand), with room for the tails `… (read <seat>)` / `(+N more, read
#: <seat>)` / `(+unread inbox, read <seat>)`. The head (`[nudge: <from>:`)
#: stays short, so a wrapped line still matches.
_NUDGE_LINE_MAX = 95
#: Truncation tail appended when the flattened body would exceed the line
#: cap: `… (read <seat>)` (the newline-flatten ` / ` separator is truncated
#: with the body).
_NUDGE_TRUNC_TAIL = "… (read {seat})"
#: Tail appended to a DELIVERED line when earlier dms in the same batch
#: were coalesced (within the per-seat window) and never typed:
#: `(+N more, read <seat>)`.
_NUDGE_MORE_TAIL = " (+{n} more, read {seat})"
#: Tail appended to a deferred-dm delivery when it rides an inbox `send()`
#: retry: names the unread inbox message whose OWN wake token would otherwise
#: be swallowed (clause b, hypothesis:l4-send-py-same-sender-stranded-line-
#: and-the-swallowed-wake). Counted INSIDE the `_NUDGE_LINE_MAX` budget when
#: passed as `trailing` to `_nudge_line` (clause c), so the delivered line
#: never exceeds the cap.
_NUDGE_INBOX_TAIL = " (+unread inbox, read {seat})"


def _nudge_line(seat: str, sender: str, body: str, more: int = 0,
                trailing: str = "") -> str | None:
    """The inline pane line for a dm nudge (hypothesis:l4-the-nudge-carries-\
    the-dm-body-inline): `[nudge: <from>]: <body>`. The body is FLATTENED
    to one line (newlines -> ` / `) and, if the delivered line would exceed
    `_NUDGE_LINE_MAX`, TRUNCATED with a `… (read <seat>)` tail. `more>0`
    appends `(+N more, read <seat>)` for the dms coalesced before this one.
    `trailing` (e.g. the `(+unread inbox, read <seat>)` deferred-delivery
    tail) is appended and counted INSIDE the `_NUDGE_LINE_MAX` budget, so no
    delivery path emits a line longer than the cap. The body STILL lands in
    the dm file (the record); this line is delivery.

    Returns None when NO tail leaves room for at least one body character --
    a pathological sender/seat whose `prefix` alone eats the whole
    `_NUDGE_LINE_MAX` budget (hypothesis:l4-ownership-matches-the-rendered-
    line-and-zero-body-retreats). The caller DEFERS the dm instead of typing
    a zero-body line (prefix + tails only): zero-body delivery is
    unreachable. None is unobservable in the declared seat/sender range."""
    flat = " / ".join(p.strip() for p in body.splitlines() if p.strip())
    if not flat:
        flat = body
    more_tail = _NUDGE_MORE_TAIL.format(n=more, seat=seat) if more else ""
    trunc = _NUDGE_TRUNC_TAIL.format(seat=seat)          # `… (read <seat>)`
    trunc_more = trunc + more_tail                       # + `(+N more, ...)`
    prefix = f"[nudge: {sender}]: "
    full = prefix + flat + more_tail + trailing
    if len(full) <= _NUDGE_LINE_MAX:
        return full
    # The full line is over the cap: the BODY slice must be floored at 0 --
    # `flat[:keep]` with a negative keep is a LONG slice, not an empty one
    # (residue of clause c: a 494-char line against a 95-char cap). When even
    # `prefix + tails` alone busts the cap (long seat/sender names), retreat
    # from richest to leanest tail -- trailing first, then the trunc tail's
    # `(+N more)`, then the read-seat tail itself -- and only give the freed
    # budget to the body, never the reverse. The first tail that fits wins.
    for tail in (trunc_more + trailing,   # read + `(+N more)` + inbox note
                 trunc_more,              # drop the inbox note (trailing first)
                 trunc,                   # then shorten the trunc tail: drop +N more
                 ""):                     # drop every tail
        keep = _NUDGE_LINE_MAX - len(prefix) - len(tail)
        if keep >= 1:
            # a body must keep at least ONE character -- keep == 0 would
            # emit a zero-body line (prefix + tails only), which carries no
            # dm; retreat to a leaner tail instead. Zero-body delivery is
            # unreachable (hypothesis:l4-ownership-matches-the-rendered-line-
            # and-zero-body-retreats).
            return prefix + flat[:keep].rstrip() + tail
    # No tail leaves room for a single body character (pathological
    # sender/seat). Refuse the line: the caller defers, never emits a
    # zero-body delivery (not reached in the declared seat/sender range).
    return None


def _nudge_token_head(token: str) -> str:
    """The part of a typed line that survives the input box wrapping it, and
    is what the "already unsubmitted" check matches. For the inline DM line
    `[nudge: <from>]: <body>` the head is up to and including the SECOND `:`
    (`[nudge: <from>]:` -- the FIRST `:` is inside the `[nudge:` tag, so it
    is not a stable end); for the fixed wake token (`[agi-nudge] unread for
    <seat>: ...`) up to the first `:`."""
    if token.startswith("[nudge:"):
        first = token.find(":")
        i = token.find(":", first + 1)
        return token if i < 0 else token[:i + 1]
    i = token.find(":")
    return token if i < 0 else token[:i + 1]


#: The pane-line shapes send.py (and rotate.py, a sibling) can leave stranded
#: in an input box. Residue A (hypothesis:l4-the-nudge-carries-the-dm-body-
#: inline): the OLD unsubmitted check matched only the head of the EXACT line
#: a call was about to type, so a retry whose text was a DIFFERENT nudge shape
#: no longer matched a stranded line and typed INTO A NON-EMPTY BOX -- the
#: separate Enter then submitted BOTH lines as ONE user turn (the owner's
#: 2026-09-11 defect). Every shape send.py/rotate.py can type must be seen as
#: "something is already in the box, do not type a second line."
_NUDGE_PREFIXES = ("[nudge:", "[agi-nudge]", "[rotation-alert]")


def _stranded_in_region(region: str) -> str | None:
    """The first nudge-shaped / rotate-shaped line stranded in the input
    region, or None when the box holds only the prompt glyph / nothing.
    Detects ANY of the shapes (inline `[nudge: <from>]:`, the `[agi-nudge]`
    wake token, and rotate.py's `[rotation-alert]`) -- never only the head of
    the one line the caller is about to type, so a DIFFERENT stranded line
    still stops a send from typing a second line after it."""
    for line in (region or "").splitlines():
        s = line.strip().lstrip("\u276f").strip()
        for pre in _NUDGE_PREFIXES:
            if s.startswith(pre):
                return pre
    return None


def _seat_row_by_name(rows: list, name: str) -> dict | None:
    """The config:seats row whose `name` equals `name`, else None."""
    for r in rows:
        if r.get("name") == name:
            return r
    return None


def _nudge_marker_path(root: Path, seat: str) -> Path:
    return _inbox_dir(root) / f"{seat}.nudge"


def _nudge_pending_path(root: Path, seat: str) -> Path:
    return _inbox_dir(root) / f"{seat}.nudge.pending"


def _pending_more(root: Path, seat: str) -> int:
    """Coalesced-but-untyped dms awaiting the next delivered nudge's
    `(+N more, read <seat>)` tail (hypothesis:l4-the-nudge-carries-the-dm-
    body-inline). 0 = no pending tail."""
    try:
        return int(_nudge_pending_path(root, seat).read_text().strip() or 0)
    except Exception:                                    # noqa: BLE001
        return 0


def _bump_pending(root: Path, seat: str) -> None:
    """Increment the pending-coalesced count; a dm coalesced inside the
    per-seat window is counted here so a LATER delivered nudge carries it.
    Best-effort, never raises."""
    try:
        p = _nudge_pending_path(root, seat)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(str(_pending_more(root, seat) + 1))
    except OSError:
        pass


def _clear_pending(root: Path, seat: str) -> None:
    """Reset the pending-coalesced count after a nudge that carried it.
    Best-effort, never raises."""
    try:
        _nudge_pending_path(root, seat).write_text("0")
    except OSError:
        pass


def _nudge_deferred_path(root: Path, seat: str) -> Path:
    """Sidecar holding the FIRST deferred dm body for a seat (sender+body
    as JSON) -- a dm whose inline line coalesced under a busy pane and must
    be delivered INLINE by a later idle retry (hypothesis:l4-the-nudge-
    carries-the-dm-body-inline). Kept OUT of the pending count file so the
    count stays a bare int (the parse is unchanged)."""
    return _inbox_dir(root) / f"{seat}.nudge.deferred"


def _read_deferred(root: Path, seat: str) -> dict | None:
    """The stored deferred {sender, body} for a seat, or None."""
    try:
        p = _nudge_deferred_path(root, seat)
        if p.is_file():
            d = json.loads(p.read_text())
            if isinstance(d, dict) and d.get("body"):
                return d
    except Exception:                                    # noqa: BLE001
        pass
    return None


def _record_deferred_render(root: Path, seat: str, more: int) -> None:
    """Persist the `(+N more)` count a deferred delivery rendered its
    inline line with (hypothesis:l4-deferred-ownership-uses-the-rendered-
    count). A stranded line left by a PRIOR deferred delivery was typed
    with the count at ITS render time, so a later retry must judge
    ownership against THAT count, not the (changed) current pending --
    otherwise a short body whose `(+N more)` tail moved between attempts
    reads as foreign and the deferred body is delivered TWICE. Best-effort,
    never raises; a record with no prior render simply stays without the
    key and the caller falls back to the current count."""
    try:
        d = _read_deferred(root, seat)
        if d is None:
            return
        d["more"] = more
        _nudge_deferred_path(root, seat).write_text(json.dumps(d))
    except OSError:
        pass


def _store_deferred(root: Path, seat: str, sender: str, body: str) -> bool:
    """Persist the FIRST deferred dm body for a seat; a later dm in the
    same batch is COUNTED (pending), never overwrites the first. Returns
    True if it stored (this is the first deferred body), False if one was
    already pending. Best-effort, never raises."""
    if _read_deferred(root, seat) is not None:
        return False
    try:
        p = _nudge_deferred_path(root, seat)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"sender": sender, "body": body}))
        return True
    except OSError:
        return False


def _clear_deferred(root: Path, seat: str) -> None:
    """Drop the deferred dm body after a line carrying it (or a fresher
    dm that supersedes it) is actually DELIVERED -- never on a coalesce.
    Best-effort, never raises."""
    try:
        p = _nudge_deferred_path(root, seat)
        if p.exists():
            p.unlink()
    except OSError:
        pass


def _record_nudge(root: Path, seat: str) -> None:
    """Stamp the per-seat nudge marker; best-effort, never raises."""
    try:
        p = _nudge_marker_path(root, seat)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(_now() + "\n")
    except OSError:
        pass


def _last_nudge_age(root: Path, seat: str) -> float | None:
    """Seconds since the last typed nudge token for this seat, or None."""
    try:
        ts = _nudge_marker_path(root, seat).read_text().strip()
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc)
                - dt.astimezone(timezone.utc)).total_seconds()
    except Exception:                                    # noqa: BLE001
        return None


def _capture_pane(tmux_session: str, target: str) -> str | None:
    """Read-only snapshot of one tmux pane; None on any tmux failure.

    Read-only on purpose: the busy/idle measurement never mutates the pane,
    and a test that reaches a real pane is the falsifier — the suite's tmux
    guard routes every tmux call to a fake.

    `-J` (tmux 3.1+): JOIN soft-wrapped lines, so a line the box wrapped
    across display rows comes back as ONE row and the ownership region
    carries no soft-wrap at all (hypothesis:l4-rendered-line-ownership-
    tolerates-the-wrap). The live capture passes `-J` unconditionally;
    `_region_join_wrap` is still applied to EVERY capture by the ownership
    match and simply collapses any wrap it finds (a no-wrap line yields one
    row and is unaffected).
    """
    try:
        cp = subprocess.run(["tmux", "capture-pane", "-p", "-J", "-t", target],
                            capture_output=True, text=True, timeout=5)
        if cp.returncode != 0:
            return None
        return cp.stdout
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def _registry_status(pid: str | int | None) -> str | None:
    """`busy` | `idle` | None from the Claude Code session registry
    `~/.claude/sessions/<pid>.json`, when the seat row carries a pid — the
    cleaner busy signal than capture-pane, used when present."""
    if not pid:
        return None
    try:
        p = (Path(os.path.expanduser("~")) / ".claude" / "sessions"
             / f"{pid}.json")
        if not p.is_file():
            return None
        st = json.loads(p.read_text()).get("status")
        return st if st in ("busy", "idle") else None
    except Exception:                                    # noqa: BLE001
        return None


def _input_region(pane: str | None) -> str:
    """The INPUT-LINE region of a capture: from the LAST prompt-marker line
    (the `\u276f` prompt glyph that heads the Claude Code input box) to the
    end, inclusive. Everything ABOVE the box -- a SUBMITTED token echoed in
    the transcript, an old `esc to interrupt` scrolled up -- is transcript
    and must not read as stranded/busy (hypothesis:l4-a-nudge-is-a-wake-
    token-not-a-message, residue 2). When no prompt glyph is found (a busy
    pane renders the spinner in place of the box) the whole capture IS the
    region -- conservative."""
    lines = (pane or "").splitlines()
    for i in range(len(lines) - 1, -1, -1):
        if "\u276f" in lines[i]:
            return "\n".join(lines[i:])
    return pane or ""


def _region_join_wrap(region: str) -> list[str]:
    """Two candidate reconstructions of the input region with any tmux
    SOFT-WRAP collapsed. The box splits a line wider than the pane across
    display rows (the measured sanctuary-director pane is 104 columns; the
    test fixture pane is 80), so a `own_line in region` membership test reads
    OUR OWN wrapped stranded line as FOREIGN -- the `\n` tmux inserts at the
    wrap column breaks the substring mid-line and the own line is re-deferred
    forever (hypothesis:l4-rendered-line-ownership-tolerates-the-wrap).
    Collapse the display rows back toward one logical line: strip each row's
    trailing whitespace, strip the first row's prompt glyph and leading
    whitespace, strip every other row's leading box/continuation whitespace.
    The box DROPS the whitespace at a WORD-boundary wrap (the break's space
    is consumed), so a word-wrapped line reconstructs by joining the rows
    with ONE SPACE; a CELL wrap in the MIDDLE of a word leaves no whitespace
    at the break, so it reconstructs only by joining with NOTHING. Try BOTH
    joins and return both reconstructions (deduplicated); a membership test
    accepts the line if it sits in EITHER, so both a word wrap and a real
    tmux cell wrap are recognised. A line that did not wrap yields the same
    row for both (the prompt glyph aside). The LIVE capture passes `-J` and
    therefore ships no soft-wrap at all, but this helper is applied to EVERY
    capture the ownership match takes -- not as the fallback for a no-`-J`
    case -- and collapses any wrap it finds; a no-wrap line is a no-op here.
    A multi-logical-line region is joined too; acceptable,
    because ownership only asks whether our rendered line's characters, in
    order, sit in the box, and the rendered line carries the `[nudge:
    <sender>]:` head that discriminates one sender's line from another's
    (clause (a) still holds: a DIFFERENT body's line does not share our
    body's characters)."""
    rows: list = []
    for i, raw in enumerate((region or "").splitlines()):
        ln = raw.rstrip()
        if i == 0:
            # the prompt glyph heads the first row of the input box
            ln = ln.lstrip().lstrip("\u276f").lstrip()
        else:
            ln = ln.strip()
        if ln:
            rows.append(ln)
    candidates: list = []
    for join in (" ", ""):
        joined = join.join(rows)
        if joined not in candidates:
            candidates.append(joined)
    return candidates


def _nudge_coalesce_reason(pane: str | None, token: str,
                           registry: str | None) -> str | None:
    """Coalescing reason when the pane must not be typed into right now: the
    pane is busy (a Claude Code mid-turn spinner), or the token already sits
    unsubmitted in the pane's input line (already queued). None = nudge now.

    Both checks are scoped to the INPUT REGION (`_input_region`), never the
    whole capture -- a submitted token echoed in the transcript, or an old
    `esc to interrupt` scrolled up, must not read as stranded/busy and cost
    a wake until it scrolls off."""
    if registry == "busy":
        return "pane busy (registry)"
    if pane is not None:
        region = _input_region(pane)
        if "esc to interrupt" in region.lower():
            return "pane busy (spinner)"
        # RESIDUE A (L4.140): ANY stranded nudge-shaped line in the box
        # blocks a send -- not only the head of the exact line being typed.
        # The inline dm line carries the sender (`[nudge: <from>]:`), so a
        # retry whose text is a DIFFERENT nudge shape used to fail the old
        # head-equality match and TYPE INTO A NON-EMPTY BOX; the separate
        # Enter then submitted BOTH lines as one user turn (the owner's
        # 2026-09-11 defect). `_stranded_in_region` covers the inline line,
        # the `[agi-nudge]` wake token, AND rotate.py's `[rotation-alert]`,
        # so a stranded one of ANY shape is never typed after. The box WRAPS
        # a line wider than the pane (the 101-char token sat unsubmitted
        # across two lines at 02:38Z); the per-line head scan still sees it.
        if _stranded_in_region(region) is not None:
            return "token already unsubmitted"
    return None


def _list_windows(tmux_session: str) -> list:
    try:
        listing = subprocess.run(
            ["tmux", "list-windows", "-t", tmux_session,
             "-F", "#{window_name}"],
            capture_output=True, text=True, timeout=5,
        )
        if listing.returncode != 0:
            return []
        return [ln.strip() for ln in listing.stdout.strip().splitlines()
                if ln.strip()]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []


def _window_listed(tmux_session: str, name: str) -> bool:
    return name in _list_windows(tmux_session)


def _window_id_listed(tmux_session: str, wid: str) -> bool:
    """True when the tmux window `@id` (`wid`, e.g. `@267`) is a CURRENT
    window of the session -- judged by `#{window_id}`, never by window name
    (clause (3) of hypothesis:l4-wake-repair-is-quiet-honest-and-readable: a
    stale @id from a reaped/rotated seat row must be detected and repaired,
    not swallowed inside `tmux send-keys`)."""
    try:
        listing = subprocess.run(
            ["tmux", "list-windows", "-t", tmux_session,
             "-F", "#{window_id}"],
            capture_output=True, text=True, timeout=5,
        )
        if listing.returncode != 0:
            return False
        return wid in [ln.strip() for ln in listing.stdout.splitlines()
                       if ln.strip()]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _nudge_target(root: Path, to: str, tmux_session: str | None,
                  repair_stale_id: bool = False,
                  ) -> tuple[str, object, str] | None:
    """Resolve the send-keys target a seat's wake lands in, exactly as
    `_nudge_window` uses it, so a silent re-check (`wake`) and the delivery
    path share ONE address resolution (hypothesis:l4-a-stranded-nudge-is-
    resubmitted-by-typing-not-enter). Returns `(target, pid, tmux_session)`
    or None when the seat has no addressable window: a NAME-addressed row is
    refused (a predecessor/namesake could occupy it) and a windowless
    (ephemeral) recipient may not be nudged by name unless actually listed.

    CLAUSE (3) (hypothesis:l4-wake-repair-is-quiet-honest-and-readable): an
    @id target is trusted ONLY while it is still a LISTED window. A stale @id
    (the row's window was reaped/rotated away) would fail inside
    `tmux send-keys -t session:@id` and the failure is swallowed -- a wake
    addressed to it returns with no line and the seat is never woken. When
    `repair_stale_id=True` (the `wake` verb passes it; the ordinary send/dms
    leave a stale @id alone -- best-effort nudge, unchanged) a stale @id
    prints a `wake repair:` line and FALLS BACK to the by-name lookup below,
    the same `_window_listed` path a name-addressed row uses.
    """
    rows = _locally_loaded_rows(root)
    row = _seat_row_by_name(rows, to)
    window_ref = (row or {}).get("window")      # e.g. "@267", a NAME, or None
    pid = (row or {}).get("pid")
    if tmux_session is None:
        import rotate  # lazy: same bin dir, DEFAULT_TMUX_SESSION lives there
        tmux_session = rotate.DEFAULT_TMUX_SESSION
    if window_ref and str(window_ref).startswith("@"):
        # CLAUSE (3): an @id is only a live target while it is a CURRENT
        # window; a stale one is named, then repaired by name below.
        if repair_stale_id and not _window_id_listed(
                tmux_session, str(window_ref)):
            print(f"wake repair: {to} row window {window_ref} is gone; "
                  f"falling back to name", file=sys.stderr)
            window_ref = None
    elif window_ref:
        # Residue 1 (hypothesis:l4-a-nudge-is-a-wake-token-not-a-message): a
        # row whose `window` cell is a NAME -- not an @id -- must be REFUSED
        # as a target: never send-keys into a name-addressed window the row
        # was supposed to carry as an @id (a predecessor or a namesake could
        # occupy it). Refuse, print the reason on stderr, and FALL BACK to
        # the by-name listing below.
        print(f"nudge: row for {to} carries window {window_ref!r} -- a NAME,"
              f" not an @id; refusing it as a target, falling back to the"
              f" window NAME", file=sys.stderr)
        window_ref = None
    # a name fallback (row has no window at all, or the @id/NAME above was
    # refused) must still be a real listed window — a windowless
    # (ephemeral/fire-and-forget) recipient is untouched, as before.
    if window_ref:
        target = f"{tmux_session}:{window_ref}"
    else:
        if not _window_listed(tmux_session, to):
            return None
        target = f"{tmux_session}:{to}"
    return (target, pid, tmux_session)


def _nudge_window(root: Path, to: str, tmux_session: str | None = None,
                 sender: str | None = None,
                 body: str | None = None,
                 repair_stale_id: bool = False,
                 resolved: tuple | None = None) -> bool:
    """Fire ONE fixed wake token (never the message body) at a perpetual
    seat's tmux window (hypothesis:l4-a-nudge-is-a-wake-token-not-a-message).

    (1) TYPES A TOKEN, not the body: the only variable part is the seat name.
    (2) IDEMPOTENT UNDER BUSY: a busy pane, or a pane already holding the
        token unsubmitted, receives nothing and a `nudge: coalesced` line
        goes to stderr; at most ONE token per unread batch (per-seat marker).
    (3) ADDRESSES BY @id: the recipient's config:seats row `window` (@id) is
        the send-keys target; the window NAME is used only when the row
        carries no window; a send-key is never addressed by name to a window
        a name-matched predecessor or namesake could occupy.
    Best-effort: a missing row/window/session/tmux is a silent no-op; never
    raises. read-only (capture-pane) only — never send-keys into a pane a
    test has not faked.
    """
    if resolved is not None:
        target, pid, tmux_session = resolved
    else:
        resolved = _nudge_target(root, to, tmux_session,
                                 repair_stale_id=repair_stale_id)
        if resolved is None:
            return False
        target, pid, tmux_session = resolved
    # A DM's pending-coalesced count (read now so the delivered/coalesced
    # decision knows whether to carry a `(+N more, read <seat>)` tail). An
    # inbox send never reads it. A DM types the INLINE pane line
    # `[nudge: <from>]: <body>` (hypothesis:l4-the-nudge-carries-the-dm-body-
    # inline); an inbox send keeps the fixed wake token.
    # A DM types the INLINE pane line `[nudge: <from>]: <body>`
    # (hypothesis:l4-the-nudge-carries-the-dm-body-inline); an inbox send
    # keeps the fixed wake token -- UNLESS a dm deferred under a busy pane,
    # in which case the retry (body=None) delivers that deferred body INLINE
    # (with the `(+N more, read <seat>)` tail) instead of the wake token.
    deferred = _read_deferred(root, to) if body is None else None
    delivering_deferred = (body is None and deferred is not None)
    if body is not None:
        more = _pending_more(root, to)
        text = _nudge_line(to, sender or "unknown", body, more)
    elif delivering_deferred:
        # CLAUSE (b): this is an inbox `send()` (body=None) retrying while a
        # deferred dm body is stored. The typed line is the DEFERRED body's
        # inline line, so the inbox message's OWN wake would otherwise be
        # swallowed -- the recipient is never told a new unread inbox message
        # waits. Carry a tail naming the unread inbox on the same delivered
        # line (hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake).
        more = _pending_more(root, to)
        d_sender = deferred.get("sender") or "unknown"
        d_body = deferred.get("body") or ""
        text = _nudge_line(to, d_sender, d_body, more,
                           trailing=_NUDGE_INBOX_TAIL.format(seat=to))
        # The render count is NOT recorded here. It is recorded only after
        # the line is actually TYPED into the pane (below), so a render that
        # never reaches the pane (coalesce-window, busy, literal-send
        # failure, or `text is None`) must not move the stored count -- a
        # strand left by a PRIOR delivery is judged against the count that
        # delivery rendered with (hypothesis:l4-deferred-ownership-uses-the-
        # rendered-count, residue: a render that does not type must not
        # overwrite the stored count).
    else:
        text = _build_nudge_token(to)
    if text is None:
        # `_nudge_line` found no tail leaving room for a single body
        # character (a pathological sender/seat whose prefix eats the whole
        # budget): never type a zero-body line -- defer the dm for a later
        # retry (hypothesis:l4-ownership-matches-the-rendered-line-and-zero-
        # body-retreats). Zero-body delivery is unreachable.
        if body is not None:
            if not _store_deferred(root, to, sender or "unknown", body):
                _bump_pending(root, to)
        print("nudge: deferred (no room to render the body inline)",
              file=sys.stderr)
        return False
    # (2) cap: one token per unread batch; a batch of dms yields one token.
    last_age = _last_nudge_age(root, to)
    if last_age is not None and last_age < _NUDGE_COALESCE_WINDOW_S:
        # A DM coalesced inside the window is counted, not typed -- the NEXT
        # delivered nudge carries `(+N more, read <seat>)`.
        if body is not None:
            _bump_pending(root, to)
        print(f"nudge: coalesced (already nudged within "
              f"{int(_NUDGE_COALESCE_WINDOW_S)}s)", file=sys.stderr)
        return False
    # (2) busy / already-queued coalescing. Measure read-only, never send.
    pane_capture = _capture_pane(tmux_session, target)
    reason = _nudge_coalesce_reason(pane_capture, text,
                                    _registry_status(pid))
    if reason == "token already unsubmitted":
        # Probe (C): a line STRANDED in an idle pane (typed by the old
        # one-call shape, by a `-l` call whose Enter never came, or left by
        # rotate.py) is submitted by a later bare Enter. Without this an idle
        # pane holding a stranded line coalesces every later send forever
        # (the marker is never stamped, the pane never changes) and the seat
        # is never woken. The busy checks come first in
        # _nudge_coalesce_reason, so this Enter never lands in a mid-turn
        # pane. Residue A (L4.140): a stranded line of ANY shape is detected
        # (never only the head of the line being typed), so the Enter submits
        # WHATEVER nudge line sits in the box and we NEVER type a second line
        # after it (a concatenated box submitted as one user turn is the
        # owner's 2026-09-11 defect).
        #: hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter:
        #: the stranded-line retry TYPES a printable space then Enter in a
        #: SEPARATE call -- never a bare Enter-only resubmit. The owner's
        #: 2026-09-11 defect was typing a SECOND nudge line onto a stranded
        #: one and submitting a concatenated box as one user turn; a single
        #: space appends ONE printable char to the EXISTING stranded line
        #: (never a second line), then Enter submits it. Two calls (probes
        #: A-D: never `text Enter` in one chunk). The master-sensei pane the
        #: target measured does NOT submit on a bare Enter (three failed
        #: 13:59Z/14:00Z/14:04Z) but does on type+Enter; the prime's probe-(C)
        #: pane was a DIFFERENT pane shape -- the typed resubmit satisfies
        #: both.
        #
        # Residue B (L4.140, F1: a marker records only a DELIVERY): a deferred
        # body / pending is cleared ONLY when a line CARRYING it was actually
        # submitted -- the plain delivery path, or a stranded line that IS
        # the deferred body's own line. If the stranded line is a DIFFERENT
        # line, our text did NOT reach the pane: carry it on a later retry
        # (store/keep the deferred body) and never clear it here. Old bytes
        # ran `_clear_deferred` unconditionally, dropping a deferred body that
        # had never touched the pane.
        region = _input_region(pane_capture)
        # CLAUSE (a): for an inline DM the head (`[nudge: <from>]:`) identifies
        # only the SENDER, and every dm from that sender shares it -- a stranded
        # line left by an EARLIER same-sender dm (different body) used to read
        # as "ours", so the new body was Entered-and-cleared and never typed
        # nor deferred (lost until the next wake). The head alone is not proof
        # our SPECIFIC body reached the pane: for an inline body (a dm, or a
        # deferred dm delivery) it must be SHOWN in the pane too before the
        # stranded line counts as ours. A bare inbox wake token has no body and
        # keeps the head-only match.
        body_for_match = body if body is not None else (d_body if delivering_deferred else None)
        if body_for_match is not None:
            # CLAUSE (d) (hypothesis:l4-ownership-matches-the-rendered-line-
            # and-zero-body-retreats): the pane holds the RENDERED line, not
            # the raw body. A body truncated to the cap (with a `… (read
            # <seat>)` / `(+N more)` tail) or flattened (newlines -> ` / `)
            # never appears verbatim in `region`, so `body_for_match in
            # region` misread our OWN stranded line as foreign and re-deferred
            # it forever. Compare region against the line this body RENDERS
            # (the same _nudge_line flatten + truncation), so a truncated /
            # flattened own line is recognised as ours and submitted (by the
            # typed resubmit -- one space + a separate Enter, never Enter-only).
            # For a DIRECT dm that line IS `text`.
            if body is not None:
                own_candidates = [text]
            else:
                # A DEFERRED delivery: `text` is the TAILED render of THE
                # CURRENT retry (count tail + `(+unread inbox...)` tail), but a
                # stranded line left by an EARLIER deferred delivery was typed
                # at ITS OWN render -- and for a body long enough to truncate
                # the tailed render is SHORTER than the untailed one (the tail
                # is counted INSIDE `_NUDGE_LINE_MAX`), so `text` / a single
                # untailed `own_line` read that own TAILED truncated strand as
                # foreign and the body was typed AGAIN on the next wake
                # (hypothesis:l4-a-truncated-deferred-body-delivers-once). Try
                # BOTH renderings the body can have -- the no-tail render and
                # the inbox-tail render -- at the RECORDED count. A record WITH
                # a recorded count is judged at exactly that count; a record
                # WITHOUT one (stored by `_store_deferred` and never rendered,
                # or written before L4.222) is matched against every render the
                # strand could have carried -- each count 0..pending, tailed
                # and untailed -- so a count that drifted since the strand was
                # typed still recognises its own line (the SECOND HALF). Never
                # widened to the head alone, so a same-sender DIFFERENT body's
                # strand still reads FOREIGN (hypothesis:l4-send-py-same-sender-
                # stranded-line-and-the-swallowed-wake, clause (a)).
                rec = (deferred or {}).get("more")
                counts = (rec,) if rec is not None \
                    else tuple(range(0, more + 1))
                _inbox_tail = _NUDGE_INBOX_TAIL.format(seat=to)
                own_candidates = []
                for k in counts:
                    own_candidates.append(
                        _nudge_line(to, d_sender, d_body, k))
                    own_candidates.append(
                        _nudge_line(to, d_sender, d_body, k,
                                    trailing=_inbox_tail))
            # hypothesis:l4-rendered-line-ownership-tolerates-the-wrap: the
            # box WRAPS a line wider than the pane across display rows, so
            # `own_line in region` reads our OWN wrapped stranded line as
            # foreign and re-defers it forever (the wrap-inserted `\n` breaks
            # the substring). The live capture passes `-J` so a real region
            # carries no soft-wrap; a captured region that has any wrap left
            # (executed WITHOUT `-J`) is collapsed first (join the rows, drop
            # the wrap-inserted whitespace, trying BOTH a word-boundary join
            # and a mid-word cell join) -- then test membership against every
            # candidate render, so a wrapped own line at any of its render
            # counts is still recognised.
            our_line_was_stranded = any(
                own in r
                for r in _region_join_wrap(region)
                for own in own_candidates)
        else:
            our_line_was_stranded = _nudge_token_head(text) in region
        #: the typed resubmit (a space typed into the existing stranded line,
        #: then a SEPARATE Enter) -- the same ownership judgement, a different
        #: retry shape (hypothesis:l4-a-stranded-nudge-is-resubmitted-by-
        #: typing-not-enter). Never `text Enter` in one chunk (paste
        #: heuristic, probes A-D); the space's own `-l` call plus the Enter
        #: call are two tmux invocations.
        if not _send_keys(target, " ", literal=True):
            return False
        if not _send_keys(target, "Enter"):
            return False
        print("nudge: submitted a stranded token (typed)",
              file=sys.stderr)
        if our_line_was_stranded:
            # the stranded line WAS ours -> a real delivery; record + clear
            _record_nudge(root, to)
            if body is not None or delivering_deferred:
                _clear_pending(root, to)
            _clear_deferred(root, to)
        elif body is not None:
            # our dm line never reached the pane (a different line did);
            # carry our body on a later idle retry -- never lose it.
            if not _store_deferred(root, to, sender or "unknown", body):
                _bump_pending(root, to)   # a later dm: +N more
            # a deferred body that is a DIFFERENT line stays stored (above
            # elif body is None skips clearing it) for that later retry.
        return True
    if reason:
        # F1 (hypothesis:l4-a-nudge-is-a-wake-token-not-a-message): this
        # batch was NOT typed into the pane. NEVER stamp the marker here --
        # a busy/queued coalesce that records itself as a delivered token
        # suppresses the later send once the pane goes idle, and the message
        # is never woken. The marker records only a DELIVERED token.
        # A DM coalesced under busy is DEFERRED (the first body stored, a
        # later one counted) so an idle retry still carries it INLINE.
        if body is not None:
            if not _store_deferred(root, to, sender or "unknown", body):
                _bump_pending(root, to)   # a later dm in the batch: +N more
        print(f"nudge: coalesced ({reason})", file=sys.stderr)
        return False
    # (4) THE SHAPE, pinned by the prime on a real Claude Code pane (nudge
    # node 83fe8049c, four probes): (A) short text + Enter in ONE send-keys
    # call is delivered, (B) a long chunk + Enter in ONE call is taken for a
    # PASTE -- the Enter becomes a newline and the text sits stranded (every
    # alarm dm of 2026-09-10), (C) a later bare Enter submits it, (D) the
    # text as a LITERAL (`-l`) in one call, a pause, then Enter as a
    # SEPARATE call is delivered. So: never `text Enter` in one call.
    if not _send_keys(target, text, literal=True):
        # Nothing typed; do not mark delivered, so a retry is not suppressed
        # (F1, same rationale). A deferred render count is NOT recorded here
        # either: a failed literal send means the line never reached the pane
        # and must not move the stored count.
        return False
    if delivering_deferred:
        # The deferred body's line is now TYPED into the pane. Record the
        # count THIS typing rendered with, so a later retry judges the strand
        # this delivery may leave (Should the Enter below fail) against THAT
        # render -- not the (possibly changed) current pending, and not a
        # count from an intervening render that never typed
        # (hypothesis:l4-deferred-ownership-uses-the-rendered-count). The
        # record is a no-op on every non-typing path above. A prior record
        # with no `more` key stays, and falls back to the current count.
        _record_deferred_render(root, to, more)
    time.sleep(_NUDGE_ENTER_DELAY_S)
    if not _send_keys(target, "Enter"):
        # The text sits unsubmitted; the next send finds it by its head and
        # takes the probe-(C) path above. Not delivered yet: no marker.
        return False
    _record_nudge(root, to)
    if body is not None or delivering_deferred:
        _clear_pending(root, to)
    _clear_deferred(root, to)
    return True


def _seat_has_pending(root: Path, to: str) -> bool:
    """Anything the wake token should announce or a stranded line should
    deliver for the seat: unread inbox blocks, a stored deferred dm, or a
    coalesced pending count. Used to stop `wake` spraying a bare wake token
    at an IDLE seat that has nothing -- heal polls every seat every pass, so
    an ungated retype would issue a token every poll once the coalesce window
    lapses (hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-
    enter)."""
    try:
        blocks, _ = _scan_messages(_inbox_path(root, to))
        if blocks:
            return True
    except Exception:                                    # noqa: BLE001
        pass
    try:
        if _pending_more(root, to) > 0:
            return True
    except Exception:                                    # noqa: BLE001
        pass
    return _read_deferred(root, to) is not None


def _nudge_announced_path(root: Path, seat: str) -> Path:
    """Sidecar next to the nudge marker recording the identity of the unread
    state the last wake token was typed FOR (clause (1) of hypothesis:l4-wake-
    repair-is-quiet-honest-and-readable: at most ONE token per unread state).
    Kept SEPARATE from `_nudge_marker_path` (`{seat}.nudge`), whose `<ts>`
    shape other paths and tests read and must not change."""
    return _inbox_dir(root) / f"{seat}.nudge.announced"


def _announced_digest(root: Path, seat: str) -> str | None:
    """The digest of the unread state `wake` last announced for the seat, or
    None when no wake has typed a token yet."""
    try:
        p = _nudge_announced_path(root, seat)
        return p.read_text().strip() or None
    except Exception:                                    # noqa: BLE001
        return None


def _record_announced(root: Path, seat: str, digest: str) -> None:
    """Stamp the announced-state sidecar after a wake token is actually
    TYPED for a NEW unread state; best-effort, never raises."""
    try:
        p = _nudge_announced_path(root, seat)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(digest)
    except OSError:
        pass


def _clear_announced(root: Path, seat: str) -> None:
    """Drop the announced-state sidecar when the seat's unread is consumed
    (a read moves the marker, so a later NEW state must not look already-
    announced). Best-effort, never raises."""
    try:
        p = _nudge_announced_path(root, seat)
        if p.exists():
            p.unlink()
    except OSError:
        pass


def _unread_digest(root: Path, seat: str) -> str:
    """Identity of the seat's current announce state: the unread inbox text
    (after any read marker), the pending-coalesced count, and whether a
    deferred dm body waits. `wake` records this after typing a token and stays
    quiet on a later pass whose digest is unchanged (clause (1)): healing polls
    every seat every pass, so an unchanged unread inbox would otherwise retype
    the token once the 30s `_NUDGE_COALESCE_WINDOW_S` lapses."""
    text = ""
    try:
        inbox = _inbox_path(root, seat)
        if inbox.is_file():
            raw = inbox.read_text()
            lines = raw.splitlines(keepends=True)
            for i, ln in enumerate(lines):
                if ln == READ_MARKER:
                    raw = "".join(lines[i + 1:])
                    break
            text = raw
    except Exception:                                    # noqa: BLE001
        pass
    blob = "\x00".join((text, str(_pending_more(root, seat)),
                        "1" if _read_deferred(root, seat) else "0"))
    return hashlib.sha256(blob.encode("utf-8", "replace")).hexdigest()


def _wake_outcome(outcome: str, delivered: bool) -> bool:
    """Print the ONE outcome line for the `wake` verb and return the delivery
    truth (True = a token/strand/deferred actually reached the pane, so the
    exit code is 0; False = nothing delivered, exit 1). The line is exactly one
    of: typed-token | resubmitted-strand | delivered-deferred | busy-deferred
    | nothing-pending | no-target (clause (2) of hypothesis:l4-wake-repair-is-
    quiet-honest-and-readable)."""
    print(outcome)
    return delivered


def wake(root: Path, to: str, tmux_session: str | None = None) -> bool:
    """Re-check ONE seat and resubmit / deliver a wake when there is
    something to deliver (hypothesis:l4-a-stranded-nudge-is-resubmitted-by-
    typing-not-enter, extended by hypothesis:l4-wake-repair-is-quiet-honest-
    and-readable for clauses (1)-(3)). Called by rotate.py's
    `_announce_rotation` right after the alert and by heal.py's watch pass
    for every live seat row each poll.

    READ-ONLY until it has something to do:
      - pane IDLE with a stranded nudge-shaped line -> the shared
        `_nudge_window` path resubmits it by TYPING (space + Enter, never
        Enter-only) and judges ownership on the rendered line as one delivery;
      - pane IDLE, no strand, but the seat has unread/pending/deferred and
        that state was NOT already announced -> the ordinary waking path
        types the wake token (or delivers a stored deferred dm INLINE);
      - pane BUSY with something pending -> `_nudge_window` coalesces to ONE
        stderr line and does nothing (the deferred record is already written);
      - nothing pending at all -> a silent no-op.
    Address by @id when the row carries one and it is still a LISTED window
    (clause 3: a stale @id prints a `wake repair:` line and falls back to
    name); name fallback only as today.

    Clause (1): at most ONE token per unread state. After typing a token for
    a state, `wake` records the state's digest and stays quiet on a later
    pass over the SAME digest -- the heal polls every seat every pass, so an
    unchanged unread inbox would otherwise retype the token once the 30s
    coalesce window lapses. The seat's own read clears the sidecar.

    Clause (2): prints exactly ONE outcome line and returns True only when
    something actually reached the pane (so `main()` exits 0 only on a
    delivery). heal.py/rotate.py ignore the return value by design.
    """
    resolved = _nudge_target(root, to, tmux_session, repair_stale_id=True)
    if resolved is None:
        return _wake_outcome("no-target", delivered=False)
    target, pid, tms = resolved
    pane = _capture_pane(tms, target)
    reason = _nudge_coalesce_reason(pane, _build_nudge_token(to),
                                    _registry_status(pid))

    # A stranded nudge-shaped line in the pane is delivered (resubmitted by
    # TYPING) regardless of pending -- the resubmit itself IS the wake.
    if reason == "token already unsubmitted":
        ok = _nudge_window(root, to, tmux_session=tms, repair_stale_id=True, resolved=resolved)
        return _wake_outcome("resubmitted-strand", delivered=ok)

    if not _seat_has_pending(root, to):
        # nothing stranded and nothing pending: never type a bare wake token
        # into a seat with nothing to announce (the heal polls every seat).
        return _wake_outcome("nothing-pending", delivered=False)

    # Clause (1): never retype a token for an unread state we already
    # announced. The 30s `_NUDGE_COALESCE_WINDOW_S` alone would let an
    # unchanged unread inbox retype once it lapses under heal's every-seat
    # polling; the digest gate stops that for as long as the state is unchanged.
    digest = _unread_digest(root, to)
    if _announced_digest(root, to) == digest:
        return _wake_outcome("nothing-pending", delivered=False)

    if reason is not None:
        # Pane busy / spinner with something pending: nothing typed. The
        # deferred record is already written; `_nudge_window` prints its own
        # coalesced line, this wake prints its ONE outcome.
        _nudge_window(root, to, tmux_session=tms, repair_stale_id=True, resolved=resolved)
        return _wake_outcome("busy-deferred", delivered=False)

    # Pane IDLE with a NEW unread state: type the wake token, or deliver the
    # stored deferred dm INLINE when one waits (read before `_nudge_window`
    # clears it).
    delivering_deferred = _read_deferred(root, to) is not None
    ok = _nudge_window(root, to, tmux_session=tms, repair_stale_id=True, resolved=resolved)
    if ok:
        _record_announced(root, to, digest)
        return _wake_outcome("delivered-deferred" if delivering_deferred
                             else "typed-token", delivered=True)
    # A delivery was attempted but nothing reached the pane (e.g. the 30s
    # window caught it); `_nudge_window` already printed its own line.
    return _wake_outcome("nothing-pending", delivered=False)


def _send_keys(target: str, *keys: str, literal: bool = False) -> bool:
    """One `tmux send-keys` call; False on any failure. `literal=True` types
    the keys as text (`-l`) — no key-name parsing, no Enter."""
    argv = ["tmux", "send-keys"]
    if literal:
        argv.append("-l")
    argv += ["-t", target, *keys]
    try:
        cp = subprocess.run(argv, capture_output=True, text=True, timeout=5)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
    return cp.returncode == 0


# ── verbs ─────────────────────────────────────────────────────────────────


def send(root: Path, to: str, text: str, sender: str | None) -> None:
    """Append one message block to the recipient's inbox.

    Signs the message -- one ``sig: <scheme>:<fingerprint>:<sig_hex>`` line
    after ``to:`` -- IFF ``<sessions>/seats/<from_id>.key`` exists. Without a
    key the block is byte-identical to the unsigned form (every existing
    test_send.py test stays green untouched). The signed bytes are exactly
    ``ts\nfrom\nto\n\ntext`` (:func:`_canonical_msg`).
    """
    inbox = _inbox_path(root, to)
    inbox.parent.mkdir(parents=True, exist_ok=True)

    ts = _now()
    from_id = _detect_sender(sender)
    sig_line = _sign_line(root, from_id, ts, to, text)
    head = f"{MSG_SEP}ts: {ts}\nfrom: {from_id}\nto: {to}\n"
    if sig_line is not None:
        head += sig_line + "\n"
    block = head + f"\n{text}\n"

    with open(inbox, "a") as f:
        f.write(block)

    # Best-effort wake-token nudge into a perpetual seat's window; a no-op
    # for windowless (ephemeral) recipients. One fixed token only — never the
    # body (hypothesis:l4-a-nudge-is-a-wake-token-not-a-message).
    _nudge_window(root, to)

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


def _parse_block(block: str) -> tuple[dict, str]:
    """Split one block into (header_meta, text).

    The header is the ``key: value`` lines up to the first blank line
    (``ts``/``from``/``to`` and, when signed, ``sig``); ``text`` is everything
    after the blank line, reassembled line-for-line (the exact inverse of the
    writer's ``\n
{text}\n``). A block without the empty separator line (no
    text) yields an empty text.
    """
    body = block[len(MSG_SEP):] if block.startswith(MSG_SEP) else block
    lines = body.splitlines()
    meta: dict = {}
    i = 0
    while i < len(lines) and lines[i] != "":
        line = lines[i]
        if ": " in line:
            k, _, v = line.partition(": ")
            meta[k] = v
        elif ":" in line:
            k, _, v = line.partition(":")
            meta[k] = v.lstrip()
        i += 1
    text = "\n".join(lines[i + 1:])
    return meta, text


def _seat_row_in(rows: list, from_id: str) -> dict | None:
    """The config:seats row whose identity is ``from_id``. Identity mirrors
    whois's resolver: a row's ``name``, its ``session_ref``, or a
    ``session_id`` uuid PREFIX of at least WHOIS_MIN_SESSION_ID_PREFIX chars.
    Returns None when no row matches."""
    for r in rows:
        if r.get("name") == from_id or r.get("session_ref") == from_id:
            return r
        if (from_id and len(from_id) >= WHOIS_MIN_SESSION_ID_PREFIX
                and (r.get("session_id") or "").startswith(from_id)):
            return r
    return None


def _load_rows(root: Path) -> list | None:
    """The seat rows, through the SAME resolver whois uses: the PUSHED ref
    first, then the working-tree rows as the fallback. Returns None when
    neither yields any rows -- a reader then labels any sig FORGED rather
    than guessing."""
    seeded = _pushed_seats(root, _PUSHED_SEATS, True)
    if seeded is not None:
        rows, _sha = seeded
        return rows or None
    rows = _locally_loaded_rows(root)
    return rows or None


def _verify_block(root: Path, rows: list | None,
                  meta: dict, text: str) -> str:
    """The ONE label line for a block: VERIFIED / UNSIGNED / FORGED.

    ``VERIFIED <seat> (<scheme>)`` when a ``sig`` line is present and verifies
    against the from-seat's row (pubkey + sig_scheme matched); ``UNSIGNED``
    when there is no sig line; ``FORGED`` when a sig is present and fails any
    check (bad shape, unknown scheme, unknown sender, a row with no
    pubkey/sig_scheme, a scheme the row does not name, or a signature that
    does not verify). The label is NEVER a drop -- the caller prints the block
    in full under all three.
    """
    sig = meta.get("sig")
    if not sig:
        return "UNSIGNED"
    try:
        sig_scheme, fp, sig_hex = sig.split(":", 2)
        sig_bytes = bytes.fromhex(sig_hex)
    except (ValueError, TypeError):
        return "FORGED"
    if rows is None:
        return "FORGED"
    row = _seat_row_in(rows, meta.get("from", ""))
    if row is None:
        return "FORGED"
    row_scheme = row.get("sig_scheme") or ""
    row_pub = row.get("pubkey") or ""
    if not row_scheme or not row_pub:
        return "FORGED"
    # a sig under a scheme the row does not name is a forgery, even if the
    # bytes happen to be signed with something -- the row declares what it
    # will accept.
    if row_scheme != sig_scheme:
        return "FORGED"
    try:
        scheme = seatsig.get(sig_scheme)
        pub = bytes.fromhex(row_pub)
    except Exception:                                              # noqa: BLE001
        return "FORGED"
    msg = _canonical_msg(meta.get("ts", ""), meta.get("from", ""),
                         meta.get("to", ""), text).encode()
    if not scheme.verify(pub, msg, sig_bytes):
        return "FORGED"
    return f"VERIFIED {row.get('name', meta.get('from', '?'))} ({sig_scheme})"


def _labels_for_blocks(root: Path, blocks: list[str]) -> list[str]:
    """The label lines for a batch of blocks, one per block.

    Rows are resolved ONCE for the batch (pushed-then-local) and only when at
    least one block carries a sig line -- an all-unsigned inbox never touches
    git, so a batch read of ordinary mail stays network-free.
    """
    parsed = [_parse_block(b) for b in blocks]
    rows = None
    if any("sig" in m for m, _t in parsed):
        rows = _load_rows(root)
    return [_verify_block(root, rows, m, t) for m, t in parsed]


def _print_blocks_with_labels(root: Path, blocks: list[str]) -> None:
    """Print one label line before each block, then the block in FULL."""
    labels = _labels_for_blocks(root, blocks)
    for i, block in enumerate(blocks):
        if i > 0:
            print(MSG_SEP, end="")
        print(labels[i])
        print(block, end="")


def _deferred_stamp(root: Path, me: str, deferred: dict) -> str:
    """A display timestamp for a stored deferred dm: the record's own `ts`
    when one exists, else the sidecar's mtime (a record stored by the live
    path carries no `ts`). UTC, HH:MM with a Z, like the nudge stream."""
    ts = deferred.get("ts")
    if ts:
        return str(ts)
    try:
        m = _nudge_deferred_path(root, me).stat().st_mtime
        return datetime.fromtimestamp(m, timezone.utc).strftime("%H:%MZ")
    except OSError:
        return "<unknown ts>"


def _print_deferred_block(root: Path, me: str, deferred: dict) -> None:
    """Print a stored deferred dm as its OWN block, headed
    `deferred dm from <sender> (<ts>)`, so a reader at a seam sees it as a
    thing of its own rather than folded into the inbox stream
    (hypothesis:l4-wake-repair-is-quiet-honest-and-readable, clause 4).
    read-only for the record — the caller chooses whether to clear it."""
    sender = deferred.get("sender") or "unknown"
    print(f"deferred dm from {sender} ({_deferred_stamp(root, me, deferred)})")
    body = deferred.get("body", "") or ""
    if body and not body.endswith("\n"):
        body += "\n"
    print(body, end="")


def read(root: Path, me: str, sender: str | None) -> None:
    """Print unread blocks and mark them read."""
    inbox = _inbox_path(root, me)
    blocks, marker_index = _scan_messages(inbox)
    deferred = _read_deferred(root, me)

    if not blocks and deferred is None:
        print(f"inbox for {me}: empty")
        return

    # A stored deferred dm prints FIRST, before the inbox blocks, and the
    # record is then cleared — a director who never had an idle pane still
    # sees it at a seam, exactly once (clause 4). The record's own
    # delivered-count semantics for the PANE path are untouched
    # (`_clear_deferred` is the same no-op-guarded helper that path uses).
    if deferred is not None:
        _print_deferred_block(root, me, deferred)
        _clear_deferred(root, me)

    # Print inbox blocks, each prefixed by its verification label.
    if blocks:
        _print_blocks_with_labels(root, blocks)

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
    # The seat just consumed its unread (clause (1) of hypothesis:l4-wake-
    # repair-is-quiet-honest-and-readable): drop the announced-state sidecar
    # so a LATER new unread state is never mistaken for one already typed.
    _clear_announced(root, me)


def peek(root: Path, me: str) -> None:
    """Print unread blocks without marking them read."""
    inbox = _inbox_path(root, me)
    blocks, _ = _scan_messages(inbox)
    deferred = _read_deferred(root, me)

    if not blocks and deferred is None:
        print(f"inbox for {me}: empty")
        return

    # peek shows a stored deferred dm WITHOUT clearing it — a seam without
    # the delivered-count side effects of `read` (clause 4).
    if deferred is not None:
        _print_deferred_block(root, me, deferred)

    # Print inbox blocks (peek never marks read).
    if blocks:
        _print_blocks_with_labels(root, blocks)


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
    # Wake nudge of the other party when it exists (silent no-op otherwise),
    # carrying the DM body INLINE as `[nudge: <me>]: <text>` so the
    # recipient sees the message without a `send.py read` round-trip
    # (hypothesis:l4-the-nudge-carries-the-dm-body-inline); idempotent under
    # a busy pane. The body STILL lands in the dm file -- the pane line is
    # delivery, the file is the record.
    _nudge_window(locations.find_project_root(croot) or croot, other,
                  sender=_detect_sender(sender), body=text)
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

#: L4.114 (r3): whois authorizes by a 6-hex ref OR by a PREFIX of a row's
#: `session_id` uuid. A prefix shorter than this is REFUSED (never a guess).
WHOIS_MIN_SESSION_ID_PREFIX = 6


def _resolve_rows(rows: list, session_ref: str,
                  claim: str | None) -> tuple[int, str]:
    """Answer the is-this-who-they-say question for one ref. Two directions:
    with no --claim, name the seat + role the ref belongs to; with
    --claim NAME, answer whether this ref IS that row (a ref present in the
    table but under a DIFFERENT name/role answers NO — the impersonation case).

    L4.114 (r3): a ref that is not an exact `session_ref` match is still
    authorized when it is a PREFIX of a row's `session_id` uuid, at least
    WHOIS_MIN_SESSION_ID_PREFIX chars — a shorter prefix is refused (never
    treated as a match)."""
    hits = [r for r in rows if r.get("session_ref") == session_ref]
    if not hits:
        # r3: prefix-match a row's session_id uuid (state min length; refuse
        # shorter as NO-MATCH rather than guessing on a too-small prefix).
        if len(session_ref) >= WHOIS_MIN_SESSION_ID_PREFIX:
            hits = [r for r in rows
                    if (r.get("session_id") or "").startswith(session_ref)]
            if not hits:
                return (WHOIS_NO_MATCH,
                        f"NO-MATCH: {session_ref!r} belongs to no seat row "
                        "by session_ref or session_id prefix "
                        f"(min prefix {WHOIS_MIN_SESSION_ID_PREFIX})")
        else:
            return (WHOIS_NO_MATCH,
                    f"NO-MATCH: {session_ref!r} (< "
                    f"{WHOIS_MIN_SESSION_ID_PREFIX} chars) is too short to "
                    "authorize by session_id prefix and matches no "
                    "session_ref")
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

    p_keygen = sub.add_parser(
        "keygen", parents=[common],
        help="mint a seat signing key under <sessions>/seats/<seat>.key (mode "
             "0600); prints the two seat-row cells (pubkey, sig_scheme) and "
             "writes no graph node -- hypothesis:l4-a-seat-signs-with-a-"
             "swappable-scheme")
    p_keygen.add_argument("--seat", required=True, help="seat name")
    p_keygen.add_argument("--scheme", default="ed25519",
                          help="swappable scheme name (default ed25519)")

    p_wake = sub.add_parser(
        "wake", parents=[common],
        help="re-check one seat: resubmit a stranded nudge by typing + Enter"
             " (never Enter-only), or wake an idle pane whose seat has "
             "unread; busy/no-op (hypothesis:l4-a-stranded-nudge-is-"
             "resubmitted-by-typing-not-enter)")
    p_wake.add_argument("target", help="seat name")

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

    if args.verb == "keygen":
        keygen(root, args.seat, args.scheme)
        return 0

    if args.verb == "wake":
        # Clause (2) (hypothesis:l4-wake-repair-is-quiet-honest-and-readable):
        # exit 0 ONLY when the wake actually delivered a token/strand/deferred
        # to a pane; 1 otherwise. heal.py/rotate.py call send.wake() directly
        # and deliberately ignore the value; only this verb path returns it.
        return 0 if wake(root, args.target) else 1

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
