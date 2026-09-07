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
    - The successor name defaults to belam-N (highest existing belam-*
      tmux window plus one; a belam-* window with no trailing integer counts
      as N=1). --name overrides.
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

#: Remote-control debug log path (legacy fallback).
REMOTE_CONTROL_LOG = Path(".agi") / "sessions" / "remote-control.log"

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
        "rc_log": "remote-control debug log",
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


def _derive_successor_name(windows: list[str], prefix: str = "belam") -> str:
    """The next successor name: highest `prefix-<N>` plus one.

    A window that starts with `prefix` but carries no trailing integer (bare
    `belam`, or the live prime's `belam-S1-L3`) counts as N=1. Nothing known
    about `prefix` yields `prefix-1`.
    """
    best = 0
    for w in windows:
        if not (w == prefix or w.startswith(prefix + "-")):
            continue
        rest = w[len(prefix):]
        m = re.fullmatch(r"-(\d+)", rest)
        if m:
            best = max(best, int(m.group(1)))
        else:
            best = max(best, 1)
    return f"{prefix}-{best + 1}"


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


# ---- meter subcommand -----------------------------------------------------


def cmd_meter(args: argparse.Namespace, root: Path) -> int:
    """Print context-usage fraction and optionally check against threshold."""

    guard = _check_branch_guard(root)
    if guard:
        print(guard, file=sys.stderr)
        return 1

    # Determine which log to parse
    session_log = args.session_log
    source = "unknown"

    if session_log is not None:
        # Explicit path — use it directly, must exist
        log_path = Path(session_log).expanduser().resolve()
        if not log_path.exists():
            print(f"ERR: --session-log {session_log} not found", file=sys.stderr)
            return 1
        source = "explicit"
    else:
        # Try CC transcript first
        cc_path = find_newest_cc_transcript()
        if cc_path is not None:
            log_path = cc_path
            source = "cc_transcript"
        else:
            # Fall back to remote-control debug log
            rc_path = root / REMOTE_CONTROL_LOG
            if rc_path.exists():
                log_path = rc_path
                source = "rc_log"
            else:
                print("ERR: no session log found. Tried CC transcripts "
                      f"(~/.claude/projects/{CC_PROJECT_SLUG}/*.jsonl) and "
                      f"remote-control log ({REMOTE_CONTROL_LOG}). Pass "
                      "--session-log PATH explicitly.",
                      file=sys.stderr)
                return 1

    # Parse usage
    usage = None
    if source in ("explicit", "cc_transcript"):
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
    if not name or not re.match(r"^[A-Za-z0-9_-]+$", name):
        print(f"ERR: invalid name {name!r}. Use letters, digits, hyphens, "
              f"or underscores.", file=sys.stderr)
        return 1

    tmux_session = args.tmux_session or DEFAULT_TMUX_SESSION
    prompt_file = args.prompt_file or DEFAULT_PROMPT_FILE
    pf = Path(prompt_file).expanduser().resolve()
    if not pf.exists():
        print(f"ERR: prompt file not found: {prompt_file}", file=sys.stderr)
        return 1

    # Resolve model / effort / settings (flags override role defaults)
    model = args.model
    effort = args.effort
    settings = json.loads(args.settings) if args.settings else None
    if root is not None:
        if not model:
            model = load_role(root, args.tier, "model")
        if not effort:
            effort = load_role(root, args.tier, "effort")
        if settings is None:
            settings = load_role(root, args.tier, "settings")

    debug_file = f".agi/sessions/{name}.log"
    claude_cmd = _successor_command(
        name=name, tier=args.tier, prompt_file=str(pf),
        model=model, effort=effort, settings=settings, debug_file=debug_file,
    )

    # Quote for shell display (ultracode roles are env-gated + keyworded)
    shell_cmd = _shell_cmd(claude_cmd, settings)

    if args.dry_run:
        print(shell_cmd)
        return 0

    # Check for existing tmux window
    existing = _existing_windows(tmux_session, args.window_path)
    if name in existing:
        print(f"ERR: tmux window {name!r} already exists in session "
              f"{tmux_session!r}. Use a different name.",
              file=sys.stderr)
        return 1

    _launch_window(tmux_session, name, shell_cmd)
    print(f"spawned {name!r} in tmux session {tmux_session!r}")
    print(f"  watch at: https://claude.ai/chat (remote-control mode)")
    return 0


# --- loop subcommand ------------------------------------------------------


def _read_first_reply(path: str | Path, timeout: int = 120) -> str | None:
    """Poll `path` until it carries content; return the first non-empty line,
    or None if the timeout is hit first."""
    p = Path(path).expanduser()
    deadline = time.time() + timeout
    while time.time() < deadline:
        if p.exists() and p.stat().st_size > 0:
            text = p.read_text(encoding="utf-8", errors="replace").strip()
            if text:
                return text.splitlines()[0].strip() or text
        time.sleep(2)
    return None


def cmd_loop(args: argparse.Namespace, root: Path) -> int:
    """The super-ralph rotation primitive: meter, rotate when due, confirm.

    Meter; when under director_rotate_at (and not --force), hold with no
    rotation. Otherwise derive the successor name (`belam-<N>` unless
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

    model = args.model or load_role(root, role, "model")
    effort = args.effort or load_role(root, role, "effort")
    settings = json.loads(args.settings) if args.settings else \
        load_role(root, role, "settings")

    pf = Path(args.prompt_file or DEFAULT_PROMPT_FILE).expanduser().resolve()
    if not pf.exists():
        print(f"ERR: prompt file not found: {pf}", file=sys.stderr)
        return 1

    debug_file = args.debug_file or f".agi/sessions/{name}.log"
    continuation = (
        "ROTATION CONTINUATION: if the handoff needs no change, answer "
        "exactly the single word `continue` and stop. Otherwise reply with "
        "the exact diff you would make."
    )
    claude_cmd = _successor_command(
        name=name, tier=role, prompt_file=str(pf),
        model=model, effort=effort, settings=settings, debug_file=debug_file,
        extra=continuation,
    )
    shell_cmd = _shell_cmd(claude_cmd, settings)

    print(f"rotate {role!r} --> successor {name!r}")

    if args.dry_run:
        print(shell_cmd)
        return 0

    rc = _launch_window(tmux_session, name, shell_cmd)
    if rc != 0:
        return rc

    reply = _read_first_reply(args.session_log or debug_file,
                              timeout=args.timeout)
    if reply is not None and reply.strip().lower() == "continue":
        print("handoff stood: successor answered the single word `continue`.",
              file=sys.stderr)
        return 0
    if reply is None:
        print("warn: could not read a reply from the successor log "
              "(give it time, then re-run loop).", file=sys.stderr)
        return 0
    print("successor replied (handoff needs change):", file=sys.stderr)
    print("  " + reply.strip().replace("\n", "\n  "), file=sys.stderr)
    return 0


# --- status subcommand ----------------------------------------------------


def cmd_status(args: argparse.Namespace) -> int:
    """List tmux windows in sessions whose name starts with agi-master or
    belam."""

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
    p_meter.set_defaults(func=cmd_meter)

    # spawn
    p_spawn = sub.add_parser("spawn", help="launch a successor in tmux")
    p_spawn.add_argument("--name", default=None,
                        help="successor name (tmux window + remote-control id); "
                             "defaults to belam-N derived from existing windows")
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
    p_status.set_defaults(func=cmd_status)

    args = ap.parse_args(argv)

    # meter and loop need the project root
    if args.cmd in ("meter", "loop"):
        root = find_project_root()
        if root is None:
            print("ERR: no agi project found from cwd", file=sys.stderr)
            return 1
        return args.func(args, root)

    # spawn tolerates a missing project root (chiefly for --dry-run previews)
    if args.cmd == "spawn":
        return args.func(args, find_project_root())

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())