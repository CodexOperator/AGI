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
import subprocess
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
    """The seat (post) name for a worktree, or None.

    A seat runs in `<repo>/.agi/worktrees/seat-<name>`; worktrees are being
    renamed `post-<name>`, so BOTH spellings resolve during the alias season
    (hypothesis:l4-a-seat-is-a-post-everywhere). None when the caller is not
    in a seat worktree — in which case we print the command WITHOUT `--pin`
    rather than guess a pin path, because guessing which pin belongs to you
    is the original defect this whole chain is about.
    """
    for part in Path(cwd).resolve().parts:
        for prefix in ("seat-", "post-"):
            if part.startswith(prefix):
                return part[len(prefix):] or None
    return None

def _config_label(root: Path) -> str:
    """'config:posts' or 'config:seats' — the ACTUAL geometry config file this
    root resolves, so the emitted source label names the file the row came
    from instead of a hardcoded 'config:seats' (hypothesis:l4-a-seat-is-a-
    post-everywhere: the live file is posts.md after the rename)."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import geometry_config  # noqa: PLC0415 — lazy, engine-optional (P7).
        _, key = geometry_config.resolve(root)
        return f"config:{key}"
    except Exception:
        return "config:seats"


def _seat_rows(root: Path) -> list:
    """Rows of the `config:posts` geometry node, post-first.

    `config:seats` is renamed `config:posts` (hypothesis:l4-a-seat-is-a-post-
    everywhere): the SHARED resolver (`geometry_config.py`) reads
    `nodes/.geometry/posts.md` + `posts:` and falls back to the deprecated
    `seats.md`/`seats:` for one season. We route through that ONE resolver so
    this hook has no second copy of the registry — a literal `seats.md` stat
    would read absent/empty the moment the live file is `posts.md`.
    """
    if root is None:
        return []
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import geometry_config  # noqa: PLC0415 — lazy, the hook must not
        #   hard-depend on the engine being importable (P7).
        return geometry_config.load_rows(root)
    except Exception:
        return []


def _main_root(root: Path):
    """Return `(integration-tree graph root, reason)` for the seat's own `root`.

    A seat's OWN worktree `root` carries a possibly-STALE `config:seats`: its
    row is merged from `origin/season/s2` only at the seat's next merge, while
    the Prime edits `rotate_at` on the main checkout — so a line the Prime
    lowers on main does not reach a working seat for an entire generation.
    The main checkout is one call away — `locations.git_common_root`, which is
    already importable (the hook inserts `<hooks>/../bin` on sys.path).

    The second element is WHY we believe the returned root is (or is not) main:
      `main`            — running IN the main checkout: `git_common_root(root)`
                          is root itself (identity). Caller labels `(main checkout)`.
      `resolved`        — a DIFFERENT repo root mapped to its graph root via
                          `find_project_root`; the caller reads it as
                          `(main checkout)`, and works its own `root` row only
                          as a fallback (labelled honestly `(worktree)`).
      `unresolved:no-graph-root` — `git_common_root(root)` gave a non-identity
                          dir, but `find_project_root(main)` found no graph
                          there. `root` is returned unchanged and the caller
                          must NOT label it main.
      `unresolved:<ExceptionName>` — git failed outright (git unavailable,
                          network, anything). `root` is returned unchanged and
                          the caller keeps a full worktree read (P7).

    P7: never a hard dependency. On ANY failure this returns `(root,
    unresolved:<ExcName>)` and the caller still completes a worktree read:
    the hook never raises and always still emits a threshold.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import locations  # noqa: PLC0415 — lazy, like _canonical_pin
        main = Path(locations.git_common_root(root))
        if main == root:
            return root, "main"
        main_graph = locations.find_project_root(main)
        if main_graph:
            return Path(main_graph).resolve(), "resolved"
        return root, "unresolved:no-graph-root"
    except Exception as exc:
        return root, f"unresolved:{type(exc).__name__}"


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
    `config:seats <seat>.rotate_at (main checkout)` vs `(worktree)` — and the
    `(main checkout)` label is earned ONLY by a genuinely resolved main (reason
    `main` or `resolved`). A worktree row read because main could NOT be
    resolved is labelled `(worktree; main unresolved: <why>)`, never main —
    the exact lie the round exists to remove. A rotate_at that is missing,
    unparseable or NON-POSITIVE falls through to the ladder default — the
    guard is intact (0 must never become a 0.0 threshold, or
    `fraction/threshold` in `_emit` divides by zero).
    """
    # AGI_POST wins over AGI_SEAT (the deprecated alias) for one season —
    # hypothesis:l4-a-seat-is-a-post-everywhere. The shared resolver owns the
    # post-first / seat-fallback order and the once-per-process notice.
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import geometry_config  # noqa: PLC0415 — lazy, engine-optional (P7).
        seat = geometry_config.resolved_seat_env()
    except Exception:
        seat = os.environ.get("AGI_POST") or os.environ.get("AGI_SEAT")
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
    main_root, main_reason = _main_root(root)
    if main_reason == "main":
        # In the main checkout: one tree, and it IS the main checkout.
        candidates = [(root, "main checkout")]
    elif main_reason == "resolved":
        # A DIFFERENT repo root resolved to a real graph root. Read the MAIN
        # row first; fall back to the seat's OWN worktree row only when the
        # main graph has no row — and that fallback is labelled honestly
        # `(worktree)` (main was resolved, it simply had no row for the seat).
        candidates = [(main_root, "main checkout"), (root, "worktree")]
    else:
        # main could NOT be resolved (git unavailable / no graph root there):
        # there is no main tree to read — only the worktree row, labelled WITH
        # WHY it is not main. Never label this worktree row `(main checkout)`.
        candidates = [(root, f"worktree; main unresolved: {main_reason}")]
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
                        f"{_config_label(cand_root)} {seat}.rotate_at "
                        f"({tree_label})")
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


# ═══════════════════════════════════════════════════════════════════════════
# goal:g15.25 line (4) — the meter hook ROTATES at threshold (rotate-out ZERO
# calls), NEVER while a merge-up is in flight, and NEVER twice for one
# generation. hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up.
# A rotation landing mid-merge is worse than one extra tool call, and it is the
# kind of thing that only fails under load (Prime XI 21:20Z, the GATE verbatim).
# So when an over-line seat's state is clean the hook BACKGROUNDS
# `rotate.py rotate-self --name <seat> --role director --timeout 900 --force
# --stops '<one line>'` itself (rotate-out ZERO calls) and prints the card the
# stops line lands on; when a gate HOLDS it prints its reason and does nothing,
# re-checking on the next prompt. Every gate answers CLEAN when unmeasurable and
# the hook never raises / never blocks / never delays the prompt (P7).
# ═══════════════════════════════════════════════════════════════════════════

#: The rotate-self invocation the hook backgrounds at threshold. rotate-out ZERO
#: calls: the hook IS the rotate-out, and `--stops` delivers the rotation line
#: as a signed dm itself (goal:g15.25 line (3)). `--timeout 900` bounds the
#: rotate-self; `--force` bypasses only the meter-due gate, never the captives.
ROTATE_SELF = (
    "python3 {bin}/rotate.py rotate-self --name {seat} --role director "
    "--timeout 900 --force --stops {stops!r}"
)

#: The exact deferral headline the claim makes load-bearing wherever it prints.
DEFER_PREFIX = "rotation deferred: merge-up in flight"


def _git_maybe(cwd, *args: str) -> list[str] | None:
    """git in `cwd`, stdout lines, or None on ANY failure (not a repo, a
    missing ref, git unavailable). P7: never raises; a measurement that cannot
    be taken reads as absent (clean), exactly as rotate.py's captives degrade."""
    try:
        out = subprocess.run(["git", "-C", str(cwd), *args],
                             capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return None
    if out.returncode != 0:
        return None
    return [ln for ln in out.stdout.splitlines()]


def _git_toplevel(cwd) -> Path | None:
    """The repo work-tree top for `cwd`, or None (not a repo / gitless)."""
    lines = _git_maybe(cwd, "rev-parse", "--show-toplevel")
    if not lines:
        return None
    try:
        return Path(lines[0].strip())
    except (ValueError, OSError):
        return None


def _git_count_maybe(cwd, *args: str) -> int | None:
    """The first stdout line as an int, or None when git cannot answer."""
    lines = _git_maybe(cwd, *args)
    if not lines or not lines[0].strip():
        return None
    try:
        return int(lines[0].strip())
    except ValueError:
        return None


def _pid_alive(pid: int) -> bool:
    """A pid with a live process — the dead-vs-live judgement the suite-lock
    gate needs (a dead holder's lock is stale-broken, i.e. NOT held)."""
    if not pid or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True   # alive, owned by someone else
    except OSError:
        return False
    return True


def _shared_sessions_dir(root: Path) -> Path | None:
    """The graph's ONE shared sessions dir (routed through the main checkout), or
    None when rotate cannot be imported (P7). Reuses rotate's resolver so the
    hook has no second copy of the path rule."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import rotate  # noqa: PLC0415, PLC0415
        return Path(rotate._sessions_dir(root))
    except Exception:  # noqa: BLE001
        return None


def _season_branch_checked(root: Path) -> str:
    """The season branch name, resolved through rotate's ONE resolver (never a
    hardcoded `season/s2`), or '' when rotate cannot be imported (P7)."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import rotate  # noqa: PLC0415
        return rotate.season_branch(root)
    except Exception:  # noqa: BLE001
        return ""


def _read_generation(root: Path, seat: str) -> int:
    """The seat's generation for the once-per-generation latch, 0 unmeasurable."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import rotate  # noqa: PLC0415
        return int(rotate._read_generation(root, seat))
    except Exception:  # noqa: BLE001
        return 0


def _merge_head_present(root: Path) -> bool:
    """MAIN's `.git/MERGE_HEAD` present — a merge-up is being performed on the
    main checkout RIGHT NOW. read on the MAIN root (`_main_root`), the exact
    tree the claim's gate (b) names."""
    main_root, _ = _main_root(root)
    return bool(_git_maybe(main_root, "rev-parse", "-q", "--verify",
                           "MERGE_HEAD"))


def _suite_lock_held(root: Path) -> bool:
    """A LIVE runner holds `<sessions>/verify-suite.lock` (verification.py). A
    lock whose holder pid is dead (or unparseable/absent) is stale-broken — NOT
    held — mirroring acquire_suite_lock's dead-pid break."""
    s = _shared_sessions_dir(root)
    if s is None:
        return False
    lock = s / "verify-suite.lock"
    if not lock.exists():
        return False
    try:
        holder = int(lock.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return False
    return _pid_alive(holder)


def _season_unpushed(root: Path) -> bool:
    """An unpushed merge commit on the season branch: `origin/<season>..<season>`
    is non-zero from the MAIN checkout. This is the `git status -sb` *ahead* the
    claim names. Unmeasurable reads clean (P7); a season branch with no local
    ref (not checked out) reads clean too — there is nothing to merge-up that is
    not pushed."""
    sb = _season_branch_checked(root)
    main_root, _ = _main_root(root)
    top = _git_toplevel(main_root)
    if top is None or not sb:
        return False
    n = _git_count_maybe(top, "rev-list", "--count", f"origin/{sb}..{sb}")
    return bool(n)


def _merge_in_flight(root: Path) -> str | None:
    """Which of the three merge-up signals holds, or None when clean. FIXED
    order (hypothesis line (4) gate (b)): MAIN's MERGE_HEAD, the suite lock,
    then a season unpushed merge commit. Returns the `(<which>)` label of the
    FIRST that holds. Never raises (P7): an unmeasurable signal reads clean."""
    if _merge_head_present(root):
        return "merge in progress on MAIN"
    if _suite_lock_held(root):
        return "verify-suite lock live"
    if _season_unpushed(root):
        return "unpushed merge commit on the season branch"
    return None


def _card_path(root: Path, seat: str) -> Path:
    """The seat card `.agi/sessions/quorum/<seat>.md` the hook must find fresh —
    own worktree copy first, the shared main copy only when no own copy exists
    (mirrors rotate._own_card_path, without its git routing)."""
    for p in (root / "sessions" / "quorum" / f"{seat}.md",
              root / ".agi" / "sessions" / "quorum" / f"{seat}.md"):
        if p.exists():
            return p
    s = _shared_sessions_dir(root)
    return (s / "quorum" / f"{seat}.md") if s is not None else \
        root / "sessions" / "quorum" / f"{seat}.md"


def _work_last_ts(top, card_rel: str | None, seats_rel: str | None) -> int | None:
    """The last WORK commit's mtime at the repo top, or None when unmeasurable.
    Mirrors rotate.py check 4's exclusion: comms dms, rotation records, the
    card itself and the seat own-row seats are bookkeeping, NEVER WORK — so a
    stops write can satisfy (not re-trigger) the card-age captive."""
    spec = ["log", "-1", "--no-merges", "--format=%ct", "--", ".",
            ":(exclude).agi/comms", ":(exclude).agi/sessions/rotations"]
    if card_rel:
        spec.append(f":(exclude){card_rel}")
    if seats_rel:
        spec.append(f":(exclude){seats_rel}")
    lines = _git_maybe(top, *spec)
    if not lines or not lines[0].strip():
        return None
    try:
        return int(lines[0].strip())
    except ValueError:
        return None


def _card_stale_measure(root: Path, seat: str, card: Path) -> tuple[bool, str]:
    """Card-age captive (gate (a)): `(stale, clear_line)`. The card must be
    NEWER than the last WORK commit; when it is older the hook does NOT rotate
    and prints the card line to write instead. Unmeasurable last-WORK (no git)
    reads NOT stale — the same ok-unmeasurable rule rotate's captives use."""
    top = _git_toplevel(root) or root
    try:
        card_rel = str(card.resolve().relative_to(Path(top).resolve()))
    except (ValueError, OSError):
        card_rel = None
    seats_rel = None
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import rotate  # noqa: PLC0415
        sres = str(rotate._ack_seats_path(root).resolve()
                   .relative_to(Path(top).resolve()))
        seats_rel = sres
    except Exception:  # noqa: BLE001
        seats_rel = None
    last_ts = _work_last_ts(top, card_rel, seats_rel)
    stale = False
    if last_ts is not None and card.exists():
        try:
            stale = card.stat().st_mtime < last_ts
        except OSError:
            stale = False   # an unstat-able card reads not-stale (P7)
    return stale, f"rotate.py handoff --driven --seat {seat}"


def _prepare_other_captives(root: Path, seat: str) -> list[tuple[str, str]]:
    """Gate (c) — prepare's captives OTHER than card-age: behind / dirty / pin /
    ack, LISTED with their clear commands. Runs `_prepare_checks(perform=False)`
    so it LISTS and never performs (P7: the hook must not merge or mutate — the
    spawned rotate-self --stops runs the same checklist itself, with --perform).
    The card-age captive is already gated separately as (a)."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
        import rotate  # noqa: PLC0415
        checks = rotate._prepare_checks(root, seat, perform=False)
    except Exception:  # noqa: BLE001
        return []
    out: list[tuple[str, str]] = []
    for blocker, name, clear in checks:
        if not blocker:
            continue
        if name.startswith("card older than last commit"):
            continue
        out.append((name, clear))
    return out


def _last_signed_dm(root: Path) -> str:
    """The first line (first 80 chars) of the newest signed dm for the project,
    or '' when none can be read. Signed acts live under `<repo>/comms/*/dm/`.
    Never raises (P7)."""
    comms = root.parent / "comms"
    best: Path | None = None
    best_mt = -1.0
    try:
        for dmd in comms.glob("*/dm"):
            for f in dmd.iterdir():
                if not f.is_file():
                    continue
                try:
                    mt = f.stat().st_mtime
                except OSError:
                    continue
                if mt > best_mt:
                    best_mt = mt
                    best = f
    except OSError:
        return ""
    if best is None:
        return ""
    try:
        first = best.read_text(encoding="utf-8", errors="replace")
        line = first.strip().splitlines()[0].strip() if first.strip() else ""
        return line[:80]
    except OSError:
        return ""


def _stops_line(root: Path, seat: str) -> str:
    """`stops: <commit subject> | last dm: <first 80 chars>` — the seat's two
    most recent signed acts (goal:g15.25 line (4) FALSIFIER: the stops text is
    NEVER empty when a signed commit exists). An unmeasurable half degrades to
    'n/a' so the line is always non-empty. Never raises (P7)."""
    card = _card_path(root, seat)
    top = _git_toplevel(root) or root
    try:
        card_rel = str(card.resolve().relative_to(Path(top).resolve()))
    except (ValueError, OSError):
        card_rel = None
    subject = "n/a"
    for cand in (root, _main_root(root)[0]):
        spec = ["log", "-1", "--no-merges", "--format=%s", "--", ".",
                ":(exclude).agi/comms", ":(exclude).agi/sessions/rotations"]
        if card_rel:
            spec.append(f":(exclude){card_rel}")
        lines = _git_maybe(cand, *spec)
        if lines and lines[0].strip():
            subject = lines[0].strip()
            break
    dm = _last_signed_dm(root)
    return f"stops: {subject} | last dm: {dm[:80]}"


#: once-per-generation latch dir, under the shared sessions dir. Keyed by
#: seat + generation so a slow spawn is never doubled (gate (d)).
_LATCH_SUBDIR = "rotations"


def _latch_path(root: Path, seat: str, gen: int) -> Path:
    """The once-per-generation latch, keyed to the seat's OWN tree's sessions
    dir — NOT the shared MAIN-sessions dir — so a worktree seat's transient
    hook latch NEVER lands under MAIN's checkout (a live git-status churn
    source and a cross-tree name collision). `root` here is the GRAPH root
    (the `.agi/` itself, per `_project_root`), so its OWN sessions dir sits
    directly under it: `<root>/sessions` — identity for a non-worktree seat,
    whose own tree IS the shared graph, so nothing changes on MAIN. Durable
    rotation records in `rotations/` stay tracked; only this transient
    `hook-*.lock` is ignored (see .gitignore)."""
    return root / "sessions" / _LATCH_SUBDIR / f"hook-{seat}-gen{gen}.lock"


def _latch_holder_pid(latch: Path) -> int | None:
    """The `pid <n>` recorded in a latch file, or None when it cannot be read.
    The latch names the ROTATE-SELF process (never the hook's own, which exits
    the instant it spawns), so a holder pid here is the process whose lifetime
    the latch belongs to."""
    try:
        for ln in latch.read_text(encoding="utf-8").splitlines():
            m = re.match(r"pid\s+(\d+)", ln)
            if m:
                return int(m.group(1))
    except (OSError, ValueError):
        return None
    return None


def _latch_held(latch: Path) -> bool:
    """A latch is HELD while a live process holds its lock. A dead holder — a
    rotate-self that FAILED mid-flight, or one that COMPLETED (which bumps the
    generation, so the next prompt reads a different latch key anyway) — leaves
    a stale latch, and a stale latch is NOT held. The dead-vs-live judgement is
    the same idiom as `_suite_lock_held` (and acquire_suite_lock's dead-pid
    break): a lock whose holder is not alive must not silently block the thing
    it guards for the rest of the generation."""
    pid = _latch_holder_pid(latch)
    if pid is None:
        return False
    return _pid_alive(pid)


def _rotate_self_argv(bin_dir: Path, seat: str, stops: str) -> list[str]:
    """The full argv of the background rotate-self the hook spawns at threshold
    (rotate-out ZERO calls — the hook IS the rotate-out). One builder, shared by
    the production spawn and the test seam so the two can never disagree."""
    return ["python3", str(bin_dir / "rotate.py"), "rotate-self",
            "--name", seat, "--role", "director", "--timeout", "900",
            "--force", "--stops", stops]


#: The ONE launch seam every background rotate-self Popen goes through. Tests
#: replace THIS module attribute with a recorder (never patch the whole
#: function) — an out-of-process run imports this module freshly, so a function
#: patch is invisible there and a REAL rotate.py rotate-self can still fire,
#: which is exactly how c1f01e920 happened: a live rotate-self --stops for the
#: sensei-director seat launched from a kid's pytest. A test that goes through
#: this seam proves the argv on the built bytes without ever reaching
#: subprocess.Popen.
_Popen = subprocess.Popen

def _spawn_rotate_self(root: Path, seat: str, stops: str) -> int | None:
    """Background `rotate.py rotate-self --stops <stops>` for `seat` (rotate-out
    ZERO calls — the hook ITSELF is the rotate-out). Detached, devnull, so the
    hook returns immediately and NEVER blocks the prompt (P7); `--timeout 900`
    bounds the rotate-self. Returns the pid, or None on any failure (never
    raises). Launch goes through the ONE seam `_Popen` (see above); sets an
    env-var short-circuit so an out-of-process test (fresh interpreter, seam
    not patchable) can never fire a REAL rotate-self from a pytest."""
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    argv = _rotate_self_argv(bin_dir, seat, stops)
    if os.environ.get("AGI_HOOK_NO_SPAWN"):
        # Out-of-process safety (c1f01e920) AND operator suppression — the
        # DEFENSE-IN-DEPTH net under the gate (e) guard in `_gated_rotate`
        # (which prints the decline and writes NO latch). If a caller reaches
        # this seam directly under NO_SPAWN, return None — NEVER a recorder
        # pid: a None is unlatched by the caller's spawn-failed path, so no
        # phantom pid can ever land in a latch. The argv stays provable via
        # the `_rotate_self_argv` builder (never reached, nothing lost).
        return None
    try:
        proc = _Popen(argv, stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL,
                      stdin=subprocess.DEVNULL,
                      start_new_session=True)
    except Exception:  # noqa: BLE001
        return None
    return proc.pid


def _gated_rotate(root: Path, seat: str) -> str | None:
    """goal:g15.25 line (4) — the hook's auto-rotation decision for an over-line
    seat. Runs the FOUR gates IN ORDER; each gate that HOLDS prints its reason
    and does NOTHING (re-check next prompt). Every gate clean → spawns the
    background rotate-self and prints what it spawned. Returns the deferral
    `<which>` reason when a gate held, else None (rotated). Prints its own
    status lines; never raises (P7)."""
    if not seat:
        return "no-seat-identified"
    card = _card_path(root, seat)

    # gate (a) card-age captive
    stale, clear_line = _card_stale_measure(root, seat, card)
    if stale:
        print("[rotation] card-age captive: the seat card is older than the "
              "last WORK commit — the hook does not rotate a seat whose card "
              "is stale. Write it, then re-check on the next prompt:")
        print(f"  {clear_line}")
        return "card-stale"

    # gate (b) NO MERGE-UP IN FLIGHT — THE POINT of the node, tested first.
    which = _merge_in_flight(root)
    if which:
        print(f"{DEFER_PREFIX} ({which}) — the hook does not rotate while a "
              f"merge-up is in flight; re-check on the next prompt.")
        return which

    # ----- stale-latch release: runs BEFORE gate (c), so a latch whose holder
    # pid is DEAD is released even on a prompt where a LATER captive holds the
    # rotation. Gate (c) used to return first, stranding the dead latch so it
    # blocked every later rotation until a human removed it by hand.
    gen = _read_generation(root, seat)
    latch = _latch_path(root, seat, gen)
    if latch.exists() and not _latch_held(latch):
        # STALE-broken: the rotate-self that held this generation died (a
        # mid-flight FAILURE — the exact hole — or completion, which bumped
        # the generation so the seat now lives on a NEWER latch key). A stale
        # latch must NOT lock this seat out of auto-retry for the rest of the
        # generation, so release it and let a fresh spawn claim it (mirror of
        # _suite_lock_held's dead-pid break). Done here, before gate (c), so
        # the release is never skipped by a captive that holds below.
        try:
            latch.unlink()
        except OSError:
            pass

    # gate (c) prepare's other captives — LISTED, never performed (P7).
    blockers = _prepare_other_captives(root, seat)
    if blockers:
        for name, clear in blockers:
            print(f"[rotation] prepare captive: {name} — {clear}")
        return f"prepare:{blockers[0][0]}"

    # gate (d) once-per-generation latch — HELD test only now (the stale
    # release for this generation already ran BEFORE gate (c)); a slow spawn
    # is never doubled.
    if _latch_held(latch):
        print(f"rotation deferred: already rotating {seat} gen {gen} "
              f"(latch {latch.name} held by a live rotate-self); re-check on "
              f"the next prompt.")
        return f"latch-gen-{gen}"

    # gate (e) OPERATOR SUPPRESSION — AGI_HOOK_NO_SPAWN in the hook's env
    # (an operator export leaking into the hook) must NEVER latch the seat
    # against a phantom. Pre-fix the short-circuit lived inside
    # `_spawn_rotate_self` and returned 12345 (a recorder pid), so the caller
    # printed 'spawned' and wrote the once-per-generation latch as
    # 'pid 12345' for a rotate-self that never started — latching the seat for
    # the WHOLE generation against a fake. Here, FIRST, before any latch is
    # claimed: print the decline, write NOTHING, and let a later prompt retry
    # when the suppression lifts. The argv stays provable through the
    # `_rotate_self_argv` builder.
    if os.environ.get("AGI_HOOK_NO_SPAWN"):
        print("rotation: declined: AGI_HOOK_NO_SPAWN — the hook will NOT "
              f"spawn a rotate-self for {seat} (spawn suppressed by the "
              "operator env). NO latch was written; the seat can retry on "
              "the next prompt, or rotate manually.")
        return "no-spawn"

    # claim the latch BEFORE spawning so a concurrent prompt cannot double it.
    try:
        latch.parent.mkdir(parents=True, exist_ok=True)
        latch.write_text(f"pid {os.getpid()} hook\n"
                         f"seat {seat}\ngen {gen}\n", encoding="utf-8")
    except OSError:
        pass   # a latch we cannot write must not block the rotation (P7)

    stops = _stops_line(root, seat)
    pid = _spawn_rotate_self(root, seat, stops)
    if pid is None:
        try:
            latch.unlink()   # a failed spawn must let a later prompt retry
        except OSError:
            pass
        print(f"rotation: FAILED to spawn rotate-self for {seat} (no pid); "
              f"rotate manually with the command below.")
        return "spawn-failed"

    # Record the ROTATE-SELF pid (not the hook's own, which exits the instant
    # it returns here): the latch is then held only WHILE its rotate-self
    # lives, so a mid-flight failure releases it on the next prompt (the latch-'
    # on-failure hole, closed) rather than latching this generation forever.
    try:
        latch.write_text(f"pid {pid} rotate-self\n"
                         f"seat {seat}\ngen {gen}\n", encoding="utf-8")
    except OSError:
        pass   # a latch we cannot rewrite must not fail the rotation (P7)
    print(f"rotation: spawned rotate-self for {seat} in the background "
          f"(rotate-out ZERO calls, pid {pid}); the stops line lands on "
          f"the card: {card}")
    return None


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
        # goal:g15.25 line (4) — the hook ROTATES at threshold (gated); when a
        # gate holds it prints the deferral so the operator sees WHY an
        # over-line seat has not rotated, and re-checks next prompt.
        deferral = _gated_rotate(root, seat)
        if deferral:
            suffix = (f"\n\n{DEFER_PREFIX} ({deferral}) — the hook is not "
                      "rotating this seat while that holds; it re-checks on "
                      "the next prompt.")
        else:
            suffix = ("\n\nRotation spawned in the background for this seat "
                      "(rotate-out ZERO calls); the stops line is landing on "
                      "its card. The command below inspects/rotates by hand "
                      "if needed.")
        return _emit(AT_OR_OVER_TITLE,
                     f"This session is at or over its rotation line: "
                     f"{fraction:.4f} ≥ {threshold:.4f}. Rotate NOW. If you were "
                     f"mid-round, hand off cleanly first."
                     + suffix)

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