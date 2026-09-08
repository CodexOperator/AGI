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
import subprocess
import sys
import time
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
DEFAULT_DIRECTOR_ROTATE_AT = 0.35

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


def _read_pin_target(pin: Path) -> Path | None:
    """The transcript a pin names, or None when the pin is empty/absent."""
    try:
        target = pin.read_text(encoding="utf-8").strip()
    except OSError:
        return None
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
        target = _read_pin_target(pin)
        if target is not None:
            return target, "seat_pin" if seat else "pin_file"
        return None, f"pin_file-missing"
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
        # (hypothesis:l3-meter-own-transcript).
        pinp = Path(args.pin).expanduser().resolve()
        pinp.parent.mkdir(parents=True, exist_ok=True)
        pinp.write_text(str(log_path) + "\n", encoding="utf-8")

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

    An ultracode role's launch is gated by exporting CLAUDE_CODE_WORKFLOWS=1
    before the command (hypothesis:l3-rotate-ultracode-env).
    """
    joined = " ".join(shlex.quote(c) for c in claude_cmd)
    if _is_ultracode(settings):
        return ULTRACODE_ENV_EXPORT + " && " + joined
    return joined


def _launch_window(tmux_session: str, name: str, shell_cmd: str) -> int:
    """Run `shell_cmd` in a new tmux window. Returns 0 on success."""
    launch_cmd = f"cd {shlex.quote(os.getcwd())} && {shell_cmd}"
    try:
        subprocess.run(
            ["tmux", "new-window", "-t", tmux_session, "-n", name, launch_cmd],
            capture_output=True, text=True, timeout=10,
        )
        return 0
    except FileNotFoundError:
        print("ERR: tmux not found. Install tmux or pass --dry-run to preview.",
              file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print("warn: tmux new-window timed out — window may still be created.",
              file=sys.stderr)
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


def _write_rotation_record(root: Path, record: dict) -> Path:
    """Write one JSON rotation record under `.agi/sessions/rotations/`.

    One file per rotation, named `<seat>.<UTC timestamp>.json` so a reader can
    glob `<seat>.*.json` and see that seat's whole rotation history. Returns
    the written path.
    """
    rot = _rotations_dir(root)
    rot.mkdir(parents=True, exist_ok=True)
    seat = str(record.get("seat") or "anonymous")
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = rot / f"{seat}.{stamp}.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return path


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

    For each such seat: at/over `director_rotate_at` (0.35) send exactly ONE
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

    # (1) handoff
    if not args.dry_run:
        _write_handoff(root, seat, gen, predecessor_session=seat)
    print(f"(1) handoff -> .agi/sessions/seats/{seat}.handoff.md "
          f"generation {gen}")

    # (2) rename own window aside, freeing the plain seat name
    if not args.dry_run:
        _rename_own_window(seat, new_name, tmux_session, args.window_path)
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
            refusal="successor window absent"))
        print(f"ERR: successor window {seat!r} is NOT present in tmux session "
              f"{tmux_session!r}; refusing to report rotation success "
              f"(windows: {succ['names']!r}).", file=sys.stderr)
        return 1

    # (5) read back. Record the successor log's size BEFORE the spawn
    #     completed so the read cursor ignores anything (a stale `continue`)
    #     written before the successor started (read-before-write cursor).
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
            refusal=f"predecessor window {new_name!r} gone"))
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
        pred=pred, readback_log=log, cursor_offset=offset))

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
    p_loop.set_defaults(func=cmd_loop)

    # status
    p_status = sub.add_parser(
        "status", help="list agi-master and belam tmux sessions")
    p_status.add_argument("--seats", action="store_true",
                          help="list registry seats instead (seat/generation/"
                               "fraction/age, one line per row)")
    p_status.set_defaults(func=cmd_status)

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
    p_rs.set_defaults(func=cmd_rotate_self)

    args = ap.parse_args(argv)

    # meter, loop, alarms and rotate-self need the project root
    if args.cmd in ("meter", "loop", "alarms", "rotate-self"):
        root = find_project_root()
        if root is None:
            print("ERR: no agi project found from cwd", file=sys.stderr)
            return 1
        return args.func(args, root)

    # spawn tolerates a missing project root (chiefly for --dry-run previews)
    if args.cmd == "spawn":
        return args.func(args, find_project_root())

    # status needs the root only for --seats; the tmux half runs without it
    if args.cmd == "status":
        return args.func(args, find_project_root())

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())