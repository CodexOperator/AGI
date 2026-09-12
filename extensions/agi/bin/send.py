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
import fcntl
import hashlib
import re
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
import geometry_config  # noqa: E402
import branches  # noqa: E402 -- the ONE branch-name grammar (g15 round I)
import reaper_log  # noqa: E402 -- the ONE per-event log resolver, shared with heal.py's _watch_log (clause (3))
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

# The block boundary is the separator IMMEDIATELY followed by a header line
# ("ts:"), never a body line that happens to equal "---" -- a signed body that
# contains a "---" line must stay ONE block, or its own sig reads FORGED on the
# split tail (SL6.06, hypothesis:l4-sign-exactly-the-bytes-the-reader-parses...).
# (?m)^ anchors the separator at a fresh line (blocks are concatenated with a
# trailing \\n, so the next block ALWAYS starts a new line). Only "---\n" is
# consumed; the lookahead requires a FULL header after it (a `ts:` line AND the
# following `from:` line) so the header stays on the block. A signed BODY that
# happens to contain a "---\n" line immediately followed by a body line that
# merely STARTS with "ts: " no longer fragments: without a `from:` after it,
# there is no full header, so it stays ONE block and its own sig reads VERIFIED
# instead of FORGED on a split tail (SL6.06, SL7.02 clause (4)). One canonical
# split used by the inbox scan AND the conversation reader.
_MSG_BOUNDARY_RE = re.compile(r"(?m)^---\n(?=ts: [^\n]*\nfrom: )")

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


def _signing_key_obj(root: Path, seat: str, key_file: Path) -> dict | None:
    """g15.26 (c) -- the signing key dict, with the PENDING-SUCCESSOR
    preference. A `<seat>.key.pending` (persisted by
    rotate._persist_pending_key when a push FAILED after the committed row
    had already been switched to the successor pubkey) whose `pub_hex` EQUALS
    the pubkey the COMMITTED row names for this seat is used to sign: the row
    on origin (once pushed) names exactly that pubkey, so a dm signed with the
    pending successor private key reads VERIFIED, never RETIRED/FORGED,
    across the deferred-swap window (the falsifier of this clause).
    This is a PREFERENCE, not a replacement: when no pending file exists, or
    its pub_hex does NOT match the committed row, or the committed row cannot
    be read, the signer falls back to the live `<seat>.key` and signs EXACTLY
    as before -- a seat with no deferred swap never changes a byte. Returns
    the JSON dict, or None when neither key yields a usable object (the
    caller then emits an unsigned line, as today)."""
    import json as _json
    from pathlib import Path as _Path
    _pend = _Path(key_file).parent / f"{_Path(key_file).name}.pending"
    if _pend.is_file():
        try:
            _pobj = _json.loads(_pend.read_text())
        except (ValueError, OSError):
            _pobj = None
        if _pobj and _pobj.get("pub_hex") and _pobj.get("priv_hex"):
            _committed = _seats_committed_rows(root)
            _row = _seat_row_in(_committed, seat) if _committed else None
            _row_pub = str((_row or {}).get("pubkey") or "")
            if _row_pub and _row_pub == str(_pobj.get("pub_hex")):
                return _pobj
    try:
        return _json.loads(_Path(key_file).read_text())
    except (ValueError, OSError):
        return None


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

    Signs only when `<sessions>/seats/<from_id>.key` exists (a seat that has
    generated a key). When the seat is in the DEFERRED successor swap (a
    `<seat>.key.pending` whose pub_hex matches the COMMITTED row's pubkey),
    the pending successor private key is used (g15.26 (c)) so the dm reads
    VERIFIED against origin's pushed row, never RETIRED/FORGED; otherwise the
    live `<seat>.key` signs exactly as before. The line is
    ``sig: <scheme>:<fingerprint>:<sig_hex>`` -- scheme name, the short
    fingerprint (first 16 hex of sha256 of the public key) for a
    human-readable handle, then the signature hex. The private seed is used
    only to sign, never printed or logged.
    """
    key_file = _seat_key_path(root, from_id)
    if not key_file.is_file():
        return None
    obj = _signing_key_obj(root, from_id, key_file)
    if obj is None:
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


def _graph_root(root: Path) -> Path:
    """The graph root (the `.agi` dir holding config.json) for a given root.

    A G11 project root is the parent of `.agi/`; an already-resolved graph
    root IS the `.agi` dir. ``write.submit`` keys every node path off THIS
    root (write.py `_load_seats` reads `<root>/nodes/.geometry/seats.md`),
    so keygen must hand write.submit the graph root, never the project root.
    """
    if (root / ".agi" / "config.json").is_file():
        return root / ".agi"
    return root


# ── comms reserved config (hypothesis:l4-lockdown-is-a-reserved-boolean...) ──

#: The `comms` config keys this build knows. Every key returns a default when
#: absent -- an absent block is ALL defaults, never an error. `lockdown` is
#: RESERVED this round: `true` warns and encrypts nothing. `verify` is the flip
#: switch of goal:g15.26 -- `informational` (default) prints FORGED blocks and
#: whois answers in full (Prime ruling A, sig never gates the exit);
#: `enforcing` refuses a FORGED label in read/peek and whois --sig (clauses 1
#: and 3). The value must stay `informational` until the named review flips it.
_COMMS_DEFAULTS = {
    "lockdown": False,
    "verify": "informational",
}

#: The one warning printed per send and per read/peek when `lockdown` is set.
#: Words chosen so no cipher is ever named as a STATE -- the flag is reserved,
#: not built (next season, rungs 5-8).
#: Shown in `-h` / `keygen -h` (clause 4 of hypothesis:l4-lockdown-is-a-
#: reserved-boolean) so the reserved flag is discoverable without reading
#: source. Exact wording is load-bearing -- read it, don't paraphrase.
_LOCKDOWN_RESERVED_HELP = (
    "comms.lockdown is RESERVED: false by default; true warns and encrypts "
    "nothing until lockdown is built (next season, rungs 5-8)."
)

_LOCKDOWN_WARNING = (
    "WARNING: comms.lockdown is set but lockdown is NOT BUILT (next season, "
    "rungs 5-8): messages stay plaintext-and-signed; no custodian signing "
    "server is required yet"
)


def _comms_config(root: Path) -> dict:
    """The `comms` config block from the nearest graph root's config.json,
    with a default for EVERY key this build knows. Absent block = all
    defaults; a malformed or unreadable config yields the defaults too --
    never raises."""
    graph = _main_graph_root(root)
    try:
        cfg = locations.load_config(graph)
        comms = cfg.get("comms") or {}
        if not isinstance(comms, dict):
            comms = {}
    except Exception:  # noqa: BLE001 -- a config problem never blocks comms
        comms = {}
    out = dict(_COMMS_DEFAULTS)
    out.update({k: v for k, v in comms.items() if k in _COMMS_DEFAULTS})
    return out


def _lockdown_requirements(cfg: dict) -> list[str]:
    """What a BUILT lockdown WILL require. A named seam, not a build: nothing
    here runs a cipher, a key exchange, or an envelope change -- the list
    feeds only the reserved-flag documentation and a test. First item is the
    always-on requirement; the custodian signing server is optional."""
    return ["encrypted-at-rest", "custodian-signing-server: optional"]


def _lockdown_warn(root: Path, cfg: dict | None = None) -> None:
    """Print the one reserved-flag warning to stderr when comms.lockdown is
    set. Called once per send and once per read/peek, so the flag's whole
    effect on the operator is exactly one line per seam -- never a block, and
    never a change to the bytes on the wire."""
    c = cfg if cfg is not None else _comms_config(root)
    if not c.get("lockdown"):
        return
    print(_LOCKDOWN_WARNING, file=sys.stderr)


def _live_row(row: dict) -> bool:
    """A LIVE seat row carries a live pid or a session_id (hypothesis
    l4-every-live-row-is-keyed...) -- exactly the rows a prime keys with
    `keygen --all-live`. A row with neither is not live and is left alone.
    """
    return bool(row.get("pid") or row.get("session_id"))


def _mint_seat_key(root: Path, seat: str,
                   scheme_name: str) -> tuple[Path, bytes] | None:
    """Mint ``<sessions>/seats/<seat>.key`` (0600) and return ``(path, pub)``.

    REFUSES -- returns None -- when a key file ALREADY exists: a second
    keygen must never destroy a key by name (hypothesis:l4-every-live-row-is-
    keyed...). ``KeyError`` names an unknown scheme before anything is touched.
    The PRIVATE seed is used only to write the file; it is never printed,
    logged, or returned.
    """
    scheme = seatsig.get(scheme_name)  # KeyError names the unknown scheme
    d = _seats_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{seat}.key"
    if path.exists():
        return None
    _priv, pub = scheme.keygen()
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
    return path, pub


def _row_write_submit(graph: Path, rows: list, actor: str, role: str) -> bool:
    """Write the ``config:posts`` rows through write.submit (the sanctioned
    writer; ``config:seats``/``seats`` is the one-season alias). Returns True
    on success, False when the write could not be admitted (no config node,
    no admitted actor, no seating) -- a keygen never fails to mint a key
    because the row could not be written, and it never prints the private
    seed either way.
    """
    try:
        import write as write_mod  # local; write.py imports no send.py
        _, list_key = geometry_config.resolve(graph)
        e = write_mod.Edit(f"config:{list_key}")
        write_mod.verb_set(e, list_key, json.dumps(rows))
        write_mod.submit(graph, e, actor=actor, role=role)
        return True
    except Exception:                                          # noqa: BLE001
        # Reporting is the caller's job (clause (1)): `keygen` prints the ONE
        # canonical line `keygen: key minted but the row write was refused
        # ...` when this returns False. Never a second copy here.
        return False


def _seats_rows(graph: Path) -> list:
    """The current `config:seats` rows on disk, or [] when absent."""
    try:
        import write as write_mod  # local
        return list(write_mod._load_seats(graph))
    except Exception:                                          # noqa: BLE001
        return []


# Clause (1) row-write outcome, threaded from `keygen` to `_cli_keygen`
# WITHOUT changing keygen's public Path|list|None contract (direct callers
# and the 25+ tests that assert it stay untouched). `keygen` resets it to
# True at entry and clears it when a MINTED key's row write was refused or
# the seat row was not found; `_cli_keygen` reads it once and exits 2. The
# key stays minted either way (a keygen never fails to mint); only the CLI
# exit code and the one stderr line change.
_last_keygen_row_ok = True


def _keygen_row_refused(reason: str) -> None:
    """The ONE canonical stderr line for a minted-but-unkeyed row (clause
    (1)) and the flag `_cli_keygen` keys on. Exactly one line, no block, no
    second copy of the text anywhere."""
    global _last_keygen_row_ok
    _last_keygen_row_ok = False
    print(f"keygen: key minted but the row write was refused -- {reason}; "
          f"the row is UNKEYED until a prime writes it", file=sys.stderr)


def keygen(root: Path, seat: str = "", scheme_name: str = seatsig.DEFAULT_SCHEME,
           all_live: bool = False, actor: str = "",
           role: str = "") -> Path | list[Path] | None:
    """Mint one or more seat signing keys and WRITE the row cells the seat
    row carries (hypothesis:l4-every-live-row-is-keyed...).

    ``keygen <seat>`` mints ``<sessions>/seats/<seat>.key`` (0600), prints the
    ``pubkey`` / ``sig_scheme`` / ``enc_scheme: none`` cells, and via
    write.submit writes them into the seat's OWN row in config:seats under
    the self-row carve-out declared in schemas/[config].md. ``keygen
    --all-live`` (the prime, the registry-wide writer the schema admits) keys
    every LIVE row (a live pid / session_id) that carries no ``pubkey``,
    skips already-keyed rows, and prints one line per row.

    A key file that ALREADY exists is NEVER overwritten: the seat is refused
    by name (returns None), so a second keygen cannot destroy a key. The
    PRIVATE seed is never printed, logged, or written outside sessions/.
    Returns the key Path (single), a list of Paths (--all-live), or None
    when the requested key was refused (already exists).
    """
    global _last_keygen_row_ok
    _last_keygen_row_ok = True  # reset per call; cleared when a minted row's write is refused/missing
    if all_live:
        graph = _graph_root(root)
        rows = _seats_rows(graph)
        # PRIME GATE (mur-39 order (c)): --all-live is the registry-wide
        # backstop, reserved for the prime director. Resolve the CALLER's own
        # row (detect the sender, then find its seat row in the SAME registry
        # this all_live pass is about) and refuse the whole keygen BY NAME
        # before ANY key file is minted unless that row carries role
        # ``prime_director`` -- today only the row write was refused and the
        # .key files still landed. Rows come from ``_seats_rows`` (the node
        # read, no git), never ``_load_rows`` (pushed-then-local, which issues
        # a git fetch under tests). The explicit ``role`` argument stays
        # honoured as the documented fallback for the actorless prime call.
        caller = _detect_sender(actor)
        own = _seat_row_in(rows, caller) if caller else None
        if own is not None:
            if own.get("role") != "prime_director":
                print(
                    f"REFUSED {caller}: --all-live is prime-only; own row "
                    f"role is {own.get('role')!r}, not 'prime_director'",
                    file=sys.stderr)
                return None
        elif role != "prime_director":
            print(
                f"REFUSED {caller or '<unknown>'}: --all-live is prime-only "
                f"(own row '{caller}' not found and no prime_director role "
                "passed)", file=sys.stderr)
            return None
        results: list[Path] = []
        keyed_names: list[str] = []
        new_rows = [dict(r) for r in rows]
        wrote_any = False
        for row in rows:
            if not _live_row(row):
                continue
            name = str(row.get("name") or "")
            if row.get("pubkey"):
                print(f"skipped {name} (already keyed)")
                continue
            minted = _mint_seat_key(root, name, scheme_name)
            if minted is None:
                print(f"REFUSED {name}: key {_seat_key_path(root, name)} "
                      f"already exists; not overwriting", file=sys.stderr)
                continue
            path, pub = minted
            for nr in new_rows:
                if nr.get("name") == name:
                    nr["pubkey"] = pub.hex()
                    nr["sig_scheme"] = scheme_name
                    nr["enc_scheme"] = nr.get("enc_scheme") or "none"
                    nr.setdefault("key_history", [])  # seed: keyed rows carry the cell
            print(f"keyed {name} {seatsig.fingerprint(pub)}")
            results.append(path)
            keyed_names.append(name)
            wrote_any = True
        if wrote_any:
            if not _row_write_submit(graph, new_rows, actor=actor, role=role):
                # clause (1): every keyed row stayed UNKEYED; the CLI exits 2.
                _keygen_row_refused("write.submit returned False for the keyed rows")
            # clause (2)/(4b): ONE own-row commit whose message names EVERY
            # seat this --all-live pass keyed (`keygen --all-live: keyed<list>`),
            # staging seats.md ONLY, then the clause-(2) push leg. Best-effort;
            # never fails the keygen.
            _commit_push_all_live(root, keyed_names)
        return results
    minted = _mint_seat_key(root, seat, scheme_name)
    if minted is None:
        path = _seat_key_path(root, seat)
        print(f"REFUSED: {seat}'s key {path} already exists; not overwriting",
              file=sys.stderr)
        return None
    _path, pub = minted
    # The cells the row needs -- NEVER the private seed.
    print(f"pubkey: {pub.hex()}")
    print(f"sig_scheme: {scheme_name}")
    print("enc_scheme: none")
    # Write the cells into the seat's own row (self-row carve-out).
    graph = _graph_root(root)
    rows = _seats_rows(graph)
    new_rows = [dict(r) for r in rows]
    own = next((r for r in new_rows if r.get("name") == seat), None)
    if own is not None:
        own["pubkey"] = pub.hex()
        own["sig_scheme"] = scheme_name
        own["enc_scheme"] = own.get("enc_scheme") or "none"
        own.setdefault("key_history", [])  # seed: every keyed row carries the cell
        if not _row_write_submit(graph, new_rows, actor=actor, role=role):
            # clause (1): minted but the row write was refused -> CLI exits 2.
            _keygen_row_refused(f"write.submit returned False for seat row {seat!r}")
        # clause (2): keygen commits its own-row hunk and pushes, like every
        # key-cell writer, through SL6.01's `_commit_spawn_row` + the push
        # leg. Best-effort; a refused commit/push never fails the mint.
        _commit_push_seat_row(root, own, seat, "keygen")
    else:
        # seat row not found: a key minted that no row carries reads UNKEYED
        # forever -- the defect the claim closes. The CLI exits 2 (clause (1)).
        _keygen_row_refused(f"seat row {seat!r} is not in the registry")
    return _path


def _commit_push_seat_row(root: Path, row: dict, seat: str,
                          origin: str) -> None:
    """CLAUSE (2) commit+push for a key-cell writer's own-row write.
    Commits the seat's own-row hunk as ONE pathspec commit on MAIN's season
    branch through SL6.01's `rotate._commit_spawn_row` (never a second copy)
    and pushes that branch via its push leg. Best-effort, never raises,
    never fails the mint: a refused commit or push prints one note line to
    stderr and the key stays minted."""
    try:
        import rotate  # local: same dir (send.py pattern, no import cycle)
    except Exception as exc:  # noqa: BLE001
        print(f"note: {origin} row commit/push skipped ({exc})",
              file=sys.stderr)
        return
    def _int(v):
        try:
            return int(v or 0)
        except (TypeError, ValueError):
            return 0
    try:
        out = rotate._commit_spawn_row(
            root, seat=seat, generation=_int(row.get("generation")),
            session_id=str(row.get("session_id") or ""),
            window=str(row.get("window") or ""),
            pid=_int(row.get("pid")))
        print(f"note: {out.splitlines()[0]}", file=sys.stderr)
    except Exception as exc:  # noqa: BLE001
        print(f"note: {origin} row commit/push skipped ({exc})",
              file=sys.stderr)


def _all_live_seats_content(root: Path, top: Path,
                            keyed_names: list[str]) -> str | None:
    """The seats.md blob the `--all-live` keygen commit should stage: HEAD's
    content with ONLY the changes that carry THIS pass's keyed rows applied
    (a changed line whose `name` cell keys one of the keyed seats, or the
    whole-node frontmatter `edited_by:` stamp the same write owns), and every
    FOREIGN change REVERTED to the committed (HEAD) line. Base is HEAD, never
    the index -- a pre-staged foreign hunk cannot ride the keygen commit.
    Returns None when there is no keyed-row change to stage.

    A multi-row generalisation of rotate._seats_ownrow_content (send.py never
    edits rotate.py; sibling rows sit ADJACENT so git's unified diff folds an
    own and a foreign row into ONE hunk -- the cut is therefore made per
    CHANGED LINE, into an in-memory buffer, never onto the working tree). The
    caller stages this content into the index via update-index (working tree
    untouched), so the keygen commit carries exactly the rows it keyed and
    every foreign hunk stays unstaged and byte-untouched in the tree.
    """
    import difflib  # local: only the buffer-builder needs it
    rel = os.path.relpath(_shared_seats_path(root), top)
    try:
        run = subprocess.run(["git", "-C", str(top), "show",
                              f"HEAD:{rel}"],
                             capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return None
    if run.returncode != 0:
        return None
    try:
        work = _shared_seats_path(root).read_text(encoding="utf-8")
    except OSError:
        return None
    base_lines = run.stdout.splitlines()
    work_lines = work.splitlines()
    cells = [f'"name": "{n}"' for n in keyed_names]

    def _own(l: str) -> bool:
        # a changed line is KEYED when its row-cell `name` names one of the
        # keyed seats, or it is the top-level YAML `edited_by: <writer>`
        # frontmatter provenance stamp the SAME write owns (value-agnostic:
        # the writer's actor, not a seat name -- mirror rotate._own_row_line).
        stripped = l.lstrip("+- ")
        if stripped.startswith("edited_by: ") or stripped == "edited_by:":
            return True
        return any(c in l for c in cells)

    staged: list[str] = []
    b = w = 0
    any_own = False
    sm = difflib.SequenceMatcher(None, base_lines, work_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        staged.extend(base_lines[b:i1])
        removed = base_lines[i1:i2]
        added = work_lines[j1:j2]
        for k in range(max(len(removed), len(added))):
            old = removed[k] if k < len(removed) else None
            new = added[k] if k < len(added) else None
            is_own = ((old is not None and _own(old))
                      or (new is not None and _own(new)))
            if is_own:
                any_own = True
                if new is not None:
                    staged.append(new)   # keyed change: keep working line
                # else: a keyed deletion -- append nothing
            elif old is not None:
                staged.append(old)        # foreign change: keep committed line
        b, w = i2, j2
    staged.extend(base_lines[b:])
    if not any_own:
        return None
    return "\n".join(staged) + "\n"


def _commit_push_all_live(root: Path, keyed_names: list[str]) -> str:
    """CLAUSE (2)/(4b) -- the `--all-live` keygen commit: ONE commit of
    seats.md carrying EXACTLY the rows this pass keyed, whose message names
    EVERY seat it keyed (`keygen --all-live: keyed <a>, <b>, <c>`), then the
    clause-(2) season-branch push leg. Resolved against MAIN's graph tree (a
    linked-worktree caller commits MAIN, never its own fork). Staging seats.md
    ONLY AND ONLY the keyed rows: the committed blob is HEAD's seats.md plus
    exactly those rows (generalising rotate's own-row discipline -- see
    :func:`_all_live_seats_content`), committed against a THROWAWAY index
    seeded from HEAD via update-index --cacheinfo (working tree NEVER
    written), so keygen --all-live never sweeps a foreign writer's uncommitted
    row edit into its commit -- the foreign delta stays byte-untouched and
    uncommitted in the working copy. Best-effort, never raises, never fails
    the mint: a refused commit or push prints one note line to stderr and the
    keys stay minted. Returns the one note line.
    """
    listed = ", ".join(keyed_names)
    note = f"keygen --all-live: keyed {listed}"
    try:
        import rotate  # local: same dir (send.py pattern, no import cycle)
        import tempfile
        main_root = _shared_graph_root(root)
        top = rotate._git_toplevel(main_root)
        if top is None:
            _l = f"note: {note} — no git repo; rows stay uncommitted"
            print(_l, file=sys.stderr)
            return _l
        seats = _shared_seats_path(root)
        rel = os.path.relpath(seats, top)
        new_content = _all_live_seats_content(root, top, keyed_names)
        if new_content is None:
            _l = f"note: {note} — seats.md already clean after the write; " \
                "nothing committed"
            print(_l, file=sys.stderr)
            return _l
        # Build the keyed-only blob and commit it against a THROWAWAY index
        # seeded from HEAD (GIT_INDEX_FILE=<tmp>; read-tree HEAD, then
        # hash-object the content and update-index --cacheinfo under it) and
        # commit against THAT index with no pathspec, so git resolves the
        # committed tree from the temp index, never the working tree. The
        # shared seats.md working copy and every foreign hunk stay byte-
        # untouched throughout.
        fd, tmp_index = tempfile.mkstemp(prefix="alllive-idx-")
        os.close(fd)
        env = dict(os.environ)
        env["GIT_INDEX_FILE"] = tmp_index

        def _tmp_git(parts, input=None):
            return subprocess.run(["git", "-C", str(top)] + parts,
                                  capture_output=True, text=True, env=env,
                                  timeout=10, input=input)

        rc = None
        blob_sha = ""
        try:
            seed = _tmp_git(["read-tree", "HEAD"])
            if seed.returncode != 0:
                raise RuntimeError(seed.stderr.strip())
            blob = _tmp_git(["hash-object", "-w", "--stdin"],
                            input=new_content)
            if blob.returncode != 0 or not blob.stdout.strip():
                raise RuntimeError(blob.stderr.strip())
            blob_sha = blob.stdout.strip()
            upd = _tmp_git(["update-index", "--add", "--cacheinfo",
                            f"100644,{blob_sha},{rel}"])
            if upd.returncode != 0:
                raise RuntimeError(upd.stderr.strip())
            msg = f"keygen --all-live: keyed {listed}"
            rc = _tmp_git(["commit", "-q", "-m", msg])
        finally:
            try:
                os.unlink(tmp_index)
            except OSError:
                pass
        if rc is None or rc.returncode != 0:
            _l = f"note: {note} — git commit failed: " \
                f"{rc.stderr.strip() if rc else 'unknown'}"
            print(_l, file=sys.stderr)
            return _l
        # point the REAL index's seats.md at the committed blob so the keyed
        # rows no longer show staged; only foreign hunks remain.
        subprocess.run(["git", "-C", str(top), "update-index", "--add",
                        "--cacheinfo", f"100644,{blob_sha},{rel}"],
                       capture_output=True, text=True, timeout=10)
        push = rotate._push_season_branch(root)
        _l = f"note: {note}; {push}"
        print(_l, file=sys.stderr)
        # g15.26 claim (b): a successful all-live push means origin now
        # carries every keyed row's committed pubkey -- so for each seat
        # this pass keyed, any deferred `<seat>.key.pending` swap (written
        # when an earlier push FAILED) now COMPLETES through rotate's ONE
        # shared helper (each only flips when its committed row matches the
        # pending pubkey). Best-effort; never raises.
        for _seat in keyed_names:
            rotate._finish_pending_swap_on_push(root, _seat, push)
        return _l
    except Exception as exc:  # noqa: BLE001
        _l = f"note: {note} row commit/push skipped ({exc})"
        print(_l, file=sys.stderr)
        return _l


def _quorum_caller() -> bool:
    """True when the caller is a tier-3 parent (the quorum) — the only role
    that may reach the prime without the morals override
    (hypothesis:l3w4-quorum-reviews: "The quorum IS Belam to anyone else")."""
    role = os.environ.get("AGI_ROLE", "").strip()
    tier = os.environ.get("AGI_LADDER_TIER", "").strip()
    return role == "parent" and tier == "3"


def _detect_sender(from_flag: str | None) -> str:
    """Sender order, as built: AGI_AGENT_ID env, then AGI_SEAT, then --from,
    then "unknown".

    Identity is SUPPLIED by the harness env, never CLAIMED by a flag
    (hypothesis:l4-authority-verified-against-the-graph-not-the-message): the
    agent's own id (AGI_AGENT_ID, exported by dispatch) signs a message even
    when the caller forgot a flag; next a SEAT name (AGI_SEAT, exported by
    rotate-self / spawn / seats-launch / recovery) signs under the seat name;
    an explicit --from does NOT beat either env fallback — a flag may only
    name a sender in a hand-run shell with no exported identity; then
    "unknown" — an honest absence, not a confident wrong name
    (hypothesis:l3-send-comms-root, extended by hypothesis:l4-send-py-same-
    sender-stranded-line-and-the-swallowed-wake clause c: so every
    AGI_SEAT-exporting path dms under its seat name, never "from: unknown").
    The tmux window NAME is never an identity — a window name is a seat, not
    an agent (hypothesis:l3-agent-id-never-exported).
    """
    env = os.environ.get("AGI_AGENT_ID", "").strip()
    if env:
        return env
    seat = geometry_config.resolved_seat_env()
    if seat:
        return seat.strip()
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
    for b in _MSG_BOUNDARY_RE.split(text):
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


def _wrap_transcript_line(prefix: str, text: str, width: int) -> str:
    """Wrap a transcript line's message body under its fixed `prefix` (the
    `**sender** HH:MM — ` header), which itself is never wrapped, so a
    reader's grep on the sender still works. Continuation lines are padded
    by the prefix width, so no transcribed line exceeds `width`."""
    if width <= 0:
        return prefix + text
    avail = max(10, width - len(prefix))
    wrapped = _wrap_body(text, avail)
    if "\n" not in wrapped:
        return prefix + wrapped
    body_lines = wrapped.split("\n")
    pad = " " * len(prefix)
    out = [prefix + body_lines[0]]
    for cont in body_lines[1:]:
        out.append(pad + cont if cont else "")
    return "\n".join(out)


def render_transcript(blocks: list[dict], wrap: int = 160) -> list[str]:
    """Render messages as a chat transcript: `**sender** HH:MM — text`, the
    message body wrapped at `wrap` columns (the header prefix is never
    wrapped; `wrap <= 0` renders today's one-line-per-message form)."""
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
        lines.append(_wrap_transcript_line(f"**{sender}** {hhmm} — ", text,
                                           wrap))
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


def _build_nudge_token(seat: str, path: str | None = None) -> str:
    """ONE fixed machine-prefixed wake token for one recipient seat, always
    shorter than `_NUDGE_TOKEN_MAX` (the bare form when the seat name is
    long enough to threaten the cap).

    `path` names the wake path that typed it (clause (3) of hypothesis:l4-a-
    strand-is-only-a-line-inside-a-rendered-input-box-and-wake-names-its-path):
    `(wake:idle)` for an idle delivery, `(wake:strand)` for a stranded-line
    context. The NAMED token always leaves the PREFIX byte-identical --
    `[agi-nudge] unread for {seat}` -- so every `_NUDGE_PREFIXES` match and
    every reader's `unread for` grep keeps working; the suffix is only the
    tail. A bare `path=None` (a fire-and-forget `send()` nudge, never a
    `wake` verb) keeps the legacy token with no suffix."""
    suffix = f" (wake:{path})" if path else ""
    token = NUDGE_TOKEN_TEMPLATE.format(seat=seat) + suffix
    if len(token) > _NUDGE_TOKEN_MAX:
        token = NUDGE_TOKEN_BARE_TEMPLATE.format(seat=seat) + suffix
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


def _nudge_pending_lock_path(root: Path, seat: str) -> Path:
    return _inbox_dir(root) / f"{seat}.nudge.pending.lock"


def _pending_more(root: Path, seat: str) -> int:
    """Coalesced-but-untyped dms awaiting the next delivered nudge's
    `(+N more, read <seat>)` tail (hypothesis:l4-the-nudge-carries-the-dm-
    body-inline). 0 = no pending tail."""
    try:
        return int(_nudge_pending_path(root, seat).read_text().strip() or 0)
    except Exception:                                    # noqa: BLE001
        return 0


class _PendingLock:
    """Exclusive advisory lock over a seat's pending-count read-modify-write.
    Both `_bump_pending` and `_clear_pending` hold it, so a clear cannot
    zero a bump made at the same moment, and a bump cannot race a
    concurrent clear (hypothesis:l4-a-read-clears-the-coalesced-nudge-count)."""

    def __init__(self, root: Path, seat: str):
        self._path = _nudge_pending_lock_path(root, seat)

    def __enter__(self):
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._f = open(self._path, "a+")
        fcntl.flock(self._f, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        fcntl.flock(self._f, fcntl.LOCK_UN)
        self._f.close()
        return False


def _bump_pending(root: Path, seat: str) -> None:
    """Increment the pending-coalesced count; a dm coalesced inside the
    per-seat window is counted here so a LATER delivered nudge carries it.
    Best-effort, never raises. The read-modify-write runs under the same
    exclusive flock as `_clear_pending`, so a concurrent clear cannot zero
    a bump made at the same moment."""
    try:
        p = _nudge_pending_path(root, seat)
        p.parent.mkdir(parents=True, exist_ok=True)
        with _PendingLock(root, seat):
            p.write_text(str(_pending_more(root, seat) + 1))
    except OSError:
        pass


def _clear_pending(root: Path, seat: str, observed: int | None = None) -> None:
    """Reset (or decrement-by-observed) the pending-coalesced count after a
    nudge that carried it. Best-effort, never raises.

    When the caller passes `observed` -- the count the read saw BEFORE it
    began consuming -- writes max(0, current - observed): a dm that
    coalesced DURING the read is preserved rather than silently zeroed by
    an unconditional write. Absent `observed` clears to 0 exactly as
    before. Runs under the same exclusive flock as `_bump_pending`."""
    try:
        p = _nudge_pending_path(root, seat)
        with _PendingLock(root, seat):
            if observed is None:
                p.write_text("0")
            else:
                p.write_text(str(max(0, _pending_more(root, seat) - observed)))
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
    token-not-a-message, residue 2).

    Clause (1) (hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-
    input-box-and-wake-names-its-path): when NO prompt glyph is found -- a
    busy pane rendered the spinner in place of the box, or the capture is
    scrolled entirely above the box -- the region is EMPTY (''), NEVER the
    whole pane. The whole pane was the phantom-echo bug: a just-submitted
    `[agi-nudge] unread for <seat>` token echoed in the TRANSCRIPT read as a
    stranded in-box line, and wake RE-TYPED it (six phantom tokens
    19:17-19:33Z on master-sensei with an empty inbox). The MEASURED live
    busy shape KEEPS the box (SHAPE B, see _nudge_coalesce_reason), so this
    '' branch is the SHAPE A (box absent) safety half; an empty region is the
    safe 'no rendered box -> do not type into it' answer in either case."""
    lines = (pane or "").splitlines()
    for i in range(len(lines) - 1, -1, -1):
        if "\u276f" in lines[i]:
            return "\n".join(lines[i:])
    return ""


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
    a wake until it scrolls off. Except: when there is NO rendered box
    (region == '' -- SHAPE A: the box hidden, or the capture scrolled above
    it), there is nothing to scope the busy check to, so the WHOLE capture is
    scanned for the busy footer, and in every case the answer blocks typing
    (a no-box capture is never a confirmed idle empty box; a transcript echo
    must never read as a stranded in-box line -- clauses (1)-(2) of
    hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-
    wake-names-its-path). One exception: a BLANK capture (empty string) is
    the test/greenfield stand-in for an idle pane whose box renders empty,
    and a live pane never reaches this branch blank (a real capture always
    carries its `\u276f` box), so a blank capture keeps the legacy idle-nudge
    behaviour (returns None). A NON-BLANK, box-less, footer-less capture
    instead returns `"no rendered box"`; `wake` maps that to `nothing-pending`
    (nothing typed, marker untouched) -- the clause-(2) fix for a pending
    seat whose capture cannot be a box.

    The MEASURED live busy shape is SHAPE B: the pane KEEPS its `\u276f` box
    and `esc to interrupt` sits in the FOOTER below the box's separator, still
    INSIDE the region (a real `tmux capture-pane -p` of @291 in this session
    -- not the box-less spinner the premise guessed). The committed fixture
    fixtures/claude_pane_busy.txt matches it."""
    if registry == "busy":
        return "pane busy (registry)"
    if pane is not None:
        region = _input_region(pane)
        if region == "":
            # No rendered input box (SHAPE A: the box hidden under a busy
            # spinner / the capture scrolled above it, OR an empty mock
            # capture standing in for an idle pane). There is no box to
            # scope the busy footer to, so the WHOLE capture is scanned for it
            # (a box-less busy pane must still read busy). The STRAND scan is
            # never run on an empty region -- a just-submitted
            # `[agi-nudge] unread for <seat>` token echoed in the TRANSCRIPT
            # above where the box would be is NOT stranded (the phantom
            # retype, clauses (1)-(2)). A busy footer blocks; otherwise a
            # NON-BLANK, box-less, footer-less capture is the SHAPE A hazard
            # (a pane scrolled above its box, or a transcript echo of where a
            # box would be) and is NEVER a confirmed idle box -- clause (2)
            # of hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-
            # input-box-and-wake-names-its-path -- so wake maps it to
            # `nothing-pending` (nothing typed, marker untouched) and send's
            # nudge coalesces to `(no rendered box)`, never a blind site to
            # type into.
            if "esc to interrupt" in pane.lower():
                return "pane busy (spinner)"
            if (pane or "").strip():
                # Non-blank capture with no rendered box and no busy footer:
                # never a confirmed idle box -> do not type into it.
                return "no rendered box"
            # A BLANK capture is the test/greenfield stand-in for an idle
            # pane whose box renders as an empty string. A live pane never
            # reaches here as blank -- `_capture_pane` of a real pane always
            # carries its `\u276f` box -- so the empty-string mock keeps the
            # legacy idle-nudge behaviour (send's `_nudge_window` tests model
            # the to-be-typed pane as an empty capture).
            return None
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
                  repair_stale_id: bool = True,
                  ) -> tuple[str, object, str] | None:
    """Resolve the send-keys target a seat's wake lands in, exactly as
    `_nudge_window` uses it, so a silent re-check (`wake`) and the delivery
    path share ONE address resolution (hypothesis:l4-a-stranded-nudge-is-
    resubmitted-by-typing-not-enter). Returns `(target, pid, tmux_session)`
    or None when the seat has no addressable window: a NAME-addressed row is
    refused (a predecessor/namesake could occupy it) and a windowless
    (ephemeral) recipient may not be nudged by name unless actually listed.

    CLAUSE (3) (hypothesis:l4-wake-repair-is-quiet-honest-and-readable,
    extended by hypothesis:l4-send-py-same-sender-stranded-line-and-the-
    swallowed-wake clause b): an @id target is trusted ONLY while it is still
    a LISTED window. A stale @id (the row's window was reaped/rotated away)
    would fail inside `tmux send-keys -t session:@id` and the failure would
    be swallowed -- a message addressed to it returns with no line and the
    seat is never woken. `repair_stale_id` now defaults True for EVERY
    caller (send, dm and wake alike): a stale @id prints a `nudge repair:`
    line and FALLS BACK to the by-name lookup below, the same
    `_window_listed` path a name-addressed row uses. When that by-name
    fallback ALSO finds no window, ONE named line goes to stderr -- silence
    is the defect -- then None is returned, and the message itself stays in
    the inbox as always.
    """
    rows = _locally_loaded_rows(root)
    row = _seat_row_by_name(rows, to)
    window_ref = (row or {}).get("window")      # e.g. "@267", a NAME, or None
    pid = (row or {}).get("pid")
    if tmux_session is None:
        import rotate  # lazy: same bin dir, DEFAULT_TMUX_SESSION lives there
        tmux_session = rotate.DEFAULT_TMUX_SESSION
    stale_ref: str | None = None
    if window_ref and str(window_ref).startswith("@"):
        # CLAUSE (3): an @id is only a live target while it is a CURRENT
        # window; a stale one is named, then repaired by name below.
        if repair_stale_id and not _window_id_listed(
                tmux_session, str(window_ref)):
            print(f"nudge repair: {to} row window {window_ref} is gone; "
                  f"falling back to name", file=sys.stderr)
            stale_ref = str(window_ref)
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
            # A stale @id that the by-name fallback ALSO cannot find is
            # never silent: ONE named line (clause b). A row that simply had
            # no window (ephemeral) stays a silent no-op as before.
            if stale_ref is not None:
                print(f"nudge: {to} row window {stale_ref} is gone and no "
                      f"window named {to} is listed -- message written, no "
                      f"wake", file=sys.stderr)
            return None
        target = f"{tmux_session}:{to}"
    return (target, pid, tmux_session)


def _nudge_window(root: Path, to: str, tmux_session: str | None = None,
                 sender: str | None = None,
                 body: str | None = None,
                 repair_stale_id: bool = True,
                 resolved: tuple | None = None,
                 path: str | None = None) -> bool:
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
        text = _build_nudge_token(to, path)
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


def _wake_outcome(outcome: str, delivered: bool, seat: str,
                  window_id: str | None = None) -> bool:
    """Print the ONE outcome line for the `wake` verb and return the delivery
    truth (True = a token/strand/deferred actually reached the pane, so the
    exit code is 0; False = nothing delivered, exit 1). The line is exactly one
    of: typed-token | resubmitted-strand | delivered-deferred | busy-deferred
    | nothing-pending | no-target (clause (2) of hypothesis:l4-wake-repair-is-
    quiet-honest-and-readable).

    Clause (3) (hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-
    box-and-wake-names-its-path): ALSO writes ONE per-seat line through the
    SAME resolver heal.py's `_watch_log` uses (`reaper_log.log`, lifted to a
    shared helper -- never a second log path):

        wake <seat>: <path> <state> [@<window_id>]

    `<state>` is one of delivered | deferred | nothing-pending | no-target;
    `<path>` is idle | strand, the path the wake travelled (strand for a
    resubmitted stranded line). """
    print(outcome)
    state = {
        "no-target": "no-target",
        "resubmitted-strand": "delivered" if delivered else "deferred",
        "nothing-pending": "nothing-pending",
        "busy-deferred": "deferred",
        "typed-token": "delivered",
        "delivered-deferred": "delivered",
    }.get(outcome, "deferred")
    path = "strand" if outcome == "resubmitted-strand" else "idle"
    wid = f" {window_id}" if window_id else ""
    reaper_log.log(f"wake {seat}: {path} {state}{wid}")
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
    (clause 3: a stale @id prints a `nudge repair:` line and falls back to
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
        return _wake_outcome("no-target", delivered=False, seat=to)
    target, pid, tms = resolved
    window_id = target.split(":", 1)[1] if ":" in target else None
    pane = _capture_pane(tms, target)
    reason = _nudge_coalesce_reason(pane, _build_nudge_token(to, "idle"),
                                    _registry_status(pid))

    # A stranded nudge-shaped line in the pane is delivered (resubmitted by
    # TYPING) regardless of pending -- the resubmit itself IS the wake. The
    # strand branch never fires on a busy / no-box pane (clause (2): a busy
    # pane's echoed or stranded token never causes wake to re-type a phantom
    # token -- _nudge_coalesce_reason returns a busy or no-box reason first,
    # never 'token already unsubmitted').
    if reason == "token already unsubmitted":
        ok = _nudge_window(root, to, tmux_session=tms, repair_stale_id=True,
                           resolved=resolved, path="strand")
        return _wake_outcome("resubmitted-strand", delivered=ok, seat=to,
                             window_id=window_id)

    if reason == "no rendered box":
        # Clause (2) (hypothesis:l4-a-strand-is-only-a-line-inside-a-
        # rendered-input-box-and-wake-names-its-path): an EMPTY input region
        # (no rendered `\u276f` box AND no busy footer) is never a confirmed
        # idle box -- the measured idle pane always renders its box -- so a
        # pending seat whose capture cannot be a box is NOT typed into.
        # Nothing typed, marker untouched (nothing announced), and the ONE
        # reaper log line carries `idle nothing-pending`. Deliberately NOT
        # the strand branch and NOT the ordinary type path (which is what
        # the pre-fix `None` allowed: a pending seat with a box-less capture
        # was still typed into).
        return _wake_outcome("nothing-pending", delivered=False, seat=to,
                             window_id=window_id)

    if not _seat_has_pending(root, to):
        # nothing stranded and nothing pending: never type a bare wake token
        # into a seat with nothing to announce (the heal polls every seat).
        return _wake_outcome("nothing-pending", delivered=False, seat=to,
                             window_id=window_id)

    # Clause (1): never retype a token for an unread state we already
    # announced. The 30s `_NUDGE_COALESCE_WINDOW_S` alone would let an
    # unchanged unread inbox retype once it lapses under heal's every-seat
    # polling; the digest gate stops that for as long as the state is unchanged.
    digest = _unread_digest(root, to)
    if _announced_digest(root, to) == digest:
        return _wake_outcome("nothing-pending", delivered=False, seat=to,
                             window_id=window_id)

    if reason is not None:
        # Pane busy / spinner with something pending: nothing typed. The
        # deferred record is already written; `_nudge_window` prints its own
        # coalesced line, this wake prints its ONE outcome.
        _nudge_window(root, to, tmux_session=tms, repair_stale_id=True,
                      resolved=resolved)
        return _wake_outcome("busy-deferred", delivered=False, seat=to,
                             window_id=window_id)

    # Pane IDLE with a NEW unread state: type the wake token, or deliver the
    # stored deferred dm INLINE when one waits (read before `_nudge_window`
    # clears it).
    delivering_deferred = _read_deferred(root, to) is not None
    ok = _nudge_window(root, to, tmux_session=tms, repair_stale_id=True,
                       resolved=resolved, path="idle")
    if ok:
        _record_announced(root, to, digest)
        return _wake_outcome("delivered-deferred" if delivering_deferred
                             else "typed-token", delivered=True, seat=to,
                             window_id=window_id)
    # A delivery was attempted but nothing reached the pane (e.g. the 30s
    # window caught it); `_nudge_window` already printed its own line.
    return _wake_outcome("nothing-pending", delivered=False, seat=to,
                         window_id=window_id)


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
    _lockdown_warn(root)
    inbox = _inbox_path(root, to)
    inbox.parent.mkdir(parents=True, exist_ok=True)

    ts = _now()
    from_id = _detect_sender(sender)
    sig_line = _sign_line(root, from_id, ts, to, text)
    head = f"{MSG_SEP}ts: {ts}\nfrom: {from_id}\nto: {to}\n"
    if sig_line is not None:
        # The envelope (Prime ruling B, hypothesis:l4-every-live-row-is-keyed...):
        # a signed message carries `env: v1` beside its `sig:` line so a reader
        # can tell the envelope version from the payload. The scheme NAME on the
        # sig line comes from the signing key's row, never a literal.
        head += "env: v1\n" + sig_line + "\n"
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

    # Read with newline="" so CR/CRLF survive: the sig covers the EXACT bytes
    # the sender passed (mur-39 order (d)), and read_text()'s universal-newline
    # translation would fold a lone CR (and CRLF) into LF before _parse_block
    # could ever see it -- making every CR-carrying message read FORGED.
    text = inbox.open("r", newline="").read()
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

    # Split into blocks by the message separator -- only where a separator is
    # followed by a "ts:" header, so a body line equal to "---" cannot fragment
    # one signed block into two (a split tail would verify against nothing and
    # read FORGED).
    blocks = [b for b in _MSG_BOUNDARY_RE.split(unread_text) if b.strip()]
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
    # Split on "\n" ALONE, never splitlines(): splitlines() treats CR, CRLF,
    # VT, FF, FS, GS, RS and U+2028/U+2029 as line boundaries too, so a body
    # carrying a CR is silently re-fragmented -- and the sig covers the EXACT
    # bytes the sender passed, so a normalized body can never re-verify (the
    # CR-body / FORGED defect, mur-39 order (d)). Header lines are pure LF, so
    # the first-blank-line boundary is unchanged; but the body is reassembled
    # line-for-line on "\n" so every "\r" survives byte-for-byte.
    lines = body.split("\n")
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
    # Reassemble the body on "\n", then strip EXACTLY the ONE trailing "\n"
    # the writer appends (`block = head + f"\n{text}\n"`) -- never rstrip,
    # which would strip a GENUINE trailing LF from a legitimate body and drive
    # its own signature to FORGED, and would also eat the "\n" of a trailing
    # CRLF (leaving a lone "\r"). text[:-1] removes exactly one byte, so a
    # trailing CR survives. This is the exact inverse of the writer's store, and
    # it reproduces the signed bytes (SL6.06).
    text = "\n".join(lines[i + 1:])
    if text.endswith("\n"):
        text = text[:-1]
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
    than guessing.

    hypothesis:l4-the-label-authority-falls-back-to-mains-committed-row...
    CLAUSE (1): a PUSHED row that names NO key cell (no ``pubkey`` or no
    ``sig_scheme``) falls back per-seat to the SAME seat's COMMITTED row in
    MAIN's HEAD (``git show HEAD:<seats.md>`` at the shared graph root --
    never the dirty working copy, never ``_locally_loaded_rows``), so a
    freshly keyed/rotated post's signed dms verify instead of reading
    UNKEYED/FORGED until the hourly push. A pushed row that DOES name a key
    stays authoritative (a stale MAIN key never overrides origin)."""
    seeded = _pushed_seats(root, _PUSHED_SEATS, True)
    if seeded is not None:
        rows, _sha, _resolved_ref = seeded
        if rows:
            return _merge_main_committed_keys(root, rows)
        # hypothesis:l4-the-main-committed-reader... — an EMPTY pushed row
        # set (a real, reachable authority that carries no rows) reads None,
        # never the dirty working copy. Before F1 it returned None here;
        # restoring that means a reader labels any sig FORGED rather than
        # guessing against an uncommitted local file.
        return None
    rows = _locally_loaded_rows(root)
    return rows or None


def _in_git_repo(root: Path) -> bool:
    """Filesystem-only probe (NEVER a subprocess — the send test guard
    forbids non-tmux subprocess calls under test): True when ``root``'s tree
    is inside a git work tree (a ``.git`` file or dir walking up). Exists so
    the committed-row fallback short-circuits on a gitless root/fixture
    without spawning git."""
    cur = Path(root)
    while True:
        if (cur / ".git").exists():
            return True
        parent = cur.parent
        if parent == cur:
            return False
        cur = parent


def _seats_committed_rows(root: Path) -> list:
    """MAIN's COMMITTED seat rows -- ``git show HEAD:<seats.md>`` at MAIN's
    graph root. The per-seat fallback authority for a PUSHED row that names
    no key cell. Reads the BLOB from HEAD (never the dirty working copy),
    so a key that is committed but not yet pushed is still the authority
    for an unkeyed pushed row. Returns [] when the committed content cannot
    be read (no repo, no blob, not a path git addresses).

    A reader inside a LINKED WORKTREE must still reach MAIN's committed row:
    git is run from MAIN's graph root (``_shared_graph_root``), never the
    caller's worktree, and the blob is read with ``git -C <main-toplevel>
    show HEAD:<rel>``. Running git at a worktree's root makes
    ``rev-parse --show-toplevel`` return the WORKTREE toplevel, so
    ``relative_to`` fails against MAIN's seats path and the helper returns
    [] -- the fallback never fires for the very reader (a ``--branch`` kid)
    that needs it most
    (hypothesis:l4-the-main-committed-reader-runs-git-at-mains-toplevel...)."""
    if not _in_git_repo(root):
        return []
    seats = _shared_seats_path(root)
    graph = _shared_graph_root(root)
    top = _run_git(graph, ["rev-parse", "--show-toplevel"])
    if top is None or top.returncode != 0:
        return []
    try:
        top_path = Path(top.stdout.strip())
        rel = seats.resolve().relative_to(top_path.resolve())
    except (ValueError, OSError):
        return []
    shown = _run_git(top_path, ["show", f"HEAD:{rel}"])
    if shown is None or shown.returncode != 0:
        return []
    return _load_seats_rows(shown.stdout)


def _merge_main_committed_keys(root: Path, pushed: list) -> list:
    """CLAUSE (1) merge: a pushed row that names no key cell (no ``pubkey``
    or no ``sig_scheme``) inherits the key cells of the SAME seat's COMMITTED
    row in MAIN's HEAD -- per-seat, never the dirty working copy. A pushed
    row that DOES name a key stays authoritative. The inheriting row is
    tagged ``_main_committed`` so the label site can name the authority
    (clause 3). Never raises."""
    committed = _seats_committed_rows(root)
    if not committed:
        return pushed
    by_name = {r.get("name"): r for r in committed if r.get("name")}
    if not by_name:
        return pushed
    out: list = []
    for r in pushed:
        nr = dict(r)
        nr.pop("_main_committed", None)
        name = nr.get("name")
        if not (nr.get("pubkey") and nr.get("sig_scheme")) and name:
            main_row = by_name.get(name)
            if main_row:
                for cell in ("pubkey", "sig_scheme", "enc_scheme",
                             "key_history"):
                    if not nr.get(cell) and main_row.get(cell):
                        nr[cell] = main_row[cell]
                if nr.get("pubkey") or nr.get("sig_scheme"):
                    nr["_main_committed"] = True
        out.append(nr)
    return out


def _row_for_label(root: Path, rows: list | None, name: str) -> dict | None:
    """The ONE row resolver every signature verifier feeds from: the PUSHED
    row first (the author's own key wins -- a stale MAIN key never overrides
    origin), then MAIN's COMMITTED row for the same seat (`_seats_committed_rows`,
    `git show HEAD`, never the dirty copy -- the SL7.08 seam's authority),
    else None. A name found in NEITHER labels ``UNVERIFIABLE`` (never FORGED,
    hypothesis:l4-an-absent-pushed-row-reads-unverifiable...); ``rows is
    None`` (no pushed set at all) likewise falls through to the committed
    row, then None. A row that IS resolved yet fails its OWN signature still
    reads FORGED exactly as today -- this resolver only ever SUPPLIES the
    authoritative row, it never softens a verdict against a row. Merges,
    never rebases: for a pushed row that is PRESENT and fails, the caller's
    existing generation-guarded seam (`_seam_main_committed`) still runs,
    because the pushed row wins here and the seam owns the would-be-FORGED
    case. The COMMITTED row is returned tagged ``_main_committed`` so a
    VERIFIED label names the authority (:func:`_verify_block`,
    :func:`_whois_sig_label`).
    """
    if rows is not None:
        row = _seat_row_in(rows, name)
        if row is not None:
            return row
    committed = _seats_committed_rows(root)
    crow = _seat_row_in(committed, name)
    if crow is None:
        return None
    tagged = dict(crow)
    tagged["_main_committed"] = True
    return tagged


def _row_for_pubkey(root: Path, rows: list | None, prefix: str) -> dict | None:
    """The ONE row a whois ``--key`` + ``--sig`` verifies a signature against:
    the UNIQUE row whose CURRENT ``pubkey`` cell starts with ``prefix``
    (min ``WHOIS_MIN_KEY_PREFIX`` hex, uniqueness enforced — never a guess),
    in the pushed set first then MAIN's committed row, else None. Mirrors
    :func:`_row_for_label` but selects by KEY (hypothesis:l4-prime-key-is-read-
    from-the-pushed-ref-and-whois-key-with-sig-resolves-the-sig-row-by-pubkey):
    a ``--key`` claim's signature is verified against the very row the caller's
    pubkey named, never a row picked by name/session_ref — before this, the
    key prefix landed in the session_ref slot of :func:`_row_for_label`, which
    matches no name/session_ref and the sig read UNVERIFIABLE forever."""
    def _pick(rows):
        if len(prefix) < WHOIS_MIN_KEY_PREFIX or not all(
                c in "0123456789abcdefABCDEF" for c in prefix):
            return None
        hits = [r for r in (rows or [])
                if (r.get("pubkey") or "").startswith(prefix)]
        if len(hits) == 1:
            return hits[0]
        return None
    if rows is not None:
        row = _pick(rows)
        if row is not None:
            return row
    crow = _pick(_seats_committed_rows(root))
    if crow is None:
        return None
    tagged = dict(crow)
    tagged["_main_committed"] = True
    return tagged


def _label_for_sig(row: dict, sig_scheme: str, fp: str, sig_bytes: bytes,
                   msg: bytes, seat_name: str) -> str:
    """The ONE label for a parsed sig against ONE seat row.

    Shared by the inbox label writer (:func:`_verify_block`) and whois's
    signature verification, so both answer identically. Resolves the
    scheme from the sig's OWN name (the registry is the only coupling),
    then the RETIRED path comes FIRST: a sig whose fingerprint matches a
    ``key_history`` entry on the row AND verifies under that retired pub
    answers ``RETIRED:<fp>`` (never FORGED). Otherwise the row must NAME the
    sig's scheme (a genuine sig under a scheme the row does not declare is
    a forgery) AND verify under the row's current pubkey for ``VERIFIED``.
    """
    try:
        scheme = seatsig.get(sig_scheme)
    except Exception:                                              # noqa: BLE001
        return "FORGED"
    # RETIRED path: a key_history entry matching the sig's fingerprint, whose
    # pub verifies the sig. A retired pub the seat once owned is still a
    # genuine past key -- RETIRED, never FORGED (hypothesis:l4-every-live-
    # row-is-keyed...). The scheme used is the sig's own name.
    for entry in row.get("key_history") or []:
        if entry.get("fp") != fp:
            continue
        entry_pub = entry.get("pub") or ""
        if not entry_pub:
            continue
        try:
            if scheme.verify(bytes.fromhex(entry_pub), msg, sig_bytes):
                return f"RETIRED:{fp}"
        except Exception:                                          # noqa: BLE001
            continue
    # LIVE path: the row declares what it accepts. A row that NAMES no key
    # (no pubkey, no sig_scheme) cannot refute anything -- a signed block
    # from such a row reads UNKEYED <seat> (printed in full, never withheld,
    # never REFUSED), NOT FORGED: FORGED is reserved for a signature that
    # FAILS against a key the row NAMES (hypothesis:l4-a-sig-against-a-row-
    # with-no-key-on-file-reads-unkeyed-never-forged).
    row_scheme = row.get("sig_scheme") or ""
    row_pub = row.get("pubkey") or ""
    if not row_scheme or not row_pub:
        return f"UNKEYED {seat_name}"
    if row_scheme != sig_scheme:
        return "FORGED"
    try:
        pub = bytes.fromhex(row_pub)
    except ValueError:
        return "FORGED"
    if not scheme.verify(pub, msg, sig_bytes):
        return "FORGED"
    return f"VERIFIED {seat_name} ({sig_scheme})"


def _row_generation(row: dict) -> int:
    """A seat row's ``generation`` cell as an int (0 when absent/unparseable),
    so a lagging vs. successor key can be compared by freshness. Clause (3):
    MAIN's committed row is the successor authority only when its generation
    is >= the pushed row's -- a stale MAIN key never overrides a newer one."""
    try:
        return int(row.get("generation") or 0)
    except (TypeError, ValueError):
        return 0


def _seam_main_committed(root: Path, row: dict, seat_name: str,
                         sig_scheme: str, fp: str, sig_bytes: bytes,
                         msg: bytes) -> str:
    """Clause (3) SEAM RULE -- the SECOND consult at the label site, never a
    change to F1's `_merge_main_committed_keys`. A sig the pushed row's own
    key material cannot verify (would-be FORGED) is NOT immediately a forgery:
    origin may be a lagging row still holding the PREDECESSOR key while MAIN's
    COMMITTED row already carries the successor. Consult MAIN's committed row
    for the same seat (`_seats_committed_rows`, `git show HEAD` -- NEVER the
    dirty copy). If that row's pubkey or key_history verifies the sig AND its
    generation is >= the pushed row's, answer ``VERIFIED <seat> (<scheme>,
    main-committed)`` (or ``RETIRED:<fp>``). If MAIN's committed row cannot
    be read (no git, no such seat) answer ``UNVERIFIABLE <seat> (row not on
    origin yet)`` -- printed like UNSIGNED, never withheld, never REFUSED,
    never FORGED. FORGED stays reserved for a signature that verifies under
    NO row anywhere."""
    committed = _seats_committed_rows(root)   # git show HEAD, never dirty copy
    if not committed:
        return f"UNVERIFIABLE {seat_name} (row not on origin yet)"
    ident = row.get("name") or seat_name
    crow = _seat_row_in(committed, ident)
    if crow is None:
        return f"UNVERIFIABLE {seat_name} (row not on origin yet)"
    # MAIN is the successor authority only when STRICTLY fresher than origin
    # (generation greater, never equal): a MAIN row at the same generation as
    # origin's is not provably the successor, so a stale-bound-equal MAIN must
    # not override a keyed origin row (hypothesis falsifier: a pushed key
    # stays authoritative over a not-fresher MAIN key).
    if _row_generation(crow) <= _row_generation(row):
        return "FORGED"
    sub = _label_for_sig(crow, sig_scheme, fp, sig_bytes, msg, seat_name)
    if sub.startswith("VERIFIED"):
        if sub.endswith(")"):
            return sub[:-1] + ", main-committed)"
        return sub + ", main-committed"
    if sub.startswith("RETIRED:"):
        return sub
    # MAIN's committed row exists and is fresh but verifies under no key
    # either: the sig verifies under NO row anywhere -- FORGED.
    return "FORGED"


def _verify_block(root: Path, rows: list | None,
                  meta: dict, text: str) -> str:
    """The ONE label line for a block: VERIFIED / UNSIGNED / FORGED / RETIRED.

    ``VERIFIED <seat> (<scheme>)`` when a ``sig`` line is present and verifies
    against the from-seat's row (pubkey + sig_scheme matched); ``UNSIGNED``
    when there is no sig line; ``UNKEYED <seat>`` when a sig is present but the
    from-seat's row NAMES no pubkey or no sig_scheme (nothing to refute it --
    readers print UNKEYED like UNSIGNED, never withheld, never REFUSED);
    ``UNVERIFIABLE (no row: <name>)`` when the from-seat's row resolves in
    NEITHER the pushed set NOR MAIN's committed rows -- never FORGED, printed
    like UNSIGNED, never REFUSED (hypothesis:l4-an-absent-pushed-row-...);
    ``FORGED`` when a sig is present and fails a check AGAINST A KEY THE ROW
    NAMES (bad shape, unknown scheme, a scheme the row does not
    name, or a signature that does not verify -- but NOT a row with no
    pubkey/sig_scheme, which is UNKEYED, and NOT a row missing everywhere,
    which is UNVERIFIABLE); ``RETIRED:<fp>`` when the sig's
    fingerprint matches a key_history entry of the from-seat and verifies
    under that retired pub. The label is NEVER a drop -- the caller prints
    the block in full under all labels, and under comms.verify==enforcing only
    the EXACT label FORGED is refused.
    """
    sig = meta.get("sig")
    if not sig:
        return "UNSIGNED"
    try:
        sig_scheme, fp, sig_hex = sig.split(":", 2)
        sig_bytes = bytes.fromhex(sig_hex)
    except (ValueError, TypeError):
        return "FORGED"
    row = _row_for_label(root, rows, meta.get("from", ""))
    if row is None:
        return f"UNVERIFIABLE (no row: {meta.get('from', '?')})"
    msg = _canonical_msg(meta.get("ts", ""), meta.get("from", ""),
                         meta.get("to", ""), text).encode()
    label = _label_for_sig(row, sig_scheme, fp, sig_bytes, msg,
                           row.get("name", meta.get("from", "?")))
    # Clause (3) SEAM RULE: a would-be FORGED is the case where origin may be
    # lagging MAIN -- the pushed row holds the PREDECESSOR key while MAIN's
    # COMMITTED row already carries the successor. When the root IS a git
    # work tree, consult MAIN's committed row as a SECOND authority (git show
    # HEAD, never the dirty copy); see `_seam_main_committed` for the full
    # contract. A gitless root has NO MAIN to lag against, so the ordinary
    # FORGED verdict stands (a tampered body / wrong key is forged regardless
    # of git) -- the seam is only ever a way to VERIFY, never to soften a real
    # forgery. This never changes `_label_for_sig`'s own verdicts (SL6.03) nor
    # F1's `_merge_main_committed_keys`.
    if label == "FORGED" and _in_git_repo(root):
        label = _seam_main_committed(root, row,
                                     row.get("name", meta.get("from", "?")),
                                     sig_scheme, fp, sig_bytes, msg)
    # Clause (3) merge tag: when `_load_rows` fell back to MAIN's COMMITTED
    # row for an unkeyed pushed row, name the authority on the VERIFIED line.
    elif row.get("_main_committed") and label.startswith("VERIFIED"):
        # the authority tag sits INSIDE the scheme parens (clause 3: a
        # ``VERIFIED <seat> (<scheme>, main-committed)`` label).
        if label.endswith(")"):
            label = label[:-1] + ", main-committed)"
        else:
            label += ", main-committed"
    return label


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


def _wrap_body(text: str, width: int) -> str:
    """`fold -s` wrap that preserves every line's leading whitespace and
    every blank line EXACTLY (hypothesis:l4-wrap-preserves-leading-
    whitespace-and-trailing-blank-lines-exactly). Each logical line keeps
    its indent (the run of leading spaces/tabs) on the first physical line
    and on every continuation line, and is never folded inside the indent;
    blank lines (interior and trailing) are kept byte-for-byte; a line that
    needs no wrap prints byte-identical (indent, internal runs of spaces,
    trailing spaces all included) because folding touches ONLY lines longer
    than `width` and breaks only at a single space outside the indent, never
    inside a node id, sha, path, URL or [VERIFIED|UNSIGNED|UNKEYED|FORGED]
    label (an over-width token stays whole on its own line). `width <= 0`
    returns the
    text unchanged.
    """
    if width <= 0:
        return text
    res: list[str] = []
    for para in text.split("\n"):
        res.append(_wrap_logical_line(para, width))
    return "\n".join(res)


def _wrap_logical_line(para: str, width: int) -> str:
    """Wrap ONE logical line (the text up to a single newline). If the whole
    line fits in `width`, return it byte-identical. Otherwise fold only the
    content after the leading indent, re-emitting that indent in front of
    every physical line so the indentation survives wrapping.
    """
    if len(para) <= width:
        return para                       # byte-identical: no wrap needed
    stripped = para.lstrip(" \t")
    indent = para[: len(para) - len(stripped)]
    body_txt = stripped
    if not body_txt:
        return para                       # whitespace-only line, kept verbatim
    avail = width - len(indent)
    if avail <= 0:
        return para                       # indent alone exceeds width; no fold inside it
    lines: list[str] = []
    cur = ""
    for word in body_txt.split(" "):
        if not word:
            continue                      # interior multi-space run: fold at it
        if len(word) > avail:
            # an over-long token stays whole on its own line
            if cur:
                lines.append(indent + cur)
                cur = ""
            lines.append(indent + word)
            continue
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= avail:
            cur += " " + word
        else:
            lines.append(indent + cur)
            cur = word
    if cur or not lines:
        lines.append(indent + cur)
    return "\n".join(lines)


def _wrap_block(block: str, width: int) -> str:
    """Wrap ONLY a block's message body (everything after the header's blank
    line), leaving the header line set (`ts:`/`from:`/`to:`/`sig:`) byte-
    identical, so a reader's `grep '^from:'` and the `awk`/read-marker idioms
    keep working. The header-vs-body boundary is the SAME first-blank-line
    rule as `_parse_block`, never re-derived by a second rule. Display-only:
    `width <= 0` returns the block unchanged, byte for byte.
    """
    if width <= 0:
        return block
    b = block[len(MSG_SEP):] if block.startswith(MSG_SEP) else block
    lines = b.splitlines()
    i = 0
    while i < len(lines) and lines[i] != "":
        i += 1
    if i >= len(lines) or not lines[i + 1:]:
        return block                      # header-only block (no body)
    header = lines[:i]
    body_lines = lines[i + 1:]
    wrapped = _wrap_body("\n".join(body_lines), width)
    rebuilt = "\n".join(header) + "\n\n" + wrapped
    # restore the block's EXACT trailing newline count (hypothesis:l4-wrap-
    # preserves-leading-whitespace-and-trailing-blank-lines-exactly clause 2):
    # a body ending in \n\n prints ending in \n\n, not re-collapsed to one.
    rebuilt = rebuilt.rstrip("\n") + "\n" * (len(b) - len(b.rstrip("\n")))
    if block.startswith(MSG_SEP) and not rebuilt.startswith(MSG_SEP):
        rebuilt = MSG_SEP + rebuilt
    return rebuilt


def _sig_fp_from_block(block: str) -> str:
    """The signature fingerprint from a block's `sig:` line
    (`scheme:fp:hex`), or '' when the block carries no parseable sig. Used
    only for the refusal line's `fp <...>` field; the fingerprint itself has
    already been parsed by `_verify_block` to reach the FORGED label, so this
    is a display read, never an authority."""
    try:
        sig = _parse_block(block)[0].get("sig") or ""
    except Exception:                                            # noqa: BLE001
        return ""
    try:
        return sig.split(":", 2)[1]
    except IndexError:
        return ""


def _quarantine_block(root: Path, me: str, block: str) -> Path:
    """Append one refused block's RAW inbox bytes verbatim to
    `<inbox_dir>/quarantine/<me>.md` -- once per DISTINCT block -- and return
    the absolute path written.

    The inbox stores each block as `MSG_SEP + block` (the writer's `_block`
    prepends `---\n`), and `_scan_messages` splits that sep off, so the raw
    bytes are reassembled by prepending `MSG_SEP` when absent. Never rewrites
    or truncates the quarantine file -- always append, `newline=""` so CR
    bytes survive (mur-39 order (d), the same trap the writer documents).

    Dedupe by the sha256 of the raw block bytes (hypothesis:l4-quarantine-
    dedupes-by-block-hash...): `peek` never advances the read cursor, so a
    repeated peek of the same FORGED block would otherwise grow the
    quarantine by one identical copy per call. The quarantine is the durable
    RECORD of what was withheld -- not an event log of how often it was
    refused -- so one distinct block is kept once. The dedupe marker is a
    sidecar `<me>.hashes` (one hex per line, append-only), never a marker
    line inside the quarantine body, so the body stays the exact inbox bytes
    verbatim. A block already recorded is not appended again, but the caller
    still prints the REFUSED line (the refusal happens every event; only the
    durable copy is once)."""
    qdir = _inbox_dir(root) / "quarantine"
    qdir.mkdir(parents=True, exist_ok=True)
    path = qdir / f"{me}.md"
    raw = block if block.startswith(MSG_SEP) else MSG_SEP + block
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    hashes_path = qdir / f"{me}.hashes"
    existing: set[str] = set()
    if hashes_path.is_file():
        try:
            existing = set(hashes_path.read_text().splitlines())
        except OSError:  # a read race never turns a refusal into a crash
            existing = set()
    if h not in existing:
        with open(path, "a", newline="") as f:
            f.write(raw)
        with open(hashes_path, "a", newline="") as f:
            f.write(h + "\n")
    return path.resolve()


def _print_blocks_with_labels(root: Path, me: str, blocks: list[str],
                              wrap: int = 160) -> None:
    """Print one label line before each block, then the block in FULL, its
    message body wrapped at `wrap` columns (display-only; the inbox file and
    read marker are untouched). `wrap <= 0` prints today's byte-for-byte
    output.

    Under comms.verify == "enforcing" AND ONLY THEN, a block whose label is
    EXACTLY `FORGED` (never RETIRED/UNSIGNED/VERIFIED) is refused: one
    `REFUSED FORGED ...` line prints INSTEAD of the block, and the block's RAW
    inbox bytes are appended to the seat's quarantine file. Any other verify
    value, or an absent `comms` block, prints identically to today."""
    labels = _labels_for_blocks(root, blocks)
    enforcing = _comms_config(root).get("verify") == "enforcing"
    for i, block in enumerate(blocks):
        if i > 0:
            print(MSG_SEP, end="")
        if enforcing and labels[i] == "FORGED":
            path = _quarantine_block(root, me, block)
            meta, _ = _parse_block(block)
            fp = _sig_fp_from_block(block)
            print(f"REFUSED FORGED from {meta.get('from','?')} "
                  f"ts {meta.get('ts','?')} fp {fp}: withheld to {path}")
            continue
        print(labels[i])
        print(_wrap_block(block, wrap), end="")


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


def _print_deferred_block(root: Path, me: str, deferred: dict,
                          wrap: int = 160) -> None:
    """Print a stored deferred dm as its OWN block, headed
    `deferred dm from <sender> (<ts>)`, so a reader at a seam sees it as a
    thing of its own rather than folded into the inbox stream
    (hypothesis:l4-wake-repair-is-quiet-honest-and-readable, clause 4).
    The heading is never wrapped; the body is wrapped at `wrap` (detail of
    hypothesis:l4-send-read-and-peek-wrap-message-bodies-at-160-columns-
    display-only). read-only for the record — the caller chooses whether to
    clear it."""
    sender = deferred.get("sender") or "unknown"
    print(f"deferred dm from {sender} ({_deferred_stamp(root, me, deferred)})")
    body = deferred.get("body", "") or ""
    body = _wrap_body(body, wrap)
    if body and not body.endswith("\n"):
        body += "\n"
    print(body, end="")


def _own_inbox_or_refuse(target: str, me: str) -> bool:
    """Refuse a positional `read <target>` whose target is not the resolved
    sender (`me`). True = it is your own inbox (proceed); False = the one
    refusal line went to stderr and NO file was touched (hypothesis:l4-send-
    py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-
    open, claim 1). `peek` never consults this gate - it reads without
    consuming, so it stays open to any target (claim 2). `me` is the RESOLVED
    sender (`_detect_sender`), never `args.me`: `--me` names read positions
    in rooms/dms, not inbox identity, and must not widen the gate (claim 4).
    A resolved sender of 'unknown' (no AGI_AGENT_ID, no AGI_SEAT, no --from)
    refuses every positional target (claim 3).
    """
    if me != "unknown" and target == me:
        return True
    remedy = (f"read: target '{target}' is not you ('{me}'); "
              f"to read your own inbox: send.py read {me}; "
              f"to look at {target}'s without consuming it: "
              f"send.py peek {target}; a dm is --dm {target}")
    if me == "unknown":
        remedy += "; pass --from <seat> if you are that seat"
    print(remedy, file=sys.stderr)
    return False


def read(root: Path, me: str, sender: str | None,
         wrap: int = 160) -> None:
    """Print unread blocks (bodies wrapped at `wrap` columns, display-only)
    and mark them read."""
    _lockdown_warn(root)
    inbox = _inbox_path(root, me)
    blocks, marker_index = _scan_messages(inbox)
    deferred = _read_deferred(root, me)

    if not blocks and deferred is None:
        print(f"inbox for {me}: empty")
        return

    # Observe the coalesced count ONCE, before anything is marked read. The
    # clear below is compare-and-clear (it subtracts this observed value),
    # so a dm that coalesces DURING the read survives instead of being
    # silently zeroed by an unconditional write (L4.294). An empty read
    # returns above, so it never observes nor touches a sidecar.
    observed = _pending_more(root, me)

    # A stored deferred dm prints FIRST, before the inbox blocks, and the
    # record is then cleared — a director who never had an idle pane still
    # sees it at a seam, exactly once (clause 4). The record's own
    # delivered-count semantics for the PANE path are untouched
    # (`_clear_deferred` is the same no-op-guarded helper that path uses).
    if deferred is not None:
        _print_deferred_block(root, me, deferred, wrap=wrap)
        _clear_deferred(root, me)

    # Print inbox blocks, each prefixed by its verification label.
    if blocks:
        _print_blocks_with_labels(root, me, blocks, wrap=wrap)

    # Mark read: find the current last line and add a marker after it.
    # If marker already existed, move it past the blocks we just printed.
    if inbox.is_file():
        # newline="" too: a rewrite here must not be the thing that strips the
        # CR the writer preserved (mur-39 order (d)).
        text = inbox.open("r", newline="").read()
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
    # A consuming read drains the coalesced nudge count too
    # (hypothesis:l4-a-read-clears-the-coalesced-nudge-count): the count is
    # "how many sends coalesced into the one token", and the read has just
    # consumed everything that count stood for, so drop `.nudge.pending` in
    # the same consuming branch. The empty case is already handled by the
    # early return above: a read that consumed nothing must NOT touch the
    # sidecars. `peek` clears nothing, unchanged.
    _clear_pending(root, me, observed)


def peek(root: Path, me: str, wrap: int = 160) -> None:
    """Print unread blocks (bodies wrapped at `wrap` columns, display-only)
    without marking them read."""
    _lockdown_warn(root)
    inbox = _inbox_path(root, me)
    blocks, _ = _scan_messages(inbox)
    deferred = _read_deferred(root, me)

    if not blocks and deferred is None:
        print(f"inbox for {me}: empty")
        return

    # peek shows a stored deferred dm WITHOUT clearing it — a seam without
    # the delivered-count side effects of `read` (clause 4).
    if deferred is not None:
        _print_deferred_block(root, me, deferred, wrap=wrap)

    # Print inbox blocks (peek never marks read).
    if blocks:
        _print_blocks_with_labels(root, me, blocks, wrap=wrap)


# ── rooms (hypothesis:l3w0-send-rooms) ────────────────────────────────────


def send_dm(croot: Path, me: str, other: str, text: str,
            sender: str | None) -> Path:
    """Append a message to the pairwise dm file `<a>--<b>.md`, names sorted.

    A dm may never address or originate from the prime, like a room
    (hypothesis:l3w4-quorum-reviews): the prime is inbox-only, reached only
    through the gated `audience` path.
    """
    _lockdown_warn(locations.find_project_root(croot) or croot)
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
    _lockdown_warn(locations.find_project_root(croot) or croot)
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
            sender: str | None, all_: bool = False, wrap: int = 160) -> list[str]:
    """Render a dm transcript after `since` (or the reader's read position),
    and mark the latest shown message read. `all_` shows the whole transcript
    without advancing the cursor; `wrap` wraps the message bodies."""
    _lockdown_warn(locations.find_project_root(croot) or croot)
    path = _dm_path(croot, me, other)
    blocks = _conv_blocks(path)
    state = _load_state(path)
    shown = _past(blocks, since, state.get(me, 0), me, path, commit=True,
                  all_=all_)
    return render_transcript(shown, wrap=wrap)


def peek_dm(croot: Path, me: str, other: str, since: str | None,
            all_: bool = False, wrap: int = 160) -> list[str]:
    _lockdown_warn(locations.find_project_root(croot) or croot)
    path = _dm_path(croot, me, other)
    blocks = _conv_blocks(path)
    state = _load_state(path)
    shown = _past(blocks, since, state.get(me, 0), me, path, commit=False,
                  all_=all_)
    return render_transcript(shown, wrap=wrap)


def read_room(croot: Path, room: str, participant: str, since: str | None,
              sender: str | None, all_: bool = False,
              wrap: int = 160) -> list[str]:
    _lockdown_warn(locations.find_project_root(croot) or croot)
    path = _room_path(croot, room)
    blocks = _conv_blocks(path)
    state = _load_state(path)
    shown = _past(blocks, since, state.get(participant, 0), participant, path,
                  commit=True, all_=all_)
    return render_transcript(shown, wrap=wrap)


def peek_room(croot: Path, room: str, participant: str, since: str | None,
              all_: bool = False, wrap: int = 160) -> list[str]:
    _lockdown_warn(locations.find_project_root(croot) or croot)
    path = _room_path(croot, room)
    blocks = _conv_blocks(path)
    state = _load_state(path)
    shown = _past(blocks, since, state.get(participant, 0), participant, path,
                  commit=False, all_=all_)
    return render_transcript(shown, wrap=wrap)


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

#: The pushed branch carries the geometry config (hypothesis:l4-a-seat-is-a-
#: post-everywhere): posts.md post-first, the deprecated seats.md as the
#: one-season alias. The prime updates and pushes it at every rotation, so its
#: HEAD is the authoritative answer after a fetch — never the local working
#: tree.
_PUSHED_SEATS = "origin/" + branches.season_main(2)
#: Candidate paths, posts.md FIRST, tried in order by `_pushed_seats`; the
#: first that `git show` succeeds on wins.
_SEATS_REPO_PATHS = (
    ".agi/nodes/.geometry/posts.md",
    ".agi/nodes/.geometry/seats.md",
)


def _load_seats_rows(content: str) -> list:
    """Parse a seats/posts.md byte-string with the engine's node-loader (the
    same path hierarchy.load_seats uses) — reusing the ONE parse, never adding
    a sixth hand-rolled reader. Reads `posts:` first, then the deprecated
    `seats:` key, so a pushed ref in either spelling resolves."""
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as tf:
        tf.write(content)
        tmp = Path(tf.name)
    try:
        nf = _fm.load_node_file(tmp)
        fm = nf.frontmatter or {}
        for key in ("posts", "seats"):
            if key not in fm:
                continue
            rows = fm[key] or []
            if isinstance(rows, list):
                return [dict(r) for r in rows if isinstance(r, dict)]
        return []
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
    `git rev-parse` for the provenance sha and `git show` for the file. The
    live spelling is resolved via ref_candidates (CANONICAL first, the old
    `origin/season/s<N>` as the one-season fallback), so a tree that has not
    been renamed yet still reads its pushed seats — the rename window never
    silently returns None."""
    if ref.startswith("origin/"):
        local_candidates = branches.ref_candidates(ref[len("origin/"):])
        probe_prefix = "origin/"
    else:
        # an opaque non-origin ref is used exactly as given (no fetch: it is
        # not a remote-tracking ref). Parent integration fix L4.306 -- the
        # ref_candidates refactor made the probe prefix unconditional, which
        # contradicted this comment and broke non-origin refs.
        local_candidates = [ref]
        probe_prefix = ""
    sha = None
    live_ref = None
    for name in local_candidates:
        probe = f"{probe_prefix}{name}"
        if do_fetch and probe_prefix:
            fetch = _run_git(root, ["fetch", "origin", name])
            if fetch is None or fetch.returncode != 0:
                continue
        cand = _run_git(root, ["rev-parse", probe])
        if cand is None or cand.returncode != 0:
            continue
        sha = cand
        live_ref = probe
        break
    if sha is None:
        return None
    shown = None
    for path in _SEATS_REPO_PATHS:
        shown = _run_git(root, ["show", f"{live_ref}:{path}"])
        if shown is not None and shown.returncode == 0:
            break
    if shown is None or shown.returncode != 0:
        return None
    # hypothesis:l4-whois-names-the-ref-it-read: return the ref that ACTUALLY
    # resolved (the member of ref_candidates rev-parse accepted), so a whois
    # reader is told the real branch it verified against -- never the
    # canonical candidate, which may not exist on origin yet.
    return _load_seats_rows(shown.stdout), sha.stdout.strip(), live_ref


def _locally_loaded_rows(root: Path) -> list:
    """Fallback rows from the WORKING-TREE file, used only for the UNVERIFIED
    fallback path — never the authority, always clearly labelled so.

    **hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main**
    — the seats node that carries `generation`/`window`/`pid`/`session_ref`/
    `session_id` (the cell a rotation moves and this reader resolves to
    address a live @id/pid) lives in the MAIN checkout's graph; a worktree
    rotation writes MAIN and never the worktree copy, so a sender reading
    from a worktree resolves MAIN's copy and addresses the same row the
    writer wrote."""
    p = _shared_seats_path(root)
    if not p.is_file():
        return []
    try:
        return _load_seats_rows(p.read_text())
    except Exception:                                            # noqa: BLE001
        return []


def _shared_graph_root(root: Path) -> Path:
    """MAIN's project graph root (the directory holding `.agi`), never the
    caller's worktree — the ONE checkout the shared-seats reader (and the
    committed-row reader) must both address. A linked-worktree call rebases to
    MAIN through `locations.git_common_root`; a caller in the main checkout or
    outside git keeps its own literal root (the legacy/graph-root and
    test-fixture layouts read exactly the file they mean)."""
    graph = Path(root)
    main = locations.git_common_root(graph)
    if main is not None and main != graph:
        # inside a git repo: the MAIN checkout's graph root.
        graph = locations.find_project_root(main) or main
    return graph


def _shared_seats_path(root: Path) -> Path:
    """The MAIN checkout's `nodes/.geometry/seats.md`, identity for a
    non-worktree caller — the resolution `locations.git_common_root` performs
    (hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main).
    The seats row a rotation writes lives in MAIN, so this reader addresses
    the same copy. Only a real linked-worktree call rebases to MAIN; a caller
    in the main checkout or outside git keeps its own literal root (the
    legacy/graph-root and test-fixture layouts read exactly the file they
    mean)."""
    graph = _shared_graph_root(root)
    if (graph / locations.GRAPH_DIR_NAME / "nodes").is_dir():
        graph = graph / locations.GRAPH_DIR_NAME
    return geometry_config.geometry_config_path(graph) or (
        graph / "nodes" / ".geometry" / "posts.md")


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

#: whois `--key` resolves a row by a PREFIX of its `pubkey` cell. The prefix
#: must be at least this many chars and the MATCH must be UNIQUE across rows —
#: a shorter or ambiguous prefix is NO-MATCH (never a guess)
#: (hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-
#: ref-is-empty...).
WHOIS_MIN_KEY_PREFIX = 8


def _whois_answer(who: dict, match_display: str, claim: str | None) -> tuple[int, str]:
    """Build the IS-AUTHORIZED/SEAT answer line for one matched row.
    ``match_display`` is the text that stands where the session_ref would
    because the row was found by key prefix or by seat name (``by key: <p>`` /
    ``by name: <n>``). When the row names a CURRENT ``window`` cell the line
    carries it (``window <@id>``), so a by-key by-name answer still yields F3's
    SendMessage address in one call — the authority row's own window, printed
    by the same resolver whois always used."""
    name = who.get("name", "?")
    role = who.get("role", "?")
    win = who.get("window") or ""
    winpart = f"  window {win}" if win else ""
    if claim:
        ok = (claim == name) or (claim == role)
        verdict = "IS-AUTHORIZED" if ok else "IS-NOT-AUTHORIZED"
        return ((WHOIS_OK if ok else WHOIS_NOT_AUTHORIZED),
                f"{verdict}: {match_display} vs claim {claim!r} "
                f"-> actual seat {name}, role {role}{winpart}")
    return WHOIS_OK, f"SEAT: {match_display} -> seat {name}, role {role}{winpart}"


def _resolve_rows(rows: list, session_ref: str,
                  claim: str | None, target: tuple | None = None) -> tuple[int, str]:
    """Answer the is-this-who-they-say question for one ref. Two directions:
    with no --claim, name the seat + role the ref belongs to; with
    --claim NAME, answer whether this ref IS that row (a ref present in the
    table but under a DIFFERENT name/role answers NO — the impersonation case).

    L4.114 (r3): a ref that is not an exact `session_ref` match is still
    authorized when it is a PREFIX of a row's `session_id` uuid, at least
    WHOIS_MIN_SESSION_ID_PREFIX chars — a shorter prefix is refused (never
    treated as a match).

    With ``target`` (a ``("key", prefix)`` or ``("seat", name)`` tuple, from
    ``--key`` / ``--seat``) the row is resolved by its ``pubkey`` PREFIX or
    by its ``name`` instead of by session_ref, and the answer names the axis
    that found it."""
    if target is not None:
        mode, val = target
        if mode == "seat":
            hits = [r for r in rows if r.get("name") == val]
            if hits:
                return _whois_answer(hits[0], f"by name: {val}", claim)
            return (WHOIS_NO_MATCH,
                    f"NO-MATCH by name: {val!r} belongs to no seat row")
        # mode == "key": a UNIQUE pubkey-prefix match, min 8 chars.
        if len(val) < WHOIS_MIN_KEY_PREFIX or not all(
                c in "0123456789abcdefABCDEF" for c in val):
            return (WHOIS_NO_MATCH,
                    f"NO-MATCH by key: {val!r} (< {WHOIS_MIN_KEY_PREFIX} hex "
                    "chars) is too short or not hex to authorize by pubkey "
                    "prefix")
        hits = [r for r in rows if (r.get("pubkey") or "").startswith(val)]
        if len(hits) > 1:
            return (WHOIS_NO_MATCH,
                    f"NO-MATCH by key: {val!r} matches {len(hits)} rows "
                    "(ambiguous pubkey prefix — never a guess)")
        if not hits:
            return (WHOIS_NO_MATCH,
                    f"NO-MATCH by key: {val!r} belongs to no seat row's pubkey")
        return _whois_answer(hits[0], f"by key: {val}", claim)
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


def _whois_msg_meta(msg_text: str) -> tuple[str, str]:
    """`(ts, from)` from the canonical ``--msg`` bytes ``ts\nfrom\nto\n\ntext``
    -- the one shape whois is handed to verify a sig against. The refusal line
    names them so a withheld whois traces to a real sender the same way a
    withheld inbox block does. Absent-line guards return ``?`` rather than
    raising or misindexing a degenerate msg."""
    lines = msg_text.split("\n")
    ts = lines[0] if lines else "?"
    from_id = lines[1] if len(lines) > 1 else "?"
    return ts, from_id


def _whois_sig_fp(sig_line: str | None) -> str:
    """The fingerprint field of a ``scheme:fp:hex`` sig line, or ``?``."""
    try:
        return sig_line.split(":", 2)[1]
    except (AttributeError, IndexError):
        return "?"


_SAFE_REF_RE = re.compile(r"[^A-Za-z0-9._-]+")


def _sanitize_ref(session_ref: str) -> str:
    """The safe FILENAME for a CLI-provided session_ref: keep ONLY
    ``[A-Za-z0-9._-]``, dropping everything else (so ``/`` and ``..``-shaped
    traversal can never escape the quarantine dir).

    REFUSES in one line (exit 2) when the sanitized ref is EMPTY (or
    strips-to-nothing) or LONGER than 64 characters, BEFORE any path is built:
    a legit harness ref is 6-8 chars, so a 65-char or empty session_ref is
    garbage/noise and must not silently truncate into a filename or craft one
    the caller never meant (SL7.02 clause (5)). The refusal is the caller's
    gate -- never a fallback string -- so no path is ever derived from a ref
    the operator did not intend.
    """
    safe = _SAFE_REF_RE.sub("", session_ref)
    if not safe or len(safe) > 64:
        print(f"ERR: bad session_ref {session_ref!r}: must be 1-64 chars of "
              f"[A-Za-z0-9._-] after sanitizing", file=sys.stderr)
        raise SystemExit(2)
    return safe


def _quarantine_whois(root: Path, session_ref: str, sig_line: str | None,
                      msg_text: str) -> Path:
    """Append one FORGED whois's OWN signed bytes to
    `<inbox_dir>/quarantine/<safe>.md` and return the absolute path.

    whois has no inbox block to withhold (the sig + msg travel on the command
    line, not the wire), so the natural record IS the ``--sig`` line plus the
    canonical ``--msg`` text whois was handed. The filename is derived from a
    SANITIZED session_ref (only ``[A-Za-z0-9._-]`` survive; an EMPTY or
    >64-char ref is REFUSED with exit 2 before this dir is even created), so no
    CLI value can choose a path -- the ORIGINAL raw ref is written as the
    record's first line so provenance survives the sanitization. SAME append
    semantics as :func:`_quarantine_block`
    (`mkdir(parents=True, exist_ok=True)`, `open(path, "a", newline="")`) --
    never rewrites or truncates, and ``newline=""`` keeps any CR surviving."""
    safe = _sanitize_ref(session_ref)   # REFUSES (exit 2) on empty or >64, pre-path
    qdir = _inbox_dir(root) / "quarantine"
    qdir.mkdir(parents=True, exist_ok=True)
    path = qdir / f"{safe}.md"
    record = f"{session_ref}\n{sig_line or '?'}\n{msg_text}\n"
    with open(path, "a", newline="") as f:
        f.write(record)
    return path.resolve()


def _whois_enforced_refusal(root: Path, session_ref: str, label: str | None,
                            sig_line: str | None,
                            msg_text: str | None) -> str | None:
    """Is this whois REFUSED under enforcement, and if so under what bytes?

    Returns the ONE refusal line when the signature label is EXACTLY
    ``FORGED`` AND the config says ``comms.verify == "enforcing"``. The caller
    then returns WHOIS_NOT_AUTHORIZED (2) EVEN IF the authority answer was 0,
    and prints this line INSTEAD of its normal text -- the same shape as
    clause (1)'s inbox refusal, so a withheld whois reads identically.

    ``--msg`` changes only WHAT is withheld: with one, the forged sig+sig_msg
    is written to the quarantine (SL7.02 clause (5) caps/refuses the derived
    filename's ref); without one there are no canonical bytes to trace a ts/from
    from and none to write, but the forgery is STILL refused (exit 2) and the
    line says so -- F4 (SL6.08) made whois exit 2 on FORGED under enforcing
    with or without ``--msg``.

    ``None`` means no refusal: whois keeps today's bytes and exit, unchanged.
    A non-FORGED label (VERIFIED/UNSIGNED/RETIRED), a non-enforcing verify, or
    an EMPTY ``session_ref`` / >64-char ref all fall through to today's
    INFORMATIONAL behavior or a ref refusal -- Prime ruling A stays the
    default, and enforcement is the ONE exception, when the config says so.
    """
    if label != "FORGED":
        return None
    if _comms_config(root).get("verify") != "enforcing":
        return None
    fp = _whois_sig_fp(sig_line)
    if not msg_text:
        # Under enforcing a FORGED label is refused even without a --msg to
        # withhold: there are no canonical bytes to trace a ts/from from and
        # none to write to the quarantine, but the forgery is still refused
        # (exit 2). Do NOT fabricate a quarantine file -- nothing was handed.
        return (f"REFUSED FORGED for {session_ref!r} fp {fp}: no --msg to "
                f"withhold, nothing quarantined")
    path = _quarantine_whois(root, session_ref, sig_line, msg_text)
    ts, from_id = _whois_msg_meta(msg_text)
    return (f"REFUSED FORGED from {from_id} ts {ts} fp {fp}: "
            f"withheld to {path} (ref {session_ref!r})")


def _whois_sig_label(root: Path, rows: list | None, session_ref: str,
                     sig_line: str | None, msg_text: str | None,
                     target: tuple | None = None) -> str | None:
    """The signature label for a whois call, or None when no signature was
    given (nothing to verify). INFORMATIONAL only: the caller (whois) reports
    this in the text but NEVER keys its exit code on it (Prime ruling A).

    ``UNSIGNED`` when no signed line was given; otherwise resolve the row for
    ``session_ref`` through the ONE shared resolver (:func:`_row_for_label` --
    pushed row first, then MAIN's committed row, then UNVERIFIABLE) and answer
    exactly as the inbox writer does. WITH ``target`` a ("key", prefix) tuple
    (from ``--key``), the row is the one whose PUBKEY matches the prefix
    (:func:`_row_for_pubkey`, unique, min WHOIS_MIN_KEY_PREFIX) -- so a by-
    key claim's signature is verified against the row the caller's pubkey
    named, never a row picked by name/session_ref
    (hypothesis:l4-prime-key-is-read-from-the-pushed-ref-and-whois-key-with-
    sig-resolves-the-sig-row-by-pubkey). And answer
    ``VERIFIED`` / ``FORGED`` / ``RETIRED:<fp>`` / ``UNVERIFIABLE (no row:
    <name>)`` exactly as the inbox writer does (:func:`_label_for_sig`), so
    whois and the speaker agree byte-for-byte. A row missing from NEITHER the
    pushed set nor MAIN's committed rows reads UNVERIFIABLE, never FORGED;
    a main-committed key that verifies answers ``VERIFIED ... main-committed``
    just like the inbox seam. """
    if not sig_line:
        return "UNSIGNED"
    try:
        sig_scheme, fp, sig_hex = sig_line.split(":", 2)
        sig_bytes = bytes.fromhex(sig_hex)
    except (ValueError, TypeError):
        return "FORGED"
    if target is not None and target[0] == "key":
        # --key --sig: the signature row is the one the caller's PUBKEY named
        # (unique prefix, min WHOIS_MIN_KEY_PREFIX), never a name/session_ref
        # pick -- a by-key claim's sig MUST verify against its own row.
        row = _row_for_pubkey(root, rows, target[1])
        if row is None:
            return f"UNVERIFIABLE (no row: key {target[1]})"
    else:
        row = _row_for_label(root, rows, session_ref)
        if row is None:
            return f"UNVERIFIABLE (no row: {session_ref})"
    # --msg IS the exact canonical message bytes the sig covers; the caller
    # reconstructs them (ts\nfrom\nto\n\ntext), because only the ONE canonical
    # shape can verify. We do not re-derive it here.
    msg = (msg_text or "").encode()
    label = _label_for_sig(row, sig_scheme, fp, sig_bytes, msg,
                           row.get("name", session_ref))
    # name the authority like the inbox seam: a VERIFIED answer resolved from
    # MAIN's committed row reads ``<scheme>, main-committed``.
    if row.get("_main_committed") and label.startswith("VERIFIED"):
        if label.endswith(")"):
            label = label[:-1] + ", main-committed)"
        else:
            label += ", main-committed"
    return label


def whois(root: Path, session_ref: str, claim: str | None,
          source: str = _PUSHED_SEATS, do_fetch: bool = True,
          sig_line: str | None = None, msg_text: str | None = None,
          target: tuple | None = None):
    """Resolve session_ref against the PUSHED config:seats.

    ``target`` is an optional ``("key", prefix)`` / ``("seat", name)`` tuple
    (from ``--key`` / ``--seat``): the row is resolved by pubkey prefix or by
    name instead of by session_ref, and the answer names that axis.

    Returns `(exit, text)` using the WHOIS_* codes: 0 only when the answer is
    both authoritative AND affirmative, 1 UNVERIFIED, 2 NOT-AUTHORIZED,
    3 NO-MATCH. Provenance (source ref + commit sha) is in every verified
    answer. When a ``sig_line`` (and ``msg_text``) is given, whois ALSO
    verifies the signature against the resolved row and reports the label
    (VERIFIED/UNSIGNED/FORGED/RETIRED) as an INFORMATIONAL extra line.

    Clause (3): under ``comms.verify == "enforcing"`` AND ONLY THEN, a label
    EXACTLY ``FORGED`` returns WHOIS_NOT_AUTHORIZED (2) EVEN IF the authority
    answer was code 0, and prints one ``REFUSED FORGED ...`` line instead of the
    normal text -- the sig is the reader's gate the same way it gates the inbox.
    With a ``--msg`` the refused sig+msg is written to the quarantine; without
    one there are no bytes to withhold, but the forgery is STILL refused and the
    line says so (nothing is quarantined). Any other verify value or a
    non-FORGED label returns today's bytes and exit unchanged: Prime ruling A
    keeps the sig label off the exit axis except at this one enforced seam.
    """
    seeded = _pushed_seats(root, source, do_fetch)
    if seeded is None:
        # Pushed authority unreachable. Do NOT silently answer from the working
        # tree: answer, but label it UNVERIFIED and exit non-zero. An
        # unauthoritative answer must never exit 0.
        local = _locally_loaded_rows(root)
        _code, answer = _resolve_rows(local, session_ref, claim, target)
        # hypothesis:l4-whois-names-the-ref-it-read: name the CANDIDATES the
        # resolver tried (canonical first, legacy fallback) -- never a single
        # unresolved name a reader cannot act on.
        if source.startswith("origin/"):
            tried = ", ".join(
                "origin/" + c
                for c in branches.ref_candidates(source[len("origin/"):]))
        else:
            tried = source
        text = (f"UNVERIFIED {session_ref}: pushed ref(s) {tried} unreachable; "
                f"reading working tree, NOT authoritative — treat as unproven\n"
                + answer)
        label = _whois_sig_label(root, local, session_ref, sig_line, msg_text,
                                 target=target)
        if label is not None:
            text += f"\n{label}"
        # A forged sig is refused even on the unproven path: 2 outranks 1,
        # and a refused forgery must never read as merely 'unverified'.
        refusal = _whois_enforced_refusal(root, session_ref, label,
                                          sig_line, msg_text)
        if refusal is not None:
            return WHOIS_NOT_AUTHORIZED, refusal
        # UNVERIFIED outranks whatever the working tree happened to say: the
        # caller must not act on an answer we could not authenticate, even a
        # negative one.
        return WHOIS_UNVERIFIED, text
    rows, sha, live_ref = seeded
    code, answer = _resolve_rows(rows, session_ref, claim, target)
    # hypothesis:l4-whois-names-the-ref-it-read: name the ref that ACTUALLY
    # resolved, never the unresolved canonical candidate.
    text = f"{answer}  (verified against {live_ref} @ {sha})"
    # INFORMATIONAL signature label: never part of the exit decision -- EXCEPT
    # clause (3)'s enforced FORGED refusal, checked below.
    label = _whois_sig_label(root, rows, session_ref, sig_line, msg_text,
                             target=target)
    if label is not None:
        text += f"\n{label}"
    refusal = _whois_enforced_refusal(root, session_ref, label,
                                      sig_line, msg_text)
    if refusal is not None:
        # FORGED under enforcing returns 2 EVEN IF the authority answer was 0.
        return WHOIS_NOT_AUTHORIZED, refusal
    return code, text


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="one-verb agent comms",
        epilog=_LOCKDOWN_RESERVED_HELP)
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
    p_read.add_argument("--wrap", type=int, default=160,
                        help="wrap message bodies at N columns (0 = raw)")

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
    p_peek.add_argument("--wrap", type=int, default=160,
                        help="wrap message bodies at N columns (0 = raw)")

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
    p_whois.add_argument("session_ref", nargs="?", default=None,
                         help="the session_ref (e.g. 7902ac) to verify "
                              "(omit when using --key or --seat)")
    p_whois.add_argument("--key", default=None,
                         help="resolve by a UNIQUE prefix (>= 8 hex chars) "
                              "of a row's pubkey instead of by session_ref "
                              "(the prime row's pubkey is filled at every "
                              "rotation when its session_ref is empty)")
    p_whois.add_argument("--seat", "--post", action=geometry_config.SeatAction,
                         default=None,
                         help="resolve by a row's seat name instead of by "
                              "session_ref")
    p_whois.add_argument("--claim", default=None,
                         help="claimed seat name or role; answer whether this "
                              "ref IS that row (impersonation check)")
    p_whois.add_argument("--source", default=_PUSHED_SEATS,
                         help=f"git ref to read seats from (default: pushed "
                              f"{_PUSHED_SEATS})")
    p_whois.add_argument("--no-fetch", dest="no_fetch", action="store_true",
                         help="skip the `git fetch` before reading")
    p_whois.add_argument("--sig", dest="sig", default=None,
                         help="a signed header line `scheme:fp:hex` to verify "
                              "against the resolved seat's row; the label "
                              "(VERIFIED/FORGED/RETIRED) is INFORMATIONAL and "
                              "does not gate the exit -- EXCEPT a FORGED label "
                              "under comms.verify==enforcing exits 2 (clause 3)")
    p_whois.add_argument("--msg", dest="msg", default=None,
                         help="the EXACT canonical message bytes the sig "
                              "covers (ts\nfrom\nto\n\ntext), to verify it "
                              "against (with --sig)")

    p_keygen = sub.add_parser(
        "keygen", parents=[common],
        help="mint a seat signing key under <sessions>/seats/<seat>.key (mode "
             "0600); prints and writes the row cells (pubkey, sig_scheme, "
             "enc_scheme: none) into the seat's own config:seats row -- or "
             "with --all-live, the prime keys every LIVE row that has no "
             "pubkey (hypothesis:l4-every-live-row-is-keyed...)",
        epilog=_LOCKDOWN_RESERVED_HELP)
    p_keygen.add_argument("--seat", "--post", action=geometry_config.SeatAction, default=None, help="seat name")
    p_keygen.add_argument("--scheme", default=seatsig.DEFAULT_SCHEME,
                          help="swappable scheme name (default "
                               f"{seatsig.DEFAULT_SCHEME})")
    p_keygen.add_argument("--all-live", dest="all_live",
                          action="store_true",
                          help="key every LIVE config:seats row lacking a "
                               "pubkey; run by the prime seat")

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
        wrap = args.wrap
        if args.room is not None:
            for line in read_room(croot, args.room, me, args.since, sender,
                                  all_, wrap=wrap):
                print(line)
            return 0
        if args.dm is not None:
            for line in read_dm(croot, me, args.dm, args.since, sender, all_,
                                wrap=wrap):
                print(line)
            return 0
        if not args.target:
            print("ERR: read needs a target (inbox) or --room/--dm",
                  file=sys.stderr)
            return 1
        # Inbox identity is the RESOLVED sender, never `args.me` (claim 4):
        # `--me` names read positions in rooms/dms, not whose inbox a
        # positional read may consume. Refuse a foreign target (claim 1).
        resolved = _detect_sender(sender)
        if not _own_inbox_or_refuse(args.target, resolved):
            return 2
        read(root, args.target, sender, wrap=wrap)
        return 0

    if args.verb == "peek":
        me = args.me or _detect_sender(sender)
        all_ = getattr(args, "all_", False)
        wrap = args.wrap
        if args.room is not None:
            for line in peek_room(croot, args.room, me, args.since, all_,
                                  wrap=wrap):
                print(line)
            return 0
        if args.dm is not None:
            for line in peek_dm(croot, me, args.dm, args.since, all_,
                                wrap=wrap):
                print(line)
            return 0
        if not args.target:
            print("ERR: peek needs a target (inbox) or --room/--dm",
                  file=sys.stderr)
            return 1
        peek(root, args.target, wrap=wrap)
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
        # --key / --seat are alternatives to the positional ref, mutually
        # exclusive with it and with each other. Exactly one resolution axis
        # must be given.
        given = [x for x in (args.session_ref, args.key, args.seat)
                 if x is not None]
        if len(given) != 1:
            print("ERR: whois needs exactly one of <session_ref>, --key, or "
                  "--seat", file=sys.stderr)
            return 1
        target = None
        if args.key is not None:
            target = ("key", args.key)
        elif args.seat is not None:
            target = ("seat", args.seat)
        rc, text = whois(root, given[0], args.claim, args.source,
                         not args.no_fetch, sig_line=args.sig,
                         msg_text=args.msg, target=target)
        print(text)
        return rc

    if args.verb == "keygen":
        return _cli_keygen(root, args)

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


def _cli_keygen(root: Path, args) -> int:
    """The keygen CLI: exit 0 when every requested key was minted AND its
    row write landed; 1 on a refusal (single-seat refusal, or an unnamed
    seat without --all-live); 2 when the key WAS minted but the row write
    was refused or the seat row was not found (clause (1)) -- the key on
    disk with no pubkey on the row would otherwise read UNKEYED forever
    under an exit 0. The one stderr line is printed by keygen._keygen_row_refused."""
    actor = _detect_sender(getattr(args, "from_id", None))
    if getattr(args, "all_live", False):
        out = keygen(root, all_live=True, scheme_name=args.scheme,
                     actor=actor)
        if out is not None and not _last_keygen_row_ok:
            return 2
        return 0 if out is not None else 1
    if not args.seat:
        print("ERR: keygen needs --seat (or --all-live)", file=sys.stderr)
        return 1
    out = keygen(root, args.seat, args.scheme, actor=actor)
    if out is not None and not _last_keygen_row_ok:
        return 2
    return 0 if out is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())
