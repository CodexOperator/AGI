#!/usr/bin/env python3
# rotation-alert.py — an agi rotation warning that arrives UNPROMPTED.
#
# hypothesis:l4-a-meter-you-must-remember-to-read-is-a-coin-flip
#
# A rotation MASTER must stop being a coin-flip action: a meter you have to
# REMEMBER to read is a discipline that depends on the one faculty a session
# loses as it fills up (it proved out twice: gen IV ran 67% past its line
# believing it was under it; gen III closed at 0.56 and wrote a worse brief).
#
# This hook is a UserPromptSubmit side-channel that speaks into the session's OWN
# turn: the hook runner hands it a JSON payload on stdin carrying that
# session's own transcript path and session id, so it structurally cannot
# capture another seat's transcript the way the fail-open meter did
# (`hypothesis:l4-the-meter-pinned-another-sessions-transcript`).
#
# ── THE ARCHITECTURAL POINTS, IN THE ORDER THE ROUND GUARDS THEM ────────────
#   P1  USE THE HANDED TRANSCRIPT PATH AND NOTHING ELSE. Never call any
#       resolver, never read a `.meter` pin, never glob a project dir, never
#       take the newest anything. The handed path is the ENTIRE point.
#   P2  VERIFY THE PAYLOAD FIELD NAMES, DO NOT ASSUME THEM, and FAIL CLOSED
#       with a named error if the field you rely on is absent.
#   P3  ESCALATE, DO NOT PING ONCE. Once per band below the rotation line,
#       silence when nothing changed; EVERY firing once at/over the line,
#       because past it the emergency does not expire.
#   P4  PER-SESSION STATE, keyed by the SESSION ID from the payload. Never by
#       seat name, never in a dir shared across agents (No shared state is
#       routed to the main checkout — that is the boundary that produced the
#       bug this round exists to prevent).
#   P5  NAME THE EXACT NEXT COMMAND, INCLUDING THE EXPLICIT `--session-log`
#       PATH, interpolated from the handed transcript path — a copy-pasteable
#       line. A reminder that only says "you should rotate" costs a turn.
#   P6  THE DENOMINATOR IS AN OPEN QUESTION: SAY WHAT YOU MEASURED AND FAIL
#       CLOSED if the window cannot be established for the running model —
#       a confident wrong fraction is the disease, not the cure.
#   P7  SILENT and exit 0 outside an agi project and on an unreadable
#       transcript — this runs on every session on the box and must never
#       break one.
#
# REGISTRATION (do NOT install — that is the owner's call, and registering it
# globally changes every session on this box). The Prime INSTALLED this hook
# under `UserPromptSubmit` — copy the shape that is ACTUALLY in
# `~/.claude/settings.json` and never edit that file:
#
#    "UserPromptSubmit": [ { "hooks": [
#        { "type": "command",
#          "command": "python3 /home/ubuntu/work/agi/extensions/agi/hooks/rotation_alert.py",
#          "timeout": 10,
#          "statusMessage": "agi rotation meter..." } ] } ]
#
# The hook must receive the runner's JSON on stdin UNCHANGED. (Claude Code's
# own `cc-session-start.sh` in this repo is a bash sibling and reads env vars
# instead; this one is stdin-driven because the rotation alert needs the
# handed transcript path, which env vars do not carry.)
"""UserPromptSubmit rotation-alert hook — stdin JSON in, warning text out."""

import json
import os
import re
import sys
from pathlib import Path

# The sash the hook is told to hand back when it fires. This is the ONE
# high-signal quantity: the operator copies it and the next command is whole.
# 🔴 `--pin` TAKES A PATH. This read `--seat {seat} --pin --session-log ...`,
# so `--pin` swallowed the `--session-log` FLAG as its own value and the
# command could not run. The hook's whole reason for existing is P5 — hand
# over a copy-pasteable next command — so an unrunnable one is not a typo,
# it is the deliverable failing. Same shape as a guard whose printed remedy
# does not clear the guard (hypothesis:l4-the-gate-is-on-a-credential-the-
# spawn-will-not-use, item 2): the reader does exactly what they were told
# and it does not work, so they conclude the tool is broken.
ROTATE_CMD = (
    "python3 {bin}/rotate.py meter --pin {pin} --session-log {transcript}"
)
#: Used when the seat cannot be derived: still correct, still runnable, and
#: it reads the caller's OWN handed transcript, which is the load-bearing half.
ROTATE_CMD_NO_SEAT = "python3 {bin}/rotate.py meter --session-log {transcript}"


def _seat_from_cwd(cwd: str) -> str | None:
    """The seat name for a seat worktree, or None.

    A seat runs in `<repo>/.agi/worktrees/seat-<name>`, so the name is
    derivable without reading any registry. None when the caller is not in a
    seat worktree — in which case we print the command WITHOUT `--pin`
    rather than guess a pin path, because guessing which pin belongs to you
    is the original defect this whole chain is about.
    """
    for part in Path(cwd).resolve().parts:
        if part.startswith("seat-"):
            return part[len("seat-"):] or None
    return None

def _seat_rows(root: Path) -> list:
    """Rows of the `config:seats` node — `.agi/nodes/.geometry/seats.md`.

    The node's frontmatter carries a YAML `seats:` key whose values are inline
    JSON objects, one per seat. We read what `dispatch.py --seat` and
    `rotate.py meter --seat` read — no second copy of the registry.
    """
    path = root / "nodes" / ".geometry" / "seats.md"
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("- "):
            continue
        try:
            rows.append(json.loads(s[2:]))
        except (json.JSONDecodeError, ValueError):
            continue
    return rows


def _main_root(root: Path) -> Path:
    """The integration tree (MAIN checkout) graph root, or `root` unchanged.

    A seat's OWN worktree `root` carries a possibly-STALE `config:seats`: its
    row is merged from `origin/season/s2` only at the seat's next merge, while
    the Prime edits `rotate_at` on the main checkout — so a line the Prime
    lowers on main does not reach a working seat for an entire generation.
    The main checkout is one call away — `locations.git_common_root`, which is
    already importable (the hook inserts `<hooks>/../bin` on sys.path).

    `git_common_root` returns the REPO root, not the graph root, so the graph
    root is re-derived there with `find_project_root` — the same two-step
    `shared_project_root` uses, and it returns the INPUT graph root (identity)
    when the two coincide, which is exactly the "running in the main checkout"
    signal the caller needs.

    Never a hard dependency: when the dir is not inside a git worktree or git
    fails, this returns `root` unchanged and we keep reading the worktree row
    (P7 — the hook runs on every session and must never break one).
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import locations  # noqa: PLC0415 — lazy, like _canonical_pin
        main = Path(locations.git_common_root(root))
        if main == root:
            return root
        main_graph = locations.find_project_root(main)
        return Path(main_graph).resolve() if main_graph else root
    except Exception:
        return root


def _seat_line(root: Path, cwd: str, ladder_default: float):
    """(seat, threshold, source_label) — the line a seat is measured against.

    A seat rotates at its OWN `rotate_at` from its `config:seats` row, not at
    the ladder's `director_rotate_at`. The seat is identified by `AGI_SEAT`
    when present, else by the cwd (the `seat-<name>` convention, with a
    path-match fallback on a row's OWN `worktree` for a seat outside that
    convention — KEPT on evidence below: the schema allows a worktree string
    outside the convention and a red-first test reaches that branch).

    The `rotate_at` VALUE is read MAIN-CHECKOUT-first: the integration tree
    (locations.git_common_root) may carry a newer `rotate_at` than this
    worktree's stale row. The worktree row wins only when the main checkout
    has no row for the seat. The emitted source string NAMES which tree won:
    `config:seats <seat>.rotate_at (main checkout)` vs `(worktree)`. A
    rotate_at that is missing, unparseable or NON-POSITIVE falls through to
    the ladder default — the guard is intact (0 must never become a 0.0
    threshold, or `fraction/threshold` in `_emit` divides by zero).
    """
    seat = os.environ.get("AGI_SEAT")
    if seat is None:
        seat = _seat_from_cwd(cwd)
        if seat is None:
            # Fidelity against the claim's word "the cwd equals a row's
            # worktree": a row may name a worktree that does not follow the
            # `seat-<name>` convention, so a path-match on the row's OWN
            # `worktree` field beats the convention parse when it exists.
            # KEPT (not deleted): the seats schema allows an arbitrary
            # worktree string, and test_h reaches this branch with a row whose
            # worktree is outside the convention — see that test's docstring
            # for the evidence. It is dead in the REAL registry only by
            # convention (every perpetual seat uses `seat-<name>`).
            cwd_res = Path(cwd).resolve()
            for row in _seat_rows(root):
                wt = row.get("worktree")
                if isinstance(wt, str) and wt:
                    try:
                        base = root.parent if wt.startswith(".agi/") else root
                        wt_res = (base / wt).resolve()
                    except (OSError, TypeError):
                        continue
                    if cwd_res.is_relative_to(wt_res) or cwd_res == wt_res:
                        seat = row.get("name")
                        break
    if not seat:
        return seat, ladder_default, "ladder.director_rotate_at"

    # MAIN-CHECKOUT ROW WINS. Read rotate_at from the integration tree first;
    # fall back to the worktree row ONLY when the main checkout has no row for
    # the seat (a main row that is present but non-positive/unparseable goes
    # to the LADDER, never to the worktree — see the guard below).
    main_root = _main_root(root)
    if main_root == root:
        # In the main checkout: one tree, and it IS the main checkout.
        candidates = [(root, "main checkout")]
    else:
        candidates = [(main_root, "main checkout"), (root, "worktree")]
    for cand_root, tree_label in candidates:
        for row in _seat_rows(cand_root):
            if row.get("name") != seat:
                continue
            if "rotate_at" not in row:
                continue
            try:
                rt = float(row["rotate_at"])
            except (TypeError, ValueError):
                # a row that declares rotate_at but cannot be parsed = missing.
                return seat, ladder_default, "ladder.director_rotate_at"
            # 🔴 NON-POSITIVE is the same as MISSING. A rotate_at of 0 (or
            # negative) must fall through to the ladder default, never become
            # threshold 0.0: `over_line = fraction >= 0.0` is then ALWAYS True
            # and `_emit` computes `fraction / threshold` → **ZeroDivisionError**
            # (P6: fail closed, never emit a confident wrong fraction — and a
            # crash is the loud wrong way). It goes to the LADDER, not to the
            # other tree, because the seat's own row is authoritative when it
            # exists; only a genuinely absent row falls through to the next
            # tree.
            if rt > 0:
                return (seat, rt,
                        f"config:seats {seat}.rotate_at ({tree_label})")
            return seat, ladder_default, "ladder.director_rotate_at"
    return seat, ladder_default, "ladder.director_rotate_at"


#: Headline used at and above the rotation line (fires every call).
AT_OR_OVER_TITLE = "## ⚠️  ROTATION OWED NOW — at or over the line"
#: Headline used while below the line but crossing a band (fires once per band).
BENEATH_TITLE = "## ⚠️  approaching rotation"

#: Bands are fractions of the rotation threshold, in rising order. Below the
#: line we emit at most ONCE per band; crossing the NEXT band emits again.
BAND_FRACTIONS = (0.40, 0.55, 0.70, 0.85, 1.0)


class RotationAlertError(Exception):
    """Named, fail-closed error when the payload cannot be trusted."""


def _project_root(cwd: str) -> Path | None:
    """Resolve the GRAPH root: the nearest enclosing `.agi` dir with a config.

    Matches `locations.find_project_root` / `lib/find-root.sh`: the project
    root IS the `.agi` directory (the graph lives at `<root>/nodes/`). Silent
    None outside an agi project (P7).
    """
    d = Path(cwd).resolve()
    for anc in (d, *d.parents):
        cfg = anc / "config.json"
        if cfg.is_file() and anc.name == ".agi":
            return anc
        # also accept the marker directly on the enclosing dir's `.agi`
        inner = anc / ".agi" / "config.json"
        if inner.is_file():
            return inner.parent
    return None


def _canonical_pin(root: Path, seat: str) -> Path | None:
    """`<canonical sessions dir>/<seat>.meter`, or None if it cannot be known.

    🔴 DO NOT COMPUTE THIS AS `root / "sessions"`. Pins are SHARED state and
    `rotate._sessions_dir` routes them to the MAIN checkout via
    `locations.git_common_root`, while a seat's root is its own worktree. On
    this box that is the difference between
    `/home/ubuntu/work/agi/.agi/sessions/` (where every reader looks) and
    `…/.agi/worktrees/seat-<name>/.agi/sessions/` (where nothing does), so a
    naive join emits a command that writes a pin no later `--seat` read will
    ever find.

    We ASK `rotate` rather than reimplement it — a sixth private copy of a
    path rule is how this project keeps paying for the same defect — and if
    rotate cannot be imported we return None so the caller emits the
    seat-less command instead. **Never guess a pin path**: guessing which pin
    is yours is the original defect of this entire chain
    (hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write).
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import rotate  # noqa: PLC0415 — deliberately lazy; the hook must not
        #                  hard-depend on the engine being importable (P7).
        return Path(rotate._sessions_dir(root)) / f"{seat}.meter"
    except Exception:
        return None


def _load_ladder(root: Path) -> dict:
    """Read the ladder node's config fields; return {} if unreadable.

    Absent vs unreadable is left to the caller: a missing field triggers a
    fail-closed refusal, NOT a silent default (P6).
    """
    path = root / "nodes" / ".geometry" / "ladder.md"
    if not path.is_file():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    fm = {}
    # tiny YAML-ish frontmatter read — only the scalar fields we need.
    in_fm = text.startswith("---")
    body = text[4:] if in_fm and text.find("\n---", 4) != -1 \
        else text[4:] if in_fm else text
    if in_fm:
        fm_text = text.split("\n---", 1)[0].split("---", 1)[-1]
    else:
        fm_text = ""
    for line in fm_text.splitlines():
        m = re.match(r"^(\w+):\s*(\S.*?)\s*$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip("'\"")
    return fm


def _latest_usage(transcript_path: Path):
    """The LATEST assistant message's context size — the numerator.

    🔴 CONTEXT USAGE IS A LEVEL, NOT A RUNNING TOTAL, and this function
    originally summed. Every assistant turn's `usage` already includes the
    whole prior context, so adding the turns together is roughly quadratic.
    MEASURED on a real transcript (211 assistant messages, gen V's own
    session): summing gave 35,751,051 tokens — a fraction of **35.75** —
    against a true 253,460 tokens and a true fraction of 0.2535. **A 141x
    overcount**, which would have fired "ROTATION OWED NOW" on essentially
    every session from its first few turns.

    The round's own fixtures could not see it: with one or two assistant
    messages the sum and the latest are the same number. That is exactly why
    a thing gets run against the real tree before its tests are believed.

    And the consequence is not merely a wrong number — a warning that always
    fires is a warning that gets waved through, which is the failure this
    hook exists to prevent (hypothesis:l4-a-check-that-cries-wolf-gets-waved-
    through). It would have been worse than no hook at all.

    Counts input_tokens + cache_read_input_tokens + cache_creation_input_tokens
    on the newest assistant message, matching what `rotate.py meter` reports
    (`parse_usage_from_cc_transcript` — "Returns the latest one"). The choice
    of what the numerator counts changes the fraction, so it is stated in the
    emitted text rather than hidden (P6).
    """
    total = 0
    seen = 0
    with transcript_path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = rec.get("message") or {}
            role = (msg.get("role") or "").lower()
            if role != "assistant":
                continue
            usage = msg.get("usage") or {}
            if not isinstance(usage, dict):
                continue
            i = usage.get("input_tokens", 0)
            cr = usage.get("cache_read_input_tokens", 0)
            cc = usage.get("cache_creation_input_tokens", 0)
            try:
                n = int(i) + int(cr) + int(cc)
            except (TypeError, ValueError):
                continue
            total = n          # LEVEL, not a running sum — see the docstring.
            seen += 1
    return total, seen


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # ---- P2 / P7: read and trust only the handed payload --------------------
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    if not raw:
        # Not a hook invocation (no stdin): stay out of the way on an
        # interactive run. Hooks are always fed stdin; console is not a hook.
        return 0
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"rotation-alert: payload is not JSON: {exc}", file=sys.stderr)
        return 0
    if not isinstance(payload, dict):
        print("rotation-alert: payload is not an object — ignoring", file=sys.stderr)
        return 0

    transcript = payload.get("transcript_path")
    session_id = payload.get("session_id")
    cwd = payload.get("cwd") or os.getcwd()

    # Fail closed with a NAMED error if the field we depend on is missing
    # (P2). Never emit a fraction we cannot trace to a handed transcript.
    if not (isinstance(transcript, str) and transcript.strip()):
        print('rotation-alert: fail-closed: payload has no "transcript_path"; '
              "refusing to guess a transcript. Emitting no rotation warning.",
              file=sys.stderr)
        return 3
    tp = Path(transcript)

    # ---- P7: silent outside an agi project ----------------------------------
    root = _project_root(cwd)
    if root is None:
        return 0

    # ---- P7: silent on an unreadable transcript -----------------------------
    if not tp.is_file():
        return 0

    # ---- P6: denominator — read the ladder, FAIL CLOSED if unmeasurable -----
    ladder = _load_ladder(root)
    try:
        window = int(ladder.get("director_context_tokens") or 0)
        ladder_default = float(ladder.get("director_rotate_at") or 0.0)
    except (TypeError, ValueError):
        window = 0
        ladder_default = 0.0
    if window <= 0 or ladder_default <= 0:
        print("rotation-alert: fail-closed: ladder declares no "
              f"director_context_tokens/window (got {ladder.get('director_context_tokens')!r}) and no "
              f"director_rotate_at (got {ladder.get('director_rotate_at')!r}); "
              "refusing to assume a denominator. Emitting no rotation warning.",
              file=sys.stderr)
        return 4
    # The line a seat is measured against is the seat's OWN rotate_at from its
    # config:seats row when the seat is identifiable (AGI_SEAT, else the cwd
    # under a row's worktree), falling back to the ladder's
    # director_rotate_at — and the emitted message SAYS which source won
    # (hypothesis:l4-a-seat-rotates-at-its-own-line).
    seat, threshold, threshold_source = _seat_line(root, cwd, ladder_default)

    try:
        used, seen = _latest_usage(tp)
    except OSError as exc:
        print(f"rotation-alert: fail-closed: cannot read transcript: {exc}", file=sys.stderr)
        return 0

    fraction = used / window

    # ---- P4: per-session escalation state, keyed by SESSION ID --------------
    # Stored under /tmp keyed by uid — LOCAL to this machine and this agent,
    # never the shared sessions dir routed to the main checkout (the exact
    # boundary that produced hypothesis:l4-the-meter-pinned-...). A session_id
    # is unique per session, so two agents' states cannot collide even in a
    # shared dir; the tmp+uid split guarantees it regardless.
    state_dir = Path(os.environ.get("AGI_ROTATION_STATE_DIR")
                     or f"/tmp/agi-rotation-{os.getuid()}")
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    state_path = state_dir / f"{session_id or 'nosession'}.json"
    fired_bands = set()
    if state_path.is_file():
        try:
            fired_bands = set(json.loads(state_path.read_text()).get("fired", []))
        except (OSError, json.JSONDecodeError):
            fired_bands = set()

    band = 0
    b_frac = 0.0
    over_line = fraction >= threshold
    # Find the highest band the current fraction crosses (below the line).
    for i, bf in enumerate(BAND_FRACTIONS):
        if fraction >= bf * threshold:
            band = i
            b_frac = bf
        else:
            break

    def _emit(title: str, headline: str) -> int:
        print(title)
        print()
        print(headline)
        print()
        print("```bash")
        bin_dir = (Path(__file__).resolve().parents[1] / "bin")
        pin = _canonical_pin(root, seat) if seat else None
        if pin is not None:
            print(ROTATE_CMD.format(bin=bin_dir, pin=pin, transcript=transcript))
        else:
            print(ROTATE_CMD_NO_SEAT.format(bin=bin_dir, transcript=transcript))
        print("```")
        print()
        print("(Fraction computed from `input_tokens + cache_read_input_tokens + "
              "cache_creation_input_tokens` on the NEWEST assistant message of the "
              f"handed transcript — a level, not a running total: {used} tokens of "
              f"a {window}-token window = {fraction:.4f} of the window = "
              f"{fraction/threshold:.4f} of the line; threshold {threshold:.4f} "
              f"from {threshold_source}.)")
        print("---")
        return 0

    if over_line:
        # Every firing at/over the line (P3). Do not consume band state.
        return _emit(AT_OR_OVER_TITLE,
                     f"This session is at or over its rotation line: "
                     f"{fraction:.4f} ≥ {threshold:.4f}. Rotate NOW. If you were "
                     "mid-round, hand off cleanly first.")

    if band < 0 or b_frac <= 0.0:
        # Below the lowest band: nothing has changed — stay silent (P3).
        return 0

    if band not in fired_bands:
        fired_bands.add(band)
        try:
            state_path.write_text(json.dumps({"session_id": session_id,
                                              "fired": sorted(fired_bands)}))
        except OSError:
            pass
        pct = int(b_frac * 100)
        return _emit(BENEATH_TITLE,
                     f"Approaching rotation ({fraction:.4f} of the window = "
                     f"{fraction/threshold:.4f} of the line). "
                     f"Crossed band {pct}% of threshold.")

    # Already fired this band this session — silence (P3).
    return 0


if __name__ == "__main__":
    raise SystemExit(main())