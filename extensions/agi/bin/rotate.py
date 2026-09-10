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
    re-resolve the graph from there; identity for a non-worktree caller."""
    graph = locations.find_project_root(root) or root
    main = locations.git_common_root(graph)
    if main is not None:
        mg = locations.find_project_root(main) or graph
        graph = mg
    if (graph / "nodes").is_dir():
        return graph / "sessions"
    if (graph / ".agi" / "nodes").is_dir():
        return graph / ".agi" / "sessions"
    # Unknown shape: default to the graph-dir reading, the production path.
    return graph / "sessions"


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
            return [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines()
                    if ln.strip()]
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


def _shell_cmd(claude_cmd: list[str], settings) -> str:
    """The quoted shell line that launches `claude_cmd`.

    TWO exports may ride in front of the command, and both compose:
    every launch carries CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 so the
    background-shell reaper is disarmed in the launched shell's OWN
    environment rather than inherited from the tmux session, which is one
    server restart from gone (hypothesis:l4-spawn-paths-export-the-reaper-knob);
    an ultracode role's launch additionally exports CLAUDE_CODE_WORKFLOWS=1
    (hypothesis:l3-rotate-ultracode-env).

    `claude_cmd` is quoted element by element, so the constitution head riding
    in argv survives whatever is prepended.
    """
    joined = " ".join(shlex.quote(c) for c in claude_cmd)
    reaper = REAPER_ENV_EXPORT + " && " + joined
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
        proc = subprocess.run(
            ["tmux", "new-window", "-t", tmux_session, "-n", name, launch_cmd],
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
                 successor_argv: str | None = None) -> tuple[int, str]:
    """THE one launch path shared by `cmd_spawn` and `cmd_loop`
    (hypothesis:l3w4-seat-transport).

    Resolves model/effort/settings for `tier` from the ladder row (caller
    flags already overridden), builds the `claude --remote-control <name>`
    command, quotes it for the shell and (unless dry-run) opens it in a new
    tmux window. Refuses when a window of that name already exists. Core is
    not prime-specific -- any named seat may launch through it.

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
        shell_cmd = _shell_cmd(claude_cmd, settings)

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


def _is_log_noise(line: str) -> bool:
    """True when `line` is a bracketed logger line, not a successor's answer.

    The debug pane/joblog mixes claude's own lines `[DEBUG] MDM settings load
    completed`, `<ts> [INFO] ...`, `<ts> [WARN] ...` with the successor's bare
    reply. A bracketed line starts with `[` (bare) or is a timestamp followed
    by a bracket (joblog `2026-09-07T..:..Z [DEBUG] ...`). The continuation
    answer `continue` is neither, so it survives the filter
    (hypothesis:l3-rotate-pin-path-readback)."""
    s = line.strip()
    if not s:
        return True
    if s.startswith("["):
        return True
    return re.match(r"^\S+\s+\[[^\]]+\]", s) is not None


def _read_first_reply(path: str | Path, timeout: int = 120,
                      start_offset: int = 0) -> str | None:
    """Poll `path` until it carries an answer; return the first non-empty line
    that is NOT a bracketed logger line (e.g. `[DEBUG] MDM settings load
    completed`), or None if the timeout is hit first.

    `start_offset` is the read-before-write cursor
    (hypothesis:l3w4-seat-rotation-loops): only bytes AFTER this offset count,
    so a successor spawned under a REUSED plain seat name cannot be confirmed
    by a predecessor's stale bare `continue` left in the same log. Default 0
    preserves the historical whole-file behaviour for `cmd_loop`.
    """
    p = Path(path).expanduser()
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if p.exists() and p.stat().st_size > start_offset:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    if start_offset:
                        fh.seek(start_offset)
                    text = fh.read()
                for line in text.splitlines():
                    if _is_log_noise(line):
                        continue
                    return line.strip()
        except OSError:
            pass
        time.sleep(2)
    return None


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
        "ROTATION CONTINUATION: if the handoff needs no change, answer "
        "exactly the single word `continue` and stop. Otherwise reply with "
        "the exact diff you would make."
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

    debug_file = args.debug_file or f".agi/sessions/{name}.log"
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

    # The successor's reply stream is ITS debug file (written by spawn_window),
    # never the meter's `--session-log` -- pointing the read-back at the
    # caller's own transcript let a prime confirm itself rotation that never
    # happened (Belam VII 2026-09-07 21:56 UTC).
    reply = _read_first_reply(debug_file, timeout=args.timeout)
    rb = Path(debug_file).expanduser().resolve()
    if reply is not None and reply.strip().lower() == "continue":
        _write_rotation_record(root, _loop_record(
            name=name, result="success", succ=succ, readback_log=rb,
            reply_decision="continue"))
        print("handoff stood: successor answered the single word `continue`.",
              file=sys.stderr)
        # The rotation succeeded: announce it to every live seat NOW, at the
        # same moment the record was written (L3.44). A refused or
        # inconclusive rotation above already returned without announcing.
        import send  # local: same dir
        _announce_rotation(
            root=root,
            croot=send.comms_root(root, getattr(args, "comms_root", None)),
            seat=name, successor=name, gen_before=None, gen_after=None,
            trigger="--force" if getattr(args, "force", False) else "meter due",
            handoff_path=str(rb),
            in_flight="successor confirmed `continue`; handoff stood",
            live_names=succ.get("names", []))
        return 0
    if reply is None:
        _write_rotation_record(root, _loop_record(
            name=name, result="inconclusive-no-reply", succ=succ,
            readback_log=rb, reply_decision="no_reply"))
        print("warn: could not read a reply from the successor log "
              "(give it time, then re-run loop).", file=sys.stderr)
        return 0
    _write_rotation_record(root, _loop_record(
        name=name, result="diff", succ=succ, readback_log=rb,
        reply_decision="diff"))
    print("successor replied (handoff needs change):", file=sys.stderr)
    print("  " + reply.strip().replace("\n", "\n  "), file=sys.stderr)
    return 0


# --- status subcommand ----------------------------------------------------


def cmd_status(args: argparse.Namespace, root: Path | None = None) -> int:
    """List tmux windows in sessions whose name starts with agi-master or
    belam; with `--seats`, list the registry seats instead — one line per
    row of seat/generation/fraction/age ("each layer lasts longer" is read
    here, never enforced).

    `--seats` is the graph-reading half and needs the project root; tmux is
    never touched for it."""

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
                   predecessor_session: str = "") -> Path:
    """Write `<S>.handoff.md` with seat/generation/rotated_at/predecessor.
    Returns the written path."""
    hand = _seat_hands(root)
    hand.mkdir(parents=True, exist_ok=True)
    hp = hand / f"{name}.handoff.md"
    hp.write_text(
        f"seat: {name}\n"
        f"generation: {generation}\n"
        f"rotated_at: {datetime.utcnow().isoformat()}Z\n"
        f"predecessor_session: {predecessor_session}\n",
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


def _write_rotate_self_started(path: Path, *, seat: str, steps: list[int],
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
                        cursor_offset: int | None = None) -> dict:
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
                 window_path: str | None = None) -> None:
    """Kill the (renamed) own window once the successor has confirmed.

    With `window_path` (tests) the name is dropped from the file instead of a
    real tmux kill-window."""
    if window_path is not None:
        p = Path(window_path)
        if p.exists():
            lines = [ln for ln in p.read_text(encoding="utf-8").splitlines()
                     if ln.strip() != name]
            p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return
    try:
        subprocess.run(
            ["tmux", "kill-window", "-t", f"{tmux_session}:{name}"],
            capture_output=True, text=True, timeout=5,
        )
    except Exception:
        pass


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

    gen_before = _read_generation(root, seat)
    gen = gen_before + 1
    new_name = f"{seat}.gen{gen}"
    tmux_session = args.tmux_session or DEFAULT_TMUX_SESSION
    dbg = args.debug_file or f".agi/sessions/{seat}.log"

    # A rotate-self rotation opens ONE record file up front (a `started`
    # record) and updates it IN PLACE through every step, so an interruption
    # at any point leaves a record whose `steps_reached` says where it died —
    # instead of nothing at all (hypothesis:l4-rotation-record-survives-
    # interruption). The final outcome rewrites the SAME path, so a completed
    # rotation still leaves exactly one record in today's shape.
    rec_path = None
    steps_reached: list[int] = []
    if not args.dry_run:
        rec_path = _rotate_self_started_path(root, seat)
        _write_rotate_self_started(
            rec_path, seat=seat, steps=steps_reached,
            gen_before=gen_before, gen_after=gen)

    # (1) handoff
    if not args.dry_run:
        _write_handoff(root, seat, gen, predecessor_session=seat)
        steps_reached.append(1)
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen)
    print(f"(1) handoff -> .agi/sessions/seats/{seat}.handoff.md "
          f"generation {gen}")

    # (2) rename own window aside, freeing the plain seat name
    if not args.dry_run:
        _rename_own_window(seat, new_name, tmux_session, args.window_path)
        steps_reached.append(2)
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen)
    print(f"(2) rename own window {seat!r} -> {new_name!r}")

    # (3) spawn the successor under the SAME plain name - never a Roman numeral
    role = (row.get("role") if row else None) \
        or getattr(args, "role", None) or "parent"
    rc, _ = spawn_window(
        name=seat, tier=role,
        prompt_file=args.prompt_file,
        model=args.model or ((row.get("model") if row else None) or None),
        effort=args.effort or ((row.get("effort") if row else None) or None),
        settings=(json.loads(args.settings) if args.settings
                  else _normalize_settings(row.get("settings") if row
                                           else None)),
        tmux_session=tmux_session, window_path=args.window_path, root=root,
        dry_run=args.dry_run, debug_file=dbg,
        successor_argv=getattr(args, "successor_argv", None),
    )
    if rc != 0:
        return rc
    if not args.dry_run:
        steps_reached.append(3)
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen)
    print(f"(3) spawn successor under the plain name {seat!r} (role {role!r})")

    if args.dry_run:
        print("(4) read back successor reply")
        print(f"(5) kill own renamed window {new_name!r}")
        print("(dry-run) ends on the PLAIN seat name; "
              f"generation: {gen} (never a Roman numeral)")
        return 0

    # (4) SUCCESSOR-WINDOW GUARANTEE: a NEW tmux window must exist under the
    #     reused PLAIN seat name, established by tmux list-windows and NEVER
    #     by spawn_window's return value (which has previously reported a
    #     successful rotation and spawned no window at all). Refuse to report
    #     success when it is absent.
    succ = _observed_windows(tmux_session, args.window_path)
    if seat not in succ["names"]:
        pred_o = _observed_windows(tmux_session, args.window_path)
        _write_rotation_record(root, _rotate_self_record(
            seat=seat, result="refused", gen_before=gen_before, gen_after=gen,
            succ=succ, pred={"name": new_name, "windows": pred_o["names"],
                             "source": pred_o["source"]},
            readback_log=Path(dbg).expanduser().resolve(),
            cursor_offset=(Path(dbg).expanduser().resolve().stat().st_size
                           if Path(dbg).expanduser().resolve().exists() else 0),
            refusal="successor window absent"), path=rec_path)
        print(f"ERR: successor window {seat!r} is NOT present in tmux session "
              f"{tmux_session!r}; refusing to report rotation success "
              f"(windows: {succ['names']!r}).", file=sys.stderr)
        return 1

    # (5) read back. Record the successor log's size BEFORE the spawn
    #     completed so the read cursor ignores anything (a stale `continue`)
    #     written before the successor started (read-before-write cursor).
    if not args.dry_run:
        steps_reached.append(4)
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen)
    log = Path(dbg).expanduser().resolve()
    offset = log.stat().st_size if log.exists() else 0
    timeout = getattr(args, "timeout", 600)
    reply = _read_first_reply(dbg, timeout=timeout, start_offset=offset)
    if reply is None or reply.strip().lower() != "continue":
        print("warn: successor did not answer the single word `continue`; "
              "leaving the renamed window in place for inspection.",
              file=sys.stderr)
        return 1

    # (5) PREDECESSOR-SURVIVAL GUARANTEE: the predecessor window (renamed
    #     aside to new_name) must still exist AFTER the successor is confirmed
    #     — a rotation that silently killed its predecessor would destroy the
    #     Belam chain in the direction nobody notices until they need it.
    #     Refuse to report success when it is gone.
    pred_raw = _observed_windows(tmux_session, args.window_path)
    pred = {"name": new_name, "windows": pred_raw["names"],
            "source": pred_raw["source"]}
    pred_alive = new_name in pred_raw["names"]
    if not pred_alive:
        _write_rotation_record(root, _rotate_self_record(
            seat=seat, result="refused", gen_before=gen_before, gen_after=gen,
            succ=succ, pred=pred, readback_log=log, cursor_offset=offset,
            refusal=f"predecessor window {new_name!r} gone"), path=rec_path)
        print(f"ERR: predecessor window {new_name!r} is NOT present in tmux "
              f"session {tmux_session!r}; refusing to report rotation "
              f"success (windows: {pred_raw['names']!r}).",
              file=sys.stderr)
        return 1

    # (6) the record is the deliverable — write it, durably, BEFORE the own
    #     window is killed, so it survives regardless of what the kill does.
    record_path = _write_rotation_record(root, _rotate_self_record(
        seat=seat, result="success", gen_before=gen_before, gen_after=gen,
        succ=_observed_windows(tmux_session, args.window_path),
        pred=pred, readback_log=log, cursor_offset=offset), path=rec_path)

    # (6.5) the rotation succeeded: announce it to every live seat NOW, at
    #     the same moment the record was written, BEFORE the own-window kill
    #     (L3.39 ordering — evidence and announcement both survive cleanup).
    import send  # local: same dir
    _announce_rotation(
        root=root,
        croot=send.comms_root(root, getattr(args, "comms_root", None)),
        seat=seat, successor=seat, gen_before=gen_before, gen_after=gen,
        trigger=getattr(args, "trigger", "rotate-self"),
        handoff_path=f".agi/sessions/seats/{seat}.handoff.md",
        in_flight=getattr(args, "in_flight",
                          f"successor {seat} confirmed; gen {gen}"),
        live_names=succ.get("names", []))

    # (7) confirmed: kill the renamed predecessor window
    _kill_window(new_name, tmux_session, args.window_path)
    print(f"(7) successor confirmed `continue`; killed own window "
          f"{new_name!r}")
    print(f"rotation recorded: {record_path}")
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

    # status
    p_status = sub.add_parser(
        "status", help="list agi-master and belam tmux sessions")
    p_status.add_argument("--seats", action="store_true",
                          help="list registry seats instead (seat/generation/"
                               "fraction/age, one line per row)")
    p_status.set_defaults(func=cmd_status)

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
    p_rs.add_argument("--successor-argv", default=None,
                      help="explicit stand-in successor command run verbatim "
                           "instead of the real claude --remote-control "
                           "(hypothesis:l3-rotate-self-successor-override)")
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

    # meter, loop, alarms and rotate-self need the project root
    if args.cmd in ("meter", "loop", "alarms", "rotate-self", "seats-launch", "seq"):
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

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())