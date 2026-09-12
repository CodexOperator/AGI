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
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
import geometry_config  # noqa: E402
import branches  # noqa: E402
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


def _season_ref_on_origin(root: Path, ref: str) -> bool:
    """Whether `ref` exists on the remote `origin` for `root` (a git tree).

    Reads the LOCAL remote-tracking ref via `rev-parse --verify` on
    `refs/remotes/origin/<ref>` — a read-only, no-network probe that returns
    True exactly when `origin/<ref>` is known present (True) vs absent
    (False). A local tracking ref is the same answer `git ls-remote
    --exit-code origin <ref>` gives for the refs this tree has ever seen,
    but it stays on the autopsy's read-only git whitelist (hypothesis:l4-a-
    recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files:
    autopsy runs only rev-list / rev-parse / status / log / show — no
    network, no writes). An absent ref degrades to False, which falls
    through to the LEGACY season spelling — the SAFE direction: a canonical
    name is only ever emitted when its origin ref is verifiably present
    (hypothesis:l4-branches-follow-the-season-grammar). Never raises."""
    return bool(_git_maybe(root, "rev-parse", "-q", "--verify",
                            f"refs/remotes/origin/{ref}"))


def season_branch(root: Path | None) -> str:
    """THE ONE resolver for the season branch name.

    Starts from `season/s{current_season}` in the ladder (`season/s2` only
    when the ladder is unreadable — load_ladder_field already warns), then
    accepts BOTH spellings and emits the canonical name ONLY when it exists
    on origin (hypothesis:l4-branches-follow-the-season-grammar).

    `branches.ref_candidates(branch)` returns the canonical first (`season
    N/main`) then the legacy alias (`season/sN`) as the one-season deprecated
    fallback; the first candidate that resolves on origin is returned, so on
    a pre-migration tree — where only `origin/season/sN` exists and
    `origin/season<N>/main` does NOT — the legacy spelling is emitted and a
    canonical name that would resolve nowhere is never printed. A tree where
    NO candidate resolves falls back to the input branch unchanged (never a
    name that does not exist; readers address it as `origin/{season}`). With
    `root is None` (no git) the origin probe is skipped and the ladder
    spelling is returned directly.

    Every literal `season/s2` site in rotate.py routes through this so a
    season change is ONLY the ladder's `current_season` (hypothesis l4-the-
    prepare-captives-measure-generation-upstream-and-season-and-the-gate-
    is-not-a-test-seam, piece 4: printed lines change text only by the
    season number)."""
    s = load_ladder_field(root, "current_season", None) if root is not None \
        else None
    if s is None:
        branch = "season/s2"
    else:
        branch = f"season/s{s}"
    if root is None:
        return branch
    for cand in branches.ref_candidates(branch):
        if _season_ref_on_origin(root, cand):
            return cand
    return branch


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


def _seat_pin_path(root: Path, seat: str) -> Path:
    """The seat's OWN pin path, `<sessions>/<seat>.meter`, the ONE form a
    `meter --pin` clear line must print (hypothesis:l4-meter-pin-refuses-a-
    target-that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears).
    Resolved via `_sessions_dir` so the printed path and the write target can
    never disagree."""
    return _sessions_dir(root) / f"{seat}{METER_PIN_EXT}"


def _valid_meter_pin_target(pinp: Path, root: Path) -> tuple[bool, str]:
    """A `--pin` write target must BE a meter pin: a basename ending in
    `{METER_PIN_EXT}` AND directly under the graph's sessions dir (the claim
    naming it). A target is otherwise refused BY NAME and never written --
    the Prime passed its own transcript (a `.jsonl`) as --pin and the live
    file became one line, so the target's shape is checked BEFORE any write.
    Returns (ok, reason); `pinp` must be resolved. The refusal prints the
    one clear line that actually clears: `--pin` takes the PIN FILE, and
    never `--seat` (which trips the cross-generation read refusal)."""
    sessions = _sessions_dir(root).resolve()
    if not pinp.name.endswith(METER_PIN_EXT):
        return (False,
                f"{pinp} is not a meter pin (a pin's name ends "
                f"'{METER_PIN_EXT}'); wrote it, it would truncate. Run: "
                f"rotate.py meter --pin "
                f"{sessions / ('<seat>' + METER_PIN_EXT)} "
                f"--session-log <path-to-the-transcript-you-own>")
    if pinp.parent.resolve() != sessions:
        return (False,
                f"{pinp} is not under the graph's sessions dir ({sessions}); "
                f"pins live there by name. Run: rotate.py meter --pin "
                f"{sessions / ('<seat>' + METER_PIN_EXT)} "
                f"--session-log <path-to-the-transcript-you-own>")
    return True, ""


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
        # A --pin target must BE a pin by name and home (hypothesis:l4-meter-
        # pin-refuses-a-target-that-is-not-a-pin...): a .jsonl transcript, a
        # node or a script is refused BY NAME and never written -- the Prime
        # passed its own transcript as --pin and the live .jsonl became one
        # line. And an EXISTING valid-path pin is overwritten only when its
        # current content parses as a pin record; a target sitting on non-pin
        # bytes is refused and left byte-identical.
        ok_target, reason = _valid_meter_pin_target(pinp, root)
        if not ok_target:
            print(f"ERR: meter --pin refuses its target. {reason}",
                  file=sys.stderr)
            return 1
        if pinp.exists() and _parse_pin_record(pinp)[1] is None:
            print(
                f"ERR: --pin {pinp} exists but its content is not a meter "
                f"pin record (one line `<generation>\\t<transcript>` or a "
                f"bare `<transcript>`); writing it would destroy those bytes. "
                f"Run: rotate.py meter --pin {_seat_pin_path(root, '<seat>')} "
                f"--session-log <path-to-the-transcript-you-own>",
                file=sys.stderr)
            return 1
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

    **A SEAT successor (amendment e) gets the `launch-wrapper` subcommand
    wrapped around the claude argv** (hypothesis:l4-rotate-self-under-pytest-
    reaps-the-host-prime, amendment (e)): the wrapper is the direct parent of
    claude, masks TERM/HUP/INT onto itself, and logs every process-sent
    signal with its sender pid so the seat's lifecycle log distinguishes, by
    construction, a SELF-TEARDOWN (child exit with no wrapper signal) from a
    TERM'd-FROM-OUTSIDE (signal 15 with a sender line) from the WINDOW-KILLED
    (HUP). The seatless line stays byte-identical to today — the wrapper is
    inserted only when `seat` is not None.
    """
    joined = " ".join(shlex.quote(c) for c in claude_cmd)
    # AGI_SEAT rides FIRST in the export chain, so it is set before the
    # reaper/ultracode knobs and the claude process — composed the same way
    # REAPER_ENV_EXPORT already composes, as one `... && ...` line.
    cmd = joined
    if seat is not None:
        wrap = " ".join(shlex.quote(c) for c in (
            _launch_wrapper_argv(seat, claude_cmd)))
        cmd = f"export AGI_POST={shlex.quote(seat)} AGI_SEAT={shlex.quote(seat)} && " + wrap
    reaper = REAPER_ENV_EXPORT + " && " + cmd
    if _is_ultracode(settings):
        return ULTRACODE_ENV_EXPORT + " && " + reaper
    return reaper


def _launch_wrapper_argv(seat: str, child_cmd: list[str]) -> list[str]:
    """The argv that runs `rotate.py launch-wrapper --seat <seat>` wrapping
    `child_cmd`.

    Built from `sys.executable` + this file's own path so the launch line is
    self-locating from any tmux window cwd (the wrapper resolves the project
    root at run time for its default log path; an explicit `--log` overrides).
    The claude argv rides after `--`; `argparse` REMAINDER keeps a leading
    `--`, which `cmd_launch_wrapper` strips.
    """
    return [sys.executable, str(Path(__file__).resolve()),
            "launch-wrapper", "--seat", seat, "--", *child_cmd]


# Signals the launch wrapper reserves onto itself so it can log and forward
# them, plus SIGCHLD so a child's death is delivered to sigwaitinfo rather
# than the default handler. SI_USER/SI_TKILL are the Linux siginfo si_code
# values for a signal a PROCESS sent (delivered via kill/os.kill), vs a tty /
# kernel signal whose si_pid is 0 (SI_KERNEL=128) — not exposed as Python
# constants, so pinned as literals.
_LAUNCH_RESERVED_SIGS = {signal.SIGTERM, signal.SIGHUP, signal.SIGINT}
_LAUNCH_WAIT_SIGS = _LAUNCH_RESERVED_SIGS | {signal.SIGCHLD}
_LINUX_SI_USER = 0      # kill(pid, sig) sent by a process
_LINUX_SI_TKILL = -6    # tgkill / kill(samepid) sent by a process


def _proc_comm(pid: int) -> str:
    """`/proc/<pid>/comm` when the process is alive, else empty."""
    try:
        with open(f"/proc/{pid}/comm", encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def _launch_wrapper_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _launch_wrapper_log(root, seat: str) -> str:
    """Default lifecycle log: `<sessions>/seats/<seat>.wrapper.log` — the
    same seats dir every seat subcommand already addresses from any cwd."""
    r = root
    if r is None:
        r = find_project_root()
        if r is None:
            raise RuntimeError("launch-wrapper: no project root resolvable; "
                               "pass --log")
    return str(_seat_hands(r) / f"{seat}.wrapper.log")


def cmd_launch_wrapper(args, root) -> int:
    """Signal-masking parent so a seat's lifecycle log distinguishes the
    three death classes (amendment e, hypothesis:l4-rotate-self-under-pytest-
    reaps-the-host-prime).

    Blocks TERM/HUP/INT (plus CHLD) onto ITSELF, starts the wrapped child
    with those signals unblocked and the tty inherited (claude stays
    interactive), then loops `signal.sigwaitinfo`:
      * a TERM/HUP/INT whose si_code is SI_USER/SI_TKILL (a process sent it)
        is logged with sender pid (/proc comm if alive) + uid and FORWARDED to
        the child;
      * a kernel/tty signal (si_pid 0) already reached the child's group —
        logged, not forwarded;
      * on SIGCHLD it reaps the child and logs its exit, then exits with the
        child's status (128+signal when signalled).

    So a seat .log distinguishes the three deaths by construction: exit 0/1
    with no wrapper signal = SELF-TEARDOWN; signal 15 with a sender line =
    TERM'd BY <pid>; signal 15 with no wrapper signal = a TERM aimed straight
    at the child (sender unknown to the wrapper); signal 1 = HUP (window
    killed). The row's `pid` is unaffected — the successor's claude pid is
    still in the derived chain, one more ancestor deep.
    """
    child_cmd = list(args.child)
    # argparse REMAINDER keeps the leading `--` separator; strip it.
    if child_cmd and child_cmd[0] == "--":
        child_cmd = child_cmd[1:]
    if not child_cmd:
        print("ERR: launch-wrapper needs a child argv after --",
              file=sys.stderr)
        return 2
    log_path = args.log or _launch_wrapper_log(root, args.seat)
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    tag = f"[launch-wrapper] {args.seat}"
    with open(log_path, "a", encoding="utf-8") as log_fh:
        def _log(line: str) -> None:
            log_fh.write(f"{tag} {line}\n")
            log_fh.flush()

        signal.pthread_sigmask(signal.SIG_BLOCK, _LAUNCH_WAIT_SIGS)
        child = subprocess.Popen(
            child_cmd,
            preexec_fn=lambda: signal.pthread_sigmask(
                signal.SIG_UNBLOCK, _LAUNCH_WAIT_SIGS),
        )
        received: list[int] = []
        while True:
            info = signal.sigwaitinfo(_LAUNCH_WAIT_SIGS)
            if info.si_signo == signal.SIGCHLD:
                break
            received.append(info.si_signo)
            if (info.si_code in (_LINUX_SI_USER, _LINUX_SI_TKILL)
                    and info.si_pid != 0):
                comm = _proc_comm(info.si_pid)
                pid_txt = (f"{info.si_pid} ({comm})" if comm
                           else str(info.si_pid))
                _log(f"SIG{info.si_signo} from pid {pid_txt} "
                     f"uid {info.si_uid} at {_launch_wrapper_now()}")
                try:
                    os.kill(child.pid, info.si_signo)
                except ProcessLookupError:
                    pass
            elif info.si_pid == 0 and info.si_signo == signal.SIGINT:
                # A tty SIGINT (Ctrl-C, `isig`) is delivered by the kernel to
                # the whole FOREGROUND PROCESS GROUP, so the child already has
                # it; forwarding would deliver it twice.
                _log(f"SIG{info.si_signo} from kernel/tty (si_pid 0) "
                     f"uid {info.si_uid} — already reached the child's group, "
                     f"NOT forwarded at {_launch_wrapper_now()}")
            elif info.si_pid == 0:
                # A tty HANGUP is different: the kernel signals only the
                # SESSION LEADER (`tty_signal_session_leader`), and signals
                # the foreground group only when that leader EXITS. Under
                # tmux the wrapper IS the pane's session leader, so a
                # `kill-window` reached nobody but us — measured by the L4.285
                # harvest (sanctuary-director 182119Z 19:05Z): the pre-fix
                # wrapper logged SIG1 "NOT forwarded" and both it and its
                # `sleep` child survived the window kill as orphans. Forward.
                _log(f"SIG{info.si_signo} from kernel/tty (si_pid 0) "
                     f"uid {info.si_uid} — a hangup reaches only the session "
                     f"leader; FORWARDED to child {child.pid} at "
                     f"{_launch_wrapper_now()}")
                try:
                    os.kill(child.pid, info.si_signo)
                except ProcessLookupError:
                    pass
            else:
                _log(f"SIG{info.si_signo} si_code {info.si_code} uid "
                     f"{info.si_uid} — NOT forwarded at "
                     f"{_launch_wrapper_now()}")

        # SIGCHLD: reap the child and report.
        try:
            _, status = os.waitpid(child.pid, 0)
        except ChildProcessError:
            status = 0
        rec = ", ".join(str(s) for s in received) if received else "none"
        if os.WIFSIGNALED(status):
            sig = os.WTERMSIG(status)
            _log(f"child {child.pid} exited signal {sig} at "
                 f"{_launch_wrapper_now()}; wrapper received {rec}")
            return 128 + sig
        code = os.WEXITSTATUS(status) if os.WIFEXITED(status) else 0
        _log(f"child {child.pid} exited status {code} at "
             f"{_launch_wrapper_now()}; wrapper received {rec}")
        return code



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


def _seat_liveness_note(seat: str | None, *, row_pid, argv_pid,
                        tmux_session: str, window_path) -> str | None:
    """The ONE liveness read both the spawn gate and the seating autopsy
    reason from (hypothesis:l4-after-join-keys-on-the-records-window-id-and-
    the-spawn-gate-and-autopsy-share-one-pid, claim (1) of l4-the-spawn-gate-
    refuses-both-directions): the seat is ALIVE iff the ROW's pid OR the
    `--pid` is alive, or a live tmux window is up for the seat. Refuses in
    BOTH directions — a live `--pid` over a dead row AND a dead `--pid` over
    a live row (the SL7.03 inverse hole: `--pid` won and masked a live row).
    A genuine first seating (NO row pid, NO `--pid`) is never gated — no
    predecessor liveness to read, no window probe. Returns a one-line note
    ('pid <N>' / 'window <id>') or None when the seat is dead."""
    for _tag, _p in (("row", row_pid), ("pid", argv_pid)):
        if _p is None:
            continue
        try:
            _g = int(_p)
        except (TypeError, ValueError):
            continue
        if not _pid_gone(_g):
            return f"pid {_g}"
    if row_pid is None and argv_pid is None:
        # a genuine first seating (no row, no --pid) is never gated
        return None
    _lwid = _successor_window_id(seat, tmux_session, window_path)
    if _lwid is not None:
        return f"window {_lwid}"
    return None


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
    seat = getattr(args, "seat", None)
    # pred_pid is derived ONCE for this spawn: `--pid` when given, else the
    # seat row's pid when a seat is named. BOTH the g15.21 dead-gate below and
    # the seating autopsy block read this single value, so a `--pid` naming a
    # live process is refused exactly like a live row pid, and the gate can
    # never disagree with the autopsy on which predecessor died
    # (hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-
    # gate-and-autopsy-share-one-pid). Never a second derivation.
    _pred_pid = getattr(args, "pid", None)
    # A first seating is a rotation without a predecessor
    # (hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor).
    # spawn RUNS the SAME role template `startup.first_turn` rotate-self runs
    # and appends the composed `## STARTUP OUTPUT` block to the seat's first
    # input — but ONLY when a caller that OWNS a concrete seat passes it (a
    # generic spawn/seat-less launch stays byte-identical today). Fail-soft:
    # no template / no first_turn yields empty.
    startup_block = ""
    first_turn = []
    # goal:g15.17 (b): a first seating's role is the SEAT ROW's role when a
    # row exists, `--tier` only as the fallback — a director seat's first-
    # seating alert/template/record never homogenizes to a prime just because
    # `--tier` defaulted to prime_director. (e): a RE-spawn of an EXISTING
    # seat pins at the generation it leaves in its row (SL3.01 residue: the
    # prime's row sat at gen 11 while the re-spawn re-pinned it to 1), never
    # at FIRST_SEATING_GEN.
    _fs_role = args.tier
    _spawn_gen = FIRST_SEATING_GEN
    _srow = None
    if seat is not None:
        # goal:g15.21 — a spawn onto a LIVE seat refuses BY NAME before any
        # write or window (hypothesis:l4-a-spawn-writes-only-onto-a-dead-
        # seat-and-no-season-literal-remains): a spawn onto a seat whose
        # predecessor pid is still running, or where a live tmux window is
        # already up for the seat, is refused. `_pred_pid` stays the SINGLE
        # predecessor the autopsy pre-fills (`--pid` when given, else the
        # row). The GATE reads, in addition, the row's OWN pid — so a dead
        # `--pid` can never mask a live ROW and a live `--pid` can never mask
        # a dead row: both directions refuse (claim (1) of
        # hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-
        # seating-commits-its-row-and-answers-the-ack; the SL7.03 inverse
        # hole). One shared helper, both the gate and the autopsy reason from
        # it (hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-
        # spawn-gate-and-autopsy-share-one-pid).
        _row_pid = None
        if root is not None:
            _row_pid = (_find_seat(root, seat) or {}).get("pid")
            if _pred_pid is None:
                _pred_pid = _row_pid
        _alive_note = None
        if root is not None:
            _alive_note = _seat_liveness_note(
                seat, row_pid=_row_pid, argv_pid=getattr(args, "pid", None),
                tmux_session=tmux_session, window_path=args.window_path)
        if _alive_note is not None:
            print(f"ERR: seat {seat!r} is alive ({_alive_note}); refusing "
                  f"spawn — the seat is already up (goal:g15.21)",
                  file=sys.stderr)
            return 1
        if root is None:
            # goal:g15.17 (a): a caller that OWNS a seat but stands OUTSIDE
            # any project root cannot compose a role template (no
            # rotations.md), write a bootstrap record, or pin a meter — every
            # first-seating side effect needs the graph. Seat the window
            # anyway and skip the template/bootstrap, saying so (the SL2.02
            # refuter's crash: the tail reached Path(None) -> TypeError at
            # _rotations_node_path).
            print("[seating] no project root: template + bootstrap skipped")
        else:
            _srow = _find_seat(root, seat)
            if _srow is not None and _srow.get("role"):
                _fs_role = _srow["role"]
            _rowgen = _seat_row_generation(root, seat)
            if _rowgen is not None:
                _spawn_gen = _rowgen
            startup_block, first_turn = _first_seating_run(
                root, seat=seat, role=_fs_role, succ_name=name,
                tmux_session=tmux_session, dry_run=args.dry_run,
                ask_diff=bool(getattr(args, "ask_diff", False)))
    # The SEAT ROW is the model source for a seated spawn, the flags only an
    # override — the same precedence rotate-self (`cmd_rotate_self`), the
    # reaper's crash-recovery respawn (heal.py) and seats-launch already use.
    # Before this, `spawn --seat X` with no --model built the LADDER default
    # for the tier flag (prime_director -> claude-fable-5-1) against a row
    # that said claude-sonnet-5: the stream-master's first seating dry-run,
    # 2026-09-12 00:2xZ. Owner, verbatim (doc:l4-owner-decisions): "Make sure
    # it only uses sonnet max on rotate and next session spawn. No surprise
    # fable please." A seat-less spawn (no row) is byte-identical to before.
    rc, _ = spawn_window(
        name=name, tier=(_fs_role if _srow is not None else args.tier),
        prompt_file=args.prompt_file,
        model=args.model or ((_srow.get("model") if _srow else None) or None),
        effort=args.effort or ((_srow.get("effort") if _srow else None) or None),
        settings=(json.loads(args.settings) if args.settings
                  else _normalize_settings(_srow.get("settings") if _srow
                                           else None)),
        tmux_session=tmux_session, window_path=args.window_path, root=root,
        dry_run=args.dry_run,
        successor_argv=getattr(args, "successor_argv", None),
        seat=seat,
        extra=startup_block,
    )
    if rc != 0:
        # A FAILED spawn removes the pre-window first-seating bootstrap record
        # `_first_seating_run` wrote before the window came up (Prime XI line
        # (7), second half): a seat that never came up must leave NO 'started'
        # record behind, so `cmd_status --record latest` stays truthful.
        # Removed rather than marked `result: failed` -- the bootstrap record
        # has no `result` field by shape, and a stale `pending: resolved after
        # join` pointing at a seating that never happened is worse than an
        # absent file.
        if seat is not None and root is not None:
            _remove_first_seating_record(root, seat)
        return rc
    if not args.dry_run:
        print(f"spawned {name!r} in tmux session {tmux_session!r}")
        print(f"  watch at: https://claude.ai/chat (remote-control mode)")
        # A recovery seating gets its predecessor autopsy pre-filled from
        # files (hypothesis:l4-a-recovery-seating-gets-its-predecessor-
        # autopsy-pre-filled-from-files): every first seating PRINTS a
        # `[seating]` block — spawned-by, predecessor pid + death ts, record /
        # wrapper, and the three worktree-state lines (behind N, unresolved
        # merge, dirty paths) — and, when the seat row names a pid that is
        # gone, appends the predecessor AUTOPSY as its LAST block so the
        # recovery successor does not reconstruct X's death by hand. `--no-
        # -autopsy` skips only the autopsy, never the block. Reads only.
        now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        seq = _current_sequence(root) if root is not None else 0
        pred_pid = _pred_pid  # the single value the dead-gate also read
        pred_death = "-"
        dead = False
        if pred_pid is not None:
            pred_pid = int(pred_pid)
            dead = _pid_gone(pred_pid)
            _data = _registry_read(getattr(args, "registry_dir", None), pred_pid)
            _tp = Path((_data.get("transcript") or transcript_from_registry_dict(_data)
                        or "")).expanduser() if (_data.get("transcript")
                        or transcript_from_registry_dict(_data)) else None
            pred_death = _death_timestamp(_data, _tp)
        for ln in _compose_seating_base_block(
                seat=seat, source="cmd_spawn", now=now,
                pred_pid=pred_pid, pred_death=pred_death, seq=seq,
                root=root):
            print(ln)
        if root is not None:
            # capture worktree state BEFORE the announce/record writes churn
            for ln in _seating_worktree_lines(root):
                print(ln)
        if dead and not getattr(args, "no_autopsy", False) and root is not None:
            print(f"[seating] previous seat died — predecessor autopsy:")
            for ln in _run_autopsy(seat=seat, pid=pred_pid,
                                   registry_dir=getattr(args, "registry_dir", None),
                                   root=root):
                print(ln)
        # A first seating sends the Sensei the same alert a rotation does
        # (hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-
        # rotation-does): after the window is up, emit the trigger: first-
        # seating dm + write the gen-1 seating record. Non-fatal — a failure
        # never fails the seating.
        ask_diff = bool(getattr(args, "ask_diff", False))
        _seating_rec = None
        if seat is not None and root is not None:
            try:
                _seating_rec = _first_seating_announce(
                    root, None,  # croot None -> resolved inside
                    seat=seat, role=_fs_role, source="cmd_spawn",
                    tmux_session=tmux_session,
                    window_path=getattr(args, "window_path", None),
                    first_turn=first_turn,
                    registry_dir=getattr(args, "registry_dir", None),
                    ask_diff=ask_diff)
            except Exception as exc:                        # noqa: BLE001
                print(f"warn: first-seating announcement failed: {exc}",
                      file=sys.stderr)
        # rotate-self step 2's TWO writes land on the spawn too (hypothesis:
        # l4-a-first-seating-is-a-rotation-without-a-predecessor): pin the
        # seat's meter at gen 1 and write seats/<S>.ack.json with `answer:
        # pending` (F8's contract). The SAME writers rotate-self uses
        # (`_pin_successor_meter` / `_write_ack`) -- never a second pin or ack
        # format. These are the SPAWN's writes, kept separate from the READ-
        # ONLY autopsy block above (which runs no non-read command). A fresh
        # first seating has no successor transcript yet, so the pin is `1\t`
        # (empty target -- rotate-self repoints it when a successor joins at
        # gen 2); an empty-target pin is safe (`_read_pin_target` returns
        # None). Non-fatal: a pin/ack failure never fails the seating.
        if seat is not None and root is not None:
            try:
                _window_id = _successor_window_id(
                    seat, tmux_session, getattr(args, "window_path", None))
            except Exception:                       # noqa: BLE001
                _window_id = ""
            # Claim (a) — the seating row commits the JOINED identity
            # (hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-
            # session-and-prints-its-row-commit-outcome): pid + session_id
            # come from the first-seating join `_first_seating_announce`
            # performed -- the registry record for the seated window @id, the
            # same `_record_join` shape rotate-self writes -- NEVER from the
            # spawner's `--pid` (that is the PREDECESSOR's or the launch
            # script's pid, whatever the caller typed, never the seated
            # window's own). A join that found nothing leaves the row's
            # pid/session_id cells EMPTY and names it in ONE stderr line.
            _jrec = _seating_rec if isinstance(_seating_rec, dict) else {}
            _jpid = _jrec.get("pid")
            _jsess = _jrec.get("session_id") or ""
            if _jpid is None and not _jsess and _jrec.get("window_id"):
                print(f"join: miss (seat {seat!r}: no registry record for "
                      f"window @{str(_jrec['window_id']).lstrip('@')} within "
                      f"the bounded join poll); the seating row commits "
                      f"EMPTY pid/session_id -- never the spawner's --pid "
                      f"({getattr(args, 'pid', None)!r})", file=sys.stderr)
            # Claim (c) -- a join MISS must NOT leave the predecessor's stale
            # pid/session_id in the seat's OWN committed row (falsifier: a
            # registry MISS commits the predecessor's pid/session into the
            # seating row as if they were the seated window's own). Pass the
            # EMPTY sentinel (`pid 0`, the seed an empty row already holds)
            # -- NEVER None -- so `_write_identity_cells`'s None-guard
            # OVERWRITES the stale cells with empty rather than skipping
            # them. `_successor_row_write`/`_commit_spawn_row` bodies stay
            # unchanged; rotate-self's hit path (a real joined pid/session)
            # is byte-identical because it never takes this branch.
            if _jpid is None:
                _jpid = 0
            try:
                _fs_writes = _first_seating_spawn_writes(
                    root=root, seat=seat, generation=_spawn_gen,
                    ask_diff=ask_diff, role=_fs_role,
                    session_id=_jsess, window=_window_id or "",
                    pid=_jpid)
            except Exception as exc:                # noqa: BLE001
                print(f"warn: first-seating meter pin / ack failed: {exc}",
                      file=sys.stderr)
            # Claim (2): a hand seating COMMITS its own seating row through
            # `_commit_spawn_row` (own-row-scoped; `verb="seating row"` -- a
            # first seating's commit is its own `seating row` write, mirror
            # to rotate-self's `spawn row` but named for what it is) and
            # pushes through `_push_season_branch` inside the helper -- so
            # MAIN is left CLEAN after the hand seating (falsifier: "a
            # seating leaves seats.md dirty in MAIN"). Best-effort, never
            # fails the seating; a gitless root / clean-unmodified row skips.
            _commit = ""
            try:
                _commit = _commit_spawn_row(
                    root, seat=seat, generation=_spawn_gen,
                    session_id=_jsess,
                    window=_window_id or "",
                    pid=_jpid,
                    verb="seating row")
            except Exception as exc:                # noqa: BLE001
                _commit = f"seating_row_commit: FAILED: {exc}"
            # Claim (b) (hypothesis:l4-a-hand-seating-commits-the-joined-pid-
            # and-session-and-prints-its-row-commit-outcome): the seating-row
            # commit + push outcome is PRINTED as ONE stderr line and carried
            # into the first-seating record (`handover.seating_row_commit`,
            # trailing `\npush:` line and all), so a failed commit or a
            # failed push is visible and the record carries the same outcome
            # the key-swap gate weighs -- the seating mirror of rotate-self's
            # `handover.spawn_row_commit`.
            if _commit:
                print(_commit, file=sys.stderr)
                if isinstance(_seating_rec, dict):
                    _seating_rec["handover"] = dict(
                        _seating_rec.get("handover") or {})
                    _seating_rec["handover"]["seating_row_commit"] = _commit
                    _seating_record_merge_handover(root, _seating_rec)
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


def _rotate_ack_file(root: Path, seat: str, gen: int) -> str:
    """ROTATE the seat's live ack out of the way when a generation completes.

    goal:g15.25 (SL7.15): a predecessor `continue` left on disk at
    `seats/<seat>.ack.json` is how a stale ack SILENCES the NEXT generation's
    `ack --gen N+1 continue` (the gen-blind no-op, part (a)). After a
    successful rotation (rotate-self) or before a crash-recovery spawn
    (heal._recover_seat) the live ack is renamed to
    `seats/<seat>.ack.gen<N>.json` — an ADDITIONAL name (F8's
    `seats/<seat>.ack.json` `answer` contract unchanged), never a changed
    shape, so the next generation starts with NO live ack. Returns a one-line
    outcome ('' when there was no live ack to rotate, or it was already
    consumed/rotated).
    """
    path = _ack_path(root, seat)
    if not path.exists():
        return ""
    try:
        old = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        old = {}
    if isinstance(old, dict) and (old.get("consumed_at")
                                  or str(path).endswith(".ack.gen")):
        # already consumed/rotated — never double-rotate.
        return "ack: already rotated"
    rotated = path.with_name(f"{seat}.ack.gen{gen}.json")
    try:
        path.rename(rotated)
    except OSError as exc:  # noqa: BLE001
        return f"ack: rotate FAILED: {exc}"
    return f"ack rotated: {rotated.name} (gen {gen})"


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
                    if ack.get("answer") in ("pending", "diff-requested"):
                        # L4.114 (s6/s7): the predecessor writes `pending` as
                        # the ack's initial state (carrying the machine
                        # identity) and the SUCCESSOR flips it to continue/
                        # diff. WITH `--ask-diff` the predecessor writes
                        # `diff-requested` instead (source: predecessor) and
                        # the successor's ONE reply is `diff` or `continue`.
                        # Neither `pending` nor `diff-requested` is terminal —
                        # keep polling for the flip, neither can confirm a
                        # rotation (hypothesis:l4-the-predecessor-answers-
                        # continue-by-default-and-ask-diff-hands-the-
                        # successor-exactly-one-call).
                        pass
                    else:
                        return ack
        except (OSError, ValueError):
            pass
        time.sleep(2)
    return None


def _ack_commits(answer: str, text: str | None, no_commit: bool = False) -> bool:
    """The ONE predicate that decides whether an answered ack commits its own
    row write: `continue` commits; `diff` with empty/whitespace text commits
    (an empty diff stands the handoff exactly like continue); `diff` with text
    never commits. `--no-commit` suppresses the commit on every path. Shared
    by the do_commit gate and the first-seating announce gate so the two can
    never disagree (g15.24 FIX-ONLY)."""
    return (answer == "continue"
            or (answer == "diff" and not (text or "").strip())) \
        and not no_commit


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
    # claim (4): under the DEFAULT-continue contract the predecessor already
    # answered the ack channel (`answer: continue, source: predecessor`), so a
    # successor that runs `ack continue` out of the old habit is a one-line
    # NO-OP -- nothing to run, exit 0, never a double-write. `ack diff` still
    # works (the override): the successor may overwrite the predecessor's
    # continue with its own diff inside the read-back window.
    if args.answer == "continue":
        _prev_src = None
        _prev_ans = None
        _prev_gen = None
        try:
            _ap = Path(_ack_path(root, seat))
            if _ap.exists():
                _pa = json.loads(_ap.read_text(encoding="utf-8", errors="replace"))
                if isinstance(_pa, dict):
                    _prev_src = _pa.get("source")
                    _prev_ans = _pa.get("answer")
                    _prev_gen = _pa.get("gen_after")
        except (OSError, ValueError):
            pass
        if _prev_src == "predecessor" and _prev_ans == "continue":
            if _prev_gen == args.gen:
                print("ack: already answered continue by your predecessor -- "
                      "nothing to run")
                return 0
            # g15.25 (SL7.15): the older no-op was GEN-BLIND — it silenced
            # a successor whose ack channel still carried a PREDECESSOR
            # continue for a DIFFERENT generation, so a crash-recovered post
            # (rotated at gen N, respawned at gen N+1) never took its
            # identity. The read-back (`_read_ack`) already refuses a
            # foreign gen_after; the no-op must too. A predecessor `continue`
            # for ANY OTHER generation is STALE: print one line naming both
            # generations and fall through to write the successor's OWN ack
            # exactly as the pre-SL7.06 path did.
            print(f"ack: stale predecessor answer for gen {_prev_gen}, this "
                  f"is gen {args.gen} -- writing your continue")
    # r3+ (L4.1xx / hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-
    # and-the-successor-one): the successor's identity is the reason the row
    # wants a session_ref at all. A GIVEN --ref must be the BARE ref (a
    # row-shaped ref — brackets, whitespace, or the seat name itself — is
    # REFUSED BY NAME); and it must not already be ANOTHER seat's identity
    # through the SAME resolution send.whois uses (imported, never
    # re-implemented). With NO --ref nothing is back-filled: the ListAgents
    # ref is harness-only and is NOT derivable from the row's session_id
    # (the zero-call lean SL1.06 kid 2 built on that derivation was measured
    # false at the harvest — see the fix-up notes below).
    import send  # local: same dir, no import cycle (send.py pattern)
    ref = (args.ref or "").strip()
    # goal:g15.17 (c): snapshot whether the seat carried a PENDING ack BEFORE
    # this ack overwrites it — rotate-self wrote `answer: pending` before the
    # successor joins, so that pending state is the proof the gen-1 ack is a
    # first ROTATION (a predecessor exists), not a first seating. cmd_ack's
    # own write below overwrites the pending ack, so the flag must be taken
    # here, before the write.
    _pending_ack_present = _pending_ack_exists(root, seat)
    issue = _ref_shape_issue(ref, seat)
    if issue:
        print(f"ERR: --ref {ref!r} refused: {issue}; pass the bare ListAgents "
              "ref (the `[ref]` ListAgents prints beside your name).",
              file=sys.stderr)
        return 2
    rows = send._locally_loaded_rows(root)
    # Director fix-up at the SL1.06 harvest (sensei-director L2), measured on
    # the live rotation 20260911T172702Z: the ListAgents ref (`caa927`) is
    # NOT a prefix of the row's session_id (the Claude session uuid
    # `27179681-…` the JOIN registers) — the two are different identities
    # (F8: the ref is harness-only). So a bare ref that resolves to NO row is
    # the NORMAL first ack, accepted and written verbatim (what whois needs).
    # What the gate refuses is IMPERSONATION: a ref that already resolves,
    # by session_ref or session_id prefix, to a DIFFERENT seat's row
    # (send.whois's IS-NOT-AUTHORIZED, resolved against every row).
    if ref and rows:
        code, _text = send._resolve_rows(rows, ref, claim=seat)
        if code == send.WHOIS_NOT_AUTHORIZED:
            print(f"ERR: --ref {ref!r} refused: {_text} — that ref is "
                  "another seat's identity; pass your OWN bare ListAgents "
                  "ref.", file=sys.stderr)
            return 2
    # r3b: `continue` COMMITS its own row write (unless --no-commit); `diff`
    # WITH text never commits (the successor still edits) -- but a `diff` with
    # an EMPTY text stands the handoff EXACTLY like `continue` (SL7.18 made
    # the empty diff stand the handoff), so it commits the own-row back-fill
    # the same way (g15.24 FIX-ONLY). Only the commit path checks
    # a pre-dirtied seats.md — the SEAT'S OWN row pre-staged or pre-edited
    # before the ack is REFUSED BY NAME before any write (SL6.09 own-row gate:
    # an unrelated FOREIGN hunk, staged or unstaged, is neither bundled nor
    # blocking — only the OWN row's uncommitted change names the refusal), so
    # the ack's own commit never double-writes a row someone was mid-edit on.
    do_commit = _ack_commits(args.answer, text,
                             getattr(args, "no_commit", False))
    # L4.291 director fix-up (sanctuary-director 195718Z harvest): the
    # identity cells now have ONE writer and it writes MAIN's seats.md
    # (`_write_identity_cells` -> `_shared_graph_root`), so every read the
    # ack makes of its own row -- the @id the JOIN keys on, the `already`
    # comparison, the dirty check and the commit -- must look at THAT file,
    # not the worktree copy the writer no longer touches (the kid left
    # `_find_seat` worktree-local; from MAIN itself `id_root == root`).
    id_root = _shared_graph_root(Path(root))
    if do_commit and ref:
        top = _git_toplevel(id_root)
        dirty = _ack_seats_dirty(id_root, top, seat) if top else None
        # g15.24 belt fallback (2c): `--wait N` re-polls the OWN-row gate
        # every 5 s up to N s before the exit-3 refusal. `--wait 0` (the
        # default) behaves exactly as today. A re-poll that succeeds clears
        # the outer refusal and lets the ack proceed normally.
        wait = getattr(args, "wait", 0) or 0
        deadline = time.monotonic() + wait if wait > 0 else None
        while dirty:
            if deadline is None or time.monotonic() >= deadline:
                break
            time.sleep(min(5.0, max(0.05, deadline - time.monotonic())))
            dirty = _ack_seats_dirty(id_root, top, seat) if top else None
        if dirty:
            print(f"ERR: refuse to ack --commit: your OWN row in "
                  f"{dirty!r} is dirty (staged or unstaged) before this ack; "
                  f"resolve it first so the ack never double-writes a row "
                  f"someone was mid-edit on.", file=sys.stderr)
            return 3
    ack = {
        "seat": seat,
        "gen_after": args.gen,
        # The ack carries the ListAgents ref the successor NAMED, or nothing.
        # SL1.06 kid 3 wrote `ref or self_sid` here (and back-filled the row
        # with the session uuid on the no-ref path) so the post-join announce
        # could compose an address — but the uuid is not an address a peer
        # can message (ListAgents shows `name [ref]`, never the uuid), so the
        # alert would have printed `name [27179681-…]`. Director fix-up at
        # the harvest: an ack without --ref leaves session_ref EMPTY and the
        # alert says pre-join, which is the truth — the ListAgents ref only
        # arrives when the successor names it (F8: ListAgents + ack).
        "session_ref": ref,
        "answer": args.answer,
        "text": text or "",
        "ts": datetime.utcnow().isoformat() + "Z",
    }
    path = _ack_path(root, seat)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ack, indent=2) + "\n", encoding="utf-8")
    print(f"ack written: {path}")
    # r3: back-fill session_ref into the successor's OWN seats row through the
    # self_row write (source: ack), so a later whois can authorize by it —
    # only from a validated --ref; the row already carries its session_id
    # (written by the JOIN at spawn), so there is nothing to back-fill on the
    # no-ref path. A THROWAWAY seat has no row; the back-fill is recorded
    # skipped and the ack still lands.
    if ref:
        # MERGE-UP 41 RESOLUTION (sanctuary-director 195718Z, prime XI's
        # ordering line 21:0xZ: KEEP BOTH halves -- L4.288's join-by-@id
        # back-fill of pid+session_id and SL4.03's commits-its-own-row +/-
        # lines; neither is a superset). The JOIN runs first and decides
        # whether anything changed; SL4.03's "already" short-circuit applies
        # only when neither the ref nor an identity cell differs.
        try:
            # L4.288 (the stale-pid hazard, FIX-ONLY): besides back-filling
            # session_ref, an ack ALSO resolves the successor's OWN identity
            # (pid + session_id) and pins its meter. Source is EXCLUSIVELY the
            # EXISTING JOIN keyed on the row's own `window` @id (L4.114: the
            # @id is the load-bearing key) — never ppid-walking, never the
            # newest registry file, never re-implemented. A recovered row
            # (`heal.py _recover_seat`) carries the DEAD pid and a blanked
            # session_id; this is where the successor's real identity lands so
            # a later pass that trusts the row's pid reads the LIVE seat.
            row = _find_seat(id_root, seat)
            window_id = (row.get("window") or "") if row else ""
            join = _join_successor(
                root=root, seat=seat, window_id=window_id or None,
                registry_dir=getattr(args, "registry_dir", None),
                poll_secs=ACK_JOIN_POLL_S)
            got_session_id = str(join.get("session_id") or "") if join.get(
                "found") else ""
            got_pid = join.get("pid") if join.get("found") else None
            # write pid/from the JOIN ONLY when it DIFFERS from the row's, and
            # session_id only when it is non-empty and DIFFERS — so a
            # rotate-self-shaped row (pid + session_id already seated) ends
            # byte-identical except session_ref.
            have_row = row is not None
            back_pid = (got_pid if (have_row and got_pid is not None
                                    and got_pid != row.get("pid")) else None)
            back_sid = (got_session_id if (have_row and got_session_id
                                           and got_session_id != (row.get(
                                               "session_id") or ""))
                        else None)
            # r3b (SL4.03): a back-fill that changed NOTHING (the row already
            # carries this ref AND the join changes no identity cell) SKIPS
            # the write + commit entirely and says so in one line —
            # write.submit's own metadata churn would otherwise dirty seats.md
            # for no row change (falsifier 3: nothing committed, one line
            # says it).
            already = (have_row
                       and (row.get("session_ref") or "") == ref
                       and back_pid is None and back_sid is None)
            if already:
                print(f"ack: {seat} row already carries session_ref={ref} — "
                      "nothing to back-fill or commit")
            else:
                # ONE outcome line per cell group: the single `write.submit`
                # carries whichever of session_ref/pid/session_id differs,
                # and the helper's own outcome line ALWAYS prints (F8: the
                # ack PRINTS the back-fill it wrote — a join miss must not
                # silence the session_ref line; director fix-up at the
                # L4.288 harvest). A hit appends the @id it joined by.
                line = _backfill_session_ref(
                    root, seat=seat, role="parent", ref=ref, pid=back_pid,
                    session_id=back_sid)
                if join.get("found") and line.endswith("(source: ack)"):
                    line = f"{line[:-1]}, joined by @{window_id.lstrip('@')})"
                print(line)
            if join.get("found"):
                # The meter pin is the lease (prime XI 19:38Z): pin the
                # successor's OWN transcript from the JOIN, but ONLY when no
                # pin exists — never overwrite an EXISTING pin.
                trans = join.get("transcript") or ""
                if trans:
                    pinp = _sessions_dir(root) / f"{seat}{METER_PIN_EXT}"
                    if pinp.exists():
                        print(f"meter pin present (untouched): {pinp}")
                    else:
                        pin_path = _pin_successor_meter(
                            root, seat=seat, generation=args.gen,
                            transcript=trans)
                        print(f"meter pinned: {pin_path}")
            else:
                # join miss: pid/session_id/pin left UNTOUCHED, the ref back-
                # fill (if any) still lands, the ack still returns 0.
                print(f"join: {join.get('note')}")
            # r3b (SL4.03): `continue` (no --no-commit) commits the row it
            # just wrote and prints the +/- lines + the exact `git push`
            # line; `--no-commit`/`diff` leave the working tree as today
            # (write + print, no commit). Nothing written -> nothing to
            # commit.
            if do_commit and not already:
                # SL2#9 seam: L4.291's id_root (the identity root, MAIN) with
                # SL5.08's failure path (stderr + unstage + exit 3).
                _ok, _out = _ack_commit_seats(id_root, seat, args, ref)
                if _ok:
                    print(_out)
                else:
                    # a failed ack commit (git add OR git commit) printed its
                    # error here, on STDERR, and UNSTAGED the row; cmd_ack
                    # exits 3 so the failure is visible and the NEXT ack's
                    # dirty gate (_ack_seats_dirty) finds seats.md clean
                    # again, not staged.
                    print(_out, file=sys.stderr)
                    return 3
        except Exception as exc:  # noqa: BLE001
            print(f"warn: session_ref back-fill failed: {exc}",
                  file=sys.stderr)
    # A HAND launch (a seat the owner started directly, never through
    # spawn/seats-launch) is a first seating acked at --gen 1 (no predecessor):
    # record it and send the SAME rotation-alert dm a rotation emits — but
    # ONLY when no seating record already exists for this seat + generation,
    # so a spawn/seats-launch that already recorded + announced is never
    # double-sent (hypothesis:l4-a-first-seating-sends-the-sensei-the-same-
    # alert-a-rotation-does; the falsifier: a second dm for the same seat+gen).
    # g15.24: the announce gate uses the SAME predicate as do_commit (_ack_commits),
    # NOT a literal `answer == "continue"`, so a gen-1 answer of `diff` with EMPTY
    # text commits AND announces once (a `diff` with text commits nothing and, by
    # the same predicate, announces nothing). The double-send falsifier (a second
    # dm for the same seat+gen) still holds via _seating_record_exists.
    if args.gen == FIRST_SEATING_GEN \
            and _ack_commits(args.answer, text,
                             getattr(args, "no_commit", False)) \
            and not _seating_record_exists(root, seat, generation=args.gen) \
            and not _rotation_record_exists(root, seat) \
            and not _pending_ack_present:
        role = "parent"
        srow = _find_seat(root, seat)
        if srow is not None:
            role = srow.get("role") or "parent"
        try:
            _first_seating_announce(
                root, None,  # croot None -> resolved inside
                seat=seat, role=role, source="cmd_ack",
                tmux_session=DEFAULT_TMUX_SESSION,
                window_path=getattr(args, "window_path", None),
                ref=ref,
                session_id=(srow.get("session_id") or "") if srow else "",
                transcript_path=((srow.get("transcript_path") or "")
                                 if srow else ""),
                registry_dir=getattr(args, "registry_dir", None))
        except Exception as exc:                        # noqa: BLE001
            print(f"warn: first-seating announcement failed: {exc}",
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
        seat=getattr(args, "seat", None),
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
        # A `diff` with a NON-EMPTY text means the handoff needs change: halt it
        # for inspection (result: diff). A `diff` with an EMPTY/whitespace text is
        # the reviewed-no-change answer the --ask-diff gate names — the handoff
        # STANDS exactly like a `continue`
        # (hypothesis:l4-the-ask-diff-gate-offers-no-continue-and-an-empty-
        # diff-stands-the-handoff).
        if answer == "diff" and (ack.get("text") or "").strip():
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
        # answer == continue, OR diff with an EMPTY text: the handoff stands.
        reply = "diff-empty" if answer == "diff" else "continue"
        _write_rotation_record(root, _loop_record(
            name=name, result="success", succ=succ,
            readback_log=Path(ack_path).expanduser().resolve(),
            reply_decision=reply))
        print("handoff stood: successor acked an EMPTY diff (no change)."
              if reply == "diff-empty"
              else "handoff stood: successor acked `continue`.",
              file=sys.stderr)
        import send  # local: same dir
        _announce_rotation(
            root=root,
            croot=send.comms_root(root, getattr(args, "comms_root", None)),
            seat=ack_seat, successor=name, gen_before=None, gen_after=None,
            trigger="--force" if getattr(args, "force", False) else "meter due",
            handoff_path=str(Path(ack_path).expanduser().resolve()),
            in_flight=("successor acked `diff-empty`; handoff stood"
                       if reply == "diff-empty"
                       else "successor acked `continue`; handoff stood"),
            live_names=succ.get("names", []),
            # mechanism 1: the successor's ack carries its OWN ref back-filled
            # from the JOIN (cmd_ack r3), so this post-ack announce composes
            # the FULL post-join address `name [ref] @window` for every peer.
            successor_ref=(ack.get("session_ref") or ""),
            successor_window=_successor_window_id(
                name, tmux_session, args.window_path) or "")
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


def _record_is_terminal_text(text: str) -> bool:
    """True when the rotation record bytes have a present s12_self_reap
    section — the terminal sentinel `--wait` polls for (L4.233).
    Best-effort: text that does not parse is not terminal."""
    try:
        doc = json.loads(text)
    except Exception:  # noqa: BLE001
        return False
    return isinstance(doc.get("s12_self_reap"), dict)


def _poll_record_terminal(path, deadline: float) -> tuple[bool, str]:
    """Poll `path` at a <=2s interval until its s12_self_reap section is
    present, or `deadline` (a monotonic instant) passes. Returns
    (terminal, last_seen_text). One read per tick: the text this function
    reads is the text it parses. When the record is already terminal on the
    first read it returns True immediately — never sleeps past an
    already-terminal record."""
    last = ""
    while True:
        try:
            last = Path(path).read_text(encoding="utf-8")
        except OSError:
            last = ""
        if _record_is_terminal_text(last):
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
        files = _rotation_record_files(root, seat)
        latest = files[-1] if files else None
        wait = int(getattr(args, "wait", 0) or 0)
        if wait > 0:
            # hypothesis:l4-status-wait-waits-for-the-record-to-appear —
            # the wait deadline covers BOTH phases: the record appearing
            # (a successor's first seconds may run before the predecessor
            # writes it) and that record reaching its terminal section.
            deadline = time.monotonic() + max(0, wait)
            if latest is None:
                # wait for a record to APPEAR within the same deadline
                while True:
                    files = _rotation_record_files(root, seat)
                    if files:
                        latest = files[-1]
                        break
                    if time.monotonic() >= deadline:
                        print(f"ERR: no rotation record for {seat} "
                              f"after {wait}s", file=sys.stderr)
                        return 2
                    time.sleep(min(2.0, max(0.05,
                                            deadline - time.monotonic())))
            terminal, last_txt = _poll_record_terminal(latest, deadline)
            if not terminal:
                print(f"# latest rotation record: {latest.name}")
                print(last_txt, end="")
                print(f"ERR: still not terminal after {wait}s",
                      file=sys.stderr)
                return 2
        if latest is not None:
            try:
                print(f"# latest rotation record: {latest.name}")
                print(latest.read_text(encoding="utf-8").rstrip())
            except OSError as exc:
                print(f"ERR: could not read latest record: {exc}",
                      file=sys.stderr)
                return 1
        else:
            print(f"(no rotation record for {seat})")
        print(f"sequence={_current_sequence(root)}")
        row = _find_seat(root, seat)
        if row is None:
            print(f"(no seats row for {seat})")
        else:
            gen = _read_generation(root, seat)
            frac = _seat_fraction(root, row)
            frac_str = "?" if frac is None else f"{frac:.3f}"
            print(f"row: {seat}\tgen={gen}\tfrac={frac_str}")
        # Sensei 182119Z audit (relayed via sensei-director L2): the one hand
        # call left above the wake floor was a fetch + behind check, because
        # F9's "the refusal IS the behind check" was not trusted. The record
        # read prints it instead, from the tree as it stands (no fetch: what
        # the seat's own git knows now), n/a when git cannot answer.
        _sb = season_branch(root)
        behind = _git_count_maybe(root, "rev-list", "--count",
                                  f"HEAD..origin/{_sb}")
        print(f"behind origin/{_sb}: "
              f"{'n/a' if behind is None else behind}")
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
    """The geometry config `posts:`/`seats:` rows (config:posts, post-first
    with a one-season config:seats fallback), or [] when absent/unparseable.
    Shared resolver: geometry_config.load_rows."""
    return geometry_config.load_rows(root)


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
        # A first seating is a rotation without a predecessor
        # (hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor):
        # seats-launch is a FIRST seating for each seat it brings up (gen 1,
        # no predecessor), so it runs the SAME template `startup.first_turn`
        # rotate-self runs and appends the composed `## STARTUP OUTPUT` block
        # to the seat's first input. Fail-soft: a role with no template or no
        # first_turn yields the empty string (byte-identical to before).
        startup_block, first_turn = _first_seating_run(
            root, seat=name, role=tier, succ_name=name,
            tmux_session=tmux_session, dry_run=args.dry_run)
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
            extra=startup_block,
            seat=name,
            successor_argv=getattr(args, "successor_argv", None),
        )
        if rc != 0:
            print(f"ERR: launch failed for seat {name!r} (rc={rc})",
                  file=sys.stderr)
            rc_all = 1
            continue
        # A first seating sends the Sensei the same alert a rotation does
        # (hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-
        # rotation-does): each newly-seated seat emits trigger: first-seating
        # + writes its gen-1 seating record. Non-fatal — never fails the
        # seating.
        if not args.dry_run:
            try:
                _first_seating_announce(
                    root, None,  # croot None -> resolved inside
                    seat=name, role=tier, source="cmd_seats_launch",
                    tmux_session=tmux_session,
                    window_path=getattr(args, "window_path", None),
                    first_turn=first_turn,
                    registry_dir=getattr(args, "registry_dir", None))
            except Exception as exc:                        # noqa: BLE001
                print(f"warn: first-seating announcement failed: {exc}",
                      file=sys.stderr)
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


def _seat_row_generation(root: Path | None, name: str) -> int | None:
    """The seat's OWN `generation` field from its config:seats row, or None
    when the seat has no live row or its row carries no generation. THE
    AUTHORITY: the row is what rotate-self writes at spawn and the ack
    back-fills (hypothesis:l4-the-prepare-captives-measure-generation-
    upstream-and-season-and-the-gate-is-not-a-test-seam)."""
    row = _find_seat(root, name) if root is not None else None
    if not row:
        return None
    g = row.get("generation")
    if isinstance(g, int):
        return g
    if g is None:
        return None
    try:
        return int(str(g))
    except (TypeError, ValueError):
        return None


def _generation_measured(root: Path, name: str) -> tuple[int, bool, str]:
    """The seat's CURRENT generation (row FIRST, handoff header as fallback)
    and whether it is measured at all.

    Returns (gen, measured, source). source is a short label for the check
    line. measured=False when NEITHER the config:seats row nor the handoff
    header carries a generation — an unmeasurable seat the prepare captive
    prints as `ok (generation unmeasured: no row, no handoff)`, never
    silently passes with cur_gen=0."""
    g = _seat_row_generation(root, name)
    if g is not None:
        return g, True, "config:seats row"
    hp = _seat_hands(root) / f"{name}.handoff.md"
    if not hp.exists():
        return 0, False, ""
    try:
        txt = hp.read_text(encoding="utf-8", errors="replace")
        for line in txt.splitlines():
            ls = line.strip()
            if ls.startswith("generation:"):
                v = ls.split(":", 1)[1].strip()
                return max(0, int(v)), True, "handoff header"
    except (OSError, ValueError):
        pass
    return 0, False, ""


def _read_generation(root: Path, name: str) -> int:
    """The seat's generation, or 0 when unmeasurable (no config:seats row
    generation, no handoff header). Row-first; the handoff is only the
    fallback."""
    gen, measured, _ = _generation_measured(root, name)
    return gen if measured else 0


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
                               gen_after: int | None = None,
                               template_source: str | None = None) -> None:
    """Write/refresh the IN-PROGRESS rotate-self record.

    `result` stays `started` until the rotation reaches an outcome (success or
    refused) and `steps_reached` records which steps have completed, so an
    interrupted rotation leaves a record whose state says exactly where it
    stopped (hypothesis:l4-rotation-record-survives-interruption). Overwrites
    `path` in place; the process keeps writing to the SAME file.
    `template_source` names which TREE the rotation template came from (the
    worktree's own, or the integration tree served because the worktree's
    geometry was stale) — mechanism 3, so a spawn is attributable.
    """
    rec: dict = {
        "rotation": "rotate-self",
        "seat": seat,
        "recorded_at": datetime.utcnow().isoformat() + "Z",
        "result": "started",
        "steps_reached": sorted(steps),
    }
    if template_source is not None:
        rec["template_source"] = template_source
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
                        steps_reached: list[str] | None = None,
                        reply_decision: str | None = None) -> dict:
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
    if reply_decision is not None:
        obs["d_reply_decision"] = reply_decision
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


def _successor_address(name: str, ref: str = "",
                       window: str = "") -> str:
    """The successor's callable address for a rotation alert, composed AFTER
    the join has resolved it: `name [ref] @window`.

    Pre-join (the successor has not yet acked a ref — the ListAgents `@id`
    from the JOIN) the alert NAMES that it is pre-join rather than silently
    dropping the ref a peer would need to reach it. The window `@id` is
    appended only when a tmux `@<N>` is actually known (the internal-seam
    path has none).
    """
    # a tmux window id already carries its `@` (`@291`); never double it
    # (Sensei 182119Z audit: the live alert read `@@291`).
    window = str(window or "").lstrip("@")
    if ref:
        addr = f"{name} [{ref}]"
        if window:
            addr += f" @{window}"
        return addr
    # PRE-JOIN: the ref is exactly the join fact that has not resolved yet.
    if window:
        return (f"{name} @{window} (pre-join: successor ref "
                f"not yet resolved)")
    return f"{name} (pre-join: successor ref not yet resolved)"


def _compose_announcement(*, seat, successor, gen_before, gen_after,
                          trigger, handoff_path, in_flight, seq=0,
                          successor_ref: str = "",
                          successor_window: str = "") -> str:
    """The five-field announcement payload — one message, never more.

    Every field is spelled because each has already cost a peer a turn: the
    outgoing seat, the successor address (`name [ref] @window` once the join
    has resolved the ref — hypothesis:l4-a-rotation-costs-the-live-seats-
    zero-calls-and-the-successor-one, mechanism 1; a pre-join alert names
    that it is pre-join), generation before/after, the trigger (meter due /
    --force / fable-limit), and the handoff path the successor is reading,
    plus one line of what is in flight so a peer can tell whether its own
    round is orphaned.
    """
    addr = _successor_address(successor, successor_ref, successor_window)
    return (f"{ROTATION_ALERT_TAG} {seat} -> {addr} | "
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
                       in_flight: str, live_names: list[str],
                       successor_ref: str = "",
                       successor_window: str = "",
                       seating: dict | None = None,
                       ask_diff: bool = False) -> list[str]:
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
    if seating is not None:
        # A FIRST SEATING: the ONE seating record is written here, at the same
        # moment the alert is emitted, so the alert and the record provably
        # share a single record (hypothesis:l4-a-first-seating-sends-the-
        # sensei-the-same-alert-a-rotation-does, g15.17 item 3).
        _write_seating_record(root, seating)
        text = _compose_seating_announcement(
            seat=seat, window_id=seating.get("window_id") or "",
            ref=seating.get("ref") or "",
            pid=seating.get("pid"),
            session_id=seating.get("session_id") or "",
            transcript_path=seating.get("transcript_path") or "",
            seq=seq, in_flight=in_flight, ask_diff=ask_diff)
    else:
        text = _compose_announcement(
            seat=seat, successor=successor, gen_before=gen_before,
            gen_after=gen_after, trigger=trigger, handoff_path=handoff_path,
            in_flight=in_flight, seq=seq, successor_ref=successor_ref,
            successor_window=successor_window)
    declared = "first seating" if seating is not None else "rotation"
    receivers = _derive_receivers(root, seat=seat, live_names=live_names)
    if seat == send.PRIME or seat.startswith(send.PRIME + "-"):
        # CLAUSE 1 (hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-
        # coalesced-nudge-still-wakes-and-detected-records-dedupe): the room
        # is NOT the petition's inbox -- `send.py read` reads
        # `<sessions>/inbox/<seat>.md`, a different file -- so a prime-specific
        # write is needed for the alert to satisfy "lands in the inbox". The
        # prime is inbox-only, but send.send() imposes no prime restriction
        # (only dm/room do), so it is the exact inbox-only path: land the SAME
        # [rotation-alert] block in the prime's OWN inbox in addition to the
        # shared alert-room post.
        try:
            send.send(root, seat, text, sender=seat)
            path = send.send_room(croot, ROTATION_ALERT_ROOM, text,
                                  sender=seat)
            print(f"announced {declared} -> {ROTATION_ALERT_ROOM} ({path})",
                  file=sys.stderr)
            return [ROTATION_ALERT_ROOM]
        except SystemExit as exc:
            print(f"warn: {declared} announcement to {ROTATION_ALERT_ROOM!r} "
                  f"failed: {exc}", file=sys.stderr)
            return []
    delivered = []
    for recv in receivers:
        try:
            # CLAUSE 1: land the SAME [rotation-alert] block in the
            # recipient's INBOX (`<sessions>/inbox/<recv>.md`, the writer
            # `send.send` uses -- the reader `send.py read <recv>` shows)
            # IN ADDITION to the pairwise dm log, so an alert is never
            # absent from a recipient's inbox and nothing depends on the
            # nudge (it is delivery, the inbox is the record). send() also
            # physically types its own wake; send_dm adds the dm-log block
            # plus its own pane line. A `send.py send` to the prime would be
            # rejected downstream but send() itself has no prime restriction,
            # so this stays the non-prime loop.
            send.send(root, recv, text, sender=seat)
            send.send_dm(croot, seat, recv, text, sender=seat)
            delivered.append(recv)
        except SystemExit as exc:
            print(f"warn: could not dm {recv!r} the {declared}: {exc}",
                  file=sys.stderr)
            continue
    print(f"announced {declared} -> {len(delivered)} recipient(s) "
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


# ── first-seating announcement ────────────────────────────────────────────
# (hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-
# does, goal:g15.17) A FIRST seating — a brand-new seat through `spawn` /
# `seats-launch`, or a HAND launch acked at `--gen 1` (no predecessor) —
# emits the SAME `[rotation-alert]` dm a rotation emits, with `trigger:
# first-seating` and generation `0 -> 1`, so the Sensei's live-seat nudge
# covers a new seat starting up exactly as it covers a rotation happening.
# The seating is recorded as ONE durable `<sessions>/rotations/<seat>.<TS>`
# `.seating.json` (same dir as rotation records), carrying the first_turn
# results; `_announce_rotation` writes it at the same moment it emits the
# alert, so the alert and the record provably share a single record.

#: The generation every first seating enters at (no predecessor).
FIRST_SEATING_GEN = 1

#: Bounded join poll for a first-seating's live pid/session/transcript.
#: Deliberately short — spawn is interactive and must not hang for a booting
#: seat; fields the sealed seat has not yet reported stay absent/honest.
FIRST_SEATING_JOIN_POLL_S = 3


def _seating_record(*, seat: str, role: str, source: str,
                    window_id: str | None, ref: str,
                    pid, session_id: str, transcript_path,
                    first_turn) -> dict:
    """One durable JSON seating record (rotation: 'seating'), generation
    `0 -> 1`, `trigger: first-seating`, carrying the nullable live fields a
    peer needs and the first_turn results — the record the alert shares.
    """
    rec = {
        "rotation": "seating",
        "seat": seat,
        "role": role,
        "source": source,
        "recorded_at": datetime.utcnow().isoformat() + "Z",
        "gen_before": 0,
        "gen_after": FIRST_SEATING_GEN,
        "trigger": "first-seating",
    }
    if window_id:
        rec["window_id"] = window_id
    if ref:
        rec["ref"] = ref
    if pid is not None:
        rec["pid"] = pid
    if session_id:
        rec["session_id"] = session_id
    if transcript_path:
        rec["transcript_path"] = str(transcript_path)
    if first_turn:
        rec["first_turn"] = first_turn
    return rec


def _write_seating_record(root: Path, record: dict) -> Path:
    """Write one JSON seating record under `.agi/sessions/rotations/`,
    named `<seat>.<UTC timestamp>.seating.json` — the SAME dir as rotation
    records, so `status --record` globs a seat's whole seating+rotation
    history. The `.seating.json` suffix (vs a rotation's plain `.json`)
    distinguishes a seating from a rotation in the shared dir. Returns the
    written path.
    """
    rot = _rotations_dir(root)
    rot.mkdir(parents=True, exist_ok=True)
    seat = str(record.get("seat") or "anonymous")
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    path = rot / f"{seat}.{stamp}.seating.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return path


def _seating_record_merge_handover(root: Path, record: dict) -> str:
    """Merge `record['handover']` into the ONE seating record already on
    disk for the same seat and `recorded_at`, in place.

    Claim (b) of hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-
    session-and-prints-its-row-commit-outcome: a hand seating's
    `_commit_spawn_row` outcome rides the seating record as
    `handover.seating_row_commit` (the seating mirror of a rotation's
    `handover.spawn_row_commit`), trailing `\npush:` line included, so the
    commit/push history lives on the record any later reader opens. The first
    seating's record is written by `_first_seating_announce` BEFORE the row
    commit, so the outcome is merged back in here once it exists. Idempotent:
    a record already carrying a handover is never double-merged; a missing or
    unmatched record is left alone. Returns the written path or ''."""
    seat = str(record.get("seat") or "")
    stamp = record.get("recorded_at")
    handover = record.get("handover") or {}
    if not seat or not handover:
        return ""
    rot = _rotations_dir(root)
    if not rot.is_dir():
        return ""
    target = None
    for p in rot.glob(f"{seat}.*.seating.json"):
        try:
            rec = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        if not isinstance(rec, dict):
            continue
        if rec.get("recorded_at") != stamp or rec.get("handover"):
            continue
        if target is None or p.stat().st_mtime >= target.stat().st_mtime:
            target = p
    if target is None:
        return ""
    try:
        rec = json.loads(target.read_text(encoding="utf-8", errors="replace"))
        if not isinstance(rec, dict):
            return ""
        merged = dict(rec.get("handover") or {})
        merged.update(handover)
        rec["handover"] = merged
        target.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError):
        return ""
    return str(target)


def _seating_record_exists(root: Path, seat: str,
                           generation: int = FIRST_SEATING_GEN) -> bool:
    """True when a seating record for `seat` at `generation` already exists.

    The ack --gen 1 dedup: a HAND-launch ack must NOT double-send a first-
    seating alert when a `spawn`/`seats-launch` already recorded (and
    announced) this seat's gen-1 seating — the falsifier "a second dm for the
    same seat + gen".
    """
    rot = _rotations_dir(root)
    if not rot.is_dir():
        return False
    for p in rot.glob(f"{seat}.*.seating.json"):
        try:
            rec = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        if rec.get("gen_after") == generation:
            return True
    return False


def _rotation_record_exists(root: Path, seat: str) -> bool:
    """True when `seat` already has a ROTATION record (a loop or rotate-self
    `.json`, never a `.seating.json`). rotate-self/loop write one BEFORE the
    successor joins, so a successor acking at gen 1 after a rotation is NOT a
    first seating — it belongs to a predecessor, and must not announce/write a
    second gen-1 seating record. A HAND launch (no spawn, no rotate-self)
    leaves none, so its ack stays a genuine first seating.
    """
    rot = _rotations_dir(root)
    if not rot.is_dir():
        return False
    for p in rot.glob(f"{seat}.*.json"):
        if p.name.endswith(".seating.json"):
            continue
        return True
    return False


def _pending_ack_exists(root: Path, seat: str) -> bool:
    """True when `seat` has a PENDING ack (`seats/<seat>.ack.json` carrying
    `answer: pending`). rotate-self writes that pending ack BEFORE its
    successor joins (F8's contract), so its successor acking at gen 1 has a
    predecessor — NOT a first seating. A HAND-launched seat has no ack file,
    so its ack stays genuine.
    """
    p = _ack_path(root, seat)
    if not p.exists():
        return False
    try:
        ack = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return False
    return isinstance(ack, dict) and ack.get("answer") == "pending"


def _seating_in_flight(first_turn) -> str:
    """One line of what the first seating ran, for the alert's `in flight`."""
    if not first_turn:
        return "first seating booting; no first_turn ran"
    done = sum(1 for r in first_turn if r.get("rc") is not None)
    refused = sum(1 for r in first_turn if r.get("refused"))
    if refused:
        return f"{done} first_turn step(s) ran, {refused} refused"
    return f"{done} first_turn step(s) ran"


def _compose_seating_announcement(*, seat, window_id: str = "", ref: str = "",
                                  pid=None, session_id: str = "",
                                  transcript_path: str = "",
                                  seq: int = 0,
                                  in_flight: str = "",
                                  ask_diff: bool = False) -> str:
    """The first-seating `[rotation-alert]` payload — one message, never more.

    Carries seat, window @id, ref (when the join has it, else the NAMED
    `ref: (pending ack)` — never a silently-dropped address a peer could not
    reach), the bounded pid, session id and transcript path (absent fields
    render as `-`, honest pre-join), the durable sequence number, and what is
    in flight. Pure formatting; runs nothing.

    WITH `--ask-diff` (SL7.06's answer contract, reused never a third shape)
    the alert appends the successor's ONE wake call -- the exact
    `rotate.py ack --seat S --gen 1 --ref <ref> diff --text -` line, NEVER
    `--gen 0`, never a bare `(pending ack)` without the line (the seating
    falsifier "an alert that says generation 0 -> 1 with no ack line or with
    --gen 0").
    """
    w = str(window_id or "").lstrip("@")
    addr = seat
    if w:
        addr += f" @{w}"
    if ref:
        addr += f" [{ref}]"
    else:
        addr += " ref: (pending ack)"
    pid_s = str(pid) if pid is not None else "-"
    body = (f"{ROTATION_ALERT_TAG} first seating {addr} | "
            f"generation 0 -> {FIRST_SEATING_GEN} | "
            f"trigger: first-seating | pid: {pid_s} | "
            f"session: {session_id or '-'} | "
            f"transcript: {transcript_path or '-'} | seq: {seq} | "
            f"in flight: {in_flight}")
    if ask_diff:
        _ref = ref or "<your ListAgents ref>"
        body += (f"\nrotate.py ack --seat {seat} --gen {FIRST_SEATING_GEN} "
                 f"--ref {_ref} diff --text -")
    return body


def _first_seating_announce(root: Path, croot, *, seat: str, role: str,
                            source: str, tmux_session: str,
                            window_path: str | None = None,
                            ref: str = "", first_turn=None,
                            live_names=None, registry_dir=None,
                            pid=None, session_id: str = "",
                            transcript_path: str = "",
                            ask_diff: bool = False) -> list[str]:
    """Write the ONE seating record and emit the SAME rotation-alert dm a
    rotation emits (trigger: first-seating) to the derived live recipients.

    The window @id comes from `_successor_window_id` (the registry JOIN key,
    reused never re-implemented); live pid/session/transcript are taken from a
    BOUNDED join when not already supplied (a freshly-seated window usually
    has its `<pid>.json` registry file within seconds); otherwise they stay
    absent/honest. Delivery failure never fails the seating — the record is
    the proof, not a gate. Returns the SEATING RECORD dict that was written
    (the same object `_announce_rotation` wrote as `<seat>.<ts>.seating.json`)
    — the JOINED identity (window_id/pid/session_id/transcript_path) plus,
    after `cmd_spawn` commits the seating row, the `handover.seating_row_commit`
    outcome — so the seating block carries the joined identity and the commit
    history exactly as a rotation's handover does. A caller that only needs
    the announcement (cmd_ack / cmd_seats_launch) may discard it.
    """
    import send  # local: same dir
    if croot is None:
        croot = send.comms_root(root)
    live_list = (live_names if live_names is not None
                 else _existing_windows(tmux_session, window_path))
    window_id = _successor_window_id(seat, tmux_session, window_path)
    if window_id and pid is None and not session_id:
        join = _join_successor(root=root, seat=seat, window_id=window_id,
                               registry_dir=registry_dir,
                               poll_secs=FIRST_SEATING_JOIN_POLL_S)
        if join.get("found"):
            pid = join.get("pid")
            session_id = join.get("session_id") or ""
            transcript_path = join.get("transcript") or ""
    seating = _seating_record(
        seat=seat, role=role, source=source, window_id=window_id, ref=ref,
        pid=pid, session_id=session_id, transcript_path=transcript_path,
        first_turn=first_turn)
    in_flight = _seating_in_flight(first_turn)
    _announce_rotation(
        root=root, croot=croot, seat=seat, successor=seat,
        gen_before=0, gen_after=FIRST_SEATING_GEN,
        trigger="first-seating",
        handoff_path="first seating: no predecessor handoff",
        in_flight=in_flight, live_names=live_list,
        successor_ref=ref, successor_window=window_id or "",
        seating=seating, ask_diff=ask_diff)
    # the seating record IS a seating's handover: it carries the JOINED
    # identity (window_id/pid/session_id/transcript_path) and is where the
    # seating-row commit outcome (`handover.seating_row_commit`, claim (b) of
    # hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-session-and-
    # prints-its-row-commit-outcome) rides. Return it so `cmd_spawn` can
    # commit THAT identity and record the outcome into the same record.
    return seating


def _first_seating_spawn_writes(*, root: Path, seat: str,
                                generation: int = FIRST_SEATING_GEN,
                                transcript: str = "",
                                ask_diff: bool = False,
                                role: str = "prime_director",
                                session_id: str = "",
                                window: str = "",
                                pid: int | None = None) -> dict:
    """A spawn's rotate-self-step-2 TWO writes, for a FIRST seating
    (hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor): pin
    the seat's meter at ITS generation (the SAME `_pin_successor_meter`
    rotate-self uses, never a second pin format) and write
    seats/<seat>.ack.json with `answer: continue, source: seating` (F8's
    contract, the same `_write_ack`; the seating writer answers its OWN ack
    so a hand seating's post also wakes at 0 -- its alert/brief prints no ack
    line unless `--ask-diff`, which instead writes `answer: diff-requested,
    source: seating` and lets the hand seating print the ONE
    `rotate.py ack ... diff --text -` line). These are the SPAWN's writes --
    rotate-self step 2's -- NOT the autopsy's (which runs read-only only);
    they are the spawn occupying its own meter and opening its ack channel.

    Claim (2) of hypothesis:l4-the-spawn-gate-refuses...: a first seating
    ALSO writes its OWN identity row into MAIN (the same `_successor_row_write`
    rotate-self uses -- generation, session_id, window, pid into the seat's
    own seats row), so `cmd_spawn` can `_commit_spawn_row` it (the `seating
    row` commit) and `_commit_spawn_row` pushes through `_push_season_branch`
    -- a hand seating leaves MAIN clean, never a dirty row riding to the next
    merge-up. When the seat has no registry row (a THROWAWAY seat) the row
    write skips and there is nothing to commit; harmless.

    The transcript is the caller's known one -- EMPTY for a fresh first
    seating (there is no successor transcript from a JOIN yet); rotate-self
    repoints the pin at the successor's transcript when a rotation joins at
    gen 2. An empty-target pin is safe: `find_pin_log` still resolves it and
    `_read_pin_target` returns None until a transcript lands. Returns
    {meter_pin, ack_path, row}."""
    mp = _pin_successor_meter(root, seat=seat, generation=generation,
                              transcript=transcript)
    _answer = "diff-requested" if ask_diff else "continue"
    ap = _write_ack(root=root, seat=seat, gen_after=generation,
                    session_ref="", answer=_answer, source="seating")
    row = _successor_row_write(
        root, actor=seat, seat=seat, role=role, session_ref="",
        generation=generation, window=window, pid=pid,
        session_id=session_id)
    return {"meter_pin": mp, "ack_path": str(ap), "row": row}


def _remove_first_seating_record(root: Path, seat: str) -> bool:
    """Remove the pre-window first-seating bootstrap record for `seat`.

    The gen-1 bootstrap record is written by `_first_seating_run` (via
    `_write_bootstrap`) BEFORE the window spawn. If the spawn then FAILS, that
    record is a promise the seat never kept -- so `cmd_spawn` removes it on a
    non-zero spawn rc, leaving NO 'started' record behind and keeping
    `cmd_status --record latest` truthful (Prime XI line (7), second half).
    Removed rather than marked `result: failed` because the bootstrap record
    has no `result` field by shape, and a stale `pending: resolved after join`
    pointing at a seating that never came up is worse than an absent file.
    Best-effort, never raises. Returns True when a record was removed."""
    p = _sessions_dir(root) / "seats" / f"{seat}.bootstrap.json"
    try:
        if p.exists():
            p.unlink()
            return True
    except OSError:
        pass
    return False


# --- recovery seating: predecessor autopsy (hypothesis:l4-a-recovery-seating-
#      gets-its-predecessor-autopsy-pre-filled-from-files) --------------------
# The recovery successor otherwise reconstructs X's death by hand (Sensei's
# spawn-seating audit 175816Z: belam spent calls 3-9 + 14 on X's death, the
# helper 181834Z repaired an unresolved merge the spawn never named). Every
# one of those facts is on disk. This region prints them FROM FILES ONLY,
# read-only — the LLM still decides continue|diff.

#: the tag every autopsy line carries, so a reader can slice the block out.
AUTOPSY_TAG = "[autopsy]"
#: how many pre-death transcript entries to print for the predecessor.
AUTOPSY_LAST_ENTRIES = 10


def transcript_from_registry_dict(data: dict) -> str:
    """The Claude Code transcript path for a per-session registry dict.

    The ONE derivation, lifted out of `_join_successor` (was inline at
    rotate.py ~4606-4610): an explicit `transcript`/`transcript_path` wins;
    else `cwd` + `sessionId` derive `~/.claude/projects/<slug>/<sessionId>\n"
    `.jsonl` where slug = every '/' and '.' in cwd replaced by '-'. The
    autopsy and the join call this SAME helper — never a copy."""
    transc = str(data.get("transcript") or data.get("transcript_path") or "")
    sess = data.get("session_id") or data.get("sessionId") or ""
    if not transc and sess and data.get("cwd"):
        slug = str(data["cwd"]).replace("/", "-").replace(".", "-")
        transc = str(CC_PROJECTS_DIR / slug / f"{sess}.jsonl")
    return transc


def _registry_file_path(registry_dir: str | None, pid: int) -> Path | None:
    """`<registry_dir>/<pid>.json` (default `~/.claude/sessions`), or None."""
    p = Path(registry_dir or REGISTRY_DEFAULT_DIR).expanduser() / f"{pid}.json"
    return p if p.exists() else None


def _registry_read(registry_dir: str | None, pid: int) -> dict:
    """The parsed `<pid>.json` registry dict, or {} when absent/unreadable."""
    fp = _registry_file_path(registry_dir, pid)
    if fp is None:
        return {}
    try:
        data = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _pid_gone(pid: int) -> bool:
    """True when no live process owns `pid` — `/proc/<pid>` is the one
    liveness read the autopsy performs (read-only, never a signal)."""
    return not Path(f"/proc/{int(pid)}").exists()


def _death_timestamp(data: dict, transcript_path: Path | None) -> str:
    """The predecessor's death timestamp, from FILES ONLY: the registry json's
    `statusUpdatedAt`/`updatedAt` (ms epoch) else the transcript's mtime, else
    `-`. Source is named on the line so the reader can distinguish a measured
    death from a guess."""
    for key in ("statusUpdatedAt", "updatedAt"):
        v = data.get(key)
        if v not in (None, ""):
            try:
                ms = int(v)
                return datetime.utcfromtimestamp(ms / 1000.0).strftime(
                    "%Y-%m-%dT%H:%M:%SZ")
            except (ValueError, TypeError, OSError):
                return str(v)
    if transcript_path is not None and transcript_path.exists():
        return datetime.utcfromtimestamp(transcript_path.stat().st_mtime)\
            .strftime("%Y-%m-%dT%H:%M:%SZ")
    return "-"


def _iter_assistant_entries(path: Path, until_ts: str | None = None):
    """Yield `(ts, summary)` for every assistant text/tool_use content block in
    a CC JSONL transcript, in file order, optionally bounded at or before
    `until_ts`. A heartbeat line is neither assistant text nor tool_use and is
    skipped by construction. `_summarize_tool_input`-shaped summaries (imported,
    never copied)."""
    try:
        import sensei
    except Exception:  # pragma: no cover - sibling import, degrade silently
        sensei = None
    from datetime import datetime as _dt

    def _norm(ts):
        if not ts:
            return None
        s = str(ts)
        try:
            s = s.replace("Z", "+00:00").replace(" ", "T")
            if "+" not in s and "-" not in s[10:]:
                s += "+00:00"
            return _dt.fromisoformat(s)
        except ValueError:
            return None

    bound = _norm(until_ts)
    try:
        fh = open(path, encoding="utf-8", errors="replace")
    except OSError:
        return
    with fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") != "assistant":
                continue
            content = ev.get("message", {}).get("content")
            if not isinstance(content, list):
                continue
            ts = ev.get("timestamp") or (ev.get("message") or {}).get("timestamp")
            ts = str(ts) if ts else None
            if bound is not None and ts is not None:
                nts = _norm(ts)
                if nts is not None and nts > bound:
                    continue
            for b in content:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "text" and b.get("text"):
                    summ = " ".join(str(b["text"]).split())
                    summ = summ[:110] + ("…" if len(summ) > 110 else "")
                    yield ts, f"text: {summ}"
                elif b.get("type") == "tool_use":
                    inp = b.get("input") or {}
                    summ = (sensei._summarize_tool_input(inp) if sensei
                            else str(inp)[:110])
                    yield ts, f"tool_use {b.get('name', '?')}: {summ}"


def _latest_service_output_log(root: Path) -> Path | None:
    """The persistent healer/service `output.log` (heal.py `healer_dir /
    "output.log"`): the newest `*/output.log` under the sessions dir."""
    sess = _sessions_dir(root)
    if not sess.is_dir():
        return None
    cands = sorted(sess.rglob("output.log"), key=lambda p: p.stat().st_mtime)
    return cands[-1] if cands else None


def _reaper_log_path(root: Path) -> Path | None:
    """Resolve the reaper log: `AGI_REAPER_LOG` env first, else the
    `config:crons` node's `services.agi-reaper.environment.AGI_REAPER_LOG`,
    else `~/logs/agi-reaper-<hash>.log` — the hash is NEVER hardcoded here."""
    env = os.environ.get("AGI_REAPER_LOG")
    if env:
        return Path(env)
    node = Path(root) / "nodes" / ".geometry" / "crons.md"
    if node.exists():
        text = node.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"AGI_REAPER_LOG:\s*(\S+)", text):
            return Path(m.group(1))
    expanded = Path.home() / "logs"
    if expanded.is_dir():
        cands = sorted(expanded.glob("agi-reaper-*.log"),
                       key=lambda p: p.stat().st_mtime)
        if cands:
            return cands[-1]
    return None


def _reaper_lines_for(pid: int, sources: list[tuple[str, Path | None]]) -> list[tuple[str, str]]:
    """Every line (labelled by source) naming `pid` in the reaper/service logs."""
    out: list[tuple[str, str]] = []
    for label, path in sources:
        if path is None or not path.exists():
            continue
        try:
            for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
                if str(pid) in ln:
                    out.append((label, ln.strip()))
        except OSError:
            continue
    return out


def _seating_worktree_lines(root: Path, season: str | None = None) -> list[str]:
    """The three worktree-state facts read for BOTH every `[seating]` block and
    the autopsy — one helper, two callers (cmd_spawn tags the line `[seating]`,
    the autopsy re-tags it `{AUTOPSY_TAG}`). Reads only: `behind N` (rev-list
    count), `unresolved merge: yes|no` (`MERGE_HEAD` present), `dirty: <n>
    paths` (porcelain, cron churn excluded exactly as `_prepare_churn_path`
    does). Returns a single rendered line carrying all three facts. The season
    is never a literal: the default resolves through `season_branch(root)` at
    call time and is addressed as the remote ref `origin/{season}` (the same
    shape every other season reader in rotate.py uses), so a season change is
    ONLY the ladder's `current_season` (hypothesis:l4-the-prepare-captives-
    measure-generation-upstream-and-season-and-the-gate-is-not-a-test-seam)."""
    if season is None:
        season = season_branch(root)
    season = f"origin/{season}"
    behind = _git_count_maybe(root, "rev-list", "--count", f"HEAD..{season}")
    merge_head = _git_maybe(root, "rev-parse", "-q", "--verify", "MERGE_HEAD")
    unresolved = bool(merge_head)
    porcelain = _git_maybe(root, "status", "--porcelain") or []
    dirty = sum(1 for ln in porcelain if not _prepare_churn_path(ln))
    return [
        f"[seating] worktree: behind {season} "
        + (str(behind) if behind is not None else "n/a")
        + f" | unresolved merge: {'yes' if unresolved else 'no'}"
        + f" | dirty: {dirty} paths",
    ]


def _compose_seating_base_block(*, seat: str, source: str, now: str,
                                pred_pid, pred_death: str, seq: int,
                                root: Path | None = None) -> list[str]:
    """The first `[seating]` line every seating prints (spawned-by, predecessor
    pid + death ts, record / wrapper) — the fact block a recovery successor
    otherwise reconstructs by hand (Sensei 175816Z calls 3-9).

    The `record:` line says the FILE STATE, never a hardcoded `none`: a first
    seating announces (and WRITES) a gen-1 seating record moments after this
    line prints, so an unconditional `record: none` would read false to anyone
    who then finds the record on disk. With `root` given, `_seating_record_
    exists` decides `present` vs `none yet (this seating writes one)`; without
    `root`, the honest pre-announce wording is used."""
    if root is not None and _seating_record_exists(root, seat):
        rec = "record: present"
    else:
        rec = "record: none yet (this seating writes one)"
    pid_s = str(pred_pid) if pred_pid is not None else "none"
    return [
        f"[seating] spawned-by: {source} at {now} | "
        f"predecessor pid: {pid_s} died {pred_death} | "
        f"{rec} | wrapper: none | seq: {seq}",
    ]


def _run_autopsy(*, seat: str, pid: int, registry_dir: str | None,
                 root: Path, season: str | None = None) -> list[str]:
    """Render the full autopsy block for a predecessor `pid` of `seat`. Prints
    FROM FILES ONLY and runs read-only commands only. Returns the `[autopsy]`
    lines (the caller may tag them into the `[seating]` block or print them as
    `rotate.py autopsy`). The worktree season default resolves through
    `season_branch(root)` — never a hardcoded season literal."""
    if season is None:
        season = season_branch(root)
    lines: list[str] = []
    data = _registry_read(registry_dir, pid)
    alive = not _pid_gone(pid)
    lines.append(f"{AUTOPSY_TAG} seat: {seat}")
    lines.append(f"{AUTOPSY_TAG} predecessor pid: {pid} "
                 + (f"alive: yes" if alive else f"alive: no (gone)"))
    transc = data.get("transcript") or transcript_from_registry_dict(data) or ""
    transc_path = Path(transc).expanduser() if transc else None
    death = _death_timestamp(data, transc_path)
    if data.get("statusUpdatedAt") or data.get("updatedAt"):
        src = "registry updatedAt"
    elif transc_path is not None:
        src = "transcript mtime"
    else:
        src = "unmeasured"
    lines.append(f"{AUTOPSY_TAG} death time: {death} (source: {src})")
    lines.append(f"{AUTOPSY_TAG} transcript: {transc_path or '-'}")
    # last 10 non-heartbeat entries before death
    lines.append(f"{AUTOPSY_TAG} last {AUTOPSY_LAST_ENTRIES} non-heartbeat entries before death:")
    if transc_path is not None and transc_path.exists():
        entries = list(_iter_assistant_entries(transc_path, until_ts=death if death != "-" else None))
        for ts, summ in entries[-AUTOPSY_LAST_ENTRIES:]:
            lines.append(f"{AUTOPSY_TAG}   {ts or '-'} {summ}")
        if not entries:
            lines.append(f"{AUTOPSY_TAG}   (no assistant text/tool_use entries in transcript)")
    else:
        lines.append(f"{AUTOPSY_TAG}   (no transcript on disk)")
    # reaper + persistent service log lines naming the pid
    rlog = _reaper_log_path(root)
    slog = _latest_service_output_log(root)
    reaper = _reaper_lines_for(pid, [("reaper", rlog), ("service", slog)])
    lines.append(f"{AUTOPSY_TAG} reaper log: {rlog or 'unresolved'}")
    if slog:
        lines.append(f"{AUTOPSY_TAG} service output.log: {slog}")
    if reaper:
        for label, ln in reaper[-10:]:
            lines.append(f"{AUTOPSY_TAG}   reaper({label}): {ln}")
    else:
        lines.append(f"{AUTOPSY_TAG}   (no reaper/service line names pid {pid})")
    # launch: the seat's latest rotation record, or record: none
    rec = _latest_rotation_record(root, seat)
    if rec:
        ow = rec.get("handover", {}).get("own_window") or rec.get("own_window")
        sw = rec.get("handover", {}).get("successor_window") or rec.get("successor_window")
        lines.append(
            f"{AUTOPSY_TAG} launch: record <{seat}> "
            + f"own_window {ow or '-'} | successor_window {sw or '-'} | "
            + f"result {rec.get('result') or rec.get('trigger') or '-'}")
    else:
        lines.append(f"{AUTOPSY_TAG} launch: not recorded (record: none)")
    # worktree state
    lines.append(_seating_worktree_lines(root, season=season)[0].replace("[seating]", AUTOPSY_TAG))
    # probable cause: L4.281 signatures (a pane-local probe, or an external
    # TERM/HUP on an idle seat) — the LLM still decides continue|diff.
    cause = _probable_cause(reaper, transc_path, _iter_assistant_entries)
    if cause:
        sig, ev = cause
        lines.append(f"{AUTOPSY_TAG} probable cause: {sig} (evidence: {ev})")
    return lines


def _probable_cause(reaper: list[tuple[str, str]], transc_path: Path | None,
                    iter_entries) -> tuple[str, str] | None:
    """The L4.281 probable-cause signatures: an external TERM/HUP on an idle
    seat (a reaper/service line naming SIGTERM/SIGHUP for the pid) or a pane-
    local probe (the predecessor's own tmux/ps line in its last calls).
    Returns (signature, evidence line) or None when nothing matches."""
    for label, ln in reaper:
        if "SIGTERM" in ln or "SIGHUP" in ln or "terminated" in ln.lower():
            return "external TERM/HUP on idle seat", ln
    if transc_path is not None and transc_path.exists():
        for ts, summ in (iter_entries(transc_path) or []):
            low = summ.lower()
            if (" tmux " in low or low.startswith("tool_use tmux")) and "list-windows" in low:
                return "pane-local probe", summ
    return None


def cmd_autopsy(args: argparse.Namespace, root: Path | None) -> int:
    """`rotate.py autopsy --seat S [--pid P] [--registry-dir D]` — print the
    predecessor's death facts FROM FILES ONLY (read-only). Prints the full
    block and exits 0; never decides, kills, edits or merges."""
    seat = args.seat
    pid = args.pid
    registry_dir = getattr(args, "registry_dir", None)
    if pid is None:
        row = _find_seat(root, seat) if root is not None else None
        pid = (row or {}).get("pid")
    if pid is None:
        print(f"{AUTOPSY_TAG} seat: {seat}")
        print(f"{AUTOPSY_TAG} predecessor pid: unknown (no --pid and the seat row carries none)")
        return 0
    for ln in _run_autopsy(seat=seat, pid=int(pid), registry_dir=registry_dir,
                           root=root):
        print(ln)
    return 0


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


# --- driven handoff writer (hypothesis:l4-rotate-self-drives-the-handoff-
#     and-prepares-the-spawn, STEP 1) --------------------------------------
#
# `rotate.py handoff --driven --seat S [--field s3 SRC] [--field s6 SRC]`
# builds §0 of the seat's CARD (<sessions>/quorum/<S>.md — the file the LLM
# writes today) from MEASURED values only, prints the ONE bounded question
# (exactly §3 where-it-stops and §6 banked), reads the answers, and writes
# the card with §0 replaced, §3/§6 filled and every other section carried
# verbatim. The 5-line header file <sessions>/seats/<S>.handoff.md is never
# touched. This is the CAPTIVE/DRIVEN rule (goal:g15.14 §2): the script
# performs every mechanical read it can and asks the LLM only for the two
# judgements the successor must make. It never writes §3/§6 for the LLM —
# that is the falsifier, and it refuses instead.
#
#: The card-length guard — the EXISTING "keep it under 100 lines total" rule
#: (hypothesis:l3w4-context-load-minimal, RULE FIVE: "keep it under 100
#: lines total across all blocks for the fattest role"). A composed card
#: past this line count refuses, naming the section with the most lines to
#: cut. Found, not invented — the rule the graph already enforces by hand.
HANDOFF_CARD_LIMIT_LINES = 100


#: The two bounded judgements the driven writer asks the LLM for. Everything
#: else on the card is measured (STEP 1 pre-fills §0) or carried verbatim.
HANDOFF_ASKED_FIELDS = ("s3", "s6")


def _git_maybe(cwd: Path, *args: str) -> list[str] | None:
    """git in `cwd`, stdout lines, or None on ANY failure (not a repo, a
    missing remote ref, a network read). The driven writer degrades a
    measurement to `n/a` rather than failing the whole card on one absent
    read; a measurement no one can see is still a line the successor can
    trust says `n/a`."""
    try:
        out = subprocess.run(["git", "-C", str(cwd), *args],
                             capture_output=True, text=True)
    except Exception:  # noqa: BLE001
        # ANY refusal degrades to None — a real OSError/SubprocessError, or a
        # test fixture that fakes subprocess.run to raise on git (the
        # rotate-self candidate runs the checklist unconditionally now, so a
        # seam that refuses git must pass through as unmeasurable, never
        # propagate: hypothesis:l4-the-prepare-captives-measure-generation-
        # upstream-and-season-and-the-gate-is-not-a-test-seam, piece 2).
        return None
    if out.returncode != 0:
        return None
    return [ln for ln in out.stdout.splitlines() if ln]


def _rotation_record_files(root: Path, seat: str) -> list:
    """Every `<seat>.*.json` ROTATION record, newest-first in name order
    (filenames carry `YYYYMMDDTHHMMSSZ`), EXCLUDING `rotation:
    crash-recovery` records (hypothesis:l4-a-rotation-alert-lands-in-the-
    inbox-..., clause 3: status must never read a detected record — or any
    crash-recovery record — as a rotation). Files that do not parse are kept
    best-effort, exactly as the pre-existing reader behaved."""
    rot = _rotations_dir(root)
    if not rot.is_dir():
        return []
    out = []
    for p in sorted(rot.glob(f"{seat}.*.json"), key=lambda p: p.name):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            out.append(p)      # unparseable: keep (best-effort, as before)
            continue
        if isinstance(rec, dict) and rec.get("rotation") == "crash-recovery":
            continue           # a crash-recovery is NEVER a rotation
        out.append(p)
    return out


def _latest_rotation_record(root: Path, seat: str) -> dict | None:
    """The newest durable rotation record for `seat`
    (`<sessions>/rotations/<seat>.*.json`), or None when the seat has no
    record yet. Record filenames carry the stamp `YYYYMMDDTHHMMSSZ`, which
    sorts lexically, so the max by name is the newest. Crash-recovery records
    (a heal outcome, never a rotation) are EXCLUDED — clause 3: a `detected`
    record must never be read as the seat's rotation."""
    files = _rotation_record_files(root, seat)
    if not files:
        return None
    try:
        return json.loads(files[-1].read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _record_join(rec: dict) -> dict:
    """ONE accessor for a rotation record's successor-join identity, accepting
    BOTH record shapes (mur-SL2.13 part 6):
      - rotate-self:  `handover.join.{window_id,pid,session_id,transcript}`,
        with `handover.successor_window.id` as the window_id fallback
        (g15.26 (d): heal.py's widest read shape still resolves here).
      - crash-recovery: TOP-LEVEL `window_id` (the shape `_write_crash_recovery`
        writes), with `respawn_outcome.window` as the *successor-window*
        fallback. `respawn_outcome` NEVER contributes a `pid`: heal's
        `_rotation_identity` (which imports THIS accessor, g15.26 (d)) reads
        succ_pids from the identity surface the producer actually writes —
        top-level pid/session_id DO NOT exist on a real CRP, and the real
        successor pid rides in `respawn_outcome` (not the identity surface),
        so surfacing it would break heal's
        test_crash_recovery_record_roundtrip_real_producer (succ_pids must
        stay empty).
    Returns a flat dict of `{pid, window_id, session_id, transcript}` — keys
    present only when the record carries them — or {} for a record with no
    join identity (an OLDER record). pids are STR-COERCED (heal.py's
    `_rotation_identity` reads this same accessor and appends them as-is, so
    an integer pid must surface as `"222"`, not `222`). Never raises, never
    None members. heal.py imports THIS copy (g15.26 (d)) — ONE definition
    serves both modules, no same-named twin."""
    out: dict = {}
    # the recovered seat's own successor window (crash-recovery respawn);
    # never a pid -- that is NOT part of the identity surface (see docstring).
    ro = rec.get("respawn_outcome")
    if isinstance(ro, dict) and ro.get("window"):
        out["window_id"] = str(ro["window"])
    # top-level fields: the crash-recovery record puts window_id at TOP level.
    if rec.get("window_id"):
        out["window_id"] = str(rec["window_id"])
    if rec.get("pid") is not None:
        out["pid"] = str(rec["pid"])
    if rec.get("session_id"):
        out["session_id"] = str(rec["session_id"])
    # rotate-self shape: the RICHER handover.join.* wins when present.
    hov = rec.get("handover")
    if isinstance(hov, dict):
        jn = hov.get("join")
        if isinstance(jn, dict):
            if jn.get("window_id"):
                out["window_id"] = str(jn["window_id"])
            if jn.get("pid") is not None:
                out["pid"] = str(jn["pid"])
            if jn.get("session_id"):
                out["session_id"] = str(jn["session_id"])
            if jn.get("transcript"):
                out["transcript"] = str(jn["transcript"])
        # heal.py's widest read shape: successor_window.id names the same
        # successor window when handover.join carried no window_id.
        sw = hov.get("successor_window")
        if isinstance(sw, dict) and sw.get("id") is not None:
            out.setdefault("window_id", str(sw.get("id")))
    return out


def _handoff_record_facts(rec: dict) -> dict:
    """The four facts STEP 1 names the record for: gen (before/after), the
    successor's window @id, its pid, and the model_confirm verdict. Each
    degrades to None when the record does not hold it. The successor window
    + pid come through `_record_join` so a crash-recovery record (top-level
    window_id) yields them exactly as a rotate-self record would."""
    facts: dict[str, object] = {"gen_before": None, "gen_after": None,
                                "window": None, "pid": None,
                                "model_confirm": None}
    obs = rec.get("observations") or {}
    gen = obs.get("b_generation") if isinstance(obs, dict) else None
    if isinstance(gen, dict):
        facts["gen_before"] = gen.get("before")
        facts["gen_after"] = gen.get("after")
    join = _record_join(rec)
    if join:
        facts["window"] = join.get("window_id")
        facts["pid"] = join.get("pid")
    hov = rec.get("handover")
    if isinstance(hov, dict):
        mc = hov.get("model_confirm") or {}
        if isinstance(mc, dict):
            facts["model_confirm"] = mc.get("verdict")
    return facts


def _harvest_handoff_facts(root: Path, seat: str) -> dict:
    """MEASURE every value the driven handoff §0 carries, each degrading to
    a readable `n/a` rather than failing the card on one absent read. This
    is RULE FOUR of hypothesis:l3w4-context-load-minimal — the state card
    is GENERATED from live sources, never hand-maintained."""
    facts: dict[str, object] = {}
    facts["stamp"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # verification.py's last counts (verification imports rotate, so this is
    # a LAZY import — READ-ONLY, verification.py is never edited). The floor
    # numbers the kept-merge baseline stamped; the suite numbers when the
    # state already holds them.
    counts = None
    try:
        import verification  # noqa: E402 -- lazy: verification imports rotate
        counts = verification._read_state(root)
    except Exception:
        counts = None
    facts["counts_active"] = str(counts.get("active")) if (counts and counts.get("active") is not None) else None
    facts["counts_deprecated"] = str(counts.get("deprecated")) if (counts and counts.get("deprecated") is not None) else None
    suite = counts.get("suite") if counts else None
    if isinstance(suite, dict) and suite:
        facts["suite"] = " / ".join(f"{k}={v}" for k, v in suite.items())
    else:
        facts["suite"] = None

    # the latest rotation record: gen, window @id, pid, model_confirm.
    rec = _latest_rotation_record(root, seat)
    if isinstance(rec, dict):
        facts.update(_handoff_record_facts(rec))
    else:
        facts.update({"gen_before": None, "gen_after": None, "window": None,
                      "pid": None, "model_confirm": None})

    # branch + behind-count vs the season branch + unpushed commits.
    branch_lines = _git_maybe(root, "rev-parse", "--abbrev-ref", "HEAD")
    facts["branch"] = branch_lines[0] if branch_lines else None
    _sb = season_branch(root)
    facts["season"] = _sb
    behind = _git_maybe(root, "rev-list", "--count", f"HEAD..origin/{_sb}")
    facts["behind"] = behind[0] if behind else None
    ahead = _git_maybe(root, "rev-list", "--count", "@{u}..HEAD")
    facts["unpushed"] = ahead[0] if ahead else None

    # the meter fraction (the seat's own pin + pinned transcript) and the
    # seat's registry row.
    row = _find_seat(root, seat) or {}
    facts["fraction"] = _seat_fraction(root, row)
    facts["role"] = row.get("role")
    facts["model"] = row.get("model")

    # the account line (provisioning.py credit_balance, READ-ONLY). A read
    # that cannot complete (no key, a refused seam, a fixture) is n/a, never
    # a hard fail.
    bal = None
    try:
        import provisioning  # noqa: E402
        bal = provisioning.credit_balance(root)
    except Exception:
        bal = None
    if bal and len(bal) >= 3:
        total, used, remaining = bal[0], bal[1], bal[2]
        facts["account"] = (f"total=${total:.2f} used=${used:.2f} "
                            f"remaining=${remaining:.2f}")
    else:
        facts["account"] = None
    return facts


def _fmt_fact(facts: dict, key: str, label: str) -> str:
    v = facts.get(key)
    return f"- **{label}:** {v if v is not None else 'n/a'}\n"


def _compose_card_s0(seat: str, facts: dict) -> str:
    """The generated §0 state block. Every measurable value is pre-filled
    here; the LLM is asked only for §3/§6. `seat` is kept for provenance so
    the block names whose card it is."""
    gb, ga = facts.get("gen_before"), facts.get("gen_after")
    if gb is not None and ga is not None:
        gen_s = f"{gb}->{ga}"
    elif ga is not None:
        gen_s = str(ga)
    elif gb is not None:
        gen_s = str(gb)
    else:
        gen_s = None
    out = []
    out.append(f"## §0 STATE (driven — `rotate.py handoff --driven --seat {seat}`, {facts.get('stamp')})")
    out.append("")
    out.append(f"- **Rotation record:** gen {gen_s if gen_s is not None else 'n/a'}, "
               f"window {facts.get('window') or 'n/a'}, "
               f"pid {facts.get('pid') or 'n/a'}, "
               f"model_confirm {facts.get('model_confirm') or 'n/a'}.")
    out.append(f"- **Node counts (verify-count.json):** active "
               f"{facts.get('counts_active') or 'n/a'}, deprecated "
               f"{facts.get('counts_deprecated') or 'n/a'}."
               + (f" Suite {facts['suite']}." if facts.get("suite") else ""))
    out.append(f"- **Tree:** branch {facts.get('branch') or 'n/a'}, "
               f"behind {facts.get('season') or 'season/s?'} "
               f"{facts.get('behind') or 'n/a'}, "
               f"unpushed {facts.get('unpushed') or 'n/a'}.")
    fr = facts.get("fraction")
    out.append(f"- **Meter:** {fr if fr is not None else 'n/a'} · "
               f"role {facts.get('role') or 'n/a'} · "
               f"model {facts.get('model') or 'n/a'}.")
    out.append(f"- **Account:** {facts.get('account') or 'n/a'}.")
    out.append("")
    return "\n".join(out)


def _split_card_sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Split a card into `(preamble, [(header, body), ...])`.

    The preamble is every line before the first `## ` header (the single-`#`
    title, a carried owner rule, blank lines) — CARRIED VERBATIM, never
    dropped. Sections split on lines starting with `## `; each header keeps
    its `## ` prefix and its body is the exact raw span of lines below it up
    to the next `## ` (`_section_body`), so a re-join loses NO section-
    boundary blank line (goal:g15.25 residue (i))."""
    preamble: list[str] = []
    sections: list[tuple[str, str]] = []
    header: str | None = None
    body: list[str] = []
    for ln in text.splitlines():
        if ln.startswith("## "):
            if header is not None:
                sections.append((header, _section_body(body)))
            header = ln
            body = []
        else:
            if header is None:
                preamble.append(ln)
            else:
                body.append(ln)
    if header is not None:
        sections.append((header, _section_body(body)))
    return "\n".join(preamble), sections


def _section_body(raw_lines: list[str]) -> str:
    """The EXACT raw span of a `## ` section's body from its collected lines.

    `raw_lines` is the line list between this header and the next `## `
    header (or EOF): blank LINE separators are `""` entries, and the EOL
    newline that always precedes the next header line is the trailing
    `"\n"` this appends. This makes `_split_card_sections` + `_render_card`
    an EXACT inverse at section boundaries, so the stops writer re-emits
    the blank line(s) that separated sections instead of stripping them
    (goal:g15.25 residue (i)). An `""`-only span (a blank line between two
    headers with no body) decodes back to ONE blank via `splitlines()`
    below, and an empty section stays empty."""
    return "\n".join(raw_lines) + "\n"


def _join_body(lines: list[str]) -> str:
    """Join a rebuilt section-body line list back into a body STRING,
    keeping a trailing blank line (a final `""` element) visible to
    `_render_card`'s `body.splitlines()` — the inverse of `_section_body`.
    A bare `"\n".join` flattens a terminal `""` to a single newline, so a
    section's trailing blank (the separator before the next `## ` header)
    would otherwise be lost on replace; this restores it (goal:g15.25
    residue (i), the `###`-path and `##`-path rebuilds)."""
    body = "\n".join(lines)
    if lines and lines[-1] == "":
        body += "\n"
    return body


def _render_card(preamble: str,
                 sections: list[tuple[str, str]]) -> str:
    """Re-join a preamble and its `(header, body)` sections into one card
    document, each section's header then its body, one per line."""
    lines: list[str] = []
    if preamble:
        lines.append(preamble)
    for header, body in sections:
        lines.append(header)
        if body:
            lines.extend(body.splitlines())
    return "\n".join(lines) + "\n"


def _section_tag(header: str) -> str | None:
    """Which of §0 / §3 / §6 a `## ...` header names, or None. Headers like
    `## 🔴 §6 BANKED` still resolve to §6 (the token is searched, not the
    first word).

    **SL2.01 (hypothesis:l4-the-driven-handoff-writer-keys-on-declared-
    titles-and-writes-the-seats-own-card):** the driven writer keys on the
    § numerals only to know which DECLARED slot to fill — the sensei-
    director card's numerics are a DIFFERENT layout (§0 identity, §5 state)
    and the where-it-stops slot resolves by TITLE
    (`_locate_where_it_stops`), never a numeral. KEYS ON
    DECLARED TITLES first, never on these."""
    for tok in ("§0", "§3", "§6"):
        if tok in header:
            return tok
    return None


def _own_card_path(root: Path, seat: str) -> Path:
    """The seat's OWN card path, found in the worktree FIRST, MAIN's shared
    copy only when no own copy exists (hypothesis SL2.01 #3). Lifted out of
    `_prepare_checks` check 4 (the meter-stale card check) — ONE helper, both
    callers. `root` is the graph root (`<tree>/.agi`, as `find_project_root`
    returns it), so the seat's own card is `<tree>/.agi/sessions/quorum/
    <S>.md`; MAIN's shared copy lives under `_sessions_dir` (which routes
    through `git_common_root` to the main checkout)."""
    _own = [Path(root) / "sessions" / "quorum" / f"{seat}.md",
            Path(root) / ".agi" / "sessions" / "quorum" / f"{seat}.md"]
    return next((c for c in _own if c.exists()),
                _sessions_dir(root) / "quorum" / f"{seat}.md")


def _subheader_in_body(body: str, token: str) -> int | None:
    """Line index of the first header line at ANY depth (`###`, etc.) in
    `body` whose text contains `token` (case-insensitive), or None.
    Subsections live inside a `## ` section's body (`_split_card_sections`
    splits only on `## `), so `### 🔴 Where it stops` is found here."""
    for i, ln in enumerate(body.splitlines()):
        s = ln.strip()
        if s.startswith("#") and token.lower() in s.lower():
            return i
    return None


STOPS_TITLE_TOKENS = ("where it stops", "next command")


def _is_stops_title(header: str) -> bool:
    """A header names the where-it-stops slot by TITLE: 'where it stops' or
    its synonym 'next command' (case-insensitive)."""
    h = header.lower()
    return any(tok in h for tok in STOPS_TITLE_TOKENS)


def _locate_where_it_stops(sections) -> tuple[int, int] | str | None:
    """Where the where-it-stops slot lives in `sections` (a `_split_card_
    sections` list). Returns `(section_idx, sub)` where `sub == -1` means the
    `## ` section header itself is the slot and `sub >= 0` is the body-line
    index of the `###`-style subheader inside it. Returns `"ambiguous"` when
    more than one match, `None` when none (caller refuses an existing-card
    miss). Resolution order:
      1. a `## ` header whose TEXT contains "where it stops";
      2. a `###`-level subheader whose text contains "where it stops".
    NEVER a numeral: `## §3 WHAT YOU NEVER TOUCH` carries the §3 numeral but
    is NOT the slot (the sensei-director §3 is NEVER TOUCH), so an untitled
    §3 header falls through to `None` and the caller (`_write_stops_section`)
    CREATES a TITLED slot at the card end instead of overwriting the untitled
    block. The legacy §3-numeral fallback is DELETED
    (hyp:l4-the-stops-slot-is-located-by-title-only…)."""
    # "next command" is the same slot under the Prime's and the Sensei's
    # titles (`## §3 🔴 NEXT COMMAND`, `## §5 🔴 NEXT COMMAND — the loop …`);
    # a title synonym keyed exactly like 'where it stops'.
    top = [(i, -1) for i, (h, _) in enumerate(sections)
           if _is_stops_title(h)]
    sub = [(i, j) for i, (_, b) in enumerate(sections)
           if (j := _subheader_in_body(b, "where it stops")) is not None
           or (j := _subheader_in_body(b, "next command")) is not None]
    if len(top) + len(sub) > 1:
        return "ambiguous"
    if len(top) == 1:
        return top[0]
    if len(sub) == 1:
        return sub[0]
    return None


def _resolved_stops_slot_text(card_path: Path) -> str:
    """The rotate-self --stops --dry-run 'stops slot:' line for a card, read
    fresh and never written: the located header line + '(replace)', or
    'none — will append at end' when no titled slot exists, or the ambiguous
    refusal. Keys on TITLE only (the numeral fallback is deleted), so a card
    carrying only `## §3 …` (no title) reports append-at-end."""
    card_txt = (card_path.read_text(encoding="utf-8")
                if card_path.exists() else "")
    _preamble, _secs = _split_card_sections(card_txt)
    _slot = _locate_where_it_stops(_secs)
    if _slot == "ambiguous":
        return "stops slot: AMBIGUOUS where-it-stops (replace refused)"
    if isinstance(_slot, tuple):
        _sec = _secs[_slot[0]]
        _hdr = _sec[0] if _slot[1] < 0 else _sec[1].splitlines()[_slot[1]]
        return f"stops slot: {_hdr.strip()} (replace)"
    return "stops slot: none — will append at end"


def _locate_banked(sections) -> tuple[int, int] | str | None:
    """Where the BANKED slot lives, title-keyed exactly like where-it-stops
    but with NO numeral fallback (the sensei-director §6 is TRAPS, never
    banked). `None` = absent, which is fine — nothing is appended (hypothesis
    wording: the Prime card has one, the sensei-director card does not).
    `"ambiguous"` = more than one BANKED header, refused rather than
    guessed."""
    top = [(i, -1) for i, (h, _) in enumerate(sections)
           if "banked" in h.lower()]
    sub = [(i, j) for i, (_, b) in enumerate(sections)
           if (j := _subheader_in_body(b, "banked")) is not None]
    if len(top) + len(sub) > 1:
        return "ambiguous"
    if len(top) == 1:
        return top[0]
    if len(sub) == 1:
        return sub[0]
    return None


def _state_rows(seat: str, facts: dict) -> list[tuple[str, str]]:
    """The measured state as (label, value) rows — the single source for
    BOTH shapes the built block can take. `seat` is provenance so the block
    names whose card it is."""
    gb, ga = facts.get("gen_before"), facts.get("gen_after")
    if gb is not None and ga is not None:
        gen_s = f"{gb}->{ga}"
    elif ga is not None:
        gen_s = str(ga)
    elif gb is not None:
        gen_s = str(gb)
    else:
        gen_s = "n/a"
    rows: list[tuple[str, str]] = []
    rows.append(("Rotation record",
                 f"gen {gen_s}, window {facts.get('window') or 'n/a'}, "
                 f"pid {facts.get('pid') or 'n/a'}, model_confirm "
                 f"{facts.get('model_confirm') or 'n/a'}."))
    nc = (f"active {facts.get('counts_active') or 'n/a'}, deprecated "
          f"{facts.get('counts_deprecated') or 'n/a'}.")
    if facts.get("suite"):
        nc += f" Suite {facts['suite']}."
    rows.append(("Node counts", nc))
    rows.append(("Tree",
                 f"branch {facts.get('branch') or 'n/a'}, behind "
                 f"{facts.get('season') or 'season/s?'} "
                 f"{facts.get('behind') or 'n/a'}, unpushed "
                 f"{facts.get('unpushed') or 'n/a'}."))
    rows.append(("Meter",
                 f"{facts.get('fraction') or 'n/a'} · "
                 f"role {facts.get('role') or 'n/a'} · "
                 f"model {facts.get('model') or 'n/a'}."))
    rows.append(("Account", str(facts.get("account") or "n/a")))
    return rows


def _render_state_body(shape: str, rows: list[tuple[str, str]]) -> str:
    """Render the measured state rows into `shape` — a 2-column table or a
    list — so the built block takes the SHAPE of what it replaces (hypothesis
    SL2.01 #2): a table card stays a table, a list card stays a list."""
    if shape == "table":
        out = ["| Field | Value |", "|---|---|"]
        for label, value in rows:
            out.append(f"| {label} | {value} |")
        return "\n".join(out)
    out = [f"- **{label}:** {value}" for label, value in rows]
    return "\n".join(out)


def _state_header(seat: str, facts: dict) -> str:
    """The `## ` header for the state section (used for a FRESH compose only;
    an existing STATE header is kept untouched while only its first
    table-or-list is rebuilt)."""
    return (f"## §0 STATE (driven — `rotate.py handoff --driven --seat "
            f"{seat}`, {facts.get('stamp')})")


def _replace_state_body(body: str, rows: list[tuple[str, str]]) -> str:
    """Scoped state replacement (hypothesis SL2.01 #2): replace the FIRST
    table-or-list directly under the STATE header with the measured block,
    carrying everything else in the section (subsections, prose) verbatim.
    A section with no table-or-list at all (e.g. the lean PRIME §0 body)
    is replaced wholesale — the writer still fills it."""
    lines = body.splitlines()
    idx = None
    kind = None
    for i, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("|"):
            idx, kind = i, "table"
            break
        if s.startswith(("- ", "* ")):
            idx, kind = i, "list"
            break
    if idx is None:
        # no table/list to scope to: replace the whole body (Prime lean §0)
        return _render_state_body("list", rows)
    j = idx
    if kind == "table":
        while j < len(lines) and lines[j].strip().startswith("|"):
            j += 1
    else:
        while j < len(lines) and lines[j].strip().startswith(("- ", "* ")):
            j += 1
    before = lines[:idx]
    after = lines[j:]
    new_block = _render_state_body(kind, rows).splitlines()
    return "\n".join(before + new_block + after)


def _replace_fence_after(lines: list[str], start: int, s3: str):
    """Replace the fenced code block starting at/after line `start`'s fence
    with `s3`, keeping the ```` ``` ```` delimiters and the header above it.
    Returns the new line list, or None when no fence is found below `start`
    (caller falls back to whole-body replacement)."""
    fence = None
    for i in range(start, len(lines)):
        if _fence_run(lines[i]) >= 3:
            fence = i
            break
    if fence is None:
        return None
    opener = _fence_run(lines[fence])
    close = None
    for i in range(fence + 1, len(lines)):
        # pair the run-length-aware closer (>= opener), so an inner shorter
        # fence under a longer outer fence never mis-pairs (residue (iii)).
        if _fence_run(lines[i]) >= opener:
            close = i
            break
    if close is None:
        close = len(lines)
    return lines[:fence + 1] + s3.splitlines() + lines[close:]


def _replace_stops_body(body: str, s3: str, sub_offset: int | None) -> str:
    """Where-it-stops replacement (hypothesis SL2.01 #2): replace only the
    fenced code block under the (possibly `###`-level) header, keeping the
    header and everything around it. When there is no fence, the whole body
    is replaced — the lean PRIME `## §3 🔴 NEXT COMMAND` body is one plain
    line and is filled wholesale."""
    lines = body.splitlines()
    for idx, ln in enumerate(lines):
        if ln.strip().startswith("```"):
            if sub_offset is None or idx > sub_offset:
                new = _replace_fence_after(lines, idx, s3)
                if new is not None:
                    return "\n".join(new)
                break
    # no fenced block: replace the whole body
    return s3


def cmd_handoff(args: argparse.Namespace, root: Path) -> int:
    """`rotate.py handoff --driven --seat S [--field s3 SRC] [--field s6 SRC]`.

    Builds §0 of the seat's card (<sessions>/quorum/<S>.md) from measured
    values, PRINTS the one bounded question (exactly §3 where-it-stops and
    §6 banked), reads the answers, runs the trim guard (a composed card over
    HANDOFF_CARD_LIMIT_LINES refuses, naming the section to cut), and writes
    the card — §0 replaced, §3/§6 filled, every other section verbatim.
    `-` for a field reads one line from stdin; a filename reads that file in
    full. An empty §3 is REFUSED (exit 2): §3 is the critical next command,
    never guessed. Nothing is written on a refusal.
    """
    if root is None:
        print("ERR: handoff --driven needs an agi project root.",
              file=sys.stderr)
        return 1
    if not args.driven:
        print("ERR: only `handoff --driven` exists today; pass --driven.",
              file=sys.stderr)
        return 2
    seat = args.seat
    if not seat:
        print("ERR: handoff --driven needs --seat S.", file=sys.stderr)
        return 2

    fields: dict[str, str] = {}
    for field, src in (args.field or []):
        if field not in HANDOFF_ASKED_FIELDS:
            print(f"ERR: handoff --driven asks only for "
                  f"{' and '.join(HANDOFF_ASKED_FIELDS)}; field {field!r} "
                  f"is not one of them.", file=sys.stderr)
            return 2
        fields[field] = src

    def _read(field_name: str) -> tuple[str, str | None]:
        src = fields.get(field_name)
        if src is None:
            return "", None
        if src == "-":
            return sys.stdin.readline().rstrip("\n"), None
        try:
            return Path(src).read_text(encoding="utf-8").strip(), None
        except OSError as e:
            return "", f"cannot read {field_name} source {src!r}: {e}"

    s3, s3_err = _read("s3")
    s6, s6_err = _read("s6")
    if s3_err:
        print(f"ERR: {s3_err}", file=sys.stderr)
        return 2
    if s6_err:
        print(f"ERR: {s6_err}", file=sys.stderr)
        return 2
    if not s3.strip():
        print("ERR: handoff --driven refuses an EMPTY §3 where-it-stops "
              "(the one next command); supply --field s3 - (or a file).",
              file=sys.stderr)
        return 2

    print("## DRIVEN HANDOFF — the LLM answers exactly these TWO fields, "
          "nothing else.")
    print("§3 where-it-stops (the one next command).")
    print("§6 banked (options + recommendation).")
    print("Supply each as --field s3 <src> / --field s6 <src> (`-` = stdin); "
          "an empty §3 is refused.")

    dry_run = bool(getattr(args, "dry_run", False))
    card_path = _own_card_path(root, seat)
    existing = (card_path.read_text(encoding="utf-8")
                if card_path.exists() else "")
    card_existed = bool(existing.strip())
    preamble, sections = _split_card_sections(existing)

    facts = _harvest_handoff_facts(root, seat)
    rows = _state_rows(seat, facts)

    # Resolve the three slots by DECLARED TITLE — never by the § numerals
    # alone (the sensei-director card's numerics are a different layout).
    state_idx = [i for i, (h, _) in enumerate(sections)
                 if "state" in h.lower()]
    stops = _locate_where_it_stops(sections)
    banked = _locate_banked(sections)

    if card_existed:
        if len(state_idx) > 1:
            found = " / ".join(h for h, _ in sections if "state" in h.lower())
            print(f"ERR: handoff --driven finds {len(state_idx)} STATE "
                  f"sections, ambiguous; refusing — {found}.", file=sys.stderr)
            return 2
        if len(state_idx) == 0:
            # A card that never declared a STATE section (the Sensei's:
            # §0 WHO YOU ARE … §5 NEXT COMMAND … §6 BANKED) GAINS one — the
            # driven block is measured values, so it is inserted ahead of
            # the next-command section (or appended when there is none),
            # under a header the NEXT run keys on by title. Never guess §0
            # by numeral: on that card §0 is identity (Sensei 18:29Z asked
            # for '§0 by prefix'; it would have overwritten its own §0).
            insert_at = (stops[0] if isinstance(stops, tuple)
                         else len(sections))
            # no numeral on an inserted header: the card already has a §0
            # (identity there), and the next run keys on the TITLE
            inserted = _state_header(seat, facts).replace(
                "## §0 STATE", "## 🔴 STATE", 1)
            sections = (list(sections[:insert_at])
                        + [(inserted, "")]
                        + list(sections[insert_at:]))
            state_idx = [insert_at]
            stops = _locate_where_it_stops(sections)
            banked = _locate_banked(sections)
            nxt = (sections[insert_at + 1][0]
                   if insert_at + 1 < len(sections) else "the end")
            print(f"handoff --driven: no STATE section declared; inserting "
                  f"one ahead of {nxt}.", file=sys.stderr)
        if isinstance(stops, str):
            print("ERR: handoff --driven finds an ambiguous where-it-stops "
                  "slot; refusing rather than guessing.", file=sys.stderr)
            return 2
        if stops is None:
            found = " / ".join(h for h, _ in sections)
            print("ERR: handoff --driven finds no where-it-stops slot (no "
                  "'where it stops' / 'next command' title) to fill; "
                  f"refusing — found: {found or '(none)'}.", file=sys.stderr)
            return 2
        if banked == "ambiguous":
            print("ERR: handoff --driven finds more than one BANKED header; "
                  "refusing rather than guessing.", file=sys.stderr)
            return 2

    def _slot_section_idx(slot) -> int | None:
        if slot is None or isinstance(slot, str):
            return None
        return slot[0]

    # Apply transforms per section. A section may hold BOTH the state block
    # and the `### where it stops` subheader (the sensei-director §5); apply
    # state-scope first, then stops-scope on the already-rebuilt body.
    state_i = state_idx[0] if len(state_idx) == 1 else None
    stops_slot = stops if not isinstance(stops, str) else None
    banked_slot = banked if not isinstance(banked, str) else None
    stops_sec = _slot_section_idx(stops_slot)
    banked_sec = _slot_section_idx(banked_slot)

    new_sections: list[tuple[str, str]] = []
    for i, (header, body) in enumerate(sections):
        if i == state_i:
            body = _replace_state_body(body, rows)
        if stops_slot is not None and stops_sec == i:
            sub = stops_slot[1]
            body = _replace_stops_body(body, s3, None if sub == -1 else sub)
        if banked_slot is not None and banked_sec == i:
            sub = banked_slot[1]
            if sub == -1:
                if s6:
                    body = s6
            else:
                # a `###`-level BANKED: keep the header + what precedes it,
                # append s6 beneath it, carry everything below the subheader
                lines = body.splitlines()
                if sub < len(lines):
                    head = "\n".join(lines[:sub + 1])
                    rest = lines[sub + 1:]
                    trail = [ln for ln in rest if ln.strip()]
                    body = head
                    if s6:
                        body += "\n" + s6
                    if trail:
                        body += "\n" + "\n".join(rest)
        new_sections.append((header, body))

    # Fresh compose: a card that did not exist gets all three slots appended
    # (the PRIME layout). A card that EXISTS is driven in place.
    if not card_existed:
        new_sections = [
            (_state_header(seat, facts), _render_state_body("list", rows)),
            ("## §3", s3),
            ("## §6", s6 or ""),
        ]

    full = _render_card(preamble, new_sections)
    line_count = full.count("\n")
    if line_count > HANDOFF_CARD_LIMIT_LINES:
        biggest = max(new_sections, key=lambda hs: len(hs[1].splitlines()))[0]
        print(f"ERR: composed card is {line_count} lines, over the "
              f"{HANDOFF_CARD_LIMIT_LINES}-line guard; cut the biggest "
              f"section ({biggest}).", file=sys.stderr)
        return 2

    if dry_run:
        print(full)
        return 0

    card_path.parent.mkdir(parents=True, exist_ok=True)
    card_path.write_text(full, encoding="utf-8")
    print(f"wrote driven handoff card {card_path} (§0 built; §3/§6 "
          f"filled; {len(sections)} section(s) handled).")
    return 0


# --- rotate-self subcommand -----------------------------------------------


# ── L4.112 (D) THE HANDOVER — kid 2 of the round ---------------------------
# The successor lifecycle assembled into ONE rotate-self call, every step
# recorded. Identity is SUPPLIED, never inferred: none of the identity-bearing
# writes happens without the successor's `session_ref` (ListAgents `@id` from
# the JOIN). The seats-row write is admitted by write.py's self_row DATA
# declaration (L4.110), never by a code branch naming `seats`.


def _write_ack(*, root: Path, seat: str, gen_after: int, session_ref: str,
               answer: str = "continue", text: str = "",
               source: str = "predecessor") -> Path:
    """Write the successor's ACK file on ITS behalf (kid-2 step 6).

    The predecessor writes into the same ack channel `cmd_ack` used, so the
    read-back confirms (or polls) the rotation the moment it reads. `source`
    marks WHO wrote the ack: `predecessor` (rotate-self / the first seating -
    writer) vs the successor's own `cmd_ack` turn; `source: predecessor` is
    how the read-back and `--ask-diff` tell a pre-answer from a successor
    reply. cmd_ack stays CALLABLE as a one-generation fallback
    (hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-design)
    but is no longer a first-class wake act under the default."""
    ack = {
        "seat": seat,
        "gen_after": gen_after,
        "session_ref": session_ref,
        "answer": answer,
        "text": text,
        "source": source,
        "ts": datetime.utcnow().isoformat() + "Z",
    }
    path = _ack_path(root, seat)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ack, indent=2) + "\n", encoding="utf-8")
    return path


def _shared_graph_root(root: Path) -> Path:
    """The MAIN checkout's GRAPH root, identity for a non-worktree caller.

    The seats node carrying the identity cells (`generation`/`window`/`pid`/
    `session_ref`/`session_id`) lives in MAIN's graph, so a worktree rotation
    writes MAIN's `.agi/nodes/.geometry/seats.md` and never the worktree copy
    (hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main).
    This is the same resolution `_sessions_dir` performs — climb through
    `locations.git_common_root`, re-derive the graph there — returning the
    graph ROOT (where `_load_seats`/`write.submit` expect it) rather than the
    sessions join. From MAIN itself the result equals `root`."""
    graph = locations.find_project_root(root) or root
    main = locations.git_common_root(graph)
    if main is not None:
        mg = locations.find_project_root(main) or graph
        graph = mg
    # `graph` is usually the `.agi/` dir itself; the legacy G11 shape has.
    # `nodes/` beneath `<root>/.agi/`.
    if (graph / locations.GRAPH_DIR_NAME / "nodes").is_dir():
        return graph / locations.GRAPH_DIR_NAME
    return graph


def _write_identity_cells(root: Path, *, seat: str, actor: str, role: str,
                          cells: dict) -> str:
    """The ONE writer of a seat's identity cells in config:posts.

    `generation`/`window`/`pid`/`session_ref`/`session_id` — every cell that
    a rotation moves — are written through here, into the MAIN checkout's
    `nodes/.geometry/posts.md` (resolved via `_shared_graph_root` and
    `geometry_config.resolve`; `config:seats`/`seats.md` is the one-season
    alias until the rename settles), never the caller's worktree copy
    (hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main).
    A worktree seat's rotation reaches MAIN where every sender reads, and the
    worktree copy is never written on these cells — nothing to diverge,
    nothing to conflict at merge-up. From MAIN itself the path is unchanged.
    The node id and frontmatter list key come from `geometry_config.resolve`
    (`config:posts`/`posts` when posts.md exists, else
    `config:seats`/`seats`), so a migrated tree's own acks write posts.md.
    Admission is the `self_row` declaration as today (the `seat` is the
    actor's own row). Returns a truthy one-line outcome when the write
    landed, or '' when the seat has no registry row (the caller prints its
    own skip message)."""
    import geometry_config  # noqa: PLC0415  (local: same dir, no cycle)
    import write  # local: same dir (send.py pattern, no import cycle)
    main_root = _shared_graph_root(root)
    rows = write._load_seats(main_root)
    new_rows: list[dict] = []
    found = False
    for r in rows:
        if r.get("name") == seat:
            nr = dict(r)
            for cell, val in cells.items():
                if val is not None:
                    nr[cell] = val
            new_rows.append(nr)
            found = True
        else:
            new_rows.append(r)
    if not found:
        return ""
    _, list_key = geometry_config.resolve(main_root)
    node_id = f"config:{list_key}"
    edit = write.Edit(node_id=node_id)
    edit.set_fm[list_key] = new_rows
    write.submit(main_root, edit, actor=actor, role=role)
    return f"wrote identity cells for seat {seat!r} into MAIN {list_key}.md"


def _successor_row_write(root: Path, *, actor: str, seat: str, role: str,
                         session_ref: str, generation: int,
                         window: str, pid: int | None = None,
                         session_id: str | None = None,
                         key_rotation: dict | None = None) -> str:
    """Write the successor's config:seats ROW via `write.py submit` (s6).

    Sets the seat's own row's `session_ref`/`session_id`/`generation`/`window`/
    `pid`. L4.114 (s6): the source of the identity is the registry JOIN —
    `source: registry` is recorded in the handover (the row itself carries no
    `source` field; the L4.110/r3 self_row declaration admits exactly
    [session_ref, session_id, generation, window, pid]).

    The row edit itself moves into `_write_identity_cells`, which resolves the
    posts node to the MAIN checkout's graph root (hypothesis:l4-a-seats-
    identity-cell-has-one-writer-and-it-writes-main); `_backfill_session_ref`
    routes through the SAME writer, so a seat's identity cells have one
    writer and it writes MAIN. The successor reuses the PLAIN seat name, so
    its row IS the seat's own row — the exact write the self_row declaration
    admits for a seated actor (only its own row, only the declared fields;
    every other row and every prime-only field byte-identical). Admission
    lives in write.py's `_enforce_written_by` reading the schema's `self_row`
    data; nothing here names `seats` in a branch. Returns a one-line outcome
    string.

    `key_rotation` (goal:g15.25 line (2), hypothesis l4-rotate-self-is-key-
    gated...): the dict returned by `_rotate_successor_key`. When present
    (a KEYED seat rotated and minted a successor key), the SAME ONE row
    write additionally sets the seat's `pubkey` to the successor pub and
    APPENDS the retired-predecessor `key_history` entry — never deletes or
    shrinks existing history, never a second submit (SL2#8 harvest seam:
    the cells ride `_write_identity_cells` like every other identity cell,
    so they land in MAIN too). `pubkey`/`key_history`/`sig_scheme` are
    declared self_row fields, so admission holds."""
    cells: dict = {"session_ref": session_ref, "generation": generation,
                   "window": window}
    if session_id is not None:
        cells["session_id"] = session_id
    if pid is not None:
        cells["pid"] = pid
    # goal:g15.25 line (2): the successor half's cells ride the SAME one row
    # write -- the successor pubkey into the seat's own row and the retired-
    # predecessor key_history entry APPENDED (never shrink existing history).
    # The current history is read from the row the ONE writer will write
    # (MAIN's), so the append is against the live list, not a worktree copy.
    if key_rotation:
        import write  # local: same dir (send.py pattern, no import cycle)
        _cur = next((r for r in write._load_seats(_shared_graph_root(root))
                     if r.get("name") == seat), {})
        _ret = key_rotation.get("retired")
        cells["pubkey"] = key_rotation.get("successor_pub")
        cells["sig_scheme"] = (_cur.get("sig_scheme")
                               or key_rotation.get("scheme"))
        _hist = list(_cur.get("key_history") or [])
        if _ret and not any(h.get("from") == _ret.get("from")
                            and h.get("to") == _ret.get("to")
                            for h in _hist if isinstance(h, dict)):
            _hist.append(_ret)
        cells["key_history"] = _hist
    if not _write_identity_cells(root, seat=seat, actor=actor, role=role,
                                 cells=cells):
        return (f"skipped: no seat-registry row with name {seat!r} "
                "(a THROWAWAY seat never writes seats.md)")
    _extra = (f" pubkey={key_rotation['successor_pub'][:16]}... "
              f"key_history={len(key_rotation['retired'])}"
              if key_rotation else "")
    return (f"config:seats row {seat!r}: session_ref={session_ref} "
            f"session_id={session_id} pid={pid} generation={generation} "
            f"window={window!r} source=registry{_extra}")


def _ref_shape_issue(ref: str, seat: str) -> str | None:
    """Return a reason if `ref` is NOT a BARE ListAgents ref: it carries
    brackets (a row-shaped ref), whitespace, or IS the seat name itself. None
    means it is a safe bare ref to carry/back-fill. An empty ref is None (no
    --ref passed) — the caller then back-fills from the row's session_id."""
    if not ref:
        return None
    if "[" in ref or "]" in ref:
        return "carries brackets (that is a row-shaped ref, not a ref)"
    if any(c.isspace() for c in ref):
        return "carries whitespace (the ref is a single bare token)"
    if ref.strip().lower() == str(seat).lower():
        return "is the seat name, not a ref"
    return None


def _backfill_session_ref(root: Path, *, seat: str, role: str,
                          ref: str, pid: int | None = None,
                          session_id: str | None = None) -> str:
    """r3 — `rotate.py ack --ref <ref>` BACK-FILLS `session_ref` into the
    successor's OWN seats row through the self_row write (source: ack).

    The `session_ref` (the successor's session/uuid prefix, proven by whois)
    travels in the row so a later whois can authorize by it. L4.288: the
    optional `pid`/`session_id` kwargs carry the successor's OWN identity from
    the JOIN by the row's own window @id, so ONE `write.submit` moves
    session_ref + pid + session_id together — never a second submit, and
    never a write from any source but the JOIN (pass only joined values that
    DIFFER from the row's, so a rotate-self-seated successor's row ends
    byte-identical to today's except session_ref). The row edit itself moves
    into `_write_identity_cells` — the ONE writer, resolving MAIN's seats
    node (hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-
    main) — so the ack's back-fill lands in the same MAIN row the rotation
    wrote. Returns a one-line outcome; the write is admitted by the self_row
    declaration."""
    cells: dict = {"session_ref": ref}
    if session_id is not None:
        cells["session_id"] = session_id
    if pid is not None:
        cells["pid"] = pid
    if not _write_identity_cells(root, seat=seat, actor=seat, role=role,
                                 cells=cells):
        return (f"skipped: no seat-registry row with name {seat!r} "
                "(a THROWAWAY seat has no row to back-fill)")
    parts = [f"session_ref={ref}"]
    if session_id is not None:
        parts.append(f"session_id={session_id}")
    if pid is not None:
        parts.append(f"pid={pid}")
    return f"back-filled {', '.join(parts)} into own row (source: ack)"


def _ack_seats_path(root: Path) -> Path:
    """The config:posts/config:seats file the ack's back-fill writes
    (`.agi/nodes/.geometry/posts.md`, else the deprecated seats.md) — the ONE
    path the ack ever stages or commits, never `-A`, never a sibling."""
    return geometry_config.geometry_config_path(root) or (
        Path(root) / "nodes" / ".geometry" / "posts.md")



def _own_row_line(line: str, seat: str, session_owns: bool = False) -> bool:
    """Whether a seats.md CHANGED line belongs to `seat`'s OWN write. One
    row sits on ONE JSON line, so the row-cell `name` cell ALONE keys the
    row — an `"edited_by": ...` cell on a FOREIGN row must never count. A
    row line is own when (and only when) it carries this seat's OWN `name`
    cell; that decision is made on the line alone, NEVER by pairing it with a
    changed line beside it (SL4/6.09 residue, mur-SL2.15: per-INDEX pairing
    staged a foreign adjacent line as own — the cut classifies each changed
    line by ROW IDENTITY, not by index).

    The FRONTMATTER provenance line (`edited_by: <writer>`, YAML form, no
    quotes) has no `name` cell, but `write.submit` restamps it on the SAME
    write that produces the own row; the whole-node stamp is part of that
    write, so it is owned WITH the own row and the tree stays clean (SL7.09
    clause (4): value-agnostic, because write.submit names the WRITER'S
    resolved actor, usually not the seat's own name). It counts as own ONLY
    when the SAME diff also carries an own-row `name`-cell change
    (`session_owns`); frontmatter alone never owns. Kept together so
    `_diff_owns_row` and `_seats_ownrow_content` read the SAME predicate and
    can never drift."""
    name_cell = f'"name": "{seat}"'
    if name_cell in line:
        return True
    # JSON row-cell vs YAML frontmatter: the top-level `edited_by:` YAML line
    # (space after the colon, no quotes) is the whole-node stamp the self-row
    # write owns, whatever actor it names — but only when this diff carries an
    # own row. A FOREIGN row's `"edited_by": ...` cell is quoted JSON inside
    # an indented `  - {...}` row line, which never starts with `edited_by: `,
    # so it can never count as own here.
    return session_owns and _is_frontmatter_edited_by(line)


def _is_frontmatter_edited_by(line: str) -> bool:
    """Whether a seats.md CHANGED line is the top-level YAML frontmatter
    provenance stamp `edited_by: <writer>` that `write.submit` restamps on
    the same self-row write. Value-agnostic (the writer's actor, not the
    seat's name). Accepts the optional unified-diff `+`/`-` prefix
    `_diff_owns_row` passes it, so the own-row GATE and the commit-content
    cut read the SAME predicate."""
    stripped = line.lstrip("+- ")
    return stripped.startswith("edited_by: ") or stripped == "edited_by:"


def _diff_owns_row(diff: str, seat: str) -> bool:
    """True when a unified diff's CHANGED lines (`+`/`-` content, never
    `+++`/`---` headers or context) carry THIS seat's OWN row (a changed line
    whose `name` cell keys the seat). The frontmatter `edited_by:` provenance
    line is owned ONLY when the SAME diff also carries an own-row `name`-cell
    change — so a seats.md whose ONLY change is a foreign `edited_by:`
    restamp reads FOREIGN: the gate (SL7.09 clause (4) tie-in) does not fire
    as own and the commit stages nothing of it. One definition, shared with
    `_seats_ownrow_content` (both call `_own_row_line`; none re-spells it)."""
    in_hunk = False
    changed: list[str] = []
    for ln in diff.splitlines():
        if ln.startswith("@@"):
            in_hunk = True
            continue
        if not in_hunk:
            continue
        if ln.startswith(("+++", "---")):
            continue
        if ln.startswith(("+", "-")):
            changed.append(ln)
    # session_owns: does this diff carry an own-row `name`-cell change? The
    # frontmatter stamp counts only beside that; alone it stays FOREIGN.
    session_owns = any(_own_row_line(l, seat) for l in changed)
    return any(_own_row_line(l, seat, session_owns) for l in changed)


def _rstrip_lines(text: str) -> list[str]:
    """Normalised comparison form of a text file: per-line TRAILING
    whitespace stripped and the EOF newline folded away. Two texts whose ONLY
    difference is trailing whitespace / a missing final newline compare EQUAL
    here (claim 2: a whitespace-only delta reads CLEAN); any leading or
    interior whitespace or a real byte still differs, so a genuine one-cell /
    interior change is never collapsed to clean."""
    return [ln.rstrip() for ln in text.splitlines()]


def _blob_text(top: Path, rev: str) -> str | None:
    """`git show <rev>` (a `HEAD:<path>` or `:<path>` index blob) as text, or
    None on any failure (not a repo, an opaque refusal)."""
    try:
        run = subprocess.run(["git", "-C", str(top), "show", rev],
                             capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return None
    if run.returncode != 0:
        return None
    return run.stdout


def _diff_is_whitespace_only(root: Path, top: Path, rel: str,
                             cached: bool) -> bool:
    """True when the two trees `git diff [--cached] -- <rel>` is comparing
    differ only in trailing whitespace / the EOF newline after per-line
    trailing-strip normalisation (claim 2). cached -> index vs HEAD; uncached
    -> index vs the working file. False on any unmeasurable read — a gate
    must never mis-free a real delta on an opaque git answer."""
    if cached:
        a = _blob_text(top, f"HEAD:{rel}")
        b = _blob_text(top, f":{rel}")
    else:
        a = _blob_text(top, f":{rel}")
        try:
            b = _ack_seats_path(root).read_text(encoding="utf-8")
        except OSError:
            return False
    if a is None or b is None:
        return False
    return _rstrip_lines(a) == _rstrip_lines(b)


def _path_delta_whitespace_only(root: Path, top: Path, path: str) -> bool:
    """True when <path> (relative to `root`) differs from ITS committed HEAD
    bytes only in trailing whitespace / the EOF newline. False when clean,
    untracked (no HEAD blob), or unmeasurable — untracked files and real
    deltas always stay dirty. Claim 2's prepare check 2 counterpart.

    Compares HEAD against BOTH the index blob (`:<rel>`) AND the working
    file (claim 6a, hypothesis:l4-prepare-check-2-reads-the-index-blob-...):
    a real delta in EITHER reads dirty, so a STAGED real edit whose working
    copy was restored to HEAD bytes (porcelain `M ` / `MM` with a clean or
    whitespace-only working delta) never reads whitespace-only and a rotation
    never proceeds over an unrecorded staged edit."""
    abs_p = os.path.abspath(os.path.join(str(root), path))
    rel_top = os.path.relpath(abs_p, str(top))
    head = _blob_text(top, f"HEAD:{rel_top}")
    if head is None:
        return False
    # the INDEX blob (`:<rel>`) — a staged real edit is head-vs-index, not
    # head-vs-working, so it must be read too or it is invisible to a
    # whitespace-only test that only compares the working file.
    index = _blob_text(top, f":{rel_top}")
    if index is not None and _rstrip_lines(index) != _rstrip_lines(head):
        # the staged index differs from HEAD in real bytes -> not
        # whitespace-only, read dirty (blocker) regardless of the working copy.
        return False
    try:
        work = Path(abs_p).read_text(encoding="utf-8")
    except OSError:
        return False
    return _rstrip_lines(head) == _rstrip_lines(work)


def _index_staged_real_change(root: Path, top: Path, path: str) -> bool:
    """True when <path>'s only REAL dirty delta vs HEAD is in the INDEX — a
    staged real edit whose working copy matches HEAD bytes. Used to name an
    index-only real change as 'staged change (index differs from HEAD)' in
    prepare check 2 (claim 6a), so a rotation never proceeds over an
    unrecorded staged edit."""
    abs_p = os.path.abspath(os.path.join(str(root), path))
    rel_top = os.path.relpath(abs_p, str(top))
    head = _blob_text(top, f"HEAD:{rel_top}")
    if head is None:
        return False
    index = _blob_text(top, f":{rel_top}")
    if index is None or _rstrip_lines(index) == _rstrip_lines(head):
        return False  # no real index change to name
    try:
        work = Path(abs_p).read_text(encoding="utf-8")
    except OSError:
        return False
    # working copy matches HEAD (clean or whitespace-only) -> the only real
    # change is the staged index edit.
    return _rstrip_lines(head) == _rstrip_lines(work)


def _seats_diff_has_own_row(root: Path, top: Path, seat: str,
                            cached: bool = False) -> bool:
    """True when `git diff [--cached] -- <seats.md>` carries a hunk that
    owns the seat's OWN row (see `_diff_owns_row`). Never raises; False when
    clean or when the diff cannot be read (not a repo)."""
    rel = os.path.relpath(_ack_seats_path(root), top)
    cmd = ["git", "-C", str(top), "diff"]
    if cached:
        cmd.append("--cached")
    cmd += ["--", rel]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return False
    if out.returncode != 0 or not out.stdout.strip():
        return False
    # claim 2 (hypothesis:l4-one-serializer-...-reads-a-whitespace-only-
    # delta-as-clean): a delta whose ONLY difference is trailing whitespace /
    # a missing EOF newline reads CLEAN. Compare the two trees git is
    # diffing under a per-line TRAILING-strip normalisation; equality means
    # the seat's row is byte-unchanged in every interior cell, so the gate
    # never refuses on whitespace-only. A real one-cell change is an interior
    # byte and still differs, so the falsifier (never treat a real change as
    # clean) holds.
    if _diff_is_whitespace_only(root, top, rel, cached):
        return False
    return _diff_owns_row(out.stdout, seat)


def _seats_ownrow_content(root: Path, top: Path, seat: str) -> str | None:
    """The seats.md content the ack's OWN-row commit should stage: HEAD's
    content with ONLY the changes that carry THIS seat's own row (a changed
    line whose `name` cell keys the seat) applied, and every FOREIGN change
    REVERTED to the committed (HEAD) line. Base is HEAD, not the index, so a
    pre-staged foreign hunk cannot ride the ack. Returns None when there is
    no own-row change to stage.

    Sibling rows sit ADJACENT in seats.md, so git's unified diff folds an
    own row and a foreign row into ONE hunk and `git apply` cannot separate
    them by hunk — the cut is therefore made per CHANGED LINE, into an
    in-memory buffer, never onto the working tree. The caller stages this
    content into the index via `update-index` (working tree untouched), so
    the ack's commit carries exactly its own row and every foreign hunk
    stays unstaged and byte-untouched in the tree. Never raises."""
    import difflib  # local: only the buffer-builder needs it
    rel = os.path.relpath(_ack_seats_path(root), top)
    # base is HEAD, NOT the index (`git show :<rel>`): a foreign hunk that
    # was STAGED before the ack would sit in the index, thus inside the base,
    # and ride the ack commit. Cutting against HEAD keeps every foreign
    # change — staged or not — out of the own-row-only content, so a
    # pre-staged foreign row ends up UNSTAGED (bytes preserved) and never
    # committed. The gate (`_ack_seats_dirty`) has already guaranteed the OWN
    # row is not pre-staged, so HEAD is a safe base.
    try:
        run = subprocess.run(["git", "-C", str(top), "show",
                              f"HEAD:{rel}"],
                             capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return None
    if run.returncode != 0:
        return None
    try:
        work = _ack_seats_path(root).read_text(encoding="utf-8")
    except OSError:
        return None
    base_lines = run.stdout.splitlines()
    work_lines = work.splitlines()


    name_re = re.compile(r'"name":\s*"([^"]*)"')

    def _key(line: str) -> str | None:
        """A line's ROW IDENTITY: the `"name": "..."` cell (the row the line
        is), or None for a frontmatter / structural line. Own/foreign is
        decided PER LINE on this cell, never by index-pairing with a
        neighbour (mur-SL2.15: a per-index pair staged a foreign line as
        own)."""
        m = name_re.search(line)
        return m.group(1) if m else None

    def _own(line: str) -> bool:
        # shared with `_diff_owns_row`: the row-cell `name` keys the OWN row,
        # plus the OWN frontmatter `edited_by: <seat>` provenance write.submit
        # adds — but the frontmatter stamp counts only beside an own-row
        # `name`-cell change in this SAME diff (_session_owns). A FOREIGN
        # row's `"edited_by": ...` JSON cell never matches, so a foreign
        # provenance restamp is never bundled as own.
        return _own_row_line(line, seat, _session_owns)

    # session_owns (clause (b)): the whole-diff context. Gather every changed
    # line (removed + added) and decide whether an own-row `name`-cell change
    # appears anywhere; the frontmatter stamp is owned only when it does.
    sm = difflib.SequenceMatcher(None, base_lines, work_lines,
                                 autojunk=False)
    _changed: list[str] = []
    for _tag, _i1, _i2, _j1, _j2 in sm.get_opcodes():
        if _tag == "equal":
            continue
        _changed.extend(base_lines[_i1:_i2])
        _changed.extend(work_lines[_j1:_j2])
    _session_owns = any(_own_row_line(_l, seat) for _l in _changed)

    def _merge_region(removed: list[str], added: list[str]) -> list[str]:
        """The staged splice of ONE replace/insert/delete opcode region.
        Each changed line is classified on its own by ROW IDENTITY (never by
        index or positional key agreement): an OWN removed line is DROPPED
        (own deletion), an OWN added line is KEPT (own change / own write), a
        FOREIGN removed line is RESTORED from HEAD, a FOREIGN added line is
        NEVER staged. Rows are paired across removed/added BY THEIR `name`
        KEY, so progress never depends on the two sides sitting at the SAME
        position — a physical SWAP of two rows (both edited, their order
        crossed inside one replace opcode) still keeps the own row's WORK
        bytes and restores the foreign row byte-identical to HEAD, instead of
        falling through to a fail-safe that dropped the own added line
        (mur-SL2.17 / goal:g15.24 (i)). One two-pointer walk over the removed
        AND added sides in their own order interleaves a WORK-only added line
        (an own row inserted into WORK that HEAD lacks) at its WALK position —
        right where it sits on the added side, before the next removed line —
        instead of flushing it to the region END, so an own inserted row
        BETWEEN two HEAD rows keeps its byte position in the staged buffer
        (goal:g15.24 (ii), SL7.52). When the two sides sit at EXACTLY this
        spot (aligned keys) or a key CROSSES inside the opcode (both present on
        both sides, wrong order), pair BY KEY: keep the own row's WORK bytes,
        restore the foreign row byte-identical to HEAD. Structural lines
        (frontmatter `edited_by:` stamp, `---`, `id:`/`type:`/`seats:`) carry
        their HEAD bytes unless the work version is an owned frontmatter stamp.
        """
        rem = [(l, _key(l)) for l in removed]
        add = [(l, _key(l)) for l in added]
        add_by_key = {k: l for l, k in add if k is not None}
        rkeys = {k for _, k in rem if k is not None}
        matched: set[str] = set()
        i = j = 0
        out: list[str] = []
        while i < len(rem) or j < len(add):
            rl, rk = rem[i] if i < len(rem) else (None, None)
            al, ak = add[j] if j < len(add) else (None, None)
            # A WORK-only added row sits HERE in the added walk (its key is
            # absent from HEAD and it is not yet emitted): stage it at this
            # position, before the next removed line — never flushed to the
            # region end. Only this seat's own write is staged.
            if al is not None and ak is not None and ak not in rkeys \
                    and ak not in matched:
                if _own(al):
                    out.append(al)
                j += 1
                continue
            if rl is None:
                # only WORK-only added rows remain past the removed side.
                if ak is None:
                    if _own(al):  # own structural addition (frontmatter stamp)
                        out.append(al)
                elif ak not in matched:
                    if _own(al):
                        out.append(al)
                    matched.add(ak)
                j += 1
                continue
            if rk == ak is not None and rk not in matched:
                # aligned same-slot pair: keep WORK bytes when own, else the
                # row is restored byte-identical to HEAD.
                out.append(al if _own(al) else rl)
                matched.add(rk)
                i += 1
                j += 1
                continue
            if rk is not None and rk not in add_by_key:
                # the row was DELETED from the work copy: restore it from
                # HEAD unless it is this seat's OWN row (own deletion).
                if not _own(rl):
                    out.append(rl)
                i += 1
                continue
            if rk is not None and rk not in matched:
                # key present on BOTH sides but crossed / not yet paired:
                # pair by KEY — keep own WORK bytes, restore foreign from HEAD.
                wal = add_by_key.get(rk)
                if wal is not None:
                    out.append(wal if _own(wal) else rl)
                    matched.add(rk)
                    i += 1
                    continue
            # structural removed line, or a removed row whose work twin is
            # already emitted: keep HEAD unless this is an owned stamp.
            if not _own(rl):
                out.append(rl)
            i += 1
        return out

    staged: list[str] = []
    any_own = False
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            # unchanged context: carry HEAD's lines verbatim. (`base_lines[
            # b:i1]` is always empty here — opcodes tile the sequences
            # contiguously — so equal lines must be emitted explicitly.)
            staged.extend(base_lines[i1:i2])
        else:
            splice = _merge_region(base_lines[i1:i2], work_lines[j1:j2])
            if any(_own(_l) for _l in base_lines[i1:i2] + work_lines[j1:j2]):
                any_own = True
            staged.extend(splice)
    if not any_own:
        return None
    return "\n".join(staged) + "\n"


def _ack_seats_dirty(root: Path, top: Path, seat: str) -> str | None:
    """The config:seats path (relative to repo top) when the SEAT'S OWN row
    in seats.md is ALREADY dirty — staged OR unstaged hunks that touch the
    seat's own row (the row keyed by the `name` cell) — else None. r3b/g15.24
    belt: the ack refuses the commit path on a PRE-DIRTIED OWN row so its own
    back-fill commit never double-writes a row someone else was mid-edit on.
    A dirty FOREIGN row (another seat's hunks) NEVER blocks the ack — the ack
    commits only its own row's hunks and leaves the foreign byte-untouched.
    None when the own row is clean, or when the read cannot answer (not a
    repo). Never raises."""
    rel = os.path.relpath(_ack_seats_path(root), top)
    if _seats_diff_has_own_row(root, top, seat, cached=True):
        return rel
    if _seats_diff_has_own_row(root, top, seat, cached=False):
        return rel
    return None


def _ack_commit_seats(root: Path, seat: str, args: argparse.Namespace,
                      ref: str) -> tuple[bool, str]:
    """r3b/g15.24 belt — `rotate.py ack ... continue` (no `--no-commit`)
    COMMITS the OWN row rewrite it just back-filled: builds the seats.md
    content that carries ONLY THIS seat's own row (the committed content
    with own-row changes applied and every FOREIGN change reverted), stages
    that content into the index ONLY — against a throwaway `GIT_INDEX_FILE`
    seeded from HEAD, so the shared seats.md WORKING TREE is never written
    — commits against that temp index (no pathspec, so the committed tree is
    resolved from the index, never the working tree), and PRINTS the seat's
    old and new row lines from the resulting commit's diff so the successor
    never re-reads. The working tree's foreign hunks are never bundled and
    end up unstaged and byte-unTouched. A back-fill that changed nothing (the
    row already carried the ref) commits nothing and says so in one line. The
    last printed line is the exact `git push` command — printed, never run.

    Returns (ok, out). ok True -> out is the multi-line success string for
    STDOUT and the row is committed. ok False -> `git commit` failed: the
    real index and the working tree were never touched by this path (so
    seats.md is not left staged — nothing to reset) and out is the error
    line the caller must PRINT TO STDERR and pair with a non-zero (3) exit:
    a failed ack commit must never leave seats.md staged — that is exactly
    the dirt that would refuse the NEXT ack."""
    top = _git_toplevel(root)
    if top is None:
        return (True, "ack: no git repo — row written, not committed "
                "(a gitless worktree has no commit to make)")
    seats = _ack_seats_path(root)
    rel = os.path.relpath(seats, top)
    # The ack commits ONLY its own row, and the shared MAIN seats.md is
    # NEVER written by this path. `git commit -- <rel>` snapshots the WORKING
    # TREE of rel, so that form cannot commit own-row-only content without
    # transiently rewriting the shared file (a concurrent writer could be
    # clobbered by the restore). Instead the own-row-only content is staged
    # against a THROWAWAY INDEX seeded from HEAD (`GIT_INDEX_FILE=<tmp>`; git
    # read-tree HEAD, then hash-object the content and update-index
    # --cacheinfo under the temp index) and committed against THAT index with
    # no pathspec, so git resolves the committed tree from the temp index,
    # never the working tree. The working tree and every foreign hunk stay
    # byte-untouched throughout. The real index's seats.md entry is then
    # pointed at the committed blob so the own-row diff is no longer staged
    # or unstaged and only foreign hunks show under `git status`.
    new_content = _seats_ownrow_content(root, top, seat)
    if new_content is None:
        return (True, "ack: no change to seats.md — nothing committed")
    row = _find_seat(root, seat) or {}
    gen = getattr(args, "gen", None)
    win = str(row.get("window") or "")
    pid = str(row.get("pid") or "")
    msg = (f"{seat} ack: gen {gen}, session_ref {ref}, "
           f"window {win}, pid {pid}")

    import tempfile
    fd, tmp_index = tempfile.mkstemp(prefix="ack-idx-")
    os.close(fd)
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = tmp_index

    def _tmp_git(parts, **kw):
        return subprocess.run(["git", "-C", str(top)] + parts,
                              capture_output=True, text=True, env=env, **kw)

    blob_sha = ""
    try:
        seed = _tmp_git(["read-tree", "HEAD"])
        if seed.returncode != 0:
            return (False, f"ERR: git commit failed: {seed.stderr.strip()}")
        blob = _tmp_git(["hash-object", "-w", "--stdin"],
                        input=new_content)
        if blob.returncode != 0 or not blob.stdout.strip():
            return (False, f"ERR: git commit failed: {blob.stderr.strip()}")
        blob_sha = blob.stdout.strip()
        upd = _tmp_git(["update-index", "--add", "--cacheinfo",
                        f"100644,{blob_sha},{rel}"])
        if upd.returncode != 0:
            return (False, f"ERR: git commit failed: {upd.stderr.strip()}")
        rc = _tmp_git(["commit", "-q", "-m", msg])
    finally:
        try:
            os.unlink(tmp_index)
        except OSError:
            pass
    if rc.returncode != 0:
        # the real index and the working tree were never touched, so seats.md
        # is left clean under the NEXT ack's dirty gate; the row (and any
        # foreign hunks) stay in the working tree, unstaged. The caller
        # prints the error line to STDERR and pairs it with exit 3.
        return (False, f"ERR: git commit failed: {rc.stderr.strip()}")
    # point the REAL index's seats.md entry at the committed blob so the own
    # row no longer shows staged/unstaged; only foreign hunks remain.
    subprocess.run(["git", "-C", str(top), "update-index", "--add",
                    "--cacheinfo", f"100644,{blob_sha},{rel}"],
                   capture_output=True, text=True)
    head = subprocess.run(["git", "-C", str(top), "rev-parse", "HEAD"],
                          capture_output=True, text=True)
    show = subprocess.run(["git", "-C", str(top), "show", "--format=",
                           head.stdout.strip(), "--", rel],
                          capture_output=True, text=True)
    lines = []
    for ln in (show.stdout if show.returncode == 0 else "").splitlines():
        if ln.startswith(("+++", "---", "@@", "diff --git", "index ")):
            continue
        if ln.startswith(("+", "-")):
            lines.append(ln)
    return (True, "ack: committed own row write (" + str(rel) + "):\n"
            + "\n".join(lines) + f"\ngit -C {top} push")


def _push_season_branch(root: Path) -> str:
    """Push MAIN's checked-out branch to ``origin`` -- the clause-(2) push
    leg the key-cell writers run AFTER their own-row commit. Best-effort,
    never raises, never fails the caller: a push failure prints exactly one
    line to STDERR naming the remote error (``push: FAILED -- <stderr>``)
    and the mint or rotation completes regardless. Prints ``push: OK --
    <branch>`` on success and ``push: SKIPPED -- ...`` when there is nothing
    to push. Never a force-push, never a second commit. Returns the same
    one line it prints (for callers that log the outcome)."""
    # RUNG 3 HUMAN GATE (hypothesis:l4-a-veto-freezes-never-frees): a merge-
    # up push is a GATED Prime-scope act. While a council+Keep veto (or an
    # owner-written human_gate) shows the scope FROZEN, the push WAITS --
    # refused by name, and never auto-released.
    try:
        from seatsig import veto as _veto

        _frozen, _why = _veto.is_frozen(_shared_graph_root(root), "prime")
        if _frozen:
            _l = f"push: HELD -- merge-up push is a gated act; {_why}"
            print(_l, file=sys.stderr)
            return _l
    except Exception:  # noqa: BLE001  (a broken veto cell never gates silently)
        pass
    main_root = _shared_graph_root(root)
    top = _git_toplevel(main_root)
    if top is None:
        _l = "push: SKIPPED -- no git repo (gitless fixture/root)"
        print(_l, file=sys.stderr)
        return _l
    try:
        branch_out = subprocess.run(
            ["git", "-C", str(top), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        _l = "push: SKIPPED -- could not resolve the branch"
        print(_l, file=sys.stderr)
        return _l
    branch = (branch_out.stdout or "").strip()
    if not branch or branch == "HEAD":
        _l = "push: SKIPPED -- detached HEAD, nothing to push"
        print(_l, file=sys.stderr)
        return _l
    try:
        push = subprocess.run(
            ["git", "-C", str(top), "push", "origin", branch],
            capture_output=True, text=True, timeout=60)
    except Exception as exc:  # noqa: BLE001
        _l = f"push: FAILED -- {exc}"
        print(_l, file=sys.stderr)
        return _l
    if push.returncode != 0:
        _l = (f"push: FAILED -- "
              f"{push.stderr.strip() or push.stdout.strip()}")
        print(_l, file=sys.stderr)
        return _l
    _l = f"push: OK -- {branch}"
    print(_l, file=sys.stderr)
    return _l


def _commit_spawn_row(root: Path, *, seat: str, generation: int,
                      session_id: str | None = None,
                      window: str = "",
                      pid: int | None = None,
                      verb: str = "spawn row") -> str:
    """g15.24 (Sensei's pick, fix (a)) — rotate-self COMMITS its own s6.1
    spawn-row write, so the successor's ONE required wake act (`rotate.py
    ack --gen N --ref X continue`) finds seats.md CLEAN and the r3b gate
    `_ack_seats_dirty` stays exactly as written (it still refuses a
    pre-dirtied seats.md from ANOTHER seat by name).

    ONE plain `git commit` in the tree the ONE writer wrote: the toplevel
    of `_shared_graph_root(root)` (MAIN's graph; `_git_toplevel(main_root)`)
    and the seats.md under it (`main_root/nodes/.geometry/seats.md`, the
    exact path `write._load_seats`/`_write_identity_cells` read and write):
    `git add -- <seats.md rel>` then
    `git commit -q -m '<seat> spawn row: gen <N>, session_id <uuid>,
    window <@id>, pid <pid>' -- <rel>`, touching seats.md ONLY (mirror
    `_ack_commit_seats` 4978-5022): same toplevel resolution, same
    'seats.md only' pathspec, NEVER `git add -A`, never a grid commit,
    never a push. A worktree rotation's identity write lands in MAIN's
    seats.md, so the commit must run against MAIN's tree (the caller's
    worktree copy was never touched and would SKIP), or MAIN's dirty row
    would ride uncommitted to the next merge-up (hypothesis:l4-the-spawn-
    row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-
    its-own-row clause (1)). From MAIN itself this is unchanged.

    A rotate-self on a root with no git repo (`_git_toplevel` -> None), or
    whose seats.md is already clean after the write (the row was
    byte-identical and `git add` staged nothing), RECORDS the skip in
    one line and commits nothing. NEVER raises, never fails the rotation.
    Returns a one-line outcome for the handover's `spawn_row_commit`.
    """
    main_root = _shared_graph_root(root)
    top = _git_toplevel(main_root)
    if top is None:
        return ("spawn_row_commit: SKIPPED — no git repo; the spawn-row "
                "write stays in the tree, never committed (gitless "
                "fixture/root)")
    # the file the ONE writer wrote: the posts/seats.md under
    # _shared_graph_root, resolved through the geometry_config resolver the
    # ONE writer uses (never the literal seats.md -- post-rename, a
    # posts.md tree must commit posts.md).
    seats = _ack_seats_path(main_root)
    rel = os.path.relpath(seats, top)
    # claim (7): the spawn-row commit stages ONLY ITS OWN row via the
    # SL6.09 own-row helper (`_seats_ownrow_content`: MAIN's HEAD content
    # with every FOREIGN change reverted), as an INDEX-ONLY write against a
    # throwaway `GIT_INDEX_FILE` seeded from HEAD — the shared seats.md
    # WORKING TREE is NEVER written, so a foreign pre-dirty row in MAIN
    # (staged OR unstaged) is never committed under this post's name (`git
    # add -- seats.md` whole would bundle it). On commit failure the real
    # index is reset (`git reset -q -- <rel>`) exactly like the ack's
    # failure path.
    new_content = _seats_ownrow_content(main_root, top, seat)
    if new_content is None:
        return ("spawn_row_commit: SKIPPED — seats.md already clean after "
                "the write (row was byte-identical); nothing committed")
    # `_seats_ownrow_content` flags the seat's own row even on an UNCHANGED
    # (equal) line, so a clean row write (own row byte-identical) still
    # builds own content — equal to HEAD. That is nothing to commit: skip.
    _hdr = subprocess.run(["git", "-C", str(top), "show",
                           f"HEAD:{rel}"], capture_output=True, text=True,
                          timeout=10)
    _head_content = _hdr.stdout if _hdr.returncode == 0 else ""
    if _head_content and _head_content == new_content:
        return ("spawn_row_commit: SKIPPED — seats.md already clean after "
                "the write (row was byte-identical); nothing committed")
    msg = (f"{seat} {verb}: gen {generation}, session_id "
           f"{session_id or ''}, window {window or ''}, pid {pid or ''}")
    import tempfile  # noqa: PLC0415  (local, mirrors _ack_commit_seats)
    fd, tmp_index = tempfile.mkstemp(prefix="spawnrow-idx-")
    os.close(fd)
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = tmp_index

    def _tmp_git(parts, **kw):
        return subprocess.run(["git", "-C", str(top)] + parts,
                              capture_output=True, text=True, env=env, **kw)

    blob_sha = ""
    try:
        seed = _tmp_git(["read-tree", "HEAD"])
        if seed.returncode != 0:
            return (f"spawn_row_commit: FAILED — git commit: "
                    f"{seed.stderr.strip()}")
        blob = _tmp_git(["hash-object", "-w", "--stdin"],
                        input=new_content)
        if blob.returncode != 0 or not blob.stdout.strip():
            return (f"spawn_row_commit: FAILED — git commit: "
                    f"{blob.stderr.strip()}")
        blob_sha = blob.stdout.strip()
        upd = _tmp_git(["update-index", "--add", "--cacheinfo",
                        f"100644,{blob_sha},{rel}"])
        if upd.returncode != 0:
            return (f"spawn_row_commit: FAILED — git commit: "
                    f"{upd.stderr.strip()}")
        rc = _tmp_git(["commit", "-q", "-m", msg])
    finally:
        try:
            os.unlink(tmp_index)
        except OSError:
            pass
    if rc.returncode != 0:
        # the own-row commit FAILED: unstage so the next write's own-row
        # gate finds seats.md clean again, exactly like the ack.
        subprocess.run(["git", "-C", str(top), "reset", "-q", "--", rel],
                       capture_output=True, text=True)
        return (f"spawn_row_commit: FAILED — git commit: "
                f"{rc.stderr.strip()}")
    # point the REAL index's seats.md entry at the committed blob so the own
    # row no longer shows staged/unstaged; only foreign hunks remain.
    subprocess.run(["git", "-C", str(top), "update-index", "--add",
                    "--cacheinfo", f"100644,{blob_sha},{rel}"],
                   capture_output=True, text=True)
    sha = ""
    try:
        out = subprocess.run(
            ["git", "-C", str(top), "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=10)
        sha = (out.stdout or "").strip()
    except Exception:  # noqa: BLE001
        sha = ""
    # clause (2): the own-row commit is followed by the season-branch PUSH --
    # best-effort, one printed line, never fails the rotation (the helper
    # prints its own outcome to stderr). The push OUTCOME is surfaced on a
    # trailing line (``\npush: <line>``) so `_apply_successor_key_gated` can
    # gate the successor-<seat>.key swap on it: a push FAILED keeps the
    # predecessor key on disk until a later ack/prepare completes the swap.
    # Early returns above (no-git / commit-failed / byte-identical) carry NO
    # push line, so push reads as unknown -> never a push failure -> the key
    # may flip exactly as before (a commit SKIPPED / gitless case is not a
    # push failure).
    _push = _push_season_branch(root)
    # g15.26 claim (b): a successful push means origin now carries the
    # committed row -- so any deferred successor-key swap for this seat (a
    # `.key.pending` written when an earlier push FAILED) COMPLETES now
    # through the ONE shared helper (`_finish_pending_swap_on_push`): the
    # successor key is atomically put in place and the pending file
    # deleted. Best-effort; `_finish_pending_swap_on_push` never raises
    # (and returns '' -- no extra line -- when there is no push OK or no
    # pending swap to complete).
    _done = _finish_pending_swap_on_push(root, seat, _push)
    if _done:
        return (f"spawn_row_commit: committed (sha {sha}) -- seats.md "
                f"own-row only: {msg}\npush: {_push}\n{_done}")
    return (f"spawn_row_commit: committed (sha {sha}) -- "
            f"own-row only: {msg}\npush: {_push}")


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
    checked-out branch via `git rev-parse`, consults
    branches.is_legal_branch (the ONE legality rule, L4.311), and reports
    no-repo otherwise."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and (out.stdout or "").strip():
            branch = out.stdout.strip()
            if branches.is_legal_branch(branch):
                return f"legal on {branch!r}"
            return (f"NOT legal on {branch!r} (grid commit would be SKIPPED "
                    f"\u2014 season main or master only)")
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
#: L4.288 — the ack-path identity join is a best-effort back-fill, never a
#: gate: bounded SHORT (at most 5 s) so a join miss costs an ack at most a few
#: seconds, never an error exit and never a >5 s wait.
ACK_JOIN_POLL_S = 3


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


def transcript_from_registry(registry_json: Path) -> Path | None:
    """Derive a Claude Code transcript path from a harness REGISTRY file.

    The registry `<pid>.json` object carries `cwd` + `sessionId`, never a
    transcript path. The transcript lives at
    `~/.claude/projects/<cwd with every '/' and '.' replaced by '-'>/
    <sessionId>.jsonl` (L4.122 — the derivation gen X pinned by hand when
    `transcript` came back empty and meter_pin / model_confirm were SKIPPED).
    Returns None when the file is unreadable, parses to a non-object, or lacks
    `cwd` or `sessionId`. The caller decides whether an absent derived path is
    a silent skip or a named refusal."""
    try:
        data = json.loads(registry_json.read_text(encoding="utf-8",
                                                  errors="replace"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    # ONE derivation: the dict form (`transcript_from_registry_dict`, the
    # SL3.01 lift the autopsy and the join call) — this Path form only adds
    # the file read and the None-on-absent contract sensei.py relies on
    # (director fix-up at the SL3.01 harvest: SL3.03 and SL3.01 each lifted
    # the same derivation under the same name with different signatures).
    transc = transcript_from_registry_dict(data)
    return Path(transc) if transc else None


def _json_scalars(data):
    """Yield every scalar (string/number/bool) under a parsed registry dict."""
    if isinstance(data, dict):
        for v in data.values():
            yield from _json_scalars(v)
    elif isinstance(data, (list, tuple)):
        for v in data:
            yield from _json_scalars(v)
    else:
        yield data


def _registry_matches_window_id(data: dict, window_id: str) -> bool:
    """True when the parsed registry JSON carries `window_id` as a DELIMITED
    @<digits> token (l4-a-join-matches-the-delimited-window-token-and-keep-
    both-is-tested). NEVER a bare substring: `@30` matches the value
    `view:@30.%0` but NOT `view:@302.%0` (a wrong join would write a foreign
    session's identity into the seat's row behind the L4.288 back-fill). tmux
    stores the window as `@<id>.%<pane>`, so @<digits> must be followed by a
    NON-id character (`.`, quote, comma, brace, whitespace, or the end of the
    value) — id characters are digits/letters/underscore. When the window id
    is not a plain number it falls back to a whole-cell equality match."""
    digits = window_id.lstrip("@")
    if not digits.isdigit():
        return any(str(v) == window_id for v in _json_scalars(data))
    pat = re.compile(r"@%s(?![0-9A-Za-z_])" % re.escape(digits))
    return any(pat.search(str(v)) for v in _json_scalars(data))


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
                try:
                    data = json.loads(raw)
                except ValueError:
                    data = {}
                if not isinstance(data, dict):
                    data = {}
                # CLAUSE A (l4-a-join-matches-the-delimited-window-token-and-
                # keep-both-is-tested): match the window @id as a DELIMITED
                # token over the PARSED JSON, never a bare substring over the
                # raw text — @30 must NOT join the registry file of @302/@308.
                if not _registry_matches_window_id(data, token):
                    continue
                try:
                    pid = int(fp.stem)
                except ValueError:
                    pid = None
                sess = (data.get("session_id") or data.get("sessionId") or "")
                # Transcript path via the ONE shared derivation (L4.122: the
                # registry carries cwd + sessionId, never a transcript path —
                # derive `~/.claude/projects/<slug>/<sessionId>.jsonl`). Same
                # helper the recovery autopsy calls — never a copy.
                transc = transcript_from_registry_dict(data)
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
    legal on — the season branch (`season_branch()` under this round's season). A
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
                           seat_row: dict | None, commit: str | None,
                           generation: int | None = None):
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
    if key == "ack":
        # GOAL:g15.25 (SL7.29) — the ack fact derives from the ACK FILE, never
        #     from the seat row (no writer ever fills a `row['ack']`, so the
        #     old read printed `ack: SKIPPED: seat row carries no ack at HEAD`
        #     for every seat while the truth sat in seats/<seat>.ack.json).
        #     Shape: the BARE `<answer> (source <source>, gen <gen_after>)`
        #     when a live ack file exists, else `none` — the block writer
        #     (`_bootstrap_block`) prefixes the key ONCE (`- ack: {val}`), so
        #     a prefixed value here would render the doubled `- ack: ack: ...`
        #     (the SL7.15 defect part (a)). The staleness bound (`head` as
        #     today) is applied by the caller, unchanged.
        # GOAL:g15.25 (SL7.42) — a RE-SEATED post must not print a leftover
        #     PRIOR-generation ack file as this seating's. When the writer
        #     knows its own generation and the ack file carries a `gen_after`
        #     that is NOT it (a stale file from an earlier seating of the
        #     same seat name), the fact is NAMED `stale: gen N` — never
        #     printed as current. generation=None (the SL7.29 direct calls
        #     that predate the bound) keeps the old read.
        ack_path = _ack_path(root, seat)
        try:
            _a = (json.loads(ack_path.read_text(
                encoding="utf-8", errors="replace"))
                  if ack_path.exists() else None)
        except (OSError, ValueError):
            _a = None
        if isinstance(_a, dict) and _a.get("answer"):
            _g = _a.get("gen_after")
            if generation is not None and _g is not None:
                try:
                    _stale = int(_g) != int(generation)
                except (TypeError, ValueError):
                    _stale = False
                if _stale:
                    return f"stale: gen {_g}", None
            return (("{} (source {}, gen {})".format(
                _a.get("answer"), _a.get("source"), _g)),
                    None)
        return "none", None
    if key == "prev_gen":
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
                     overrides: dict | None = None,
                     join_poll_secs: int | None = None) -> str:
    """s10 — write the successor's bootstrap record.

    `<sessions>/seats/<seat>.bootstrap.json` carries the template telemetry
    set PLUS the owner's fixed fact set (BOOTSTRAP_FIXED_FACTS — "they should
    receive all this telemetry by default"), each resolved to a REAL value
    where the handover can see it (the commit stamp, the config:seats row at
    HEAD, the verification result; `git rev-parse --short HEAD` is the one
    read-only git command allowed) and to a NAMED `SKIPPED: <reason>` where it
    cannot yet (a join-only or sibling-round fact — never the old blanket
    `0b owns deriving`). Every derived fact is stamped in `measured_at` with
    the commit it was measured at, so `_bootstrap_stale` can mark any
    record not at HEAD stale per its `fact_bounds` entry (the facts are still
    emitted, each with a `[stale: ...]` mark, never withheld). Returns the
    written path (string).

    `join_pending` (a set of fact keys) and `overrides` (a key->value dict)
    support the PRE-SPAWN write (hypothesis:l4-startup-first-turn-is-
    performed-by-the-service-and-the-hook-fires-at-turn-one): a key present in
    `overrides` takes that resolved value (stamped at HEAD); a key in
    `join_pending` but NOT overridden is written as `pending: resolved after
    join` (not SKIPPED, not blank) because the @id join has not happened yet.
    Default ({} / {}) writes every fact through `_derive_bootstrap_fact`
    exactly as before — the post-join call passes the joined facts as
    overrides, so the same record is UPDATED in place, not re-minted.

    `join_poll_secs` is what makes a POST-join record truthful: when a join
    WAS attempted (the caller passes the effective bounded poll, seconds) but
    left a `join_pending` key still unresolved, that key is written
    `unresolved: join found nothing within <N>s` — never the PRE-join
    `pending: resolved after join`, which would lie that a future join will
    fix it. None (the pre-join first-seating write) keeps `pending: resolved
    after join`.
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
            if join_poll_secs is None:
                tele[key] = "pending: resolved after join"
            else:
                tele[key] = (f"unresolved: join found nothing within "
                             f"{join_poll_secs}s")
            continue
        value, reason = _derive_bootstrap_fact(
            key, root=root, seat=seat, seat_row=seat_row, commit=commit,
            generation=generation)
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


def _fact_bounds(root: Path) -> dict:
    """The `fact_bounds:` staleness map of config:rotations (the frontmatter
    of `.geometry/rotations.md`): fact -> 'head' | 'permanent'. Absent or
    malformed -> {}. Read from graph content (written by write.py, never a
    hand edit); `_bootstrap_block` falls back to it when no `bounds` kwarg is
    passed."""
    try:
        nf = frontmatter.load_node_file(_rotations_node_path(root))
        fb = nf.frontmatter.get("fact_bounds")
    except Exception:  # noqa: BLE001
        return {}
    if not isinstance(fb, dict):
        return {}
    return {str(k): ("permanent" if v == "permanent" else "head")
            for k, v in fb.items()}


def _stale_facts(doc: dict, current_commit: str | None,
                 bounds: dict | None = None) -> set:
    """The head-bound facts in a bootstrap record whose measured commit
    differs from HEAD — the facts the reader must mark `[stale: ...]`.
    `bounds` maps fact -> 'head' | 'permanent' (declared in config:rotations
    `fact_bounds`, default 'head'); a 'permanent' fact is never stale; an
    unbounded fact is treated as 'head'. A fact absent from `measured_at`
    asserted nothing and is never stale; a fully-skipped doc (no
    `measured_at`) is never stale."""
    measured = (doc or {}).get("measured_at") or {}
    bounds = bounds or {}
    stale = set()
    for fact, commit in measured.items():
        if bounds.get(fact, "head") == "permanent":
            continue
        if commit != current_commit:
            stale.add(fact)
    return stale


def _bootstrap_stale(doc: dict, current_commit: str | None,
                     bounds: dict | None = None) -> bool:
    """True when the bootstrap record carries a head-bound fact measured at a
    commit other than HEAD (the whole-block refusal the hook used to enforce),
    False otherwise. PRESERVED as the bool wrapper over `_stale_facts` so the
    whole-block refusal vocabulary survives for callers that want it;
    `_bootstrap_block` no longer refuses on it (staleness is now per-fact, a
    `[stale: ...]` mark, never a refusal). `bounds` maps fact -> 'head' |
    'permanent' (declared in config:rotations `fact_bounds`; default 'head')."""
    return bool(_stale_facts(doc, current_commit, bounds))


def _bootstrap_block(root: Path, seat: str, *, commit: str | None = None,
                     bounds: dict | None = None) -> list:
    """The successor's bootstrap record as ONE injected block, or REFUSES.

    The reader half of the bootstrap injection (hypothesis:l4-startup-is-one-
    script-or-a-driven-prompt, 0b kid 3). `<sessions>/seats/<seat>.bootstrap
    .json` is the record rotate-self's button-down wrote; this returns the
    tiny diagram-shaped block the SessionStart hook should inject for a seat
    successor that wakes KNOWING its state -- or REFUSES (returns [None,
    reason]) when the record is absent ('no_record'), not a JSON object
    ('malformed') — it never refuses on staleness. `commit` is
    the test seam for HEAD (defaults to `_git_head`); `bounds` is the
    fact->'head'|'permanent' staleness map of config:rotations `fact_bounds`
    (when None read from the node; default for an unbounded fact = 'head').
    Returns [block, None] — a head-bound fact measured at an older commit is
    emitted with a `[stale: measured@<sha>, HEAD@<sha>]` mark, a permanent
    fact is never marked."""
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
    if bounds is None:
        bounds = _fact_bounds(root)
    stale = _stale_facts(doc, commit, bounds)
    gen = doc.get("generation")
    gen_s = f"gen {gen}" if isinstance(gen, int) else "gen ?"
    head = f"HEAD@{commit}" if commit else "HEAD@?"
    lines = [
        f"## ⚓ bootstrap: {seat} successor handover",
        f"(shape {doc.get('shape', '?')} · {gen_s} · {head})",
        "",
    ]
    measured = doc.get("measured_at") or {}
    tele = doc.get("telemetry")
    if isinstance(tele, dict) and tele:
        for key in sorted(tele):
            val = str(tele[key])
            if len(val) > 400:
                val = val[:397] + "…"
            if key in stale:
                msha = measured.get(key)
                m = msha if msha else "?"
                val = f"{val}  [stale: measured@{m}, HEAD@{commit or '?'}]"
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
    "prime_ref", "prime_key", "prime_seat", "worktree",
    "repo", "tmux_session", "pred_pids",
}

#: Per-placeholder CODE fallbacks: a used `{key}` whose value is EMPTY is
#: replaced by this WHOLE FRAGMENT (each `{...}` inside it resolved fresh
#: against the spawn values) instead of refusing, when the entry names no
#: `fallback:` of its own. `{prime_ref}` falls back to the by-key whois form:
#: the prime row's session_ref is EMPTY for a whole generation under SL7.06's
#: default, but its pubkey is filled at every rotation — so prime authority
#: resolves by key, never by a refusal that leaves F3's by-ref channel without
#: a ref (goal:g15.25 line (4); hypothesis:l4-prime-authority-resolves-by-key-
#: when-the-prime-rows-session-ref-is-empty...). The fragment must carry the
#: `--key` FLAG itself: substituting only the pubkey VALUE would land it in
#: the POSITIONAL session_ref slot, where whois resolves by session_ref and
#: answers NO-MATCH, never IS-AUTHORIZED.
_STARTUP_FALLBACKS = {
    "prime_ref": "--key {prime_key}",
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
        # `_resolve_shell_vars_per_token` expands `$VAR` from the whole
        # environment at
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
#: _resolve_shell_vars_per_token), never handed to a shell.
_STARTUP_SHELL_OPS = ("&&", "||", "$(", "`", "<<", ">>", ">",
                     "<", "&", "\n")


def _operator_refusal(command_or_tokens) -> str | None:
    """Return a one-line named refusal if `command` contains an unmodeled
    shell operator (`&&` `||` `$(...`  backtick `<` `>` `<<` `>>` `&` newline),
    else None. `|` and `;` are modeled separators (the no-shell executor wires
    them explicitly) and `$VAR`/`${VAR}` expands from env, so none of those
    trip this gate. Checked at allowlist time AND again on the resolved command
    before it runs (belt over the no-shell executor). Accepts a command string
    or a resolved structural token list."""
    if isinstance(command_or_tokens, str):
        text = command_or_tokens
    else:
        # structural form: any operator text carried in a token (an env VALUE
        # holding `&&`, or a placeholder-injected one) is still refused — the
        # separator chars are model edges, the rest is data and checked here.
        text = "".join(t for _, t in command_or_tokens)
    for op in _STARTUP_SHELL_OPS:
        if op in text:
            name = "newline" if op == "\n" else op
            return f"unmodeled shell operator {name!r} in first_turn command"
    return None

_SHELL_VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")


def _resolve_shell_var(m: "re.Match") -> str:
    """Return the env value for one `$VAR`/`${VAR}` match, or REFUSE (raise
    ValueError, naming the var) if it is unset. Used by the per-token resolver
    (_resolve_shell_vars_per_token). It is NO-SHELL: the value is substituted
    AS A LITERAL and never handed to a shell. Only this bare env form is
    modeled; `$(` command substitution is refused by _operator_refusal before
    it is reached."""
    name = m.group(1) or m.group(2)
    val = os.environ.get(name)
    if val is None:
        raise ValueError(f"first_turn env var ${name} is not set")
    return val


def _tokenize_struct(command: str) -> list:
    """Tokenize `command` into the STRUCTURAL form the stage grammar consumes:
    a list of ("sep", punct) elements for each genuine BARE `|`/`;` separator
    and ("arg", value) elements for every literal argv token. The punctuation-
    vs-boundary decision is made HERE, at tokenize time, so a token that is not
    itself a bare `|`/`;` (a normal argv element, or an env `$VAR` reference)
    is tagged "arg" and no later substitution can turn it into a boundary.
    A QUOTED punctuation char such as `'|'` in the template is emitted, as
    before, as a bare `|` token (token text loses the quote): it was already
    an unquoted-stage edge in _startup_units and stays one. Raises
    _StartupParseError on an unparseable command."""
    out = []
    for t in _tokenize_startup(command):
        if t == "|" or t == ";":
            out.append(("sep", t))
        else:
            out.append(("arg", t))
    return out


def _as_tokens(command_or_tokens):
    """Accept either a command STRING or a resolved structural token list
    (from _resolve_shell_vars_per_token) and return a structural token list.
    Lets the one stage grammar serve both the allowlist judge (a literal
    string, env UNEXPANDED — so `$HOME` stays literal, as before) and the
    first_turn executor (which passes its already-env-resolved structure)."""
    if isinstance(command_or_tokens, str):
        return _tokenize_struct(command_or_tokens)
    return command_or_tokens


def _resolve_shell_vars_per_token(command: str) -> list:
    """Expand `$VAR`/`${VAR}` PER ARGV ELEMENT and return the STRUCTURAL token
    list (not a re-serialised string): ("sep", punct) for each bare `|`/`;`
    separator, ("arg", value) for each literal argv element with its `$VAR`
    references replaced by the env value as ONE whole element.

    This never re-parses: the boundary decision is fixed by _tokenize_struct
    BEFORE substitution, so an env VALUE that is exactly a shlex punctuation
    char (`|`, `;`, ...) stays a single ("arg", "|") element and cannot inject
    a stage — the thing a string round-trip through shlex.join could not do
    (hypothesis:l4-a-bare-separator-env-value-cannot-inject-a-stage). A value
    carrying a double quote, a space, or a `|`/`;` cannot add an argv element
    or a boundary; what the judge and executor see is exactly the argv that
    will run. Raises _StartupParseError (unparseable command, named) or
    ValueError (an unset `$VAR`, named); never returns an unexpanded `$VAR`."""
    out = []
    for kind, t in _tokenize_struct(command):
        if kind == "arg":
            out.append(("arg", _SHELL_VAR_RE.sub(_resolve_shell_var, t)))
        else:
            out.append((kind, t))
    return out


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


def _startup_units(command_or_tokens) -> list:
    """Quote-aware split of a command into `;`-units of `|`-stages, from its
    STRUCTURAL token list (a string is tokenized first by _as_tokens). Returns
    a list of units, each a list of stages, each a list of argv tokens, with
    the bare `|`/`;` separator elements consumed as boundaries and every "arg"
    element (an env value included WHOLE) retained. A bare `|` closes the
    current stage; a bare `;` closes the current unit. Runs NOTHING. Both the
    allowlist judge and the no-shell executor derive their groups from this
    one function."""
    units, stages, cur = [], [], []
    for kind, t in _as_tokens(command_or_tokens):
        if kind == "sep" and t == "|":
            if cur:
                stages.append(cur)
                cur = []
        elif kind == "sep" and t == ";":
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


def _command_units(command_or_tokens) -> list:
    """Parse a (fully resolved) first_turn command into sequential `;`-units,
    each a list of `|`-stage (argv, env_prefix) pairs. A leading `VAR=value`
    prefix token of a stage is retained and applied as THAT ONE stage's
    environment (never the whole command); it is stripped from the argv. Runs
    NOTHING. Same grammar as the allowlist judge (_segment_parts): both derive
    from _tokenize_struct / _startup_units, so the separators are identical
    (unquoted `|`/`;` only) and nothing outside these tokens can reach the box.
    Accepts a command string or a resolved structural token list.
    Raises _StartupParseError on an unparseable command."""
    units = []
    for stage_list in _startup_units(command_or_tokens):
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


def _segment_parts(command_or_tokens) -> list:
    """Split a first_turn command into producing pipeline parts, quote-aware
    (a `|`/`;` inside quotes stays inside its argument). Returns one token-
    list per `|`-/`;`-part, a leading env assignment skipped per part. THE SAME
    grammar as the no-shell executor (_command_units): both derive from
    _tokenize_struct / _startup_units, so the judge and the executor split on
    identical separators (unquoted `|`/`;` only) and cannot diverge. Accepts a
    command string or a resolved structural token list. Raises
    _StartupParseError on an unparseable command; the allowlist guard turns
    that into a refusal, never a crash."""
    parts = []
    for stage_list in _startup_units(command_or_tokens):
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


def _producing_refusal(command_or_tokens) -> str | None:
    """Return a one-line refusal (naming the executable/verb) if ANY producing
    pipeline part of `command` is not on the startup allowlist, else None.

    Pipeline filters (head/grep/sed/...) after a `|` are allowed; every
    PRODUCING segment (`;`- or `|`-first) must pass the strict allowlist.
    An unmodeled shell operator (`&&` `||` `&` `$(...)` backtick `<` `>`
    `>>` newline) is refused first with its name — the floor that keeps the
    grammar closed even if a future executor reintroduces a shell.
    Accepts a command string or a resolved structural token list."""
    op = _operator_refusal(command_or_tokens)
    if op:
        return op
    try:
        units = _startup_units(command_or_tokens)
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


def _env_prefix_refusal(command_or_tokens, allow: frozenset) -> str | None:
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
    the executor collects prefixes. Accepts a command string or a resolved
    structural token list."""
    try:
        units = _startup_units(command_or_tokens)
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


def _resolve_fallback_fragment(frag: str, emptied_key: str,
                               values: dict) -> str:
    """Resolve every `{k}` inside a fallback FRAGMENT fresh against
    ``values``. Fail closed -- unknown key, a key whose value is EMPTY, or a
    key that IS the emptied placeholder (a fragment must not substitute
    itself) all raise a named ValueError. A `#{...}` tmux format form stays
    literal, byte-for-byte."""
    def _fsub(m):
        if m.start() > 0 and frag[m.start() - 1] == "#":
            return m.group(0)
        fk = m.group(1)
        if fk not in STARTUP_PLACEHOLDERS:
            raise ValueError(f"unknown startup placeholder {{{fk}}}")
        if fk == emptied_key:
            raise ValueError(
                f"startup fallback {{{fk}}} references the empty placeholder "
                "it substitutes")
        fv = values.get(fk, "")
        if not str(fv):
            raise ValueError(
                f"startup fallback {{{fk}}} empty at spawn "
                f"(placeholder {{{emptied_key}}} is empty)")
        return str(fv)
    return re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", _fsub, frag)


def _resolve_startup_placeholders(command: str, values: dict, *,
                                  refuse_empty: bool = False,
                                  fallback: str = "") -> str:
    """Substitute `{key}` placeholders; REFUSE (raise ValueError, naming the
    key) on any key not in the canonical STARTUP_PLACEHOLDERS set, so an
    unknown/unresolved placeholder is never silently left in the command.
    With `refuse_empty=True` (the first_turn path only), a placeholder the
    command USES whose value resolves to EMPTY is ALSO refused, naming the
    placeholder (`placeholder {key} empty at spawn`), instead of producing a
    command that runs on an empty slot and dumps a usage error. Other callers
    (the driven `next` walk, bootstrap) leave `refuse_empty` False: for them
    an empty placeholder may be legitimate, and they must not be forced to
    fall over on it.

    ``fallback`` (a WHOLE FRAGMENT string, from a per-entry ``fallback:`` on
    the first_turn template) supplies the substitution
    (hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-
    session-ref-is-empty...): when an emptied placeholder WOULD refuse, the
    fragment -- each `{...}` inside it resolved fresh against ``values`` -- is
    substituted INSTEAD. ``{prime_ref}`` empty falls back to the by-key form
    ``--key {prime_key}``. When the entry names NO fallback, the per-
    placeholder code map ``_STARTUP_FALLBACKS`` supplies one, so the CURRENT
    director template resolves prime authority by key without a template
    edit. When neither names a usable fallback (or the fallback's own
    placeholder is empty or references the emptied placeholder) the refusal
    stands (named), so a placeholder never runs empty and never silently
    self-declares a fallback."""
    def _sub(m):
        # A `{name}` that is part of tmux's OWN format syntax is LITERAL and
        # must pass through byte-for-byte: it is immediately preceded by `#`
        # (`#{window_id}`, `#{window_name}`, `#{...}`, or the newer
        # `#{...}` forms). Treating it as a startup placeholder both refused
        # the whole join command and would corrupt the literal tmux needs
        # (hypothesis:l4-startup-first-turn-is-performed-by-the-service-...).
        # A bare `{name}` NOT preceded by `#` still refuses below.
        if m.start() > 0 and command[m.start() - 1] == "#":
            return m.group(0)
        key = m.group(1)
        if key not in STARTUP_PLACEHOLDERS:
            raise ValueError(f"unknown startup placeholder {{{key}}}")
        value = values.get(key, "")
        if refuse_empty and not str(value):
            frag = fallback or _STARTUP_FALLBACKS.get(key, "")
            if frag:
                return _resolve_fallback_fragment(frag, key, values)
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
        # A per-entry `fallback:` (e.g. "fallback: --key {prime_key}") names a
        # WHOLE FRAGMENT substituted when a USED placeholder is EMPTY -- so a
        # prime-authority entry whose {prime_ref} is empty resolves by the
        # prime row's pubkey (by-key form, flags included), not by a bare
        # value dropped into the positional slot
        # (hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-
        # session-ref-is-empty-and-a-placeholder-with-a-fallback-never-
        # refuses). An entry with NO fallback of its own still resolves
        # through the per-placeholder code map `_STARTUP_FALLBACKS` (so the
        # CURRENT director template works without a template edit); an empty
        # or unresolvable fallback fails closed too: the refusal names it.
        fallback = str(entry.get("fallback") or "")
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
            record_cmd = _resolve_startup_placeholders(
                cmd, values, refuse_empty=True, fallback=fallback)
        except ValueError as exc:
            results.append({"label": label, "cmd": cmd, "refused": str(exc)})
            continue
        # Two forms (fix b): `record_cmd` keeps `$VAR` LITERAL — what the result
        # dict's `cmd` and dry-run report, byte-identical to the pre-expansion
        # text so a secret never lands in the record. `exec_tokens` env-expands
        # the STRUCTURAL token list PER ARGV ELEMENT (never a whole-string
        # re-serialisation) and is used ONLY to build the no-shell argv;
        # execution needs the value, the record must not hold it. A value
        # carrying a double quote, a space, or a `|`/`;` stays inside ONE argv
        # element and is never re-parsed — the boundary decision is fixed at
        # tokenize time, so even a value that IS exactly a punctuation char
        # cannot inject a stage (hypothesis:l4-an-env-value-cannot-break-a-
        # quoted-argument, hypothesis:l4-a-bare-separator-env-value-cannot-
        # inject-a-stage).
        try:
            exec_tokens = _resolve_shell_vars_per_token(record_cmd)
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
        # judge never saw it. An ENV value cannot inject one (expansion keeps
        # it inside one element), but the re-judge still runs on exec_tokens so
        # what is judged is what is executed. Re-run the env
        # allowlist and the producing allowlist BEFORE _command_units splits it,
        # so an injected `touch`-style stage is refused, not run, and its
        # `$VAR` stays literal in the record (hypothesis:l4-the-judge-runs-on-
        # the-substituted-command).
        exec_env_refusal = _env_prefix_refusal(exec_tokens, env_allow)
        if exec_env_refusal:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": _scrub_injected_refusal(
                                exec_env_refusal, record_cmd)})
            continue
        exec_refusal = _producing_refusal(exec_tokens)
        if exec_refusal:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": "not on startup.allow: "
                                       + _scrub_injected_refusal(
                                           exec_refusal, record_cmd)})
            continue
        # Unmodeled-operator check stays: an operator `_producing_refusal`
        # deliberately does not model (e.g. `&&`) is caught here. `$VAR` is
        # expanded for execution only; the record keeps the literal `$VAR`.
        op = _operator_refusal(exec_tokens)
        if op:
            results.append({"label": label, "cmd": record_cmd,
                            "refused": op})
            continue
        if dry_run:
            results.append({"label": label, "cmd": record_cmd, "dry": True})
            continue
        try:
            units = _command_units(exec_tokens)
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


def _first_seating_run(root: Path, *, seat: str, role: str,
                       succ_name: str,
                       tmux_session: str = DEFAULT_TMUX_SESSION,
                       dry_run: bool = False,
                       ask_diff: bool = False,
                       generation: int | None = None) -> tuple[str, list]:
    """First-seating STARTUP composition (hypothesis:l4-a-first-seating-is-a-
    rotation-without-a-predecessor).

    A FIRST seating — a brand-new seat hand-spawned through `rotate.py spawn`\
    or `seats-launch` — generation 1, no predecessor — runs the SAME role
    template `startup.first_turn` a rotation runs, through the SAME composer
    (rotate-self's `_run_first_turn_commands` / `_compose_startup_output`, one
    code path, never a copy). Returns `(block, results)`; `block` is the
    successor's `## STARTUP OUTPUT` text (empty when the role declares no
    first_turn or no rotation template exists — a first seating fails soft,
    it is an unseated convenience, not a rotation) and `results` is the per-
    command first_turn result list a first-seating seating record carries
    (hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-
    does, g15.17 item 3). `{gen}` resolves to 1 and `{pred_pids}` to the NAMED
    first-seating value 'none: first seating' (a real rotation carries the
    actual predecessor pids; an EMPTY pred_pids is the L4.179 named refusal —
    a first seating never refuses on an empty predecessor slot, it names the
    condition instead). `dry_run` composes without running commands or writing
    the bootstrap record; a real composition writes the gen-1 first-seating
    bootstrap record.
    """
    role_tmpl, _name, _src = _resolve_template(
        root, role, None, where="first-seating")
    if role_tmpl is None:
        return "", []
    startup = (role_tmpl or {}).get("startup") or {}
    if not (startup.get("first_turn") or []):
        return "", []
    # GOAL:g15.25 (SL7.49) — a FIRST seating of an EXISTING seat (crash
    # respawn, hand relaunch, `seats-launch`/`spawn --seat` onto a row whose
    # config:seats entry already carries `generation: N >= 1`) must report
    # the SEAT'S OWN row generation, never a hard-coded gen-1. The row is the
    # authority (`_seat_row_generation`, the SAME reader cmd_spawn already
    # uses), so this run's bootstrap header, its record generation, the
    # `{gen}` substitution and the ack file all agree. A brand-new seat (no
    # row, or a row with no generation) resolves to `FIRST_SEATING_GEN` and
    # is byte-identical to today. Callers may pass the gen explicitly; when
    # they pass nothing the resolution happens here, once, for BOTH call
    # sites (cmd_spawn and seats-launch) so neither recomputes it.
    _gen = generation if generation is not None \
        else (_seat_row_generation(root, seat) or FIRST_SEATING_GEN)
    values = _first_turn_values(
        root, seat=seat, gen=_gen, succ_name=succ_name,
        pred_pids="none: first seating", tmux_session=tmux_session)
    results = _run_first_turn_commands(startup, values, dry_run=dry_run)
    block = _compose_startup_output(results)
    if block and not dry_run:
        # GOAL:g15.25 (SL7.42) — a first seating has NO predecessor (gen 1),
        #     so its turn-one bootstrap `ack` fact must name the SOURCE
        #     `first-seating`, never `predecessor`, and must not fall through
        #     to `_derive_bootstrap_fact` — which would print `ack: none`
        #     (no ack file yet) or, on a RE-SEATED post, a STALE prior-gen
        #     answer still sitting in seats/<seat>.ack.json. This post acks
        #     itself once (`continue`; F8/SL7.06 default), so the truthful
        #     turn-one value is supplied verbatim through the SAME `overrides`
        #     seam the rotation path (cmd_rotate_self step 2.75) uses — one
        #     override, no new flag.
        # GOAL:g15.25 (SL7.42) — the turn-one value must track the MODE this
        #     seat will actually have. `cmd_spawn --ask-diff` inherits its ack
        #     open (`_first_seating_spawn_writes` writes answer
        #     `diff-requested` into seats/<seat>.ack.json), so a bootstrap
        #     record that says `continue` while the ack channel it opened says
        #     `diff-requested` is the same lie this node exists to kill — just
        #     in the ask-diff mode. The bootstrap ANSWER must equal the ack
        #     file's answer; SOURCE stays `first-seating` (never
        #     `predecessor`) in both modes. seats-launch (no ask-diff) is
        #     unchanged: default-`continue`. One caller parameter, no new flag.
        _answer = "diff-requested" if ask_diff else "continue"
        _ack_override = (
            f"{_answer} (source first-seating, gen {_gen}) — "
            "this post awaits one diff answer" if ask_diff else
            f"continue (source first-seating, gen {_gen}) — "
            "this post acks once itself")
        _write_bootstrap(root, seat=seat, generation=_gen,
                         telemetry=role_tmpl.get("telemetry"),
                         verification=None,
                         join_pending=set(BOOTSTRAP_JOIN_ONLY_FACTS),
                         overrides={"ack": _ack_override})
    return block, results


def _first_seating_startup(root: Path, *, seat: str, role: str,
                           succ_name: str,
                           tmux_session: str = DEFAULT_TMUX_SESSION,
                           dry_run: bool = False) -> str:
    """The block half of `_first_seating_run` — retained so a caller that
    only needs the STARTUP OUTPUT text (no seating record) keeps one call.
    """
    block, _results = _first_seating_run(
        root, seat=seat, role=role, succ_name=succ_name,
        tmux_session=tmux_session, dry_run=dry_run)
    return block


def _prime_pushed_seats(root: Path, ref: str):
    """Fetch the pushed season seats AT MOST ONCE per process for the
    (str(root), ref) key, reusing the fetched rows on every later call. This
    is the SEAM behind `_prime_row_authority` (hypothesis:l4-rotate-self-
    fetches-the-pushed-season-ref-once-per-run-through-a-seam-and-no-suite-
    test-reaches-origin): one rotation builds first_turn values at FIVE sites
    (first seating, a second compose, driven startup, startup values,
    after-join values), each of which would otherwise run a REAL `git fetch
    origin <name>` (send._pushed_seats with do_fetch=True calls _run_git, up
    to 30 s each). The memo collapses those to ONE fetch; every later build
    reuses the fetched rows. A None result (pushed ref unreachable) is also
    memoized, so a rotation does not re-fetch on a transient miss within the
    same process. A test injects the seam by monkeypatching THIS name (or
    `send._pushed_seats` below it) so a rotate-self values build never
    performs a real git fetch inside the suite."""
    key = (str(root), ref)
    if key in _PUSHED_SEATS_FETCHED_ONCE:
        return _PUSHED_SEATS_FETCHED_ONCE[key]
    import send  # local: same dir (send.py pattern, no import cycle)
    try:
        seeded = send._pushed_seats(root, ref, True)
    except Exception:                                       # noqa: BLE001
        seeded = None
    _PUSHED_SEATS_FETCHED_ONCE[key] = seeded
    return seeded


def _prime_rows_fetch_clear() -> None:
    """Drop the per-process fetch memo; a test calls this to reset between
    runs. The memo is intentionally module-global (one fetch per process), so
    isolation is by explicit clear — the standard pytest monkeypatch shape."""
    _PUSHED_SEATS_FETCHED_ONCE.clear()


#: Per-process memo so the pushed season ref behind `_first_turn_values` is
#: fetched AT MOST ONCE per rotate-self run, keyed on (str(root), ref) so two
#: separate roots in one process do not collide. The fetch itself is the REAL
#: network call (send._pushed_seats → _run_git, up to 30 s each), so without
#: this a single rotation's five first_turn values builds would fetch five
#: times — up to 150 s worst case inside the rotation's own timeout. Tests
#: clear it via `_prime_rows_fetch_clear` and may inject a fake seam.
_PUSHED_SEATS_FETCHED_ONCE: dict[tuple, object] = {}


def _prime_row_authority(root: Path) -> tuple[dict | None, str]:
    """The prime row for the startup placeholder map, read the way whois
    reads it — ONE reader: the PUSHED season ref first (`send._pushed_seats`,
    the SAME ref whois authorizes against, fetch included, via the once-per-
    process seam `_prime_pushed_seats`), the working-tree seat row only as a
    FALLBACK when the pushed ref is unreachable. A deferred-key window (a
    pending key persisted when the
    push FAILED, SL7.22) leaves the ROTATING worktree's prime row carrying a
    key the PUSHED authority does not — so a startup {prime_key} read from the
    worktree can name a key the pushed row never carries and read
    NO-MATCH/RETIRED for a live Prime (hypothesis:l4-prime-key-is-read-from-
    the-pushed-ref-and-whois-key-with-sig-resolves-the-sig-row-by-pubkey).
    Returns (row, source) with source ``"pushed"`` or
    ``"worktree (pushed ref unreachable)"``."""
    import send  # local: same dir (send.py pattern, no import cycle)

    def _pick(rows):
        for row in (rows or []):
            if row.get("role") == "prime_director":
                return row
        return None

    seeded = _prime_pushed_seats(root, send._PUSHED_SEATS)
    if seeded is not None:
        rows, _sha, _ref = seeded
        return _pick(rows), "pushed"
    # Pushed authority unreachable — the FALLBACK, named as such so a reader
    # never mistakes a rotation-local key for the pushed prime.
    return _pick(_load_seats(root)), "worktree (pushed ref unreachable)"


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
    prime_key = ""
    prime_seat = ""
    # The prime row is read the way whois reads it — ONE reader: the PUSHED
    # season ref first, the working-tree seat row only as a fallback when the
    # ref is unreachable. A deferred-key
    # window (a pending key persisted when the push FAILED, SL7.22) leaves the
    # ROTATING worktree's prime row carrying a key the PUSHED authority does
    # not — a {prime_key} read from the worktree would name a key the pushed
    # row never carries and read NO-MATCH/RETIRED for a live Prime
    # (hypothesis:l4-prime-key-is-read-from-the-pushed-ref-and-whois-key-with-
    # sig-resolves-the-sig-row-by-pubkey).
    prime_row = _prime_row_authority(root)[0]
    if prime_row is not None:
        if prime_row.get("session_ref"):
            prime_ref = str(prime_row["session_ref"])
        # The prime row's pubkey and name ARE filled at every rotation
        # (SL4.07 / SL7.09 key_history), so {prime_key}/{prime_seat} are the
        # by-key fallback axes a startup entry with an EMPTY prime session_ref
        # declares (hypothesis:l4-prime-authority-resolves-by-key-when-the-
        # prime-rows-session-ref-is-empty...).
        if prime_row.get("pubkey"):
            prime_key = str(prime_row["pubkey"])
        if prime_row.get("name"):
            prime_seat = str(prime_row["name"])
    return {
        "seat": seat,
        "succ_ref": succ_ref or "",
        "succ_name": succ_name,
        "succ_transcript": succ_transcript or "",
        "pin_ref": str(_sessions_dir(root) / f"{seat}.meter"),
        "gen": str(gen),
        "prime_ref": prime_ref,
        "prime_key": prime_key,
        "prime_seat": prime_seat,
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
DEFAULT_AFTER_JOIN_POLL_S = 1.0


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


def _transcript_live_model(transcript) -> str | None:
    """The FIRST `"model":"..."` value in the successor transcript path,
    else None. The ONE parse the after_join model-confirm poll shares with
    `_confirm_successor_model` — a transcript that carries an assistant turn
    carries a model line, and that is the signal the poll waits on."""
    if not transcript:
        return None
    p = Path(str(transcript)).expanduser()
    if not p.exists():
        return None
    for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.search(r'"model"\s*:\s*"([^"]+)"', ln)
        if m:
            return m.group(1)
    return None


def _transcript_refusal_fallback(transcript) -> str | None:
    """The LAST `model_refusal_fallback` SYSTEM event in the successor
    transcript (jsonl), as a one-line readable string, else None. The ONE
    parse that fills the bootstrap `model_refusal_fallback` join-only fact
    after join — DIFFERENT from `_transcript_live_model` (assistant-turn
    model), this reads the `subtype: model_refusal_fallback` system event the
    SAME way verification.check_seat_model's scan does (timestamp +
    apiRefusalCategory + requestId), so the bootstrap fact carries the same
    truth the seat-model check would surface. Only the LAST event is kept,
    matching verification's read. Unparseable lines are skipped, never
    raised."""
    if not transcript:
        return None
    p = Path(str(transcript)).expanduser()
    if not p.exists():
        return None
    fb = None
    for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            o = json.loads(ln)
        except ValueError:
            continue
        if not isinstance(o, dict):
            continue
        if o.get("subtype") != "model_refusal_fallback":
            continue
        ts = o.get("timestamp")
        fb = (f"ts={ts} category={o.get('apiRefusalCategory')} "
              f"requestId={o.get('requestId')}"
              if ts is not None else "present")
    return fb


def _after_join_model_confirm(root: Path, *, seat: str, values: dict,
                              poll_interval: float, budget_s: float,
                              sleep_impl=None, poll_turn_fn=None,
                              confirm_model=None):
    """goal:g15.25 (SL7.40 (a)) — perform `_confirm_successor_model` ONCE, in
    the after_join, after the successor transcript carries its first assistant
    turn. POLL the transcript (turn-driven, never a bare fixed sleep) for up to
    `budget_s` in `poll_interval` ticks; when a turn appears early the confirm
    runs at that tick, else the record NAMES the skip `skipped: no assistant
    turn within <budget>s`. `poll_turn_fn(transcript) -> live_model|None`
    (default `_transcript_live_model`), `confirm_model(**kw)` (default
    `_confirm_successor_model`) and `sleep_impl` are the fixture seams so a
    fake transcript can gain an assistant turn mid-wait without real sleep.
    Returns the confirm result (dict, or a named skip string)."""
    if poll_turn_fn is None:
        poll_turn_fn = _transcript_live_model
    if confirm_model is None:
        confirm_model = _confirm_successor_model
    row = _find_seat(root, seat) or {}
    pid = values.get("pid")
    transcript = values.get("succ_transcript") or ""
    waited = 0.0
    if transcript:
        steps = int(budget_s // poll_interval) if poll_interval > 0 else 0
        for _ in range(steps):
            if poll_turn_fn(transcript):
                break
            if sleep_impl is not None:
                sleep_impl(poll_interval)
            else:
                time.sleep(poll_interval)
            waited += poll_interval
    mc = confirm_model(
        seat=seat,
        expected_model=((row.get("model") if row else None)
                        or values.get("expected_model")),
        expected_effort=((row.get("effort") if row else None)
                         or values.get("expected_effort")),
        pid=pid, transcript=transcript)
    if isinstance(mc, str):
        return (f"skipped: no assistant turn within {int(budget_s)}s "
                f"(after_join poll waited {int(waited)}s) — "
                "successor has not answered")
    mc["confirm_at"] = "after_join"
    return mc


def _fill_bootstrap_join_facts(root: Path, *, seat: str,
                               live_model: str | None,
                               refusal_fallback: str | None) -> bool:
    """(goal:g15.25 SL7.40 (a)) fill the pre-spawn bootstrap record's TWO
    join-only facts the after_join confirm can now supply —
    `successor_live_model` and `model_refusal_fallback` — THROUGH the existing
    `_write_bootstrap` `overrides` seam: the SAME post-join rewrite rotate-self
    uses to resolve the join-only facts in place (never a new record, never a
    re-mint). run_after_join holds no template/verification/generation (the
    service-layer caller owns only the record file), so the record's own
    telemetry / verification / generation are reconstructed from the existing
    file to reach the seam; any OTHER join-only fact already resolved in that
    record (e.g. `successor_address` set by rotate-self before it handed
    after_join to the service) is carried through as an override so the
    rewrite never clobbers a value another path already resolved.
    No-op (False) when there is no live model, no bootstrap file, or the
    record will not parse — never raises."""
    if not live_model:
        return False
    bpath = _sessions_dir(root) / "seats" / f"{seat}.bootstrap.json"
    try:
        if not bpath.exists():
            return False
        b = json.loads(bpath.read_text(encoding="utf-8", errors="replace"))
        if not isinstance(b, dict):
            return False
        tele = b.get("telemetry")
        if not tele:
            return False
        # carry already-resolved join facts through the seam so a rewrite never
        # clobbers a value rotate-self already put in the record
        overrides: dict = {}
        if isinstance(tele, dict):
            for k in BOOTSTRAP_JOIN_ONLY_FACTS:
                v = tele.get(k)
                if (v is not None
                        and not (isinstance(v, str)
                                 and v.startswith(("pending:", "unresolved:",
                                                  "SKIPPED:")))):
                    overrides[k] = v
        overrides["successor_live_model"] = str(live_model)
        if refusal_fallback:
            overrides["model_refusal_fallback"] = refusal_fallback
        verification = b.get("verification")
        if not isinstance(verification, dict):
            verification = None
        _write_bootstrap(
            root, seat=seat,
            generation=b.get("generation"),
            telemetry=tele,
            verification=verification,
            overrides=overrides,
            join_pending=(set(BOOTSTRAP_JOIN_ONLY_FACTS) - set(overrides)))
        return True
    except (OSError, ValueError):
        return False


def run_after_join(root, *, seat: str, gen: int, startup: dict,
                   values: dict, record_path: str | None = None,
                   dry_run: bool = False, sleep_impl=None,
                   delay_override: float | None = None,
                   send_dm=None, timeout_s: int | None = None,
                   byte_cap: int | None = None,
                   poll_interval: float | None = None,
                   poll_turn_fn=None, confirm_model=None) -> dict:
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
    # (goal:g15.25 SL7.40 (a)) successor MODEL CONFIRM — performed ONCE here,
    # in the after_join, after the successor transcript carries its first
    # assistant turn (poll, never a bare fixed sleep; turn-driven within the
    # existing after_join timeout). The rotate-self pre-turn call (which, on
    # a real rotation, runs before the successor has answered) now records
    # `deferred: after_join`; THIS is the one confirm that actually fires.
    # Written into the SAME rotation record's `handover.model_confirm` in
    # place (never a new record, never a re-mint), and `successor_live_model`
    # is filled into the pre-spawn bootstrap record best-effort. Only runs
    # for a call that owns a rotation record to update (the service/performer
    # path with a resolved successor identity).
    model_confirm = None
    if not dry_run and record_path is not None:
        budget = timeout
        inter = (poll_interval if poll_interval is not None
                 else float(DEFAULT_AFTER_JOIN_POLL_S))
        model_confirm = _after_join_model_confirm(
            root, seat=seat, values=values,
            poll_interval=inter, budget_s=float(budget or 0),
            sleep_impl=sleep_impl, poll_turn_fn=poll_turn_fn,
            confirm_model=confirm_model)
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
                if model_confirm is not None:
                    hov = rec.get("handover")
                    if not isinstance(hov, dict):
                        hov = {}
                    hov["model_confirm"] = model_confirm
                    rec["handover"] = hov
                    if (isinstance(model_confirm, dict)
                            and model_confirm.get("live")):
                        _fill_bootstrap_join_facts(
                            root, seat=seat,
                            live_model=str(model_confirm["live"]),
                            refusal_fallback=_transcript_refusal_fallback(
                                values.get("succ_transcript") or ""))
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
            "model_confirm": model_confirm,
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
        # A crash-recovery `result: respawned` record is a rotation the service
        # must pick up too (L4.292): the recovered seat's after_join (join ->
        # pin -> pending ack) runs exactly as a rotated seat's does. One-line
        # widening of the accepted results for that rotation only.
        ok_result = rec.get("result") in ("started", "success")
        crash_ok = (rec.get("rotation") == "crash-recovery"
                    and rec.get("result") == "respawned")
        if isinstance(rec, dict) and (ok_result or crash_ok):
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
    # (l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-and-
    # autopsy-share-one-pid) key the after_join successor on the RECORD's
    # captured join window @id, re-joined through the SAME `_join_successor` so
    # the after_join and the spawn gate/autopsy share one identity (poll =
    # ONE poll interval = a single registry read over the already-up
    # successor, never the bounded 60s wait; poll 0 reads zero times by the
    # loop's shape, see the registry join deadline). A record with no window
    # @id does NO join and behaves as before.
    join = _record_join(rec)
    window_id = str(join.get("window_id") or "")
    joined = {}
    if window_id:
        joined = _join_successor(root=root, seat=seat, window_id=window_id,
                                 poll_secs=REGISTRY_JOIN_POLL_S)
    if joined.get("found"):
        pid = joined.get("pid")
        session_id = joined.get("session_id")
        transcript = joined.get("transcript")
    else:
        pid = None
        session_id = None
        transcript = join.get("transcript") or ""
    # succ_ref ONLY from the seat row's OWN session_ref cell (a harness ref,
    # never a session id); an empty ref stays empty so the composed after_join
    # dm prints `<your ListAgents ref>`, exactly as _compose_after_join_dm
    # intends today.
    sref = (row or {}).get("session_ref") or ""
    values = _first_turn_values(
        root, seat=seat, gen=int(gen) if gen is not None else 0,
        succ_name=seat, succ_ref=str(sref),
        succ_transcript=str(transcript))
    # pid/from the live join (never the stale record), informational on the
    # values map for any startup template that reads them — unknown placeholders
    # stay refused by _resolve_startup_placeholders regardless.
    values["pid"] = pid
    values["session_id"] = session_id
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


# --- rotate.py prepare -- the CAPTIVE rotate-out checklist (goal:g15.14
#     STEP 2, hypothesis:l4-rotate-self-drives-the-handoff-and-prepares-the-\n#     spawn) ---------------------------------------------------------------
#
# `rotate.py prepare --seat S` prints the captive rotate-out checklist
# BEFORE any spawn — unpushed commits, dirty tree, behind the season branch,
# card mtime older than the last commit, a stale meter pin (seat_pin-stale),
# a stale <S>.ack.json — ONE line each with the ONE command that clears it.
# exit 0 only when nothing blocks, exit 3 otherwise. rotate-self runs the
# SAME checks and refuses BY NAME with the same line: one function,
# `_prepare_checks`, two callers — never a second implementation. `--force`
# bypasses only what it bypassed today (the meter-due gate); these checklist
# blockers are not that gate.


def _git_count_maybe(root: Path, *args: str) -> int | None:
    """`_git_maybe` as an integer count, or None when git cannot answer.

    A git 'rev-list --count' may return 0 on stdout even for an empty set;
    None means 'could not measure', which the checklist treats as ok rather
    than a blocker (the degrade-to-n/a discipline of the driven writer:
    a check blocks only when there is recorded evidence to block on)."""
    lines = _git_maybe(root, *args)
    if lines is None:
        return None
    try:
        return int(lines[0].strip())
    except (ValueError, IndexError):
        return None


#: porcelain paths the checklist never counts as the seat's dirt: written by
#: the comms layer and the rotation sequence as a side effect of every dm and
#: every rotation, committed by grid_sync (not by any seat).
PREPARE_CHURN_PREFIXES = (".agi/comms/",)
#: the rotation records + sequence.json: written by rotate-self / the loop
#: at every rotation, UNTRACKED until a sync commits them (Sensei 18:29Z:
#: five uncommitted records blocked a rotate-self with 0 modified files).
PREPARE_CHURN_DIRS = (".agi/sessions/rotations/",)


def _porcelain_path(porcelain_line: str) -> str:
    """The path a `git status --porcelain` line names — the two-column
    status prefix stripped, any `old -> new` rename reduced to the new path,
    surrounding quotes removed. One extractor; `_prepare_churn_path` and the
    dirty-tree captive both use it so a churn filter and a name always agree
    on what a line's path IS."""
    path = porcelain_line[3:] if len(porcelain_line) > 3 else ""
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip().strip('"')


def _prepare_churn_path(porcelain_line: str) -> bool:
    """True when a `git status --porcelain` line -- modified OR untracked --
    names cron-owned churn rather than a file the seat changed:
    `.agi/comms/**` (send.py writes a dm file per pair as dms flow) and
    `.agi/sessions/rotations/*.json` (the records + sequence.json). Untracked
    files elsewhere still count: a new test file never `git add`-ed is
    exactly the stranded work the captive exists to name. Renames
    (`R old -> new`) are judged on the new path."""
    path = _porcelain_path(porcelain_line)
    if path.startswith(PREPARE_CHURN_PREFIXES):
        return True
    return path.startswith(PREPARE_CHURN_DIRS) and path.endswith(".json")


def _prepare_dirty_paths(porcelain: list[str] | None,
                         root: Path, top: Path | None) -> list[str]:
    """The NON-churn dirty/untracked paths `git status --porcelain` reports
    (cron-owned churn excluded exactly as `_prepare_churn_path`), in porcelain
    order, EXCLUDING a path whose ONLY delta vs HEAD is trailing whitespace /
    a missing EOF newline (claim 2: a whitespace-only delta reads CLEAN, never
    a blocker). These are the seat's own stranded modifications a dirty-tree
    captive exists to name. A real one-cell change is an interior byte and
    still names a blocker (falsifier). `top` None (not a repo) -> every
    non-churn path stays dirty, exactly as before."""
    paths = []
    for ln in (porcelain or []):
        if ln.strip() and not _prepare_churn_path(ln):
            path = _porcelain_path(ln)
            if (top is not None and path
                    and _path_delta_whitespace_only(root, top, path)):
                # a whitespace-only delta is never the seat's dirt — skip it
                continue
            paths.append(path)
    return paths


def _merge_applies_clean(root: Path, sb: str) -> bool | None:
    """Whether merging `origin/<sb>` into the current branch APPLIES with zero
    conflicts, WITHOUT touching the tree (hypothesis:l4-prepare-performs-the-
    only-behind-merge...). Read-only `git merge-tree --write-tree` (git >=
    2.38): exit 0 prints the merged tree oid (clean), non-zero prints the
    conflict list. Returns True (clean), False (conflicts), or None when
    unmeasurable (no `origin/<sb>`, an opaque git refusal). A merge with any
    conflict must stay a BLOCK for the LLM to judge — the script PERFORMS
    only what is mechanical, i.e. applies with zero conflicts."""
    proc = _git_proc(root, "merge-tree", "--write-tree", "HEAD",
                     f"origin/{sb}")
    if proc is None:
        return None
    # rc 0 clean, rc != 0 -> conflicts (ref known to exist: behind>0 measured
    # it upstream of this call). treat opaque/non-zero as a conflict, conserve.
    return proc.returncode == 0


def _merge_conflict_paths(root: Path, sb: str) -> str:
    """Comma-joined conflicting paths from `git merge-tree --write-tree`, or
    `<unknown>` when the output names none. Printed in the BLOCK so the LLM
    sees WHICH files fight before it decides to merge by hand."""
    proc = _git_proc(root, "merge-tree", "--write-tree", "HEAD",
                     f"origin/{sb}")
    if proc is None:
        return "<unknown>"
    paths = []
    for ln in proc.stdout.splitlines():
        # 'CONFLICT (content): Merge conflict in <path>' — the human line
        ln = ln.strip()
        if ln.startswith("CONFLICT") and " in " in ln:
            paths.append(ln.rsplit(" in ", 1)[-1].strip() or ln)
    return ", ".join(paths) or "<unknown>"


def _perform_season_merge(root: Path, sb: str) -> str | None:
    """Perform the only-behind merge: `git merge --no-edit origin/<sb>`.
    Returns the resulting HEAD sha (short form), or None when the merge did
    NOT land (git returned non-zero, or an opaque refusal) — a merge git
    aborted must never be reported as merged. On any non-zero merge rc (a
    REFUSED merge or a CONFLICT) this ABORTS the merge (`git merge --abort`)
    so the tree is never left half-merged (P1-a: never a half-merge). The
    MERGE returncode is the one thing that gates the success line: a merge
    that ABORTS still leaves HEAD where it was, so reporting
    `merged <sha>` on it is a false ok that lets rotate-self proceed on a
    stale branch.

    **This measures and merges ONE ref**: the CALLER (`_prepare_checks`
    --perform block) fetches first and then runs the conflict-free gate
    (`_merge_applies_clean`) on the refreshed `origin/<sb>`; there is NO
    fetch here, because re-fetching could pull a NEWER ref than the one
    measured clean and turn a measured-clean merge into a different,
    conflicting one (the divergence P1-a closes). A failed fetch need not
    abort: `origin/<sb>` may already be current, and a merge against it
    either succeeds or the merge's own rc catches the problem. Callers reach
    this ONLY after the conflict-free gate (`_merge_applies_clean`) agreed
    there are zero conflicts and check 2 (dirty tree) passed."""
    proc = _git_proc(root, "merge", "--no-edit", f"origin/{sb}")
    if proc is None or proc.returncode != 0:
        # the merge REFUSED or CONFLICTED (non-zero rc — git leaves conflict
        # markers in the tree on a conflict). Undo any half-merge so the
        # working tree is never left mid-merge (P1-a). `git merge --abort`
        # with no merge in progress is a harmless no-op.
        _git_maybe(root, "merge", "--abort")
        return None                              # refused — never "merged <sha>"
    lines = _git_maybe(root, "rev-parse", "--short", "HEAD")
    if not lines:
        return None                              # cannot verify HEAD advanced
    return lines[0].strip() or None


def _git_proc(cwd: Path, *args: str):
    """Run git in `cwd`, return the CompletedProcess, or None on ANY failure
    (not a repo, an opaque refusal). `_git_maybe` already covers the stdout-
    lines reading; THIS is the returncode-bearing seam a conflict check and a
    merge need (the driven checklist must distinguish 'conflicts' from 'clean'
    by exit status, not by output parsing alone)."""
    try:
        return subprocess.run(["git", "-C", str(cwd), *args],
                              capture_output=True, text=True)
    except Exception:  # noqa: BLE001
        return None


def _proc_children(pid: int) -> int:
    """Number of live DESCENDANT processes of `pid`, by walking the
    `/proc/<pid>/task/<tid>/children` file recursively. Returns 0 when /proc
    is absent or the pid does not exist. NEVER `ps`, NEVER signals anything —
    this only COUNTS what the OS shows as living under the seat's pid
    (hypothesis:...-lists-the-seats-live-background-tasks, piece 2)."""
    if pid <= 0 or not os.path.isdir("/proc"):
        return 0
    total = 0
    seen = {pid}
    stack = [pid]
    while stack:
        cur = stack.pop()
        for tid in Path(f"/proc/{cur}/task").glob("*"):
            try:
                ch = (tid / "children").read_text(encoding="utf-8").split()
                for c in ch:
                    c = int(c)
                    if c not in seen:
                        seen.add(c)
                        total += 1
                        stack.append(c)
            except (OSError, ValueError):
                continue
    return total


def _background_tasks(root: Path, seat: str) -> str:
    """Measure the seat's live background tasks by whatever FILES exist, and
    print what is measurable by name — never a guess, never a kill:

      * the seat's own Monitor/background-Bash CHILDREN — counted by the
        /proc ppid chain from the config:seats row's `pid` when the row names
        one (`_proc_children`);

    goal:g15.14 P2-b — the `.claude/tasks` reader is GONE. It counted
    `Path(root)/.claude/tasks`: a path that NEVER exists under a worktree
    (the harness writes per-session task state to the GLOBAL
    `~/.claude/tasks/<uuid>/`, keyed by uuid, with no per-seat stable
    meaning). A reader that never reads is a lie in the listing, so it was
    deleted rather than re-pointed — no per-seat stable path exists to point
    it at, and re-pointing it at a global dir would fabricate a per-seat
    meaning that is not there.

    Returns a short spec naming what was counted, or `unmeasured` when no
    source measured anything. This line is a LISTING, never a blocker — it
    exists so the rotating seat can SEE what it must remember to leave behind,
    not to gate the spawn."""
    parts = []
    row = _find_seat(root, seat)
    pid = row.get("pid") if row else None
    if pid is not None:
        try:
            parts.append(f"{_proc_children(int(pid))} proc")
        except (TypeError, ValueError):
            pass
    return ", ".join(parts) if parts else "unmeasured"


def _prepare_merge_target(root: Path) -> str:
    """The merge target `_prepare_checks` measures-and-merges against.

    hypothesis:l4-branches-follow-the-season-grammar clause (5): a seat's
    current branch is a post/loop branch under the main it merges up into.
    Resolve through `branches.merge_target(<current branch>)` so a canonical
    town loop/post (`season2/<town>/season1/loops/...`) targets that town's
    main (`season2/<town>/season1/main`), not a literal core main -- the
    exact-string town lookup used nowhere here. A main, town-main, or
    unparseable branch keeps `season_branch(root)` (the season main) as the
    fallback, so this never changes season_branch's own callers.
    """
    # Read HEAD's name through `_git_maybe`, the prepare path's own idiom:
    # it answers None (never raises) when git is absent or faked, so a
    # fixture that forbids subprocesses in the self-reap path keeps the
    # season-main fallback (L4.307 director fix-up).
    lines = _git_maybe(root, "rev-parse", "--abbrev-ref", "HEAD") or []
    branch = lines[0].strip() if lines else ""
    if branch and branch != "HEAD":
        try:
            parsed = branches.parse(branch)
        except ValueError:
            parsed = None
        if parsed is not None and parsed["kind"] in ("post", "loop"):
            return branches.merge_target(branch)
    return season_branch(root)


def _prepare_checks(root: Path, seat: str, perform: bool = False,
                    stops_rotation: bool = False
                    ) -> list[tuple[bool, str, str]]:
    """The ordered captive rotate-out checklist for `seat`.

    `stops_rotation` marks a `rotate-self --stops/--stops-file` run. Only such
    a run exempts the seat's ack seats path (seats.md/posts.md) from check 4's
    "last WORK commit" scan: a --stops run's OWN card+seats commit must not
    re-age the card (goal:g15.25 line (3)). A plain `prepare`, or a
    `rotate-self --prepare` which delegates to it, must NOT carry the
    exclusion (SL7.30) — seating bookkeeping on a non-stops run is still WORK
    worth ageing the card against (SL7.12 had applied it unconditionally).

    Returns `(blocker, name, clear_cmd)` tuples. This is THE ONE
    implementation: `cmd_prepare` prints it, `cmd_rotate_self` refuses on it.
    A check whose basis cannot be measured (no git repo, no pin file, no
    ack) reports ok rather than guessing — a captive step names a blocker
    only when the evidence for the blocker is actually present.

    `perform=True` (the `prepare --perform` flag, or rotate-self's own gate
    which defaults ON) lets check 3 PERFORM the only-behind merge instead of
    prompting it, but ONLY when it is mechanical: check 2 (dirty tree) passed
    AND `_merge_applies_clean` reports zero conflicts. A conflicting merge
    stays a BLOCK naming the paths; an unperformed behind stays a BLOCK with
    the merge command."""
    checks: list[tuple[bool, str, str]] = []

    # 1 unpushed commits on the checked-out branch. When `@{u}` does not
    # resolve (a fresh seat branch with no upstream yet — exactly the
    # unpushed case), count `origin/<branch>..HEAD` if that ref exists, else
    # BLOCK `no upstream for <branch>` with the push command (a branch with
    # no upstream makes a bare `@{u}..HEAD` count None, which used to fall
    # through as (None or 0) > 0 = False and leave the unpushed captive
    # INERT). A detached HEAD and an unmeasurable branch both print ok.
    branch_lines = _git_maybe(root, "rev-parse", "--abbrev-ref", "HEAD")
    branch = (branch_lines[0].strip() if branch_lines else "")
    if not branch:
        unpushed, pname, pclear = (False, "unpushed commits (unmeasured)",
                                   "git push")
    elif branch == "HEAD":
        unpushed, pname, pclear = (False, "unpushed commits "
                                   "(detached: unmeasured)", "git push")
    else:
        n = _git_count_maybe(root, "rev-list", "--count", "@{u}..HEAD")
        if n is not None:
            unpushed, pname, pclear = (n > 0, "unpushed commits", "git push")
        else:
            alt = _git_count_maybe(root, "rev-list", "--count",
                                   f"origin/{branch}..HEAD")
            if alt is not None:
                unpushed, pname, pclear = \
                    (alt > 0, f"unpushed commits vs origin/{branch}",
                     "git push")
            else:
                unpushed, pname, pclear = \
                    (True, f"no upstream for {branch}",
                     f"git push -u origin {branch}")
    checks.append((unpushed, pname, pclear))

    # 2 dirty tree — NAMES the non-churn dirty/untracked paths (up to 5,
    # then `+N more`) so no caller reads a bare "dirty tree". The clear
    # command names YOUR OWN paths -- `git add -A` is forbidden in this tree
    # (parallel agents share it; it has swept a second agent's half-written
    # node and a human's uncommitted edits into one commit). Cron-owned
    # churn is not the seat's dirt (Sensei 18:26Z, measured on a
    # MAIN-checkout seat: the checklist blocked on `.agi/comms/season-2/dm/
    # *.md`, which send.py writes as dms flow -- the seat's own included --
    # and `.agi/sessions/rotations/sequence.json`; grid_sync commits both,
    # a worktree seat never sees them). Those paths are excluded by name.
    porcelain = _git_maybe(root, "status", "--porcelain")
    top = _git_toplevel(root)
    dirty_paths = _prepare_dirty_paths(porcelain, root, top)
    # claim 2 (one-serializer hypothesis): a dirty path whose ONLY delta vs
    # HEAD is trailing whitespace / a missing EOF newline reads CLEAN — named
    # on ONE benign (never-blocking, ok) line, never a dirty-tree blocker. A
    # real one-cell change is an interior byte and still names a BLOCK.
    ws_only: list[str] = []
    if top is not None:
        for ln in (porcelain or []):
            if not ln.strip() or _prepare_churn_path(ln):
                continue
            p = _porcelain_path(ln)
            if p and _path_delta_whitespace_only(root, top, p) \
                    and p not in ws_only:
                ws_only.append(p)
    if dirty_paths:
        shown: list[str] = []
        for p in dirty_paths:
            if len(shown) >= 5:
                break
            # claim 6a: an index-only real change (staged edit, working copy
            # restored to HEAD) is named 'staged change (index differs from
            # HEAD)' — the unrecorded staged edit a rotation must not proceed
            # over — rather than a bare path.
            if _index_staged_real_change(root, top, p):
                shown.append(f"{p}: staged change (index differs from HEAD)")
            else:
                shown.append(p)
        suffix = (f", +{len(dirty_paths) - 5} more"
                  if len(dirty_paths) > 5 else "")
        dirty_name = "dirty tree: " + ", ".join(shown) + suffix
    else:
        dirty_name = "dirty tree"
    checks.append((bool(dirty_paths), dirty_name,
                   "git commit -m '<msg>' -- <the files you changed>"))
    # claim 2 benign naming: each whitespace-only-delta path is named on ONE
    # never-blocking (ok) line so prepare both passes AND says why the path
    # was not a blocker. Name relative to the repo top so the familiar
    # `seats.md` / `posts.md` form appears.
    for p in ws_only:
        abs_p = os.path.abspath(os.path.join(str(root), p))
        rel_top = os.path.relpath(abs_p, str(top))
        checks.append((False, f"{rel_top}: whitespace-only delta, "
                              f"treated as clean", ""))

    # 3 behind origin/season/sX (N commits) -- branch from the ladder via
    # season_branch, never a hardcoded season. The merge target resolves
    # through branches.merge_target when the seat's branch is a post/loop
    # (clause 5 of hypothesis:l4-branches-follow-the-season-grammar), so a
    # town seat targets its own town main, not a literal core main.
    _sb = _prepare_merge_target(root)
    behind = _git_count_maybe(root, "rev-list", "--count",
                              f"HEAD..origin/{_sb}")
    # The clear command MERGES, never rebases: `never rebase` is a standing
    # rule of this tree (CLAUDE.md, every seat card) and the seat protocol's
    # behind check is `git merge origin/season/sX` into the worktree
    # (director fix-up at the SL1.02 harvest; the kid printed `pull --rebase`).
    behind_clear = (f"git fetch origin {_sb} && git merge --no-edit "
                    f"origin/{_sb}")
    if behind is None:
        # an unmeasurable behind (no origin ref to count against) stays ok and
        # says so plainly, never a fabricated number
        checks.append((False, f"behind origin/{_sb} (unmeasured)", behind_clear))
    elif perform and not dirty_paths and behind > 0:
        # `--perform` (rotate-self defaults ON): check 2 passed (tree clean)
        # and we are measurably behind. PERFORM the merge ONLY if it is
        # mechanical -- zero conflicts. A conflicting merge is exactly the
        # judgement-free-not case: stays a BLOCK naming the paths.
        # MEASURE AND MERGE THE SAME REF (P1-a): fetch FIRST so the local
        # `origin/<sb>` is fresh, then measure the conflict-free gate and
        # merge THAT SAME ref. Measuring against a stale local ref and then
        # merging the refreshed one was a DIFFERENT merge with no abort path.
        _git_maybe(root, "fetch", "origin", _sb)
        cf = _merge_applies_clean(root, _sb)
        if cf is True:
            merged = _perform_season_merge(root, _sb)
            if merged is None:
                # the mechanical merge was attempted and did NOT land (non-
                # zero rc — e.g. the accepted churn exclusion let an
                # untracked/modified churn file through check 2, and the
                # merge wants to overwrite it while git refuses, or the
                # merge CONFLICTED). `_perform_season_merge` ABORTS any
                # half-merge so the tree is never left mid-merge (P1-a).
                # Report a BLOCK, never a false ok: rotate-self must not
                # proceed on a stale branch. The clear command still names
                # the manual merge.
                checks.append((True,
                               f"behind origin/{_sb} ({behind}) — merge "
                               f"attempted, refused by git (aborted)",
                               behind_clear))
            else:
                checks.append((False,
                               f"behind origin/{_sb} ({behind}) — merged "
                               f"{merged}",
                               behind_clear))
        elif cf is False:
            checks.append((True,
                           f"behind origin/{_sb} ({behind}) — merge conflicts: "
                           f"{_merge_conflict_paths(root, _sb)}",
                           behind_clear))
        else:
            # cannot even measure whether the merge is conflict-free -> do NOT
            # auto-merge blind; block and let the LLM judge
            checks.append((True, f"behind origin/{_sb} ({behind})",
                           behind_clear))
    else:
        ahead_n = behind or 0
        # a dirty tree (or an explicit listing baseline) leaves check 3 a BLOCK
        checks.append((ahead_n > 0, f"behind origin/{_sb} ({ahead_n})",
                       behind_clear))

    # 4 card mtime older than the last commit
    # The card lives in the SEAT'S OWN tree (`<worktree>/.agi/sessions/quorum/
    # <seat>.md`, committed on the seat branch); `_sessions_dir` routes to the
    # shared MAIN checkout, whose copy only moves at merge-up — measured at
    # gen I's rotation: the live check read MAIN's stale copy and blocked a
    # clean rotate-self (director fix-up at the SL1.02 harvest).
    # `_own_card_path` is the ONE resolver both this check and the driven
    # handoff writer use (hypothesis:l4-the-driven-handoff-writer-keys-on-
    # declared-titles-and-writes-the-seats-own-card).
    card = _own_card_path(root, seat)
    # "Older than the last commit" means the last commit that is WORK: a
    # merge from the season branch (a sync) is not, a commit of cron-owned
    # churn (comms dms, rotation records) is not, and the commit that
    # committed the card itself is not (Sensei 18:29Z: two porcelain syncs
    # aged the card and blocked the rotation). Measured at the repo top so
    # engine edits under extensions/ count, not only the graph dir.
    top = _git_toplevel(root) or root
    try:
        card_rel = str(card.resolve().relative_to(Path(top).resolve()))
    except (ValueError, OSError):
        card_rel = None
    spec = ["log", "-1", "--no-merges", "--format=%ct", "--", ".",
            ":(exclude).agi/comms", ":(exclude).agi/sessions/rotations"]
    if card_rel:
        spec.append(f":(exclude){card_rel}")
    # a rotate-out stops commit touching seats.md must not re-age the card
    # (goal:g15.25 line (3)): seating/rotation bookkeeping is not WORK, the
    # same reasoning that excludes comms + rotation records — a pure
    # card+seats commit is fully invisible to this check, so the stops write
    # satisfies this captive instead of re-triggering it. SL7.30: this
    # exclusion is CONDITIONAL on the run being a --stops rotate-self. A
    # plain `prepare` (or rotate-self --prepare) must still let a seats.md
    # WORK commit age the card — SL7.12 over-applied it to every prepare.
    if stops_rotation:
        try:
            _sres = str(_ack_seats_path(root).resolve()
                        .relative_to(Path(top).resolve()))
            spec.append(f":(exclude){_sres}")
        except (ValueError, OSError):
            pass
    last_ts = _git_count_maybe(top, *spec)
    card_stale = (last_ts is not None and card.exists()
                  and card.stat().st_mtime < last_ts)
    checks.append((card_stale, "card older than last commit",
                   f"rotate.py handoff --driven --seat {seat}"))

    # 5 meter pin missing or stale (seat_pin-stale). The check needs the
    # seat's CURRENT generation — which now comes from the config:seats ROW
    # first (the authority), the handoff header only as fallback. When
    # NEITHER is measurable the line prints ok + a plain `generation
    # unmeasured` note, never silently passing with cur_gen=0 (the old code
    # gated on `cur_gen` TRUTHINESS, so a seat whose handoff copy carried no
    # generation got cur_gen=0 and both captives went INERT).
    pin = find_pin_log(root, seat)
    cur_gen, gen_measured, gen_src = _generation_measured(root, seat)
    gen_note = (f"cur={cur_gen} ({gen_src})" if gen_measured else
                "generation unmeasured: no config:seats row, no handoff")
    stale_pin = False
    # The clear line must print the ONE command that actually clears, both
    # halves right (hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-
    # pin-and-prepare-prints-the-clear-line-that-clears): --pin takes the
    # PIN FILE (the seat's real `<sessions>/<seat>.meter`, resolved via
    # _sessions_dir so the printed path and the write target agree), and
    # the transcript comes from the pin/registry when known else the literal
    # placeholder -- never --seat (which trips the cross-generation read
    # refusal).
    known_transcript = None
    pin_transcript = None
    if pin is not None:
        written_gen, written_path = _parse_pin_record(pin)
        if written_gen is not None and gen_measured and written_gen != cur_gen:
            stale_pin = True
        pin_transcript = written_path or None
    # goal:g15.14 P1-d — when check 5 BLOCKS (stale_pin) the pin is another
    # generation's BY DEFINITION, so preferring its written_path would name
    # the WRONG transcript the clear line must re-point the meter at. Prefer
    # the config:seats ROW's transcript first (resolved the way the meter
    # itself resolves it, via transcript_from_registry_dict), and fall back
    # to the pin's written_path ONLY when the row carries none.
    if root is not None:
        seat_row = _find_seat(root, seat)
        if seat_row:
            known_transcript = (seat_row.get("transcript_path")
                                or transcript_from_registry_dict(seat_row))
            known_transcript = known_transcript or None
    if known_transcript is None:
        known_transcript = pin_transcript
    clear5 = (f"rotate.py meter --pin {_seat_pin_path(root, seat)} "
              f"--session-log {known_transcript or '<transcript>'}")
    checks.append((stale_pin,
                   f"meter pin stale (seat_pin-stale) {gen_note}",
                   clear5))

    # 6 stale <seat>.ack.json — an ack from a generation other than the seat's
    # own is a leftover that would misreport the rotation (the ack channel is
    # generation-checked: hypothesis:l4-rotate-readback-false-negative-and-
    # the-orphan-by-design). Absence is fine — this is the pre-first-rotation
    # state. Same row-first generation, same unmeasured note as check 5.
    ack = _ack_path(root, seat)
    stale_ack = False
    if ack.exists():
        try:
            data = json.loads(ack.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            data = {}
        ga = data.get("gen_after")
        if ga is not None and gen_measured and ga != cur_gen:
            stale_ack = True
    checks.append((stale_ack, f"stale ack ({seat}.ack.json) {gen_note}",
                   f"rm {ack}"))

    return checks


def cmd_prepare(args: argparse.Namespace, root: Path) -> int:
    """`rotate.py prepare --seat S`: print the captive rotate-out checklist.

    One line per checked condition, the blocking ones each carrying the ONE
    command that clears them. exit 0 only when nothing blocks; exit 3 when
    any check names a blocker. `cmd_rotate_self` runs the SAME function to
    refuse BY NAME before it spawns."""
    seat = getattr(args, "seat", None) or ""
    perform = getattr(args, "perform", False)
    # goal:g15.14 P1-b — the branch guard runs FIRST, before `_prepare_checks`
    # and ANY merge. `prepare --perform` merges the only-behind season branch
    # into the checked-out branch; on master (with season/* branches present)
    # that would MERGE season INTO master, which the seasons-as-branches
    # mapping forbids. Refuse BY NAME before any side effect. rotate-self's
    # own prepare path delegates to THIS function, so one guard here gates
    # both callers. (Falsifier: a `--prepare --perform` on a fixture master
    # branch must refuse with the guard text BEFORE the merge lands.)
    guard = _check_branch_guard(root)
    if guard:
        print(guard, file=sys.stderr)
        return 1
    checks = _prepare_checks(root, seat, perform=perform)
    blocks = [c for c in checks if c[0]]
    for blocker, name, clear in checks:
        print(f"[{'BLOCK' if blocker else 'ok'}] {name}")
        if blocker:
            print(f"       clear: {clear}")
    # the LISTING line, never a blocker: the seat's live background tasks as
    # far as files show them (hypothesis:...-lists-the-seats-live-background-
    # tasks) -- so the rotating seat SEES what it must remember to leave
    # behind, before it spawns.
    print(f"background tasks: {_background_tasks(root, seat)}")
    if blocks:
        print(f"prepare: {len(blocks)} check(s) block the spawn; fix each "
              f"BLOCK line or re-run after clearing.", file=sys.stderr)
        return 3
    print("prepare: no blockers — safe to rotate.", file=sys.stderr)
    return 0


# --- geometry freshness (rotate-self must not spawn on a stale config) -----
# hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-
# one, mechanism 3: config:rotations + config:seats (the rotation template
# and the seat registry) live in `.agi/nodes/.geometry/` and are the PRIME's
# shared source of truth. A rotating WORKTREE carries its own copy of that
# subtree; if the worktree's branch is BEHIND the shared geometry branch, its
# copy is stale and spawning a successor on it would bake the wrong template
# / seat registry into the successor SILENTLY. So rotate-self resolves WHICH
# tree's geometry it reads, once, up front: the integration tree
# (`locations.git_common_root`) when the worktree's own is behind AND the
# integration tree's is itself current; otherwise it refuses BY NAME with the
# behind-count and the sync command. The rotation record names the tree the
# template came from (`template_source`) so a spawn is always attributable.

#: the subtree of the repo whose drift makes a worktree's rotation config
#: stale. Kept a Path so git's `--` pathspec gets fresh bytes on every OS.
GEOMETRY_SUBTREE = Path(".agi/nodes/.geometry/")


def _geometry_base_ref(root: Path | None) -> str:
    """The shared geometry branch (`origin/<season branch>`) — DERIVED from
    the ladder at call time via season_branch, never a hardcoded season."""
    return f"origin/{season_branch(root)}"


def _geometry_sync_cmd(root: Path | None) -> str:
    """What a refused operator runs to refresh the geometry config before
    re-spawn. MERGE, never rebase: a standing rule of this tree (CLAUDE.md,
    every seat card); the same clear line `_prepare_checks` prints for
    "behind" (director fix-up at the SL1.06 harvest -- the kid printed
    `rebase`). Season from the ladder, never a hardcoded season."""
    b = season_branch(root)
    return (f"git fetch origin {b} && git merge --no-edit origin/{b}")


def _git_toplevel(root: Path) -> Path | None:
    """The git work-tree top for `root` (walked up when `root` is a subdir),
    or None when `root` is not inside a git repo. `root` here is the graph
    dir (`.agi/`, as `find_project_root` returns), so the repo top is usually
    its parent. Never raises."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return None
    if out.returncode != 0:
        return None
    try:
        return Path(out.stdout.strip())
    except ValueError:
        return None


def _geometry_behind_count(root: Path | None) -> int:
    """How many commits the worktree's OWN `.agi/nodes/.geometry/` is behind
    the shared geometry branch:

        git rev-list --count HEAD..<ref> -- <GEOMETRY_SUBTREE>

    0 (current) when the geometry is already at HEAD, when the remote-
    tracking base ref does not exist (a fresh/offline clone), or when the
    check cannot answer (no git at all). Never raises — a gitless test
    fixture must pass through as current, not refuse."""
    if root is None:
        return 0
    top = _git_toplevel(root)
    if top is None:
        return 0
    base = _geometry_base_ref(root)
    try:
        out = subprocess.run(
            ["git", "rev-list", "--count",
             f"HEAD..{base}", "--", str(GEOMETRY_SUBTREE)],
            cwd=str(top), capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return 0
    if out.returncode != 0:
        return 0
    try:
        return max(0, int(out.stdout.strip() or "0"))
    except ValueError:
        return 0


def _geometry_resolution_root(root: Path) -> tuple[Path | None, str]:
    """Which tree's `.agi/nodes/.geometry/` a rotate-self should read.

    The worktree's OWN geometry is the default source. When it is behind the
    shared geometry branch, spawning on it would hand the successor a stale
    config:rotations / config:seats SILENTLY — mechanism 3's falsifier. Then
    serve the config from the integration tree (`locations.git_common_root`,
    the main checkout) when THAT tree's geometry is itself current and it
    carries the rotations node; otherwise refuse BY NAME with the behind-count
    and the sync command.

    Returns (resolution_root | None, source_note). A None root means refuse:
    `source_note` is the full error string the caller prints and returns 1 on.
    """
    behind = _geometry_behind_count(root)
    if behind == 0:
        return root, "worktree (geometry current)"
    main = locations.git_common_root(root)
    main_graph = (Path(main) / ".agi") if main else None
    if main_graph is not None and str(main_graph) != str(root) \
            and _geometry_behind_count(main_graph) == 0 \
            and _rotations_node_path(main_graph).exists():
        _gb = _geometry_base_ref(root)
        return main_graph, (
            f"integration tree {main} (worktree geometry behind "
            f"{_gb} by {behind} commit(s))")
    _gb = _geometry_base_ref(root)
    return None, (
        "rotate-self refused: this worktree's .agi/nodes/.geometry/ is behind "
        f"{_gb} by {behind} commit(s); spawning on a stale "
        "rotation config would hand the successor the wrong config:rotations "
        "/ config:seats. Sync the tree and re-run: "
        f"`{_geometry_sync_cmd(root)}`.")


# --- first-decision: the point's captive harvest-or-cut --------------------
# hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps, step 4.
# `harvest-table` (L4.236/245) is NOT in this tree (grep confirms no
# harvest-table subcommand on the cut this branch was made from), so the
# pre-filled harvest row + the ONE bounded prompt per round live here as
# `first-decision`, per the brief's "implement directly, never duplicate".
#
# The script PRINTS and NEVER ANSWERS the harvest-or-cut decision: for each
# OPEN round of the seat's worktree it prints the pre-filled row (branch,
# parent, kids, verdicts, merge-base, behind) and then exactly ONE bounded
# prompt — `harvest <round> | cut <next queued node> | hold`. `--answers FILE`
# replays the LLM's choices into the NAMED next command per row — the git
# merge line carrying the EXACT branch name from `git branch --list` for a
# harvest, the dispatch line for a cut — printed, never run. FALSIFIER: a
# code path that RUNS the merge or the dispatch itself is refused; there is
# none. The decision stays the LLM's; the script only pre-fills and prints.


def _fd_git(cwd: Path, *args: str) -> tuple[int, str, str]:
    """Run git from `cwd`; return (rc, stdout, stderr). Never raises. A
    non-zero rc is a MEANINGFUL answer (`merge-base --is-ancestor` rc=1 says
    "not an ancestor", the open-round test), so the caller owns the rc."""
    try:
        r = subprocess.run(["git", "-C", str(cwd), *args],
                           capture_output=True, text=True, timeout=10)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except OSError:
        return 127, "", f"cannot run git from {cwd}"


def _fd_seat_branch(root: Path, main: Path, seat: str) -> str | None:
    """The branch a seat works on, resolved in strict order:

      1. the checked-out HEAD of the seat's worktree, from the config:seats
         `worktree` field (resolved against the MAIN checkout, so a relative
         `.agi/worktrees/seat-<S>` resolves like the live rows),
      2. a local `post/<seat>@s<s>` / `season<n>/posts/<seat>` branch (with
         the deprecated `seat/<seat>@s<s>` alias as a fallback),
      3. None.

    A worktree seat works on its own checked-out branch; the seat's open
    rounds are the `loop/*` branches cut from it (F5, config:rotations).
    """
    row = _find_seat(root, seat)
    wt = (row or {}).get("worktree") or ""
    if wt:
        p = Path(wt)
        cand = p if p.is_absolute() else (main / wt)
        if cand.is_dir():
            rc, br, _ = _fd_git(cand, "rev-parse", "--abbrev-ref", "HEAD")
            if rc == 0 and br and br != "HEAD":
                return br
    # Convention fallback, resolved in rename order (hypothesis:l4-a-seat-is-
    # a-post-everywhere): post/<seat>@s* first, then the canonical
    # season<n>/posts/<seat>, then the deprecated seat/<seat>@s* alias. Return
    # the ACTUAL spelling git reports.
    for pat in (f"post/{seat}@s*", f"season*/posts/{seat}",
                f"seat/{seat}@s*"):
        rc, out, _ = _fd_git(main, "branch", "--list", pat)
        if rc == 0:
            for line in out.splitlines():
                # `git branch --list` prefixes `*` for the current branch and
                # `+` for a branch checked out in a linked worktree; strip all.
                name = line.strip().lstrip("*+").strip()
                if name:
                    return name
    return None


def _fd_frontmatter(text: str) -> str:
    """The frontmatter block of a node's text, between the first two `---`
    lines, or '' when absent (keep the kid node body out of the regex)."""
    if not text.startswith("---"):
        return ""
    rest = text.split("\n", 1)[1] if "\n" in text else ""
    fm, _, _ = rest.partition("\n---")
    return fm


def _fd_node_kids(main: Path, branch: str, merge_base: str,
                  nodes_rel: str = ".agi/nodes/experiment") -> list[tuple[str, str]]:
    """(kid_node_id, verdict) for every experiment `.md` file ADDED on the
    round branch relative to its merge-base with the seat branch (F5: "its
    kid experiment nodes are under .agi/nodes/experiment/ on that branch").
    The node id is `experiment:` + the file stem; the verdict is the node's
    `verdict:` frontmatter field, or "" when the node carries none.

    `git branch --list` + `git diff --name-only` are the ONLY reads; nothing
    is written, checked out or merged."""
    rc, out, _ = _fd_git(main, "diff", "--name-only", merge_base, branch,
                         "--", nodes_rel)
    if rc != 0:
        return []
    kids = []
    for path in out.splitlines():
        if not path.endswith(".md") or not path.startswith(nodes_rel + "/"):
            continue
        stem = path.rsplit("/", 1)[-1][:-3]
        rc2, blob, _ = _fd_git(main, "show", f"{branch}:{path}")
        verdict = ""
        if rc2 == 0:
            fm = _fd_frontmatter(blob)
            for line in fm.splitlines():
                if line.startswith("verdict:") and ":" in line:
                    verdict = line.split(":", 1)[1].strip()
                    break
        kids.append((f"experiment:{stem}", verdict))
    return kids


def _fd_seat_worktree(root: Path, main: Path, seat: str) -> Path | None:
    """The seat's OWN worktree directory, resolved in strict order:

      1. the config:seats `worktree` field (resolved against the MAIN
         checkout, so a relative `.agi/worktrees/seat-<S>` / `post-<S>`
         resolves like the live rows) when it is a directory,
      2. the convention `.agi/worktrees/post-<S>` (else the deprecated
         `seat-<S>`) under the main checkout,
      3. None.

    Mirrors how `_fd_seat_branch` resolves the worktree; the seat's dispatch
    wrote ITS iteration manifests inside this worktree, so this is where the
    owned-agent evidence lives."""
    row = _find_seat(root, seat)
    wt = (row or {}).get("worktree") or ""
    if wt:
        p = Path(wt)
        cand = p if p.is_absolute() else (main / wt)
        if cand.is_dir():
            return cand
    # Convention fallback (hypothesis:l4-a-seat-is-a-post-everywhere): a
    # post-renamed seat lives at `.agi/worktrees/post-<seat>`; accept that
    # beside the deprecated `seat-<seat>` name, preferring post-.
    post = main / ".agi" / "worktrees" / f"post-{seat}"
    if post.is_dir():
        return post
    conv = main / ".agi" / "worktrees" / f"seat-{seat}"
    return conv if conv.is_dir() else None


def _fd_seat_agent_ids(root: Path, main: Path, seat: str) -> set[str]:
    """The set of agent ids the seat ITSELF dispatched, parsed from the seat
    worktree's own iteration manifests — `<wt>/.agi/sessions/iter-*/manifest
    .json` `agents[].id`. The seat's dispatch READ-BEFORE-WRITE wrote these
    when it cut each round, so they are EVIDENCE of which rounds are this
    seat's (the manifest-join discriminator, (b)), not a convention guess.
    An unreadable / absent manifest or a missing worktree yields an empty
    set — an under-count (no round credited), never a mis-attribution."""
    wt = _fd_seat_worktree(root, main, seat)
    if wt is None:
        return set()
    sess = wt / ".agi" / "sessions"
    if not sess.is_dir():
        return set()
    ids: set[str] = set()
    for manifest in sorted(sess.glob("iter-*/manifest.json")):
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for agent in data.get("agents") or []:
            if isinstance(agent, dict) and agent.get("id"):
                ids.add(str(agent["id"]))
    return ids


def _fd_agent_from_branch(branch: str) -> str:
    """The agent id embedded in a round branch name, in EITHER spelling of
    the dispatch convention (F5): canonical
    `season<n>/loops/<slug>-a00-XXXX`, or legacy `loop/<slug>-a00-XXXX@s<N>`
    — the trailing `a00-<hex>` run. Returns '' when the branch carries none,
    so a manually-cut branch is unresolvable and never credited."""
    seg = re.sub(r"@s\d+$", "", branch).rsplit("/", 1)[-1]
    m = re.search(r"(a00-[0-9a-zA-Z]+)$", seg)
    return m.group(1) if m else ""


def _branch_loop(short: str) -> tuple[bool, int | None]:
    """(is_round, season) for a branch short name, classified through
    branches.parse — the ONE branch-name grammar. A round is a branch whose
    kind is loop in EITHER spelling: canonical
    `season<n>/loops/<slug>-<agent>` (kind == "loop"), or the deprecated
    `loop/<slug>-<agent>@s<n>` (which parse returns as an "alias" whose
    canonical is the loop). Any other kind (main, post, town, alias to a
    non-loop) yields (False, None); an unparseable foreign branch is
    skipped, never refused."""
    try:
        parsed = branches.parse(short)
    except ValueError:
        return False, None
    if parsed["kind"] == "loop":
        return True, parsed["season"]
    if parsed["kind"] == "alias":
        try:
            canon = branches.parse(parsed["canonical"])
        except ValueError:
            return False, None
        if canon["kind"] == "loop":
            return True, canon["season"]
    return False, None


def _fd_rounds(root: Path, main: Path, seat: str, seat_branch: str) -> list[dict]:
    """The seat's OWN OPEN round branches, one dict per round.

    A round is a local `loop/<slug>-<agent>@s<N>` branch (the dispatch
    convention, F5) in the SAME season as the seat branch, that is NOT yet an
    ancestor of the seat branch — i.e. it still carries commits the seat has
    not merged (an open, un-harvested round). A round already merged in
    (--no-ff makes its tip an ancestor of the seat branch) is closed and
    skipped.

    The glob alone is NOT enough: `loop/*@s<N>` crosses every district, so a
    sibseat / parent round forking at the shared season base would be swept
    in. OWNERSHIP is decided by EVIDENCE, discriminator (b) — the manifest
    join, NOT ancestry (discriminator (a)): dispatch.py writes each spawned
    agent's id into the seat worktree's own iteration manifests
    (`<wt>/.agi/sessions/iter-*/manifest.json` `agents[].id`), so a round
    `loop/<slug>-a00-XXXXXXXX@s<N>` belongs to THIS seat iff its agent id
    appears in one of those manifests. A parent/sibseat round's agent id
    lives in ITS OWN seat's manifests, never this one's, so it is dropped
    outright — never shown with a parent copied from the seat's HEAD (a lie
    is worse than a gap). The seat worktree is resolved from config:seats
    `worktree`, falling back to `.agi/worktrees/seat-<S>`, exactly as
    `_fd_seat_branch` does for the branch. A round whose agent id is not in
    the owned set is dropped; one that cannot be resolved at all (no
    `a00-<hex>` run) is unresolvable and would print `parent: ?` were it
    surfaced — never a copied constant.

    Measured caveat (discriminator (a)'s), now moot: ancestry dropped a
    round the moment the seat ADVANCED past its fork point. The manifest
    join does not — the seat's own dispatch record is stable regardless of
    later merges.

    Every branch name comes from `git branch --list`, so the exact name
    printed is exactly what the merge line harvests with."""
    m = re.search(r"@s(\d+)$", seat_branch)
    season = m.group(1) if m else "2"
    # Enumerate local refs ONCE and classify in Python through
    # branches.parse (the ONE branch-name grammar) — NOT a second `loop/`
    # `@s<N>` glob. A round is any branch whose kind is loop (canonical
    # `season<n>/loops/<slug>-<agent>` OR the deprecated
    # `loop/<slug>-<agent>@s<n>`) in THE SEAT's season. The eager
    # `loop/*@s{season}` glob only ever matched the legacy spelling, so a
    # round cut on the canonical grammar was invisible to first-decision.
    rc, out, _ = _fd_git(main, "for-each-ref", "--format=%(refname:short)",
                         "refs/heads")
    if rc != 0:
        return []
    own_ids = _fd_seat_agent_ids(root, main, seat)
    rounds = []
    for line in out.splitlines():
        branch = line.strip()
        if not branch:
            continue
        is_loop, bseason = _branch_loop(branch)
        if not is_loop or bseason is None or bseason != int(season):
            continue
        rc_a, _, _ = _fd_git(main, "merge-base", "--is-ancestor",
                             branch, seat_branch)
        if rc_a == 0:
            continue  # already merged into the seat: closed, not open
        # discriminator (b) — the manifest join: the round is THIS seat's
        # only if its agent id (parsed from the branch name) appears in the
        # seat's own iteration manifests. No manifest hit => not this seat's
        # round — dropped, never mis-credited with the seat's parent.
        agent = _fd_agent_from_branch(branch)
        if not agent or agent not in own_ids:
            continue  # not this seat's round — never misattribute
        rc_mb, mb, _ = _fd_git(main, "merge-base", seat_branch, branch)
        merge_base = mb.split("\n", 1)[0] if rc_mb == 0 and mb else ""
        rc_be, behind, _ = _fd_git(main, "rev-list", "--count",
                                   f"{branch}..{seat_branch}")
        behind_n = int(behind) if rc_be == 0 and behind.isdigit() else -1
        kids = _fd_node_kids(main, branch, merge_base) if merge_base else []
        rounds.append({
            # `parent` is the seat branch ONLY for a manifest-verified OWN
            # round (the branch the seat dispatched it from) — never a
            # constant copied from the seat's HEAD.
            "branch": branch,
            "parent": seat_branch,
            "merge_base": merge_base[:12] if merge_base else "?",
            "behind": behind_n,
            "kids": kids,
        })
    return rounds


def _fd_short(ref: str) -> str:
    s = str(ref).strip()
    return s[:12] if len(s) > 12 else s


def _fd_print_table(rows: list[dict]) -> None:
    """Print the pre-filled harvest rows + the ONE bounded prompt per row.
    The script never chooses; the LLM reads the prompt and writes --answers."""
    if not rows:
        print("first-decision: no open rounds for this seat")
        return
    for r in rows:
        print(f"round: {r['branch']}")
        print(f"  parent: {r['parent']}")
        print(f"  merge-base: {r['merge_base']}  behind: {r['behind']}")
        if r["kids"]:
            kids = ", ".join(
                f"{kid}{(' (' + ver + ')') if ver else ''}"
                for kid, ver in r["kids"])
            print(f"  kids: {kids}")
        else:
            print("  kids: (none)")
        print(f"  prompt: harvest {r['branch']} | cut <next queued node> | hold")


def _fd_next_commands(main: Path, rows: list[dict], answers: list[str]) -> None:
    """Replay the LLM's choices into the named next command per row.

    `answers` is one choice per open round, in the same order the table
    printed them: `harvest <branch>` -> the git merge line carrying the EXACT
    branch (the round-trip proof that the branch came from `git branch
    --list`), `cut <node-id>` -> the dispatch line for that node, `hold` ->
    nothing. Every line is PRINTED, never run — the falsifier: a step that
    runs the merge or the dispatch is refused, and there is no code path
    that could."""
    for r, ans in zip(rows, answers):
        tokens = ans.split()
        verb = tokens[0] if tokens else ""
        label = " ".join(tokens[1:]) if len(tokens) > 1 else ""
        if verb == "harvest":
            branch = label or r["branch"]
            print(f"# harvest {r['branch']}")
            print(f"git merge --no-ff {branch}")
        elif verb == "cut":
            node = label
            print(f"# cut {node} (from round {r['branch']})")
            print(f"python3 extensions/agi/bin/dispatch.py {main} <iter> "
                  f"--target {node} --level small --branch")
        else:  # hold / empty
            print(f"# hold {r['branch']}")


def cmd_first_decision(args: argparse.Namespace, root: Path | None) -> int:
    """`rotate.py first-decision --seat S [--answers FILE]` — the POINT's
    captive harvest-or-cut (hypothesis:l4-the-window-reply-and-harvest-or-
    cut-are-captive-steps, step 4). Pre-fills the harvest row for every OPEN
    round of the seat's worktree, prints ONE bounded prompt per row, and —
    with --answers — prints the named next command per chosen row. PRINT
    ONLY: merges and dispatches are never run."""
    if root is None:
        print("ERR: first-decision needs an agi project root.",
              file=sys.stderr)
        return 1
    if getattr(args, "root", None):
        root = Path(args.root).resolve()
    seat = args.seat
    main = locations.git_common_root(root)
    seat_branch = _fd_seat_branch(root, main, seat)
    if not seat_branch:
        print(f"ERR: no worktree branch or post/{seat}@s* (alias "
              f"seat/{seat}@s*) branch resolves for seat {seat!r}.",
              file=sys.stderr)
        return 1
    rows = _fd_rounds(root, main, seat, seat_branch)
    _fd_print_table(rows)
    answers = getattr(args, "answers", None)
    if answers:
        p = Path(answers).expanduser().resolve()
        if not p.exists():
            print(f"ERR: --answers file not found: {p}", file=sys.stderr)
            return 1
        lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
        print("# next commands (printed, never run):")
        _fd_next_commands(main, rows, lines)
    return 0


def _rotate_key_gate(root: Path, seat: str, row: dict | None) -> str | None:
    """rotate-self is KEY-GATED (hypothesis:l4-rotate-self-is-key-gated...
    piece 1). A KEYED seat -- its row already names a ``pubkey`` -- must hold
    its own signing key file before it rotates: a rotation whose successor
    wakes without the key cannot sign its own first message. Returns an error
    line (the ``keygen`` recovery) when the gate holds, None when it passes.

    The ONE exception is a seat whose row carries NO pubkey yet -- an
    incrementally-keyed seat mints its own first key in the same step (that
    minting half is out of this slice's scope; the gate only *refuses*). A
    throwaway seat (``row`` is an empty dict / None) is never keyed and never
    refused here.
    """
    if not row or not row.get("pubkey"):
        return None
    import send  # local: same dir, no import cycle (send.py pattern)
    key_path = send._seat_key_path(root, seat)
    if key_path.exists():
        return None
    return (f"rotate-self refused: seat {seat!r} carries a pubkey but no "
            f"signing key at {key_path} -- run `send.py keygen {seat}` "
            f"first (rotate-self is key-gated: a keyed seat must hold its "
            f"own signing key to rotate).")


def _rotate_first_key(root: Path, cfg_root, seat: str, row: dict | None,
                      dry_run: bool = False) -> str:
    """rotate-self KEY-GATING, line (1) MINTING half (hypothesis
    l4-rotate-self-is-key-gated...): the ONE gate exception -- a REAL row
    whose cell carries NO pubkey yet (an incrementally-keyed fleet seat)
    mints its own FIRST key IN THE SAME rotate-self step, so its successor
    wakes with a signing key it can use (Prime 21:20Z (b)).

    REUSES ``send._mint_seat_key`` -- the one key writer, no second path, no
    ed25519 literal -- and then CLOSES the line-(1) loop by writing the
    ``pubkey`` / ``sig_scheme`` / ``enc_scheme`` cells into the seat's OWN row
    through ``send._row_write_submit`` (best-effort, exactly like ``keygen``:
    a refused / unadmitted row write NEVER fails the rotation -- the key file
    is still minted, and the note says which half landed). A row that is
    already keyed, a THROWAWAY/rehearsal row (never written to seats.md), and
    the case where the key already exists (idempotent re-rotate) are all left
    alone -- returns '' then. Returns a one-line note when it mints.

    ``--dry-run`` (ORDER 1, SL5.05): touches nothing -- no key file, no row
    write. It still REPORTS what it would do (a one-line ``(dry-run)`` note
    naming the mint it would perform) so a caller on an unkeyed real row sees
    the refusal/mint plan without a side effect.
    """
    if not row or row.get("pubkey"):
        return ""
    import send  # local: same dir, no import cycle (send.py pattern)
    scheme = row.get("sig_scheme") or send.seatsig.DEFAULT_SCHEME
    if dry_run:
        # dry-run is a planning check: report what an unkeyed real row would
        # do, but mint NOTHING and write NO row cell. Already-keyed rows
        # (above) and idempotent re-rotates (key file already exists, so the
        # live path would mint nothing) both return '' -- nothing to report.
        if send._seat_key_path(root, seat).exists():
            return ""
        return (f"(dry-run) seat {seat!r} is unkeyed; would mint its first "
                f"key at {send._seat_key_path(root, seat)} (0600) and write "
                f"its pubkey cells -- NOTHING done")
    minted = send._mint_seat_key(root, seat, scheme)
    if minted is None:
        # a key file already exists though the row is unkeyed -- idempotent
        # re-rotate; leave it, the next rotation sees the row still unkeyed
        # and re-passing the gate. Nothing to do here.
        return ""
    _path, pub = minted
    note = (f"rotating seat {seat!r} was unkeyed; minted its first key at "
            f"{_path} (incremental fleet keying) -- "
            f"{send.seatsig.fingerprint(pub)}")
    _row_keyed = False
    try:
        # The three identity cells (pubkey / sig_scheme / enc_scheme) ride
        # the ONE identity writer (_write_identity_cells) into MAIN's
        # seats.md (resolved via _shared_graph_root), NEVER
        # send._row_write_submit on the caller's graph -- a worktree post's
        # first mint would otherwise write its OWN worktree copy, a second
        # writer of the seat's own row (hypothesis:l4-the-spawn-row-write-
        # and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-
        # own-row clause (1), Prime XIII ask (a)). Best-effort, exactly as
        # before: a refused / unadmitted row write never fails the rotation
        # (the key file is still minted; the note says which half landed).
        import write as _w  # local: same dir (send.py pattern, no cycle)
        _cur = next((r for r in _w._load_seats(_shared_graph_root(root))
                     if r.get("name") == seat), {})
        if _write_identity_cells(
                root, seat=seat, actor=seat,
                role=str(row.get("role") or ""),
                cells={"pubkey": pub.hex(),
                       "sig_scheme": _cur.get("sig_scheme") or scheme,
                       "enc_scheme": _cur.get("enc_scheme") or "none"}):
            note += f"; row {seat!r} keyed"
            _row_keyed = True
    except Exception as exc:  # noqa: BLE001
        note += f"; row write not admitted ({exc})"
    # clause (2): a KEY-CELL write commits its own-row hunk through the ONE
    # spawn-row commit helper and PUSHES the season branch -- best-effort,
    # a refused commit or push never fails the rotation (the key file is
    # already minted). The identity cells ride from the row the mint reads.
    if _row_keyed:
        try:
            _cn = _commit_spawn_row(
                root, seat=seat,
                generation=int(row.get("generation") or 0),
                session_id=str(row.get("session_id") or ""),
                window=str(row.get("window") or ""),
                pid=int(row.get("pid") or 0))
            note += f"; {_cn.splitlines()[0]}"
        except Exception as exc:  # noqa: BLE001
            note += f"; key row commit not performed ({exc})"
    return note


def _rotate_successor_key(root: Path, seat: str, row: dict | None, *,
                          gen_before: int, gen_after: int,
                          dry_run: bool = False) -> dict | None:
    """goal:g15.25 line (2) SUCCESSOR KEY half (hypothesis l4-rotate-self-
    is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-
    history, pieces (2)-(4)): a KEYED seat (its row names a ``pubkey``)
    mints its successor keypair at rotation handover, RETIRES its own
    (predecessor) key into the row's ``key_history`` -- NEVER deleted --
    signing the retirement with the PREDECESSOR key BEFORE the handover, and
    hands the successor the new private key at ``<sessions>/seats/<seat>.key``
    (0600, atomic replace) with the successor ``pubkey`` written into the
    seat's OWN row.

    Returns a dict the caller rides onto the ONE existing spawn-row write
    (s6.1 ``_successor_row_write`` / its ONE ``_commit_spawn_row`` commit --
    never a second commit): ``{successor_pub, scheme, retired, note,
    pending_key}``. None when there is nothing to retire -- an unkeyed row,
    a THROWAWAY/empty row, or a keyed row with no key file (the gate
    refused that earlier).

    SL5.05 handover-order fix: the function mints + signs EARLY (while the
    PREDECESSOR private key is still on disk) but does NOT flip ``<seat>.key``
    itself -- it returns the successor private key in ``pending_key`` and the
    actual `os.replace` is DEFERRED (by `_apply_successor_key_gated`) until
    after the successor spawn-row write and its ONE commit have SUCCEEDED.
    A failed spawn / row write / commit therefore leaves the predecessor key
    file BYTE-IDENTICAL, never a successor key out of step with the row that
    names it.

    Reuses the seatsig registry and send's key-file shape/mode -- no
    ed25519 literal, no second key-writer. ``send._mint_seat_key`` is NOT
    usable here on purpose: it REFUSES when ``<seat>.key`` already exists
    (the protection that makes a retirement a REPLACE, not a mint), so the
    successor key is generated through the SAME ``seatsig.get(scheme)`` the
    one writer uses and the file is atomically replaced in the same shape.

    ``--dry-run`` mints nothing, replaces nothing, writes nothing: it
    returns a ``{dry_run: True, note}`` dict that names the retirement it
    would perform.
    """
    if not row or not row.get("pubkey"):
        return None
    import send  # local: same dir (send.py pattern, no import cycle)
    scheme_name = str(row.get("sig_scheme") or send.seatsig.DEFAULT_SCHEME)
    scheme = send.seatsig.get(scheme_name)  # KeyError names an unknown scheme
    key_path = send._seat_key_path(root, seat)
    if not key_path.is_file():
        return None
    if dry_run:
        _fp = send.seatsig.fingerprint(
            bytes.fromhex(str(row.get("pubkey"))))
        return {
            "dry_run": True,
            "scheme": scheme_name,
            "note": (f"(dry-run) seat {seat!r} is keyed; would mint its "
                     f"successor key at {key_path} (0600, atomic replace), "
                     f"retire {_fp} (gen {gen_before}->{gen_after}) into "
                     f"key_history and write the successor pubkey -- "
                     f"NOTHING done"),
        }
    # (a) read the PREDECESSOR private key (to sign the retirement) BEFORE
    #     the atomic replace destroys the file on disk.
    try:
        _obj = json.loads(key_path.read_text())
        _pred_priv = bytes.fromhex(str(_obj.get("priv_hex") or ""))
        _pred_pub = scheme.public_from_secret(_pred_priv)
    except (ValueError, OSError, TypeError):
        return None
    # (b) mint the SUCCESSOR keypair through the SAME registry.
    _succ_priv, _succ_pub = scheme.keygen()
    # (c) sign the retirement record with the PREDECESSOR key BEFORE the
    #     handover; the retired pub must verify this signature. The payload
    #     is the canonical retirement fact, reconstructible by a verifier:
    #     ``<seat>\nretire\n<from>\n<to>\n<successor pub hex>``.
    _record = (f"{seat}\nretire\n{gen_before}\n{gen_after}\n"
               f"{_succ_pub.hex()}")
    _sig = scheme.sign(_pred_priv, _record.encode()).hex()
    # (d) SL5.05 handover-order fix -- DEFER the <seat>.key REPLACE. The
    #     successor private key travels back in ``pending_key`` instead of
    #     being written here, and the actual atomic `os.replace` happens in
    #     cmd_rotate_self ONLY after the successor spawn-row write
    #     (`_successor_row_write`) and its ONE commit (`_commit_spawn_row`)
    #     have SUCCEEDED. A failed spawn (the `rc != 0` return after
    #     spawn_window), a failed row write, or a failed commit therefore
    #     leaves <seat>.key BYTE-IDENTICAL holding the PREDECESSOR key -- no
    #     successor key is ever written out of step with the row that names
    #     it. send's exact JSON shape + SEAT_KEY_MODE 0600 are re-applied by
    #     `_apply_successor_key_pending`.
    _retired = {
        "pub": _pred_pub.hex(),
        "fp": send.seatsig.fingerprint(_pred_pub),
        "from": gen_before,
        "to": gen_after,
        "rotated_by_sig": _sig,
    }
    return {
        "successor_pub": _succ_pub.hex(),
        "scheme": scheme_name,
        "retired": _retired,
        "pending_key": {
            "path": str(key_path),
            "scheme": scheme_name,
            "priv_hex": _succ_priv.hex(),
        },
        "note": (f"retired seat {seat!r}'s key {_retired['fp']} "
                 f"(gen {gen_before}->{gen_after}); successor key minted "
                 f"but NOT yet written (defers to the post-row-write "
                 f"commit); rotated_by_sig verifies under the retired pub"),
    }


def _apply_successor_key_pending(pending: dict) -> str:
    """SL5.05 handover-order fix -- perform the ONE deferred <seat>.key
    atomic replace that `_rotate_successor_key` now defers. ``pending`` is
    the ``pending_key`` dict the rotation returned (``{path, scheme,
    priv_hex}``). Writes send's exact JSON key-file shape at SEAT_KEY_MODE
    0600 via a temp + `os.replace` (no second key-writer format). Called by
    `_apply_successor_key_gated` ONLY after the successor spawn-row write and
    its ONE commit have SUCCEEDED. Returns a one-line outcome."""
    import send  # local: same dir (send.py pattern, no import cycle)
    key_path = Path(pending["path"])
    payload = json.dumps({"scheme": pending["scheme"],
                          "priv_hex": pending["priv_hex"]})
    _dir = key_path.parent
    _dir.mkdir(parents=True, exist_ok=True)
    _tmp = _dir / f".{key_path.name}.tmp"
    _fd = os.open(_tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                  send.SEAT_KEY_MODE)
    try:
        with os.fdopen(_fd, "w") as _f:
            _f.write(payload)
    except BaseException:  # noqa: BLE001
        try:
            os.close(_fd)
        except OSError:
            pass
        raise
    os.chmod(_tmp, send.SEAT_KEY_MODE)
    os.replace(_tmp, key_path)
    return (f"key_replace: wrote successor key to {key_path} "
            f"(0600, atomic replace)")


def _persist_pending_key(key_rotation: dict, key_path: Path) -> str:
    """g15.26 claim (a) -- PERSIST the pending successor key, not drop it.
    Called by `_apply_successor_key_gated` when the row WAS written and
    committed (so HEAD's committed row names the successor PUBKEY) but the
    season-branch PUSH FAILED. Writes the successor private key to
    `<sessions>/seats/<seat>.key.pending` (SEAT_KEY_MODE 0600, temp +
    os.replace, never committed) as the JSON shape `{scheme, priv_hex,
    pub_hex, gen_after, minted_at}`, derived from the rotation dict -- so a
    later successful push of that row can complete the swap
    (`_complete_pending_key_swap`). Without this file the successor private
    key exists nowhere on disk (it lived only in the rotation dict before
    this), and the seat would go on signing under a predecessor key origin's
    row (once pushed) no longer names. Best-effort: if the file cannot be
    written we still report the deferred swap (never raise). Returns ONE
    line naming the pending path."""
    import send  # local: same dir (send.py pattern, no import cycle)
    _pend = key_path.parent / f"{key_path.name}.pending"
    _pend.parent.mkdir(parents=True, exist_ok=True)
    _frag = {
        "scheme": key_rotation.get("scheme")
        or (key_rotation.get("pending_key") or {}).get("scheme"),
        "priv_hex": (key_rotation.get("pending_key") or {}).get("priv_hex"),
        "pub_hex": key_rotation.get("successor_pub"),
        "gen_after": (key_rotation.get("retired") or {}).get("to"),
        "minted_at": (key_rotation.get("note") or ""),
    }
    _tmp = _pend.parent / f".{_pend.name}.tmp"
    try:
        _fd = os.open(_tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                      send.SEAT_KEY_MODE)
        try:
            with os.fdopen(_fd, "w") as _f:
                _f.write(json.dumps(_frag))
        except BaseException:  # noqa: BLE001
            try:
                os.close(_fd)
            except OSError:
                pass
            raise
        os.chmod(_tmp, send.SEAT_KEY_MODE)
        os.replace(_tmp, _pend)
    except (OSError, TypeError, ValueError):
        return (f"key_replace: NOT applied -- push did not succeed; "
                f"{key_path} left byte-identical; pending successor key "
                f"could NOT be persisted to {_pend}"
                f" (deferred swap on later join-origin)")
    return (f"key_replace: NOT applied -- push did not succeed; "
            f"{key_path} left byte-identical; pending successor key "
            f"persisted to {_pend} (0600, deferred swap on a later "
            f"successful push)")


def _complete_pending_key_swap(root: Path, seat: str) -> str:
    """g15.26 claim (b) -- COMPLETE a deferred successor-key swap at a later
    successful push of that row. Callers invoke it AFTER `_push_season_branch`
    reports a successful push (origin now carries the committed row). A
    `<sessions>/seats/<seat>.key.pending` file (written by
    `_persist_pending_key` when an earlier push FAILED) whose `pub_hex`
    equals the seat's COMMITTED row pubkey (read fresh via `git show
    HEAD`, never the dirty copy -- origin just received exactly this HEAD)
    triggers the ONE deferred atomic replace of `<seat>.key` with the
    pending private key, then deletes the pending file and prints one line
    `key swap completed (deferred from gen N)`. If the pending file's
    pub_hex does NOT match the committed row (the row still names the OLD
    pubkey), the pending file is left alone -- the swap stays deferred, and
    ONE line says so. Absent pending file / gitless root -> '' (nothing to
    do, never a failure). Never raises."""
    import send  # local: same dir (send.py pattern)
    _key = send._seat_key_path(root, seat)
    _pend = _key.parent / f"{_key.name}.pending"
    if not _pend.is_file():
        return ""
    try:
        _obj = json.loads(_pend.read_text())
    except (ValueError, OSError):
        return (f"key swap NOT completed -- unreadable pending file "
                f"{_pend} (left as-is)")
    _pend_pub = str(_obj.get("pub_hex") or "")
    if not _pend_pub:
        return (f"key swap NOT completed -- pending file {_pend} carries "
                f"no pub_hex (left as-is)")
    # HEAD's committed row is origin's row right now (the push just
    # succeeded): only a full match flips the key.
    _committed = send._seats_committed_rows(root)
    _row = send._seat_row_in(_committed, seat) if _committed else None
    _row_pub = str((_row or {}).get("pubkey") or "")
    _gen = str(_obj.get("gen_after") or _obj.get("gen") or "?")
    if not _row or _row_pub != _pend_pub:
        return (f"key swap NOT completed -- committed row for {seat} still "
                f"names the old pubkey (deferred, gen {_gen})")
    try:
        _tmp = _key.parent / f".{_key.name}.tmp"
        _fd = os.open(_tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
                      send.SEAT_KEY_MODE)
        try:
            with os.fdopen(_fd, "w") as _f:
                _f.write(json.dumps({"scheme": _obj.get("scheme"),
                                     "priv_hex": _obj.get("priv_hex")}))
        except BaseException:  # noqa: BLE001
            try:
                os.close(_fd)
            except OSError:
                pass
            raise
        os.chmod(_tmp, send.SEAT_KEY_MODE)
        os.replace(_tmp, _key)
        _pend.unlink()
    except (OSError, ValueError):
        return (f"key swap NOT completed -- could not replace {_key} "
                f"(pending {_pend} left as-is)")
    return f"key swap completed (deferred from gen {_gen})"


def _finish_pending_swap_on_push(root: Path, seat: str,
                                 push_line: str | None) -> str:
    """g15.26 claim (b) -- ONE helper every push-OK site calls to complete a
    deferred `<seat>.key.pending` swap. It completes the swap exactly when
    ``push_line`` reports a successful push (starts ``push: OK``): that is the
    exact gate `_commit_spawn_row` used to stock locally, lifted into a
    single call so a future push site (ack/prepare/cron/keygen --all-live)
    cannot drift into completing a swap on a FAILED push. Returns the one-line
    outcome ('' when there is no push OK, no pending file, or the committed
    row still names the old pubkey) and prints the completed-swap line to
    stderr. Never raises."""
    if not str(push_line or "").startswith("push: OK"):
        return ""
    _done = _complete_pending_key_swap(root, seat)
    if _done:
        print(_done, file=sys.stderr)
    return _done


def _apply_successor_key_gated(key_rotation, row_outcome, commit_outcome) -> str:
    """SL5.05 handover-order gate -- turn a rotation's DEFERRED successor key
    into the on-disk <seat>.key ONLY when the successor spawn-row write, its
    ONE commit, AND the season-branch PUSH all SUCCEEDED (mur-SL2.13 (2): the
    swap waits for the push -- a push FAILED still yields the join, but the
    key is deferred and NOT swapped, so a key on disk never disagrees with
    what origin holds). ``key_rotation`` is `_rotate_successor_key`'s dict
    (a NO-OP -> '' when it carries no ``pending_key``); ``row_outcome`` is
    the `_successor_row_write` return (starts ``config:seats row`` on
    success) and ``commit_outcome`` is the `_commit_spawn_row` return (starts
    ``spawn_row_commit: FAILED`` / ``FAILED:`` on failure; carries a trailing
    ``\npush: <line>`` when the push leg ran). A push line starting ``push:
    FAILED`` defers the swap with ONE stderr line naming it; a SKIPPED or
    absent push is NOT a failure (a gitless / byte-identical case flips the
    key exactly as before). Any other combination -- row write failed, commit
    failed, or the write never ran -- leaves the predecessor key file
    BYTE-IDENTICAL and records the refusal, never replacing it. Never raises.
    Returns one line for the handover's ``key_replace``."""
    if not key_rotation or not key_rotation.get("pending_key"):
        return ""
    _path = key_rotation["pending_key"]["path"]
    _row_ok = str(row_outcome or "").startswith("config:seats row")
    _commit = str(commit_outcome or "")
    _commit_failed = _commit.startswith(("spawn_row_commit: FAILED",
                                         "FAILED:"))
    # the push outcome rides the commit string's trailing line, if present:
    # ``\npush: push: FAILED -- ...``. Absent (early-return paths never
    # reached the push) or SKIPPED is NOT a failure -- only ``push: FAILED``.
    _push_line = _commit.rpartition("\npush: ")[2]
    # rpartition keeps the helper's own ``push: ...`` prefix on _push_line.
    _push = _push_line
    _push_failed = _push.startswith("push: FAILED")
    if _row_ok and not _commit_failed and not _push_failed:
        return _apply_successor_key_pending(key_rotation["pending_key"])
    if not _row_ok:
        _why = "row write"
    elif _commit_failed:
        _why = "commit"
    else:
        _why = "push"
    # SL: on a push failure the swap is DEFERRED -- the ONE stderr line naming
    # the deferred swap (the caller prints this return to stderr). g15.26
    # claim (a): unlike a row-write/commit failure (where NO successor pubkey
    # reached a committed row, so there is nothing to complete), a push
    # failure leaves HEAD's COMMITTED row naming the successor pubkey -- so
    # the pending successor key is PERSISTED to <seat>.key.pending, not
    # dropped with the return string, and a later successful push of that row
    # (`_complete_pending_key_swap`) atomically completes the swap. The
    # falsifier "after a failed push the minted key exists nowhere on disk"
    # is closed here.
    if _why == "push":
        return _persist_pending_key(key_rotation, Path(_path))
    return (f"key_replace: NOT applied -- {_why} did not succeed; "
            f"{_path} left byte-identical with the predecessor key, NO "
            f"successor key written (deferred swap on later join-origin) "
            f"(row={str(row_outcome)!r} commit={_commit!r} "
            f"push={_push!r})")


def _stamp_rotating_header(full: str, frac: float, hmz: str) -> str:
    """Stamp the card's OWN `# SESSION HANDOFF` header with the rotation
    fact, in the SAME write that lands the where-it-stops slot.

    goal:g15.25 line (3) (hypothesis:l4-rotate-self-stamps-the-card-header-
    itself... (a)): the FIRST line matching `^# SESSION HANDOFF` gains exactly
    ONE trailing parenthetical ` (rotating at <frac> of the line, <HH:MMZ>)`;
    when such a ` (rotating at` parenthetical is ALREADY present it is
    REPLACED, never double-appended (a second run re-stamps). A card with NO
    `# SESSION HANDOFF` header is returned byte-identical (never invent a
    header). Operates on the fully rendered card text."""
    stamp = f" (rotating at {frac:.4f} of the line, {hmz})"
    lines = full.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("# SESSION HANDOFF"):
            if " (rotating at" in ln:
                start = ln.index(" (rotating at")
                end = ln.find(")", start)
                if end == -1:
                    end = len(ln)
                lines[i] = ln[:start] + stamp + ln[end + 1:]
            else:
                lines[i] = ln.rstrip() + stamp
            break
    return "\n".join(lines) + "\n"


def _fence_run(ln: str) -> int:
    """Length of the backtick fence run on `ln`, or 0 when it is not a
    CommonMark fence line. A fence line is optional leading whitespace then
    a run of >= 3 backticks (the opener may carry a trailing info string,
    the closer is backticks alone). Returns the run length so a length-aware
    scan can pair the OUTER fence and let an inner (shorter) fence survive
    as content (goal:g15.25 residue (iii))."""
    s = ln.strip()
    if not s.startswith("`"):
        return 0
    n = 0
    for ch in s:
        if ch == "`":
            n += 1
        else:
            break
    return n if n >= 3 else 0


def _fence_for(stops_text: str) -> str:
    """The fence string that wraps `stops_text`: a run of backticks LONGER
    than every code fence already inside it, three by default. CommonMark
    closes a fence with the next run >= the opener, so an inner fence one
    shorter never closes the block (goal:g15.25 residue (iii)) — a stops
    text carrying its own ``` nests inside a four-backtick (or longer)
    outer fence and pairs correctly on the next write."""
    inner = 3
    for ln in stops_text.splitlines():
        n = _fence_run(ln)
        if n >= inner:
            inner = n + 1        # outer must EXCEED every inner fence run
    return "`" * inner


def _render_stops_block(stops_text: str, diff_gap: str | None) -> str:
    """Render the where-it-stops SLOT BLOCK -- the ```-fenced code block
    holding the stops text, plus the optional `diff requested:` line AFTER
    the fence -- as ONE unit. BOTH the CREATE and the REPLACE paths of
    `_write_stops_section` build the slot's block from this single function,
    so a slot written fresh and one filled over an existing block take an
    identical shape, and the exterior prose of an existing slot that sits
    OUTSIDE the fence is carried verbatim by the callers. The fence is
    always part of the block; a stops text that itself carries a ```
    fence is wrapped in a LONGER outer fence (`_fence_for`, the CommonMark
    rule) so the inner fence is content, never a delimiter (goal:g15.25
    line (3), residue (iii))."""
    fence = _fence_for(stops_text)
    out = fence + "\n" + stops_text.rstrip("\n") + "\n" + fence
    if diff_gap:
        out += f"\n\ndiff requested: {diff_gap}"
    return out


def _stops_replace_fenced_region(lines: list[str], block: str):
    """Replace the fenced region of `lines` (the slot's content span) with
    `block` -- the WHOLE fenced block written together -- carrying every
    line OUTSIDE the fence (prose before it and after it) verbatim. Returns
    the new line list, or None when `lines` carries no fence (the caller
    then replaces the whole span). The whole region from the opening
    delimiter to the matching closing delimiter is replaced by the single
    rendered block, so the slot gains a fresh fence+prose unit instead of
    splicing the stops text between pre-existing delimiters (which a stops
    text carrying its own fence would interlock with)."""
    fence_i = None
    for i, ln in enumerate(lines):
        if _fence_run(ln) >= 3:
            fence_i = i
            break
    if fence_i is None:
        return None
    opener = _fence_run(lines[fence_i])
    close_i = None
    # CommonMark closes on the first fence run >= the opener — so with a
    # longer outer fence the inner (shorter) fences are content and only the
    # real closer (run >= opener) pairs (goal:g15.25 residue (iii)).
    for i in range(fence_i + 1, len(lines)):
        if _fence_run(lines[i]) >= opener:
            close_i = i
            break
    if close_i is None:
        close_i = len(lines) - 1
    # the rendered block trails a `diff requested:` line after the close
    # fence; a re-write must REPLACE (never stack) the previous block's
    # trailer, so extend the replaced region over an optional blank + one
    # such trailer line (goal:g15.25 residue (ii)).
    tail = close_i + 1
    if tail < len(lines) and lines[tail].strip() == "":
        tail += 1
    if (tail < len(lines)
            and lines[tail].lstrip().startswith("diff requested:")):
        close_i = tail
    return lines[:fence_i] + block.splitlines() + lines[close_i + 1:]


def _write_stops_section(card_path: Path, seat: str, stops_text: str,
                         diff_gap: str | None = None,
                         frac: float | None = None):
    """goal:g15.25 line (3) -- write <stops_text> as the body of the seat's
    own card's where-it-stops slot (the `### 🔴 Where it stops` section, or
    any header whose title `_locate_where_it_stops` keys on -- 'where it
    stops' / 'next command'), replacing only the slot's FENCED block (the
    fence + the stops text together, rendered by `_render_stops_block`) and
    carrying the slot's own prose OUTSIDE the fence -- before it and after
    it -- byte-identical. When the card has no where-it-stops slot at ALL,
    the slot is CREATED at the card's end as `### 🔴 Where it stops` using
    the SAME render function. When `--ask-diff <gap>` accompanies `--stops`,
    the gap is ALSO written as `diff requested: <gap>` after the fence.
    Returns `(body, slot)` on success (slot in {'replaced', 'created'})
    or `(None, error)` when the where-it-stops slot is AMBIGUOUS (refused,
    never guessed). Never raises."""
    existing = (card_path.read_text(encoding="utf-8")
                if card_path.exists() else "")
    preamble, sections = _split_card_sections(existing)
    stops = _locate_where_it_stops(sections)
    if stops == "ambiguous":
        return None, "ambiguous where-it-stops slot on the own card; " \
                     "refused (rotate-self --stops never guesses)"
    if stops is None:
        extra = (f"### 🔴 Where it stops\n"
                 + _render_stops_block(stops_text, diff_gap))
        full = _render_card(preamble, sections)
        full = full.rstrip("\n") + "\n\n" + extra + "\n"
        if frac is not None:
            full = _stamp_rotating_header(
                full, frac, datetime.utcnow().strftime("%H:%MZ"))
        card_path.parent.mkdir(parents=True, exist_ok=True)
        card_path.write_text(full, encoding="utf-8")
        return full, "created"
    sec_idx, sub = stops
    header, body = sections[sec_idx]
    if sub is not None and sub >= 0:
        # a `###`-level subheader INSIDE a `## ` section: replace only the
        # subheader + its block up to the next heading (or EOF), carrying
        # everything ABOVE the subheader in the section verbatim (the claim:
        # 'replacing that section up to the next heading').
        lines = body.splitlines()
        keep = lines[:sub]
        sub_header = (lines[sub] if sub < len(lines)
                      else "### 🔴 Where it stops")
        end = len(lines)
        in_fence = False
        opener = 0
        for j in range(sub + 1, len(lines)):
            r = _fence_run(lines[j])
            if in_fence:
                # a fence closes only on a fence of the SAME character
                # whose run is at least the opener's (CommonMark); an inner
                # shorter fence and any `#` line inside it stay content
                # (goal:g15.25 residue (iii)).
                if r >= opener:
                    in_fence = False
                continue
            if r >= 3:                      # an opener: record its run
                in_fence = True
                opener = r
                continue
            if lines[j].strip().startswith("#"):
                end = j
                break
        tail = lines[end:] if end < len(lines) else []
        block = _render_stops_block(stops_text, diff_gap)
        new_region = _stops_replace_fenced_region(lines[sub + 1:end], block)
        if new_region is None:
            new_region = block.splitlines()   # no fence: whole slot replaced
        new_body = _join_body(keep + [sub_header] + new_region + tail)
    else:
        block = _render_stops_block(stops_text, diff_gap)
        new_region = _stops_replace_fenced_region(body.splitlines(), block)
        new_body = block if new_region is None else _join_body(new_region)
    sections[sec_idx] = (header, new_body)
    full = _render_card(preamble, sections)
    if frac is not None:
        full = _stamp_rotating_header(
            full, frac, datetime.utcnow().strftime("%H:%MZ"))
    card_path.parent.mkdir(parents=True, exist_ok=True)
    card_path.write_text(full, encoding="utf-8")
    return full, "replaced"


def _commit_stops_row(root: Path, seat: str, card_path: Path,
                      msg: str) -> str:
    """goal:g15.25 line (3) -- the ONE rotate-out commit: the stop text's
    own card + the seat's OWN seats.md row, and NOTHING else, as ONE
    pathspec commit. NEVER `git add -A`: the card is staged by blob from the
    working tree and the seats.md row by the own-row content
    (`_seats_ownrow_content`), both into a throwaway index seeded from HEAD,
    so a foreign dirty seats.md row or any other dirty path never rides the
    rotate-out. The commit lands in the tree the card lives in (`_git_toplevel
    (root)` -- the seat's own worktree, where `_own_card_path` resolves). A
    seat with no own-row seats change commits the card ALONE (still one
    rotate-out commit, still 'nothing outside card + seats.md'). Never
    raises. Returns a one-line outcome for the caller to print."""
    if card_path is None or not card_path.exists():
        return "stop_commit: SKIPPED — no own card to commit"
    top = _git_toplevel(root)
    if top is None:
        return "stop_commit: SKIPPED — no git repo (gitless fixture/root)"
    card_rel = os.path.relpath(card_path, top)
    if card_rel.startswith(".."):
        return "stop_commit: SKIPPED — own card sits outside the repo top"
    seats = _ack_seats_path(root)
    seats_rel = os.path.relpath(seats, top)
    own = _seats_ownrow_content(root, top, seat)
    _stage_seats = None
    if own is not None:
        _hs = subprocess.run(["git", "-C", str(top), "show",
                              f"HEAD:{seats_rel}"], capture_output=True,
                             text=True, timeout=10)
        if _hs.returncode != 0 or _hs.stdout != own:
            _stage_seats = own   # the own row actually differs from HEAD
    import tempfile  # noqa: PLC0415  (mirrors _ack_commit_seats / spawn_row)
    fd, tmp_index = tempfile.mkstemp(prefix="stoprow-idx-")
    os.close(fd)
    env = dict(os.environ)
    env["GIT_INDEX_FILE"] = tmp_index

    def _tg(parts, **kw):
        return subprocess.run(["git", "-C", str(top)] + parts,
                              capture_output=True, text=True, env=env, **kw)

    try:
        seed = _tg(["read-tree", "HEAD"])
        if seed.returncode != 0:
            seed = _tg(["read-tree", "--empty"])
            if seed.returncode != 0:
                return (f"stop_commit: FAILED — git read-tree: "
                        f"{seed.stderr.strip()}")
        cb = _tg(["hash-object", "-w", "--stdin"],
                 input=card_path.read_text(encoding="utf-8"))
        if cb.returncode != 0 or not cb.stdout.strip():
            return "stop_commit: FAILED — card hash-object"
        upd = _tg(["update-index", "--add", "--cacheinfo",
                   f"100644,{cb.stdout.strip()},{card_rel}"])
        if upd.returncode != 0:
            return (f"stop_commit: FAILED — card update-index: "
                    f"{upd.stderr.strip()}")
        if _stage_seats is not None:
            sb = _tg(["hash-object", "-w", "--stdin"], input=_stage_seats)
            if sb.returncode != 0 or not sb.stdout.strip():
                return "stop_commit: FAILED — seats hash-object"
            u2 = _tg(["update-index", "--add", "--cacheinfo",
                      f"100644,{sb.stdout.strip()},{seats_rel}"])
            if u2.returncode != 0:
                return (f"stop_commit: FAILED — seats update-index: "
                        f"{u2.stderr.strip()}")
        rc = _tg(["commit", "-q", "-m", msg])
        if rc.returncode != 0:
            return (f"stop_commit: FAILED — git commit: "
                    f"{rc.stderr.strip()}")
        # point the REAL index's card (and own-row seats) entry at the
        # committed blob — the same sync `_ack_commit_seats` does for its own
        # row — so the rotate-out leaves `git status` CLEAN (the claim's
        # proof target). WITHOUT this the temp-index commit advances HEAD but
        # leaves the real index stale: the card+seats show staged+unstaged
        # modified, and a later only-behind season merge that re-touches
        # either path is REFUSED by git ("local changes would be
        # overwritten") — which is exactly the push-line-2 merge the captive
        # checklist performs before the spawn. Sync is best-effort and never
        # fails the commit (the tree is already committed; a refused sync
        # only reprints them dirty).
        subprocess.run(
            ["git", "-C", str(top), "update-index", "--add",
             "--cacheinfo", f"100644,{cb.stdout.strip()},{card_rel}"],
            capture_output=True, text=True)
        if _stage_seats is not None:
            subprocess.run(
                ["git", "-C", str(top), "update-index", "--add",
                 "--cacheinfo", f"100644,{sb.stdout.strip()},{seats_rel}"],
                capture_output=True, text=True)
    finally:
        try:
            os.unlink(tmp_index)
        except OSError:
            pass
    sha = ""
    try:
        out = subprocess.run(["git", "-C", str(top), "rev-parse",
                              "--short", "HEAD"], capture_output=True,
                             text=True, timeout=10)
        sha = (out.stdout or "").strip()
    except Exception:  # noqa: BLE001
        sha = ""
    _touched = card_rel + (f", {seats_rel}" if _stage_seats is not None else "")
    return (f"stop_commit: committed {_touched} (ONE rotate-out commit "
            f"@{sha or '?'})")


def _stops_push(root: Path, label: str = "stops") -> str | None:
    """goal:g15.25 line (3) -- push the branch a rotate-out commit landed on.
    Returns None on success (one push line printed to stderr) or a NAMING
    refusal line on failure: a refused push is a BLOCK (exit 3, nothing
    rotated). Never a force-push, never a second commit. `label` names which
    rotate-out push this is -- `stops` for push line 1 (right after the
    stops commit) and `merge` for push line 2 (the only-behind merge commit
    the captive checklist performs); ONE helper, both pushes, never a third
    implementation."""
    top = _git_toplevel(root)
    if top is None:
        return "no git repo to push (gitless fixture/root)"
    try:
        out = subprocess.run(["git", "-C", str(top), "rev-parse",
                              "--abbrev-ref", "HEAD"], capture_output=True,
                             text=True, timeout=10)
        branch = (out.stdout or "").strip()
    except Exception as exc:  # noqa: BLE001
        return f"could not resolve the branch: {exc}"
    if not branch or branch == "HEAD":
        return "detached HEAD, nothing to push"
    try:
        push = subprocess.run(["git", "-C", str(top), "push", "origin",
                               branch], capture_output=True, text=True,
                              timeout=60)
    except Exception as exc:  # noqa: BLE001
        return f"push refused: {exc}"
    if push.returncode != 0:
        return (f"push refused out: "
                f"{push.stderr.strip() or push.stdout.strip()}")
    print(f"{label} push: OK -- {branch}", file=sys.stderr)
    return None


def _rotate_human_gate(root: Path, seat: str,
                       actor: str | None = None) -> tuple[str | None, dict | None]:
    """RUNG 3 HUMAN GATE (hypothesis:l4-a-veto-freezes-never-frees): rotating
    ANOTHER post is a GATED Prime-scope act. While a council+Keep veto (or an
    owner-written human_gate) shows the ``prime`` scope FROZEN, a rotation whose
    target ``seat`` is NOT the caller's own post is refused BY NAME and never
    auto-released -- no timeout, no restart, no rotation frees it, only an owner
    answer in the veto room (the claim's freeze-never-frees).

    A rotation of the caller's OWN post (the ``self_row`` carve-out) is NEVER
    gated. The actor defaults to ``$AGI_SEAT`` -- the identity a seat carries
    when it was spawned; an IDENTIFIED caller who tries to rotate another seat
    is gated when frozen, and an unidentified caller is treated as gated too
    (an unknown actor cannot claim the self carve-out).

    Returns ``(held_line, freeze_dict)`` -- ``held_line``/``freeze_dict`` both
    None means the rotation may proceed; otherwise the line names the HELD act
    and the dict carries the freeze (scope + why) for the ROTATION RECORD, so a
    reader of the record sees the freeze without asking viewport --live.
    """
    if actor is None:
        actor = os.environ.get("AGI_SEAT") or ""
    if actor and seat and actor == seat:
        return None, None  # the caller's OWN post is never gated (self_row)
    try:
        from seatsig import veto as _veto

        _groot = _shared_graph_root(root)
        _frozen, _why = _veto.is_frozen(_groot, "prime")
        if _frozen:
            held = (f"rotation: HELD -- rotating another post {seat!r} is a "
                    f"gated Prime-scope act; {_why}")
            _gate = None
            try:
                _gate = _veto.active_gate(_veto.read(_groot), "prime")
            except Exception:  # noqa: BLE001  (the frozen verdict still stands)
                _gate = None
            freeze = {
                "scope": "prime",
                "hold_reason": _why,
                "auto_released": False,
                "note": "an unanswered human gate freezes, never frees; "
                        "only an owner answer in the veto room clears it",
            }
            if _gate:
                for _k in ("veto_ref", "since", "reason"):
                    if _gate.get(_k):
                        freeze[_k] = _gate[_k]
            return held, freeze
    except Exception:  # noqa: BLE001  (a broken veto cell never gates silently)
        pass
    return None, None


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
    # goal:g15.14 STEP 2 -- `rotate-self --prepare` is the same captive
    # checklist the `prepare` subcommand prints, on the SAME 
    # `_prepare_checks`: one implementation, two spellings. Its branch guard
    # lives in `cmd_prepare` (P1-b): the guard fires there FIRST, before any
    # merge, so a `--prepare --perform` on master cannot MERGE season INTO
    # master. A seat on a refusing branch asks the guard, then what blocks it.
    if getattr(args, "prepare", False):
        args.seat = args.name
        # goal:g15.14 R1 (P1-c one spelling over) — the REGISTRY gate runs in
        # the `--prepare` path too, BEFORE any merge. `cmd_prepare` (which
        # this path delegates to) has NO registry check of its own, and
        # `--prepare` sets `perform = not dry_run` — so without this gate
        # `rotate-self --prepare --name <unregistered>` on a behind clean
        # worktree would MERGE a commit before refusing `no seat`. Same rule
        # as P1-c in the non-prepare path: the seat must exist in
        # config:seats unless --throwaway (a rehearsal-only registration that
        # never writes seats.md).
        if not getattr(args, "throwaway", False):
            _prow = _find_seat(root, args.seat)
            if _prow is None:
                print(f"ERR: no seat {args.seat!r} in the seats registry "
                      f"(.agi/nodes/.geometry/seats.md).", file=sys.stderr)
                return 1
        # rotate-self's own gate performs the only-behind merge by DEFAULT
        # (hypothesis:...-prepare-performs-the-only-behind-merge...) -- a
        # clean, zero-conflict season merge is mechanical and costs 2-4 tool
        # calls if prompted instead. A --dry-run inspection still NEVER merges.
        args.perform = not bool(getattr(args, "dry_run", False))
        return cmd_prepare(args, root)
    # RUNG 3 HUMAN GATE (hypothesis:l4-a-veto-freezes-never-frees): rotating
    # ANOTHER post is a GATED Prime-scope act. While the prime scope is FROZEN,
    # refuse BY NAME before ANY side effect (stops write, started record,
    # handoff, rename, spawn); a rotation of the caller's OWN post (self_row)
    # is never gated. The freeze is made VISIBLE IN THE ROTATION RECORD, so a
    # reader sees scope+why without asking viewport --live (claim (3)).
    _hgate, _hfreeze = _rotate_human_gate(root, args.name)
    if _hgate:
        _write_rotation_record(root, {
            "rotation": "rotate-self",
            "seat": args.name,
            "recorded_at": datetime.utcnow().isoformat() + "Z",
            "result": "held",
            "refusal_reason": _hgate,
            "human_gate": _hfreeze,
        })
        print(_hgate, file=sys.stderr)
        return 3
    guard = _check_branch_guard(root)
    if guard:
        print(guard, file=sys.stderr)
        return 1
    # (geometry guard, mechanism 3): a worktree whose own .agi/nodes/.geometry/
    # is BEHIND the shared geometry branch would spawn its successor on a
    # stale config:rotations / config:seats. Resolve WHICH tree the geometry
    # comes from once, up front — the integration tree when the worktree's own
    # is behind but the integration tree's is current; else refuse BY NAME with
    # the behind-count and the sync command. `cfg_root` feeds seat + template
    # resolution; every other rotate-self path keeps the worktree `root`.
    cfg_root, geom_src = _geometry_resolution_root(root)
    if cfg_root is None:
        print(geom_src, file=sys.stderr)
        return 1
    seat = args.name
    # goal:g15.14 P1-c — the registry gate runs BEFORE the prepare/perform
    # step. The only-behind merge `_prepare_checks(perform=)` performs is a
    # SIDE EFFECT; on a behind worktree an unregistered `--name` would
    # otherwise MERGE a commit before the "no seat" refusal. So the seat must
    # exist in the registry FIRST, and an unregistered name refuses with NO
    # merge performed. A THROWAWAY seat (hypothesis:l3-rotate-self-successor-
    # override) is a rehearsal-only registration that NEVER writes seats.md:
    # it skips this registry gate and builds a default row instead (role from
    # --role, default parent; model/effort/settings resolved from the ladder
    # inside spawn_window). Without --throwaway the gate holds exactly as
    # before — an unregistered name errors `no seat`.
    row = None
    if not getattr(args, "throwaway", False):
        row = _find_seat(cfg_root, seat)
        if row is None:
            print(f"ERR: no seat {seat!r} in the seats registry "
                  f"(.agi/nodes/.geometry/seats.md).", file=sys.stderr)
            return 1
    else:
        row = {}  # default row; never consulted against seats.md

    # goal:g15.25 line (3) -- the rotate-OUT is ONE call. When `--stops`
    # (`--stops-file F`, `--stops -` reads stdin) is given, write the stops
    # text into the seat's OWN card's where-it-stops section, commit card +
    # the seat's own seats.md row as ONE pathspec commit, push the seat
    # branch, and print the rotation line -- the post's out-count is ONE
    # call, no separate send.py (the [rotation-alert] dm IS the rotation
    # line). This runs BEFORE the captive checklist so captives 1 (unpushed),
    # 2 (dirty) and 4 (card mtime vs the last WORK commit) are satisfied BY
    # this write+commit+push, then the checklist runs unchanged. A refused
    # push is a BLOCK (exit 3, nothing rotated). `--dry-run` prints the stops
    # write, the commit message and BOTH push lines and touches nothing.
    # Without `--stops`/`--stops-file` the flow is byte-identical to today.
    _stops_src = getattr(args, "stops", None)
    _stops_file = getattr(args, "stops_file", None)
    _stops_has = _stops_src is not None or _stops_file is not None
    if _stops_has:
        _stops_text: str | None = None
        _stops_err = None
        if _stops_file is not None and _stops_src is None:
            try:
                _stops_text = Path(_stops_file).read_text(encoding="utf-8")
            except OSError as e:
                _stops_err = f"cannot read --stops-file {_stops_file!r}: {e}"
        elif _stops_src == "-":
            _stops_text = sys.stdin.read()
        elif _stops_src is not None:
            _stops_text = _stops_src
        if _stops_err or (_stops_text is None or not _stops_text.strip()):
            print(f"ERR: rotate-self --stops: "
                  f"{_stops_err or 'refuses an EMPTY stops text'}",
                  file=sys.stderr)
            return 2
        _gb = _read_generation(root, seat)
        _stops_gap = getattr(args, "ask_diff", False)
        _gap = _stops_gap if isinstance(_stops_gap, str) and _stops_gap \
            else None
        _first = _stops_text.strip().splitlines()[0][:80]
        _msg = (f"{seat} rotate-out gen {_gb}->{_gb + 1}: {_first}")
        _card = _own_card_path(root, seat)
        if args.dry_run:
            print(f"(--stops) {_resolved_stops_slot_text(_card)}")
            print(f"(--stops) would write where-it-stops into {_card}")
            print(f"(--stops) commit: {_msg!r} "
                  f"(card + the seat's own seats.md row, nothing else)")
            print("(--stops) push: the seat branch (push line 1); the "
                  "only-behind merge commit push (push line 2) before the "
                  "spawn")
            print("rotation line: delivered as the [rotation-alert] dm to "
                  "<prime> (no send.py call needed; --dry-run, nothing "
                  "written)")
        else:
            # (a) the header stamp rides this SAME write: the meter fraction
            #     is read ONCE via the seat's own pin (the value rotate-self
            #     already reads -- never re-derived), and passed down so the
            #     rotate-out is ONE card write + ONE commit.
            _frac = _seat_fraction(root, row)
            _full, _slot = _write_stops_section(
                _card, seat, _stops_text, diff_gap=_gap, frac=_frac)
            if _full is None:
                print(f"ERR: rotate-self --stops: {_slot}", file=sys.stderr)
                return 2
            print(_commit_stops_row(root, seat, _card, _msg),
                  file=sys.stderr)
            _perr = _stops_push(root)
            if _perr:
                print(f"rotate-self refused: {_perr} — clear it, then "
                      f"re-run (nothing rotated).", file=sys.stderr)
                return 3
            # g15.26 claim (b): this rotate-out PUSH succeeded, so origin
            # now carries the seat's committed row -- a deferred
            # `.key.pending` swap from an earlier failed push COMPLETES
            # through the ONE shared helper (only when the committed row
            # matches the pending key).
            _finish_pending_swap_on_push(root, seat, "push: OK")
            print("rotation line: delivered as the [rotation-alert] dm "
                  "to <prime> (no send.py call needed)")

    # goal:g15.14 STEP 2 — the captive rotate-out checklist runs BEFORE any
    # side effect (the started record, the handoff, the own-window rename,
    # the spawn). THIS is the one implementation: `rotate.py prepare` prints
    # it, rotate-self runs the SAME `_prepare_checks` and refuses BY NAME
    # with the same line. `--force` bypasses only what it bypassed today
    # (the meter-due gate); these blockers are not that gate.
    # The gate is UNCONDITIONAL — the `--window-path` fixture seam is NOT a
    # gate key (hypothesis l4-the-prepare-captives-measure-generation-
    # upstream-and-season-and-the-gate-is-not-a-test-seam, piece 2: a live
    # invocation passing --window-path used to skip the whole checklist
    # silently). Each check already answers ok when its basis is unmeasurable
    # (no git -> _git_maybe None; no pin; no ack), so a fixture root passes
    # by the same rule a real one does; a subprocess faked to refuse git
    # degrades to None, never propagates.
    # The gate performs the only-behind merge UNLESS we are dry-running
    # (--dry-run prints everything and touches nothing: a merge is a touch).
    _perform_gate = not bool(getattr(args, "dry_run", False))
    # push line 2 bookend: capture HEAD right before the checklist so the
    # merge-push below can tell a checklist-performed only-behind merge from
    # an untouched branch. The stoppable flow already pushed (line 1); a
    # clean-at-start non-stops branch is unpushed-zero here too. Only check
    # 3 WRITES a commit during the checklist, so HEAD moving is exactly a
    # merge landing. Unmeasurable HEAD (None/empty) forces no merge-push.
    _head_before_checks = _git_maybe(root, "rev-parse", "--short", "HEAD")
    _blocks = [c for c in _prepare_checks(root, seat, perform=_perform_gate,
                                          stops_rotation=_stops_has)
               if c[0]]
    # the LISTING line, never a blocker -- the rotating seat sees its live
    # background tasks BEFORE it spawns, so it knows what to leave behind
    # (hypothesis:...-lists-the-seats-live-background-tasks)
    print(f"background tasks: {_background_tasks(root, seat)}",
          file=sys.stderr)
    if _blocks:
        for _b, _nm, _cl in _blocks:
            print(f"rotate-self blocked: {_nm} — {_cl}", file=sys.stderr)
        print("rotate-self refused: clear the prepare blocker(s) above, then "
              "re-run (rotate.py prepare --seat <S> lists them).",
              file=sys.stderr)
        return 3

    # goal:g15.25 line (3) -- the ONLY-BEHIND MERGE COMMIT push (push line
    # 2), right after the checklist and BEFORE any side effect (the key
    # mint, the handoff, the rename, the spawn). The checklist PERFORMS
    # check 3's only-behind merge when it is clean; that merge lands as a
    # NEW commit AFTER the stops push already ran (or after a clean-at-start
    # non-stops branch), and nothing pushed it before the spawn -- today the
    # live flow ran ONE push while the dry-run printed two. When HEAD moved
    # during the checklist the merge commit is sitting unpushed: push it NOW
    # (the second push line), and a refused push is a BLOCK (exit 3, nothing
    # rotated) -- the same discipline as the stops push, via the SAME helper
    # (never a third push implementation). `--dry-run` never merges, so HEAD
    # provably cannot move and this is a no-op there (the dry-run already
    # prints both push lines in the stops block above, and a merge is a
    # touch dry-run must not perform).
    _head_after_checks = _git_maybe(root, "rev-parse", "--short", "HEAD")
    if (_head_before_checks and _head_after_checks
            and _head_before_checks[0] != _head_after_checks[0]):
        _mperr = _stops_push(root, label="merge")
        if _mperr:
            print(f"rotate-self refused: {_mperr} — clear it, then "
                  f"re-run (nothing rotated).", file=sys.stderr)
            return 3
        # g15.26 claim (b): the merge commit's HEAD now names the seat's
        # committed pubkey and this push succeeded -- complete any deferred
        # pending swap through the ONE shared helper.
        _finish_pending_swap_on_push(root, seat, "push: OK")

    # goal:g15.25 line (1) -- rotate-self is KEY-GATED. A keyed seat cannot
    # rotate without its own signing key file; the gate refuses BY NAME and
    # runs BEFORE any side effect (started record, handoff, rename, spawn).
    _key_err = _rotate_key_gate(root, seat, row)
    if _key_err:
        print(_key_err, file=sys.stderr)
        return 1
    # goal:g15.25 line (1) minting half -- an UNKEYED real row mints its own
    # first key in this SAME step (incremental fleet keying), so its
    # successor wakes keyed. Best-effort row write; never fails the rotation.
    _mint_note = _rotate_first_key(
        root, cfg_root, seat, row,
        dry_run=bool(getattr(args, "dry_run", False)))
    if _mint_note:
        print(_mint_note, file=sys.stderr)

    # L4.112 (A): resolve the rotation template at the TOP of rotate-self,
    # BEFORE any side effect (the started record, the handoff, the own-window
    # rename). A missing / unhelpful rotations.md must refuse HERE, leaving the
    # window name and the handoff file untouched. The role is derived from the
    # seat row (identity SUPPLIED from the registry, never inferred), with
    # --role as its escape hatch for a throwaway seat.
    role = (row.get("role") if row else None) \
        or getattr(args, "role", None) or "parent"
    tmpl, tmpl_name, tmpl_src = _resolve_template(
        cfg_root, role, getattr(args, "template", None))
    if tmpl is None:
        print(f"ERR: {tmpl_src}", file=sys.stderr)
        return 1
    # goal:g15.17 (d)(ii): a JOIN-ONLY rotate-self is refused BY NAME — a
    # role whose template declares a `startup` block but no `first_turn` has
    # nothing to hand its successor but the join itself; rotating it would
    # spawn a successor that boots into emptiness. (The plain legacy template
    # with NO `startup` key — the pre-startup shape many tests and the
    # historical rotations use — is untouched; the refusal targets a template
    # that DECLARES a startup pipeline and then strips first_turn from it.)
    _fs_startup = tmpl.get("startup")
    if isinstance(_fs_startup, dict) and not (_fs_startup.get("first_turn") or []):
        print(f"ERR: role {role!r} template {tmpl_name!r} is join-only "
              "(startup declared with no first_turn) — rotate-self refused: "
              "a seat with no first_turn has nothing to hand off. "
              "(goal:g15.17)", file=sys.stderr)
        return 1
    print(f"(0) template -> {tmpl_name!r} ({tmpl_src}) "
          f"brief={tmpl.get('brief_file')!r} "
          f"steps={tmpl.get('steps')} telemetry={tmpl.get('telemetry')} "
          f"geometry={geom_src}")
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
    # (hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-
    #  hands-the-successor-exactly-one-call): `--ask-diff` opts the rotation
    # into handing the successor ONE explicit `diff` call instead of
    # pre-answering the ack channel.
    ask_diff = bool(getattr(args, "ask_diff", False))

    # goal:g15.25 line (2) SUCCESSOR KEY half (hypothesis l4-rotate-self-
    # is-key-gated...): a KEYED seat mints its successor keypair at rotation
    # handover and signs the retirement with its own (predecessor) key BEFORE
    # this point (the predecessor private key is read while still on disk).
    # The actual atomic replace of <sessions>/seats/<seat>.key is DEFERRED
    # (SL5.05 handover-order fix) until AFTER the successor spawn-row write
    # (s6.1 `_successor_row_write`) and its ONE commit (g15.24
    # `_commit_spawn_row`) succeed -- the successor pubkey + key_history
    # cells ride that ONE write (never a second commit). A failed spawn /
    # row write / commit leaves the predecessor key file BYTE-IDENTICAL.
    # `--dry-run` reports what it would do and touches nothing. The row
    # cells are consumed at s6.1 via `_key_rotation`.
    # g15.26 claim (a): COMPLETE any deferred `<seat>.key.pending` swap
    # BEFORE `_rotate_successor_key` mints a new successor generation. On a
    # seat that already carries a `.key.pending` (a prior push FAILED after
    # the spawn-row write committed), the committed HEAD row already names
    # the pending successor pubkey -- so flipping `.key` now (when the
    # committed row matches) resolves the old gen N->N+1 swap BEFORE this
    # rotation mints N+1->N+2, instead of orphaning the old pending key and
    # double-counting key_history once the spawn-row commit runs. The mint
    # below then reads a `.key` that already agrees with HEAD. Never on a
    # dry-run (the swap is a real write; dry-run touches nothing).
    if not getattr(args, "dry_run", False):
        _done = _complete_pending_key_swap(root, seat)
        if _done:
            print(_done, file=sys.stderr)
    _key_rotation = _rotate_successor_key(
        root, seat, row, gen_before=gen_before, gen_after=gen,
        dry_run=bool(getattr(args, "dry_run", False)))
    if _key_rotation:
        _kn = _key_rotation.get("note")
        if _kn:
            print(_kn, file=sys.stderr)

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
            gen_before=gen_before, gen_after=gen,
            template_source=geom_src)

    # (1) handoff — the successor's identity travels in the handoff HEADER so
    # it wakes already knowing its own session_ref (kid-2 step 5).
    if not args.dry_run:
        _write_handoff(root, seat, gen, predecessor_session=seat,
                       session_ref=session_ref)
        _rs_mark(steps_reached, tmpl_steps, "handoff", "1")
        _write_rotate_self_started(rec_path, seat=seat, steps=steps_reached,
                                   gen_before=gen_before, gen_after=gen,
                                   template_source=geom_src)
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
                                       gen_before=gen_before, gen_after=gen,
                                       template_source=geom_src)
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
                                       gen_before=gen_before, gen_after=gen,
                                       template_source=geom_src)
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
    if ask_diff:
        # --ask-diff leg: the predecessor wrote `diff-requested`; the
        # successor's ONE wake call is the diff review, exactly one call
        # (hypothesis:l4-the-predecessor-answers-continue-by-default-
        # and-ask-diff-hands-the-successor-exactly-one-call).
        ack_gate = (
            "ROTATION CONTINUATION (--ask-diff): your ONE wake action is "
            f"`python3 extensions/agi/bin/rotate.py ack --seat {seat} "
            f"--gen {gen} --ref <your own ListAgents ref> diff --text -` -- "
            "run it to review the handoff (the predecessor has NOT answered "
            "it). The handoff STANDS on an EMPTY diff text (`--text -` with "
            "no stdin, or `--text ''`); a non-empty diff text halts it for "
            "inspection."
        )
    else:
        ack_gate = (
            "ROTATION CONTINUATION: ack: answered continue by your "
            "predecessor -- nothing to run. The handoff needs no action on "
            "your first turn: your predecessor already answered the ack "
            "channel. (If the handoff actually needs change, you may still "
            f"run `python3 extensions/agi/bin/rotate.py ack --seat {seat} "
            f"--gen {gen} --ref <your own ListAgents ref> diff --text -` "
            "to halt the rotation for inspection.)"
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
        # (SL7.29 part (b)) the ack answer is fully knowable BEFORE the spawn
        #     (`_answer = "diff-requested" if ask_diff else "continue"`), so
        #     the PRE-SPAWN bootstrap record carries it verbatim via the
        #     `overrides` seam -- `- ack: continue (source predecessor, gen
        #     N)` (or diff-requested) at TURN ONE, instead of `ack: none`
        #     (which happened because the pre-spawn `_derive_bootstrap_fact`
        #     found no ack FILE yet -- the ack is only written at s6.3, AFTER
        #     the successor has already read this record). The post-join s11
        #     rewrite and the existing `overrides` machinery are unchanged;
        #     this only makes the TURN-ONE record truthful.
        _ack_answer = "diff-requested" if ask_diff else "continue"
        _write_bootstrap(
            root, seat=seat, generation=gen,
            telemetry=tmpl.get("telemetry"), verification=verification,
            join_pending=set(BOOTSTRAP_JOIN_ONLY_FACTS),
            overrides={"ack": f"{_ack_answer} (source predecessor, gen {gen})"})

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
                                   gen_before=gen_before, gen_after=gen,
                                   template_source=geom_src)
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
        print("(4) read back successor reply — ack channel ->")
        print(f"    ack path: {_ack_path(root, seat)}")
        print("    (default: the predecessor answered `continue` itself, so the "
              "read-back confirms the rotation with ZERO successor calls; "
              "`--ask-diff` instead leaves `diff-requested` for the successor's "
              "ONE `diff`/`continue` reply)")
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
        print(f"(generation {gen_before} -> {gen}); ack record answered "
              "continue for the successor (source: predecessor, wake 0)")
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
        _belam_gate = (role == "prime_director"
                       or getattr(args, "belam_prefix", None))
        if is_chain_seat:
            print(f"(dry-run) numeral-chain seat: successor name "
                  f"{spawn_name!r}, generation = numeral {gen}, own window "
                  "@id = tmux display-message -p '#{window_id}' "
                  "(knowable only live), ack path "
                  f"{_ack_path(root, seat)}")
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
                          f"{list(reversed(chain))!r}, TERM'd "
                          f"DEEPEST-FIRST, then the window killed by @id")
        # (r5 dry-run) the Belam FIFO cap -- the ONE reap a numeral-chain
        #     seat runs, and the cap reap for ANY `--belam-prefix` seat.
        #     GATED on the LIVE seam (role == "prime_director" OR
        #     --belam-prefix, the same condition s6.6 at the LIVE cap uses),
        #     NEVER on `is_chain_seat` alone: a plain seat GIVEN
        #     --belam-prefix reaps live but its dry-run used to print no r5
        #     plan at all. NAMED live-derived, read-only: the OLDEST
        #     predecessor window when the chain would exceed FIVE, its @id,
        #     its pane pid and the ps -e chain it would TERM deepest-first.
        #     Touches nothing. Same call path the live r5 uses
        #     (`_belam_oldest` over the live windows + the spawn_name
        #     successor; `_pane_pid(@id)` -> `_descendant_chain`).
        if _belam_gate:
            pfx = getattr(args, "belam_prefix", None) or "belam"
            oldest = _belam_oldest(_existing_for_chain, spawn_name, pfx)
            if oldest is None:
                _gated_own = ("the own-window reap is GATED OFF on a "
                              "numeral-chain seat" if is_chain_seat else
                              "the own-window reap (r4/s12) above still "
                              "runs")
                print(f"    (r5) Belam FIFO cap: chain stays at/below FIVE "
                      f"live {pfx!r} windows -> no Belam cap reap "
                      f"({_gated_own})")
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
                              f"{list(reversed(chain))!r}, TERM'd "
                              f"DEEPEST-FIRST, then the window killed by @id")
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
    # the effective bounded join poll (seconds), None when NO join ran — a
    # post-join bootstrap must not promise `pending: resolved after join` for
    # facts the join left unresolved (Prime XI line (7), second half).
    join_poll_eff = None
    if session_ref:
        # internal seam: identity supplied directly; no registry JOIN.
        succ_session_id = session_ref
    elif succ_window_id:
        join_poll_eff = (getattr(args, "registry_poll", None)
                         or REGISTRY_JOIN_TIMEOUT_S)
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
                generation=gen,
                # goal:g15.25 line (2): the successor pubkey + key_history
                # cells ride this ONE spawn-row write (and the ONE
                # `_commit_spawn_row` below) -- never a second submit.
                key_rotation=_key_rotation)
        except Exception as exc:  # noqa: BLE001
            handover["successor_row"] = f"FAILED: {exc}"
        # (g15.24, Sensei's pick, fix (a)): rotate-self COMMITS the s6.1
        # spawn-row write ITSELF, immediately after `_successor_row_write`
        # succeeds and before anything else runs — ONE plain `git commit` in
        # the seat worktree's toplevel, seats.md ONLY (mirror
        # `_ack_commit_seats`; never `-A`, never a grid commit, never a
        # push). The successor's ONE required wake act, `rotate.py ack ...
        # continue`, then finds seats.md CLEAN and the r3b gate
        # `_ack_seats_dirty` stays as written. The outcome (sha or the reason
        # it did not commit) is recorded in the handover as
        # `spawn_row_commit` and printed in the rotation record. A THROWAWAY
        # seat (`successor_row` = skipped) wrote NO row, so nothing commits.
        # Never raises, never fails the rotation (gated + helper is
        # already fail-soft).
        if handover["successor_row"].startswith("config:seats row"):
            try:
                handover["spawn_row_commit"] = _commit_spawn_row(
                    root, seat=seat, generation=gen,
                    session_id=succ_session_id,
                    window=succ_window_id or spawn_name,
                    pid=succ_pid)
            except Exception as exc:  # noqa: BLE001
                handover["spawn_row_commit"] = f"FAILED: {exc}"
        # SL5.05 handover-order fix: the actual <seat>.key REPLACE happens
        # HERE and only here -- after the successor spawn-row write and its
        # ONE commit have SUCCEEDED (never a second commit). `_rotate_successor_key`
        # minted + signed EARLY but DEFERRED the os.replace; a failed spawn
        # (the rc return above), row write, or commit leaves the predecessor
        # key file BYTE-IDENTICAL and records the refusal in the handover.
        handover["key_replace"] = _apply_successor_key_gated(
            _key_rotation,
            handover.get("successor_row"),
            handover.get("spawn_row_commit"))
        if handover["key_replace"]:
            print(handover["key_replace"], file=sys.stderr)
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
        # (s6.3) write the ACK on the successor's behalf, carrying the machine
        #     identity. DEFAULT (no `--ask-diff`): `answer: continue,
        #     source: predecessor` -- the predecessor answers its OWN ack, so
        #     the read-back immediately confirms the rotation and the successor
        #     runs NO ack (wake 0). WITH `--ask-diff` the predecessor instead
        #     writes `answer: diff-requested, source: predecessor` and hands
        #     the successor EXACTLY ONE wake call --
        #     `rotate.py ack ... diff --text -` -- so the rotation halts for
        #     handoff inspection exactly as today
        #     (hypothesis:l4-the-predecessor-answers-continue-by-default-and-
        #     ask-diff-hands-the-successor-exactly-one-call).
        _ack_answer = "diff-requested" if ask_diff else "continue"
        try:
            handover["ack_written"] = str(_write_ack(
                root=root, seat=seat, gen_after=gen,
                session_ref=succ_session_id, answer=_ack_answer))
            if ask_diff:
                print("(s6.3) --ask-diff: the successor's ONE wake call is:\n"
                      f"    python3 extensions/agi/bin/rotate.py ack --seat "
                      f"{seat} --gen {gen} --ref <your ListAgents ref> "
                      "diff --text -", file=sys.stderr)
            else:
                print("(s6.3) default: answered `continue` for the successor "
                      "(source: predecessor); the successor runs NO ack (wake "
                      "0).", file=sys.stderr)
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
        # (O3/g15.25 (c)) the reap stand-in seam is RETIRED: s12_self_reap
        #     (written at the end of this same flow) is the ONE reap section.
        #     The record never claimed the predecessor was NOT reaped while
        #     s12 said it was reaped — one truth per record.
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
                                   gen_before=gen_before, gen_after=gen,
                                   template_source=geom_src)
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
                                   gen_before=gen_before, gen_after=gen,
                                   template_source=geom_src)
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
    reply_decision = None
    if ack is not None and ack.get("answer") == "continue":
        acked_continue = True
    elif ack is not None and ack.get("answer") == "diff":
        # A `diff` with an EMPTY/whitespace text is the reviewed-no-change
        # answer the --ask-diff gate names: the handoff STANDS, on the same
        # success path as `continue`. A non-empty diff text means the handoff
        # needs change and halts (hypothesis:l4-the-ask-diff-gate-offers-no-
        # continue-and-an-empty-diff-stands-the-handoff).
        if not (ack.get("text") or "").strip():
            acked_continue = True
            reply_decision = "diff-empty"
        else:
            _write_rotation_record(root, _rotate_self_record(
                seat=seat, result="diff", gen_before=gen_before, gen_after=gen,
                succ=succ,
                readback_log=Path(_ack_path(root, seat)).expanduser(),
                refusal="successor acked diff: handoff needs change"),
                path=rec_path)
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
    # (s5) model_confirm — the PRE-TURN probe (goal:g15.25 SL7.40 (b)). On a
    #     real rotation the successor has produced NO assistant turn yet at
    #     this point (this runs before the own-window kill), so the confirm
    #     would always come back skipped and the record would LIE that no
    #     model was confirmed even after the successor answers. The probe
    #     stays (cheap, and on a fixture it may already have a turn) but a
    #     skip is recorded DEFERRED `after_join` — the ONE real confirm runs
    #     in run_after_join once the successor transcript carries a turn, and
    #     overwrites THIS in place. A reader can tell pre-turn deferral from
    #     a real verdict: `deferred:` is a non-verdict, never `skipped:`.
    _mc = _confirm_successor_model(
        seat=seat,
        expected_model=((row.get("model") if row else None) or args.model),
        expected_effort=((row.get("effort") if row else None)
                         or args.effort),
        pid=succ_pid, transcript=succ_transcript)
    if isinstance(_mc, str):
        handover["model_confirm"] = (
            "deferred: after_join — no assistant turn yet at rotate-self; "
            "run_after_join confirms once the successor transcript carries one")
    else:
        _mc["confirm_at"] = "rotate-self"
        handover["model_confirm"] = _mc

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
        overrides=overrides,
        join_poll_secs=join_poll_eff)

    # (6) the record is the deliverable — write it, durably, BEFORE the own
    #     window is killed, so it survives regardless of what the kill does.
    record_path = _write_rotation_record(root, _rotate_self_record(
        seat=seat, result="success", gen_before=gen_before, gen_after=gen,
        succ=_observed_windows(tmux_session, args.window_path),
        pred=pred, readback_log=log, cursor_offset=offset,
        handover=handover, steps_reached=steps_reached,
        reply_decision=reply_decision), path=rec_path)

    # (5.75) GOAL:g15.25 (SL7.15) — a completed rotation ROTATES the ack
    #     file. The successor confirmed gen `gen`; that generation's live ack
    #     (`seats/<seat>.ack.json`) is now RENAMED to `seats/<seat>.ack.gen
    #     <gen>.json` so the NEXT generation (a fresh successor or a
    #     crash-recovery respawn at gen+1) starts with NO live ack. A stale
    #     predecessor `continue` left on disk is exactly what the gen-blind
    #     no-op (part (a)) used to mistake for THIS successor's answer; the
    #     rename makes that impossible by construction. F8's
    #     `seats/<seat>.ack.json` `answer` contract is unchanged — the
    #     rotated file is an ADDITIONAL name, never a changed shape.
    _rot = _rotate_ack_file(root, seat, gen)
    if _rot:
        if _rot.startswith("ack rotated:"):
            # (b) the record names the ack AS IT EXISTS at record time: the
            #     live `seats/<seat>.ack.json` is now `.ack.gen<N>.json`, so
            #     the SAME record's `ack_written` is rewritten to the rotated
            #     path (a reader following the record must not open a path
            #     that no longer exists) and the spawn-time value is preserved
            #     under `ack_written_at_spawn`. Naming only -- the ack SHAPE
            #     is untouched. The record file is rewritten in place (same
            #     path `_write_rotation_record` already opened).
            _spawn_ack = handover.get("ack_written")
            if (isinstance(_spawn_ack, str) and _spawn_ack
                    and not _spawn_ack.startswith("FAILED")):
                handover["ack_written_at_spawn"] = _spawn_ack
                handover["ack_written"] = str(_ack_path(root, seat)
                                               .with_name(
                                                   f"{seat}.ack.gen{gen}.json"))
                if record_path:
                    _rp = Path(record_path)
                    if _rp.exists():
                        _rec = json.loads(_rp.read_text(
                            encoding="utf-8", errors="replace"))
                        _rec["handover"] = handover
                        _write_rotation_record(root, _rec, path=record_path)
        print(_rot)

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
        # Director fix-ups at the SL1.07 harvest (sensei-director L2):
        # `{succ_ref}` is the ListAgents ref the successor NAMED in its ack
        # (read at (4)) when it did — the JOIN's succ_session_id is the
        # session uuid, not an address a peer can message; and a FIXTURE run
        # (window_path seam) has no live successor to wait on, so its delay
        # is 0 — the default 20 s sleep ran for real in five selfreap
        # fixtures (115 s of suite time) before this line.
        aj_values = _first_turn_values(
            root, seat=seat, gen=gen, succ_name=spawn_name,
            succ_ref=((ack or {}).get("session_ref") or succ_session_id
                      or ""),
            succ_transcript=succ_transcript or "",
            tmux_session=tmux_session)
        aj = run_after_join(
            root, seat=seat, gen=gen, startup=startup or {},
            values=aj_values, record_path=str(record_path),
            delay_override=(0 if getattr(args, "window_path", None)
                            is not None else None))
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
        live_names=succ.get("names", []),
        # mechanism 1: the address a peer can message is `name [ref]` where
        # ref is the successor's ListAgents ref — which arrives ONLY in its
        # ack (`ack --ref`, F8). The JOIN's succ_session_id is the Claude
        # session uuid from the registry file, a different identity (director
        # fix-up at the SL1.06 harvest, measured on rotation 172702Z: join
        # session_id 27179681-…, ListAgents ref caa927). So the announce
        # carries the ACK's ref, and NAMES pre-join when the ack had none.
        successor_ref=((ack or {}).get("session_ref") or ""),
        successor_window=succ_window_id or "")

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
        #
        # L4.281 (hypothesis:l4-rotate-self-under-pytest-reaps-the-host-prime):
        #   (a) under PYTEST_CURRENT_TEST with NO --own-chain seam the derive
        #       is REFUSED by name — a probe running inside the pytest runtime
        #       would otherwise climb from $TMUX_PANE up into ITS OWN host
        #       shell and TERM the prime above it (measured: a review
        #       subagent's scratchpad probe reaped the host claude, belam.log
        #       58240-58290, L4.155 provisioning-under-pytest mirror).
        #   (b) a DERIVED chain is TERM'd only when it holds the seat ROW's
        #       own pid (authority against the graph); a row with no pid or a
        #       mismatching pid is SKIPPED, named in the record and on stdout.
        #       The test SEAM path (--own-chain) is unchanged — an injectable
        #       stand-in is safe by construction.
        own_chain_seam = getattr(args, "own_chain", None)
        pytest_running = bool(os.environ.get("PYTEST_CURRENT_TEST"))
        src_name = None
        pane_pid = None
        if own_chain_seam:
            own_chain = [int(p) for p in own_chain_seam]
            reap_source = f"test seam (--own-chain): pid {own_chain[0]}"
        elif pytest_running:
            # (a) refuse the derive outright inside the pytest runtime.
            own_chain = []
            reap_source = (
                "REFUSED: PYTEST_CURRENT_TEST set with no --own-chain seam — "
                "the $TMUX_PANE / window-@id derive would reach a LIVE pane "
                "from inside the test runtime (L4.155 mirror; a probe reaped "
                "the host prime) — the live predecessor chain is reaped "
                "externally by PID (Belam cap / prime)")
        else:
            # production derive path (pytest absent):
            if own_window_id:
                pane_pid = _pane_pid(own_window_id)
                src_name = f"own window @id {own_window_id}"
            if pane_pid is None and os.environ.get("TMUX_PANE"):
                pane_pid = _pane_pid(os.environ.get("TMUX_PANE"))
                src_name = f"$TMUX_PANE {os.environ.get('TMUX_PANE')}"
            if pane_pid:
                own_chain = _derive_own_chain(pane_pid)
                if not own_chain:
                    own_chain = []
                    reap_source = (f"SKIPPED: own pid {os.getpid()} not under "
                                   f"pane pid {pane_pid} from {src_name}; no "
                                   "chain to TERM")
                else:
                    # (b) authority against the graph: TERM only when the
                    # derived chain holds the seat ROW's own pid.
                    derived = own_chain
                    row_pid = (row or {}).get("pid")
                    if row_pid is None:
                        own_chain = []
                        reap_source = (
                            f"SKIPPED: seat row {seat!r} carries no pid; "
                            f"derived chain {derived} NOT TERM'd (a row "
                            "without its own pid cannot authorize a reap)")
                    elif row_pid not in derived:
                        own_chain = []
                        reap_source = (
                            f"SKIPPED: seat row pid {row_pid} not in the "
                            f"derived chain {derived}; NOT TERM'd (a row "
                            "that does not own the chain cannot reap it)")
                    else:
                        reap_source = (f"derived from {src_name} pane "
                                       f"{pane_pid}: chain {derived} "
                                       "(deepest-first; authority row pid "
                                       f"{row_pid})")
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
            # The named seat's own copy (hypothesis:l4-a-seat-is-a-post-
            # everywhere): accept `.agi/worktrees/post-<seat>` beside the
            # deprecated `seat-<seat>`, reading whichever exists and
            # preferring post- when both are present.
            owned = wt_root / f"post-{seat}" / ".agi" / "sessions"
            if not owned.is_dir():
                owned = wt_root / f"seat-{seat}" / ".agi" / "sessions"
            if owned.is_dir():
                for d in sorted(owned.iterdir()):
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
                   "refs/heads")
    for ln in out.splitlines():
        branch = ln.strip()
        is_loop, season = _branch_loop(branch)
        if not is_loop or season is None:
            continue
        agent = _fd_agent_from_branch(branch)
        if not agent:
            continue
        mapping.setdefault(agent, (branch, season))
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

    The stat and kid list come from the round's OWN changeset: the commits on
    the round branch NOT reachable from `base_branch` (the ref the round was
    cut from — the season-resolved seat ref, else the manifest's
    base_branch). `git rev-list <round> ^<base>` names them newest-first; the
    diff runs from the OLDEST own commit's parent to the round tip
    (`<first_own>^..<round>`), so a multi-commit round (kid commit + parent
    `done:` commit, or a director fix-up on the branch) reports BOTH commits'
    files, and a round with NO own commits (a zero-commit round cut at the
    seat tip, or a round already merged into the base so every commit is
    reachable from it) reports `-` with an empty kid list — it never
    attributes the base's (seat's) commit to the round
    (hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits). A
    moved base tip never shifts the base; the rev-list exclusion re-derives
    the own commits against the base's current state.

    `resolved` True means git actually answered: both refs resolved and a
    rev-list ran. A resolvable-but-EMPTY own changeset (no own commits) still
    reports `resolved=True` with a `-` diff and empty kids — that is git's
    honest "the round added nothing of its own" answer, not a failure.
    `resolved` False means git could not answer at all (unknown branch or
    unresolvable base), which is the only situation the on-disk fallback may
    fire.
    """
    if not base_branch or base_branch.strip() == "-":
        return "-", [], False
    if not _git_out(main, "rev-parse", "--verify", "--quiet",
                    base_branch).strip():
        return "-", [], False
    if not _git_out(main, "rev-parse", "--verify", "--quiet",
                    round_branch).strip():
        return "-", [], False
    # The round's own commits, newest-first: everything on the round branch
    # not reachable from the base it was cut from. Empty means the round owns
    # nothing (zero-commit, or already merged into the base) — report `-`
    # rather than the base's / seat's commit.
    own = _git_out(main, "rev-list", round_branch,
                   f"^{base_branch}").splitlines()
    if not own:
        return "-", [], True
    first_own = own[-1]  # oldest own commit == the round's first step
    a = f"{first_own}^"
    stat = _git_out(main, "diff", "--stat", f"{a}..{round_branch}").strip()
    stat_s = stat.replace("\n", " | ") or "-"
    names = _git_out(main, "diff", "--name-only",
                     f"{a}..{round_branch}").splitlines()
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

    # The season for the `@s<N>` segment of the seat ref comes from the same
    # resolver dispatch.py uses — spawn_gate.read_ladder_season on the graph's
    # ladder (hypothesis:l4-harvest-table-attributes-only-the-rounds-own-
    # commits part (2): the `@s2` literal was hardcoded and drifted). Fail
    # open to the largest season stamped on the discovered loop branches (the
    # durable git fact) so a repo without a ladder still resolves; only if
    # neither yields a season is the seat ref skipped and the manifest's
    # base_branch taken instead.
    season: int | None = None
    try:
        import spawn_gate  # noqa: E402 -- local: same dir (lazy, dispatch uses it)
        season = spawn_gate.read_ladder_season(main / ".agi" / "nodes")
    except ImportError:
        season = None
    if season is None:
        seasons = {s for _, s in branches.values()}
        season = max(seasons) if seasons else None

    # The seat branch the claim names as the diff base, when --seat is given
    # and that ref exists (hypothesis:harvest-table-subcommand item (d)).
    # The seat ref named as the diff base, resolved to its ACTUAL spelling
    # (hypothesis:l4-a-seat-is-a-post-everywhere): post/<seat>@s<n> first,
    # then the canonical season<n>/posts/<seat>, then the deprecated
    # seat/<seat>@s<n> alias.
    seat_base = ""
    if want_seat and season:
        for cand in (f"post/{want_seat}@s{season}",
                     f"season{season}/posts/{want_seat}",
                     f"seat/{want_seat}@s{season}"):
            if _git_out(main, "rev-parse", "--verify", "--quiet",
                        cand).strip():
                seat_base = cand
                break

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
    p_meter.add_argument("--seat", "--post", action=geometry_config.SeatAction, default=None,
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
    p_spawn.add_argument("--seat", "--post", action=geometry_config.SeatAction, default=None,
                        help="seat successor identity; when given, AGI_SEAT=<name> "
                             "is exported before the claude argv so the SessionStart "
                             "hook copy can fire at turn one. Absent -> launch line "
                             "byte-identical to a plain spawn (owed item v)")
    p_spawn.add_argument("--tmux-session", default=DEFAULT_TMUX_SESSION,
                        help="tmux session to create the window in "
                             f"(default: {DEFAULT_TMUX_SESSION})")
    p_spawn.add_argument("--window-path", default=None,
                        help="read existing tmux window names from this file "
                             "instead of calling tmux (tests)")
    p_spawn.add_argument("--pid", type=int, default=None,
                        help="predecessor pid for the recovery autopsy (else "
                             "the seat row's pid)")
    p_spawn.add_argument("--no-autopsy", action="store_true",
                        help="skip the predecessor-autopsy block a recovery "
                             "seating otherwise appends to `[seating]` "
                             "(hypothesis:l4-a-recovery-seating-gets-its-"
                             "predecessor-autopsy-pre-filled-from-files)")
    p_spawn.add_argument("--ask-diff", "--successor-diff",
                        action="store_true",
                        help="the first-seating writer leaves `diff-requested` "
                             "and the seating alert prints the exact "
                             "`rotate.py ack --seat S --gen 1 --ref <ref> "
                             "diff --text -` line (SL7.06's answer contract, "
                             "reused never a third shape); default answers "
                             "`continue, source: seating` so the post wakes at 0")
    p_spawn.add_argument("--dry-run", action="store_true",
                        help="print the command instead of running it")
    p_spawn.set_defaults(func=cmd_spawn)

    # autopsy: the recovery seating's predecessor-death forensics, from FILES
    # ONLY, read-only. Prints the fact block the successor otherwise rebuilds
    # by hand (Sensei 175816Z calls 3-9+14); the LLM still decides continue|diff.
    p_ap = sub.add_parser(
        "autopsy",
        help="print a predecessor seat's death forensics from files only "
             "(read-only; never decides/kills/merges)")
    p_ap.add_argument("--seat", "--post", action=geometry_config.SeatAction, required=True, help="seat name")
    p_ap.add_argument("--pid", type=int, default=None,
                      help="predecessor pid (default: the seat row's pid)")
    p_ap.add_argument("--registry-dir", default=None,
                      help="per-session registry dir to read the predecessor's "
                           "<pid>.json from (default: ~/.claude/sessions) — tests")
    p_ap.add_argument("--root", default=None,
                      help="project root override (default: resolve from cwd)")
    p_ap.set_defaults(func=cmd_autopsy)

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
    p_loop.add_argument("--seat", "--post", action=geometry_config.SeatAction, default=None,
                        help="seat successor identity; when given, AGI_SEAT=<name> "
                             "is exported before the claude argv so the SessionStart "
                             "hook copy can fire at turn one. Absent -> launch line "
                             "byte-identical to today (owed item v)")
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
    p_ack.add_argument("--seat", "--post", action=geometry_config.SeatAction, required=True,
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
    # L4.288 (the stale-pid hazard, FIX-ONLY): the test seam + the registry
    # source for the ack-path identity JOIN. Same option spawn/loop take; the
    # ack resolves the successor's OWN row by the JOIN keyed on the row's
    # `window` @id, from HERE, never from ~/.claude/sessions under test.
    p_ack.add_argument("--registry-dir", default=None,
                       help="per-session registry dir for the own-row identity "
                            "JOIN (default: ~/.claude/sessions)")
    p_ack.add_argument("--no-commit", action="store_true", dest="no_commit",
                       help="write + print the back-fill but do NOT commit "
                            "the seat row even on a committing answer - the "
                            "three answers commit as: continue commits; diff "
                            "with empty text commits; diff with text never "
                            "commits")
    # g15.24 belt fallback (2c): when the own-row dirty gate refuses, re-poll
    # the gate every 5 s up to N s before the exit-3 refusal. --wait 0 (the
    # default) behaves exactly as today.
    p_ack.add_argument("--wait", type=int, default=0,
                       help="when the own-row dirty gate refuses, re-poll it "
                            "every 5 s up to N s before the exit-3 refusal "
                            "(default: 0 = no re-poll)")
    p_ack.set_defaults(func=cmd_ack)

    # status
    p_status = sub.add_parser(
        "status", help="list agi-master and belam tmux sessions")
    p_status.add_argument("--seats", action="store_true",
                          help="list registry seats instead (seat/generation/"
                               "fraction/age, one line per row)")
    p_status.add_argument("--seat", "--post", action=geometry_config.SeatAction, default=None,
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
    p_ht.add_argument("--seat", "--post", action=geometry_config.SeatAction, default=None,
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
    p_next.add_argument("--seat", "--post", action=geometry_config.SeatAction, required=True, help="seat name")
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

    # handoff --driven: the STEP 1 driven handoff card writer (goal:g15.14).
    # Builds §0 from measured values, asks the LLM ONLY for §3/§6.
    p_h = sub.add_parser(
        "handoff", help="driven handoff card writer: build §0 of the seat's "
                          "quorum card from measured values, ask the LLM only "
                          "for §3 where-it-stops and §6 banked "
                         "(hypothesis:l4-rotate-self-drives-the-handoff-and-"
                         "prepares-the-spawn)")
    p_h.add_argument("--driven", action="store_true",
                     help="driven mode: build §0, prompt for §3/§6 (the only "
                          "mode that exists today)")
    p_h.add_argument("--seat", "--post", action=geometry_config.SeatAction, default=None, help="seat name")
    p_h.add_argument("--field", action="append", nargs=2, metavar=("FIELD", "SRC"),
                     help="field value source; FIELD is s3 or s6, SRC is a "
                          "filename or `-` for stdin (repeatable)")
    p_h.add_argument("--dry-run", dest="dry_run", action="store_true",
                     help="compose the card and print it to stdout but write "
                          "nothing, so the director judges before the real "
                          "write")
    p_h.set_defaults(func=cmd_handoff)

    # prepare: the captive rotate-out checklist (goal:g15.14 STEP 2).
    p_pr = sub.add_parser(
        "prepare", help="print the captive rotate-out checklist: one line per "
                          "check with the ONE command that clears it; exit 0 "
                          "when nothing blocks, exit 3 otherwise "
                         "(hypothesis:l4-rotate-self-drives-the-handoff-and-"
                         "prepares-the-spawn)")
    p_pr.add_argument("--seat", "--post", action=geometry_config.SeatAction, default="",
                      help="seat name (a seat-bound checklist: card path, "
                           "meter pin, ack file)")
    p_pr.add_argument("--perform", action="store_true",
                      help="PERFORM check 3 (the only-behind season merge) "
                           "when it is mechanical: tree clean and the merge "
                           "applies with zero conflicts. A merge with any "
                           "conflict stays a BLOCK for the LLM to judge. "
                           "OFF (listing only) by default for bare `prepare`; "
                           "rotate-self's own gate defaults it ON.")
    p_pr.set_defaults(func=cmd_prepare)


    # first-decision --seat S: the point's CAPTIVE harvest-or-cut
    # (hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps,
    # step 4). Pre-fills the harvest row for each OPEN round, prints ONE
    # bounded prompt per row, and (--answers) prints the named next command.
    # PRINT ONLY — the merge/dispatch are never run.
    p_fd = sub.add_parser(
        "first-decision", help="the point's captive harvest-or-cut: print "
                                "the pre-filled row + ONE bounded prompt per "
                                "open round; --answers replays the choice "
                                "into the named next command (never run)")
    p_fd.add_argument("--seat", "--post", action=geometry_config.SeatAction, required=True, help="seat name")
    p_fd.add_argument("--answers", default=None,
                      help="file of choices, one per open round in table "
                           "order: 'harvest <branch>' | 'cut <node-id>' | "
                           "'hold'")
    p_fd.add_argument("--root", default=None,
                      help="project root override (default: resolve from cwd)")
    p_fd.set_defaults(func=cmd_first_decision)

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
    # (hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-
    #  hands-the-successor-exactly-one-call, --ask-diff leg): by default the
    # predecessor pre-answers the successor's ack channel itself; WITH this
    # flag it instead writes `answer: diff-requested, source: predecessor` and
    # hands the successor EXACTLY ONE wake call -- `rotate.py ack ... diff
    # --text -` -- so the rotation halts for handoff inspection exactly as a
    # manual `diff` does today.
    p_rs.add_argument("--ask-diff", "--successor-diff",
                      nargs="?", const=True, default=False,
                      help="write the ack as `diff-requested` (source: "
                           "predecessor) and hand the successor exactly one "
                           "diff call, instead of pre-answering `pending`; "
                           "a value (`--ask-diff '<gap>'`) is ALSO written "
                           "into the stops section as `diff requested: "
                           "<gap>` when `--stops` accompanies it")
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
    p_rs.add_argument("--prepare", action="store_true",
                      help="print the captive rotate-out checklist and exit "
                           "(0 clear / 3 blocked) without rotating -- the "
                           "same `_prepare_checks` rotate-self refuses on "
                           "(goal:g15.14 STEP 2)")
    p_rs.add_argument("--comms-root", default=None,
                      help="override the comms dir the rotation announcement "
                           "is delivered to (default: send.py's comms_root)")
    p_rs.add_argument("--trigger", default="rotate-self",
                      help="spell the rotation's trigger in the announcement "
                           "(meter due / --force / fable-limit)")
    p_rs.add_argument("--in-flight", default=None,
                      help="one line of what is in flight, for peers to know "
                           "if their round is orphaned")
    # goal:g15.25 line (3) -- the rotate-OUT is ONE call. `--stops 'text'`
    # (or `--stops-file F`; `--stops -` reads stdin) writes <text> as the
    # body of the seat's own card's `### 🔴 Where it stops` section, and the
    # ONE rotate-out commit (card + the seat's own seats.md row, nothing
    # else) + push + the rotation line all happen INSIDE rotate-self -- the
    # post's out-count is ONE call, no separate send.py.
    p_rs.add_argument("--stops", default=None,
                      help="what the seat leaves behind: written into the '"
                           "seat's own card's `### 🔴 Where it stops` section "
                           "at rotate-out (`-` reads stdin); commits it with "
                           "the seat's own seats.md row in ONE pathspec "
                           "commit and pushes")
    p_rs.add_argument("--stops-file", default=None,
                      help="read the stops text from FILE instead of "
                           "--stops (mutually the rotate-out stops write)")
    p_rs.set_defaults(func=cmd_rotate_self)

    # bootstrap-block: the SessionStart hook's reader — emit the successor's
    # bootstrap record as ONE injected block, or REFUSE (exit 1, silent).
    p_bb = sub.add_parser(
        "bootstrap-block", help="emit the bootstrap block for a seat "
                                 "successor, or REFUSE when absent/malformed "
                                 "(a stale fact is MARKED stale, still emitted)")
    p_bb.add_argument("--seat", "--post", action=geometry_config.SeatAction, required=True, help="seat name")
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

    # launch-wrapper: signal-masking parent so a seat's lifecycle log
    # distinguishes self-teardown from TERM'd-from-outside from window-killed
    # (hypothesis:l4-rotate-self-under-pytest-reaps-the-host-prime, amendment e)
    p_lw = sub.add_parser(
        "launch-wrapper", help="signal-masking parent that wraps a seat's "
                               "claude argv and logs every process-sent "
                               "TERM/HUP/INT with its sender pid")
    p_lw.add_argument("--seat", "--post", action=geometry_config.SeatAction, required=True,
                      help="seat name (log attribution + default log path)")
    p_lw.add_argument("--log", default=None,
                      help="append wrapper lifecycle lines here (default: "
                           "<sessions>/seats/<seat>.wrapper.log)")
    p_lw.add_argument("--root", default=None,
                      help="project root for the default log path (test seam; "
                           "else find_project_root at run time)")
    p_lw.add_argument("child", nargs=argparse.REMAINDER,
                      help="the wrapped argv after -- (e.g. `-- claude "
                           "--remote-control <name> <prompt>`)")
    p_lw.set_defaults(func=cmd_launch_wrapper)

    args = ap.parse_args(argv)

    # complete works purely from its explicit paths + git; no project root.
    if args.cmd == "complete":
        return args.func(args, None)

    # launch-wrapper resolves its own log path at run time (root=None triggers
    # find_project_root inside); no project root required up front.
    if args.cmd == "launch-wrapper":
        return args.func(args, getattr(args, "root", None))

    # meter, loop, alarms, rotate-self, ack and seats-launch need the project root
    if args.cmd in ("meter", "loop", "alarms", "rotate-self", "ack",
                    "next", "seats-launch", "seq", "handoff", "prepare",
                    "first-decision", "autopsy"):
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