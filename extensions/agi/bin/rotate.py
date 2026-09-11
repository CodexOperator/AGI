#!/usr/bin/env python3
"""rotate.py — director rotation: meter context usage, spawn a successor.

Subcommands:
  meter [--session-log PATH] [--check]
    - Print the context-usage fraction for the newest Claude Code transcript
      (or an explicit log file) against the ladder node's context window.
    - --check exits 1 when fraction >= director_rotate_at threshold; else 0.

  spawn [--name NAME] [--tier TIER] [--model M] [--effort E]
        [--settings JSON] [--prompt-file PATH] [--tmux-session agi-rc]
        [--window-path PATH] [--dry-run]
    - Build a `claude --remote-control NAME ...` command and run it in a new
      tmux window. Refuses if a window of that name already exists.
      When --window-path is given, read tmux window names from that file
      instead of calling tmux (used in tests).
    - Model, effort and settings default from the ladder roles table row for
      --tier (default prime_director); fall back to `harnesses.claude-code`
      in config.json, then to the ladder's fixed top-tier defaults. The
      prompt is assembled through brief.py so the constitution head precedes
      the prompt text.
    - The successor name defaults to `<prefix>-<ROM>` (Roman numeral) derived
      from existing windows: the current prime's `bel-S1-L3` yields
      `bel-S1-L3-II`, then `-III`. --name overrides.
    - --dry-run prints the command and touches nothing.

  loop --role TIER [--name-prefix P] [--name NAME] [--force] [--dry-run]
       [--session-log PATH] [--debug-file PATH] [--timeout SECONDS]
       [--model M] [--effort E] [--settings JSON] [--prompt-file PATH]
    - The super-ralph rotation primitive: meter, and when the fraction is
      over director_rotate_at (or --force), spawn the successor and then read
      its first reply from its log. The single word `continue` alone means the
      handoff stood with no change; anything else is the diff the successor
      would make.

  status
    - List tmux windows in sessions whose name starts with agi-master or
      belam, with their age.

Both meter and spawn (and loop) refuse to run while the repo is checked out
on `master` once a `season/*` branch exists: under seasons-as-branches the
prime works on `season/sN`, and `master` is the last closed season, frozen
to merges only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
from graph_core.persistence import frontmatter  # noqa: E402


# --- config ----------------------------------------------------------------

#: Default context window in tokens when the ladder node does not declare one.
DEFAULT_DIRECTOR_CONTEXT_TOKENS = 1_000_000

#: Default rotate-at fraction when the ladder node does not declare one.
DEFAULT_DIRECTOR_ROTATE_AT = 0.47

#: Engine root for resolving <engine> placeholders.
ENGINE_ROOT = Path(__file__).resolve().parent.parent.parent.parent

#: Where Claude Code stores project transcripts.
CC_PROJECTS_DIR = Path.home() / ".claude" / "projects"

#: Default project slug used by Claude Code for this repo.
CC_PROJECT_SLUG = "-home-ubuntu-work-agi"

#: Default tmux session for remote-control.
DEFAULT_TMUX_SESSION = "agi-rc"

#: Remote-control debug log path (legacy fallback), relative to the graph
#: dir (which `find_project_root()` returns) -- so `<graph>/sessions/`.
REMOTE_CONTROL_LOG = Path("sessions") / "remote-control.log"

#: Default prompt file, alongside this script.
DEFAULT_PROMPT_FILE = (
    ENGINE_ROOT / "extensions" / "agi" / "briefs" / "prime-director-successor.md"
)

#: Fallback role row when neither the ladder roles table nor config.json has it.
#: Fable 5.1 at max with the ultracode settings flag is the ladder contract for
#: prime/director.
DEFAULT_CC_ROLES = {
    "prime_director": {
        "harness": "claude-code",
        "model": "claude-fable-5-1",
        "effort": "max",
        "settings": {"ultracode": True},
        "tier": 3,
    },
    "director": {
        "harness": "claude-code",
        "model": "claude-fable-5-1",
        "effort": "max",
        "settings": {"ultracode": True},
        "tier": 2,
    },
    "parent": {
        "harness": "claude-code",
        "model": "claude-opus-5",
        "effort": "max",
        "settings": {"ultracode": True},
        "tier": 3,
    },
}

#: The roles table spells a settings bundle by its NAME for the CC tiers
#: (e.g. `settings: ultracode`). "Ultracode" is not an effort level -- it is a
#: settings flag -- so a bare word is resolved here to the flag object the
#: claude adapter passes as `--settings '{"ultracode":true}'`.
SETTINGS_ALIASES = {
    "ultracode": {"ultracode": True},
}

#: The launch gate and the opt-in trigger for Claude Code's dynamic
#: ("ultracode") workflows (hypothesis:l3-rotate-ultracode-env). The env var
#: is what actually enables it on this box (measured live by the prime: a
#: settings flag alone and the keyword alone both came back `no`; env var +
#: keyword came back `yes`), and the bare keyword `ultracode` as the first
#: line of the user turn opts the turn in. `--settings` is retained because
#: whether it is still needed WITH the env var is unproven (a fourth
#: throwaway -- env + keyword, no settings -- is still open).
ULTRACODE_KEYWORD = "ultracode"
ULTRACODE_ENV_EXPORT = "export CLAUDE_CODE_WORKFLOWS=1"
# hypothesis:l4-spawn-paths-export-the-reaper-knob — every launch must carry
# the knob that disarms the background-shell reaper in its OWN environment,
# not inherit it from the tmux session. An inherited value is one tmux
# restart from gone (or a window created outside agi-rc), so the seat-launch
# path prefixes it onto the launched shell line unconditionally.
REAPER_ENV_EXPORT = "export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1"


def _normalize_settings(val):
    """Coerce a roles-table settings cell to a dict, or None.

    Accepts a dict (use as-is), a bare known word (resolve via
    SETTINGS_ALIASES), or empty/absent (None => no --settings flag).
    """
    if val is None or val == "":
        return None
    if isinstance(val, dict):
        return val if val else None
    if isinstance(val, str):
        return SETTINGS_ALIASES.get(val.strip().lower())
    return None


# --- helpers ---------------------------------------------------------------


def find_project_root() -> Path | None:
    """Resolve the graph root, same as every other engine entry point."""
    root = locations.find_project_root()
    return root


def load_ladder_field(root: Path, field: str, default):
    """Read a field from the ladder node, or return `default`.

    Prints a warning when the field is absent and the default is used,
    so the operator knows to edit the ladder node.
    """
    path = Path(root) / "nodes" / ".geometry" / "ladder.md"
    if not path.exists():
        print(f"warn: ladder node not found at {path} — using default "
              f"{field}={default}. Add it to the node.", file=sys.stderr)
        return default
    try:
        nf = frontmatter.load_node_file(path)
        val = nf.frontmatter.get(field)
        if val is None:
            print(f"warn: ladder node has no {field} field — using default "
                  f"{default}. Edit the node to set it.", file=sys.stderr)
            return default
        return val
    except Exception as exc:
        print(f"warn: could not read ladder node {field}: {exc} — "
              f"using default {default}", file=sys.stderr)
        return default


def find_newest_cc_transcript(slug: str = CC_PROJECT_SLUG) -> Path | None:
    """The newest `.jsonl` file under `~/.claude/projects/<slug>/`.

    Returns None if no transcript exists yet.
    """
    proj_dir = CC_PROJECTS_DIR / slug
    if not proj_dir.is_dir():
        return None
    candidates = sorted(proj_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    return candidates[-1] if candidates else None


# The env var a spawner uses to tell the meter which transcript this role owns.
# Set by the claude-code adapter once it captures the child's session_id
# (hypothesis:l3-meter-own-transcript).
AGI_SESSION_LOG_VAR = "AGI_SESSION_LOG"


#: The meter pin extension, matching the brief's `<window-name>.meter`.
METER_PIN_EXT = ".meter"


def _derive_cc_slug(cwd: str) -> str:
    """The Claude Code project slug for a cwd: the absolute path with every
    `/` replaced by `-`. `claude -p` keys its transcript dir by the child's
    cwd this way, so an advisor run from its own working dir lands under a
    DIFFERENT slug than the prime -- which is why a hardcoded slug made every
    role's meter read the prime's transcript (measured on 2026-09-07: the
    advisor's `-home-ubuntu-work-agi--agi` vs the prime's
    `-home-ubuntu-work-agi`)."""
    return cwd.replace("/", "-")


def _sessions_dir(root: Path) -> Path:
    """The graph's sessions dir, never the doubled `<root>/.agi/.agi` path
    (hypothesis:l3-rotate-pin-path-readback).

    `find_project_root()` returns the GRAPH dir (the `.agi/` itself), so the
    sessions dir usually sits directly under it: `<graph>/sessions/`. A caller
    that passes the REPO root instead (`<repo>` root = `<graph>`'s parent)
    gets `<repo>/.agi/sessions` -- the SAME physical dir. Detection is by
    content (`nodes/` marks a graph dir), so a leftover doubled
    `<graph>/.agi` from before the fix (which holds old pins but no `nodes/`)
    is NOT mistaken for the graph.

    **hypothesis:l3w4-parent-branch-merge-up** — a `--branch` kid runs in its
    own git worktree with its own `.git`/`.agi`; the meter pins must stay the
    ONE shared directory on the main checkout (same rule as the budget dir
    and comms), so a rotation seat in a worktree reads the same room the
    parent wrote. Route through the main checkout (`git_common_root`) and
    re-resolve the graph from there; identity for a non-worktree caller.

    This is the hoisted body of `locations.shared_sessions_dir` (the shared-    
    room resolver); both are one implementation so the plain join and the
    shared resolver can never disagree (falsifier g4 of hypothesis:l4-a-check-
    that-answers-a-question-it-is-not-asking)."""
    return locations.shared_sessions_dir(root)


def find_pin_log(root: Path, seat: str | None = None) -> Path | None:
    """The newest `<root>/sessions/*.meter` pin, or the seat's own pin.

    `root` is the GRAPH dir (as `find_project_root()` returns), so the pins
    live at `<graph>/sessions/` -- the same dir the debug logs land in, never
    the doubled `<graph>/.agi/sessions/` (hypothesis:l3-rotate-pin-path-
    readback). When `seat` is given, the seat-stable pin `<root>/sessions/"
    "<seat>.meter` wins over every other pin regardless of mtime
    (hypothesis:l3w4-seat-registry) -- the meter for a named seat reads its
    own pin even as newer foreign pins land.

    A pin's content is a single line: the absolute path to the transcript this
    agent owns. Written by `rotate.py meter --pin` or by the claude adapter
    once it captures the child's session_id `(hypothesis:l3-meter-own-
    transcript)`. Returning the NEWEST lets several agents each pin their own
    transcript while the meter that is actually running reads its own.
    """
    sessions = _sessions_dir(root)
    if not sessions.is_dir():
        return None
    if seat is not None:
        sp = sessions / f"{seat}{METER_PIN_EXT}"
        return sp if sp.is_file() else None
    pins = sorted(sessions.glob(f"*{METER_PIN_EXT}"),
                  key=lambda p: p.stat().st_mtime)
    return pins[-1] if pins else None


def _parse_pin_record(pin: Path) -> tuple[int | None, str | None]:
    """A pin's content, split into `(generation, transcript_path)`.

    Two formats coexist so old pins keep working: a bare path (legacy,
    written before hypothesis:l3-seat-pin-not-repointed-on-rotation --
    `generation` is `None`, meaning "no writer recorded, don't check"), or
    `<generation>\\t<path>` written by a seat-aware `--pin` (the generation
    the OCCUPANT held when it wrote its own transcript in). Either way the
    path is the second/only field; a malformed generation degrades to
    "unknown" rather than failing the whole read."""
    try:
        raw = pin.read_text(encoding="utf-8").strip()
    except OSError:
        return None, None
    if not raw:
        return None, None
    if "\t" in raw:
        gen_s, _, path_s = raw.partition("\t")
        try:
            gen = int(gen_s.strip())
        except ValueError:
            gen = None
        return gen, path_s.strip()
    return None, raw


def _read_pin_target(pin: Path) -> Path | None:
    """The transcript a pin names, or None when the pin is empty/absent."""
    _, target = _parse_pin_record(pin)
    if not target:
        return None
    lp = Path(target).expanduser().resolve()
    return lp if lp.exists() else None


def resolve_transcript(*, root: Path, session_log: str | None = None,
                       env=None, seat: str | None = None) -> tuple[Path | None, str]:
    """The transcript the meter should read, resolved in strict order
    (hypothesis:l3-meter-own-transcript):

      1. `--session-log PATH` (explicit, must exist)
      2. env `AGI_SESSION_LOG` (must exist)
      3. a pin file `<root>/.agi/sessions/*.meter` naming our transcript
         (`--seat NAME` reads the seat-stable `<NAME>.meter` instead of the
         newest-mtime pin, hypothesis:l3w4-seat-registry)
      4. the transcript dir for OUR cwd slug (the child ran from this cwd)
      5. newest transcript in the fallback slug dir `.

    Returns `(log_path, source)` where `source` is a short tag naming which
    rule won. `(None, source)` means the top rules were tried and the file was
    absent (source ends `-missing`), or nothing at all was found (`no_log`).
    The caller uses the source to decide whether to warn."""
    env = os.environ if env is None else env
    # 1 -- explicit beats everything; absent is an error, not a fallthrough.
    if session_log is not None:
        lp = Path(session_log).expanduser().resolve()
        return (lp, "explicit") if lp.exists() else (None, "explicit-missing")
    # 2 env
    ev = env.get(AGI_SESSION_LOG_VAR)
    if ev:
        lp = Path(ev).expanduser().resolve()
        if lp.exists():
            return lp, "AGI_SESSION_LOG"
        return None, "AGI_SESSION_LOG-missing"
    # 3 pin file
    pin = find_pin_log(root, seat)
    if pin is not None:
        written_gen, target_s = _parse_pin_record(pin)
        if not target_s:
            return None, "pin_file-missing"
        lp = Path(target_s).expanduser().resolve()
        if not lp.exists():
            return None, "pin_file-missing"
        # Identity is supplied, never inferred (hypothesis:l4-the-meter-
        # adopts-a-pin-it-did-not-write). A generation-bearing pin is bound
        # to the named agent that stamped it. A SEATLESS read (seat=None)
        # falls into the newest-mtime search across every agent's pins, so a
        # gen-bearing winner here is ANOTHER agent's pin: reporting a
        # confident number for the transcript it names would attribute a
        # session the caller never named to this caller. Refuse loudly, and
        # let cmd_meter tell the operator what supplies an identity. A
        # legacy pin with no generation field (written_gen is None) predates
        # gen-stamping and keeps the room-level semantics below.
        if seat is None and written_gen is not None:
            return None, "pin_unattributed"
        # A seat pin that names a generation (hypothesis:l3-seat-pin-not-
        # repointed-on-rotation) must match the CURRENT occupant's own
        # generation, or this is a predecessor's stale pin read by a
        # successor rotation never re-pointed -- refuse loudly rather than
        # print a confident number that belongs to a session that already
        # ended. A legacy pin with no generation field (written_gen is
        # None) has nothing to compare and passes through unchanged.
        if seat is not None and written_gen is not None:
            cur_gen = _read_generation(root, seat)
            if written_gen != cur_gen:
                return None, f"seat_pin-stale:{written_gen}:{cur_gen}"
        return lp, "seat_pin" if seat else "pin_file"
    # 4 slug from this cwd
    slug = _derive_cc_slug(os.getcwd())
    for cand_slug in (slug, CC_PROJECT_SLUG):
        cand = find_newest_cc_transcript(cand_slug)
        if cand is not None:
            return cand, "cc_transcript_slug"
    return None, "no-transcript"


def parse_usage_from_cc_transcript(path: Path) -> dict | None:
    """Extract usage from the newest assistant message in a CC transcript.

    Each JSONL line is a CC event; a message with role='assistant' carries
    a `usage` object. Returns the latest one, or None if none found.
    """
    latest_usage = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = ev.get("message") or ev
            if not isinstance(msg, dict):
                continue
            if msg.get("role") == "assistant" and "usage" in msg:
                usage = msg["usage"]
                if isinstance(usage, dict) and usage.get("input_tokens") is not None:
                    latest_usage = usage
    return latest_usage


def parse_usage_from_rc_log(path: Path) -> dict | None:
    """Extract usage from a remote-control debug log.

    The log contains lines like:
      USAGE: {"input_tokens": N, "output_tokens": N, ...}
    """
    latest_usage = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            m = re.match(r"^USAGE:\s*(.*)", line)
            if not m:
                continue
            raw = m.group(1).strip()
            if raw == "[REDACTED]" or "redacted" in raw.lower():
                continue
            try:
                usage = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(usage, dict) and usage.get("input_tokens") is not None:
                latest_usage = usage
    return latest_usage


def calculate_fraction(usage: dict, context_tokens: int) -> float:
    """Compute (input_tokens + cache_read + cache_creation) / context_tokens."""
    tokens = (
        usage.get("input_tokens", 0)
        + usage.get("cache_read_input_tokens", 0)
        + usage.get("cache_creation_input_tokens", 0)
    )
    if context_tokens <= 0:
        return 0.0
    return tokens / context_tokens


def usage_source_name(source: str) -> str:
    """Human-readable name for the usage data source."""
    return {
        "cc_transcript": "claude-code transcript",
        "cc_transcript_slug": "claude-code transcript (newest heuristic)",
        "rc_log": "remote-control debug log",
        "explicit": "claude-code transcript (explicit)",
        "AGI_SESSION_LOG": "claude-code transcript (AGI_SESSION_LOG)",
        "pin_file": "claude-code transcript (pinned)",
        "unknown": "unknown source",
    }.get(source, source)


# ---- branch guard (seasons as branches) -----------------------------------


def _check_branch_guard(root: Path | None) -> str | None:
    """Refuse rotation tooling on `master` once a `season/*` branch exists.

    Under the adopted seasons-as-branches mapping the prime works on
    `season/sN`; `master` is the last closed season and only receives merges.
    Returns an explanatory error string when the repo is checked out on master
    with a season/* branch present, else None. Never raises: a repo that
    cannot answer git (tests, gitless checkout) simply passes the guard.
    """
    if root is None:
        return None
    try:
        cur = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        return None
    branch = cur.stdout.strip()
    if branch != "master":
        return None
    try:
        refs = subprocess.run(
            ["git", "for-each-ref", "--format=%(refname:short)",
             "refs/heads/season"],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        return None
    seasons = [ln.strip() for ln in refs.stdout.strip().splitlines() if ln.strip()]
    if seasons:
        return (
            "rotate refuses to run on master: season branches exist "
            f"({', '.join(seasons)}); the prime works on season/sN. "
            f"Check out `{seasons[0]}` and re-run."
        )
    return None


# ---- role resolution (ladder roles table, else config.json, else defaults)


def _config_json(root: Path) -> dict:
    """Read `<graph root>/config.json`, tolerant of absence/parse errors."""
    path = Path(root) / "config.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _ladder_roles_table(root: Path | None) -> list[dict]:
    """The ladder node's `roles:` rows (each a dict), or []."""
    if root is None:
        return []
    path = Path(root) / "nodes" / ".geometry" / "ladder.md"
    if not path.exists():
        return []
    try:
        nf = frontmatter.load_node_file(path)
        roles = nf.frontmatter.get("roles") or []
        if isinstance(roles, list):
            return [r for r in roles if isinstance(r, dict)]
    except Exception:
        pass
    return []


def load_role(root: Path | None, tier: str, field: str):
    """`model`/`effort`/`settings`/`harness` for a role.

    Resolution order: the ladder's `roles:` row for `role == tier`, then
    `harnesses.claude-code` in config.json (the fallback), then the fixed
    top-tier `DEFAULT_CC_ROLES`. `settings` cells are normalized through
    `_normalize_settings`. Returns None only when nothing at all is known for
    that field.
    """
    val = None
    if root is not None:
        for row in _ladder_roles_table(root):
            if row.get("role") == tier and row.get(field) is not None:
                val = row[field]
                break
        if val is None:
            h = (_config_json(root).get("harnesses") or {}).get("claude-code") or {}
            if field == "model":
                models = h.get("models") or {}
                val = models.get(tier) or models.get("director")
            elif field == "effort":
                val = (h.get("effort") or {}).get(tier)
            elif field == "harness":
                if h:
                    val = "claude-code"
            elif field == "settings":
                s = h.get("settings")
                if isinstance(s, dict) and s:
                    val = s
    if val is None:
        val = (DEFAULT_CC_ROLES.get(tier) or {}).get(field)
    if field == "settings":
        return _normalize_settings(val)
    return val


def _is_ultracode(settings) -> bool:
    """True when the resolved settings flag names ultracode.

    The ladder's `settings: ultracode` cell (resolved to `{"ultracode": true}`)
    is what turns a successor's environment on: rotate must prefix the tmux
    launch with `export CLAUDE_CODE_WORKFLOWS=1` and open the user turn with
    the keyword `ultracode` (hypothesis:l3-rotate-ultracode-env).
    """
    return bool(settings) and bool(settings.get("ultracode"))


# ---- successor name derivation --------------------------------------------


def _existing_windows(tmux_session: str, window_path: str | None = None) -> list[str]:
    """Existing tmux window names in `tmux_session`.

    When `window_path` is given, read names from that file (one per line)
    instead of calling tmux — used by tests.
    """
    if window_path:
        p = Path(window_path)
        if p.exists():
            out = []
            for ln in p.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                # L4.114 (s2): a window-path line may carry the window's tmux
                # @id as an `@<N> ` prefix (the test seam for the pane's own
                # @id capture); the window NAME is everything after it. A bare
                # `<name>` line is unchanged, so existing fixtures stay valid.
                if ln.startswith("@"):
                    _, _, rest = ln.partition(" ")
                    if rest.strip():
                        ln = rest.strip()
                out.append(ln)
            return out
        return []
    try:
        result = subprocess.run(
            ["tmux", "list-windows", "-t", tmux_session, "-F", "#{window_name}"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return [ln.strip() for ln in result.stdout.strip().splitlines()
                    if ln.strip()]
    except Exception:
        pass
    return []


_ROMAN_DIGITS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
_ROMAN_PAIRS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]


def _roman_value(s: str) -> int:
    total = 0
    prev = 0
    for ch in reversed(s):
        v = _ROMAN_DIGITS.get(ch, 0)
        if v == 0:
            return 0
        total += -v if v < prev else v
        prev = v
    return total


def _is_roman(s: str) -> bool:
    """True only for a canonical (well-formed) Roman numeral > 0."""
    if not s:
        return False
    v = _roman_value(s)
    return v > 0 and _int_to_roman(v) == s


def _int_to_roman(n: int) -> str:
    """Integer -> canonical Roman numeral (n >= 1)."""
    out = []
    for val, sym in _ROMAN_PAIRS:
        while n >= val:
            out.append(sym)
            n -= val
    return "".join(out)


def _split_roman_suffix(w: str) -> tuple[str, int]:
    """Split a window name into (base, line_value).

    A window ending in `-<ROM>` (a canonical Roman numeral) yields the name
    with that suffix stripped and the Roman value (a `-II` window is line 2,
    so its successor is `-III`). A bare base with no suffix (e.g.
    `belam-S1-L3`, the current prime) is the FIRST of the line and returns
    value 1 -- its successor is therefore `-II`.
    """
    dash = w.rfind("-")
    if dash > 0:
        tok = w[dash + 1:]
        if _is_roman(tok):
            return w[:dash], _roman_value(tok)
    return w, 1


def _derive_successor_name(windows: list[str], prefix: str = "belam") -> str:
    """The next successor name in the Roman-numeral scheme.

    Windows carry Roman suffixes in the owner's rotation: the prime is
    `belam-S1-L3` (line value 1), its successors `-II`, `-III`, ... The base
    of the sequence is the current window's name stripped of any trailing
    `-<ROM>`. A window that does not start with `prefix` is ignored, and
    nothing known about `prefix` makes `prefix` itself the base at line 1
    (so the first derived successor is `<prefix>-II`).
    """
    best_val = 0
    best_base = None
    for w in windows:
        if not (w == prefix or w.startswith(prefix + "-")):
            continue
        base, val = _split_roman_suffix(w)
        if best_base is None or val > best_val:
            best_val = val
            best_base = base
    if best_base is None:
        best_base = prefix
        best_val = 1
    return f"{best_base}-{_int_to_roman(best_val + 1)}"


# ---- successor command ----------------------------------------------------


def _build_claude_command(name: str, prompt_text: str, debug_file: str,
                          model=None, effort=None, settings=None) -> list[str]:
    """The remote-control argv: `claude --remote-control NAME ... <prompt>`."""
    cmd = [
        "claude",
        "--remote-control", name,
        "--permission-mode", "bypassPermissions",
        "--debug-file", debug_file,
    ]
    if model:
        cmd += ["--model", str(model)]
    if effort:
        cmd += ["--effort", str(effort)]
    if settings:
        cmd += ["--settings", json.dumps(settings)]
    cmd.append(prompt_text)
    return cmd


def _successor_command(*, name: str, tier: str, prompt_file: str, model,
                       effort, settings, debug_file: str, extra: str = "") -> list[str]:
    """The full successor argv: body read from `prompt_file`, `{name}`
    substituted, the constitution head prepended through brief.py, then
    model/effort/settings appended as flags."""
    body = Path(prompt_file).read_text(encoding="utf-8").replace("{name}", name)
    if _is_ultracode(settings):
        # keyword as the first line of the user turn, right after the head
        # (the prime's live probe: it must be in the user turn, after the
        # constitution head is fine).
        body = ULTRACODE_KEYWORD + "\n" + body
    if extra:
        body += "\n\n" + extra
    import brief  # local: same dir, may be absent in a misleading env
    prompt_text = brief.successor_prompt(tier=tier, body=body)
    return _build_claude_command(name, prompt_text, debug_file,
                                 model=model, effort=effort, settings=settings)


def _assembled_successor_command(*, name: str, tier: str, model, effort,
                                 settings, debug_file: str,
                                 extra: str = "",
                                 dispatch_py: str =
                                 "extensions/agi/bin/dispatch.py",
                                 cli_py: str =
                                 "extensions/agi/bin/cli.py") -> list[str]:
    """Build the successor argv for a non-prime seat from its assembled brief.

    The body is the joined segments of `brief.assemble(tier=..., agent_id=name,
    iter_n=0)` — a perpetual seat has no iteration number. assemble() already
    prepends the constitution head (for the liaison, the director's read_order
    via `_LIAISON_HEAD_TIER`), so unlike the prime's static-file path we do NOT
    call brief.successor_prompt() again: doing both would double-insert the
    head (hypothesis:l3w4-liaison-seat).
    """
    import brief  # local: same dir, may be absent in a misleading env
    parts = brief.assemble(tier=tier, agent_id=name, iter_n=0,
                           dispatch_py=dispatch_py, cli_py=cli_py)
    body = "\n\n".join(parts)
    if _is_ultracode(settings):
        # keyword as the first line of the user turn (see _successor_command)
        body = ULTRACODE_KEYWORD + "\n" + body
    if extra:
        body += "\n\n" + extra
    return _build_claude_command(name, body, debug_file,
                                 model=model, effort=effort, settings=settings)


# ---- meter subcommand -----------------------------------------------------


def _openrouter_key(root: Path) -> str | None:
    """`OPENROUTER_API_KEY`, env first, then `.env` at the repo root.

    `root` here is the GRAPH root (`.agi/`, per `find_project_root`), not
    the repo root -- `.env` lives one level up, so this must resolve
    through `locations.repo_root` rather than join onto `root` directly.
    """
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    env_path = locations.repo_root(root) / ".env"
    if not env_path.exists():
        return None
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            return line.split("=", 1)[1].strip()
    return None


def _openrouter_get(url: str, key: str) -> dict | None:
    """One best-effort GET against an OpenRouter endpoint. Never raises --
    a spend check must not fail a pin claim over a network hiccup."""
    try:
        req = urllib.request.Request(
            url, headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8")).get("data")
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None


def fresh_spend_status(root: Path) -> str | None:
    """Live OpenRouter balance, both scopes, at the moment a pin is claimed.

    Owner, 2026-09-08: "someone got something wrong regarding spend cap,
    it needs to be shown on pin accept fresh." What went wrong, named so it
    is not repeated: a report carried the per-spawn provisioning KEY's own
    sub-cap ("~$9.4 remaining") as though it were the ceiling, when the
    ACCOUNT behind it held several dollars more and the key's own limit is
    raisable (`PATCH /api/v1/keys/<hash>`, already used twice this loop).
    Showing only one of the two numbers is that exact error reproduced in
    the tool, so this always prints BOTH, the key labelled as a sub-cap on
    ONE key, never as "all there is". Returns None (silently) if no key is
    configured or the network call fails -- a pin claim must still succeed
    with no spend visibility rather than fail loudly over it.
    """
    key = _openrouter_key(root)
    if not key:
        return None
    key_data = _openrouter_get("https://openrouter.ai/api/v1/key", key)
    credits_data = _openrouter_get("https://openrouter.ai/api/v1/credits", key)
    parts = []
    if key_data and key_data.get("limit_remaining") is not None:
        parts.append(f"key sub-cap: ${key_data['limit_remaining']:.2f} "
                     f"remaining of ${key_data.get('limit')} (raisable)")
    if credits_data:
        total = credits_data.get("total_credits")
        used = credits_data.get("total_usage")
        if total is not None and used is not None:
            parts.append(f"account: ${total - used:.2f} remaining of "
                         f"${total:.2f} total")
    if not parts:
        return None
    return "; ".join(parts)


def cmd_meter(args: argparse.Namespace, root: Path) -> int:
    """Print context-usage fraction and optionally check against threshold."""

    guard = _check_branch_guard(root)
    if guard:
        print(guard, file=sys.stderr)
        return 1

    # Determine which log to parse. Resolution order (hypothesis:l3-meter-
    # own-transcript): --session-log, then env AGI_SESSION_LOG, then the pin
    # file, then our cwd's slug dir (newest, with a WARN), then the
    # remote-control debug log as a last resort.
    log_path, source = resolve_transcript(root=root, session_log=args.session_log,
                                          seat=getattr(args, "seat", None))

    if source.startswith("seat_pin-stale:"):
        _, written_gen, cur_gen = source.split(":")
        seat = getattr(args, "seat", None)
        print(f"ERR: seat pin for {seat!r} was written by generation "
              f"{written_gen} but this session is generation {cur_gen} -- "
              f"refusing a cross-generation read (hypothesis:l3-seat-pin-"
              f"not-repointed-on-rotation). Re-pin with `rotate.py meter "
              f"--pin {_sessions_dir(root)}/{seat}.meter` to claim the seat "
              f"before trusting --seat {seat}.", file=sys.stderr)
        return 1

    if source == "pin_unattributed":
        # A seatless read that falls to the newest-mtime pin search and the
        # winner is another agent's generation-bearing pin cannot attribute
        # that transcript to this caller (hypothesis:l4-the-meter-adopts-a-
        # pin-it-did-not-write). Refuse and name what would supply identity
        # -- never print a confident number for a session we did not name.
        print("ERR: the newest pin a seatless read would consult belongs to "
              "another agent (it carries an owner's generation) -- refusing "
              "to report a number for a transcript the caller did not name. "
              "Supply identity: run `rotate.py meter --seat <NAME>` to read "
              "your own seat's pin, or `rotate.py meter --session-log <path>` "
              "to name the transcript explicitly.", file=sys.stderr)
        return 1

    if source in ("explicit-missing", "AGI_SESSION_LOG-missing",
                  "pin_file-missing"):
        # An explicit/environment pin was set but names a missing file: that is
        # a fault, not a hint to read someone else's newest transcript on
        # their behalf. Name what was asked for.
        hint = {
            "explicit-missing": f"--session-log {args.session_log}",
            "AGI_SESSION_LOG-missing": f"${AGI_SESSION_LOG_VAR} "
                                       f"={os.environ.get(AGI_SESSION_LOG_VAR)}",
            "pin_file-missing": f"pin file under {_sessions_dir(root)}",
        }[source]
        print(f"ERR: could not read the pinned transcript ({hint}) not found.",
              file=sys.stderr)
        return 1
    if log_path is None:
        # no transcript anywhere (slug dirs empty): remote-control log fallback
        rc_path = root / REMOTE_CONTROL_LOG
        if rc_path.exists():
            log_path = rc_path
            source = "rc_log"
        else:
            print("ERR: no session log found. Tried env "
                  f"${AGI_SESSION_LOG_VAR}, pin files under "
                  f"{_sessions_dir(root)}/*.meter, transcripts for "
                  f"cwd slug ({_derive_cc_slug(os.getcwd())}), and the "
                  f"remote-control log ({REMOTE_CONTROL_LOG}).",
                  file=sys.stderr)
            return 1
    if source == "cc_transcript_slug":
        # The heuristic fallback: nothing pinned this agent to its own
        # transcript, so the newest file in the slug dir won. Name it so the
        # operator can see whether it really is this agent's.
        print(f"warn: no --session-log/env/pin; read the NEWEST transcript in "
              f"slug dir by heuristic: {log_path}", file=sys.stderr)

    if getattr(args, "pin", None) and log_path is not None:
        # Write the pin naming the transcript just read, so later meters for
        # this agent read the SAME file even as newer foreign transcripts land
        # (hypothesis:l3-meter-own-transcript). When the pin is a SEAT pin
        # (named `<seat>.meter`, or written with --seat) stamp it with the
        # writer's own generation so a later read by a DIFFERENT generation
        # (rotation happened, the pin was never re-pointed) is detectable
        # (hypothesis:l3-seat-pin-not-repointed-on-rotation) instead of
        # silently handing over a predecessor's stale number.
        #
        # Identity is supplied, never inferred (hypothesis:l4-the-meter-
        # adopts-a-pin-it-did-not-write). A pin records WHOM a transcript
        # belongs to, so it may record only a transcript the caller explicitly
        # named (rule 1 --session-log or rule 2 $AGI_SESSION_LOG), or one a
        # NAMED seat attributes. A bare --pin (none of those) would adopt
        # whichever foreign pin is newest in the shared sessions dir and then
        # re-stamp it with THIS caller's own generation -- the re-stamp that
        # silences seat_pin-stale, the very guard this repair exists to
        # trigger. Refuse and name the exact command that supplies identity.
        env_log = os.environ.get(AGI_SESSION_LOG_VAR)
        identity_supplied = (args.session_log is not None or env_log
                             or getattr(args, "seat", None) is not None)
        if not identity_supplied:
            print(
                f"ERR: --pin needs an identity to record. A bare --pin could "
                f"adopt another agent's pin and certify it with your own "
                f"generation. Run: rotate.py meter --pin "
                f"{Path(args.pin).resolve()} --session-log "
                f"<path-to-the-transcript-you-own>", file=sys.stderr)
            return 1
        pinp = Path(args.pin).expanduser().resolve()
        pinp.parent.mkdir(parents=True, exist_ok=True)
        seat_for_gen = getattr(args, "seat", None)
        if not seat_for_gen and pinp.name.endswith(METER_PIN_EXT):
            seat_for_gen = pinp.stem
        if seat_for_gen:
            cur_gen = _read_generation(root, seat_for_gen)
            pinp.write_text(f"{cur_gen}\t{log_path}\n", encoding="utf-8")
        else:
            pinp.write_text(str(log_path) + "\n", encoding="utf-8")

        # A pin claim is a fresh generation's first act, so it is the moment
        # a stale spend assumption is most expensive to carry forward
        # (owner, 2026-09-08 -- see fresh_spend_status's docstring for the
        # exact error this closes). Best-effort: silent on no key/network.
        spend = fresh_spend_status(root)
        if spend:
            print(f"spend (fresh at claim): {spend}")

    # Parse usage
    usage = None
    if source in ("explicit", "AGI_SESSION_LOG", "pin_file",
                  "cc_transcript_slug"):
        usage = parse_usage_from_cc_transcript(log_path)
        if usage is None and source == "explicit":
            # Retry as RC log
            usage = parse_usage_from_rc_log(log_path)
            if usage is not None:
                source = "rc_log"
    elif source == "rc_log":
        usage = parse_usage_from_rc_log(log_path)
    else:
        usage = parse_usage_from_cc_transcript(log_path)

    if usage is None:
        print(f"warn: no usage data found in {log_path} "
              f"(via {usage_source_name(source)}).", file=sys.stderr)
        threshold = load_ladder_field(root, "director_rotate_at",
                                      DEFAULT_DIRECTOR_ROTATE_AT)
        print(f"0.0\t(no usage data)\tsource={usage_source_name(source)}\t"
              f"threshold={threshold}")
        if args.check:
            return 0  # 0.0 is below threshold, so --check passes
        return 0

    context_tokens = load_ladder_field(root, "director_context_tokens",
                                       DEFAULT_DIRECTOR_CONTEXT_TOKENS)
    threshold = load_ladder_field(root, "director_rotate_at",
                                  DEFAULT_DIRECTOR_ROTATE_AT)

    fraction = calculate_fraction(usage, context_tokens)

    tokens_used = (
        usage.get("input_tokens", 0)
        + usage.get("cache_read_input_tokens", 0)
        + usage.get("cache_creation_input_tokens", 0)
    )

    print(f"{fraction:.4f}\t{tokens_used}/{context_tokens} tokens\t"
          f"source={usage_source_name(source)}\tthreshold={threshold}")

    if args.check:
        if fraction >= threshold:
            return 1
        return 0
    return 0


# --- spawn subcommand -----------------------------------------------------


def _shell_cmd(claude_cmd: list[str], settings, *, seat: str | None = None) -> str:
    """The quoted shell line that launches `claude_cmd`.

    Three exports may ride in front of the command, and all compose:
    every launch carries CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 so the
    background-shell reaper is disarmed in the launched shell's OWN
    environment rather than inherited from the tmux session, which is one
    server restart from gone (hypothesis:l4-spawn-paths-export-the-reaper-knob);
    an ultracode role's launch additionally exports CLAUDE_CODE_WORKFLOWS=1
    (hypothesis:l3-rotate-ultracode-env); a SEAT successor's launch exports
    AGI_SEAT so the SessionStart hook COPY (cc-session-start.next.sh, which
    keys its bootstrap injection on AGI_SEAT) can fire at turn one on the
    live path (hypothesis:l4-startup-first-turn-is-performed-by-the-service-
    and-the-hook-fires-at-turn-one). AGI_SEAT is emitted only when a seat is
    given, so a plain `spawn`/`loop` with NO seat stays byte-identical to
    today — the export appears only for a seat successor.

    `claude_cmd` is quoted element by element, so the constitution head riding
    in argv survives whatever is prepended.
    """
    joined = " ".join(shlex.quote(c) for c in claude_cmd)
    # AGI_SEAT rides FIRST in the export chain, so it is set before the
    # reaper/ultracode knobs and the claude process — composed the same way
    # REAPER_ENV_EXPORT already composes, as one `... && ...` line.
    cmd = joined
    if seat is not None:
        cmd = f"export AGI_SEAT={shlex.quote(seat)} && " + cmd
    reaper = REAPER_ENV_EXPORT + " && " + cmd
    if _is_ultracode(settings):
        return ULTRACODE_ENV_EXPORT + " && " + reaper
    return reaper


# tmux refuses a command longer than its own buffer with `command too long`.
# Measured 2026-09-08 (hypothesis:l3-rotate-launch-window-silent-failure): the
# prime's own rotation line is ~16KB because the constitution head rides in
# argv, `spawn` cleared the limit by roughly 200 bytes and `loop` -- which
# appends the rotation continuation -- did not. Anything above this goes
# through a script file instead, so the launch line's length stops mattering.
# POST-TRIM (l3w4-context-load-minimal move ONE, brief.py prayers-only head):
# the successor prompt for the prime is now measured 2140 tokens / 8436 bytes
# (head 611 tok + prime-director-successor.md body 1529 tok), well under the
# old ~16KB, but still past `_TMUX_ARG_SAFE`, so the script path stays the
# rule rather than the exception.
_TMUX_ARG_SAFE = 8192


def _launch_window(tmux_session: str, name: str, shell_cmd: str) -> int:
    """Run `shell_cmd` in a new tmux window. Returns 0 on success.

    Two failures were live here until 2026-09-08 and both were silent, which
    is why three primes in a row saw `loop` report a rotation that had not
    happened (traps 0o and the Rotation section of HANDOFF.md):

    1. **tmux's `command too long`.** The whole `claude` invocation, including
       the constitution head, was handed to `tmux new-window` as one argv
       element. Past roughly 16KB tmux refuses outright. `spawn` and `loop`
       build the same line and differ only by the 214-byte continuation, so
       one worked and one did not -- a knife-edge, not a design. Above
       `_TMUX_ARG_SAFE` the command is written to a mode-0600 script and tmux
       is handed `bash <script>`, a few dozen bytes, so growth in the head or
       the prompt can no longer break rotation. The script is deliberately
       NOT deleted: bash reads a script incrementally, so removing it early
       can truncate a running successor.
    2. **The return code was discarded.** `subprocess.run` captured tmux's
       stderr into a variable that was thrown away and the function returned
       0 unconditionally, so `command too long` never reached a human. The
       downstream window-existence check added at L3.33 caught the *symptom*;
       this returns the *cause*.
    """
    launch_cmd = f"cd {shlex.quote(os.getcwd())} && {shell_cmd}"
    if len(launch_cmd) > _TMUX_ARG_SAFE:
        fd, script = tempfile.mkstemp(prefix=f"agi-launch-{name}-",
                                      suffix=".sh")
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("#!/usr/bin/env bash\n")
            fh.write(launch_cmd + "\n")
        launch_cmd = f"bash {shlex.quote(script)}"
    try:
        # L4.114 (s3): `-P -F '#{window_id}'` makes tmux print the new
        # window's @id on stdout so the caller can JOIN the successor by its
        # WINDOW @id (the `-P` flag was missing here before this round; a
        # rename/kill addressed the window by dotted name, which real tmux
        # refuses — see proof (d), owned by kid 2). The @id is discarded when
        # no one reads it; capture happens in _successor_window_id.
        proc = subprocess.run(
            ["tmux", "new-window", "-t", tmux_session, "-n", name,
             "-P", "-F", "#{window_id}", launch_cmd],
            capture_output=True, text=True, timeout=10,
        )
    except FileNotFoundError:
        print("ERR: tmux not found. Install tmux or pass --dry-run to preview.",
              file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print("warn: tmux new-window timed out — window may still be created.",
              file=sys.stderr)
        return 0
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip() or "<no output>"
        print(f"ERR: tmux new-window failed for {name!r} "
              f"(rc={proc.returncode}): {detail}", file=sys.stderr)
        return proc.returncode
    return 0


def spawn_window(*, name: str, tier: str, prompt_file: str,
                 model=None, effort=None, settings=None,
                 tmux_session: str = DEFAULT_TMUX_SESSION,
                 window_path: str | None = None, root: Path | None = None,
                 dry_run: bool = False, debug_file: str | None = None,
                 extra: str = "",
                 seat: str | None = None,
                 successor_argv: str | None = None) -> tuple[int, str]:
    """THE one launch path shared by `cmd_spawn` and `cmd_loop`
    (hypothesis:l3w4-seat-transport).

    Resolves model/effort/settings for `tier` from the ladder row (caller
    flags already overridden), builds the `claude --remote-control <name>`
    command, quotes it for the shell and (unless dry-run) opens it in a new
    tmux window. Refuses when a window of that name already exists. Core is
    not prime-specific -- any named seat may launch through it.

    `seat` (hypothesis:l4-startup-first-turn-is-performed-by-the-service-...)
    is the successor's SEAT identity, exported into the launched shell as
    AGI_SEAT BEFORE the claude process starts. Only a caller that OWNS a
    concrete seat passes it (cmd_rotate_self, cmd_seats_launch); a generic
    spawn/loop passes None and the launch line stays byte-identical to
    today (see _shell_cmd).

    `successor_argv` (hypothesis:l3-rotate-self-successor-override) is an
    EXPLICIT stand-in command that replaces the real claude successor. When
    given, that shell line is launched verbatim (still through _launch_window,
    still gated by the same-name window refusal, still reading its `continue`
    back from the successor's own debug file). It is impossible to trip by
    accident: it only takes effect when an explicit override string is passed,
    so the DEFAULT is byte-for-byte today's real `claude --remote-control`.

    Returns `(exit_code, shell_cmd)`. On dry-run the shell line is printed
    and (0, shell_cmd) returned; every failure prints its ERR and returns
    a non-zero exit code with an empty string.
    """
    if not name or not re.match(r"^[A-Za-z0-9_-]+$", name):
        print(f"ERR: invalid name {name!r}. Use letters, digits, hyphens, "
              f"or underscores.", file=sys.stderr)
        return 1, ""

    # Resolve model / effort / settings (caller flags override role defaults)
    if root is not None:
        if not model:
            model = load_role(root, tier, "model")
        if not effort:
            effort = load_role(root, tier, "effort")
        if settings is None:
            settings = load_role(root, tier, "settings")

    if root is not None and not debug_file:
        # (w2) route the DEFAULT debug log through `_sessions_dir` (the ONE
        # resolver the pins share), not the relative string `.agi/sessions/...`
        # which `Path(dbg).resolve()` in the read-back resolves against CWD --
        # a seat running from its worktree therefore reads+writes a DIFFERENT
        # file from one in the main checkout. Explicit `--debug-file` still wins.
        dbg = str(_sessions_dir(root) / f"{name}.log")
    else:
        dbg = debug_file or f".agi/sessions/{name}.log"

    # An explicit stand-in successor command (hypothesis:l3-rotate-self-
    # successor-override): the override REPLACES the claude argv entirely.
    # It only takes effect when passed explicitly — the default below is
    # byte-for-byte today's real claude successor.
    if successor_argv is not None:
        shell_cmd = successor_argv
    else:
        # A non-prime seat spawned with no explicit --prompt-file gets its body
        # from the assembled brief. assemble() already inserts the constitution
        # head, so we skip successor_prompt() — calling both would double-insert it
        # (hypothesis:l3w4-liaison-seat). The prime's static-file path, and any
        # explicit --prompt-file, are untouched.
        if prompt_file is None and tier != "prime_director":
            claude_cmd = _assembled_successor_command(
                name=name, tier=tier, model=model, effort=effort,
                settings=settings, debug_file=dbg, extra=extra,
            )
        else:
            if prompt_file is None:
                prompt_file = DEFAULT_PROMPT_FILE
            pf = Path(prompt_file).expanduser().resolve()
            if not pf.exists():
                print(f"ERR: prompt file not found: {prompt_file}", file=sys.stderr)
                return 1, ""
            claude_cmd = _successor_command(
                name=name, tier=tier, prompt_file=str(pf),
                model=model, effort=effort, settings=settings, debug_file=dbg,
                extra=extra,
            )

        # Quote for shell display (ultracode roles are env-gated + keyworded)
        shell_cmd = _shell_cmd(claude_cmd, settings, seat=seat)

    if dry_run:
        print(shell_cmd)
        return 0, shell_cmd

    # Refuse when a window of that name already exists
    existing = _existing_windows(tmux_session, window_path)
    if name in existing:
        print(f"ERR: tmux window {name!r} already exists in session "
              f"{tmux_session!r}. Use a different name.",
              file=sys.stderr)
        return 1, ""

    rc = _launch_window(tmux_session, name, shell_cmd)
    return rc, shell_cmd


def cmd_spawn(args: argparse.Namespace, root: Path | None) -> int:
    """Build and (unless --dry-run) run a `claude --remote-control` command."""

    if root is not None:
        guard = _check_branch_guard(root)
        if guard:
            print(guard, file=sys.stderr)
            return 1

    name = args.name
    if not name:
        existing = _existing_windows(args.tmux_session or DEFAULT_TMUX_SESSION,
                                     args.window_path)
        name = _derive_successor_name(existing, prefix="belam")

    tmux_session = args.tmux_session or DEFAULT_TMUX_SESSION
    rc, _ = spawn_window(
        name=name, tier=args.tier,
        prompt_file=args.prompt_file,
        model=args.model, effort=args.effort,
        settings=json.loads(args.settings) if args.settings else None,
        tmux_session=tmux_session, window_path=args.window_path, root=root,
        dry_run=args.dry_run,
        successor_argv=getattr(args, "successor_argv", None),
    )
    if rc != 0:
        return rc
    if not args.dry_run:
        print(f"spawned {name!r} in tmux session {tmux_session!r}")
        print(f"  watch at: https://claude.ai/chat (remote-control mode)")
    return 0


# --- loop subcommand ------------------------------------------------------

# NOTE: the legacy debug-log read-back (`_read_first_reply` / `_is_log_noise`)
# is DELETED, not kept as a fallback (hypothesis:l4-rotate-readback-false-
# negative-and-the-orphan-by-design): a DEBUG LOGGER cannot carry the
# successor's prose (42 seat logs, ~295k lines, 0 non-noise line), so a
# fallback that opens one is the defect wearing a safety label. The reply
# channel is the explicit, identity-supplied ACK below.


def _ack_path(root: Path, seat: str) -> Path:
    """`<graph>/sessions/seats/<seat>.ack.json` — the explicit reply channel.

    The replacement for the debug-log read-back (hypothesis:l4-rotate-
    readback-false-negative-and-the-orphan-by-design): the successor writes
    its ACK here with its OWN identity (`gen_after`, `session_ref`), instead
    of the predecessor trying to read a reply out of a DEBUG LOGGER that can
    never carry prose (42 seat logs, ~295k lines, 0 non-noise). Same seats
    dir as the handoff, because that is the one place both sides already
    address from any cwd.
    """
    return _seat_hands(root) / f"{seat}.ack.json"


def _resolve_seat_for_name(root: Path, session_name: str) -> str:
    """The SEAT for a session/window name, resolved through the seats row.

    The ACK channel is keyed by the SEAT name everywhere (`_ack_path(root,
    seat)`); `rotate.py ack --seat <seat>` is the ONE call that writes it. A
    reader that holds only a numeral-chain session/window name
    (`belam-S1-L4-VII` — the successor's tmux window / remote-control name)
    resolves the SEAT through config:seats (the row's `name` is the seat; the
    numeral is the session/window name), so it reads the SAME
    `<sessions>/seats/<seat>.ack.json` the one ack wrote — not a phantom
    per-numeral file. A name with no matching row (a THROWAWAY / unregistered
    numeral) falls back to the name itself, so existing plain-seat paths are
    unchanged. P2, fifth fix-only dispatch.

    **L4.122 merge-up 24 residue (S): LONGEST-prefix match, never first.** A
    seat that is a DASH-PREFIX of another (rows `a` and `a-b`) must resolve
    `a-b-X` to the `a-b` seat, not the shorter `a` — first-match caused the
    wrong ack path / row. Collect every matching row and keep the LONGEST
    name.
    """
    best = None
    for row in _load_seats(root):
        rname = row.get("name") or ""
        if rname and (session_name == rname
                      or session_name.startswith(rname + "-")):
            if best is None or len(rname) > len(best):
                best = rname
    return best if best is not None else session_name


def _read_ack(path: str | Path, gen_after: int | None, timeout: int = 600) \
        -> dict | None:
    """Poll `<seat>.ack.json` until it carries an ACK for `gen_after`.

    Returns the parsed ack dict when the file exists AND its `gen_after`
    equals the generation the reader spawned (identity supplied, never
    inferred — the L4.99 rule); None on timeout. An ACK with the WRONG
    generation is REFUSED (treated as absent), so a stale or foreign ack left
    in a reused seat name can never confirm a successor it was not written
    for."""
    p = Path(path).expanduser()
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if p.exists():
                ack = json.loads(p.read_text(encoding="utf-8", errors="replace"))
                if not isinstance(ack, dict):
                    pass  # malformed shape — keep polling
                elif gen_after is None or ack.get("gen_after") == gen_after:
                    if ack.get("answer") == "pending":
                        # L4.114 (s6/s7): the predecessor writes `pending` as
                        # the ack's initial state (carrying the machine
                        # identity) and the SUCCESSOR flips it to continue/
                        # diff. A `pending` answer is not terminal — keep
                        # polling for the flip, it cannot confirm a rotation.
                        pass
                    else:
                        return ack
        except (OSError, ValueError):
            pass
        time.sleep(2)
    return None


def cmd_ack(args: argparse.Namespace, root: Path) -> int:
    """The successor's explicit, identity-supplied reply to its rotation.

    `rotate.py ack --seat S --gen N --ref <ref> continue|diff [--text -]`
    writes `<sessions>/seats/<seat>.ack.json` carrying `seat`/`gen_after`/
    `session_ref`/`answer`/`text`/`ts`. Both rotation readers (cmd_loop and
    cmd_rotate_self) read THAT file after the spawn cursor and refuse an ack
    whose gen_after is not the generation they spawned.

    DEPRECATED since L4.112 (E): the WRITE of the ack moves to the predecessor
    inside rotate-self (kid 2), so the successor makes ZERO tool calls on wake.
    Kept CALLABLE for one generation as a fallback; the help text marks it.
    """
    if root is None:
        print("ERR: ack needs an agi project root.", file=sys.stderr)
        return 1
    seat = args.seat
    if args.answer not in ("continue", "diff"):
        print(f"ERR: answer must be `continue` or `diff`, got {args.answer!r}.",
              file=sys.stderr)
        return 1
    text = args.text
    if text == "-":
        # `--text -` reads the diff body from stdin: a long diff can exceed
        # one shell argument, so the successor streams it in.
        text = sys.stdin.read()
    ack = {
        "seat": seat,
        "gen_after": args.gen,
        "session_ref": args.ref or "",
        "answer": args.answer,
        "text": text or "",
        "ts": datetime.utcnow().isoformat() + "Z",
    }
    path = _ack_path(root, seat)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ack, indent=2) + "\n", encoding="utf-8")
    print(f"ack written: {path}")
    # r3: `--ref` back-fills session_ref into the successor's OWN seats row
    # through the self_row write (source: ack), so a later whois can
    # authorize by it. A THROWAWAY seat has no row; the back-fill is recorded
    # skipped and the ack still lands.
    if args.ref:
        try:
            print(_backfill_session_ref(
                root, seat=seat, role="parent", ref=args.ref))
        except Exception as exc:  # noqa: BLE001
            print(f"warn: session_ref back-fill failed: {exc}",
                  file=sys.stderr)
    return 0


def cmd_loop(args: argparse.Namespace, root: Path) -> int:
    """The super-ralph rotation primitive: meter, rotate when due, confirm.

    Meter; when under director_rotate_at (and not --force), hold with no
    rotation. Otherwise derive the successor name (`<base>-<ROM>` unless
    --name-prefix/-name), spawn it with head + prompt-file body, then read
    the successor's first reply from its log: the single word `continue`
    means the handoff stood with no change.
    """
    if root is None:
        print("ERR: loop needs an agi project root.", file=sys.stderr)
        return 1

    guard = _check_branch_guard(root)
    if guard:
        print(guard, file=sys.stderr)
        return 1

    if not args.force:
        meter_args = SimpleNamespace(session_log=args.session_log, check=True)
        meter_code = cmd_meter(meter_args, root)
        if meter_code == 0:
            print("BELOW director_rotate_at: no rotation, loop holds.",
                  file=sys.stderr)
            return 0

    role = args.role
    tmux_session = args.tmux_session or DEFAULT_TMUX_SESSION
    existing = _existing_windows(tmux_session, args.window_path)
    name = args.name or _derive_successor_name(
        existing, prefix=args.name_prefix or "belam")

    continuation = (
        "ROTATION CONTINUATION: acknowledge your handoff with the explicit "
        "ACK channel, not a bare word. First act after reading: run "
        "`python3 extensions/agi/bin/rotate.py ack --seat <your seat name> "
        "--gen <N> --ref <your own ListAgents ref> continue` if the handoff "
        "needs no change, or `... diff --text '<the exact diff>'` if it does. "
        "The predecessor's read-back reads THAT ack file and refuses an ack "
        "whose gen_after is not your generation."
    )
    rc, _ = spawn_window(
        name=name, tier=role,
        prompt_file=args.prompt_file,
        model=args.model, effort=args.effort,
        settings=json.loads(args.settings) if args.settings else None,
        tmux_session=tmux_session, window_path=args.window_path, root=root,
        dry_run=args.dry_run, debug_file=args.debug_file, extra=continuation,
        successor_argv=getattr(args, "successor_argv", None),
    )
    if rc != 0:
        return rc

    if args.debug_file:
        debug_file = args.debug_file
    else:
        # (w2) the default successor debug log is shared-room (see the branch
        # in spawn_window): route through `_sessions_dir` so the predecessor's
        # read-back and the successor's writes address the SAME file from any
        # cwd (worktree seat or main checkout).
        debug_file = str(_sessions_dir(root) / f"{name}.log")
    print(f"rotate {role!r} --> successor {name!r}")

    if args.dry_run:
        return 0

    # FAIL LOUDLY WINDOW-CHECK (hypothesis:l3w4-seat-rotation-loops ADDENDUM,
    # Belam VII's own rotation): the successor's tmux window must actually be
    # present and answering before loop reports rotation success. A prime that
    # believed a success line with no successor window behind it would emit its
    # closing prayer and exit, stranding the ladder with no prime at all.
    # The observation is taken from tmux list-windows (or the window-path
    # stand-in), NEVER from the spawn tool's return value, and the rotation
    # records itself durably either way.
    succ = _observed_windows(tmux_session, args.window_path)
    if name not in succ["names"]:
        _write_rotation_record(root, _loop_record(
            name=name, result="refused",
            succ=succ, readback_log=Path(debug_file).expanduser().resolve(),
            refusal="successor window absent"))
        print(f"ERR: successor window {name!r} is NOT present in tmux session "
              f"{tmux_session!r}; refusing to report rotation success "
              f"(windows: {succ['names']!r}).",
              file=sys.stderr)
        return 1

    # The successor's reply is the EXPLICIT ACK channel
    # (hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-design),
    # written by the successor with its OWN identity. The DEBUG LOGGER the old
    # reader opened cannot carry prose (42 seat logs, ~295k lines, 0 non-
    # noise), so it is DELETED, not kept as a fallback. `loop` manages no
    # generation (it records and announces gen_before=None, gen_after=None), so
    # there is no gen_after to check here; the ack's seat is bound by its
    # per-seat file path, and generation-checking lives on the rotate-self path
    # that owns the meter. A missing checksum here is a DOCUMENTED residue, not
    # a silent gap (see the experiment under hypothesis:l4-rotate-readback-
    # false-negative-and-the-orphan-by-design).
    #
    # P2 (fifth dispatch): the ACK channel is keyed by the SEAT name
    # EVERYWHERE. `name` here is the successor's session/window name (a
    # numeral chain for the prime — `belam-S1-L4-<numeral>`), so resolve the
    # SEAT through the seats row and read `_ack_path(root, seat)`; a numeral
    # ack written under `--seat belam` must reach this exact file. A name with
    # no row falls back to the name itself (THROWAWAY seat unchanged).
    ack_seat = _resolve_seat_for_name(root, name)
    ack_path = _ack_path(root, ack_seat)
    ack = _read_ack(ack_path, gen_after=None, timeout=args.timeout)
    if ack is not None:
        answer = ack.get("answer")
        if answer == "diff":
            _write_rotation_record(root, _loop_record(
                name=name, result="diff", succ=succ,
                readback_log=Path(ack_path).expanduser().resolve(),
                reply_decision="diff"))
            print("successor acked diff (handoff needs change):",
                  file=sys.stderr)
            txt = ack.get("text") or ""
            if txt:
                print("  " + txt.strip().replace("\n", "\n  "),
                      file=sys.stderr)
            return 0
        # answer == continue
        _write_rotation_record(root, _loop_record(
            name=name, result="success", succ=succ,
            readback_log=Path(ack_path).expanduser().resolve(),
            reply_decision="continue"))
        print("handoff stood: successor acked `continue`.", file=sys.stderr)
        import send  # local: same dir
        _announce_rotation(
            root=root,
            croot=send.comms_root(root, getattr(args, "comms_root", None)),
            seat=ack_seat, successor=name, gen_before=None, gen_after=None,
            trigger="--force" if getattr(args, "force", False) else "meter due",
            handoff_path=str(Path(ack_path).expanduser().resolve()),
            in_flight="successor acked `continue`; handoff stood",
            live_names=succ.get("names", []))
        return 0

    # Three realities, one record (ACKED / PRESENT-BUT-SILENT / ABSENT): the
    # successor window was already confirmed present above, and no ack arrived
    # -> PRESENT-BUT-SILENT, recorded inconclusive; never confirmed.
    rb = Path(ack_path).expanduser().resolve()
    _write_rotation_record(root, _loop_record(
        name=name, result="inconclusive-no-reply", succ=succ,
        readback_log=rb, reply_decision="no_reply"))
    print("warn: successor window present but no ACK arrived (give it time, "
          "then re-run loop).", file=sys.stderr)
    return 0


# --- status subcommand ----------------------------------------------------


def _record_is_terminal(path) -> bool:
    """True when the rotation record has a present s12_self_reap section —
    the terminal sentinel `--wait` polls for (L4.233). Best-effort: a record
    that does not parse is not terminal."""
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return False
    return isinstance(doc.get("s12_self_reap"), dict)


def _poll_record_terminal(path, wait: int) -> tuple[bool, str]:
    """Poll `path` at a <=2s interval until its s12_self_reap section is
    present, or `wait` seconds elapse. Returns (terminal, last_seen_text).
    When the record is already terminal on the first read it returns True
    immediately — never sleeps past an already-terminal record."""
    deadline = time.monotonic() + max(0, wait)
    last = ""
    while True:
        try:
            last = Path(path).read_text(encoding="utf-8")
        except OSError:
            last = ""
        if _record_is_terminal(path):
            return True, last
        if time.monotonic() >= deadline:
            return False, last
        time.sleep(min(2.0, max(0.05, deadline - time.monotonic())))


def cmd_status(args: argparse.Namespace, root: Path | None = None) -> int:
    """List tmux windows in sessions whose name starts with agi-master or
    belam; with `--seats`, list the registry seats instead — one line per
    row of seat/generation/fraction/age ("each layer lasts longer" is read
    here, never enforced).

    `--seats` is the graph-reading half and needs the project root; tmux is
    never touched for it."""

    if getattr(args, "record", None):
        # hypothesis:l4-rotations-startup-commands-must-parse — the read a
        # rotated-in seat does first thing, in the FIRST TURN: the latest
        # durable rotation record for its seat + the current sequence + its
        # own row. Read-only; never touches tmux and never writes (it replaces
        # the old first_turn `rotate.py whois`, which did not exist).
        seat = getattr(args, "seat", None)
        if not seat:
            print("ERR: --record latest needs --seat <seat>", file=sys.stderr)
            return 2
        if root is None:
            print("ERR: --record needs an agi project root", file=sys.stderr)
            return 1
        rot_dir = _rotations_dir(root)
        files = sorted(rot_dir.glob(f"{seat}.*.json")) if rot_dir.exists() else []
        if not files:
            print(f"(no rotation record for {seat})")
        else:
            latest = files[-1]
            # hypothesis:rotate-status-record-latest-gains-wait (L4.233) —
            # `--wait N` re-reads the latest record until its s12_self_reap
            # section is terminal, or N seconds elapse. A caller that needs
            # the terminal result no longer hand-rolls a sleep+reinvoke loop.
            wait = int(getattr(args, "wait", 0) or 0)
            if wait > 0:
                terminal, last_txt = _poll_record_terminal(latest, wait)
                if not terminal:
                    print(f"# latest rotation record: {latest.name}")
                    print(last_txt, end="")
                    print(f"ERR: still not terminal after {wait}s",
                          file=sys.stderr)
                    return 2
            try:
                print(f"# latest rotation record: {latest.name}")
                print(latest.read_text(encoding="utf-8").rstrip())
            except OSError as exc:
                print(f"ERR: could not read latest record: {exc}",
                      file=sys.stderr)
                return 1
        print(f"sequence={_current_sequence(root)}")
        row = _find_seat(root, seat)
        if row is None:
            print(f"(no seats row for {seat})")
        else:
            gen = _read_generation(root, seat)
            frac = _seat_fraction(root, row)
            frac_str = "?" if frac is None else f"{frac:.3f}"
            print(f"row: {seat}\tgen={gen}\tfrac={frac_str}")
        return 0

    if getattr(args, "seats", False):
        if root is None:
            print("ERR: --seats needs an agi project root", file=sys.stderr)
            return 1
        for row in _load_seats(root):
            seat = row.get("name") or "?"
            gen = _read_generation(root, seat)
            frac = _seat_fraction(root, row)
            frac_str = "?" if frac is None else f"{frac:.3f}"
            pin = find_pin_log(root, seat)
            age_str = "?"
            if pin is not None:
                try:
                    age_sec = int(time.time() - pin.stat().st_mtime)
                    age_str = f"{age_sec // 60}m{age_sec % 60}s"
                except (OSError, ValueError):
                    pass
            print(f"{seat}\tgen={gen}\tfrac={frac_str}\tage={age_str}")
        return 0

    try:
        result = subprocess.run(
            ["tmux", "list-sessions", "-F", "#{session_name}"],
            capture_output=True, text=True, timeout=5,
        )
    except FileNotFoundError:
        print("ERR: tmux not found.", file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print("warn: tmux list-sessions timed out.", file=sys.stderr)
        return 1

    if result.returncode != 0:
        print("(no tmux sessions)", file=sys.stderr)
        return 0

    sessions = [s.strip() for s in result.stdout.strip().splitlines()
                if s.strip().startswith("agi-master")
                or s.strip().startswith("belam")]
    if not sessions:
        print("(no agi-master or belam tmux sessions)")
        return 0

    now = time.time()
    for sess in sorted(sessions):
        try:
            win_result = subprocess.run(
                ["tmux", "list-windows", "-t", sess,
                 "-F", "#{window_name}\t#{window_active}\t#{window_activity}"],
                capture_output=True, text=True, timeout=5,
            )
            for line in win_result.stdout.strip().splitlines():
                parts = line.split("\t", 2)
                if len(parts) < 3:
                    continue
                wname, active, activity_ts = parts
                try:
                    age_sec = int(now - int(activity_ts))
                    age_str = f"{age_sec // 60}m{age_sec % 60}s"
                except (ValueError, TypeError):
                    age_str = "?"
                active_mark = " *" if active == "1" else ""
                print(f"  {sess}:{wname}{active_mark} ({age_str})")
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            print(f"  {sess}: (could not list windows)")
    return 0


# --- seats registry (config:seats) -----------------------------------------


def _load_seats(root: Path | None) -> list[dict]:
    """The `seats:` rows of `.agi/nodes/.geometry/seats.md` (config:seats),
    or [] when absent/unparseable."""
    if root is None:
        return []
    path = Path(root) / "nodes" / ".geometry" / "seats.md"
    if not path.exists():
        return []
    try:
        nf = frontmatter.load_node_file(path)
        seats = nf.frontmatter.get("seats") or []
        if isinstance(seats, list):
            return [r for r in seats if isinstance(r, dict)]
    except Exception:
        pass
    return []


def _find_seat(root: Path | None, name: str) -> dict | None:
    for row in _load_seats(root):
        if row.get("name") == name:
            return row
    return None


# --- rotation templates (.geometry/rotations.md) ---------------------------
# L4.110 owner amendment: rotations are config-maxxed — a .geometry config
# node (rotations.md, type config, written_by owner/prime_director) carries
# named templates; each role names a default; rotate-self resolves
# --template > role default > refuse loudly naming the node. A TEMPLATE is a
# named {brief_file, steps[], telemetry[]}. No brief path is hardcoded in
# rotate.py — the brief file travels in the template.


def _rotations_node_path(root: Path) -> Path:
    return Path(root) / "nodes" / ".geometry" / "rotations.md"


def _load_templates(root: Path) -> dict:
    """The `templates:` rows of `.geometry/rotations.md`, or {} when absent /
    unparseable. Each entry: role-name -> {brief_file, steps, telemetry}.
    """
    path = _rotations_node_path(root)
    if not path.exists():
        return {}
    try:
        nf = frontmatter.load_node_file(path)
        tmpl = nf.frontmatter.get("templates") or {}
    except Exception:  # noqa: BLE001
        return {}
    if not isinstance(tmpl, dict):
        return {}
    out = {}
    for name, ent in tmpl.items():
        if isinstance(ent, dict):
            out[str(name)] = ent
    return out


def _resolve_template(root: Path, role: str, explicit: str | None,
                      where: str = "rotate-self"):
    """Resolve a rotation template, fail-closed, naming the config node when
    it cannot. Resolution order is testable (L4.110 proof e/f/g):
        --template <name> > role default > refuse loudly naming the node.

    `explicit` is the literal `--template` value; when given it may name ANY
    role's template (a helper rotated on the director's template is legal).
    With no flag, the seat's own role must have a default. A missing node, an
    unknown explicit name, or a role without a default all refuse with a
    message that NAMES the node (the live state until the prime creates it).
    Returns (template_dict, resolved_name, source) or raises SystemExit-like
    refusal via a returned error string — the caller decides how to surface it.
    """
    templates = _load_templates(root)
    node = _rotations_node_path(root)
    if not templates:
        return None, None, \
            (f"no rotation templates: {node} is absent or declares none; "
             "rotate-self cannot resolve a brief/step list. "
             "(L4.110)")
    if explicit:
        t = templates.get(explicit)
        if t is None:
            return None, None, \
                (f"no template named {explicit!r} in {node} "
                 f"(have: {', '.join(sorted(templates))})")
        return t, explicit, "--template flag"
    t = templates.get(role)
    if t is None:
        return None, None, \
            (f"role {role!r} has no default template in {node} "
             f"(have: {', '.join(sorted(templates))})")
    return t, role, f"role default ({role})"


# --- complete (hypothesis:l4-seat-session-iter-dirs, half b) --------------


def _git_lines(cwd: Path, *args: str) -> list[str]:
    """Run a git command in `cwd`; return stdout split into lines."""
    out = subprocess.run(["git", "-C", str(cwd), *args],
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.strip()}")
    return [ln for ln in out.stdout.splitlines() if ln]


def _verify_tree_copy(src: Path, dst: Path) -> bool:
    """True iff `dst` holds exactly `src`'s files with equal content.

    The completeness gate for the session copy: we only tear down the seat
    worktree once its iter dirs are provably resident in main. Neither
    directory is touched by this check.
    """
    if not src.is_dir() or not dst.is_dir():
        return False
    src_files = {p for p in src.rglob("*") if p.is_file()}
    dst_files = {p for p in dst.rglob("*") if p.is_file()}
    if len(src_files) != len(dst_files):
        return False
    for sf in src_files:
        rel = sf.relative_to(src)
        df = dst / rel
        if not df.is_file():
            return False
        try:
            if sf.read_bytes() != df.read_bytes():
                return False
        except OSError:
            return False
    return True


def cmd_complete(args: argparse.Namespace, root: Path | None) -> int:
    """Retire a seat worktree after its round is merged up (hypothesis:
    l4-seat-session-iter-dirs, half b SESSION-COMPLETE).

    A seat runs in its own git worktree; its iteration session dirs
    (`sessions/iter-*`) live in that worktree's `.agi` and are gitignored, so
    a merge carries nothing. `complete` is the retirement step: it refuses
    unless the seat branch is already an ancestor of its parent branch (the
    merge-up prerequisite), copies the worktree's `iter-*` session dirs into
    the MAIN checkout's `.agi/sessions/` (never overwriting anything that
    already lives there), and only then removes the worktree and the branch.

    Refusals (exit non-zero, NOTHING removed):
      - the seat branch is not an ancestor of its parent branch (merge first);
      - the worktree is dirty (uncommitted work => the session is not done).

    `iter-*` dirs that already exist in main are left byte-for-byte intact and
    reported as skipped. The worktree's tracked content is preserved by being
    an ancestor of the parent branch, so removing the worktree and the branch
    deletes no node: the graph the worktree held is already resident in main's
    history.
    """
    wt = Path(args.worktree).resolve()
    if not wt.is_dir():
        print(f"ERR complete: worktree not found: {wt}", file=sys.stderr)
        return 1

    # Main checkout: explicit override or the common git dir's parent repo.
    main = Path(args.main).resolve() if args.main else locations.git_common_root(wt)
    if main is None or not main.is_dir():
        print(f"ERR complete: cannot resolve main checkout from {wt}",
              file=sys.stderr)
        return 1

    # The branch the seat worktree is sitting on.
    try:
        seat_branch = _git_lines(wt, "rev-parse", "--abbrev-ref", "HEAD")[0]
    except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERR complete: cannot read seat branch: {exc}", file=sys.stderr)
        return 1
    if seat_branch == "HEAD":
        print(f"ERR complete: {wt} is on a detached HEAD; a seat branch is "
              "required", file=sys.stderr)
        return 1

    # The merge-up target branch. Explicit, else the main checkout's own HEAD.
    if args.parent:
        parent_branch = args.parent
    else:
        try:
            parent_branch = _git_lines(main, "branch", "--show-current")[0]
        except (RuntimeError, OSError, subprocess.SubprocessError) as exc:
            print(f"ERR complete: cannot resolve parent branch: {exc}",
                  file=sys.stderr)
            return 1
    if not parent_branch:
        print("ERR complete: no parent branch resolvable (detached HEAD in "
              "main?); pass --parent", file=sys.stderr)
        return 1

    # --- refusal 1: merge-up prerequisite --------------------------------
    anc = subprocess.run(
        ["git", "-C", str(main), "merge-base", "--is-ancestor",
         seat_branch, parent_branch],
        capture_output=True, text=True)
    if anc.returncode != 0:
        print(f"REFUSE complete: branch {seat_branch} is not an ancestor of "
              f"{parent_branch}; merge the seat's round up first. Nothing "
              "was removed.", file=sys.stderr)
        return 1

    # --- refusal 2: dirty worktree (uncommitted work => not done) ---------
    dirty = subprocess.run(["git", "-C", str(wt), "status", "--porcelain"],
                           capture_output=True, text=True)
    if dirty.stdout.strip():
        print(f"REFUSE complete: worktree {wt} has uncommitted work "
              f"({len(dirty.stdout.splitlines())} changed paths); a seat is "
              "not complete until its round is committed and merged. Nothing "
              "was removed.", file=sys.stderr)
        return 1

    # --- copy the iter session dirs into main -----------------------------
    src_sess = wt / ".agi" / "sessions"
    dst_sess = main / ".agi" / "sessions"
    copied = []
    skipped = []
    if src_sess.is_dir():
        for name in sorted(p.name for p in src_sess.iterdir()
                           if p.is_dir() and p.name.startswith("iter-")):
            src_dir = src_sess / name
            dst_dir = dst_sess / name
            if dst_dir.exists():
                skipped.append(name)
                print(f"skip {name}: already exists in main, left byte-for-byte "
                      "intact")
                continue
            try:
                shutil.copytree(src_dir, dst_dir)
            except OSError as exc:
                print(f"ERR complete: copying {name} failed: {exc}. Nothing "
                      "removed.", file=sys.stderr)
                return 1
            copied.append(name)
            print(f"copied {name} -> {dst_sess}")

    # Completeness gate on every dir we copied AND every dir we skipped;
    # abort before any teardown. A skipped dir must match main's copy: the
    # coming `git worktree remove` deletes the worktree's copy, and when it
    # DIFFERS from main's the "left byte-for-byte intact" claim is an
    # equality nobody checked — the worktree copy is lost silently.
    # (hypothesis:l4-complete-and-fallback-invariants)
    for name in copied + skipped:
        if not _verify_tree_copy(src_sess / name, dst_sess / name):
            kind = "copied" if name in copied else "skipped"
            print(f"ERR complete: {kind} {name} does not match its copy in "
                  "main; refusing to remove the seat (main's copy is safe).",
                  file=sys.stderr)
            return 1

    # --- tear down: worktree, then branch --------------------------------
    rm = subprocess.run(["git", "-C", str(main), "worktree", "remove", str(wt)],
                        capture_output=True, text=True)
    if rm.returncode != 0:
        print(f"ERR complete: git worktree remove failed (no branch removed): "
              f"{rm.stderr.strip()}", file=sys.stderr)
        return 1
    bd = subprocess.run(["git", "-C", str(main), "branch", "-D", seat_branch],
                        capture_output=True, text=True)
    if bd.returncode != 0:
        print(f"WARN complete: worktree removed but `git branch -D "
              f"{seat_branch}` failed: {bd.stderr.strip()}", file=sys.stderr)
        print(f"REMOVED worktree {wt} (branch {seat_branch} retained)")
        return 0
    if copied or skipped:
        print(f"complete: session dirs harvested ({len(copied)} copied, "
              f"{len(skipped)} skipped); seat retired")
    else:
        print("complete: no iter-* session dirs to harvest; seat retired")
    return 0


# --- seats-launch & tiling (hypothesis:l3w4-seat-sessions-and-tiling) -----


#: The one session_kind that is ephemeral and earns NO launched window.
#: fire-and-forget is ephemeral by definition and excluded. remote-control and
#: tty are BOTH non-ephemeral and each gets a launch line, per the owner ask
#: "all of the non-ephemeral roles" and claim test 1, which excludes ONLY
#: fire-and-forget (hypothesis:l3w4-seat-sessions-and-tiling).
EPHEMERAL_KIND = "fire-and-forget"


def _seats_that_launch(rows: list[dict]) -> list[dict]:
    """The seats.md rows that get their own launched session.

    A seat is ephemeral (skipped) only when its `session_kind` is
    `fire-and-forget`. remote-control and tty rows are both non-ephemeral and
    are returned intact, because the launch reads model+effort+name+pin from
    the row.
    """
    return [r for r in rows if r.get("session_kind") != EPHEMERAL_KIND]


def cmd_seats_launch(args: argparse.Namespace, root: Path) -> int:
    """Launch one remote-control session per non-ephemeral seat, through the
    SAME `spawn_window` path the prime uses — never a second launcher
    (hypothesis:l3w4-seat-sessions-and-tiling).

    Each seat row resolves one launch with ITS model, effort and settings;
    each gets its own debug/pin file under `.agi/sessions/<name>.*` so
    rotate.py meter reads ITS transcript and not the prime's. fire-and-forget
    and tty seats are skipped. `--dry-run` prints/returns every line and
    touches nothing; a real run refuses any already-open window by name.
    """
    rows = _load_seats(root)
    targets = _seats_that_launch(rows)
    if not targets:
        print("no non-ephemeral (remote-control/tty) seats in config:seats",
              file=sys.stderr)
        return 1

    tmux_session = args.tmux_session or DEFAULT_TMUX_SESSION
    rc_all = 0
    for row in targets:
        name = row.get("name")
        if not name:
            continue
        tier = row.get("role") or "parent"
        settings = _normalize_settings(row.get("settings"))
        rc, _ = spawn_window(
            name=name,
            tier=tier,
            prompt_file=args.prompt_file,
            model=row.get("model"),
            effort=row.get("effort"),
            settings=settings,
            tmux_session=tmux_session,
            window_path=args.window_path,
            root=root,
            dry_run=args.dry_run,
            extra="",
            seat=name,
            successor_argv=getattr(args, "successor_argv", None),
        )
        if rc != 0:
            print(f"ERR: launch failed for seat {name!r} (rc={rc})",
                  file=sys.stderr)
            rc_all = 1
    if not args.dry_run and rc_all == 0:
        # READ-BACK: never trust the printed success — a rotation has reported
        # fine and spawned no window at all (trap-0c class, L3.32/33). Confirm
        # each launched seat is now a real window in the session.
        launched = [r.get("name") for r in targets if r.get("name")]
        live = _existing_windows(tmux_session, args.window_path)
        missing = [n for n in launched if n not in live]
        if missing:
            print(f"ERR: launch reported ok but read-back found no window: "
                  f"{', '.join(missing)}", file=sys.stderr)
            return 1
        print(f"seats-launch: launched {len(targets)} non-ephemeral session(s) "
              f"in tmux session {tmux_session!r}; read-back confirmed "
              f"{len(launched)}/{len(launched)} window(s)")
    return rc_all


def partition_tiles(n: int, x: int, y: int, width: int, height: int):
    """Partition rect (x,y,width,height) into exactly `n` leaf rectangles.

    Recursive balanced binary split along the longer axis, integer pixels:
    n leaves in, n rects out, no overlap, no gaps, covering `width*height`
    exactly. This is the geometry the tiler feeds a WM on X :1 so the
    livestream shows every seat session with nothing hidden behind another.
    """
    if n <= 1:
        return [(x, y, width, height)]
    a = (n + 1) // 2
    b = n - a
    if width >= height and width > 0:
        # vertical split: left column holds `a` leaves, right holds `b`
        aw = min(max(width * a // n, a), width - b)
        bw = width - aw
        return (partition_tiles(a, x, y, aw, height)
                + partition_tiles(b, x + aw, y, bw, height))
    # horizontal split: top band holds `a`, bottom holds `b`
    ah = min(max(height * a // n, a), height - b)
    bh = height - ah
    return (partition_tiles(a, x, y, width, ah)
            + partition_tiles(b, x, y + ah, width, bh))


def cmd_tile(args: argparse.Namespace, root: Path) -> int:
    """Compute (and optionally place) a full-screen partition for N windows.

    Pure geometry: reads N / W / H and prints the per-window rects, no gaps,
    no overlap. `--apply` additionally reads the LIVE window set and hands
    each rect to a WM on X :1 (wmctrl or xdotool) so the livestream shows
    every seat session with nothing hidden. Kept a separate command on
    purpose (hypothesis:l3w4-seat-sessions-and-tiling): it reads the live
    window set and re-runs whenever the set of seats changes, rather than
    being wired into spawn.
    """
    w, h = args.width, args.height
    if w < 1 or h < 1:
        print("ERR: --width/--height must be >= 1", file=sys.stderr)
        return 1
    if args.apply:
        return _cmd_tile_apply(args, root, w, h)
    n = args.count
    if n is None or n < 1:
        print("ERR: --apply, or --count N (>=1), is required",
              file=sys.stderr)
        return 1
    tiles = partition_tiles(n, 0, 0, w, h)
    if args.dry_run or not args.json:
        for i, (tx, ty, tw, th) in enumerate(tiles):
            print(f"{i}: x={tx} y={ty} w={tw} h={th}")
    if args.json:
        import json as _json
        print(_json.dumps([list(t) for t in tiles]))
    return 0


#: WM tools able to place/geometry windows on X :1, in preference order.
_WM_TOOLS = ("wmctrl", "xdotool")

#: The process runner used to issue WM commands. Indirection so tests can
#: inject a fake without touching the shared `subprocess` module.
_RUN = subprocess.run


def _screen_tool() -> str | None:
    """The first WM tool on PATH that can place a window on X :1, else None."""
    for tool in _WM_TOOLS:
        if shutil.which(tool):
            return tool
    return None


def _wm_tool_argv(tool: str, name: str, rect: tuple) -> list[str]:
    """The argv that moves/resizes window `name` to `rect` (x,y,w,h).

    wmctrl matches a window by title (our seat name) and moves/resizes in
    one call; xdotool searches by name then moves and resizes. Both target
    exactly the named terminal, so geometry never lands on the wrong pane
    (the livestream constraint: only the intended window moves).
    """
    x, y, tw, th = rect
    if tool == "wmctrl":
        return ["wmctrl", "-r", name, "-e", f"0,{x},{y},{tw},{th}"]
    if tool == "xdotool":
        return ["xdotool", "search", "--name", name,
                "windowmove", str(x), str(y),
                "windowsize", str(tw), str(th)]
    raise ValueError(f"unknown WM tool {tool!r}")


def _place_windows(rects: dict, tool: str | None,
                   run=None) -> tuple[int, int]:
    """Place each named window at its rect on X :1.

    `rects` maps name -> (x,y,w,h). `tool` None degrades to (placed=0,
    issued=0) — the caller prints the graceful-degradation note. `run` is
    injected for tests (None => the module `_RUN`). A non-zero rc for one
    window is logged and skipped, never fatal: a terminal may legitimately be
    closed.
    Returns (windows_placed, commands_issued).
    """
    if not tool:
        return 0, 0
    if run is None:
        run = _RUN
    issued, placed = 0, 0
    for name, rect in rects.items():
        argv = _wm_tool_argv(tool, name, rect)
        try:
            proc = run(argv, capture_output=True, text=True, timeout=5)
            issued += 1
            if proc.returncode == 0:
                placed += 1
            else:
                detail = (getattr(proc, "stderr", None) or "").strip()
                print(f"warn: {tool} could not place {name!r}:"
                      f" {detail or proc.returncode}", file=sys.stderr)
        except Exception as e:  # noqa: BLE001 — per-window, never fatal
            issued += 1
            print(f"warn: {tool} failed for {name!r}: {e}", file=sys.stderr)
    return placed, issued


def _live_window_names(root: Path | None, window_path: str | None,
                       tmux_session: str) -> list[str]:
    """Windows open in the seat tmux session, in tile order.

    Intersects the live window set with the non-ephemeral seat registry so
    only seat sessions (what the livestream shows) are tiled. Falls back to
    the whole live set when no seat names show up (e.g. tiling before the
    registry is read).
    """
    live = _existing_windows(tmux_session, window_path)
    if not live:
        return []
    seats = {r.get("name") for r in _seats_that_launch(_load_seats(root))}
    keep = [n for n in live if n in seats]
    return keep or live


def _cmd_tile_apply(args: argparse.Namespace, root: Path, w: int, h: int) -> int:
    """Place the live seat windows on X :1 at a full-screen partition.

    Reads the live window names (or `--names`), computes the no-gap partition
    over W/H, and hands each rect to the available WM tool. Graceful
    degradation: no wmctrl/xdotool on PATH => geometry printed, exit 0.
    """
    tmux_session = args.tmux_session or DEFAULT_TMUX_SESSION
    if args.names:
        names = [n.strip() for n in args.names.split(",") if n.strip()]
    else:
        names = _live_window_names(root, args.window_path, tmux_session)
    if not names:
        print("ERR: no live windows to tile (nothing open in tmux session "
              f"{tmux_session!r}); pass --names or open the seats first",
              file=sys.stderr)
        return 1
    n = len(names)
    tiles = partition_tiles(n, 0, 0, w, h)
    rects = {name: tiles[i] for i, name in enumerate(names)}
    tool = _screen_tool()
    placed, issued = _place_windows(rects, tool)
    if not tool:
        print(f"tile --apply: no wmctrl/xdotool on PATH — X :1 not reached. "
              f"Geometry for {len(rects)} window(s):")
    else:
        print(f"tile --apply: placed {placed}/{len(rects)} window(s) on X :1 "
              f"via {tool} ({issued} command(s) issued)")
    for name, (tx, ty, tw, th) in rects.items():
        print(f"  {name}: x={tx} y={ty} w={tw} h={th}")
    return 0


def _seat_hands(root: Path) -> Path:
    """The seat handoff dir: `<graph>/sessions/seats/` (created on demand).

    The design (hypothesis:l3w4-seat-rotation-loops) files one handoff per
    seat here: `<S>.handoff.md`, carrying `seat`, `generation`, `rotated_at`,
    `predecessor_session`."""
    return _sessions_dir(root) / "seats"


def _read_generation(root: Path, name: str) -> int:
    """The `generation:` read from a seat's existing handoff, or 0 when the
    handoff is absent or unparsable (the rotation that writes gen N always
    follows prior gen N-1)."""
    hp = _seat_hands(root) / f"{name}.handoff.md"
    if not hp.exists():
        return 0
    try:
        txt = hp.read_text(encoding="utf-8", errors="replace")
        for line in txt.splitlines():
            ls = line.strip()
            if ls.startswith("generation:"):
                v = ls.split(":", 1)[1].strip()
                return max(0, int(v))
    except (OSError, ValueError):
        pass
    return 0


def _write_handoff(root: Path, name: str, generation: int,
                   predecessor_session: str = "",
                   session_ref: str = "") -> Path:
    """Write `<S>.handoff.md` with seat/generation/rotated_at/predecessor.

    `session_ref` (the successor's ListAgents `@id` from the JOIN) is carried
    into the handoff HEADER so the successor wakes already knowing its own
    identity, and a reader can see which live session owns this generation
    (L4.112 (D) kid-2 step 5). Returns the written path."""
    hand = _seat_hands(root)
    hand.mkdir(parents=True, exist_ok=True)
    hp = hand / f"{name}.handoff.md"
    hp.write_text(
        f"seat: {name}\n"
        f"generation: {generation}\n"
        f"rotated_at: {datetime.utcnow().isoformat()}Z\n"
        f"predecessor_session: {predecessor_session}\n"
        + (f"session_ref: {session_ref}\n" if session_ref else "")
        ,
        encoding="utf-8",
    )
    return hp


# ---- durable rotation record (hypothesis:l3-rotation-record-and-
#      predecessor-guarantee) -----------------------------------------------

#: Subdir of the graph's sessions dir where every rotation records ITSELF.
ROTATIONS_DIR_NAME = "rotations"


def _rotations_dir(root: Path) -> Path:
    """`<graph>/sessions/rotations/` — the durable rotation-record dir.

    Created on demand. The record survives cleanup and is committed, so a
    rotation whose proof would otherwise exist only as pasted prose keeps a
    replayable artefact behind it.
    """
    return _sessions_dir(root) / ROTATIONS_DIR_NAME


def _observed_windows(tmux_session: str, window_path: str | None = None) -> dict:
    """The window list as an OBSERVED FACT with its source, so a record never
    has to trust the tool's own return value.

    Returns `{"names": [...], "source": ...}` where `source` names the read
    that established it: `tmux list-windows -t <session> -F #{window_name}`
    for a real session, or the window-path file under test (which is a
    stand-in for exactly that read, never the spawn tool's return).
    """
    if window_path:
        names = _existing_windows(tmux_session, window_path)
        source = f"window-path file {window_path}"
    else:
        names = _existing_windows(tmux_session, None)
        source = f"tmux list-windows -t {tmux_session} -F #{{window_name}}"
    return {"names": names, "source": source}


def _write_rotation_record(root: Path, record: dict,
                           path: Path | None = None) -> Path:
    """Write one JSON rotation record under `.agi/sessions/rotations/`.

    One file per rotation, named `<seat>.<UTC timestamp>.json` so a reader can
    glob `<seat>.*.json` and see that seat's whole rotation history. When
    `path` is given (a rotate-self STARTED record opened earlier), the final
    outcome is written to THAT SAME file, updating it in place — so an
    interrupted rotation and its completed outcome never split into two
    records (hypothesis:l4-rotation-record-survives-interruption). Returns
    the written path.
    """
    rot = _rotations_dir(root)
    rot.mkdir(parents=True, exist_ok=True)
    seat = str(record.get("seat") or "anonymous")
    if path is None:
        stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        path = rot / f"{seat}.{stamp}.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return path


def _rotate_self_started_path(root: Path, seat: str) -> Path:
    """The ONE filename a rotate-self rotation records into for its lifetime.

    Computed from the current UTC timestamp the same way
    `_write_rotation_record` names a fresh file, but captured ONCE at the
    start of a rotate-self call so every progress write and the final outcome
    land on the same path. Without this a `started` file and a `success` file
    would carry separate timestamps and a rotation would leave two records.
    """
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    return _rotations_dir(root) / f"{seat}.{stamp}.json"


def _rs_mark(steps: list[str], tmpl_steps: list[str], name: str,
             fallback: str) -> None:
    """Record one completed rotate-self step into the progress list.

    L4.112 (C): the step list is driven by `tmpl_steps` from the rotation
    template, not by a hardcoded list. When `name` is one of the template's
    steps it is recorded verbatim; a housekeeping step the template does not
    name keeps its own `fallback` marker so the record still shows progress
    (kid 2 adds the handover steps to the template, not here).
    """
    steps.append(name if name in tmpl_steps else fallback)


def _write_rotate_self_started(path: Path, *, seat: str, steps: list[str],
                               gen_before: int | None = None,
                               gen_after: int | None = None) -> None:
    """Write/refresh the IN-PROGRESS rotate-self record.

    `result` stays `started` until the rotation reaches an outcome (success or
    refused) and `steps_reached` records which steps have completed, so an
    interrupted rotation leaves a record whose state says exactly where it
    stopped (hypothesis:l4-rotation-record-survives-interruption). Overwrites
    `path` in place; the process keeps writing to the SAME file.
    """
    rec: dict = {
        "rotation": "rotate-self",
        "seat": seat,
        "recorded_at": datetime.utcnow().isoformat() + "Z",
        "result": "started",
        "steps_reached": sorted(steps),
    }
    if gen_before is not None:
        rec["gen_before"] = gen_before
        rec["gen_after"] = gen_after
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")


def _rotate_self_record(*, seat: str, result: str, refusal: str | None = None,
                        gen_before: int | None = None, gen_after: int | None = None,
                        succ=None, pred=None, readback_log=None,
                        cursor_offset: int | None = None,
                        handover: dict | None = None,
                        steps_reached: list[str] | None = None) -> dict:
    """One durable JSON record for a rotate-self rotation: observations (a)-(e)
    of hypothesis:l3-rotation-record-and-predecessor-guarantee, each an
    observed fact with the command output that established it.
    """
    obs: dict = {}
    if succ is not None:
        obs["a_successor_window_under_plain_name"] = {
            "present": seat in succ["names"],
            "window": seat,
            "windows": succ["names"],
            "source": succ["source"],
        }
    if gen_before is not None:
        obs["b_generation"] = {"before": gen_before, "after": gen_after}
    if readback_log is not None:
        obs["c_readback_log_path"] = str(readback_log)
    if cursor_offset is not None:
        obs["d_stale_continue_cursor"] = {
            "start_offset": cursor_offset,
            "read_before_write": True,
            "note": "only bytes AFTER start_offset can confirm the successor; "
                    "a stale pre-spawn `continue` at/before the cursor is refused",
        }
    if pred is not None:
        # `pred` carries name (the renamed aside window) + the observed list.
        obs["e_predecessor_alive"] = {
            "present": pred.get("name") in pred.get("windows", []),
            "name": pred.get("name"),
            "windows": pred.get("windows", []),
            "source": pred.get("source"),
        }
    rec = {
        "rotation": "rotate-self",
        "seat": seat,
        "recorded_at": datetime.utcnow().isoformat() + "Z",
        "result": result,
        "observations": obs,
    }
    if refusal:
        rec["refusal_reason"] = refusal
    if steps_reached is not None:
        rec["steps_reached"] = steps_reached
    if handover is not None:
        rec["handover"] = handover
    return rec


def _loop_record(*, name: str, result: str, refusal: str | None = None,
                 succ=None, readback_log=None,
                 reply_decision: str | None = None) -> dict:
    """One durable JSON record for a cmd_loop rotation: the successor window
    (observed, never tool-return), the read-back log path, and the reply
    decision. `loop` does not rename a predecessor aside, so it has no (e)
    observation of its own; the successor-absent refusal is its guarantee.
    """
    obs: dict = {}
    if succ is not None:
        obs["a_successor_window_under_name"] = {
            "present": name in succ["names"],
            "window": name,
            "windows": succ["names"],
            "source": succ["source"],
        }
    if readback_log is not None:
        obs["c_readback_log_path"] = str(readback_log)
    if reply_decision is not None:
        obs["d_reply_decision"] = reply_decision
    rec = {
        "rotation": "loop",
        "seat": name,
        "recorded_at": datetime.utcnow().isoformat() + "Z",
        "result": result,
        "observations": obs,
    }
    if refusal:
        rec["refusal_reason"] = refusal
    return rec


# ── rotation announcement (hypothesis:l3w4-rotation-announces-itself) ──────
# One announcement per SUCCESSFUL rotation, to every live seat, carrying the
# five fields that have each already cost someone a turn. Delivery rides
# send.py's EXISTING verbs (dm for non-prime seats; the alert room for the
# prime, which is inbox-only and must never post into quorum — the audience
# door is the claim's word for it). This module owns the payload and the
# recipient derivation; the transport verb is the swap point for
# channel:l3w4-shared-mail-alert when it lands. A refused or inconclusive
# rotation writes its record and announces NOTHING.

#: Tags every rotation alert so a reader can tell a machine rotation from the
#: owner speaking (hypothesis:l3w4-shared-mail-alert constraint 3).
ROTATION_ALERT_TAG = "[rotation-alert]"

#: The PRIME's only announce door — a dedicated alert room, NOT quorum. The
#: owner's rule: the prime posts into the audience door, never into quorum.
ROTATION_ALERT_ROOM = "rotation-alerts"


#: Monotonic per-project rotation-alert sequence counter — hypothesis
#: :l3w4-rotation-announces-itself scope extension (2026-09-08). A timestamp
#: is not enough: everyone involved in the 06:25Z stop / 12:14Z resume
#: incident had timestamps and nobody compared them. A seat that must CHECK a
#: counter cannot silently hold a superseded order. The counter lives in the
#: SAME directory as the rotation records (`sessions/rotations/sequence.json`),
#: so it is durable, committed, and "recorded alongside the rotation record".
SEQUENCE_FILE = "sequence.json"


def _seq_file(root: Path) -> Path:
    return _rotations_dir(root) / SEQUENCE_FILE


def _current_sequence(root: Path) -> int:
    """The last-issued rotation-alert sequence number, or 0 when none yet.

    This is the seat-visible read a peer uses to tell "is the order I am
    holding still current?": one cheap read, no round trip. An order stamped
    with a sequence OLDER than this value is superseded.
    """
    p = _seq_file(root)
    if p.is_file():
        try:
            return int(json.loads(p.read_text()).get("sequence", 0))
        except Exception:
            return 0
    return 0


def _next_sequence(root: Path) -> int:
    """Advance the durable per-project rotation-alert counter and return it.

    Called once per SUCCESSFUL rotation, at the same moment the record is
    written. A refused or inconclusive rotation never reaches it.
    """
    nxt = _current_sequence(root) + 1
    rot = _rotations_dir(root)
    rot.mkdir(parents=True, exist_ok=True)
    _seq_file(root).write_text(json.dumps({"sequence": nxt}) + "\n",
                               encoding="utf-8")
    return nxt


def _compose_announcement(*, seat, successor, gen_before, gen_after,
                          trigger, handoff_path, in_flight, seq=0) -> str:
    """The five-field announcement payload — one message, never more.

    Every field is spelled because each has already cost a peer a turn: the
    outgoing seat, the successor name, generation before/after, the trigger
    (meter due / --force / fable-limit), and the handoff path the successor
    is reading, plus one line of what is in flight so a peer can tell whether
    its own round is orphaned.
    """
    return (f"{ROTATION_ALERT_TAG} {seat} -> {successor} | "
            f"generation {gen_before} -> {gen_after} | "
            f"trigger: {trigger} | handoff: {handoff_path} | "
            f"seq: {seq} | in flight: {in_flight}")


def _derive_receivers(root: Path, *, seat: str,
                      live_names: list[str]) -> list[str]:
    """Every live seat to be told of a rotation: config:seats rows
    intersected with live tmux windows, minus the rotating seat itself.

    A seat whose tmux window is absent — never lived or already killed —
    drops out of the set: there is no point announcing to a corpse. Derived,
    never hand-typed, so shelter-master owns the registry and this stays in
    lock-step with it. Returns sorted for determinism.
    """
    live = set(live_names or [])
    out = []
    for row in _load_seats(root):
        name = row.get("name")
        if not name or name == seat:
            continue
        if live and name not in live:
            continue
        out.append(name)
    return sorted(out)


def _announce_rotation(*, root: Path, croot, seat: str, successor: str,
                       gen_before, gen_after, trigger: str, handoff_path: str,
                       in_flight: str, live_names: list[str]) -> list[str]:
    """Emit exactly ONE announcement to every derived live recipient.

    The PRIME is inbox-only (send_dm refuses it), so it posts the same payload
    once to ROTATION_ALERT_ROOM instead — never into quorum. Every non-prime
    seat dms each derived recipient via send.send_dm, which also nudges the
    recipient's tmux window on the existing seat-transport hop. A delivery
    failure is logged and NEVER fails the rotation — the announcement is the
    proof, not a gate. Returns the recipients reached.
    """
    import send  # local: same dir
    seq = _next_sequence(root)
    text = _compose_announcement(
        seat=seat, successor=successor, gen_before=gen_before,
        gen_after=gen_after, trigger=trigger, handoff_path=handoff_path,
        in_flight=in_flight, seq=seq)
    receivers = _derive_receivers(root, seat=seat, live_names=live_names)
    if seat == send.PRIME or seat.startswith(send.PRIME + "-"):
        try:
            path = send.send_room(croot, ROTATION_ALERT_ROOM, text,
                                  sender=seat)
            print(f"announced rotation -> {ROTATION_ALERT_ROOM} ({path})",
                  file=sys.stderr)
            return [ROTATION_ALERT_ROOM]
        except SystemExit as exc:
            print(f"warn: rotation announcement to {ROTATION_ALERT_ROOM!r} "
                  f"failed: {exc}", file=sys.stderr)
            return []
    delivered = []
    for recv in receivers:
        try:
            send.send_dm(croot, seat, recv, text, sender=seat)
            delivered.append(recv)
        except SystemExit as exc:
            print(f"warn: could not dm {recv!r} the rotation: {exc}",
                  file=sys.stderr)
            continue
    print(f"announced rotation -> {len(delivered)} recipient(s) "
          f"{delivered!r}", file=sys.stderr)
    # hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter:
    # `send_dm` nudges each recipient on the seat-transport hop; a recipient
    # whose pane was BUSY at that moment now holds the dm UNREAD but unwoken
    # (the nudge coalesced). Re-run `send.wake` once per delivered recipient
    # right here, NON-fatal and never a gate -- the announcement is the proof.
    # An immediately-woken recipient is already delivered (the per-seat
    # coalesce-window marker stops a second type); one still busy coalesces
    # again and heal.py's watch pass (next poll, <= 30 s) repairs the strand.
    # This call site does NOT sleep 30 s on the rotation path: a daemon delay
    # would die when the short-lived announce process exits, so the prompt
    # re-wake is immediate and heal's poll is the delayed repair.
    for recv in delivered:
        try:
            send.wake(root, recv)
        except Exception as exc:                          # noqa: BLE001
            print(f"warn: post-rotation wake to {recv!r} failed: {exc}",
                  file=sys.stderr)
    return delivered


def cmd_sequence(args: argparse.Namespace, root: Path) -> int:
    """Print the current rotation-alert sequence number.

    The seat-visible read a peer uses to tell whether an order it holds is
    superseded: a value older than this is stale.
    """
    print(_current_sequence(root))
    return 0


def _rename_own_window(seat: str, new_name: str, tmux_session: str,
                       window_path: str | None = None) -> None:
    """Rename the seat's own tmux window `<seat>` aside to `new_name`.

    With `window_path` (tests) the new name is written as the file's new
    window-name list instead of calling tmux."""
    if window_path is not None:
        _replace_window_name(window_path, seat, new_name)
        return
    try:
        subprocess.run(
            ["tmux", "rename-window", "-t", f"{tmux_session}:{seat}",
             new_name],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        # rename is best-effort; the successor spawn is the load-bearing step
        pass


def _replace_window_name(window_path: str, old: str, new: str) -> None:
    """Swap `old` for `new` in a window-name file (test seam)."""
    p = Path(window_path)
    if not p.exists():
        p.write_text(new + "\n", encoding="utf-8")
        return
    lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    out = [new if ln == old else ln for ln in lines]
    p.write_text("\n".join(out) + "\n", encoding="utf-8")


def _kill_window(name: str, tmux_session: str,
                 window_path: str | None = None,
                 window_id: str | None = None) -> None:
    """Kill the (renamed) own window once the successor has confirmed.

    s12: when the window's tmux @id is known (`window_id`, captured in s2 from
    inside the pane) the kill addresses the window BY that @id, never by a
    dotted name — `tmux kill-window -t <s>:foo.gen9` parses the dot as
    window.pane and fails `can't find pane`, and a bare `foo.gen9` can RESOLVE
    to the plain-named successor window (measured L4.114/m2). Address by @id
    when we have it; fall back to the name only when we do not.

    With `window_path` (tests) the name / @id line is dropped from the file
    instead of a real tmux kill-window. Returns a status string: "killed"
    when the kill landed (or, on the test seam, an owned line was dropped),
    "already_gone" when the window is already absent (no owned line to drop,
    or tmux reports `can't find window`), or "error" when tmux threw. Never
    raises (L4.158: a kill failure is recorded, not raised)."""
    if window_path is not None:
        p = Path(window_path)
        if p.exists():
            lines = []
            found = False
            for ln in p.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln:
                    continue
                if window_id and ln.startswith(window_id):
                    found = True
                    continue  # drop the line owned by the reap-by-@id
                if ln == name:
                    found = True
                    continue
                lines.append(ln)
            p.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return "killed" if found else "already_gone"
        return "already_gone"
    target = f"{tmux_session}:{window_id}" if window_id else f"{tmux_session}:{name}"
    try:
        r = subprocess.run(
            ["tmux", "kill-window", "-t", target],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:  # noqa: BLE001
        return "error"
    err = (r.stderr or "").lower()
    if r.returncode != 0 and ("can't find window" in err
                              or "no such window" in err
                              or "can't find session" in err):
        return "already_gone"
    return "killed"


def _seat_fraction(root: Path, row: dict) -> float | None:
    """Context fraction for a seat row: read its seat-stable pin
    (`pin_ref` -> `.agi/sessions/<name>.meter`), parse the named transcript,
    and divide by the ladder's context window. None when the pin or a usage
    record is absent (caller warns and skips the seat)."""
    name = row.get("name")
    if not name:
        return None
    threshold = load_ladder_field(root, "director_rotate_at",
                                  DEFAULT_DIRECTOR_ROTATE_AT)
    # Reuse the same meter pin resolution the `meter` command uses: the
    # seat-stable `.agi/sessions/<name>.meter` wins over newer foreign pins.
    pin = find_pin_log(root, name)
    if pin is None:
        return None
    target = _read_pin_target(pin)
    if target is None:
        return None
    usage = parse_usage_from_cc_transcript(target)
    if usage is None:
        usage = parse_usage_from_rc_log(target)
    if usage is None:
        return None
    context_tokens = load_ladder_field(root, "director_context_tokens",
                                       DEFAULT_DIRECTOR_CONTEXT_TOKENS)
    return calculate_fraction(usage, context_tokens)


def cmd_alarms(args: argparse.Namespace, root: Path) -> int:
    """Meter every seat whose registry row names `--holder` as `rotated_by`.

    For each such seat: at/over `director_rotate_at` (0.47) send exactly ONE
    dm `rotate now` to the holder (never more), nothing else — no spawn, no
    tmux. Below threshold prints `hold <seat> <fraction>`. `--once` meters
    each held seat once and returns so the parent's regression test is
    deterministic; without it the loop meters every `--interval` seconds.
    """
    holder = args.holder
    threshold = load_ladder_field(root, "director_rotate_at",
                                  DEFAULT_DIRECTOR_ROTATE_AT)
    import send  # local: same dir
    croot = Path(args.comms_root) if args.comms_root else send.comms_root(root)
    due = 0
    for row in _load_seats(root):
        if row.get("rotated_by") != holder:
            continue
        seat = row.get("name")
        frac = _seat_fraction(root, row)
        if frac is None:
            print(f"warn: no pin/usage for seat {seat!r} — skipping",
                  file=sys.stderr)
            continue
        if frac < threshold:
            print(f"hold {seat} {frac:.4f}")
            continue
        # at/over threshold: one dm to the holder, plain "rotate now".
        try:
            send.send_dm(croot, holder, seat, "rotate now",
                         sender=holder)
        except SystemExit as exc:
            print(f"warn: could not dm holder {holder!r} for {seat!r}: {exc}",
                  file=sys.stderr)
            continue
        print(f"rotate now -> {seat} (fraction {frac:.4f})")
        due += 1
    if args.once:
        return 0
    while True:
        time.sleep(args.interval)
        return cmd_alarms(args, root)


# --- rotate-self subcommand -----------------------------------------------


# ── L4.112 (D) THE HANDOVER — kid 2 of the round ---------------------------
# The successor lifecycle assembled into ONE rotate-self call, every step
# recorded. Identity is SUPPLIED, never inferred: none of the identity-bearing
# writes happens without the successor's `session_ref` (ListAgents `@id` from
# the JOIN). The seats-row write is admitted by write.py's self_row DATA
# declaration (L4.110), never by a code branch naming `seats`.


def _write_ack(*, root: Path, seat: str, gen_after: int, session_ref: str,
               answer: str = "continue", text: str = "") -> Path:
    """Write the successor's ACK file on ITS behalf (kid-2 step 6).

    The successor makes ZERO tool calls on wake: the predecessor writes
    `continue` into the same ack channel `cmd_ack` used, so the read-back
    confirms the rotation the moment it polls. cmd_ack stays CALLABLE as a
    one-generation fallback (hypothesis:l4-rotate-readback-
    false-negative-and-the-orphan-by-design) but is no longer the successor's
    first act."""
    ack = {
        "seat": seat,
        "gen_after": gen_after,
        "session_ref": session_ref,
        "answer": answer,
        "text": text,
        "ts": datetime.utcnow().isoformat() + "Z",
    }
    path = _ack_path(root, seat)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ack, indent=2) + "\n", encoding="utf-8")
    return path


def _successor_row_write(root: Path, *, actor: str, seat: str, role: str,
                         session_ref: str, generation: int,
                         window: str, pid: int | None = None,
                         session_id: str | None = None) -> str:
    """Write the successor's config:seats ROW via `write.py submit` (s6).

    Sets the seat's own row's `session_ref`/`session_id`/`generation`/`window`/
    `pid`. L4.114 (s6): the source of the identity is the registry JOIN —
    `source: registry` is recorded in the handover (the row itself carries no
    `source` field; the L4.110/r3 self_row declaration admits exactly
    [session_ref, session_id, generation, window, pid]).

    The successor reuses the PLAIN seat name, so its row IS the seat's own
    row — the exact write the self_row declaration admits for a seated actor
    (only its own row, only the declared fields; every other row and every
    prime-only field byte-identical). Admission lives in write.py's
    `_enforce_written_by` reading the schema's `self_row` data; nothing here
    names `seats` in a branch. Returns a one-line outcome string."""
    import write  # local: same dir (send.py pattern, no import cycle)
    rows = write._load_seats(root)
    new_rows: list[dict] = []
    found = False
    for r in rows:
        if r.get("name") == seat:
            nr = dict(r)
            nr["session_ref"] = session_ref
            if session_id is not None:
                nr["session_id"] = session_id
            nr["generation"] = generation
            nr["window"] = window
            if pid is not None:
                nr["pid"] = pid
            new_rows.append(nr)
            found = True
        else:
            new_rows.append(r)
    if not found:
        return (f"skipped: no seat-registry row with name {seat!r} "
                "(a THROWAWAY seat never writes seats.md)")
    edit = write.Edit(node_id="config:seats")
    edit.set_fm["seats"] = new_rows
    write.submit(root, edit, actor=actor, role=role)
    return (f"config:seats row {seat!r}: session_ref={session_ref} "
            f"session_id={session_id} pid={pid} generation={generation} "
            f"window={window!r} source=registry")


def _backfill_session_ref(root: Path, *, seat: str, role: str,
                          ref: str) -> str:
    """r3 — `rotate.py ack --ref <ref>` BACK-FILLS `session_ref` into the
    successor's OWN seats row through the self_row write (source: ack).

    The `session_ref` (the successor's session/uuid prefix, proven by whois)
    travels in the row so a later whois can authorize by it. Returns a
    one-line outcome; the write is admitted by the self_row declaration."""
    import write  # local: same dir
    rows = write._load_seats(root)
    new_rows = []
    found = False
    for r in rows:
        if r.get("name") == seat:
            nr = dict(r)
            nr["session_ref"] = ref
            new_rows.append(nr)
            found = True
        else:
            new_rows.append(r)
    if not found:
        return (f"skipped: no seat-registry row with name {seat!r} "
                "(a THROWAWAY seat has no row to back-fill)")
    edit = write.Edit(node_id="config:seats")
    edit.set_fm["seats"] = new_rows
    write.submit(root, edit, actor=seat, role=role)
    return f"back-filled session_ref={ref} into own row (source: ack)"


def _pin_successor_meter(root: Path, *, seat: str, generation: int,
                         transcript: str) -> str:
    """Pin the successor's meter at ITS transcript (kid-2 step 4).

    Writes `<graph>/sessions/<seat>.meter` = `<gen>\t<transcript>` — the same
    seat-stable pin `rotate.py meter --seat` reads. `transcript` is the
    successor's OWN transcript from the JOIN, NEVER the newest `.jsonl` in the
    sessions dir. Returns the written pin path."""
    sessions = _sessions_dir(root)
    sessions.mkdir(parents=True, exist_ok=True)
    pinp = sessions / f"{seat}{METER_PIN_EXT}"
    pinp.write_text(f"{generation}\t{transcript}\n", encoding="utf-8")
    return str(pinp)


def _pid_alive(pid: int) -> bool:
    """True when a live process owns `pid` (os.kill probe, no signal sent)."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except (PermissionError, OSError):
        return True
    return True


def _short_ps(pid: int) -> str:
    """`ps -o pid=,cmd= -p <pid>` output, or '' when absent/failed."""
    try:
        out = subprocess.run(
            ["ps", "-o", "pid=,cmd=", "-p", str(pid)],
            capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""
    return out


def _record_s12_self_reap(record_path: Path | None, reap: dict) -> None:
    """Append the s12 self-reap evidence into the already-written rotation
    record (L4.118/R2: every step writes its own evidence). The record is
    written durably BEFORE the window kill so it survives it; this adds the
    LAST-ACT reap observation into that same file. Best-effort — never raises
    (the reap itself, not the bookkeeping, is load-bearing).
    """
    if not record_path:
        return
    p = Path(record_path)
    if not p.exists():
        return
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return
    doc["s12_self_reap"] = reap
    try:
        p.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass


def _pane_pid(tmux_pane: str) -> int | None:
    """The pane's own controlling process id, from `tmux display-message`.

    `$TMUX_PANE` is a `%<N>` token (the pane id) inside a tmux pane; the
    pane's controlling process id comes from
    `tmux display-message -p -t '<pane>' '#{pane_pid}'`. Returns None on any
    failure (empty token, no tmux session under test where the conftest guard
    answers rc-1, or a non-numeric read) — the caller records SKIPPED naming
    TMUX_PANE. L4.118/R2 uses this to derive the predecessor's OWN chain.
    """
    if not tmux_pane:
        return None
    try:
        out = subprocess.run(
            ["tmux", "display-message", "-p", "-t", tmux_pane,
             "#{pane_pid}"],
            capture_output=True, text=True, timeout=5).stdout.strip()
        return int(out) if out.isdigit() else None
    except Exception:  # noqa: BLE001
        return None


def _read_ps_parent_table() -> dict[int, int]:
    """The whole-system parent table `{pid: ppid}` from `ps -e -o pid=,ppid=`.

    **L4.122 criterion 1 (merge-up 23): `ps -e` enumerates ALL processes**,
    never the default same-tty selection. When rotate.py runs under the Bash
    tool it has NO controlling terminal, so the bare default `ps -o pid=,ppid=`
    selects only other no-tty processes and the pane's live chain (on pts/18)
    is invisible. `ps -e` sees every pid regardless of tty, so both the own
    chain climb and the Belam FIFO reap's descendant walk see the whole tree.
    Never raises on a failed read (returns {})."""
    parent_of: dict[int, int] = {}
    try:
        out = subprocess.run(["ps", "-e", "-o", "pid=,ppid="],
                             capture_output=True, text=True,
                             timeout=10).stdout
    except Exception:  # noqa: BLE001
        return {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            try:
                pid, ppid = int(parts[0]), int(parts[1])
            except ValueError:
                continue
            parent_of[pid] = ppid
    return parent_of


def _descendant_chain(pane_pid: int) -> list[int]:
    """ALL pids below `pane_pid` in the whole-system `ps -e` parent table.

    BFS from `pane_pid`, shallow->deep; used by the Belam FIFO reap (r5) to
    derive the OLDEST predecessor's claude chain (its pane bash -> wrapper ->
    claude) from the window's pane pid. Returns [] on an empty/unreachable
    table — the caller records SKIPPED naming the missing chain."""
    parent_of = _read_ps_parent_table()
    children: dict[int, list[int]] = {}
    for pid, ppid in parent_of.items():
        children.setdefault(ppid, []).append(pid)
    chain: list[int] = []
    stack = [pane_pid]
    while stack:
        cur = stack.pop(0)
        for child in children.get(cur, []):
            chain.append(child)
            stack.append(child)  # BFS -> shallow..deep
    return chain


def _derive_own_chain(pane_pid: int,
                      own_pid: int | None = None) -> list[int]:
    """The predecessor's OWN process chain, derived live, EXCLUDING the
    rotate-self pid and its direct shell parent from the TERM list.

    From `pane_pid` (the pane's controlling pid), climb the `ps -e` parent
    table from the OWN pid (rotate.py) up to the pane pid, then drop the own
    pid and its direct parent — the chain to TERM is everything between the
    pane and the shell that runs rotate.py, i.e. the measured [pane bash,
    claude wrapper, claude] (L4.114: pane 1943505 -> wrapper 1943515 ->
    claude 1943519).

    **L4.122 criterion 1 (merge-up 23): `ps -e` enumerates ALL processes**,
    never the default same-tty selection. When rotate.py runs under the
    Bash tool it has NO controlling terminal, so the bare default `ps -o
    pid=,ppid=` selects only other no-tty processes — the pane's live chain
    (on pts/18) is invisible and the climb returned [] on the real gen IX->X
    rotation even though the pane was right there. `ps -e` sees every pid
    regardless of tty, so the climb from a Bash-tool shell in the pane
    returns the three-pid chain [pane bash, wrapper, claude], not []. The
    own pid may only appear BELOW the pane pid (rotate.py runs inside that
    pane); if the climb cannot connect to it, return [] and the caller
    records SKIPPED naming the missing connection rather than guessing.
    """
    own = own_pid if own_pid is not None else os.getpid()
    parent_of = _read_ps_parent_table()
    chain = [own]
    cur = parent_of.get(own)
    while cur is not None and cur != pane_pid:
        chain.append(cur)
        cur = parent_of.get(cur)
    if cur is None:
        return []  # own pid is not under this pane pid — refuse to guess
    chain.append(pane_pid)
    chain.reverse()  # shallow->deep: [pane, ..., own]
    parent = chain[-2] if len(chain) >= 2 else None
    excl = {own, parent}
    return [p for p in chain if p not in excl]


def _shield_final_signals() -> list:
    """Ignore the signals a dying process tree fires at a self-reap's tail.

    TERM-ing the pane bash / wrapper / claude chain sends SIGHUP / SIGTERM /
    SIGPIPE to whatever is still in that session (rotate.py's own shell among
    them). rotate.py must survive long enough to print the verification and
    reach the final window kill, which is the true last act after the record
    is written and pushed (L4.118/R2).

    Returns the previous handler list so the caller RESTORES them afterward
    (the pytest process shares this runtime — a persistent SIG_IGN would leak
    into every later reap test).
    """
    old: list = []
    for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGPIPE):
        try:
            old.append((sig, signal.getsignal(sig)))
            signal.signal(sig, signal.SIG_IGN)
        except (ValueError, OSError, AttributeError):
            pass
    return old


def _restore_shield_signals(old: list) -> None:
    """Restore the handlers `_shield_final_signals` replaced (test hygiene:
    the pytest runtime is shared; a persistent ignore would break reap tests)."""
    for sig, handler in old:
        try:
            signal.signal(sig, handler)
        except (ValueError, OSError):
            pass


def _button_down_legal_hint(root: Path) -> str:
    """Read-only one-liner for the dry-run: which branch a grid commit would
    run on. NEVER commits/pushes (dry-run touches nothing); only reads the
    checked-out branch via `git rev-parse`, and reports no-repo otherwise."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and (out.stdout or "").strip():
            return f"legal on {out.stdout.strip()!r}"
    except Exception:  # noqa: BLE001
        pass
    return "no repo / unknown branch (grid commit would be SKIPPED)"


def _reap_pid(pid: int) -> dict:
    """Reap the predecessor's own process by PID, verified gone with ps.

    NEVER a mere tmux window kill (killing a window does not kill the agent,
    measured L3.42) and NEVER the caller's real process without an explicit
    stand-in: a pid <= 0, or == os.getpid(), is refused with `reaped: False`.
    Against a real stand-in (a test's own spawned `sleep`), TERM the pid and
    verify with `ps` that it is gone. Returns the observation dict."""
    pid = int(pid)
    if pid <= 0 or pid == os.getpid():
        return {"pid": pid, "existed_before": None, "reaped": False,
                "gone_after": None,
                "note": "refused: not a pid this caller may reap (never the "
                         "real own pid without an explicit stand-in; the CLI "
                         "flag was removed L4.114, tests inject the seam)"}
    was = _pid_alive(pid)
    ps_before = _short_ps(pid)
    reaped = False
    if was:
        try:
            os.kill(pid, 15)  # SIGTERM
        except OSError:
            pass
        # A TERM'd process lingers as a zombie (`[sleep] <defunct>`) that an
        # `os.kill(pid, 0)` probe still sees until its parent reaps it. When
        # the pid IS our child, WAITPID it away; a non-child TERM falls back
        # to the direct table probe below.
        try:
            for _ in range(100):
                try:
                    wpid, _ = os.waitpid(pid, os.WNOHANG)
                except ChildProcessError:
                    break  # not our child to reap
                if wpid == pid:
                    reaped = True
                    break
                time.sleep(0.02)
        except Exception:  # noqa: BLE001
            reaped = False
        if not reaped:
            reaped = not _pid_alive(pid)
    gone = reaped or not _pid_alive(pid)
    ps_after = _short_ps(pid)
    return {"pid": pid, "existed_before": was, "reaped": reaped,
            "gone_after": gone, "ps_before": ps_before, "ps_after": ps_after}


def _reap_chain(pids: list[int], *, wait_secs: float = 5.0,
                kill_survivors: bool = True) -> dict:
    """s12 — TERM a predecessor process chain DEEPEST-FIRST, verify each gone.

    `pids` is the chain ordered SHALLOW->DEEP ([pane bash, claude wrapper,
    claude]) as measured at L4.114 (pane 1943505 -> wrapper 1943515 -> claude
    1943519). TERM the deepest first (reversed) so removing the pane's bash
    never orphans a live claude. Each pid's observation records was_alive,
    termd, gone_after and the `ps -p` reads around it.

    Each pid gets up to `wait_secs` to die after TERM; a survivor is SIGKILL'd
    when `kill_survivors` (L4.118/R2: "wait up to 5 s per pid, KILL what
    survives").

    Refuses the caller's OWN pid and any pid <= 0 (like `_reap_pid`):
    rotate.py never TERMs itself. The OWN chain it MAY TERM is derived live by
    `_derive_own_chain` (which already excludes the own pid and its direct
    shell parent); this guard is the second, independent fence.
    """
    chain: list[dict] = []
    for pid in reversed(pids):
        pid = int(pid)
        if pid <= 0 or pid == os.getpid():
            chain.append({
                "pid": pid, "was_alive": None, "termd": False,
                "gone_after": False,
                "note": "refused: never the real own pid; rotate-self's "
                         "own chain is derived by _derive_own_chain, which "
                         "excludes this pid"})
            continue
        was = _pid_alive(pid)
        ps_before = _short_ps(pid)
        termd = False
        if was:
            try:
                os.kill(pid, signal.SIGTERM)
            except OSError:
                pass
            deadline = time.time() + wait_secs
            while time.time() < deadline and _pid_alive(pid):
                # L4.122 criterion 2 (merge-up 23): bind `wpid` BEFORE the
                # `if`. A pid that is NOT our child (an ancestor pane bash /
                # wrapper / claude that survives SIGTERM) makes `waitpid`
                # raise ChildProcessError on the FIRST iteration; with `wpid`
                # unbound, `if wpid == pid` raised UnboundLocalError at
                # rotate.py:3040 and the whole self-reap died before the
                # SIGKILL. Bind None first; the ChildProcessError branch keeps
                # polling the table until the deadline, then SIGKILLs.
                wpid = None
                try:
                    wpid, _ = os.waitpid(pid, os.WNOHANG)
                except ChildProcessError:
                    pass  # not our child to reap; keep polling the table
                except Exception:  # noqa: BLE001
                    break
                if wpid == pid:
                    termd = True
                    break
                time.sleep(0.05)
            if not termd:
                termd = not _pid_alive(pid)
            if not termd and kill_survivors:
                try:
                    os.kill(pid, signal.SIGKILL)
                except OSError:
                    pass
                termd = not _pid_alive(pid)
                # L4.122: SIGKILL lands, but a REPARENTED process (init / a
                # subreaper) may take a beat to collect the zombie — the
                # `os.kill(pid,0)` probe still sees the corpse at that instant,
                # so gone_after was falsely False right after the kill. Poll
                # briefly so the recorded gone_after reflects the eventual
                # state, not the reaping race.
                if not termd:
                    deadline_t = time.time() + 1.0
                    while time.time() < deadline_t and _pid_alive(pid):
                        time.sleep(0.05)
                    termd = not _pid_alive(pid)
        gone = termd or not _pid_alive(pid)
        chain.append({"pid": pid, "was_alive": was, "termd": termd,
                      "gone_after": gone, "ps_before": ps_before,
                      "ps_after": _short_ps(pid)})
    return {"order": "deepest-first", "chain": chain}


def _belam_oldest(live: list[str], successor: str, prefix: str) -> str | None:
    """The OLDEST live Belam window to reap under the five-deep cap.

    On a prime_director rotation the predecessor chain stays exactly five
    deep: when the live Belam windows PLUS the just-joined `successor` would
    make a SIXTH, the cap names the OLDEST (lowest Roman line value) to reap.
    Returns that window name, or None when the chain stays at/below five."""
    live_belam = [w for w in live if w == prefix or w.startswith(prefix + "-")]
    candidate = set(live_belam) | {successor}
    if len(candidate) <= 5:
        return None
    if not live_belam:
        return None
    # oldest = lowest line value; a bare base (no Roman) is line 1
    by_line = sorted(live_belam,
                     key=lambda w: _split_roman_suffix(w)[1])
    return by_line[0]


def _reap_belam_oldest(*, tmux_session: str, oldest: str,
                       window_path: str | None = None,
                       pids: list[int] | None = None,
                       s12_reap: dict | None = None,
                       record_path: Path | None = None) -> dict:
    """r5 — reap the OLDEST Belam predecessor by PID when the chain would
    exceed FIVE (FIFO per the owner: 'rotation reaps from the wrong end, filo
    not fifo').

    The predecessor's window pane pid (`tmux display-message -p -t @id
    '#{pane_pid}'`, resolved from the oldest window's tmux @id) PLUS the
    claude child, derived with the same `ps -e` climb (`_descendant_chain`),
    are TERM'd DEEPEST-FIRST (`_reap_chain`), waited, KILL-ed survivors, then
    ITS window is killed BY @id (`_kill_window`). The record carries
    {oldest, window_id, pids, reaped, ps_after}.

    L4.150: the belam-cap record entry is written PLANNED-FIRST —
    `{planned: True, oldest, window_id, pids, chain}` lands in
    `s12_self_reap.belam_reap` BEFORE the first TERM, then updated
    best-effort with `reaped`/`ps_after`/`order` after — the same (e) shape
    `_record_s12_self_reap` uses for the own chain, so an interrupted cap
    reap (rotate.py dying between a TERM and the post-reap write) keeps its
    planned evidence. `s12_reap` + `record_path` are the evidence sink;
    best-effort, never raises.

    ALL of it lives behind THIS ONE function so hypothesis:l4-the-pin-is-the-
    lease can swap in the belam.pred-1..5 pin rule later (do not build the
    lease here). `pids` is the test seam (stand-in pids); production derives
    the chain from the oldest window's pane pid. Never raises; a chain it
    cannot derive records SKIPPED naming the missing input."""
    oldest_id = _successor_window_id(oldest, tmux_session, window_path)

    def _kill_oldest_by_id() -> dict:
        """L4.158 — on a SKIPPED path, still kill the oldest window BY @id
        so the FIFO cap never leaves six windows. When no @id was resolved
        record `window_killed: false` and do NOT call tmux. A window that is
        already gone records it (never an error); a kill failure never
        raises."""
        if not oldest_id:
            return {"window_killed": False, "already_gone": False}
        try:
            status = _kill_window(oldest, tmux_session, window_path,
                                  window_id=oldest_id)
        except Exception:  # noqa: BLE001
            status = "error"
        return {"window_killed": status == "killed",
                "already_gone": status == "already_gone"}

    _write_belam_planned = (lambda e: (
        s12_reap.__setitem__("belam_reap", e)
        if s12_reap is not None else None,
        _record_s12_self_reap(record_path, s12_reap)
        if s12_reap is not None else None))
    if not pids:
        pane_pid = _pane_pid(oldest_id) if oldest_id else None
        if not pane_pid:
            kill = _kill_oldest_by_id()
            e = {"oldest": oldest, "window_id": oldest_id, "pids": [],
                 "reaped": False, "ps_after": [],
                 "window_killed": kill["window_killed"],
                 "skipped": (("already gone: the oldest window "
                               f"{oldest!r} (@id {oldest_id}); no pane pid; "
                               "window already gone")
                              if kill["already_gone"]
                              else ("SKIPPED: no pane pid for the oldest "
                                    f"window {oldest!r} (@id {oldest_id}); "
                                    "the Belam FIFO cap could not derive "
                                    "its chain"))}
            _write_belam_planned(e)
            return e
        pids = _descendant_chain(pane_pid)
        if not pids:
            kill = _kill_oldest_by_id()
            e = {"oldest": oldest, "window_id": oldest_id, "pids": [],
                 "reaped": False, "ps_after": [], "pane_pid": pane_pid,
                 "window_killed": kill["window_killed"],
                 "skipped": (("already gone: the oldest window "
                               f"{oldest!r} (@id {oldest_id}); no chain "
                               "under the pane pid; window already gone")
                              if kill["already_gone"]
                              else ("SKIPPED: no chain under pane pid "
                                    f"{pane_pid} for the oldest window "
                                    f"{oldest!r}; nothing to reap"))}
            _write_belam_planned(e)
            return e
    # (e) the PLANNED belam-cap entry — written BEFORE the first TERM, so an
    #     interrupted reap keeps its planned evidence.
    _write_belam_planned({"planned": True, "oldest": oldest,
                          "window_id": oldest_id, "pids": pids,
                          "chain": pids})
    observed = _reap_chain(pids)
    reaped = bool(observed["chain"]) and all(
        (not p["was_alive"]) or p["gone_after"]
        for p in observed["chain"])
    # kill the OLDEST's window BY @id (never a dotted/plain name — L4.114/m2:
    # `belam-S1-L4-I.genN` parses the dot as window.pane and a bare name can
    # resolve to the SUCCESSOR).
    _kill_window(oldest, tmux_session, window_path, window_id=oldest_id)
    entry = {"oldest": oldest, "window_id": oldest_id, "pids": pids,
             "reaped": reaped, "order": observed["order"],
             "ps_after": [_short_ps(p) for p in pids],
             "chain": observed["chain"]}
    # best-effort update of the planned belam-cap entry with the observations
    # after (never raises — the reap, not the bookkeeping, is load-bearing).
    if s12_reap is not None:
        s12_reap["belam_reap"] = entry
        _record_s12_self_reap(record_path, s12_reap)
    return entry


# ---- L4.114 THE JOIN: successor identity from the per-session registry ----
# The predecessor no longer receives the successor's identity as a CLI flag:
# it JOINS the successor by the WINDOW @id it observed tmux assign (s3), never
# by the session prefix, reading `~/.claude/sessions/<pid>.json` for the
# process that owns that window. The @id is the load-bearing key: the
# registry file's session_id/prefix may be anything, but its window identity
# must carry the same @<N> token (proof a). `--registry-dir` is the test
# seam; production defaults to `~/.claude/sessions`.

REGISTRY_DEFAULT_DIR = "~/.claude/sessions"
REGISTRY_JOIN_POLL_S = 2      #: poll interval, seconds
REGISTRY_JOIN_TIMEOUT_S = 60  #: bounded join poll


def _successor_window_id(seat: str, tmux_session: str,
                         window_path: str | None = None) -> str | None:
    """The successor window's tmux @id (the `@<N>` token), or None.

    With `window_path` (test seam, s3) the @id comes from a window-path line
    of the form `@<N> <name>`; a plain `<name>` line yields None, so existing
    plain-name fixtures never trip the JOIN. Real tmux parses
    `list-windows -F '#{window_id} #{window_name}'` and name-matches. The @id
    (never the session prefix) is what the registry JOIN keys on."""
    if window_path is not None:
        p = Path(window_path)
        if p.exists():
            for ln in p.read_text(encoding="utf-8").splitlines():
                ln = ln.strip()
                if not ln.startswith("@"):
                    continue
                ident, _, name = ln.partition(" ")
                if name.strip() == seat:
                    return ident.strip()
        return None
    try:
        out = subprocess.run(
            ["tmux", "list-windows", "-t", tmux_session,
             "-F", "#{window_id} #{window_name}"],
            capture_output=True, text=True, timeout=5).stdout
        for ln in out.splitlines():
            ident, _, name = ln.partition(" ")
            if name.strip() == seat:
                return ident.strip()
    except Exception:  # noqa: BLE001
        pass
    return None


def _join_successor(*, root: Path, seat: str, window_id: str | None,
                    registry_dir: str | None = None,
                    poll_secs: int | None = None) -> dict:
    """JOIN the successor from the per-session registry by WINDOW @id (s4).

    Polls `registry_dir` (`~/.claude/sessions` by default) for `<pid>.json`
    files, matching each file's CONTENT by the window @id token — never by
    filename or session prefix. Bounded to `poll_secs` (default 60). Returns
    a dict. On a match: {found: True, window_id, pid, session_id, transcript,
    name, path, note}. On timeout/absence: {found: False, window_id, note}
    where the note NAMES `registry file for @<id>` (proof a)."""
    if not window_id:
        return {"found": False, "window_id": window_id,
                "note": "no successor window @id captured (window_id empty)"}
    reg = Path(registry_dir or REGISTRY_DEFAULT_DIR).expanduser()
    deadline = time.time() + (poll_secs if poll_secs is not None
                              else REGISTRY_JOIN_TIMEOUT_S)
    token = window_id
    while time.time() < deadline:
        if reg.is_dir():
            for fp in sorted(reg.glob("*.json")):
                try:
                    raw = fp.read_text(encoding="utf-8", errors="replace")
                except OSError:
                    continue
                if token not in raw:
                    continue
                try:
                    data = json.loads(raw)
                except ValueError:
                    data = {}
                if not isinstance(data, dict):
                    data = {}
                try:
                    pid = int(fp.stem)
                except ValueError:
                    pid = None
                sess = (data.get("session_id") or data.get("sessionId") or "")
                transc = (data.get("transcript") or data.get("transcript_path")
                          or "")
                if not transc and sess and data.get("cwd"):
                    # L4.122: the registry carries cwd + sessionId, never a
                    # transcript path — the live gen IX->X join returned
                    # `transcript: ""` and meter_pin / model_confirm were
                    # SKIPPED. Derive the Claude Code transcript the way gen X
                    # pinned it by hand: `~/.claude/projects/<cwd with every
                    # '/' and '.' replaced by '-'>/<sessionId>.jsonl` (measured
                    # cwd .../worktree/seat-sanctuary-director ->
                    # -home-ubuntu-work-agi--agi-worktrees-...).
                    slug = str(data["cwd"]).replace("/", "-").replace(".", "-")
                    transc = str(CC_PROJECTS_DIR / slug / f"{sess}.jsonl")
                nm = data.get("name") or data.get("agent") or seat
                return {"found": True, "window_id": window_id, "pid": pid,
                        "session_id": str(sess), "transcript": str(transc),
                        "name": str(nm), "path": str(fp),
                        "note": f"joined by @{token.lstrip('@')} in "
                                f"registry file {fp.name}"}
        time.sleep(REGISTRY_JOIN_POLL_S)
    return {"found": False, "window_id": window_id,
            "note": f"registry file for @{window_id.lstrip('@')} not found "
                     f"in {reg} within the bounded join poll"}


def _confirm_successor_model(*, seat: str, expected_model: str | None,
                             expected_effort: str | None,
                             pid: int | None,
                             transcript: str | None) -> dict | str:
    """Confirm the successor's live model/effort against the seat row (s5).

    REQUESTED = the argv token after the FIRST `--model` in
    `ps -o args= -p <pid>`; LIVE = the first `"model":"..."` in the
    successor transcript. Records {expected, requested, live, verdict};
    returns a string naming the missing input when there is no assistant turn
    (no transcript, or no model line in it)."""
    expected = {"model": expected_model, "effort": expected_effort}
    requested: dict = {}
    if pid:
        argv = _short_ps(pid)
        toks = argv.split()
        if "--model" in toks:
            i = toks.index("--model")
            if i + 1 < len(toks):
                requested["model"] = toks[i + 1]
    live: dict = {}
    if transcript:
        p = Path(str(transcript)).expanduser()
        if p.exists():
            for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
                m = re.search(r'"model"\s*:\s*"([^"]+)"', ln)
                if m:
                    live["model"] = m.group(1)
                    break
    if not live:
        return ("skipped: no assistant turn in the successor transcript — "
                "cannot confirm model/effort")
    verdict = ("ok" if (requested.get("model") == expected.get("model")
                         and live.get("model") == expected.get("model"))
               else "mismatch")
    return {"expected": expected, "requested": requested, "live": live,
            "verdict": verdict}


def _button_down(*, root: Path, branch_allow: bool = True,
                 legal_branch: str | None = None) -> str:
    """s8 — commit the record+row and grid-commit, ONLY where legal.

    `git rev-parse --abbrev-ref HEAD` establishes whether `root` is a real
    repo; `legal_branch` (when supplied) is the ONE branch a grid commit is
    legal on — the season branch (`season/s2` under this round's season). A
    grid commit is legal ONLY when a real branch is checked out AND the gate
    is on AND (when a legal branch is declared) the branch IS it; any other
    state RECORDS `SKIPPED: grid commit illegal on <branch>` naming the real
    branch and runs no commit/push. On a fixture root there is no repo, so
    this records the skip — the test proves the SKIPPED wording (s8 live
    path) and no real commit ever happens from a test. Returns a one-line
    outcome for the rotation record."""
    branch = None
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5)
        if out.returncode == 0:
            branch = (out.stdout or "").strip() or None
    except Exception:  # noqa: BLE001
        branch = None
    legal = branch is not None and branch_allow
    if legal and legal_branch is not None:
        legal = (branch == legal_branch)
    if not legal:
        reason = f"SKIPPED: grid commit illegal on {branch or '<no-repo>'}"
        if legal_branch and branch:
            reason += f" (branch != {legal_branch})"
        elif not branch_allow:
            reason += " (season gate off)"
        return reason + "; record left for the loop"
    try:
        subprocess.run([sys.executable,
                        str(Path(__file__).with_name("grid.py")),
                        "commit", "--all"],
                       cwd=str(root), capture_output=True, text=True,
                       timeout=60)
        return f"grid committed — record+row on branch {branch}"
    except Exception as exc:  # noqa: BLE001
        return f"FAILED: {exc}"


# -- s11: the cheapest verification level rotate-self cites (<15s) -------
VERIFICATION_LEVEL = "quick"  # links + goals-check + write-guard (verification.py:14)
BOOTSTRAP_SHAPE = "v1"        # shape id of <sessions>/seats/<seat>.bootstrap.json


def _run_verification(root: Path, argv: list[str] | None = None) -> dict:
    """s11 — run verification.py at the cheapest existing level and return it.

    Level `quick` (`--json`) is the cheapest existing level
    (links + goals-check + write-guard, <15s — verification.py:14) and is the
    one this round actually cites; it never runs pytest (the suite window is
    the prime's, verification.py is read/ran, never edited). `argv` is the
    test seam (a fixture root has no graph to verify). NEVER raises: any
    failure is recorded as {skipped: ...} for the bootstrap record.
    """
    if argv is None:
        argv = [sys.executable,
                str(Path(__file__).with_name("verification.py")),
                "--json", "--level", VERIFICATION_LEVEL, "--root", str(root)]
    try:
        out = subprocess.run(argv, capture_output=True, text=True, timeout=120)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "level": VERIFICATION_LEVEL,
                "skipped": f"verification could not run: {exc}"}
    if out.returncode != 0:
        return {"ok": False, "level": VERIFICATION_LEVEL,
                "skipped": f"verification exit {out.returncode}",
                "tail": (out.stdout or "").strip().splitlines()[-1:]}
    try:
        data = json.loads(out.stdout or "{}")
    except Exception:  # noqa: BLE001
        return {"ok": False, "level": VERIFICATION_LEVEL,
                "skipped": "verification --json output not parseable"}
    data["ok"] = True
    data["level"] = VERIFICATION_LEVEL
    return data


def _git_head(root: Path, *, argv: list[str] | None = None) -> str | None:
    """Read-only: the short HEAD commit of `root`, or None when it is not a
    git repo. `git rev-parse --short HEAD` is a pure read — the ONE git
    command the bootstrap record is allowed, because it only stamps a fact's
    age and never mutates (it is `SKIPPED` when there is no repo, never
    guessed). `argv` is the test seam (a fixture root has no repo)."""
    try:
        out = subprocess.run(
            argv or ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and (out.stdout or "").strip():
            return out.stdout.strip()
    except Exception:  # noqa: BLE001
        pass
    return None


def _derive_bootstrap_fact(key: str, *, root: Path, seat: str,
                           seat_row: dict | None, commit: str | None):
    """Resolve ONE bootstrap fact to a real value the handover can see, else
    None with a NAMED skip reason. NEVER the old blanket `0b owns deriving`:
    every skip names the connection that is missing (the seat row field, the
    join, the sibling round that owns it), so a cold reader knows who to ask.
    `root` is the repo, `seat` the successor's name, `seat_row` its
    config:seats row (or {} when no row exists), `commit` the HEAD stamp (or
    None when there is no repo). Returns (value, reason)."""
    row = seat_row or {}
    if key == "commit":
        return commit, ("no git repo to stamp at" if commit is None else None)
    if key == "seat_row":
        if row:
            return (f"HEAD@{commit}: {json.dumps(row, sort_keys=True)}" if commit
                    else json.dumps(row, sort_keys=True)), None
        return None, f"no seat row for {seat} in config:seats"
    if key == "seed":
        return ((str(row["seed"]) if row.get("seed") is not None else None),
                ("seat row carries no seed" if row.get("seed") is None else None))
    if key == "model":
        return ((str(row["model"]) if row.get("model") else None),
                ("seat row carries no model at HEAD"
                 if not row.get("model") else None))
    if key in ("effort", "window", "worktree"):
        return ((str(row[key]) if row.get(key) else None),
                (f"seat row carries no {key}" if not row.get(key) else None))
    if key in ("ack", "prev_gen"):
        return ((str(row[key]) if row.get(key) is not None else None),
                (f"seat row carries no {key} at HEAD"
                 if row.get(key) is None else None))
    # -- join-only: only the @id join (after_join round) can supply these ----
    if key == "successor_live_model":
        return None, "successor live model is known only after the @id join (after_join)"
    if key == "successor_address":
        return None, "successor address is the @id join result (after_join)"
    if key == "model_refusal_fallback":
        return None, "last model_refusal_fallback is read from the successor transcript after join"
    # -- sibling rounds own these derivations; named, never a blank ----------
    if key == "mail":
        return None, "mail is `send.py read` unread dms, a sibling round's derivation"
    if key == "account":
        return None, "account is the credits endpoint, a sibling round's derivation"
    if key == "floor":
        return None, "floor numbers, a sibling round's derivation"
    if key == "registry":
        return None, "workflow registry state, a sibling round's derivation"
    if key == "crons":
        return None, "crons state, a sibling round's derivation"
    return None, f"no handover derivation for {key}"


BOOTSTRAP_FIXED_FACTS = [
    "commit", "seat_row", "successor_live_model", "successor_address",
    "model_refusal_fallback", "mail", "account", "floor", "registry",
    "crons",
]

# The bootstrap facts that depend on the @id JOIN (hypothesis:l4-startup-...).
# Pre-spawn they cannot be resolved, so the pre-spawn record writes each with
# the explicit `pending: resolved after join` marker — never a blank, never a
# `SKIPPED: <predecessor owns>` reason that leaves a cold reader guessing who
# to ask. After the join, rotate-self REWRITES the same record with these
# resolved (post-join overrides).
BOOTSTRAP_JOIN_ONLY_FACTS = [
    "successor_live_model", "successor_address", "model_refusal_fallback",
]


def _write_bootstrap(root: Path, *, seat: str, generation: int | None,
                     telemetry, verification: dict | None,
                     commit: str | None = None,
                     join_pending: set | None = None,
                     overrides: dict | None = None) -> str:
    """s10 — write the successor's bootstrap record.

    `<sessions>/seats/<seat>.bootstrap.json` carries the template telemetry
    set PLUS the owner's fixed fact set (BOOTSTRAP_FIXED_FACTS — "they should
    receive all this telemetry by default"), each resolved to a REAL value
    where the handover can see it (the commit stamp, the config:seats row at
    HEAD, the verification result; `git rev-parse --short HEAD` is the one
    read-only git command allowed) and to a NAMED `SKIPPED: <reason>` where it
    cannot yet (a join-only or sibling-round fact — never the old blanket
    `0b owns deriving`). Every derived fact is stamped in `measured_at` with
    the commit it was measured at, so `_bootstrap_stale` can refuse any record
    that is not at HEAD. Returns the written path (string).

    `join_pending` (a set of fact keys) and `overrides` (a key->value dict)
    support the PRE-SPAWN write (hypothesis:l4-startup-first-turn-is-
    performed-by-the-service-and-the-hook-fires-at-turn-one): a key present in
    `overrides` takes that resolved value (stamped at HEAD); a key in
    `join_pending` but NOT overridden is written as `pending: resolved after
    join` (not SKIPPED, not blank) because the @id join has not happened yet.
    Default ({} / {}) writes every fact through `_derive_bootstrap_fact`
    exactly as before — the post-join call passes the joined facts as
    overrides, so the same record is UPDATED in place, not re-minted.
    """
    if commit is None:
        commit = _git_head(root)
    seat_row = _find_seat(root, seat)

    join_pending = join_pending or set()
    overrides = overrides or {}
    keys = []
    if isinstance(telemetry, list):
        keys = list(telemetry)
    elif isinstance(telemetry, dict):
        keys = list(telemetry)
    for k in BOOTSTRAP_FIXED_FACTS:
        if k not in keys:
            keys.append(k)

    tele: dict = {}
    measured_at: dict = {}
    for key in keys:
        if key in overrides:
            tele[key] = overrides[key]
            if commit:
                measured_at[key] = commit
            continue
        if key in join_pending:
            tele[key] = "pending: resolved after join"
            continue
        value, reason = _derive_bootstrap_fact(
            key, root=root, seat=seat, seat_row=seat_row, commit=commit)
        if value is None:
            tele[key] = f"SKIPPED: {reason}"
        else:
            tele[key] = value
            if commit:
                measured_at[key] = commit
    if verification and commit:
        measured_at["verification"] = commit

    doc = {
        "shape": BOOTSTRAP_SHAPE,
        "seat": seat,
        "generation": generation,
        "written_by": "rotate-self",
        "commit": commit,
        "measured_at": measured_at,
        "telemetry": tele,
        "verification": verification or {"skipped": "no verification run"},
    }
    p = _sessions_dir(root) / "seats" / f"{seat}.bootstrap.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    return str(p)


def _bootstrap_stale(doc: dict, current_commit: str | None,
                     bounds: dict | None = None) -> bool:
    """True when the bootstrap record carries a fact measured at a commit
    older than HEAD — i.e. it must be REFUSED, never injected stale state.
    `bounds` maps fact -> 'head' | 'permanent' (declared in config:rotations
    `## facts`; default 'head' = must be the live commit) and is parsed by the
    caller — the SessionStart hook (the sibling round) calls this before
    injecting. A SKIPPED fact (absent from `measured_at`) asserted nothing and
    is never stale; a fully-skipped doc (no `measured_at`) is never stale
    (nothing to refuse) — the hook injects what is fresh and leaves the named
    skip to the driven prompt. The function the hook can call."""
    measured = (doc or {}).get("measured_at") or {}
    if not measured:
        return False
    bounds = bounds or {}
    for fact, commit in measured.items():
        if bounds.get(fact, "head") == "permanent":
            continue
        if commit != current_commit:
            return True
    return False


def _bootstrap_block(root: Path, seat: str, *, commit: str | None = None,
                     bounds: dict | None = None) -> list:
    """The successor's bootstrap record as ONE injected block, or REFUSES.

    The reader half of the bootstrap injection (hypothesis:l4-startup-is-one-
    script-or-a-driven-prompt, 0b kid 3). `<sessions>/seats/<seat>.bootstrap
    .json` is the record rotate-self's button-down wrote; this returns the
    tiny diagram-shaped block the SessionStart hook should inject for a seat
    successor that wakes KNOWING its state -- or REFUSES (returns [None,
    reason]) when the record is absent ('no_record'), not a JSON object
    ('malformed'), or `_bootstrap_stale(.., HEAD, bounds)` says a measured
    fact is not at HEAD ('stale'). NEVER raises into the hook. `commit` is
    the test seam for HEAD (defaults to `_git_head`); `bounds` is the
    fact->'head'|'permanent' staleness map of config:rotations `## facts`
    (default {} = everything must be the live commit). Returns [block, None]
    when fresh."""
    if commit is None:
        commit = _git_head(root)
    p = _sessions_dir(root) / "seats" / f"{seat}.bootstrap.json"
    try:
        doc = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return [None, "no_record"]
    except ValueError:
        return [None, "malformed"]
    if not isinstance(doc, dict):
        return [None, "malformed"]
    if _bootstrap_stale(doc, commit, bounds):
        return [None, "stale"]
    gen = doc.get("generation")
    gen_s = f"gen {gen}" if isinstance(gen, int) else "gen ?"
    head = f"HEAD@{commit}" if commit else "HEAD@?"
    lines = [
        f"## ⚓ bootstrap: {seat} successor handover",
        f"(shape {doc.get('shape', '?')} · {gen_s} · {head})",
        "",
    ]
    tele = doc.get("telemetry")
    if isinstance(tele, dict) and tele:
        for key in sorted(tele):
            val = str(tele[key])
            if len(val) > 400:
                val = val[:397] + "…"
            lines.append(f"- {key}: {val}")
    else:
        lines.append("- (no telemetry recorded)")
    return ["\n".join(lines) + "\n", None]


def cmd_bootstrap_block(args: argparse.Namespace,
                       root: Path | None = None) -> int:
    """The CLI the SessionStart hook calls: emit the bootstrap block for a
    seat, or REFUSE silently-non-zero. `--seat` names the seat, `--root` the
    project root (default: resolve from cwd). `--json` wraps the outcome,
    `--quiet` prints nothing on success (a test/CI convenience). `--commit`
    is the test seam. Exit 0 on emit, 1 on refuse — never raises."""
    import json as _json  # noqa: PLC0415  (local, keeps name clear of rotate's json)
    root = root if root is not None else (args.root or find_project_root())
    bounds = None
    if getattr(args, "bounds", None):
        try:
            bounds = json.loads(args.bounds)
        except ValueError:
            bounds = None
    if root is None:
        block, reason = None, "outside_project"
    else:
        block, reason = _bootstrap_block(
            Path(root), args.seat, commit=args.commit, bounds=bounds)
    if args.json:
        if block is not None:
            print(_json.dumps({"emitted": True, "seat": args.seat,
                               "block": block}))
        else:
            print(_json.dumps({"emitted": False, "seat": args.seat,
                               "reason": reason}))
        return 0 if block is not None else 1
    if block is not None:
        if not args.quiet:
            sys.stdout.write(block)
        return 0
    return 1


def _repoint_livestream_views(*, tmux_session: str, seat: str,
                              succ_id: str | None,
                              window_path: str | None = None,
                              view_path: str | None = None) -> dict:
    """s9 — re-point the `view-<seat>` livestream session to the successor's
    window @id.

    `view-<seat>` is the grouped tmux session the livestream shows (same
    window set as `<tmux_session>`, e.g. view-sanctuary-director). When the
    view session exists, select the successor's window BY @id
    (`select-window -t 'view-<seat>:@<succ-id>'`) and verify with
    `list-windows -t view-<seat> -F '#{window_id} #{window_active}'`, recording
    what it says. When the session is absent (or no @id was captured) record
    SKIPPED naming it. Under test `window_path` is set (the fixture's stand-in
    for the whole tmux read): a `view_path` seam holds the view session's
    `@<id> <active>` lines; without one the step records SKIPPED and never
    touches real tmux. Returns an observation dict; never raises / never fails
    the rotation (a livestream is an observable, not a guarantee).
    """
    view_sess = f"view-{seat}"
    if not succ_id:
        return {"session": view_sess, "target": None,
                "skipped": f"no successor window @id captured to re-point "
                            f"{view_sess} to"}
    # test/fixture mode — never real tmux.
    if window_path is not None:
        if view_path is None:
            return {"session": view_sess, "target": succ_id,
                    "skipped": f"no view-path seam in this fixture; live "
                                f"{view_sess} re-point deferred to the real run"}
        try:
            lines = [ln.strip() for ln in
                     Path(view_path).read_text(encoding="utf-8").splitlines()
                     if ln.strip()]
        except OSError:
            return {"session": view_sess, "target": succ_id,
                    "skipped": f"view session {view_sess} absent "
                                f"(no {view_path})"}
        active = [w for w in lines if w.strip().endswith(" 1")]
        return {"session": view_sess, "target": succ_id,
                "command": ["tmux", "select-window", "-t",
                             f"{view_sess}:{succ_id}"],
                "active_windows": lines,
                "live_active": active}
    # real tmux.
    try:
        ls = subprocess.run(["tmux", "list-windows", "-t", view_sess],
                            capture_output=True, text=True, timeout=5)
    except Exception:  # noqa: BLE001
        return {"session": view_sess, "target": succ_id,
                "skipped": f"view session {view_sess} absent"}
    if ls.returncode != 0:
        return {"session": view_sess, "target": succ_id,
                "skipped": f"view session {view_sess} absent"}
    sel = subprocess.run(["tmux", "select-window", "-t",
                          f"{view_sess}:{succ_id}"],
                         capture_output=True, text=True, timeout=5)
    ver = subprocess.run(
        ["tmux", "list-windows", "-t", view_sess,
         "-F", "#{window_id} #{window_active}"],
        capture_output=True, text=True, timeout=5)
    active_windows = ([ln.strip() for ln in ver.stdout.strip().splitlines()
                       if ln.strip()] if ver.returncode == 0 else [])
    return {"session": view_sess, "target": succ_id,
            "selected_rc": sel.returncode, "command":
            ["tmux", "select-window", "-t", f"{view_sess}:{succ_id}"],
            "active_windows": active_windows}


# ---- STARTUP first_turn (hypothesis:l4-startup-is-one-script-or-a-
#      driven-prompt, 0b round) -----------------------------------------
#
# A rotation template's `startup` block can carry a `first_turn` list —
# commands rotate-self runs BEFORE spawn so a new rotation lands already
# holding its telemetry (rotation record, seat row, authority, git state,
# inbox, live spawns, write.py verbs — the measured gen-X first calls the
# owner wants folded into the rotation, see .geometry/rotations.md). Each
# command is allowlisted (refused by executable/verb, its LABEL named, never
# run), placeholder-resolved (an unknown placeholder is refused, never
# silently left in), timed per-command, byte-capped, and its outputs are
# composed into a `## STARTUP OUTPUT` block appended to the successor's first
# input turn after the head and the brief (the successor runs nothing).

#: The one canonical placeholder set a first_turn command may name. Any
#: `{key}` NOT in this set, or not present in the caller's values map, is
#: refused rather than silently substituted — an empty-but-known value still
#: resolves (the successor row fields arrive from the join/row); an unknown
#: key is a template bug and must be named.
STARTUP_PLACEHOLDERS = {
    "seat", "succ_ref", "succ_name", "succ_transcript", "pin_ref", "gen",
    "prime_ref", "worktree", "repo", "tmux_session", "pred_pids",
}

#: Per-command timeout and output cap defaults when the template's startup
#: block does not declare them.
DEFAULT_FIRST_TURN_TIMEOUT_S = 60
DEFAULT_STARTUP_BYTE_CAP = 4000

#: The default startup allowlist (executable basenames). A producing command
#: whose executable is NOT here is refused and its label named. `python` is
#: additionally constrained to engine scripts (a path that ends `.py` under
#: `extensions/` or `/bin/`); `git`/`tmux` to their read-only subcommands;
#: `curl` to the credits endpoint. Pipeline filters after a `|` are judged
#: against _STARTUP_FILTERS below.
DEFAULT_STARTUP_ALLOW = {"python", "python3", "git", "tmux", "ps", "curl"}

#: Per-subcommand ALLOWLIST over the git producing judge's arguments
#: (hypothesis:l4-a-producing-git-stage-is-argument-restricted). A git first
#: stage used to be accepted on the READONLY SUBCMD name alone, so its
#: ARGUMENTS never reached the judge: `git log -p -- .env` printed a tracked
#: file's contents into the rotation record and the successor's STARTUP
#: OUTPUT, `git log --output=FILE` (or `git diff --output=FILE`) wrote a file,
#: and `git -c core.pager=<cmd> log` / `--exec-path` ran a program. Now a git
#: stage is an ALLOWLIST PARSER over subcommand AND arguments, in the same
#: spirit as _filter_arg_refusal: `-C <path>` is the one value-taking global
#: option (consumed before the subcommand), then every token is judged against
#: the subcommand's sets below. Each entry is (allowed short-FLAG letters,
#: allowed `--long` forms, allow-bare-`-N`), where the bare `-N` slot is the
#: log count (`git log --oneline -5`). Nothing else — `-p`/`--patch` (dumps
#: file contents), `--output` (writes a file), `-c`/`--exec-path` (runs a
#: program), `-- <pathspec>` (reads a named path), or any token containing
#: `$`/backtick/`~` — is ever on a set, so each falls through to the NAMED
#: refusal `producer git <token> not on the allowlist`.
#:
#: Each row is a 4-tuple (allowed short-FLAG letters, allowed `--long` forms,
#: allow-bare-`-N`, REQUIRED `--long` forms). `fetch` is NOT on the allowlist
#: at all (hypothesis:l4-the-git-allowlist-has-no-network-write): a bare `git
#: fetch` is a NETWORK WRITE (it advances remote-tracking refs) and no
#: rotation template uses it, so it falls through to `producer git fetch not
#: on the allowlist`. `diff` REQUIRES `--stat`: a bare `git diff` would print
#: the working-tree PATCH into the record and the successor's STARTUP OUTPUT,
#: so a `diff` whose args never name `--stat` is refused even though the flag
#: itself is allowed.
_GIT_ALLOW = {
    "status":    (frozenset("sb"), frozenset(), False, frozenset()),
    "log":       (frozenset(), frozenset(("--oneline", "--stat")), True, frozenset()),
    "diff":      (frozenset(), frozenset(("--stat",)), False, frozenset(("--stat",))),
    "rev-parse": (frozenset(), frozenset(("--abbrev-ref",)), False, frozenset()),
    "branch":    (frozenset(), frozenset(("--show-current",)), False, frozenset()),
}
_TMUX_READONLY_SUBCMDS = {"list-windows", "list-sessions", "list-panes",
                          "display-message"}

#: Harmless post-`|` stdio filters allowed in any first_turn pipeline. Only a
#: PRODUCING (first) segment is judged strictly; these read stdio and can't
#: reach the box on their own.
_STARTUP_FILTERS = {"head", "tail", "sed", "grep", "egrep", "cat", "echo",
                    "cut", "sort", "wc", "tr", "awk", "uniq"}

#: Refused FILTER-STAGE argument classes (hypothesis:l4-a-filter-stage-is-
#: argument-restricted). A post-`|` stdio filter used to be skipped by
#: executable NAME alone, so its ARGUMENTS never reached the judge:
#: `| sort -o M` wrote a file, `| head -1 /etc/hostname` read a path into the
#: startup output, and `| awk BEGIN{system(...)}` executed a program body. Now
#: a filter stage is judged too, on the SAME strict standard a producing
#: command is: no argument token may name a path (contain `/`), no argument
#: may be a file-writing/redirecting option (`-o`/`-w`/`-i`/`--output`/`-f`,
#: which for sed/grep/sort/cut name an output file or in-place write), awk is
#: refused outright (its program body can reach `system`/`getline`/`>`/`|`),
#: and sed's `-i` (in-place write) / bare `e` (execute) program forms are
#: refused. Any refused argument is a NAMED refusal (`filter <exe> <arg>`)
#: before anything runs.
#:
#: The refusal is PER-TOOL, not blanket (hypothesis:l4-a-filter-stage-is-
#: argument-restricted, counter-example fix): an option is refused only where
#: it already NAMES a file/in-place write/execute for that executable. The
#: earlier blanket list (`-o -w -i --output -f` on EVERY filter) over-refused
#: benign stdio flags — `sort -f` (fold case), `cut -f1` (fields), `grep -i`
#: (ignore case), `uniq -w` (compare width) are all benign and MUST run. Only
#: sort (`-o`/`--output` output file), sed (`-i` in-place) and grep/egrep
#: (`-f`/`--file` pattern file) carry a real file option; every other filter
#: (head/tail/tr/wc/cat/echo/cut/uniq) is governed ONLY by the path rule.
#: The post-`|` stdio-filter judge is an ALLOWLIST PARSER, not a denylist
#: (hypothesis:l4-a-filter-stage-is-argument-restricted, goal:g17.1 ruling
#: merge-up 33: a denylist of known-bad options is the WRONG mechanism for a
#: security judge — it cannot keep up with the option space, and every miss is
#: a leak). A filter stage is (exe, tokens); SHORT-OPTION CLUSTERS are expanded
#: character by character (`-ni` = `-n -i`, `-if` = `-i -f`); a value-taking
#: option consumes exactly its value (attached `-c1-80` or a separate next
#: token); every option must be in the exe's ALLOWED set; each positional is
#: governed by COUNT and SHAPE. Anything else — an unlisted short letter, an
#: unlisted `--long`, an extra/odd positional, a token containing
#: `$`/`${`/backtick/`~` — is refused as `filter <exe> <token> not on the
#: allowlist`. awk is refused outright; a pipe-fed exe that is not a modeled
#: filter is refused as `filter <exe>` (a first_turn pipeline has no reason to
#: pipe into a producer, closing `| git log -p -- .env` without touching the
#: git allowlist).

#: {exe: (allowed short FLAGS [no value], allowed VALUE-TAKING short letters)}
_FILTER_ALLOW = {
    "head": (frozenset(), frozenset("nc")),
    "tail": (frozenset(), frozenset("nc")),
    "grep": (frozenset("civnowxEFh"), frozenset("mABCe")),
    "egrep": (frozenset("civnowxEFh"), frozenset("mABCe")),
    "sed": (frozenset("nEr"), frozenset()),
    "cut": (frozenset("s"), frozenset("cfd")),
    "sort": (frozenset("nrufs"), frozenset("kt")),
    "uniq": (frozenset("cudi"), frozenset("w")),
    "wc": (frozenset("lwcm"), frozenset()),
    "tr": (frozenset("dsc"), frozenset()),
    "cat": (frozenset("nAs"), frozenset()),
    "echo": (frozenset("n"), frozenset()),
}

#: max free POSITIONALS per exe (grep/egrep the PATTERN, sed the PROGRAM;
#: a second on either is a FILE operand). tr allows up to two SETS; echo's
#: positionals are free (below).
_FILTER_POS_MAX = {
    "head": 0, "tail": 0, "grep": 1, "egrep": 1, "sed": 1,
    "cut": 0, "sort": 0, "uniq": 0, "wc": 0, "cat": 0, "echo": 0,
}

#: tr takes up to TWO SET positionals (`tr a-z A-Z`); a third is a refusal.
_FILTER_TR_SETS = 2

#: Substrings that make an echo positional a leak (it would otherwise print an
#: env value into the record/output) and are therefore refused outright.
_FILTER_FORBIDDEN = ("$", "`", "~")

#: head/tail accept a bare numeric option `-N` (`head -5`); the digit-run form
#: is its own allowlist slot.
_NUM_OPT_RE = re.compile(r"^-\d+$")

#: sed program GRAMMAR allowlist. A program is split on `;`; every command must
#: be a substitute `s` (delimiter d, three fields, flags g/I/p/[0-9]) or an
#: address command (`A`, `A,B`, `/re/`, `$`, optional, then one of p/d/q/!d).
#: Anything else — any `e`/`w`/`r`/`R`/`W` command, a `{`, a `:label`, a `b` —
#: is refused as `filter sed program`, because sed commands can read (`r`),
#: write (`w`), or execute (`e`) files/shell.
_SED_SUB_RE = re.compile(
    # substitute `s`. The delimiter must be a punctuation SEPARATOR — not a
    # flag char, not alphanumeric, not backslash — so a flag char can never
    # be mistaken for a delimiter (under the old lazy `(.*?)` grammar
    # `sgxgygeg`/`s0x0y0e0` let a delimiter that was itself a legal flag char
    # absorb an `e`/`w` into the flags field). Each field is anchored to
    # never contain a bare delimiter (an escaped `\.` pair is allowed, so
    # `s/a\/b/c/g` still passes), and flags stay limited to `[gIp0-9]*`.
    r"^s([^gIp0-9a-zA-Z\\])"
    r"(?:(?:\\.)|(?!\1).)*\1"
    r"(?:(?:\\.)|(?!\1).)*\1"
    r"([gIp0-9]*)$", re.S)
_SED_ADDR_RE = re.compile(
    r"^(?:(?:\d+|\$|/(?:\\.|[^/\\])*/)"
    r"(?:,(?:\d+|\$|/(?:\\.|[^/\\])*/))?)?"
    r"(p|d|q|!d)$", re.S)


#: Env VARs refused UNCONDITIONALLY in a first_turn `VAR=value` prefix, even
#: when a template declares them on `startup.env_allow` (hypothesis:l4-a-
#: filter-stage-is-argument-restricted, FOLD). PATH and PYTHONPATH steer which
#: binary the executor finds; LD_* subverts a running binary's loader. A
#: template author adding `env_allow: [PATH]` out of convenience must still
#: not be able to redirect binary lookup, so these are refused no matter what
#: the allowlist says, not only by their absence from it.
_FOLD_ENV = ("PATH", "PYTHONPATH")


def _sed_program_allowed(program: str) -> bool:
    """True iff every `;`-separated command of `program` matches the sed
    grammar allowlist (substitute `s`, or `A`/`A,B`/`/re/`/`$` address + one of
    p/d/q/!d). Any `e`/`w`/`r`/`R`/`W` command, brace, label, `b`, `=` or
    other form is refused."""
    for cmd in program.split(";"):
        cmd = cmd.strip()
        if not cmd:
            continue
        if not (_SED_SUB_RE.match(cmd) or _SED_ADDR_RE.match(cmd)):
            return False
    return True


def _filter_arg_refusal(exe: str, args: list) -> str | None:
    """Return a one-line NAMED refusal for a post-`|` stdio filter stage, or
    None if the stage is on the allowlist. ALLOWLIST PARSER (goal:g17.1
    ruling, merge-up 33): short-option clusters expand char by char, a
    value-taking option consumes its value, every option must be in the exe's
    ALLOWED set, positionals are governed by COUNT and SHAPE. Anything else is
    refused as `filter <exe> <token> not on the allowlist`; awk outright as
    `filter awk`; an unmodeled exe as `filter <exe>`.
    """
    if exe == "awk":
        # a program body can reach system/getline/`>`/`|`; refused outright
        return "filter awk"
    if exe not in _FILTER_ALLOW:
        # a pipe-fed stage that is not a modeled filter — never a producer
        return f"filter {exe}"
    flags, valueopts = _FILTER_ALLOW[exe]
    if exe == "tr":
        pos_max = _FILTER_TR_SETS
    else:
        pos_max = _FILTER_POS_MAX[exe]
    pos = 0
    # grep/egrep: once the PATTERN has been supplied by `-e`, the free-
    # positional budget drops to ZERO — a further non-option token is a FILE
    # operand (`grep -e x .env` reads .env), not a second pattern.
    pattern_supplied = False
    i = 0
    while i < len(args):
        tok = args[i]
        # EVERY token of EVERY filter stage — options, option values and
        # positionals alike. A `$`, backtick or `~` anywhere is refused:
        # `_resolve_shell_vars` expands `$VAR` from the whole environment at
        # exec time even inside single quotes, so `sed 's/x/$SECRET/'`,
        # `grep '$SECRET'` (a match oracle) and `tr abcdef "$SECRET"` (a
        # mapping) would otherwise leak or map an env value into the record
        # and the successor's STARTUP OUTPUT. A `~` is a path homing/
        # tilde-expansion vector. Nothing legitimate is lost: a sed `$p`
        # address or grep `x$` anchor already fails at exec time (`first
        # turn env var $p is not set`).
        for bad in _FILTER_FORBIDDEN:
            if bad in tok:
                return f"filter {exe} {tok} not on the allowlist"
        if not tok.startswith("-"):
            # a POSITIONAL, governed by count and shape
            if exe == "echo":
                # echo positionals are FREE (forbidden chars already swept
                # above) — the value prints back to the record verbatim.
                i += 1
                continue
            if exe in ("grep", "egrep") and pattern_supplied:
                return f"filter {exe} {tok} not on the allowlist"
            if pos >= pos_max:
                return f"filter {exe} {tok} not on the allowlist"
            pos += 1
            if exe == "sed" and not _sed_program_allowed(tok):
                # the program positional is the whole gate; a bad program is
                # refused with its grammar name, not the generic allowlist msg
                return "filter sed program"
            i += 1
            continue
        if tok.startswith("--"):
            # no `--long` form is on any filter's ALLOWED set
            return f"filter {exe} {tok} not on the allowlist"
        if exe in ("head", "tail") and _NUM_OPT_RE.match(tok):
            i += 1                  # bare `-N` form (`head -5`)
            continue
        # SHORT-OPTION CLUSTER: expand char by char; a value-taking letter
        # consumes the rest of the cluster (attached) or the next token.
        body = tok[1:]
        j = 0
        skip = 1                    # tokens past this one the cluster consumes
        while j < len(body):
            ch = body[j]
            if ch in valueopts:
                if ch == "e" and exe in ("grep", "egrep"):
                    pattern_supplied = True    # `-e PAT` IS the pattern
                if body[j + 1:]:
                    j = len(body)  # attached value `-c1-80` / `-m3`
                elif i + 1 < len(args):
                    # a separate-token value `-n 5` consumed via skip; the
                    # outer loop never re-visits it, so sweep it for
                    # forbidden chars HERE, exactly like the option token, or
                    # `-e $SECRET` would expand the env value at exec time.
                    val_tok = args[i + 1]
                    for bad in _FILTER_FORBIDDEN:
                        if bad in val_tok:
                            return (f"filter {exe} {val_tok} "
                                    "not on the allowlist")
                    skip = 2        # separate value `-n 5` consumed
                    j = len(body)
                else:
                    return f"filter {exe} -{ch} not on the allowlist"
            elif ch in flags:
                j += 1
            else:
                return f"filter {exe} -{ch} not on the allowlist"
        i += skip
    return None



#: Shell operators a first_turn command may NOT contain. `|` and `;` ARE
#: modeled (the no-shell executor wires pipelines and sequential commands
#: explicitly, approach A of hypothesis:l4-first-turn-allowlist-cannot-be-
#: bypassed-by-the-shell); every OTHER shell metacharacter is refused with a
#: named reason before anything runs, because we run WITHOUT a shell and do
#: not model it. A refusal now is the explicit floor: if a future change
#: reintroduces `shell=True`, this named gate still stops the bypass. A bare
#: `$VAR`/`${VAR}` is NOT here — it is resolved safely from os.environ (see
#: _resolve_shell_vars), never handed to a shell.
_STARTUP_SHELL_OPS = ("&&", "||", "$(", "`", "<<", ">>", ">",
                     "<", "&", "\n")


def _operator_refusal(command: str) -> str | None:
    """Return a one-line named refusal if `command` contains an unmodeled
    shell operator (`&&` `||` `$(...`  backtick `<` `>` `<<` `>>` `&` newline),
    else None. `|` and `;` are modeled separators (the no-shell executor wires
    them explicitly) and `$VAR`/`${VAR}` expands from env, so none of those
    trip this gate. Checked at allowlist time AND again on the resolved command
    before it runs (belt over the no-shell executor)."""
    for op in _STARTUP_SHELL_OPS:
        if op in command:
            name = "newline" if op == "\n" else op
            return f"unmodeled shell operator {name!r} in first_turn command"
    return None

_SHELL_VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def _resolve_shell_var(m: "re.Match") -> str:
    """Return the env value for one `$VAR`/`${VAR}` match, or REFUSE (raise
    ValueError, naming the var) if it is unset. Shared by the whole-string
    (_resolve_shell_vars) and per-token (_resolve_shell_vars_per_token)
    resolvers. Both are NO-SHELL: the value is substituted AS A LITERAL and
    never handed to a shell. Only this bare env form is modeled; `$(` command
    substitution is refused by _operator_refusal before either is reached."""
    name = m.group(1) or m.group(2)
    val = os.environ.get(name)
    if val is None:
        raise ValueError(f"first_turn env var ${name} is not set")
    return val


def _resolve_shell_vars(command: str) -> str:
    """Whole-STRING env expansion, kept for the (now unused by first_turn)
    callers that expand a full command before tokenizing. The first_turn
    executor does NOT use this form — it uses _resolve_shell_vars_per_token,
    so an env VALUE can never re-introduce shell syntax
    (hypothesis:l4-an-env-value-cannot-break-a-quoted-argument)."""
    return _SHELL_VAR_RE.sub(_resolve_shell_var, command)


def _resolve_shell_vars_per_token(command: str) -> str:
    """Expand `$VAR`/`${VAR}` AFTER quote-aware tokenization, PER TOKEN, then
    rejoin with shlex.join — the ONE env resolver the first_turn executor uses
    (hypothesis:l4-an-env-value-cannot-break-a-quoted-argument).
    `_tokenize_startup` splits the command into argv elements FIRST; each
    element then has its `$VAR`/`${VAR}` references replaced by the value as
    ONE literal token (never word-split), and the elements are rejoined so the
    allowlist re-judge and the no-shell executor re-parse them identically (a
    `shlex.join` round-trip is exact for this grammar, punctuation_chars
    included). A value carrying a double quote, a space, or a `|`/`;` therefore
    stays INSIDE that single argv element — it cannot add an argv element and
    cannot inject a stage; what the re-judge sees is exactly what will execute.
    Raises _StartupParseError (unparseable command, named) or ValueError (an
    unset `$VAR`, named); never returns an unexpanded `$VAR`."""
    expanded = [_SHELL_VAR_RE.sub(_resolve_shell_var, t)
                for t in _tokenize_startup(command)]
    return shlex.join(expanded)


class _StartupParseError(ValueError):
    """Raised when a first_turn command cannot be tokenized (unbalanced quote,
    trailing backslash, etc.). The caller (the allowlist guard / runner) turns
    this into a NAMED refusal, never a crash of rotate-self."""
    pass


def _tokenize_startup(command: str) -> list:
    """Quote-aware shlex tokenization of a WHOLE first_turn command in one
    pass. An UNQUOTED `|` or `;` (shlex punctuation chars) is emitted as its
    own single-token separator; a `|`/`;` inside quotes stays inside its
    argument token, so a quoted argument like `"a|b"` survives whole. This is
    the ONE grammar both the allowlist judge (_segment_parts) and the no-shell
    executor (_command_units) split on, so the two cannot diverge — the whole
    point of hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell.
    Raises _StartupParseError (naming the shlex error) on an unparseable
    command, e.g. an unbalanced quote or trailing backslash."""
    try:
        lex = shlex.shlex(command, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        return list(lex)
    except ValueError as exc:
        raise _StartupParseError(
            "unparseable first_turn command: %s" % exc) from exc


def _startup_units(command: str) -> list:
    """Quote-aware split of a tokenized command into `;`-units of `|`-stages.
    Returns a list of units, each a list of stages, each a list of tokens, with
    the unquoted `|`/`;` separators removed (they became single tokens in
    _tokenize_startup and are consumed here as boundaries). An unquoted `|`
    closes the current stage; an unquoted `;` closes the current unit. Runs
    NOTHING. Both the allowlist judge and the no-shell executor derive their
    groups from this one function."""
    toks = _tokenize_startup(command)
    units, stages, cur = [], [], []
    for t in toks:
        if t == "|":
            if cur:
                stages.append(cur)
                cur = []
        elif t == ";":
            if cur:
                stages.append(cur)
                cur = []
            if stages:
                units.append(stages)
                stages = []
        else:
            cur.append(t)
    if cur:
        stages.append(cur)
    if stages:
        units.append(stages)
    return units


def _command_units(command: str) -> list:
    """Parse a (fully resolved) first_turn command into sequential `;`-units,
    each a list of `|`-stage (argv, env_prefix) pairs. A leading `VAR=value`
    prefix token of a stage is retained and applied as THAT ONE stage's
    environment (never the whole command); it is stripped from the argv. Runs
    NOTHING. Same grammar as the allowlist judge (_segment_parts): both derive
    from _tokenize_startup / _startup_units, so the separators are identical
    (unquoted `|`/`;` only) and nothing outside these tokens can reach the box.
    Raises _StartupParseError on an unparseable command."""
    units = []
    for stage_list in _startup_units(command):
        parsed = []
        for stage in stage_list:
            toks = stage[:]
            i = 0
            prefix = {}
            while i < len(toks) and "=" in toks[i] and not toks[i].startswith("-"):
                var, _, val = toks[i].partition("=")
                prefix[var] = val
                i += 1
            parsed.append((toks[i:], prefix))
        if any(argv for argv, _ in parsed):
            units.append(parsed)
    return units


def _run_units_no_shell(units: list, timeout_s: int):
    """Run sequential `;` units, each a `|` pipeline, WITHOUT a shell (approach
    A). Each stage is subprocess.run(stage_argv, shell=False), the prior stage's
    stdout wired as the next stage's stdin; a stage's own `VAR=value` prefix is
    passed as env. Returns (last_rc, merged_output). Nothing outside the parsed
    argv can execute: no shell, no redirects, no `&&`/`||`/`$(...)`/backticks.

    Filter semantics (hypothesis:l4-first-turn-filters-truncate): per `|`
    pipeline only the LAST stage's stdout is appended to the merged output, so
    a `| head -N` / `| sed -n ...` stdio filter actually truncates — a producer
    stage's stdout is piped into the next stage (its only destination) and not
    echoed past the filter. Every stage's stderr is still merged in order
    (a failing middle stage stays visible). `;` units still concatenate. The
    byte cap and truncation flag live in the caller and are untouched."""
    last_rc, chunks = 0, []
    for stages in units:
        prev_in = None
        n = len(stages)
        for idx, (argv, prefix) in enumerate(stages):
            if not argv:
                continue
            proc = subprocess.run(argv, shell=False, capture_output=True,
                                  input=prev_in, text=True, timeout=timeout_s,
                                  env={**os.environ, **prefix})
            last_rc = proc.returncode
            prev_in = proc.stdout
            is_last = (idx == n - 1)
            # Only the LAST stage of a pipeline contributes its stdout; every
            # stage's stderr is kept, in stage order.
            merged = proc.stdout if (is_last and proc.stdout) else ""
            if proc.stderr:
                merged = ((merged + "\n" + proc.stderr).strip()
                          if merged else proc.stderr.strip())
            if merged:
                chunks.append(merged)
    return last_rc, "\n".join(c for c in chunks if c)


def _segment_parts(command: str) -> list:
    """Split a first_turn command into producing pipeline parts, quote-aware
    (a `|`/`;` inside quotes stays inside its argument). Returns one token-
    list per `|`-/`;`-part, a leading env assignment skipped per part. THE SAME
    grammar as the no-shell executor (_command_units): both derive from
    _tokenize_startup / _startup_units, so the judge and the executor split on
    identical separators (unquoted `|`/`;` only) and cannot diverge. Raises
    _StartupParseError on an unparseable command; the allowlist guard turns
    that into a refusal, never a crash."""
    parts = []
    for stage_list in _startup_units(command):
        for stage in stage_list:
            toks = stage[:]
            i = 0
            while i < len(toks) and "=" in toks[i] and not toks[i].startswith("-"):
                i += 1
            parts.append(toks[i:])
    return parts


def _git_arg_refusal(args: list) -> str | None:
    """Return a one-line NAMED refusal for a unit-leading git stage, or None
    if (subcommand, args) is on the allowlist (hypothesis:l4-a-producing-git-
    stage-is-argument-restricted). ALLOWLIST PARSER, same spirit as
    _filter_arg_refusal: `-C <path>` (git's global workdir option) is the one
    value-taking option, consumed before the subcommand; then every token is
    judged against the subcommand's allowed short-FLAG letters, `--long`
    forms, and (for log) the bare `-N` count. A `--` pathspec separator, a
    `$`/backtick/`~` anywhere, and any off-allowlist option fall through to
    the same NAMED `producer git <token> not on the allowlist` refusal.
    """
    i = 0
    while i + 1 < len(args) and args[i] == "-C":
        val = args[i + 1]
        for bad in ("$", "`", "~"):
            if bad in val:
                return f"producer git {val} not on the allowlist"
        i += 2                      # consume git's global `-C <path>`
    if i >= len(args):
        return "producer git"
    sub = args[i]
    allow = _GIT_ALLOW.get(sub)
    if allow is None:
        return ("producer git " + " ".join(args)).strip()
    flags, longs, numeric, requires = allow
    i += 1
    pos = 0
    seen = set()
    while i < len(args):
        tok = args[i]
        for bad in ("$", "`", "~"):
            if bad in tok:
                return f"producer git {tok} not on the allowlist"
        if tok == "--":
            return f"producer git {tok} not on the allowlist"
        if not tok.startswith("-"):
            # a positional; only rev-parse takes HEAD (and once)
            if sub == "rev-parse" and pos == 0 and tok == "HEAD":
                pos += 1
                i += 1
                continue
            return f"producer git {tok} not on the allowlist"
        if tok.startswith("--"):
            base = tok.split("=", 1)[0]
            if base not in longs:
                return f"producer git {base} not on the allowlist"
            seen.add(base)
            i += 1
            continue
        if numeric and _NUM_OPT_RE.match(tok):
            i += 1                  # log's bare `-N` count
            continue
        # short-option cluster; every letter must be an allowed flag
        for ch in tok[1:]:
            if ch not in flags:
                return f"producer git {tok} not on the allowlist"
        i += 1
    for req in requires:
        if req not in seen:
            # a REQUIRED --long form never appeared (diff without --stat would
            # print the working-tree patch) — refuse the subcommand by name
            return f"producer git {sub} {req} required"
    return None


def _producing_refusal(command: str) -> str | None:
    """Return a one-line refusal (naming the executable/verb) if ANY producing
    pipeline part of `command` is not on the startup allowlist, else None.

    Pipeline filters (head/grep/sed/...) after a `|` are allowed; every
    PRODUCING segment (`;`- or `|`-first) must pass the strict allowlist.
    An unmodeled shell operator (`&&` `||` `&` `$(...)` backtick `<` `>`
    `>>` newline) is refused first with its name — the floor that keeps the
    grammar closed even if a future executor reintroduces a shell.
    """
    op = _operator_refusal(command)
    if op:
        return op
    try:
        units = _startup_units(command)
    except _StartupParseError as exc:
        # Never raise out of the guard: an unparseable command (unbalanced
        # quote, trailing backslash, ...) is a NAMED refusal, not a crash of
        # rotate-self.
        return "unparseable command: %s" % exc
    for unit in units:
        for stageno, stage in enumerate(unit):
            toks = stage[:]
            i = 0
            while i < len(toks) and "=" in toks[i] and not toks[i].startswith("-"):
                i += 1
            toks = toks[i:]
            if not toks:
                continue
            raw_exe = toks[0]
            if "/" in raw_exe:
                # a path-form exe token (any `/`, incl. `/tmp/x/head`, `./head`)
                # is judged BY NAME, not by basename — basename would silently
                # allow an off-allowlist binary behind a path. This holds for
                # unit-leading producers AND pipe-fed filter stages alike
                # (hypothesis:l4-a-filter-exe-is-judged-by-path-and-a-sed-
                # grammar-anchors-its-fields).
                return f"producer {raw_exe} is a path, not an allowlisted name"
            exe = raw_exe
            args = toks[1:]
            if stageno > 0:
                # a PIPE-FED stage: must be a stdio filter, judged on its
                # ARGUMENTS (hypothesis:l4-a-filter-stage-is-argument-
                # restricted) — no off-allowlist option, no positionals.
                if exe in _STARTUP_FILTERS:
                    fret = _filter_arg_refusal(exe, args)
                    if fret:
                        return fret
                    continue
                # a pipe-fed PRODUCER (git/python3/ps/...) has no reason to
                # appear mid-pipeline; refused by name (closes
                # `| git log -p -- .env` without touching the git allowlist).
                return f"filter {exe}"
            # unit-leading PRODUCER, on the strict allowlist
            if exe == "ps":
                continue
            if exe in ("python", "python3"):
                script = args[0] if args else ""
                if not (script.endswith(".py")
                        and ("extensions/" in script or "/bin/" in script)):
                    return f"{exe} {script}".strip()
                continue
            if exe == "git":
                gref = _git_arg_refusal(args)
                if gref:
                    return gref
                continue
            if exe == "tmux":
                sub = args[0] if args else ""
                if sub not in _TMUX_READONLY_SUBCMDS:
                    return ("tmux " + " ".join(args)).strip()
                continue
            if exe == "curl":
                joined = " ".join(toks)
                if "openrouter.ai" in joined and "credits" in joined:
                    continue
                return ("curl " + " ".join(args)).strip()
            return (exe + " " + " ".join(args)).strip()
    return None


def _env_prefix_refusal(command: str, allow: frozenset) -> str | None:
    """Return a one-line refusal (naming the VAR and the allowlist) if ANY
    leading `VAR=value` env prefix in `command` names a VAR not on the startup
    env allowlist, else None. A leading `VAR=value` is APPLIED to that stage's
    child env by the no-shell executor (_command_units/_run_units_no_shell) but
    was DROPPED by the allowlist judge (_segment_parts skips it), so
    `PATH=<dir> <allowlisted argv0>` could silently reach an off-allowlist
    program (hypothesis:l4-first-turn-env-prefix-is-judged). A prefix whose VAR
    is not explicitly on `startup.env_allow` (default EMPTY) is REFUSED here,
    before the executor ever sees the command. An unparseable command yields
    None — the producing judge (_producing_refusal) names that separately.
    Only the leading `VAR=value` run per stage is checked, matching exactly how
    the executor collects prefixes."""
    try:
        units = _startup_units(command)
    except _StartupParseError:
        return None
    for stage_list in units:
        for stage in stage_list:
            for t in stage:
                if "=" in t and not t.startswith("-"):
                    var = t.partition("=")[0]
                    if var in _FOLD_ENV or var.startswith("LD_"):
                        return f"env prefix {var} refused unconditionally"
                    if var not in allow:
                        return f"env prefix {var} not on startup.env_allow"
                else:
                    break
    return None


_REFUSAL_REDACT = "<expanded value redacted>"


_REFUSAL_MIN_DROP_CHARS = 4

# The fixed prose words rotate.py's own refusal messages emit (whitespace-
# split form). A message word that is one of these is never mistaken for an
# env-injected fragment even when — by coincidence — it is a substring of some
# env VALUE (hypothesis:l4-an-env-value-cannot-break-a-quoted-argument).
_REFUSAL_TEMPLATE_WORDS = frozenset([
    "allowlist", "allowlisted", "startup.allow:", "startup.env_allow",
    "unmodeled", "shell", "operator", "first_turn", "command",
    "unparseable", "unconditionally", "injected", "producer", "filter",
    "prefix", "refused", "placeholder", "executable", "spawn",
])


def _scrub_injected_refusal(message: str, record_cmd: str) -> str:
    """Rebuild a RE-JUDGE refusal message so no fragment of an env VALUE
    survives into it. The re-judge (`_producing_refusal` / `_env_prefix_refusal`
    on the env-EXPANDED `exec_cmd`) must run on the expanded form to SEE an
    injected stage, but the record keeps every `$VAR` literal (fix b), so a
    word of `message` that is a substring of some expanded env value AND is
    absent verbatim from the literal `record_cmd` is an ENV-INJECTED fragment —
    a secret-shaped word the value carried. It is dropped and the record's
    literal `$VAR` names are appended, so the refusal names its source without
    ever echoing the value. A word present in `record_cmd` (template text,
    boilerplate, a genuinely-spelled stage) is kept; a message naming no env
    value at all is returned unchanged (placeholder-injected content already
    lives in `record_cmd` by design — only ENV vars stay literal).

    Two guards keep an INNOCENT refusal intact (hypothesis:l4-an-env-value-
    cannot-break-a-quoted-argument): a word is only ever dropped when it is at
    least _REFUSAL_MIN_DROP_CHARS long (short common words like `a`/`on`/`me`/`the`
    are substrings of almost any path VALUE and are NOT injection) and when it
    is not a word of rotate.py's own refusal prose (_REFUSAL_TEMPLATE_WORDS).
    This is the FALSIFIER guard of hypothesis:l4-the-refusal-names- the-record-
    stage-not-the-expanded-tokens: a refusal never contains a substring of an
    env value that is not in record_cmd, and an honest refusal never collapses
    to the bare redaction trailer."""
    sources = []
    for m in _SHELL_VAR_RE.finditer(record_cmd):
        name = m.group(1) or m.group(2)
        val = os.environ.get(name)
        if val is None:
            continue
        sources.append((name, val))
    if not sources:
        return message
    kept, redacted_any = [], False
    for tok in message.split():
        if (len(tok) >= _REFUSAL_MIN_DROP_CHARS
                and tok not in _REFUSAL_TEMPLATE_WORDS
                and any(tok in val for _, val in sources)
                and tok not in record_cmd):
            redacted_any = True      # an injected value fragment: drop it
            continue
        kept.append(tok)
    if not redacted_any:
        return message
    names = ", ".join("$" + n for n, _ in sources)
    label = " ".join(kept).strip()
    trailer = f"{_REFUSAL_REDACT} (expanded from {names})"
    return f"{label} {trailer}" if label else trailer


def _resolve_startup_placeholders(command: str, values: dict, *,
                                  refuse_empty: bool = False) -> str:
    """Substitute `{key}` placeholders; REFUSE (raise ValueError, naming the
    key) on any key not in the canonical STARTUP_PLACEHOLDERS set, so an
    unknown/unresolved placeholder is never silently left in the command.
    With `refuse_empty=True` (the first_turn path only), a placeholder the
    command USES whose value resolves to EMPTY is ALSO refused, naming the
    placeholder (`placeholder {key} empty at spawn`), instead of producing a
    command that runs on an empty slot and dumps a usage error. Other callers
    (the driven `next` walk, bootstrap) leave `refuse_empty` False: for them
    an empty placeholder may be legitimate, and they must not be forced to
    fall over on it."""
    def _sub(m):
        key = m.group(1)
        if key not in STARTUP_PLACEHOLDERS:
            raise ValueError(f"unknown startup placeholder {{{key}}}")
        value = values.get(key, "")
        if refuse_empty and not str(value):
            raise ValueError(f"placeholder {{{key}}} empty at spawn")
        return str(value)
    return re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", _sub, command)


def _run_first_turn_commands(startup: dict, values: dict, *,
                             dry_run: bool = False) -> list:
    """Run the template's `startup.first_turn` list, one at a time, BEFORE
    spawn, returning one result dict per entry.

    Order of gates per entry, all fail-closed and named in the result:
      1. env allowlist — a leading `VAR=value` prefix whose VAR is not on
         `startup.env_allow` (default EMPTY) is REFUSED (var named) and never
         applied (hypothesis:l4-first-turn-env-prefix-is-judged);
      2. allowlist — an off-allowlist executable/verb is REFUSED (label named)
         and never run;
      3. placeholders — an unknown `{key}` is REFUSED (key named);
      4. run — one command at a time, per-command timeout
         (`first_turn_timeout_s`, default 60); output truncated to the byte
         cap (`byte_cap`, default 4000) and marked.
    `dry_run` resolves and records every entry but runs NOTHING. Never
    raises; every failure surfaces as a result dict.
    """
    startup = startup or {}
    entries = startup.get("first_turn") or []
    timeout_s = startup.get("first_turn_timeout_s") or DEFAULT_FIRST_TURN_TIMEOUT_S
    byte_cap = startup.get("byte_cap") or DEFAULT_STARTUP_BYTE_CAP
    env_allow = frozenset(startup.get("env_allow") or [])
    results = []
    for e in entries:
        entry = e if isinstance(e, dict) else {"label": str(e), "cmd": str(e)}
        label = entry.get("label", "")
        cmd = entry.get("cmd", "")
        env_refusal = _env_prefix_refusal(cmd, env_allow)
        if env_refusal:
            results.append({"label": label, "cmd": cmd,
                            "refused": env_refusal})
            continue
        refusal = _producing_refusal(cmd)
        if refusal:
            results.append({"label": label, "cmd": cmd,
                            "refused": f"not on startup.allow: {refusal}"})
            continue
        try:
            record_cmd = _resolve_startup_placeholders(cmd, values,
                                                       refuse_empty=True)
        except ValueError as exc:
            results.append({"label": label, "cmd": cmd, "refused": str(exc)})
            continue
        # Two forms (fix b): `record_cmd` keeps `$VAR` LITERAL — what the result
        # dict's `cmd` and dry-run report, byte-identical to the pre-expansion
        # text so a secret never lands in the record. `exec_cmd` env-expands it
        # PER TOKEN (never on the whole string) and is used ONLY to build the
        # no-shell argv; execution needs the value, the record must not hold it.
        # A value carrying a double quote, a space, or a `|`/`;` stays inside
        # ONE argv element and is never re-parsed (hypothesis:l4-an-env-value-
        # cannot-break-a-quoted-argument).
        try:
            exec_cmd = _resolve_shell_vars_per_token(record_cmd)
        except _StartupParseError as exc:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": "unparseable command: %s" % exc})
            continue
        except ValueError as exc:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": str(exc)})
            continue
        # Belt over the no-shell executor: re-judge the EXEC command IN FULL.
        # A PLACEHOLDER value can inject a whole new stage wrapped in `;` or `|`
        # (both MODELED separators); placeholders substitute into the string
        # BEFORE tokenization, so the injected stage is here and the template
        # judge never saw it. An ENV value cannot inject one (per-token
        # expansion keeps it inside one element), but the re-judge still runs on
        # exec_cmd so what is judged is what is executed. Re-run the env
        # allowlist and the producing allowlist BEFORE _command_units splits it,
        # so an injected `touch`-style stage is refused, not run, and its
        # `$VAR` stays literal in the record (hypothesis:l4-the-judge-runs-on-
        # the-substituted-command).
        exec_env_refusal = _env_prefix_refusal(exec_cmd, env_allow)
        if exec_env_refusal:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": _scrub_injected_refusal(
                                exec_env_refusal, record_cmd)})
            continue
        exec_refusal = _producing_refusal(exec_cmd)
        if exec_refusal:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": "not on startup.allow: "
                                       + _scrub_injected_refusal(
                                           exec_refusal, record_cmd)})
            continue
        # Unmodeled-operator check stays: an operator `_producing_refusal`
        # deliberately does not model (e.g. `&&`) is caught here. `$VAR` is
        # expanded for execution only; the record keeps the literal `$VAR`.
        op = _operator_refusal(exec_cmd)
        if op:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": op})
            continue
        if dry_run:
            results.append({"label": label, "cmd": record_cmd, "dry": True})
            continue
        try:
            units = _command_units(exec_cmd)
        except _StartupParseError as exc:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": "unparseable command: %s" % exc})
            continue
        if not units:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": "no executable in first_turn command"})
            continue
        try:
            rc, out = _run_units_no_shell(units, timeout_s)
        except subprocess.TimeoutExpired:
            results.append({"label": label, "cmd": record_cmd,
                            "timed_out_after_s": timeout_s})
            continue
        truncated = False
        if len(out) > byte_cap:
            out = out[:byte_cap]
            truncated = True
        results.append({"label": label, "cmd": record_cmd, "rc": rc,
                        "output": out, "truncated": truncated,
                        "byte_cap": byte_cap})
    return results


def _compose_startup_output(results: list) -> str:
    """Compose the successor's `## STARTUP OUTPUT` block from the per-command
    results. The heading is contract (a test pins it); every entry lists its
    label, status and output. Runs NOTHING — pure formatting over the results
    the runner already produced."""
    lines = [
        "## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)",
    ]
    for r in results:
        lines.append("")
        if r.get("refused"):
            status = "REFUSED"
        elif r.get("dry"):
            status = "DRY-RUN"
        elif r.get("timed_out_after_s"):
            status = f"TIMEOUT (>{r['timed_out_after_s']}s)"
        else:
            status = f"exit {r.get('rc')}"
        lines.append(f"[{r.get('label', '')}] {status}")
        lines.append(f"$ {r.get('cmd', '')}")
        if r.get("refused"):
            lines.append(f"    refused — {r['refused']}")
        elif r.get("dry"):
            lines.append("    (dry-run — not executed)")
        elif r.get("timed_out_after_s"):
            lines.append(f"    timed out after {r['timed_out_after_s']}s")
        else:
            if r.get("truncated"):
                lines.append(f"    (output truncated to {r['byte_cap']} bytes)")
            out = (r.get("output") or "").strip()
            if out:
                lines.extend(f"    {ln}" for ln in out.splitlines())
    return "\n".join(lines)


def _first_turn_values(root: Path, *, seat: str, gen: int,
                       succ_name: str, succ_ref: str = "",
                       succ_transcript: str = "",
                       tmux_session: str = DEFAULT_TMUX_SESSION,
                       worktree: str | None = None, repo: str | None = None,
                       pred_pids: str = "") -> dict:
    """Build the placeholder values map for a rotation's first_turn commands.

    `seat`/`gen`/`succ_name`/`tmux_session` are known at spawn time; the rest
    are best-effort from the join, the successor row, the seats registry and
    the filesystem. Every key in STARTUP_PLACEHOLDERS is present (possibly
    empty) so any referenced placeholder resolves to SOMETHING — an unknown
    key is what is refused, never a known-but-empty one.
    """
    if worktree is None:
        worktree = os.getcwd()
    if repo is None:
        try:
            repo = str(locations.repo_root(root))
        except Exception:  # noqa: BLE001
            repo = str(worktree)
    prime_ref = ""
    for row in _load_seats(root):
        if row.get("role") == "prime_director" and row.get("session_ref"):
            prime_ref = str(row["session_ref"])
            break
    return {
        "seat": seat,
        "succ_ref": succ_ref or "",
        "succ_name": succ_name,
        "succ_transcript": succ_transcript or "",
        "pin_ref": str(_sessions_dir(root) / f"{seat}.meter"),
        "gen": str(gen),
        "prime_ref": prime_ref,
        "worktree": str(worktree),
        "repo": str(repo),
        "tmux_session": tmux_session,
        "pred_pids": pred_pids or "",
    }


# ---- STARTUP DRIVEN next (hypothesis:l4-startup-is-one-script-or-a-
#      driven-prompt, OPERATOR path) --------------------------------------
#
# The AUTOMATED half (kid 1, above) RUNS the template `startup` steps for
# the successor. The DRIVEN half is the OPERATOR walk — for whatever cannot
# be scripted, and for a human turning a seat's startup by hand:
#
#   rotate.py next --seat <seat> [--record-ok|--record-fail] [--json]
#
# PRINTS EXACTLY the next `startup` step's literal command (placeholders
# resolved) and NOTHING ELSE on the default path, one step per call,
# advancing only on a recorded success (`--record-ok`). A step is DONE only
# when its recorded success exists; a recorded failure is NOT done and is
# re-printed. Progress persists at `<sessions>/seats/<seat>.startup.json`
# (step list + per-step status). `next` NEVER runs a command — the operator
# does; that is the whole point of the driven path. The step list is the
# SAME template `startup` block (first_turn then after_join) read through
# the SAME loader, and placeholders resolve with the SAME
# `_resolve_startup_placeholders`, so a driven and an automated walk agree
# on what the startup is.

STARTUP_DONE_LINE = ("## STARTUP DONE — every startup step has a "
                     "recorded success")


# ---- STARTUP after_join — THE SERVICE performs the captive first turn ----
# hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-
# fires-at-turn-one (0b-b owed item (i)). The template `startup` block carries
# an `after_join` list (commands that need the successor's identity — the join,
# the pin, the ack `continue` as the default, model_confirm, the reap proof) and
# `after_join_delay_s` (default 20). THE SERVICE (the heal.py watch loop when
# `agent_dispatch.inline_reaper` is false, else the rotate-self post-spawn
# tail when no service runs) waits the delay, then runs the whole list as ONE
# flow, writes every command's output into the rotation record, and sends ONE
# dm (the successor's SECOND input) through send.py's fixed nudge. The cap-
# tive dm prints the exact copy-paste line for the one remaining decision
# (a `diff` against the handoff); the successor runs NOTHING itself.

DEFAULT_AFTER_JOIN_DELAY_S = 20
DEFAULT_AFTER_JOIN_TIMEOUT_S = 60


def _inline_reaper_enabled(root: Path) -> bool:
    """True when `agent_dispatch.inline_reaper` is truthy — the reaper runs
    INSIDE dispatch, so NO separate persistent service exists and rotate-self
    is the performer of the captive after_join. False means the heal.py watch
    loop IS the service and owns after_join. Absent config defaults to True
    (current behaviour unchanged; a declared service is a one-edit opt-in), and
    a missing `agent_dispatch` block reads defensively."""
    try:
        cfg_path = locations.config_path(root) if root is not None else None
        if cfg_path is None:
            return True
        cfg = json.loads(cfg_path.read_text())
    except Exception:                                   # noqa: BLE001
        return True
    ad = (cfg or {}).get("agent_dispatch") or {}
    return bool(ad.get("inline_reaper", True))


def _run_after_join_command(entry, values: dict, timeout_s: int,
                            byte_cap: int) -> dict:
    """Resolve + run ONE after_join command through the no-shell executor,
    returning a first_turn-shaped result dict (label, cmd, rc/output) or a
    named refusal. The after_join list is PRIME-CLEANED trusted config (judged
    at the merge-up so the WHOLE templates value passes the L4.234 gate), so it
    is NOT re-run through the producing allowlist — only placeholder-resolved,
    tokenized, and executed no-shell (a placeholder value can never inject a
    stage outside `_command_units`' grammar, and `_operator_refusal` is checked
    so no unmodeled `&&`/`||` survives).`"""
    if not isinstance(entry, dict):
        entry = {"label": str(entry), "cmd": str(entry)}
    label = entry.get("label", "")
    cmd = entry.get("cmd", "")
    try:
        record_cmd = _resolve_startup_placeholders(cmd, values,
                                                   refuse_empty=False)
    except ValueError as exc:
        return {"label": label, "cmd": cmd, "refused": str(exc)}
    try:
        exec_cmd = _resolve_shell_vars_per_token(record_cmd)
    except (_StartupParseError, ValueError) as exc:
        return {"label": label, "cmd": record_cmd, "refused": str(exc)}
    try:
        units = _command_units(exec_cmd)
    except _StartupParseError as exc:
        return {"label": label, "cmd": record_cmd, "refused": str(exc)}
    op = _operator_refusal(exec_cmd)
    if op:
        return {"label": label, "cmd": record_cmd, "refused": op}
    if not units:
        return {"label": label, "cmd": record_cmd,
                "refused": "no executable in after_join command"}
    try:
        rc, out = _run_units_no_shell(units, timeout_s)
    except subprocess.TimeoutExpired:
        return {"label": label, "cmd": record_cmd,
                "timed_out_after_s": timeout_s}
    truncated = False
    if len(out) > byte_cap:
        out = out[:byte_cap]
        truncated = True
    return {"label": label, "cmd": record_cmd, "rc": rc, "output": out,
            "truncated": truncated, "byte_cap": byte_cap}


def _compose_after_join_dm(seat: str, gen: int, succ_ref: str,
                           results: list) -> str:
    """The successor's SECOND input — one captioned block naming the service
    as the performer, every after_join command's label+output, and the ONE
    CAPTIVE copy-paste line for the single remaining decision (`diff` against
    the handoff). Pure formatting; runs and sends nothing."""
    lines = [
        "## AFTER_JOIN OUTPUT (the SERVICE ran the rotation's after_join for "
        "you; you ran nothing)",
        "This is your SECOND input, delivered `after_join_delay_s` after spawn.",
    ]
    for r in results:
        lines.append("")
        if r.get("refused"):
            status = "REFUSED"
        elif r.get("timed_out_after_s"):
            status = f"TIMEOUT (>{r['timed_out_after_s']}s)"
        else:
            status = f"exit {r.get('rc')}"
        lines.append(f"[{r.get('label', '')}] {status}")
        lines.append(f"$ {r.get('cmd', '')}")
        if r.get("refused"):
            lines.append(f"    refused — {r['refused']}")
        elif r.get("timed_out_after_s"):
            lines.append(f"    timed out after {r['timed_out_after_s']}s")
        else:
            if r.get("truncated"):
                lines.append(f"    (output truncated to {r['byte_cap']} bytes)")
            out = (r.get("output") or "").strip()
            if out:
                lines.extend(f"    {ln}" for ln in out.splitlines())
    lines.append("")
    lines.append("Where a decision remains (only a `diff` against the "
                 "handoff), emit EXACTLY this copy-paste line:")
    lines.append("python3 extensions/agi/bin/rotate.py "
                 f"ack --seat {seat} --gen {gen} "
                 f"--ref {succ_ref or '<your ListAgents ref>'} diff --text -")
    return "\n".join(lines)


def run_after_join(root, *, seat: str, gen: int, startup: dict,
                   values: dict, record_path: str | None = None,
                   dry_run: bool = False, sleep_impl=None,
                   delay_override: float | None = None,
                   send_dm=None, timeout_s: int | None = None,
                   byte_cap: int | None = None) -> dict:
    """THE captive after_join first turn, performed by the SERVICE — never by
    the successor (hypothesis:l4-startup-first-turn-is-performed-by-the-
    service-and-the-hook-fires-at-turn-one, owed (i)).

    Waits `startup.after_join_delay_s` (default 20; `delay_override` wins for
    tests so nothing waits), then runs the template `startup.after_join` list
    as ONE ordered flow, writes every command's output into the rotation
    record at `record_path` (appending an `after_join` key), and sends ONE dm
    (the successor's SECOND input) through send.py's fixed nudge. `dry_run`
    resolves and plans everything but waits, runs, writes and sends NOTHING.

    `sleep_impl` (default time.sleep) and `send_dm(to, text)` (default
    send.send(root, seat, text, None)) are injectable so the fixture proves
    the delay and the dm without a real 20 s wait or a real tmux nudge.
    Returns {delay_s, results, dm, appended, record_path}. Never raises on
    record/send failure — each surfaces as a result / return field."""
    startup = startup or {}
    entries = startup.get("after_join") or []
    delay_s = (delay_override if delay_override is not None
               else int(startup.get("after_join_delay_s")
                        or DEFAULT_AFTER_JOIN_DELAY_S))
    timeout = timeout_s or (startup.get("first_turn_timeout_s")
                            or DEFAULT_AFTER_JOIN_TIMEOUT_S)
    cap = byte_cap or (startup.get("byte_cap") or DEFAULT_STARTUP_BYTE_CAP)
    if not dry_run and delay_s > 0:
        if sleep_impl is None:
            time.sleep(delay_s)
        else:
            sleep_impl(delay_s)
    results: list = []
    if dry_run:
        for e in entries:
            entry = e if isinstance(e, dict) else {"label": str(e), "cmd": str(e)}
            try:
                cmd = _resolve_startup_placeholders(
                    entry.get("cmd", ""), values, refuse_empty=False)
                results.append({"label": entry.get("label", ""),
                                "cmd": cmd, "dry": True})
            except ValueError as exc:
                results.append({"label": entry.get("label", ""),
                                "cmd": entry.get("cmd", ""),
                                "refused": str(exc)})
    else:
        for e in entries:
            results.append(_run_after_join_command(e, values, timeout, cap))
    dm = _compose_after_join_dm(
        seat, gen, values.get("succ_ref", ""), results)
    appended = False
    if not dry_run and record_path is not None:
        rp = Path(record_path)
        if rp.exists():
            try:
                rec = json.loads(rp.read_text())
                if not isinstance(rec, dict):
                    raise ValueError("record not an object")
                rec["after_join"] = {
                    "performed_by": "service",
                    "delay_s": delay_s,
                    "results": results,
                    "dm": dm,
                }
                rp.write_text(json.dumps(rec, indent=2) + "\n",
                              encoding="utf-8")
                appended = True
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                appended = False
    if not dry_run and send_dm is None:
        def send_dm(to: str, text: str) -> None:
            import send as _send
            _send.send(root, to, text, None)
    sent = False
    if not dry_run and send_dm is not None:
        send_dm(seat, dm)
        sent = True
    return {"delay_s": delay_s, "results": results, "dm": dm,
            "appended": appended, "sent": sent,
            "record_path": str(record_path) if record_path else None}


def _latest_rotate_record(root: Path, seat: str):
    """The seat's newest recorded rotation document ({..}.json) whose result
    marks a rotation that happened (started/success), or None. Best-effort
    discovery for the SERVICE: a rotation's after_join runs against the records
    rotate-self wrote."""
    try:
        pat = _rotations_dir(root) / f"{seat}.*.json"
        files = sorted(pat.parent.glob(pat.name))
    except OSError:
        return None
    for f in reversed(files):
        try:
            rec = json.loads(f.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(rec, dict) and (rec.get("result") in ("started", "success")
                                      or rec.get("rotation") in ("rotate-self",)):
            return rec, f
    return None


def run_after_join_for_seat(root, seat: str, *, now: float | None = None,
                            sleep_impl=None, send_dm=None) -> dict | None:
    """The heal.py watch loop's per-seat action: discover the seat's latest
    rotation record that has NOT yet had its captive after_join run and whose
    `after_join_delay_s` has elapsed, and run it. Returns None when nothing is
    due (best-effort, read-only discovery). `now` injectable for the fixture.
    Reads the startup template through `_resolve_template` for the seat's role
    so the SAME `after_join` list + delay the rotate-self caller would run is
    the one the service runs."""
    pair = _latest_rotate_record(root, seat)
    if pair is None:
        return None
    rec, path = pair
    if rec.get("after_join"):
        return None  # already performed
    delay_s = int((rec.get("after_join") or {}).get("delay_s")
                  or DEFAULT_AFTER_JOIN_DELAY_S)
    rec_ts = rec.get("recorded_at", "")
    if rec_ts:
        try:
            ts = datetime.strptime(rec_ts, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            try:
                ts = datetime.strptime(rec_ts, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                ts = None
        if ts is not None:
            now = now if now is not None else time.time()
            if (ts.timestamp() + delay_s) > now:
                return None  # not yet due
    row = _find_seat(root, seat)
    role = (row or {}).get("role") or "parent"
    tmpl, _name, _src = _resolve_template(root, role)
    startup = (tmpl.get("startup") if tmpl else None) or {}
    gen = rec.get("gen_after")
    values = _first_turn_values(
        root, seat=seat, gen=int(gen) if gen is not None else 0,
        succ_name=seat)
    # succ_ref best-effort from the record's handover, so the ack writes a real
    # ref when the join supplied one.
    hov = rec.get("handover") or {}
    join = hov.get("join") or {}
    sref = join.get("session_id") or ""
    if not sref:
        sr = hov.get("successor_row")
        if isinstance(sr, dict):
            sref = sr.get("session_id") or ""
    if sref:
        values["succ_ref"] = str(sref)
    return run_after_join(
        root, seat=seat, gen=int(gen) if gen is not None else 0,
        startup=startup, values=values, record_path=str(path),
        sleep_impl=sleep_impl, send_dm=send_dm, delay_override=0)


def _startup_step_list(startup) -> list:
    """The template `startup` block as an ordered (phase,label,cmd) list:
    `first_turn` entries then `after_join` entries — the order rotate-self
    runs them. A bare-string entry is its own label and command."""
    if not isinstance(startup, dict):
        return []
    steps = []
    for phase in ("first_turn", "after_join"):
        for e in startup.get(phase) or []:
            entry = (e if isinstance(e, dict)
                     else {"label": str(e), "cmd": str(e)})
            steps.append((phase, entry.get("label", ""), entry.get("cmd", "")))
    return steps


def _startup_state_path(root: Path, seat: str) -> Path:
    """`<sessions>/seats/<seat>.startup.json` — the driven walk's progress."""
    return _sessions_dir(root) / "seats" / f"{seat}.startup.json"


def _startup_signature(template_name: str, steps: list) -> str:
    """A stable fingerprint of (template, step labels). A template change
    rebuilds a stale progress file rather than mis-advancing on old indices."""
    return (template_name + "|"
            + "|".join(f"{p}:{label}" for p, label, _ in steps))


def _load_startup_state(path: Path, seat: str, sig: str,
                        step_meta: list) -> dict:
    """Read the driven-walk progress file; return a fresh all-pending state
    when absent, stale (signature changed), or malformed. State shape:
        {seat, sig, steps: [{phase,label,status} ...]}  status: ok|fail|pending
    A step is DONE only when status == "ok"."""
    def _blank():
        return {"seat": seat, "sig": sig,
                "steps": [{"phase": p, "label": l, "status": "pending"}
                           for p, l in step_meta]}
    if path.exists():
        try:
            st = json.loads(path.read_text(encoding="utf-8"))
            ok = (isinstance(st, dict) and st.get("sig") == sig
                  and isinstance(st.get("steps"), list)
                  and len(st["steps"]) == len(step_meta))
            if ok:
                for s in st["steps"]:
                    if not isinstance(s, dict) or s.get("status") not in (
                            "ok", "fail", "pending"):
                        ok = False
                        break
        except (OSError, ValueError):
            st, ok = None, False
        if ok:
            st["seat"] = seat
            return st
    return _blank()


def _startup_current(state: dict) -> int | None:
    """Index of the first step without a recorded success, or None when the
    list is exhausted (every step OK)."""
    for i, s in enumerate(state.get("steps") or []):
        if s.get("status") != "ok":
            return i
    return None


def cmd_next(args: argparse.Namespace, root: Path) -> int:
    """`rotate.py next --seat S [--record-ok|--record-fail] [--json]` — the
    OPERATOR half of the DRIVEN startup path (hypothesis:l4-startup-is-one-
    script-or-a-driven-prompt). PRINTS the next `startup` step's literal
    command (placeholders resolved) and nothing else on the default path,
    advancing only on a recorded success. NEVER runs a command."""
    if root is None:
        print("ERR: next needs an agi project root.", file=sys.stderr)
        return 1
    if getattr(args, "root", None):
        root = Path(args.root).resolve()
    seat = args.seat
    role = args.role
    if role is None:
        row = _find_seat(root, seat)
        role = (row or {}).get("role") or "parent"
    tmpl, name, _source = _resolve_template(root, role, args.template,
                                            where="next")
    if tmpl is None:
        print(f"ERR: {name}", file=sys.stderr)
        return 1
    startup = tmpl.get("startup") or {}
    step_list = _startup_step_list(startup)
    step_meta = [(p, l) for p, l, _ in step_list]
    if not step_meta:
        print(f"ERR: template {name!r} has no startup step list for seat "
              f"{seat!r} — nothing to walk", file=sys.stderr)
        return 1
    gen = (args.gen if args.gen is not None
           else _read_generation(root, seat) + 1)
    values = _first_turn_values(
        root, seat=seat, gen=gen, succ_name=args.succ_name or seat,
        tmux_session=args.tmux_session or DEFAULT_TMUX_SESSION)
    resolved = {}
    for p, l, c in step_list:
        try:
            resolved[(p, l)] = _resolve_startup_placeholders(c, values)
        except ValueError as exc:
            resolved[(p, l)] = f"ERR {exc}"
    path = _startup_state_path(root, seat)
    sig = _startup_signature(name, step_list)
    state = _load_startup_state(path, seat, sig, step_meta)
    idx = _startup_current(state)
    if args.record and idx is not None:
        state["steps"][idx]["status"] = args.record  # "ok" | "fail"
        idx = _startup_current(state)
    # persist one step's progress per call
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")
    except OSError as exc:
        print(f"ERR next: cannot persist progress {path}: {exc}",
              file=sys.stderr)
        return 1
    if idx is None:  # exhausted
        total = len(step_meta)
        if args.json:
            print(json.dumps({"seat": seat, "complete": True,
                              "steps_total": total, "steps_done": total}))
        else:
            print(STARTUP_DONE_LINE)
        return 0
    s = state["steps"][idx]
    if args.json:
        print(json.dumps({"seat": seat, "index": idx, "phase": s["phase"],
                          "label": s["label"],
                          "cmd": resolved[(s["phase"], s["label"])],
                          "steps_total": len(step_meta), "steps_done": idx,
                          "complete": False},
                         ensure_ascii=False))
    else:
        print(resolved[(s["phase"], s["label"])])
    return 0


def cmd_rotate_self(args: argparse.Namespace, root: Path) -> int:
    """The self-rotation primitive for a NON-prime seat.

    `rotate.py rotate-self --name S`: reads S's own registry row for
    role/model/effort/settings (no `--tier`), then (1) writes the seat's
    handoff with the incremented generation, (2) renames its own tmux window
    `S` aside to `S.gen<N>`, freeing the plain name, (3) spawns its successor
    under the SAME plain name (never a Roman numeral), (4) reads back the
    successor's single-word `continue` from the successor log — through the
    read-before-write cursor so a stale predecessor `continue` in the reused
    plain-name log cannot confirm it — and (5) kills its own renamed window.
    `--dry-run` prints all five steps and touches nothing."""
    if root is None:
        print("ERR: rotate-self needs an agi project root.", file=sys.stderr)
        return 1
    guard = _check_branch_guard(root)
    if guard:
        print(guard, file=sys.stderr)
        return 1
    seat = args.name
    row = None
    # A THROWAWAY seat (hypothesis:l3-rotate-self-successor-override) is a
    # rehearsal-only registration that NEVER writes seats.md: it skips the
    # registry gate the Sanctuary Master owns and builds a default row instead
    # (role from --role, default parent; model/effort/settings resolved from
    # the ladder inside spawn_window). Without --throwaway the gate holds
    # exactly as before — an unregistered name errors `no seat`.
    if not getattr(args, "throwaway", False):
        row = _find_seat(root, seat)
        if row is None:
            print(f"ERR: no seat {seat!r} in the seats registry "
                  f"(.agi/nodes/.geometry/seats.md).", file=sys.stderr)
            return 1
    else:
        row = {}  # default row; never consulted against seats.md

    # L4.112 (A): resolve the rotation template at the TOP of rotate-self,
    # BEFORE any side effect (the started record, the handoff, the own-window
    # rename). A missing / unhelpful rotations.md must refuse HERE, leaving the
    # window name and the handoff file untouched. The role is derived from the
    # seat row (identity SUPPLIED from the registry, never inferred), with
    # --role as its escape hatch for a throwaway seat.
    role = (row.get("role") if row else None) \
        or getattr(args, "role", None) or "parent"
    tmpl, tmpl_name, tmpl_src = _resolve_template(
        root, role, getattr(args, "template", None))
    if tmpl is None:
        print(f"ERR: {tmpl_src}", file=sys.stderr)
        return 1
    print(f"(0) template -> {tmpl_name!r} ({tmpl_src}) "
          f"brief={tmpl.get('brief_file')!r} "
          f"steps={tmpl.get('steps')} telemetry={tmpl.get('telemetry')}")
    # L4.112 (C): the ordered step list rotate-self runs comes from the
    # template, not from a hardcoded list. The progress markers in
    # `steps_reached` are spelled from these names where the step exists.
    tmpl_steps: list[str] = [str(s) for s in (tmpl.get("steps") or [])]

    tmux_session = args.tmux_session or DEFAULT_TMUX_SESSION
    # P1 (fifth dispatch): a NUMERAL-CHAIN seat — the prime, today the only
    # such seat (role prime_director) — derives its successor name from the
    # existing windows the way cmd_loop does (`belam-S1-L4-<next numeral>`, by
    # REUSING `_derive_successor_name` / `_split_roman_suffix`, never copied),
    # and its generation IS the numeral. The chain prefix comes from the seat
    # row's `name` (goal:g8.2); nothing here branches on any literal seat
    # string. A plain-named seat is unchanged: predecessor window `seat` ->
    # successor `seat`, `.gen<N>` own-window rename, generation = gen_before+1.
    _existing_for_chain = _existing_windows(tmux_session, args.window_path)
    is_chain_seat = (role == "prime_director")
    if is_chain_seat:
        # the predecessor's own (pre-rotation) window is the highest live
        # numeral in the chain (its numeral is the successor's minus one line)
        _chain_live = [w for w in _existing_for_chain
                       if w == seat or w.startswith(seat + "-")]
        own_chain_name = max(
            _chain_live, key=lambda w: _split_roman_suffix(w)[1],
            default=None)
        # L4.122 merge-up 24 residue (G): gen_before for a CHAIN seat comes
        # from the ROW/numeral — the predecessor's own window's line value —
        # NEVER the handoff counter. The live gen IX->X record announced
        # `0 -> 8` from a stale `_read_generation` counter; the numeral is
        # the true generation (P1: generation IS the numeral). Falls back to
        # the counter only when no chain window is live yet (a fresh prime).
        gen_before = (_split_roman_suffix(own_chain_name)[1]
                      if own_chain_name else _read_generation(root, seat))
        spawn_name = _derive_successor_name(_existing_for_chain, prefix=seat)
        _, gen = _split_roman_suffix(spawn_name)   # generation IS the numeral
        new_name = None   # .gen<N> own-window rename is plain-seat only
    else:
        gen_before = _read_generation(root, seat)
        gen = gen_before + 1
        spawn_name = seat
        own_chain_name = None
        new_name = f"{seat}.gen{gen}"
    # `pred_name` is the window that will be killed by @id at s12 after the
    # successor is confirmed: the renamed own window (plain seat) or the
    # predecessor's own numeral window (chain seat).
    pred_name = new_name if not is_chain_seat else own_chain_name
    dbg = args.debug_file or str(_sessions_dir(root) / f"{seat}.log")
    # L4.112 (D): the successor's identity from the JOIN (ListAgents `@id`),
    # SUPPLIED, never inferred. None of the identity-bearing handover writes
    # happens without it — the newest `.jsonl` in the sessions dir never
    # supplies identity.
    session_ref = (getattr(args, "session_ref", None) or "").strip()

    # A rotate-self rotation opens ONE record file up front (a `started`
    # record) and updates it IN PLACE through every step, so an interruption
    # at any point leaves a record whose `steps_reached` says where it died —
    # instead of nothing at all (hypothesis:l4-rotation-record-survives-
    # interruption). The final outcome rewrites the SAME path, so a completed
    # rotation still leaves exactly one record in today's shape.
    rec_path = None
    steps_reached: list[str] = []
    if not args.dry_run:
        rec_path = _rotate_self_started_path(root, seat)
        _write_rotate_self_started(
            rec_path, seat=seat, steps=steps_reached,
            gen_before=gen_before, gen_after=gen)

    # (1) handoff — the successor's identity travels in the handoff HEADER so
    # it wakes already knowing its own session_ref (kid-2 step 5).
    if not args.dry_run:
        _write_handoff(root, seat, gen, predecessor_session=seat,
                       session_ref=session_ref)
        _rs_mark(steps_reached, tmpl_steps, "handoff", "1")
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen)
    print(f"(1) handoff -> .agi/sessions/seats/{seat}.handoff.md "
          f"generation {gen}")

    # (2) rename own window aside, freeing the plain seat name. The `.genN`
    #     rename applies ONLY to plain-named seats (P1): a numeral-chain seat
    #     (the prime) keeps its numeral windows and is reaped by @id at s12;
    #     it records the rename as done-by-skip, never renaming a constructed
    #     name that has no window behind it (measured L4-VI: renaming 'belam'
    #     failed — the real window is belam-S1-L4-<numeral>).
    if is_chain_seat:
        if not args.dry_run:
            _rs_mark(steps_reached, tmpl_steps, "rename", "2")
            _write_rotate_self_started(rec_path, seat=seat,
                                       steps=steps_reached,
                                       gen_before=gen_before, gen_after=gen)
        print(f"(2) own-window rename: SKIPPED for numeral-chain seat "
              f"{seat!r} (`.genN` applies only to plain-named seats; the "
              f"own-window reap is GATED OFF at step (8) on a numeral- "
              f"chain seat; the ONLY reap is the Belam FIFO cap (r5) when "
              f"the chain would exceed FIVE)")
    else:
        if not args.dry_run:
            _rename_own_window(seat, new_name, tmux_session, args.window_path)
            _rs_mark(steps_reached, tmpl_steps, "rename", "2")
            _write_rotate_self_started(rec_path, seat=seat,
                                       steps=steps_reached,
                                       gen_before=gen_before, gen_after=gen)
        print(f"(2) rename own window {seat!r} -> {new_name!r}")

    # (2.5) STARTUP first_turn (hypothesis:l4-startup-is-one-script-or-a-
    #     driven-prompt, 0b round) — resolve and (unless dry-run) RUN each
    #     template `startup.first_turn` command BEFORE spawn, one at a time,
    #     allowlisted / placeholder-resolved / timed / byte-capped, then
    #     compose the successor's `## STARTUP OUTPUT` block so it lands at
    #     wake holding its telemetry (rotation record, seat row, authority,
    #     git state, inbox, live spawns) — the successor runs nothing.
    startup = tmpl.get("startup") if tmpl else None
    startup_values = _first_turn_values(
        root, seat=seat, gen=gen, succ_name=spawn_name,
        succ_ref=session_ref,
        succ_transcript=getattr(args, "successor_transcript", None) or "",
        tmux_session=tmux_session)
    first_turn_results = _run_first_turn_commands(
        startup or {}, startup_values, dry_run=args.dry_run)
    startup_block = _compose_startup_output(first_turn_results)
    if first_turn_results:
        mode = "DRY-RUN -- nothing executed" if args.dry_run \
            else "output composed for the successors first turn"
        print(f"(2.5) startup first_turn: {len(first_turn_results)} "
              f"command(s) resolved; {mode}")

    # (3) spawn the successor under the SAME plain name - never a Roman numeral
    # L4.112 (C): the template is consumed on the existing call path -- when
    # --prompt-file is NOT given, the successor prompt is the template's
    # brief_file with `{seat}` substituted (the director's brief is the seat's
    # QUORUM scratchpad, .agi/sessions/quorum/{seat}.md); --prompt-file still
    # overrides. The consume-path applies on a REAL spawn: a dry-run is a
    # refusal/planning check (the top print already shows brief=), and the
    # template tests are hermetic -- their brief paths are not materialised.
    # The real spawn is where the file-existence gate in spawn_window lives.
    prompt_file = args.prompt_file
    if (not args.dry_run and prompt_file is None
            and tmpl is not None and tmpl.get("brief_file")):
        prompt_file = str(tmpl["brief_file"]).replace("{seat}", seat)
    ack_gate = (
        "ROTATION CONTINUATION: acknowledge your handoff with the explicit "
        "ACK channel, not a bare word. First act after reading your handoff: "
        f"run `python3 extensions/agi/bin/rotate.py ack --seat {seat} "
        f"--gen {gen} --ref <your own ListAgents ref> continue` if the handoff "
        "needs no change, or `... diff --text '<the exact diff>'` if it does. "
        "The predecessor's read-back reads THAT ack and refuses an ack whose "
        "gen_after is not this generation."
    )
    extra = ack_gate + ("\n\n" + startup_block if startup_block else "")

    # (2.75) PRE-SPAWN VERIFICATION + BOOTSTRAP (hypothesis:l4-startup-first-
    #     turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one).
    #     The bootstrap record must EXIST at turn one: the SessionStart hook
    #     COPY (cc-session-start.next.sh) keys its injection on the record's
    #     presence, and it can only fire at turn one if the record is on disk
    #     BEFORE the claude successor starts. Every fact knowable pre-spawn
    #     (seat, generation, the rotation template's telemetry facts, the HEAD
    #     commit, the verification result) is written NOW; the join-only facts
    #     (BOOTSTRAP_JOIN_ONLY_FACTS — successor's live model vs its row, its
    #     @id address, the model_refusal_fallback) carry the explicit
    #     `pending: resolved after join` marker — never a blank, never a
    #     `SKIPPED: <predecessor owns>` reason. Verification is tree-wide and
    #     independent of the successor, so it runs ONCE here (moved from s11)
    #     and is reused for both writes. After the join, s11 REWRITES the same
    #     record with the joined facts resolved.
    if args.dry_run:
        # dry-run stays a refusal/planning check: no verification subprocess,
        # no bootstrap write (turn-one proof is a live/fixture property).
        verification = None
    elif (args.window_path is not None
          and getattr(args, "verification_argv", None) is None):
        verification = {"ok": False, "level": VERIFICATION_LEVEL,
                        "skipped": "SKIPPED: fixture, real verification "
                                    "deferred (no graph; "
                                    "--verification-argv seam absent)"}
    else:
        verification = _run_verification(
            root, argv=getattr(args, "verification_argv", None))
    if not args.dry_run:
        _write_bootstrap(
            root, seat=seat, generation=gen,
            telemetry=tmpl.get("telemetry"), verification=verification,
            join_pending=set(BOOTSTRAP_JOIN_ONLY_FACTS))

    rc, _ = spawn_window(
        name=spawn_name, tier=role,
        prompt_file=prompt_file,
        model=args.model or ((row.get("model") if row else None) or None),
        effort=args.effort or ((row.get("effort") if row else None) or None),
        settings=(json.loads(args.settings) if args.settings
                  else _normalize_settings(row.get("settings") if row
                                           else None)),
        tmux_session=tmux_session, window_path=args.window_path, root=root,
        dry_run=args.dry_run, debug_file=dbg, extra=extra, seat=seat,
        successor_argv=getattr(args, "successor_argv", None),
    )
    if rc != 0:
        return rc
    if not args.dry_run:
        _rs_mark(steps_reached, tmpl_steps, "spawn", "3")
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen)
    print(f"(3) spawn successor under the "
          f"{'numeral-chain name' if is_chain_seat else 'plain name'} "
          f"{spawn_name!r} (role {role!r})")

    if args.dry_run:
        # L4.118 (R1) — the dry-run ENUMERATES every step live would execute,
        # derived the same way the live call derives it, touching NOTHING (no
        # write, no spawn, no kill; only read-only git/tmux reads for the
        # informational lines). The @id values themselves are only knowable
        # live, so the mechanism that captures them is what is spelled.
        if first_turn_results:
            print("(2.5) startup first_turn (resolved, NOTHING run):")
            for r in first_turn_results:
                if r.get("refused"):
                    state = "REFUSED: " + r["refused"]
                elif r.get("dry"):
                    state = "dry-run"
                else:
                    state = f"exit {r.get('rc')}"
                print(f"    [{r.get('label', '')}] {state}: {r.get('cmd', '')}")
        print("(4) read back successor reply — pending ack channel ->")
        print(f"    pending ack path: {_ack_path(root, seat)}")
        print("    (the successor's own `rotate.py ack --seat "
              f"{seat} --gen {gen}` flips it continue/diff; a diff leaves "
              "the renamed window for inspection)")
        print("(5) successor-window guarantee: tmux list-windows must show "
              f"the {'numeral-chain' if is_chain_seat else 'plain'} name "
              f"{spawn_name!r}")
        print("    join: follow the successor's window @id into the "
              f"registry dir "
              f"{getattr(args, 'registry_dir', None) or REGISTRY_DEFAULT_DIR}; "
              "match the FILE whose tmux @id is that @id (never a session "
              "prefix, never the newest .jsonl — identity is SUPPLIED)")
        print("    successor row fields:"
              " [session_ref, session_id, generation, window, pid] "
              "source: registry")
        print("    model confirm: expected="
              f"{((row.get('model') if row else None) or args.model)!r} "
              "requested=`ps -o args=` after the first `--model`; "
              "live='model' in the successor transcript")
        print("    meter pin: the successor transcript from the JOIN")
        print("    handoff identity: successor session_id written to the "
              "handoff header")
        print("(6) release own authority ", end="")
        print(f"(generation {gen_before} -> {gen}); ack record written pending")
        print(f"    bootstrap record: "
              f"{_sessions_dir(root) / 'seats' / f'{seat}.bootstrap.json'}  "
              f"telemetry={tmpl.get('telemetry')}")
        print(f"    verification: verification.py --level {VERIFICATION_LEVEL}")
        print("(7) button-down: commit the record+row + `grid.py commit "
              "--all` where legal")
        print(f"    grid legality on THIS branch: "
              f"{_button_down_legal_hint(root)}")
        print("    livestream re-point: view-<seat> select-window BY the "
              "successor @id")
        print(f"(8) s12 self-reap: own window @id -> pane_pid -> "
              f"`ps -e` descendants, TERM'd DEEPEST-FIRST "
              "(rotate.py's own pid and its direct shell parent EXCLUDED), "
              "KILL survivors, then the own window by @id; a numeral-chain "
              "seat GATES this off (owner chain rule) and the Belam FIFO "
              "cap reaps the OLDEST instead")
        print("    own @id it would capture: tmux display-message -p "
              "'#{window_id}' (knowable only live)")
        print("    successor @id capture: tmux new-window -P -F '#{window_id}' "
              f"under the {'numeral-chain' if is_chain_seat else 'plain'} name "
              f"{spawn_name!r}")
        if is_chain_seat:
            print(f"(dry-run) numeral-chain seat: successor name "
                  f"{spawn_name!r}, generation = numeral {gen}, own window "
                  "@id = tmux display-message -p '#{window_id}' "
                  "(knowable only live), ack path "
                  f"{_ack_path(root, seat)}")
            # (r5 dry-run) the Belam FIFO cap -- the ONE reap a numeral-
            #     chain seat runs. NAMED live-derived, read-only: the
            #     OLDEST predecessor window when the chain would exceed
            #     FIVE, its @id, its pane pid and the ps -e chain it would
            #     TERM deepest-first. Touches nothing. Same call path the
            #     live r5 uses (`_belam_oldest` over the live windows + the
            #     spawn_name successor; `_pane_pid(@id)` -> `_descendant_chain`).
            pfx = getattr(args, "belam_prefix", None) or "belam"
            oldest = _belam_oldest(_existing_for_chain, spawn_name, pfx)
            if oldest is None:
                print(f"    (r5) Belam FIFO cap: chain stays at/below FIVE "
                      f"live {pfx!r} windows -> no reap (the own-window "
                      f"reap is GATED OFF on a numeral-chain seat)")
            else:
                oldest_id = _successor_window_id(
                    oldest, tmux_session, args.window_path)
                print(f"    (r5) Belam FIFO cap WOULD reap the OLDEST "
                      f"predecessor {oldest!r} (@id {oldest_id})")
                pane_pid = (_pane_pid(oldest_id) if oldest_id else None)
                if not pane_pid:
                    print(f"        SKIPPED: no pane pid for window "
                          f"{oldest!r} (@id {oldest_id}); the Belam FIFO "
                          f"cap could not derive its chain (a live tmux "
                          f"run reads `tmux display-message -p -t @id "
                          f"#{{pane_pid}}` -> `ps -e` climb)")
                else:
                    chain = _descendant_chain(pane_pid)
                    if not chain:
                        print(f"        SKIPPED: no ps -e chain under pane "
                              f"pid {pane_pid} for {oldest!r}; nothing to "
                              f"reap")
                    else:
                        print(f"        pane pid {pane_pid} -> ps -e chain "
                              f"{chain!r}, TERM'd DEEPEST-FIRST, then the "
                              f"window killed by @id")
        else:
            print("(dry-run) ends on the PLAIN seat name; "
                  f"generation: {gen} (never a Roman numeral)")
            # (r4/s12 dry-run) the OWN-window/OWN-chain reap a plain seat
            #     WOULD run. NAMED live-derived, read-only. The @id is
            #     resolved from the CURRENT `<seat>` window, NEVER from the
            #     rename target `<seat>.genN` = pred_name: a tmux
            #     `rename-window` PRESERVES the window's @id, and the .genN
            #     name does not exist YET at dry-run time (step (2) will
            #     create it by renaming the live `<seat>` window), so
            #     resolving from pred_name always yields None.
            own_id = _successor_window_id(seat, tmux_session,
                                          args.window_path)
            print(f"    (r4/s12) own-window reap WOULD kill {pred_name!r} "
                  f"(@id {own_id}) — the rename of the current "
                  f"{seat!r} window (rename preserves the @id)")
            pane_pid = (_pane_pid(own_id) if own_id else None)
            if not pane_pid:
                print(f"        SKIPPED: no pane pid for {seat!r} "
                      f"(@id {own_id}) naming what becomes {pred_name!r}; "
                      f"the own-chain reap could not derive it (a live run "
                      f"reads `tmux display-message -p -t @id "
                      f"#{{pane_pid}}` -> `ps -e` climb)")
            else:
                chain = _descendant_chain(pane_pid)
                if not chain:
                    print(f"        SKIPPED: no ps -e chain under pane pid "
                          f"{pane_pid} for {seat!r}; nothing to reap")
                else:
                    print(f"        pane pid {pane_pid} -> ps -e chain "
                          f"{chain!r}, TERM'd DEEPEST-FIRST, then the "
                          f"window killed by @id")
        # (0b-b owed (i)) after_join dry-run: the template's `after_join` list
        # is ENUMERATED (resolved, NOTHING run, no delay, no record write, no
        # dm) so a caller sees exactly what the service/rotate-self will run
        # after spawn. The captive copy-paste line is printed as the decision
        # the successor would receive.
        if startup:
            plan = run_after_join(root, seat=seat, gen=gen,
                                  startup=startup, values=startup_values,
                                  dry_run=True,
                                  record_path=str(rec_path) if rec_path else None)
            print(f"(9) after_join dry-run: {len(plan['results'])} command(s) "
                  f"resolved after a {plan['delay_s']}s delay; NOTHING run, no "
                  f"dm sent")
            for r in plan["results"]:
                state = "REFUSED: " + r["refused"] if r.get("refused") \
                    else "dry-run"
                print(f"    [{r.get('label', '')}] {state}: {r.get('cmd', '')}")
            print("    captive dm decision line (the successor's SECOND input):")
            print(f"    python3 extensions/agi/bin/rotate.py ack --seat {seat} "
                  f"--gen {gen} --ref <your ListAgents ref> diff --text -")
        return 0

    # (4) SUCCESSOR-WINDOW GUARANTEE: a NEW tmux window must exist under the
    #     reused PLAIN seat name, established by tmux list-windows and NEVER
    #     by spawn_window's return value (which has previously reported a
    #     successful rotation and spawned no window at all). Refuse to report
    #     success when it is absent.
    succ = _observed_windows(tmux_session, args.window_path)
    if spawn_name not in succ["names"]:
        pred_o = _observed_windows(tmux_session, args.window_path)
        _write_rotation_record(root, _rotate_self_record(
            seat=seat, result="refused", gen_before=gen_before, gen_after=gen,
            succ=succ, pred={"name": pred_name, "windows": pred_o["names"],
                             "source": pred_o["source"]},
            readback_log=Path(dbg).expanduser().resolve(),
            cursor_offset=(Path(dbg).expanduser().resolve().stat().st_size
                           if Path(dbg).expanduser().resolve().exists() else 0),
            refusal="successor window absent"), path=rec_path)
        print(f"ERR: successor window {spawn_name!r} is NOT present in tmux "
              f"session {tmux_session!r}; refusing to report rotation success "
              f"(windows: {succ['names']!r}).", file=sys.stderr)
        return 1

    # L4.114 THE HANDOVER. Identity-bearing successor-lifecycle writes, every
    # one recorded. Identity comes from the registry JOIN (s4) by the
    # successor's WINDOW @id — or, under test, from an internally-supplied
    # `session_ref` seam (argparse no longer exposes --session-ref; tests
    # inject it via the SimpleNamespace they build). Gate: identity must be
    # AVAILABLE — either the seam or a captured successor window @id. With
    # neither (a plain-name fixture, no identity) the handover records only
    # the window identities and the rotation still succeeds as before. When a
    # JOIN is ATTEMPTED but finds no registry file, the rotation is NOT a
    # success — it is recorded `skipped` naming `registry file for @<id>`
    # (proof a). Every step writes its own evidence; any skipped step makes
    # the result something other than success.
    handover: dict = {}
    succ_window_id = _successor_window_id(
        spawn_name, tmux_session, args.window_path)
    # (s2) record BOTH own and successor window identities (name + @id); the
    #      @id is what a later rename/kill-by-@id (s12, kid 2) will address.
    #      For a chain seat the own window is the predecessor's numeral window
    #      (pred_name), never a constructed `.genN` name.
    handover["own_window"] = {
        "name": pred_name,
        "id": (_successor_window_id(pred_name, tmux_session, args.window_path)
               if pred_name else None)}
    handover["successor_window"] = {"name": spawn_name, "id": succ_window_id}

    succ_session_id = None
    succ_pid = None
    succ_transcript = getattr(args, "successor_transcript", None)
    joined = None
    if session_ref:
        # internal seam: identity supplied directly; no registry JOIN.
        succ_session_id = session_ref
    elif succ_window_id:
        joined = _join_successor(
            root=root, seat=seat, window_id=succ_window_id,
            registry_dir=getattr(args, "registry_dir", None),
            poll_secs=getattr(args, "registry_poll", None))
        if joined["found"]:
            succ_session_id = joined["session_id"] or session_ref
            succ_pid = joined["pid"]
            if not succ_transcript and joined["transcript"]:
                succ_transcript = joined["transcript"]
            succ_name = joined["name"] or seat
        else:
            succ_session_id = None

    identity_available = bool(session_ref) or bool(succ_window_id)
    if identity_available and not (joined is not None and not joined["found"]):
        if session_ref:
            handover["join"] = {"source": "seam",
                                "note": "identity supplied by internal seam"}
        else:
            handover["join"] = joined
        # (s6.1) write the successor's config:seats ROW via `write.py submit`.
        #     Admitted by the self_row DATA declaration (L4.110/r3); a
        #     THROWAWAY seat has no registry row, so this records 'skipped',
        #     never writes seats.md.
        try:
            handover["successor_row"] = _successor_row_write(
                root, actor=seat, seat=seat, role=role,
                # merge-up 24 residue (W): the row's `window` cell is the
                # WINDOW @id (the successor's tmux @id, so send.py
                # `_nudge_window` can address it without the name-resolution
                # hazard of L4.120 claim-3), NOT the window NAME — falling
                # back to the name only when no @id was captured (the
                # internal session_ref seam has no @id).
                window=succ_window_id or spawn_name,
                # r3 (seventh dispatch): the row's `session_ref` is the
                # ListAgents ref, NEVER the uuid (rotate.py:3818). The uuid
                # lives in `session_id`; the ListAgents ref is not derivable,
                # so until the successor's `ack --ref` back-fills it, the
                # cell stays EMPTY — never the uuid.
                session_ref="",
                pid=succ_pid, session_id=succ_session_id,
                generation=gen)
        except Exception as exc:  # noqa: BLE001
            handover["successor_row"] = f"FAILED: {exc}"
        # (s5, deferred to the post-ack success path — r1): model_confirm
        # runs AFTER the ack confirms a successor ASSISTANT TURN exists, or
        # reads argv only — NEVER a read of the successor transcript before
        # its first turn. Computed just before the record write (the X->XI
        # record: `skipped: no assistant turn in the successor transcript`).
        # (s6.2) pin the successor's meter at ITS OWN transcript — never the
        #     newest .jsonl.
        if succ_transcript:
            handover["meter_pin"] = _pin_successor_meter(
                root, seat=seat, generation=gen,
                transcript=str(succ_transcript))
        else:
            handover["meter_pin"] = ("skipped: no successor transcript "
                                      "from the JOIN")
        # (s6.3) write the ACK as `pending`, carrying the machine identity —
        #     the SUCCESSOR flips it to continue/diff. NEVher pre-write
        #     `continue`: an unflipped pending ack confirms nothing.
        try:
            handover["ack_written"] = str(_write_ack(
                root=root, seat=seat, gen_after=gen,
                session_ref=succ_session_id, answer="pending"))
        except Exception as exc:  # noqa: BLE001
            handover["ack_written"] = f"FAILED: {exc}"
        # (s6.4) release own authority. config:seats self_row fields are
        #     [session_ref, session_id, generation, window, pid] — there is no
        #     `retired` field, so the predecessor generation is retired by
        #     RECORD here.
        handover["own_authority_released"] = (
            f"generation {gen_before} of seat {seat!r} retired; successor "
            f"generation {gen} owns it (release by RECORD: the config:seats "
            "self_row schema has no retired field)")
        # (s6.5) reap our own process by PID — an EXPLICIT STAND-IN (internal
        #     seam; the CLI flag is gone). Real own pids are never reaped
        #     here.
        own_pid = getattr(args, "own_pid", None)
        if own_pid:
            handover["reap_own_pid"] = _reap_pid(int(own_pid))
        else:
            handover["reap_own_pid"] = {
                "pid": None, "reaped": False,
                "note": "no own-pid stand-in supplied; the predecessor's "
                        "process is NOT reaped by this run"}
        # (s6.6) Belam cap: a prime_director keeps the predecessor chain
        #     exactly five deep — reap the OLDEST when a sixth would exist.
        if role == "prime_director" or getattr(args, "belam_prefix", None):
            pfx = getattr(args, "belam_prefix", None) or "belam"
            # merge-up 24 residue (B): count the SUCCESSOR (spawn_name — the
            # numeral window that is actually live), not the SEAT base.
            # Passing `seat` over-counts the chain by one: the bare base name
            # is treated as a live chain window even when only the numeral
            # windows exist, inflating the Belam cap. spawn_name == seat for
            # a plain seat, so plain-seat behaviour is unchanged.
            oldest = _belam_oldest(succ["names"], spawn_name, pfx)
            handover["belam_cap"] = {
                "prefix": pfx, "would_exceed_five": oldest is not None,
                "oldest_to_reap": oldest,
                "live_belam": sorted(
                    w for w in succ["names"]
                    if w == pfx or w.startswith(pfx + "-"))}
        _rs_mark(steps_reached, tmpl_steps, "handover", "4.5")
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen)
    elif joined is not None and not joined["found"]:
        # The JOIN was ATTEMPTED and no registry file matched the successor's
        # window @id: the rotation is NOT a success. Record `skipped` naming
        # `registry file for @<id>` (proof a).
        _write_rotation_record(root, _rotate_self_record(
            seat=seat, result="skipped",
            gen_before=gen_before, gen_after=gen,
            succ=succ, handover=handover,
            readback_log=Path(dbg).expanduser().resolve(),
            refusal=joined["note"]), path=rec_path)
        print(f"ERR: {joined['note']}; rotation NOT reported success.",
              file=sys.stderr)
        return 1

    # (5) read back. Record the successor log's size BEFORE the spawn
    #     completed so the read cursor ignores anything (a stale `continue`)
    #     written before the successor started (read-before-write cursor).
    if not args.dry_run:
        _rs_mark(steps_reached, tmpl_steps, "readback", "4")
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen)
    log = Path(dbg).expanduser().resolve()
    offset = log.stat().st_size if log.exists() else 0
    timeout = getattr(args, "timeout", 600)
    # The explicit ACK channel is the ONLY read-back
    # (hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-design):
    # the successor writes its ack with its OWN gen_after, which we REFUSE if
    # it is not the generation we spawned. An acked `continue` confirms the
    # rotation; an acked `diff` means the handoff needs change and the own
    # window lives for inspection. The legacy debug-log read is DELETED, not
    # kept as a fallback (a debug logger cannot carry prose).
    ack = _read_ack(_ack_path(root, seat), gen_after=gen, timeout=timeout)
    acked_continue = False
    if ack is not None and ack.get("answer") == "continue":
        acked_continue = True
    elif ack is not None and ack.get("answer") == "diff":
        _write_rotation_record(root, _rotate_self_record(
            seat=seat, result="diff", gen_before=gen_before, gen_after=gen,
            succ=succ, readback_log=Path(_ack_path(root, seat)).expanduser(),
            refusal="successor acked diff: handoff needs change"), path=rec_path)
        print("successor acked diff (handoff needs change); leaving the "
              "renamed window in place for inspection.", file=sys.stderr)
        return 1

    # Three realities (ACKED / PRESENT-BUT-SILENT / ABSENT): the window was
    # confirmed present above and no ack arrived -> PRESENT-BUT-SILENT, the
    # (w3) decision record: SUCCEEDED BUT UNWITNESSED, never confirmed. A
    # rotation that actually succeeded (window live, successor working) must
    # not freeze at `started` -- write the terminal record here.
    if not acked_continue:
        if not args.dry_run:
            _write_rotation_record(root, _rotate_self_record(
                seat=seat, result="unwitnessed", gen_before=gen_before, gen_after=gen,
                succ=succ, readback_log=log, cursor_offset=offset,
                refusal=("successor did not ACK; window present but silent; "
                         "rotation SUCCEEDED BUT UNWITNESSED")), path=rec_path)
        print("warn: successor did not ACK (window present but silent); "
              "leaving the renamed window in place for inspection.",
              file=sys.stderr)
        return 1

    # (5) PREDECESSOR-SURVIVAL GUARANTEE: the predecessor window (renamed
    #     aside to new_name) must still exist AFTER the successor is confirmed
    #     — a rotation that silently killed its predecessor would destroy the
    #     Belam chain in the direction nobody notices until they need it.
    #     Refuse to report success when it is gone.
    pred_raw = _observed_windows(tmux_session, args.window_path)
    pred = {"name": pred_name, "windows": pred_raw["names"],
            "source": pred_raw["source"]}
    pred_alive = (pred_name is not None) and (pred_name in pred_raw["names"])
    if not pred_alive:
        _write_rotation_record(root, _rotate_self_record(
            seat=seat, result="refused", gen_before=gen_before, gen_after=gen,
            succ=succ, pred=pred, readback_log=log, cursor_offset=offset,
            # merge-up 24 residue (P): the refusal record names pred_name
            # (the real predecessor window being reaped), never the
            # constructed new_name (.genN — None on a chain seat).
            refusal=f"predecessor window {pred_name!r} gone"), path=rec_path)
        print(f"ERR: predecessor window {pred_name!r} is NOT present in tmux "
              f"session {tmux_session!r}; refusing to report rotation "
              f"success (windows: {pred_raw['names']!r}).",
              file=sys.stderr)
        return 1

    # (5.5) s8 BUTTON-DOWN: commit the record+row grid-commit, ONLY where
    #     legal. On a fixture (no git repo) this RECORDS the skip and runs no
    #     grid commit/push — the test proves the SKIPPED wording.
    if not args.dry_run:
        handover["button_down"] = _button_down(
            root=root, branch_allow=getattr(args, "grid_commit_legal", True),
            legal_branch=getattr(args, "grid_commit_branch", None))

    # (s9) re-point the livestream views to the successor's window @id.
    handover["livestream_repoint"] = _repoint_livestream_views(
        tmux_session=tmux_session, seat=seat, succ_id=succ_window_id,
        window_path=args.window_path,
        view_path=getattr(args, "view_path", None))
    # (s11) POST-JOIN BOOTSTRAP REWRITE (hypothesis:l4-startup-first-turn-
    #     is-performed-by-the-service-and-the-hook-fires-at-turn-one). The
    #     record was WRITTEN pre-spawn (step 2.75) so the hook finds it at
    #     turn one; this UPDATES the SAME path in place (never re-minted)
    #     with the @id-join facts now resolved, so the join-only markers
    #     (`pending: resolved after join`) become real values. Verification
    #     was computed pre-spawn and is reused — it never runs twice.
    # (s5) model_confirm first — computed AFTER the successor's ack confirmed
    #     an ASSISTANT TURN exists (r1): REQUESTED from `ps -o args=` after the
    #     first `--model`; LIVE from the first `"model":"..."` in the
    #     successor transcript. Never a read of the transcript before a first
    #     turn (the X->XI record said `skipped: no assistant turn`). The live
    #     model is one of the join-resolved bootstrap facts.
    handover["model_confirm"] = _confirm_successor_model(
        seat=seat,
        expected_model=((row.get("model") if row else None) or args.model),
        expected_effort=((row.get("effort") if row else None)
                         or args.effort),
        pid=succ_pid, transcript=succ_transcript)

    overrides: dict = {}
    succ_wid = handover.get("successor_window", {}).get("id")
    if succ_wid:
        overrides["successor_address"] = str(succ_wid)
    mc = handover.get("model_confirm")
    if isinstance(mc, dict) and mc.get("live"):
        overrides["successor_live_model"] = str(mc["live"])
    handover["bootstrap"] = _write_bootstrap(
        root, seat=seat, generation=gen,
        telemetry=tmpl.get("telemetry"), verification=verification,
        join_pending=(set(BOOTSTRAP_JOIN_ONLY_FACTS) - set(overrides)),
        overrides=overrides)

    # (6) the record is the deliverable — write it, durably, BEFORE the own
    #     window is killed, so it survives regardless of what the kill does.
    record_path = _write_rotation_record(root, _rotate_self_record(
        seat=seat, result="success", gen_before=gen_before, gen_after=gen,
        succ=_observed_windows(tmux_session, args.window_path),
        pred=pred, readback_log=log, cursor_offset=offset,
        handover=handover, steps_reached=steps_reached), path=rec_path)

    # (6.4) THE SERVICE performs the captive after_join first turn (0b-b owed
    #     (i)). rotate-self is the FALLBACK performer when NO persistent
    #     service runs (`agent_dispatch.inline_reaper` truthy = the reaper runs
    #     inline in dispatch, so no heal.py watch owns after_join). When the
    #     watch loop IS the service (inline_reaper false — the live box),
    #     rotate-self leaves after_join to it and says so. A fixture forces
    #     the fallback via `--after-join` (getattr) without touching config.
    aj = None
    _force_aj = bool(getattr(args, "after_join", False))
    if not _inline_reaper_enabled(root) and not _force_aj:
        print("(6.4) after_join deferred to the persistent service "
              "(agent_dispatch.inline_reaper=false)")
    else:
        # joined facts re-resolved for the after_join values (the successor
        # identity is known only now).
        aj_values = _first_turn_values(
            root, seat=seat, gen=gen, succ_name=spawn_name,
            succ_ref=succ_session_id or "",
            succ_transcript=succ_transcript or "",
            tmux_session=tmux_session)
        aj = run_after_join(
            root, seat=seat, gen=gen, startup=startup or {},
            values=aj_values, record_path=str(record_path))
        print(f"(6.4) after_join performed by rotate-self (fallback): "
              f"{len(aj['results'])} command(s) after a {aj['delay_s']}s "
              f"delay; record appended: {aj['appended']}, dm sent: "
              f"{aj['sent']}")

    # (6.5) the rotation succeeded: announce it to every live seat NOW, at
    #     the same moment the record was written, BEFORE the own-window kill
    #     (L3.39 ordering — evidence and announcement both survive cleanup).
    import send  # local: same dir
    _announce_rotation(
        root=root,
        croot=send.comms_root(root, getattr(args, "comms_root", None)),
        seat=seat, successor=spawn_name, gen_before=gen_before, gen_after=gen,
        trigger=getattr(args, "trigger", "rotate-self"),
        handoff_path=str(_sessions_dir(root) / "seats" / f"{seat}.handoff.md"),
        in_flight=getattr(args, "in_flight",
                          f"successor {seat} confirmed; gen {gen}"),
        live_names=succ.get("names", []))

    # (7) s12 LAST ACT — the LIVE SELF-REAP (L4.118/R2; SEVENTH dispatch
    #     r4 / e / D / r5): after the record is written and (6.5) announced:
    #   r4  the OWN chain is derived from the seat OWN window @id
    #       (own_window_id, captured at s2 / the row's window cell) ->
    #       `tmux display-message -p -t @id '#{pane_pid}'` -> `ps -e` climb;
    #       $TMUX_PANE only when no @id is known; the reap text names the
    #       source that fed it;
    #   e   the s12_self_reap evidence is written PLANNED (durable, same
    #       file) BEFORE the first TERM — a SUCCESSFUL own-chain reap TERMs
    #       rotate.py's own process, so a post-hoc write was unreachable and
    #       success and evidence were mutually exclusive (live X->XI leaked
    #       no s12 key at all). A best-effort update overwrites it with the
    #       observations after;
    #   D   on a numeral-chain seat the OWN window and OWN chain are NEVER
    #       killed (the owner chain rule keeps the five newest predecessors
    #       idle in their windows); the own-window kill + own-chain reap stay
    #       for plain-named seats only;
    #   r5  when the Belam chain would exceed FIVE the cap reaps the OLDEST
    #       by PID and kills ITS window by @id (`_reap_belam_oldest`) — the
    #       one reap that DOES run on a chain seat.
    _shield_old = _shield_final_signals()
    own_window_id = handover.get("own_window", {}).get("id")
    oldest_to_reap = handover.get("belam_cap", {}).get("oldest_to_reap")

    # the PLANNED s12 evidence — written BEFORE the first TERM (e).
    s12_reap: dict = {"order": "deepest-first", "planned": True}

    # (r5) Belam FIFO cap: the one reap on a chain seat, the cap reap for any
    #     --belam-prefix seat. Its evidence lands in s12_self_reap.belam_reap.
    belam_reap = None
    if oldest_to_reap:
        belam_reap = _reap_belam_oldest(
            tmux_session=tmux_session, oldest=oldest_to_reap,
            window_path=args.window_path,
            pids=getattr(args, "belam_pids", None),
            s12_reap=s12_reap, record_path=record_path)
        # L4.150: the planned belam-cap entry was already written (inside
        # _reap_belam_oldest) BEFORE the first TERM; the observed entry is
        # now folded into s12_reap best-effort as well.
        _record_s12_self_reap(record_path, s12_reap)

    if is_chain_seat:
        # (D) the own window + own chain kill are GATED OFF on a numeral-
        #     chain seat (the owner chain rule keeps the five newest
        #     predecessors idle in their windows). The ONLY reap is the Belam
        #     FIFO cap above.
        s12_reap.update({
            "gated": "own window + own chain kill GATED OFF on a "
                     "numeral-chain seat (owner chain rule keeps the five "
                     "newest predecessors idle in their windows)",
            "own_window_id": own_window_id,
            "own_chain_reap": "GATED OFF",
        })
        _record_s12_self_reap(record_path, s12_reap)
        outcome = (f"reaped the OLDEST "
                   f"{oldest_to_reap!r}" if belam_reap
                   else "no Belam cap reap")
        print(f"(7) numeral-chain seat {seat!r}: own window "
              f"{own_window_id!r} + own chain NOT killed (owner chain "
              f"rule); {outcome}")
    else:
        # r4: derive the OWN chain source — the seat OWN window @id -> pane
        #     pid first, then $TMUX_PANE only when no @id is known. Every
        #     outcome names the source that fed the skip (L4.122 criterion 3:
        #     a skip NAMES the missing input).
        own_chain_seam = getattr(args, "own_chain", None)
        src_name = None
        pane_pid = None
        if own_chain_seam:
            own_chain = [int(p) for p in own_chain_seam]
            reap_source = f"test seam (--own-chain): pid {own_chain[0]}"
        else:
            if own_window_id:
                pane_pid = _pane_pid(own_window_id)
                src_name = f"own window @id {own_window_id}"
            if pane_pid is None and os.environ.get("TMUX_PANE"):
                pane_pid = _pane_pid(os.environ.get("TMUX_PANE"))
                src_name = f"$TMUX_PANE {os.environ.get('TMUX_PANE')}"
            if pane_pid:
                own_chain = _derive_own_chain(pane_pid)
                if own_chain:
                    reap_source = (f"derived from {src_name} pane "
                                   f"{pane_pid}: chain {own_chain} "
                                   "(deepest-first)")
                else:
                    own_chain = []
                    reap_source = (f"SKIPPED: own pid {os.getpid()} not under "
                                   f"pane pid {pane_pid} from {src_name}; no "
                                   "chain to TERM")
            else:
                own_chain = []
                keep = (f" (source: {src_name} gave no pane pid; "
                        "TMUX_PANE absent, no seam)")
                reap_source = ("SKIPPED: no pane pid" + keep
                               + "; the live predecessor chain is reaped "
                                 "externally by PID (Belam cap / prime)")
        # e: write the PLANNED entry (derived chain + source) BEFORE the
        #     first TERM; update best-effort with the observations after.
        s12_reap["chain"] = own_chain
        s12_reap["reap_source"] = reap_source
        _record_s12_self_reap(record_path, s12_reap)
        ps_after: list = []
        if own_chain:
            observed = _reap_chain(own_chain)
            s12_reap.update(observed)     # best-effort observations after
            _record_s12_self_reap(record_path, s12_reap)
            ps_after = [_short_ps(p) for p in own_chain]
        else:
            s12_reap["skipped"] = reap_source
            _record_s12_self_reap(record_path, s12_reap)
        print(f"(7) successor confirmed `continue`; own chain "
              f"reap [{reap_source}]: "
              f"{s12_reap.get('chain', s12_reap.get('skipped'))}")
        print(f"    ps after: {ps_after or '(no chain derived/reaped)'}")
        _kill_window(pred_name, tmux_session, args.window_path,
                     window_id=own_window_id)
        print(f"    predecessor window list: "
              f"{_observed_windows(tmux_session, args.window_path)['names']!r}")
    print(f"rotation recorded: {record_path}")
    _restore_shield_signals(_shield_old)
    return 0


# --- harvest-table (hypothesis:harvest-table-subcommand) ------------------


def _git_out(cwd: Path, *args: str) -> str:
    """`git` stdout as one string, tolerant: "" on any failure.

    harvest-table is a reporting tool: a missing branch, worktree or manifest
    is a row beat, never a crash. Callers that need failure loudly use the
    existing `_git_lines`/subprocess.run forms instead.
    """
    try:
        out = subprocess.run(["git", "-C", str(cwd), *args],
                             capture_output=True, text=True)
    except (OSError, subprocess.SubprocessError):
        return ""
    if out.returncode != 0:
        return ""
    return out.stdout


def _frontmatter_scalars(text: str) -> dict[str, str]:
    """Pull scalar `key: value` fields out of a node's frontmatter block.

    We only need id/verdict/confidence, so a tolerant scan beats pulling in a
    YAML dependency. Non-scalar fields (lists) are ignored.
    """
    outdict: dict[str, str] = {}
    if not text.startswith("---"):
        return outdict
    rest = text.split("\n", 1)[1] if "\n" in text else ""
    block, _, _after = rest.partition("\n---")
    for ln in block.splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", ln)
        if m and m.group(2):
            outdict[m.group(1)] = m.group(2).strip("\"'")
    return outdict


def _harvest_round_dirs(main: Path, seat: str | None = None) -> list[Path]:
    """One manifest dir per `iter-*` round, from the root shapes a seat uses.

    A round's AUTHORITATIVE copy names the PARENT-tier agent (tier ==
    "parent") that dispatch cut the round branch for — and the branch is
    named after that parent, never the kids. Such a record lives in a seat's
    worktree (`.agi/worktrees/seat-<S>/.agi/sessions/`, where a seat's rounds
    are kept while main holds none), not in main's own sessions dir and not
    in a kid's worktree. So the copy that wins for a round id is, in priority
    order: main's (a `rotate.py complete` copy is the durable one), the
    named seat's worktree copy (when --seat is given), then any worktree
    copy whose manifest still carries a parent-tier record, then any other
    worktree copy. That ordering is the whole fix for the live falsifier of
    hypothesis:harvest-table-subcommand: without it, the scanner reads a
    KID-only worktree manifest (a00-* sorts before seat-*), keys rows by kid
    id, and finds no loop branch named after a kid.
    """
    found: dict[str, tuple[int, Path]] = {}

    def _mf_has_parent(p: Path) -> bool:
        try:
            mf = json.loads((p / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return False
        return any((a.get("tier") or "").strip() == "parent"
                   for a in (mf.get("agents") or []))

    def _absorb(p: Path, pri: int) -> None:
        if (p.is_dir() and p.name.startswith("iter-")
                and (p / "manifest.json").is_file()):
            cur = found.get(p.name)
            if cur is None or pri < cur[0]:
                found[p.name] = (pri, p)

    main_sess = main / ".agi" / "sessions"
    if main_sess.is_dir():
        for d in sorted(main_sess.iterdir()):
            _absorb(d, 0)
    wt_root = main / ".agi" / "worktrees"
    if wt_root.is_dir():
        # The named seat's own copy first.
        if seat:
            s = wt_root / f"seat-{seat}" / ".agi" / "sessions"
            if s.is_dir():
                for d in sorted(s.iterdir()):
                    _absorb(d, 1)
        # Then any worktree manifest that still carries a parent-tier record
        # (parent worktrees and the other seats), so a parent-named round is
        # never shadowed by the same round's kid-only worktree manifest.
        for agent_dir in sorted(wt_root.iterdir()):
            s = agent_dir / ".agi" / "sessions"
            if not s.is_dir():
                continue
            for d in sorted(s.iterdir()):
                if _mf_has_parent(d):
                    _absorb(d, 2)
        # Finally the kid-only worktree manifests.
        for agent_dir in sorted(wt_root.iterdir()):
            s = agent_dir / ".agi" / "sessions"
            if not s.is_dir():
                continue
            for d in sorted(s.iterdir()):
                if not _mf_has_parent(d):
                    _absorb(d, 3)
    return [p for _, p in sorted(found.values(), key=lambda kv: kv[1].name)]


def _harvest_loop_branches(main: Path) -> dict[str, tuple[str, int]]:
    """agent_id -> (branch, season) for every `loop/<slug>-<agent>@s<N>`.

    Derived from `git for-each-ref` because the branch name is the durable
    fact (hypothesis:harvest-table-subcommand): it survives the worktree being
    removed once the round is brought home, and it never has to be rebuilt
    from a slug convention that may have drifted. First branch per agent wins
    (the earliest cut).
    """
    mapping: dict[str, tuple[str, int]] = {}
    out = _git_out(main, "for-each-ref", "--format=%(refname:short)",
                   "refs/heads/loop")
    for ln in out.splitlines():
        m = re.match(r"^(.*)-(a00-[0-9a-f]{8})@s(\d+)$", ln.strip())
        if not m:
            continue
        mapping.setdefault(m.group(2), (ln.strip(), int(m.group(3))))
    return mapping


def _harvest_read_node_fields(main: Path, branch: str, rel: str) -> dict:
    """id/verdict/confidence of the experiment node `rel` at the branch tip.

    Prefers on-disk (the worktree, else main), because the file is already
    there for a live round and reading it costs nothing; falls back to
    `git show branch:path` so a finished round whose worktree is gone still
    reports its kids.
    """
    for base in (main / ".agi" / "worktrees", main):
        p = base / rel
        if p.is_file():
            try:
                return _frontmatter_scalars(p.read_text(encoding="utf-8"))
            except OSError:
                return {}
    return _frontmatter_scalars(_git_out(main, "show", f"{branch}:{rel}"))


def _harvest_diffstat(main: Path, base_branch: str,
                      round_branch: str) -> tuple[str, list[str], bool]:
    """(diffstat text, kid experiment node relpaths, resolved) for the round.

    Both are diffed from `merge-base(base_branch, round_branch)` to the
    round branch tip, so a moved base tip never shifts the base and the
    stat shows exactly what the round added — the round's own nodes, never
    content merged into the base after the cut.

    `resolved` True means git actually answered: `round_branch` resolved and
    a merge-base with `base_branch` exists. A resolvable but LEGITIMATELY
    EMPTY diff (tip == base, or no experimental nodes added) still reports
    `resolved=True` with an empty kid list — that is git's honest "no
    changes" answer, not a failure. `resolved` False means git could not
    answer at all (unknown branch or no merge-base), which is the only
    situation the on-disk fallback may fire.
    """
    mb = _git_out(main, "merge-base", base_branch, round_branch).strip()
    if not mb:
        return "-", [], False
    tip = _git_out(main, "rev-parse", "--verify", "--quiet",
                   round_branch).strip()
    if mb and tip and mb == tip:
        # Fully-merged round: merge-base(base, round) == the round branch
        # tip, so `mb..round_branch` is empty. Recover the round's OWN
        # changeset from the branch itself — the round is what the branch
        # added after the seat history it was cut from, and a dispatched
        # round branch is a single commit, so `<round_branch>^..<round_branch>`
        # is exactly that (hypothesis:harvest-table-subcommand, measured
        # equal to the merge-changeset on L4.231/L4.228). Only if the branch
        # has no parent to diff against do we fall back to the empty range.
        left = f"{round_branch}^"
        a, b = (left, round_branch) if _git_out(
            main, "rev-parse", "--verify", "--quiet", left).strip() \
            else (mb, round_branch)
    else:
        a, b = mb, round_branch
    stat = _git_out(main, "diff", "--stat", f"{a}..{b}").strip()
    stat_s = stat.replace("\n", " | ") or "-"
    names = _git_out(main, "diff", "--name-only", f"{a}..{b}").splitlines()
    kids = [n for n in names
            if n.startswith(".agi/nodes/experiment/")
            and n.endswith(".md")]
    return stat_s, kids, True


def cmd_harvest_table(args: argparse.Namespace, root: Path | None) -> int:
    """`harvest-table --seat S [--round N | --all-live] [--root R]`.

    Prints one row per ROUND deriving the five facts the director discovers
    by hand today (hypothesis:harvest-table-subcommand): the round's branch,
    worktree path, a diffstat against the merge-base with the seat branch,
    the round's kid experiment node ids, and each kid's verdict. The branch
    is looked up from the round's PARENT-tier agent record (dispatch names
    the round branch after the parent, never the kid), the kids are the
    experiment nodes ADDED on that branch relative to the merge-base, and
    every fact is derived from git + the session manifests so a finished
    round whose worktree is gone still reports branch/diffstat/kids from
    git alone. Exit 0 even when a filter matches zero rounds (the message
    names what was searched).
    """
    main = None
    if getattr(args, "root", None):
        main = locations.git_common_root(Path(args.root).resolve())
    elif root:
        main = locations.git_common_root(root)
    else:
        main = locations.find_project_root()
    if main is None or not (main / ".git").exists():
        print("ERR harvest-table: no git project resolvable as the main "
              "checkout", file=sys.stderr)
        return 1

    want_seat = (args.seat or "").strip() or None
    want_round = (args.round or "").strip() or None
    if want_round and not want_round.startswith("iter-"):
        want_round = "iter-" + want_round

    branches = _harvest_loop_branches(main)
    parent = _git_out(main, "branch", "--show-current").strip()

    # The seat branch the claim names as the diff base, when --seat is given
    # and that ref exists (hypothesis:harvest-table-subcommand item (d)).
    seat_base = f"seat/{want_seat}@s2" if want_seat else ""
    if seat_base and not _git_out(main, "rev-parse", "--verify", "--quiet",
                                  seat_base).strip():
        seat_base = ""

    header = ("round | agent | branch | worktree | diffstat-vs-merge-base | "
              "kids | verdicts")
    rows: list[str] = []
    for rd in _harvest_round_dirs(main, want_seat):
        try:
            mf = json.loads((rd / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        agents = mf.get("agents") or []
        if not agents:
            continue
        if want_seat and not any(a.get("dispatched_by") == want_seat
                                 for a in agents):
            continue
        if want_round and rd.name != want_round:
            continue
        if args.all_live and not any(a.get("status") == "running"
                                     for a in agents):
            continue
        # One row per ROUND. The PARENT-tier agent names the round branch
        # (dispatch.py cuts `loop/<24-char slug prefix>-<parent-id>@s<N>`,
        # never the kid's id); kids are derived from the git diff, not from
        # the manifest's kid list (which is a cross-check only). Fall back to
        # any agent id that names a loop ref when a parent-tier record is
        # absent (e.g. a kid-only main manifest).
        rec = next((a for a in agents
                    if (a.get("tier") or "").strip() == "parent"), None)
        if rec is None:
            rec = next((a for a in agents
                        if branches.get((a.get("id") or "").strip())), None)
        r_agent = (rec.get("id") or "").strip() if rec else ""
        branch = (((rec.get("branch") or "").strip() if rec else "")
                  or (branches.get(r_agent, (None,))[0] or "-"))
        # Worktree from the record when it still EXISTS on disk, else by
        # convention, else `-` once the worktree is removed (the durable fact
        # stays in git).
        wt_dir = (main / ".agi" / "worktrees" / r_agent) if r_agent else main
        wt_s = (rec.get("worktree") or "").strip() if rec else ""
        if wt_s:
            if not Path(wt_s).is_dir():
                wt_s = "-"
        else:
            wt_s = str(wt_dir) if wt_dir.is_dir() else "-"
        # Diff base: the seat branch first (item (d)), else the record's
        # base_branch, else the main checkout's current branch. The manifest
        # base is the branch the round was actually cut from (dispatch.py
        # stamps it); the main checkout's branch is not the round's base once
        # rounds are cut from seat branches while main sits on season/.
        base = (seat_base or ((rec.get("base_branch") or "").strip()
                              if rec else "") or parent or "-")
        rows_kid: list[tuple[str, str]] = []  # (kid_node_id, verdict)
        diff_s = "-"
        resolved = False
        if branch != "-":
            diff_s, rels, resolved = _harvest_diffstat(main, base, branch)
            for rel in rels:
                f = _harvest_read_node_fields(main, branch, rel)
                rows_kid.append((f.get('id', rel), f.get('verdict', '-')))
        if not resolved and r_agent and wt_dir.is_dir():
            # git could NOT answer at all (no branch, or no recorded base to
            # diff against). Fall back to on-disk experiment nodes naming the
            # target. A resolvable-but-empty diff is git's legitimate "no
            # changes" answer — reported as no kids, never overridden by
            # scanning a shared worktree's stale nodes.
            target = (rec.get("target") or "") if rec else ""
            exp = wt_dir / ".agi" / "nodes" / "experiment"
            if exp.is_dir():
                for nf in sorted(exp.glob("*.md")):
                    t = nf.read_text(encoding="utf-8")
                    if target and target.replace(":", "-") in t:
                        f = _frontmatter_scalars(t)
                        rows_kid.append((f.get('id', nf.stem),
                                         f.get('verdict', '-')))
                if rows_kid:
                    diff_s = "(worktree disk; no git diff)"
        kid_ids = " ; ".join(kid for kid, _ in rows_kid) or "-"
        verdicts = " ; ".join(v for _, v in rows_kid) or "-"
        rows.append(f"{rd.name} | {r_agent or '-'} | {branch} | {wt_s} | "
                    f"{diff_s} | {kid_ids} | {verdicts}")

    if not rows:
        note = ""
        if want_seat:
            note = f" seat={want_seat}"
        if want_round:
            note += f" round={want_round}"
        if args.all_live:
            note += " live=only"
        print(f"harvest-table: 0 rows (no manifest/iter dirs matching{note})",
              file=sys.stderr)
        return 0
    print(header)
    for r in rows:
        print(r)
    return 0


# --- main ------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    # meter
    p_meter = sub.add_parser("meter", help="print context-usage fraction")
    p_meter.add_argument("--session-log", default=None,
                        help="path to a Claude Code JSONL transcript or "
                             "remote-control debug log")
    p_meter.add_argument("--check", action="store_true",
                        help="exit 1 if fraction >= threshold; else 0")
    p_meter.add_argument("--seat", default=None,
                        help="seat name: read the seat-stable "
                             ".agi/sessions/<name>.meter pin over the "
                             "newest-mtime pin (hypothesis:l3w4-seat-registry)")
    p_meter.add_argument("--pin", default=None,
                        help="write a pin file naming the transcript this "
                             "role owns (hypothesis:l3-meter-own-transcript)")
    p_meter.set_defaults(func=cmd_meter)

    # spawn
    p_spawn = sub.add_parser("spawn", help="launch a successor in tmux")
    p_spawn.add_argument("--name", default=None,
                        help="successor name (tmux window + remote-control id); "
                             "defaults to <base>-<ROM> derived from existing windows")
    p_spawn.add_argument("--tier", default="prime_director",
                        help="role tier for model/effort/settings defaults "
                             "(default: prime_director)")
    p_spawn.add_argument("--model", default=None,
                        help="model alias override (default from ladder roles "
                             "table / config.json harnesses.claude-code)")
    p_spawn.add_argument("--effort", default=None,
                        help="effort level override (low|medium|high|xhigh|max)")
    p_spawn.add_argument("--settings", default=None,
                        help="JSON settings flag, e.g. '{\"ultracode\":true}'")
    p_spawn.add_argument("--prompt-file", default=None,
                        help="successor body file (default: "
                             "prime-director-successor.md); the constitution "
                             "head is always prepended through brief.py")
    p_spawn.add_argument("--successor-argv", default=None,
                        help="explicit stand-in successor command run verbatim "
                             "instead of the real claude --remote-control "
                             "(hypothesis:l3-rotate-self-successor-override)")
    p_spawn.add_argument("--tmux-session", default=DEFAULT_TMUX_SESSION,
                        help="tmux session to create the window in "
                             f"(default: {DEFAULT_TMUX_SESSION})")
    p_spawn.add_argument("--window-path", default=None,
                        help="read existing tmux window names from this file "
                             "instead of calling tmux (tests)")
    p_spawn.add_argument("--dry-run", action="store_true",
                        help="print the command instead of running it")
    p_spawn.set_defaults(func=cmd_spawn)

    # loop
    p_loop = sub.add_parser("loop", help="super-ralph rotation: meter, rotate "
                                         "when due, confirm successor")
    p_loop.add_argument("--role", default="prime_director",
                        help="role tier for defaults (default: prime_director)")
    p_loop.add_argument("--name-prefix", default="belam",
                        help="successor name prefix (default: belam)")
    p_loop.add_argument("--name", default=None,
                        help="explicit successor name (skips derivation)")
    p_loop.add_argument("--force", action="store_true",
                        help="rotate even when under director_rotate_at")
    p_loop.add_argument("--session-log", default=None,
                        help="path to read the successor's reply from "
                             "(default: the spawned debug file)")
    p_loop.add_argument("--debug-file", default=None,
                        help="override the successor's --debug-file path")
    p_loop.add_argument("--timeout", type=int, default=120,
                        help="seconds to wait for the successor reply "
                             "(default: 120)")
    p_loop.add_argument("--model", default=None, help="model override")
    p_loop.add_argument("--effort", default=None, help="effort override")
    p_loop.add_argument("--settings", default=None,
                        help="JSON settings flag, e.g. '{\"ultracode\":true}'")
    p_loop.add_argument("--prompt-file", default=None,
                        help="successor body file (head prepended)")
    p_loop.add_argument("--successor-argv", default=None,
                        help="explicit stand-in successor command run verbatim "
                             "instead of the real claude --remote-control "
                             "(hypothesis:l3-rotate-self-successor-override)")
    p_loop.add_argument("--tmux-session", default=DEFAULT_TMUX_SESSION,
                        help=f"tmux session (default: {DEFAULT_TMUX_SESSION})")
    p_loop.add_argument("--window-path", default=None,
                        help="read existing window names from this file (tests)")
    p_loop.add_argument("--dry-run", action="store_true",
                        help="print the command instead of running it")
    p_loop.add_argument("--comms-root", default=None,
                        help="override the comms dir the rotation announcement "
                             "is delivered to (default: send.py's comms_root)")
    p_loop.set_defaults(func=cmd_loop)

    # ack: the successor's explicit reply (hypothesis:l4-rotate-readback-
    # false-negative-and-the-orphan-by-design). The replacement for the
    # debug-log read-back.
    p_ack = sub.add_parser(
        "ack", help="[DEPRECATED] write the successor's explicit rotation reply "
                    "(<sessions>/seats/<seat>.ack.json); the predecessor writes "
                    "the ack in kid 2 (rotate self) -- kept callable for one "
                    "generation as a fallback only")
    p_ack.add_argument("--seat", required=True,
                       help="the successor's seat name", dest="seat")
    p_ack.add_argument("--gen", type=int, required=True, dest="gen",
                       help="the generation this ACK confirms (gen_after)")
    p_ack.add_argument("--ref", default=None, dest="ref",
                       help="the successor's own ListAgents session ref")
    p_ack.add_argument("answer", choices=("continue", "diff"),
                       help="continue | diff")
    p_ack.add_argument("--text", default=None,
                       help="the diff text, when answer is diff; `-` reads it "
                            "from stdin")
    p_ack.set_defaults(func=cmd_ack)

    # status
    p_status = sub.add_parser(
        "status", help="list agi-master and belam tmux sessions")
    p_status.add_argument("--seats", action="store_true",
                          help="list registry seats instead (seat/generation/"
                               "fraction/age, one line per row)")
    p_status.add_argument("--seat", default=None,
                          help="seat name to read with --record")
    p_status.add_argument("--record", default=None,
                          help="print the LATEST durable rotation record for "
                               "--seat, plus the current sequence and the "
                               "seat's own row (read-only)")
    p_status.add_argument("--wait", type=int, default=0,
                          help="with --record latest: re-read the latest "
                               "record at a <=2s interval until its "
                               "s12_self_reap section is present (terminal) "
                               "or N seconds elapse. On success print the "
                               "normal output; on timeout print the last-seen "
                               "record, ERR and exit 2.")
    p_status.set_defaults(func=cmd_status)

    # harvest-table: one row per (round, kid agent) giving the five facts the
    # director still discovers by hand (hypothesis:harvest-table-subcommand)
    p_ht = sub.add_parser(
        "harvest-table",
        help="report each round's branch/worktree/diffstat-vs-merge-base/"
             "kid-experiment-ids/verdicts, from git + session manifests")
    p_ht.add_argument("--seat", default=None,
                      help="only rounds dispatched_by this seat")
    p_ht.add_argument("--round", default=None,
                      help="only the named iter (accepts 'L4.236' or "
                           "'iter-L4.236')")
    p_ht.add_argument("--all-live", action="store_true",
                      help="only rounds with at least one running agent")
    p_ht.add_argument("--root", default=None,
                      help="project root override (default: resolve from cwd)")
    p_ht.set_defaults(func=cmd_harvest_table)

    # seq: print the current rotation-alert sequence number (one read)
    p_seq = sub.add_parser(
        "seq", help="print the current rotation-alert sequence number "
                      "(a seat's one-read check for a superseded order)")
    p_seq.set_defaults(func=cmd_sequence)

    # alarms --holder S: meter held seats, dm `rotate now` when a pin crosses
    # director_rotate_at (hypothesis:l3w4-seat-rotation-loops)
    p_alarms = sub.add_parser(
        "alarms", help="meter seats rotated_by the holder; dm `rotate now` "
                        "when a pin crosses director_rotate_at")
    p_alarms.add_argument("--holder", required=True,
                          help="the seatholder whose `rotated_by` seats this "
                          "meters (e.g. the advisor that rotates its "
                          "director-kids)")
    p_alarms.add_argument("--once", action="store_true",
                          help="meter each held seat once, send due dms, and "
                          "return (regression-friendly)")
    p_alarms.add_argument("--interval", type=int, default=300,
                          help="seconds between meters when not --once "
                          "(default: 300)")
    p_alarms.add_argument("--comms-root", default=None,
                          help="override the comms root (tests)")
    p_alarms.set_defaults(func=cmd_alarms)

    # next --seat S: the DRIVEN (operator) half of the startup path. Prints
    # exactly one literal command per call; advances only on --record-ok.
    p_next = sub.add_parser(
        "next", help="print the next startup step (one literal command) for a "
                     "seat, advancing only on a recorded success — the "
                     "DRIVEN operator half (hypothesis:l4-startup-is-one-\n"
                     "script-or-a-driven-prompt)")
    p_next.add_argument("--seat", required=True, help="seat name")
    p_next.add_argument("--role", default=None,
                        help="role tier to resolve the template (default: the "
                             "seat's registry row role)")
    p_next.add_argument("--template", default=None,
                        help="explicit rotation template name "
                             "(.geometry/rotations.md)")
    p_next.add_argument("--record-ok", dest="record", action="store_const",
                        const="ok", default=None,
                        help="record the current step as succeeded, then print "
                             "the next one")
    p_next.add_argument("--record-fail", dest="record", action="store_const",
                        const="fail", default=None,
                        help="record the current step as failed (it is re-printed "
                             "by the next call)")
    p_next.add_argument("--json", action="store_true",
                        help="emit a small JSON object instead of the bare command")
    p_next.add_argument("--gen", type=int, default=None,
                        help="generation for placeholder resolution (default: "
                             "handoff gen + 1)")
    p_next.add_argument("--succ-name", default=None,
                        help="successor name for placeholder resolution "
                             "(default: the seat name)")
    p_next.add_argument("--tmux-session", default=DEFAULT_TMUX_SESSION,
                        help=f"tmux session (default: {DEFAULT_TMUX_SESSION})")
    p_next.add_argument("--root", default=None,
                        help="project root override (default: resolve from cwd)")
    p_next.set_defaults(func=cmd_next)

    # rotate-self --name S: the non-prime self-rotation primitive
    p_rs = sub.add_parser(
        "rotate-self", help="rotate a non-prime seat onto a same-named "
                             "successor and kill its own window")
    p_rs.add_argument("--name", required=True,
                      help="the seat's own plain registry name")
    p_rs.add_argument("--force", action="store_true",
                      help="rotate without an over-threshold meter check")
    p_rs.add_argument("--timeout", type=int, default=600,
                      help="seconds to wait for the successor `continue` "
                           "(default: 600)")
    p_rs.add_argument("--debug-file", default=None,
                      help="override the successor log path (default: "
                           ".agi/sessions/<name>.log)")
    p_rs.add_argument("--model", default=None, help="model override")
    p_rs.add_argument("--effort", default=None, help="effort override")
    p_rs.add_argument("--settings", default=None,
                      help="JSON settings flag")
    p_rs.add_argument("--prompt-file", default=None,
                      help="successor body file (default by tier)")
    p_rs.add_argument("--throwaway", action="store_true",
                      help="rehearsal-only seat: skip the seats.md registry "
                           "gate, never write seats.md "
                           "(hypothesis:l3-rotate-self-successor-override)")
    p_rs.add_argument("--role", default=None,
                      help="role tier for a --throwaway seat (default: parent)")
    p_rs.add_argument("--template", default=None,
                      help="rotation template name (L4.110): resolve THIS "
                           "template for this one rotation -- may name another "
                           "role's template. Default: the seat role's own "
                           "default. Source: .geometry/rotations.md.")
    p_rs.add_argument("--successor-argv", default=None,
                      help="explicit stand-in successor command run verbatim "
                           "instead of the real claude --remote-control "
                           "(hypothesis:l3-rotate-self-successor-override)")
    # ++ L4.114 handover: identity is SUPPLIED by the registry JOIN by the
    # successor's WINDOW @id, not by a --session-ref flag (that flag is
    # GONE; tests inject the seam into the Namespace directly). --registry-dir
    # is the test seam; production defaults to ~/.claude/sessions.
    p_rs.add_argument("--registry-dir", default=None,
                      help="per-session registry dir to JOIN the successor "
                           "from (default: ~/.claude/sessions) — tests")
    p_rs.add_argument("--registry-poll", type=int, default=None,
                      help="seconds to bound the registry JOIN poll "
                           "(default: 60) — tests")
    p_rs.add_argument("--successor-transcript", default=None,
                      help="the successor's OWN transcript path from the JOIN; "
                           "the meter pin is written AT this, never the newest "
                           "sessions-dir .jsonl.")
    p_rs.add_argument("--belam-prefix", default=None,
                      help="force the Belam-cap check (count windows under this "
                           "prefix, reap the OLDEST when a sixth would exist). "
                           "Default: only for role prime_director, prefix belam.")
    p_rs.add_argument("--tmux-session", default=DEFAULT_TMUX_SESSION,
                      help=f"tmux session (default: {DEFAULT_TMUX_SESSION})")
    p_rs.add_argument("--window-path", default=None,
                      help="read/write window names from this file (tests)")
    p_rs.add_argument("--dry-run", action="store_true",
                      help="print all five steps and touch nothing")
    p_rs.add_argument("--comms-root", default=None,
                      help="override the comms dir the rotation announcement "
                           "is delivered to (default: send.py's comms_root)")
    p_rs.add_argument("--trigger", default="rotate-self",
                      help="spell the rotation's trigger in the announcement "
                           "(meter due / --force / fable-limit)")
    p_rs.add_argument("--in-flight", default=None,
                      help="one line of what is in flight, for peers to know "
                           "if their round is orphaned")
    p_rs.set_defaults(func=cmd_rotate_self)

    # bootstrap-block: the SessionStart hook's reader — emit the successor's
    # bootstrap record as ONE injected block, or REFUSE (exit 1, silent).
    p_bb = sub.add_parser(
        "bootstrap-block", help="emit the bootstrap block for a seat "
                                 "successor, or REFUSE when absent/stale")
    p_bb.add_argument("--seat", required=True, help="seat name")
    p_bb.add_argument("--root", default=None,
                      help="project root (default: resolve from cwd)")
    p_bb.add_argument("--commit", default=None,
                      help="HEAD stamp (test seam; else git rev-parse)")
    p_bb.add_argument("--bounds", default=None,
                      help="JSON fact->'head'|'permanent' staleness map "
                           "(config:rotations ## facts; test seam)")
    p_bb.add_argument("--json", action="store_true",
                      help="emit a JSON envelope and exit 0/1")
    p_bb.add_argument("--quiet", action="store_true",
                      help="print nothing on success (exit code only)")
    p_bb.set_defaults(func=cmd_bootstrap_block)

    # seats-launch
    p_sl = sub.add_parser(
        "seats-launch", help="launch one remote-control session per "
                             "non-ephemeral seat in config:seats")
    p_sl.add_argument("--prompt-file", default=None,
                      help="successor body file (default by tier; None uses "
                           "the assembled brief for non-prime seats)")
    p_sl.add_argument("--tmux-session", default=DEFAULT_TMUX_SESSION,
                        help=f"tmux session (default: {DEFAULT_TMUX_SESSION})")
    p_sl.add_argument("--window-path", default=None,
                      help="read existing window names from this file (tests)")
    p_sl.add_argument("--successor-argv", default=None,
                      help="explicit stand-in successor command run verbatim "
                           "instead of the real claude --remote-control")
    p_sl.add_argument("--dry-run", action="store_true",
                      help="print/return every launch line and touch nothing")
    p_sl.set_defaults(func=cmd_seats_launch)

    # tile
    p_tile = sub.add_parser(
        "tile", help="full-screen partition for N windows: no overlap, no gaps")
    p_tile.add_argument("--count", type=int, default=None,
                        help="number of windows to tile (required unless --apply)")
    p_tile.add_argument("--width", type=int, default=1920,
                        help="screen width px (default: 1920)")
    p_tile.add_argument("--height", type=int, default=1080,
                        help="screen height px (default: 1080)")
    p_tile.add_argument("--apply", action="store_true",
                        help="place live seat windows on X :1 via wmctrl/xdotool "
                             "(graceful if neither is installed)")
    p_tile.add_argument("--names", default=None,
                        help="comma-separated window names to tile (else live "
                             "seat windows from the tmux session)")
    p_tile.add_argument("--tmux-session", default=DEFAULT_TMUX_SESSION,
                        help=f"tmux session (default: {DEFAULT_TMUX_SESSION})")
    p_tile.add_argument("--window-path", default=None,
                        help="read live window names from this file (tests)")
    p_tile.add_argument("--dry-run", action="store_true",
                        help="print one rect per line (default behaviour)")
    p_tile.add_argument("--json", action="store_true",
                        help="print rects as JSON instead of lines")
    p_tile.set_defaults(func=cmd_tile)

    # complete: retire a seat worktree after merge-up (hypothesis
    #            l4-seat-session-iter-dirs, half b)
    p_c = sub.add_parser(
        "complete", help="retire a seat worktree: refuse unless merged up, "
                          "harvest its iter-* session dirs into main, then "
                          "remove the worktree and branch")
    p_c.add_argument("--worktree", required=True,
                     help="path to the seat's git worktree to retire")
    p_c.add_argument("--parent", default=None,
                     help="merge-up target branch; defaults to the main "
                          "checkout's checked-out branch")
    p_c.add_argument("--main", default=None,
                     help="main checkout root override (default: resolved "
                          "via git_common_root)")
    p_c.set_defaults(func=cmd_complete)

    args = ap.parse_args(argv)

    # complete works purely from its explicit paths + git; no project root.
    if args.cmd == "complete":
        return args.func(args, None)

    # meter, loop, alarms, rotate-self, ack and seats-launch need the project root
    if args.cmd in ("meter", "loop", "alarms", "rotate-self", "ack",
                    "next", "seats-launch", "seq"):
        root = find_project_root()
        if root is None:
            print("ERR: no agi project found from cwd", file=sys.stderr)
            return 1
        return args.func(args, root)

    # tile needs the project root only to resolve root (geometry-free cmd)
    if args.cmd == "tile":
        return args.func(args, find_project_root())

    # spawn tolerates a missing project root (chiefly for --dry-run previews)
    if args.cmd == "spawn":
        return args.func(args, find_project_root())

    # status needs the root only for --seats; the tmux half runs without it
    if args.cmd == "status":
        return args.func(args, find_project_root())

    # harvest-table needs the main checkout root (worktrees/sessions/branches)
    if args.cmd == "harvest-table":
        return args.func(args, find_project_root())

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())