#!/usr/bin/env python3
"""rotate.py — director rotation: meter context usage, spawn a successor.

Subcommands:
  meter [--session-log PATH] [--check]
    - Print the context-usage fraction for the newest Claude Code transcript
      (or an explicit log file) against the ladder node's context window.
    - --check exits 1 when fraction >= director_rotate_at threshold; else 0.

  spawn --name NAME [--prompt-file PATH] [--tmux-session agi-rc]
        [--window-path PATH] [--dry-run]
    - Build a `claude --remote-control NAME ...` command and run it in a new
      tmux window. Refuses if a window of that name already exists.
      When --window-path is given, read tmux window names from that file
      instead of calling tmux (used in tests).
    - --dry-run prints the command and touches nothing.

  status
    - List tmux windows in sessions whose name starts with agi-master,
      with their age.
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

    The usage object looks like:
      {"input_tokens": N, "output_tokens": N,
       "cache_read_input_tokens": N, "cache_creation_input_tokens": N}
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
            # Look for messages with role "assistant" that carry usage
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

    Returns the latest usage object, or None if redacted or absent.
    """
    latest_usage = None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            m = re.match(r"^USAGE:\s*(.*)", line)
            if not m:
                continue
            raw = m.group(1).strip()
            # Detect redacted usage (e.g. "[REDACTED]" or "redacted")
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


# --- meter subcommand -----------------------------------------------------


def cmd_meter(args: argparse.Namespace, root: Path) -> int:
    """Print context-usage fraction and optionally check against threshold."""

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
        # Print 0.0 fraction with no usage
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

    # Print one-line report
    print(f"{fraction:.4f}\t{tokens_used}/{context_tokens} tokens\t"
          f"source={usage_source_name(source)}\tthreshold={threshold}")

    if args.check:
        if fraction >= threshold:
            return 1
        return 0
    return 0


# --- spawn subcommand -----------------------------------------------------


def cmd_spawn(args: argparse.Namespace) -> int:
    """Build and (unless --dry-run) run a `claude --remote-control` command."""

    name = args.name
    if not name or not re.match(r"^[A-Za-z0-9_-]+$", name):
        print(f"ERR: invalid name {name!r}. Use letters, digits, hyphens, "
              f"or underscores.", file=sys.stderr)
        return 1

    tmux_session = args.tmux_session or DEFAULT_TMUX_SESSION
    prompt_file = args.prompt_file
    if prompt_file is None:
        prompt_file = DEFAULT_PROMPT_FILE
    pf = Path(prompt_file).expanduser().resolve()
    if not pf.exists():
        print(f"ERR: prompt file not found: {prompt_file}", file=sys.stderr)
        return 1

    # Read and substitute prompt
    prompt_text = pf.read_text(encoding="utf-8")
    prompt_text = prompt_text.replace("{name}", name)

    # Build the command
    debug_file = f".agi/sessions/{name}.log"
    claude_cmd = [
        "claude",
        "--remote-control", name,
        "--permission-mode", "bypassPermissions",
        "--debug-file", debug_file,
        prompt_text,
    ]

    # Quote for shell display
    shell_cmd = " ".join(shlex.quote(c) for c in claude_cmd)

    if args.dry_run:
        print(shell_cmd)
        return 0

    # Check for existing tmux window
    try:
        result = subprocess.run(
            ["tmux", "list-windows", "-t", tmux_session, "-F", "#{window_name}"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            existing = result.stdout.strip().splitlines()
            if name in existing:
                print(f"ERR: tmux window {name!r} already exists in session "
                      f"{tmux_session!r}. Use a different name.",
                      file=sys.stderr)
                return 1
    except (subprocess.TimeoutExpired, FileNotFoundError):
        # tmux not available or session doesn't exist; will try to create
        pass

    # Spawn new tmux window
    launch_cmd = f"cd {shlex.quote(os.getcwd())} && {shell_cmd}"
    try:
        subprocess.run(
            ["tmux", "new-window", "-t", tmux_session, "-n", name,
             launch_cmd],
            capture_output=True, text=True, timeout=10,
        )
    except FileNotFoundError:
        print("ERR: tmux not found. Install tmux or pass --dry-run to preview.",
              file=sys.stderr)
        return 1
    except subprocess.TimeoutExpired:
        print("warn: tmux new-window timed out — window may still be created.",
              file=sys.stderr)

    print(f"spawned {name!r} in tmux session {tmux_session!r}")
    print(f"  watch at: https://claude.ai/chat (remote-control mode)")
    return 0


# --- status subcommand ----------------------------------------------------


def cmd_status(args: argparse.Namespace) -> int:
    """List tmux windows in sessions whose name starts with agi-master."""

    try:
        # List all tmux sessions matching agi-master*
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
                if s.strip().startswith("agi-master")]
    if not sessions:
        print("(no agi-master tmux sessions)")
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
    p_spawn.add_argument("--name", required=True,
                        help="successor name (used as tmux window name and "
                             "remote-control session id)")
    p_spawn.add_argument("--prompt-file", default=None,
                        help="prompt file for the successor (default: "
                             "prime-director-successor.md)")
    p_spawn.add_argument("--tmux-session", default=DEFAULT_TMUX_SESSION,
                        help="tmux session to create the window in "
                             f"(default: {DEFAULT_TMUX_SESSION})")
    p_spawn.add_argument("--dry-run", action="store_true",
                        help="print the command instead of running it")
    p_spawn.set_defaults(func=cmd_spawn)

    # status
    p_status = sub.add_parser("status", help="list agi-master tmux sessions")
    p_status.set_defaults(func=cmd_status)

    args = ap.parse_args(argv)

    # meter and spawn need the project root
    if args.cmd in ("meter",):
        root = find_project_root()
        if root is None:
            print("ERR: no agi project found from cwd", file=sys.stderr)
            return 1
        return args.func(args, root)

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())