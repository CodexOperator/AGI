#!/usr/bin/env python3
"""dispatch.py — spawn N pi agents in parallel with zoom-targeted contexts.

Reads <project>/agi-tree.config.json for parallelism + model.
Writes session manifest at <project>/sessions/iter-NNN/manifest.json (or
iter-L1.08 for a loop-scoped id; `locations.iteration_dir` spells both) so
heal.py can detect timeouts. This script never picks an iteration id -- the
caller allocates one (`driver.sh` via `locations.py --claim-iter`).

Each agent gets:
- zoom context file (built by zoom.py)
- skill manifest pointer (agi)
- completion-CLI instruction

The pi processes run detached; this script returns once they're spawned.
Caller (driver.sh) polls heal.py to monitor + heal.

Usage:
    dispatch.py <project_root> <iter_n>
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import random
import shlex
import subprocess
import sys
import tempfile
import time
import uuid
from contextlib import contextmanager
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent  # extensions/agi
ZOOM_PY = PLUGIN_ROOT / "bin" / "zoom.py"
CLI_PY = PLUGIN_ROOT / "bin" / "cli.py"

# goal:s17 -- the one node-writing routine, reached the same way `cli.py` and
# `post_wire.py` reach it. dispatch.py used to carry its own un-gated copy.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import adapters  # noqa: E402
import locations  # noqa: E402
import spawn_gate  # noqa: E402  -- read_ladder_season (L2.06 stamps used it without importing it)
import node_writer  # noqa: E402
import provisioning  # noqa: E402
import spawn_budget  # noqa: E402
import stall_detect  # noqa: E402 -- hyp:l4-stalled-is-a-state-the-harness-can-see (record, don't repair)
from spawn_budget import TERMINAL  # noqa: E402 -- the ONE terminal-status set (hyp:l4-one-definition-of-terminal)

#: goal:g11.1 — re-exported from `locations` rather than redefined.
config_path = locations.config_path


# Env vars Claude Code injects so its own agent can use the user's Anthropic
# subscription (Token Plan). If pi inherits these, every spawned subagent
# silently consumes that same quota and competes with the interactive CC
# session for it. Scrub them so pi falls back to its own configured provider
# (typically minimax via ~/.pi/agent/settings.json).
ENV_VARS_TO_SCRUB = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_MODEL",
    "CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC",
    "CLAUDE_CODE_EMIT_TOOL_USE_SUMMARIES",
    "CLAUDE_CODE_ENABLE_ASK_USER_QUESTION_TOOL",
    "CLAUDE_CODE_DISABLE_CRON",
    "CLAUDE_AGENT_SDK_VERSION",
    "CLAUDECODE",
    # goal:g1.11 -- the key that MINTS keys is never handed to a child. A kid
    # holding it could mint uncapped keys or revoke the ones the run depends
    # on, which is strictly worse than the subscription leak the names above
    # close. Same mechanism, one more name.
    provisioning.PROVISIONING_KEY_VAR,
)


def scrubbed_env() -> dict[str, str]:
    """Inherited env minus Claude-Code-injected Anthropic credentials.

    Public because `heal.py` spawns pi too and was spawning it with the raw
    inherited environment — the exact leak this function exists to close, on
    the one path that only runs when something has already gone wrong. One
    definition, both spawners.
    """
    env = {k: v for k, v in os.environ.items() if k not in ENV_VARS_TO_SCRUB}
    return env


#: Legacy private name. Kept so nothing that already imported it breaks.
_scrubbed_env = scrubbed_env


def _resolved_seat(args_seat: str | None) -> str | None:
    """The AGI_SEAT value to export, or None to leave the key absent.

    Precedence (hypothesis:l4-dispatch-exports-seat): `--seat` WINS when
    given; an AGI_SEAT already in the inherited env SURVIVES when `--seat`
    is absent; neither present means the key is absent -- never a
    placeholder, never a fallback to the ladder name.
    """
    if args_seat:
        return args_seat
    return os.environ.get("AGI_SEAT")


# --- secret redaction for the debugger's spawn.json (hypothesis:l4-dispatch-
# echoes-less-than-it-knows) ---------------------------------------------
# Redaction is by NAME pattern (KEY, TOKEN, SECRET, PASSWORD) AND by VALUE
# shape (sk- and sk-or-v1- prefixes), both, so a value-shaped secret in an
# unnamed var is caught by the shape half, not just the name half. A value
# is never printed in full, in part, or as a prefix on dispatch's stdout or
# in spawn.json -- only as "..." + its last 4 characters, enough to
# recognize one's own key without carrying a doxable fragment.
_SECRET_NAME_PATTERNS = ("KEY", "TOKEN", "SECRET", "PASSWORD")


def _redact_secret_value(value: str) -> str:
    """'...' + last 4 chars, or a fixed marker for a shorter value."""
    if len(value) <= 4:
        return "<redacted>"
    return "..." + value[-4:]


def _looks_like_secret(name: str, value: str) -> bool:
    """Secret by name pattern (KEY/TOKEN/SECRET/PASSWORD) or value shape."""
    upper = str(name).upper()
    if any(p in upper for p in _SECRET_NAME_PATTERNS):
        return True
    v = str(value)
    return v.startswith("sk-") or v.startswith("sk-or-v1-")


def _redact_env_map(env: dict) -> dict:
    """A copy of `env` with every secret's VALUE replaced by its tail-4 form.

    Key names survive (a debugger must know which var WAS set); only values
    are redacted. Used for spawn.json only -- the child's real env is
    untouched.
    """
    out = {}
    for k, v in env.items():
        out[k] = _redact_secret_value(str(v)) if _looks_like_secret(k, v) else v
    return out


def zoom_command(root: Path, iter_n: int, agent_id: str,
                 level: str, target: str | None, push_further: bool = False) -> list[str]:
    """The `zoom.py` invocation for one kid's context bundle.

    **`--runtime pi` is explicit and must stay that way (goal:s8).** Without it
    zoom.py falls back to `default_runtime()`, which answers `"cc"` for any
    project whose config carries a `cc_dispatch` block — and a project can
    carry both, because the two runtimes are alternatives, not exclusive
    states. This project does, so every pi kid was handed the CC contract:
    *"Do not call cli.py"*, in the one runtime where `cli.py done` is how the
    manifest closes. Both kids on the 2026-08-31 live run reported the
    contradiction and, correctly, ignored their own context file.

    The process doing the dispatching knows which runtime it is. A config key
    never can.
    """
    cmd = ["python3", str(ZOOM_PY), str(root), str(iter_n), agent_id,
           "--level", level, "--runtime", "pi"]
    if level == "small" and target:
        cmd.extend(["--target", target])
    if push_further:
        # hypothesis:l3w4-push-further-loops — re-dispatch at the SAME target
        # id so a continuation kid composes from the parent's push_further
        # text and stamps `pushed_from: <target>` (see _scaffold_node_for_agent).
        cmd.append("--push-further")
    return cmd


# hypothesis:l3w4-parent-branch-merge-up — per-parent git worktree on a
# `loop/<slug>-<agent8>@s<N>` branch. The four helpers below are the
# dispatch side of the claim: `--branch` cuts each spawn its own worktree
# OFF THE SPAWNER'S checked-out branch (ADDENDUM items 1 & 3), the worktree
# lives under the MAIN checkout's `.agi/worktrees/<agent>/` resolved through
# `locations.git_common_root` (ADDENDUM item 4, so a spawner running inside a
# worktree never nests one agent's tree inside another's), and the lease /
# agent record carries `branch`/`base_branch`/`worktree` so `season.py
# merge-up` knows which base to climb into (item 2).


def spawner_base_branch(workdir: Path) -> str | None:
    """The branch the SPAWNER is ON — the base of any branch it cuts.

    ADDENDUM item 1: the base of a new branch is the spawner's checked-out
    branch (`git rev-parse --abbrev-ref HEAD` in the spawner's cwd), never a
    hardcoded `season/sN`. A director on `tier1/<name>` cuts its parents from
    `tier1/<name>`, an advisor cuts directors from its own branch, and only
    the prime's layer cuts from `season/sN`. Returns None when git is broken
    or the HEAD is detached (nothing to base a child branch on).
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(workdir), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    name = out.stdout.strip()
    # On a detached HEAD `--abbrev-ref HEAD` prints the literal "HEAD" —
    # there is no branch to base a child on, which is exactly the case the
    # helper exists to detect for the caller.
    if not name or name == "HEAD":
        return None
    return name


# hypothesis:l4-a-round-is-cut-from-the-branch-you-are-on — HALF A: the
# freshness guard. A round cut with `--branch` is only as fresh as the branch
# it is cut FROM, and dispatch never said when that base is stale: a seat that
# has not synced to the integration branch (`season/sN`) since other seats
# landed work spawns a round against stale code, and nothing told the
# dispatcher (measured: the L4.122 helper dispatched 312 lines behind on
# provisioning.py). This guard MEASURES how far the spawner's HEAD is behind
# `origin/season/sN` and returns a structured record the caller emits and acts
# on. fail-OPEN on the network: an unreachable origin yields status
# "unchecked", never a false stale claim, so a spawn is never blocked on a
# remote being down.
_ENGINE_PATH_LEADS = ("extensions/", "skills/", "src/", "bin/", "hooks/")


def _is_engine_path(p: str) -> bool:
    """True when a changed path is engine source (not graph data)."""
    return p.startswith(_ENGINE_PATH_LEADS)


def _stale_base_spawn(root: Path, season: int) -> dict:
    """How far the spawner's HEAD is behind the integration branch.

    Returns one of:
      {"status": "current", "behind": 0, "files": []}
      {"status": "behind", "behind": N, "files": [engine files differing]}
      {"status": "unchecked", "behind": 0, "files": []}  (origin unreachable)

    Every git command is run captured and fail-open — the guard is a
    witness, not an authority — so a flaky tool or an unreachable remote
    degrades to current/unchecked rather than fabricating a stale read.
    The fetch is run first so `behind` is measured against what is actually
    on origin, not whatever the local ref last happened to see.
    """
    integration = f"origin/season/s{season}"
    try:
        fr = subprocess.run(
            ["git", "-C", str(root), "fetch", "origin",
             f"season/s{season}"],
            capture_output=True, text=True, timeout=60)
        if fr.returncode != 0:
            # A failed fetch means the remote tip is unknowable -> we cannot
            # call anyone stale on evidence. fail-open, per the claim.
            return {"status": "unchecked", "behind": 0, "files": []}
    except (subprocess.TimeoutExpired, OSError, subprocess.SubprocessError):
        return {"status": "unchecked", "behind": 0, "files": []}
    # Belt-and-suspenders: the stale claim must rest on a resolvable remote
    # ref, not on a fetch that printed success through a warning. If the
    # remote tip does not resolve, the gap is unknowable -> unchecked.
    try:
        rr = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--verify", "--quiet",
             f"{integration}^{{commit}}"],
            capture_output=True, text=True, timeout=30)
        if rr.returncode != 0 or not rr.stdout.strip():
            return {"status": "unchecked", "behind": 0, "files": []}
    except (subprocess.TimeoutExpired, OSError, subprocess.SubprocessError):
        return {"status": "unchecked", "behind": 0, "files": []}
    behind = 0
    try:
        cr = subprocess.run(
            ["git", "-C", str(root), "rev-list", "--count",
             f"HEAD..{integration}"],
            capture_output=True, text=True, timeout=30)
        if cr.returncode == 0 and cr.stdout.strip():
            behind = int(cr.stdout.strip())
    except (subprocess.TimeoutExpired, ValueError, OSError,
            subprocess.SubprocessError):
        behind = 0
    if behind <= 0:
        return {"status": "current", "behind": 0, "files": []}
    # Behind: name the engine files that differ so the message says WHAT is
    # stale, not just that *something* is. Three dots = merge base..remote tip
    # = exactly the work the spawner does not have.
    files: list[str] = []
    try:
        dr = subprocess.run(
            ["git", "-C", str(root), "diff", "--name-only",
             f"HEAD...{integration}"],
            capture_output=True, text=True, timeout=30)
        if dr.returncode == 0:
            files = sorted(f for f in dr.stdout.splitlines()
                           if _is_engine_path(f))
    except (subprocess.TimeoutExpired, OSError, subprocess.SubprocessError):
        files = []
    return {"status": "behind", "behind": behind, "files": files}


def _stale_base_record(stale: dict, season: int) -> dict:
    """The structured next-actions record emitted on a stale base (HALF A).

    Machine-readable so HALF B (hypothesis:l4-startup-is-one-script-or-a-
    driven-prompt) can DRIVE the pick without parsing prose: the issue, the
    gap, the differing engine files, and the enumerated resolving actions. A
    re-invocation carrying a resolution (a synced base, or
    `--allow-stale-base <reason>`) proceeds; the speaker here only EMITS.
    """
    return {
        "issue": "stale-base",
        "behind": stale.get("behind", 0),
        "files": stale.get("files", []),
        "integration": f"season/s{season}",
        "actions": [
            {"id": "sync", "cmd": f"git merge origin/season/s{season}"},
            {"id": "override", "cmd": "dispatch ... --allow-stale-base <reason>"},
            {"id": "abort"},
        ],
    }


def loop_branch_name(target: str | None, agent_id: str, season: int) -> str:
    """`loop/<slug>-<agent8>@s<N>` — the per-agent branch name.

    ADDENDUM item 3: the agent id rides in the branch name so nested layers
    never collide — a director, a parent and a kid each cut branches carrying
    their own id, and the `loop/` prefix keeps them off the tier branches
    (`tier<N>/<name>` stays reserved for directors/prime per HANDOFF §6 item
    7). The slug is the target's id with the `:` flattened, so a human can
    tell which aim the branch carries.
    """
    slug = (target or "explore").replace(":", "-")[:32]
    return f"loop/{slug}-{agent_id}@s{season}"


def branch_worktree_for_spawn(root: Path, branch: str, agent_id: str,
                              base_branch: str) -> Path:
    """`git worktree add <main>/.agi/worktrees/<agent> -b <branch> <base>`.

    ADDENDUM item 4: the worktree lives under the MAIN checkout's
    `.agi/worktrees/<agent>/`, resolved through `locations.git_common_root`,
    so a spawner that is ITSELF running inside a worktree does not land one
    agent's tree inside another's — the common git dir is always the main
    repo's `.git`. The base is the spawner's own branch (item 1), so merges
    climb one layer at a time. Returns the worktree checkout root. Raises
    RuntimeError naming the branch and base when the worktree cannot be
    created.
    """
    main = locations.git_common_root(root)  # main checkout, from any depth
    wt = main / ".agi" / "worktrees" / agent_id
    wt.parent.mkdir(parents=True, exist_ok=True)
    out = subprocess.run(
        ["git", "-C", str(main), "worktree", "add", "-b", branch,
         str(wt), base_branch],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"git worktree add -b {branch} from {base_branch}: "
                           f"{out.stderr.strip()}")
    return wt


def drop_branch_worktree(root: Path, worktree: Path) -> None:
    """Best-effort remove of a worktree created by `--branch` but never used.

    Called on every spawn-failure path after a worktree was cut, so a botched
    spawn does not leak a worktree and its branch. `git worktree remove` is
    issued from the MAIN checkout (`git_common_root`), never the worktree
    itself; `--force` discards whatever stray bytes landed in it before the
    abort. Any removal failure is swallowed — the seat's next `merge-up` /
    `worktree list` pass is the safety net, not this.
    """
    try:
        main = locations.git_common_root(root)
        subprocess.run(
            ["git", "-C", str(main), "worktree", "remove", "--force",
             str(worktree)],
            capture_output=True, text=True,
        )
    except (OSError, subprocess.SubprocessError):
        pass


def child_working_graph(*, passed_root: Path | None,
                        spawner_env_root: str | None) -> Path | None:
    """Re-root the child's working graph to the SPAWNER's worktree.

    `hypothesis:l3w4-parent-branch-merge-up` recursion fix. A parent spawned
    with `--branch` runs in its own git worktree (dispatch exports that
    worktree as `AGI_TREE_PROJECT_ROOT` to the child env), and when it spawns
    a KID (`--tier kid`, no `--branch`) the kid must INHERIT that worktree as
    its working tree — not walk back out to the main checkout, which is what
    resolving the kid's root from the passed project path alone used to do.
    L3.30 runtime rehearsal (Belam VII): both worktrees stood EMPTY while
    every kid's edits and session dirs landed in the main checkout, so
    `merge-up` would have merged two empty branches — a green result meaning
    the opposite of what it says.

    Only the tree the CHILD edits changes here. Shared state (spawn budget,
    comms root, meter pins) re-resolves to the main checkout through
    `git_common_root` in the callees that own it, so this never weakens the
    tree-wide concurrency bound (ADDENDUM item 4).
    """
    if passed_root is None:
        return passed_root
    if not spawner_env_root:
        return passed_root
    env_graph = locations.find_project_root(spawner_env_root) \
        or Path(spawner_env_root).resolve()
    if env_graph == passed_root:
        return passed_root
    return env_graph


def child_engine_paths(child_graph: Path | None) -> dict:
    """Re-root the child's ENGINE paths to its own checkout, not main's.

    `hypothesis:l3-branch-source-paths-never-rerooted`. dispatch.py re-roots
    the child GRAPH thoroughly (`child_working_graph`) but leaves
    `PLUGIN_ROOT`, `CLI_PY`, `skill_prompt` and `dispatch_py` as module
    constants derived from `Path(__file__)` of the dispatch.py that is
    RUNNING — which, under `--branch`, is the main checkout's dispatch.py. So
    a kid's argv carried a worktree node path beside main-absolute engine
    paths, and the model followed the only source anchor it was given: main.
    `locations.source_root` already computes exactly the checkout root this
    needs and was wired to nothing; it is the resolver for precisely this.

    The same four values are computed against the child's own source root and
    returned, falling back per-path to the module constants when a candidate
    does not exist — a non-agi project's source tree has no engine, and its
    kid must keep using the engine that spawned it. Call once `child_graph`
    is settled (on BOTH the `--branch` and the plain spawn), and pass the
    returned values at the `build_command` site.
    """

    def _fallback() -> dict:
        return {
            "source_root": PLUGIN_ROOT,
            "cli_py": CLI_PY,
            "skill_prompt": PLUGIN_ROOT / "lib" / "agent-prompt.md",
            "dispatch_py": Path(__file__).resolve(),
        }

    if child_graph is None:
        return _fallback()
    try:
        src = locations.source_root(child_graph)
    except Exception:
        src = None
    if src is None:
        return _fallback()

    out = _fallback()
    out["source_root"] = src
    # The engine layout inside an agi-project checkout: <src>/extensions/agi.
    _candidates = {
        "cli_py": ("extensions", "agi", "bin", "cli.py"),
        "skill_prompt": ("extensions", "agi", "lib", "agent-prompt.md"),
        "dispatch_py": ("extensions", "agi", "bin", "dispatch.py"),
    }
    for key, rel in _candidates.items():
        candidate = Path(src, *rel)
        if candidate.exists():
            out[key] = candidate
    return out


def pi_model_args(cfg: dict, tier: str = "kid") -> list[str]:
    """LEGACY SHIM — the pi flags now live in `adapters/pi_adapter.py`.

    Kept, and kept working, for two callers outside `goal:g4.6`'s scope:
    `heal.py` imports it by name, and `tests/test_dispatch.py` asserts on it.
    Same rule this file already applies to `scrubbed_env` and this project
    applies to legacy config names — a public name other code imports is a
    compatibility surface, so it delegates rather than disappearing.

    **This is not the live path.** `main()` resolves a harness from config and
    calls that adapter's `build_command`, so no spawn goes through here.
    """
    _name, harness = adapters.resolve(cfg)
    return adapters.load(harness["adapter"]).model_args(harness, tier)


@contextmanager
def _manifest_lock(iter_dir: Path):
    """Hold an exclusive flock for the whole read-merge-write cycle.

    `goal:s28` made the manifest write a *merge* so a parent's own entry
    survives its kid's dispatch into the same iteration. `goal:g4.8` needs
    that merge to survive **concurrency**, which it did not: the cycle read
    the manifest, spawned, then wrote, and two dispatches overlapping in that
    window each wrote a manifest built from the same stale read. The rename
    was atomic; the cycle around it was not, and atomicity of the last step
    was mistaken for atomicity of the operation.

    Measured 2026-09-02, before the fix, 8 concurrent dispatches x 6 runs:
    **6/6 runs lost entries, typically 6-7 of 8.** A lost entry is a spawned
    agent nothing tracks — `heal.py` cannot time it out and `post_wire`
    cannot wire its node, which is `goal:g7`'s invariant (nothing the loop
    produces is silently lost) failing at the point of spawn.

    The lock file is never deleted. Unlinking it would let one process hold a
    lock on an inode another has already replaced, which is the same class of
    bug one layer down.
    """
    iter_dir.mkdir(parents=True, exist_ok=True)
    lock_path = iter_dir / ".manifest.lock"
    fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def _merge_manifest(iter_dir: Path, base: dict, new_records: list[dict],
                    unadmitted: list[dict] | None = None) -> dict:
    """Re-read the manifest under lock, merge `new_records` by id, write it.

    The re-read is the fix, not the lock alone: this invocation's own view of
    `agents` is stale by the time its processes are spawned, so the entries
    written are merged against whatever is on disk *now* rather than against
    what was there when the run started. Merge is by agent `id`, so a
    re-dispatch (healing) updates in place instead of duplicating — the
    behaviour `goal:s28` established, now applied to the authoritative copy.

    `unadmitted` is merged the same way and into its own list (`goal:g4.8`).
    It is kept apart from `agents` deliberately: an unadmitted slot has no pid
    and no process, so anything that polls `agents` for liveness — `heal.py`,
    `_reaper_phase` — must not find it there and go looking for a corpse that
    was never born.
    """
    manifest_path = iter_dir / "manifest.json"
    with _manifest_lock(iter_dir):
        merged = dict(base)
        agents: list[dict] = []
        prior_unadmitted: list[dict] = []
        if manifest_path.exists():
            try:
                old = json.loads(manifest_path.read_text())
                agents = old.get("agents", [])
                prior_unadmitted = old.get("unadmitted", [])
                merged["started_at"] = old.get("started_at", merged.get("started_at"))
            except (json.JSONDecodeError, OSError):
                print(f"warn: corrupt manifest at {manifest_path}, starting fresh",
                      file=sys.stderr)
                agents = []
                prior_unadmitted = []
        by_id = {a.get("id"): i for i, a in enumerate(agents) if a.get("id")}
        for rec in new_records:
            idx = by_id.get(rec.get("id"))
            if idx is None:
                by_id[rec.get("id")] = len(agents)
                agents.append(rec)
            else:
                agents[idx] = rec
        merged["agents"] = agents

        skipped = list(prior_unadmitted)
        skipped_by_id = {a.get("id"): i for i, a in enumerate(skipped) if a.get("id")}
        for rec in unadmitted or []:
            idx = skipped_by_id.get(rec.get("id"))
            if idx is None:
                skipped_by_id[rec.get("id")] = len(skipped)
                skipped.append(rec)
            else:
                skipped[idx] = rec
        merged["unadmitted"] = skipped
        # A unique temp name in the same directory. The previous fixed
        # `.manifest.json.tmp` was shared, so one dispatch renamed the file
        # out from under another and the loser died with FileNotFoundError --
        # after `Popen` had already run, which is the spawned-but-untracked
        # agent this whole function exists to prevent.
        fd, tmp_name = tempfile.mkstemp(dir=str(iter_dir), prefix=".manifest.json.",
                                        suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as fh:
                json.dump(merged, fh, indent=2)
            os.replace(tmp_name, manifest_path)
        except BaseException:
            Path(tmp_name).unlink(missing_ok=True)
            raise
    return merged


# hypothesis:l3w0-ladder-roles-table — (tier, role) -> spawn spec.
#
# The ladder node's `roles:` table maps a (tier, role) row to
# harness / model / effort / settings. A declared row wins outright;
# config `harnesses.<h>.models[role]` is the historical fallback and stays
# exactly as it was when the table has no row. `--list-rows` resolves every
# declared row and prints it without spawning anything — the dry-proof this
# hypothesis's VERIFY asks for.


def _default_role_for_tier(tier: str) -> str:
    """hypothesis:l3-dispatch-role-default — the ladder role a spawn
    defaults to when `--role` is not given.

    The bug this closes: `--role` defaulted to ``kid`` whatever `--tier`
    said, so a director's bare `--tier parent` spawn resolved the tier-0
    kid row and loaded the deepseek kid model instead of the parent model.
    Tier and role are the same ladder column in the roles table (a row is
    keyed by both), so the default role is the spawn tier itself. An
    explicit `--role` still wins over this in `main()`.
    """
    return tier or "kid"


def _default_tier_for_role(role: str) -> int:
    """The ladder tier a role lives at when `--ladder-tier` is not given.

    Ties are not ambiguous because a role has a canonical home: kids and the
    tier-0 directors/parents sit at 0, tier-1 directors/parents at 1, and
    the prime director (with its parents) at 3. The L3 shape declares no
    tier-2 rows (the advisors embody the visions, §1.9 of the command
    ladder brief), so `director`/`parent` default to 1, not 2.
    """
    return {"kid": 0, "parent": 1, "director": 1, "prime_director": 3}.get(
        role, 0)


def _brief_tier_for(tier: str, ladder_tier: int, target: str | None) -> str:
    """Route a tier-3 parent spawn aimed at a vision node to the advisor brief.

    `hypothesis:l3w3-advisor-brief` — the three advisors ARE the tier-3
    parents (claude-code, opus 5, effort max, ultracode), each embodying one
    vision. `dispatch.py --tier parent --ladder-tier 3 --target vision:<id>`
    used to assemble the generic parent brief, so an advisor sent out with
    the parent's job description would never sit the tier3-quorum or spawn
    its perpetual-goal director. When the spawn tier is parent, the ladder
    tier is 3 AND the target names a vision node, the BRIEF tier becomes
    `advisor` even though the model/role still resolve as parent (threaded
    through the adapter's `brief_tier`).
    """
    if (tier == "parent" and int(ladder_tier) == 3
            and target and target.startswith("vision:")):
        return "advisor"
    return tier


def _assert_allowed_model(harness_name: str, harness: dict,
                        model: str | None) -> None:
    """FAIL CLOSED on `allowed_models` (hypothesis:l4-dispatch-model-allowlist).

    The harness's `allowed_models` list is the ONLY census a harness may spawn
    from. An ABSENT or EMPTY list refuses EVERY model -- it never means 'allow
    everything', because a default that opens on absence is a gate that
    disappears exactly when someone deletes it. A model that is not in the list
    is refused by name (model, harness, list). A tier with no resolved model
    exports no AGI_MODEL at all, so there is nothing to allow or refuse.

    Placed at the one value every consumer reads -- the effective model is
    fixed before this call and the live env, the dry-run env mirror and the
    agent record all read that same value -- so one refusal here is a refusal
    at all four check sites without four copies of the rule.
    """
    if not model:
        return
    allowed = harness.get("allowed_models")
    if not allowed:
        raise adapters.AdapterError(
            f"model {model!r} refused for harness {harness_name!r}: "
            f"`allowed_models` is absent or empty, and the allowlist gate "
            f"fails closed -- every model is refused when the list is missing "
            f"or cleared (hypothesis:l4-dispatch-model-allowlist)")
    if str(model) not in {str(m) for m in allowed}:
        raise adapters.AdapterError(
            f"model {model!r} is not in harness {harness_name!r} "
            f"allowed_models {list(allowed)} -- refusing to spawn "
            f"(hypothesis:l4-dispatch-model-allowlist)")


def resolve_role_spec(cfg: dict, roles: list | None, tier: int,
                      role: str) -> dict:
    """Resolve (tier, role) to {harness, model, effort, settings, from_ladder}.

    A row in `roles` matching both keys wins; its empty/short cells resolve
    to None (no flag). With no row (or no table at all) the historical
    config path answers: `harness` from `adapters.resolve`, `model` from
    `harnesses.<h>.models[role]`, `effort` from `harnesses.<h>.effort[role]`.
    `from_ladder` distinguishes the source so callers can report it.
    """
    # hypothesis:l4-a-model-change-is-one-write — the ladder `roles:` table is
    # the ONE source of a role's model/effort/settings. The row lookup and the
    # blank-cell -> None mapping live in adapters/ (the shared resolver
    # dispatch.py, workflow.py and heal.py import), so one write.py on the
    # ladder IS the model write.
    row = adapters.ladder_role_row(roles, tier, role)
    if row is not None:
        _spec = adapters.spec_from_ladder_row(row)
        _spec["from_ladder"] = True
        return _spec
    _name, harness = adapters.resolve(cfg)
    models = harness.get("models") or {}
    model = models.get(role) if isinstance(models, dict) else None
    effort = harness.get("effort")
    if isinstance(effort, dict):
        effort = effort.get(role)
    if not isinstance(model, str) or not model.strip():
        model = None
    if not isinstance(effort, str) or not effort.strip():
        effort = None
    return {
        "harness": _name,
        "model": model,
        "effort": effort,
        # hypothesis:l3w4-director-kids-on-glm — no config fallback for
        # thinking: it is a ladder/seat cell, never a global default.
        "thinking": None,
        "settings": None,
        "from_ladder": False,
    }


def resolve_seat_spec(seats: list | None, name: str) -> dict | None:
    """Resolve one seat row by NAME to {harness, model, effort, settings}.

    hypothesis:l3w4-seat-registry. A seat's own cells override the ladder's
    (tier, role) class table -- that is how the liaison diverges from the
    director class (sonnet/high, not opus/max) while staying privileged as a
    director on tier 1. Returns None when the registry is absent or has no
    row for `name`, which fails open to the (tier, role) ladder lookup.
    """
    for r in (seats or []):
        if r.get("name") != name:
            continue
        return {
            "harness": r.get("harness") or None,
            "model": (r.get("model") or "").strip() or None,
            "effort": (r.get("effort") or "").strip() or None,
            # hypothesis:l3w4-director-kids-on-glm — a seat may dial its own
            # reasoning effort, so a GLM seat is told to think high.
            "thinking": (r.get("thinking") or "").strip() or None,
            "settings": r.get("settings") or None,
            "from_seat": True,
        }
    return None


def _compile_role_rows(roles: list | None) -> list[tuple[int, str, dict]]:
    """Resolve every declared row -> (tier, role, spec), in declaration order.

    The shared body behind `--list-rows` and its test; printing is the only
    thing `main` adds on top.
    """
    out: list[tuple[int, str, dict]] = []
    for r in (roles or []):
        try:
            tier = int(r.get("tier"))
        except (TypeError, ValueError):
            continue
        role = r.get("role")
        if not isinstance(role, str) or not role.strip():
            continue
        out.append((tier, role, resolve_role_spec({}, roles, tier, role)))
    return out


def _list_rows(root: Path, cfg: dict) -> int:
    """Dry print the roles table, resolved. Nothing is spawned or written."""
    roles = spawn_gate.read_ladder_roles(root / "nodes" if root else None)
    if not roles:
        print("ladder: no roles table declared — every tier falls back to "
              "config harnesses.*")
        return 0
    print(f"ladder roles table: {len(roles)} rows")
    for tier, role, spec in _compile_role_rows(roles):
        print(f"tier={tier} role={role:<15} harness={spec['harness'] or '-':<11} "
              f"model={spec['model'] or '-':<28} "
              f"effort={spec['effort'] or '-':<5} "
              f"settings={spec['settings'] or '-'}")
    return 0


def apply_advisor_goal_env(value: str | None) -> None:
    """Seed/clear the advisor-goal env read by `brief.assemble(tier=advisor)`.

    `hypothesis:l3w3-advisor-brief` addendum after L3.12 — a `--goal goal:<id>`
    pins which perpetual-goal director the advisor brief says to spawn. The
    brief is assembled inside `adapter.build_command`, and every harness calls
    it, so the goal is threaded through the ENVIRONMENT rather than a new
    keyword on every adapter (claude_code_adapter.py belongs to another kid
    this round). Set once per invocation, before the spawn loop.
    """
    if value:
        os.environ["AGI_ADVISOR_GOAL"] = value
    else:
        os.environ.pop("AGI_ADVISOR_GOAL", None)


def _read_prompt_file(path: str | None) -> str | None:
    """hypothesis:l3-parent-never-told-to-iterate, carry-forward axis (SD.12)
    -- read the per-kid brief channel text. `-` means stdin; anything else is
    a UTF-8 file path. The text is passed as the KID'S `addendum` brief
    segment, never inlined on the argv -- a kid's result holds arbitrary
    characters including quotes and newlines. None (no flag) returns None,
    which leaves the kid brief byte-identical to a non-addendum spawn.
    """
    if path is None:
        return None
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def _dry_run_report(*, root: Path, cfg: dict, harness_name: str,
                    dispatch_harness: dict, adapter: object, args,
                    targets, tier_eff: int) -> int:
    """hypothesis:l3-dispatch-dry-run — resolve and print every slot's spawn.

    Resolves exactly what the live path resolves (target, tier, role, ladder
    tier, brief tier via `_brief_tier_for`, model and effort rows, env
    exports), assembles the brief, prints a compact report (quoted, shell-safe
    command line; exported env; brief tier; brief line count and first 20
    lines) and exits 0. It never registers a spawn-budget slot, never writes a
    manifest or a session dir, and never calls Popen — the caller has already
    deferred `iter_dir.mkdir`, so nothing lands on disk.

    The command line is built through each harness's OWN `build_command` (the
    same call the live spawn loop makes), so model/effort/settings routing,
    the advisor brief swap, the tool bundles and the ultracode env gate are
    all exercised for real; only the `context_file` is a placeholder (a dry
    run does not want to pay for a zoom render), and the `sess_dir` is a
    disposable temp dir that is removed before this returns.
    """
    import brief as _brief
    import tempfile

    current_season = spawn_gate.read_ladder_season(
        root / "nodes" if root else None)
    if current_season is None:
        current_season = 1
    cap = spawn_budget.max_live(cfg)
    parallel = adapters.parallelism(cfg)
    # hypothesis:l3-parent-never-told-to-iterate -- the per-dispatch kid
    # ceiling, named in the parent brief so an iterating parent plans around
    # it instead of discovering an unexplained stop.
    kid_ceiling = spawn_budget.parent_max_kids(cfg)
    # hypothesis:l3-branch-source-paths-never-rerooted -- mirror the live
    # loop's re-rooted engine paths in the dry report (which dry-prints the
    # same argv a real spawn would get).
    engine_paths = child_engine_paths(root)

    for slot, target_entry in enumerate(targets):
        if len(target_entry) == 4:
            level, target, strategy, _role = target_entry
        else:
            level, target, strategy = target_entry
        if level == "auto":
            # Resolution-only: we need one deterministic level for the report.
            level = "big"
        agent_id = f"dry{slot:02d}-{uuid.uuid4().hex[:8]}"
        brief_tier = _brief_tier_for(args.tier, tier_eff, target)
        with tempfile.TemporaryDirectory() as td:
            sess_dir = Path(td)
            # Placeholder context — we resolve the spawn, not the map.
            # Written via open().write rather than a node-writer call: the
            # suite asserts dispatch.py only ever writes named session
            # artefacts.
            ctx_file = sess_dir / "context.md"
            with open(ctx_file, "w", encoding="utf-8") as _fh:
                _fh.write(
                    f"# dry-run context (placeholder, no zoom render)\n\n"
                    f"target: {target}\nlevel: {level}\n")
            cmd = adapter.build_command(
                harness=dispatch_harness, tier=args.tier,
                brief_tier=brief_tier, context_file=str(ctx_file),
                agent_id=agent_id, iter_n=args.iter_n,
                sess_dir=sess_dir, scaffold=None, cli_py=engine_paths["cli_py"],
                skill_prompt=engine_paths["skill_prompt"],
                dispatch_py=engine_paths["dispatch_py"],
                source_root=engine_paths["source_root"],
                target=target, parallel=parallel, max_live=cap,
                kid_ceiling=kid_ceiling,
                addendum=_read_prompt_file(args.prompt_file),
                role=args.role, ladder_tier=tier_eff,
            )
            # The env a child WOULD have been spawned with — same exports the
            # live loop builds in main(), kept here so the dry report shows
            # the real values (AGI_*, CLAUDE_CODE_WORKFLOWS) without a spawn.
            env = adapter.child_env(harness=dispatch_harness,
                                    base=scrubbed_env(), tier=args.tier)
            env["AGI_TIER"] = args.tier
            # hypothesis:l4-spawn-paths-export-the-reaper-knob -- mirror of
            # the live spawn_env export, so the dry report SHOWS the reaper
            # knob without a spawn (a check that costs a spawn is a check that
            # never runs).
            env["CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP"] = "1"
            env["AGI_ROLE"] = args.role
            env["AGI_LADDER_TIER"] = str(tier_eff)
            env["AGI_SEASON"] = str(current_season)
            loop_ref = target or "explore"
            env["AGI_LOOP"] = f"{loop_ref}@s{current_season}"
            model_val = dispatch_harness.get("models", {}).get(args.tier, "")
            if model_val:
                env["AGI_MODEL"] = str(model_val)
            profile_val = dispatch_harness.get("profiles", {}).get(
                args.tier, "balanced")
            env["AGI_PROFILE"] = str(profile_val)
            # hypothesis:l3-agent-id-never-exported — mirror of the live
            # spawn_env identity exports, kept so the dry report shows the
            # child WOULD receive its own id and actor.
            env["AGI_AGENT_ID"] = agent_id
            env["AGI_ACTOR"] = agent_id
            # hypothesis:l4-dispatch-exports-seat — mirror of the live
            # spawn_env seat export, so the dry report shows the REAL value
            # (--seat wins, else an inherited AGI_SEAT survives, else absent).
            # base=scrubbed_env() already carries an inherited AGI_SEAT, so
            # only the --seat override must be written here.
            seat_val = _resolved_seat(args.seat)
            if seat_val:
                env["AGI_SEAT"] = seat_val
            if args.tier in ("kid", "parent"):
                env["GIT_CONFIG_COUNT"] = "1"

            # The brief, assembled directly so the report can show ITS line
            # count and first 20 lines without depending on how a harness
            # spells the prompt to disk.
            segments = _brief.assemble(
                tier=brief_tier, agent_id=agent_id, iter_n=args.iter_n,
                cli_py=engine_paths["cli_py"],
                dispatch_py=engine_paths["dispatch_py"], scaffold=None,
                source_root=engine_paths["source_root"],
                target=target, parallel=parallel, max_live=cap,
                kid_ceiling=kid_ceiling,
                addendum=_read_prompt_file(args.prompt_file),
                session_dir=sess_dir)
        brief_text = "\n\n".join(s.rstrip("\n") for s in segments)
        brief_lines = [l for l in brief_text.splitlines() if l.strip()]

        print(f"[dry-run] slot={slot} harness={harness_name} "
              f"tier={args.tier} role={args.role} ladder_tier={tier_eff} "
              f"level={level} target={target or '-'} "
              f"brief_tier={brief_tier}")
        # Compact: pi inlines every brief segment as its own flag, so the raw
        # command would print hundreds of lines of the brief itself. The brief
        # is shown separately below; here a long argument is shortened to a
        # marker. claude-code keeps the brief in a file, so its line stays
        # clean and short.
        def _compact(a: str) -> str:
            q = shlex.quote(a)
            if len(q) > 200:
                return q[:180] + f"...<{len(q)} chars>"
            return q
        print(f"  command: {' '.join(_compact(a) for a in cmd)}")
        export_keys = ["AGI_TIER", "AGI_ROLE", "AGI_LADDER_TIER",
                       "AGI_SEASON", "AGI_LOOP", "AGI_MODEL",
                       "AGI_PROFILE", "AGI_AGENT_ID", "AGI_ACTOR",
                       "AGI_SEAT", "GIT_CONFIG_COUNT",
                       "CLAUDE_CODE_WORKFLOWS",
                       "CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP"]
        shown = [f"{k}={env[k]}" for k in export_keys if k in env]
        print(f"  env: {' '.join(shown)}")
        print(f"  brief: tier={brief_tier} {len(brief_lines)} lines; "
              f"first 20:")
        for ln in brief_lines[:20]:
            print(f"    {ln}")
    print("dry-run: nothing spawned, nothing written, no budget slot taken")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=locations.iteration_id)
    ap.add_argument(
        "--template",
        default=None,
        help="Override pipeline_template from config (e.g. 'research', 'builder-first')",
    )
    ap.add_argument(
        "--target",
        default=None,
        help="Aim every slot at this node id, bypassing attractiveness scoring",
    )
    ap.add_argument(
        "--level",
        default=None,
        choices=["big", "small", "auto"],
        help="Zoom level for --target (default: small)",
    )
    ap.add_argument(
        "--push-further",
        action="store_true",
        help="hypothesis:l3w4-push-further-loops — re-dispatch at --target, "
             "composing from the target's push_further text and stamping "
             "pushed_from: <target> on the continuation kid. Refused "
             "(exit 2, no lease, no session dir) when --target is an "
             "overview/vision/moral node: the push stops at the quorum.",
    )
    ap.add_argument(
        "--strategy",
        default="extend_existing",
        help="Strategy label recorded for an aimed slot (default: extend_existing)",
    )
    ap.add_argument(
        "--harness",
        default=None,
        help="Harness to spawn through (default: spawn.harness from config)",
    )
    ap.add_argument(
        "--tier",
        default="kid",
        help="Tier to spawn: selects harnesses.<h>.models[tier] (default: kid)",
    )
    ap.add_argument(
        "--role",
        default=None,
        help="Ladder role to spawn (kid|parent|director|prime_director); "
             "resolved against the ladder's roles table (default: derived "
             "from --tier, so a parent tier means role parent)",
    )
    ap.add_argument(
        "--ladder-tier",
        type=int,
        default=None,
        help="Ladder tier (0-3) for roles-table lookup; default derives from "
             "--role when a row exists, else config fallback",
    )
    ap.add_argument(
        "--goal",
        default=None,
        help="Perpetual goal pinned for an advisor's spawned director "
             "(advisor brief only): --tier parent --ladder-tier 3 "
             "--target vision:<id> --goal goal:<id>",
    )
    ap.add_argument(
        "--seat",
        default=None,
        help="Seat name to dispatch as (hypothesis:l3w4-seat-registry). The "
             "seat's own row in config:seats overrides harness/model/effort/"
             "settings from the ladder's (tier, role) class table. No row for "
             "the name falls back to the ladder. Export AGI_SEAT=<name> for "
             "the meter pin to land seat-stable.",
    )
    ap.add_argument(
        "--list-rows",
        action="store_true",
        help="Dry print: resolve every role in the ladder's roles table and "
             "exit without spawning (hypothesis:l3w0-ladder-roles-table)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve and print the fully-resolved spawn for every slot -- "
             "command line, exported env, brief tier, brief line count and "
             "first 20 lines -- WITHOUT spawning, writing a session dir, or "
             "taking a spawn-budget slot. Exits 0 (hypothesis:l3-dispatch-\n"
             "dry-run).",
    )
    ap.add_argument(
        "--branch",
        action="store_true",
        help="Run each spawn in its own git worktree on "
             "loop/<slug>-<agent>@s<N>, cut from the SPAWNER's checked-out "
             "branch; the kid edits only that worktree and its lease/record "
             "carries branch/base_branch/worktree for season.py merge-up "
             "(hypothesis:l3w4-parent-branch-merge-up)",
    )
    ap.add_argument(
        "--allow-stale-base",
        default=None,
        metavar="REASON",
        help="hypothesis:l4-a-round-is-cut-from-the-branch-you-are-on HALF A "
             "-- skip the stale-base refusal: record this REASON on the "
             "agent's branch_ref and cut the round anyway. Being behind the "
             "integration branch is legitimate for a nested layer (a "
             "director cutting from tier1/<name>), but it must be a CONSCIOUS "
             "override, never a default. Without it, a --branch spawn whose "
             "base is behind origin/season/sN is refused (exit 3) with a "
             "structured stale-base record, so the issue cannot be silently "
             "ignored. fail-open: an unreachable origin is never refused.",
    )
    ap.add_argument(
        "--detach",
        action="store_true",
        help="Skip the reaper phase and return immediately after spawn. "
             "The caller (e.g. a parent agent) polls cli.py status to "
             "detect completion. Without this flag dispatch blocks until "
             "all agents finish or the timeout expires.",
    )
    ap.add_argument(
        "--prompt-file",
        default=None,
        help="hypothesis:l3-parent-never-told-to-iterate, carry-forward axis "
             "(SD.12) -- per-kid brief channel. Path to a file (or `-` for "
             "stdin) whose text is threaded into the spawned kid's brief as "
             "its OWN labelled segment ('WHAT THE LAST KID PRODUCED'). Give "
             "this to the NEXT kid's spawn with the last kid's result written "
             "to a file, so the second is never a blind rerun of the first. "
             "Read by path, never inlined as an argv string: a kid's result "
             "holds arbitrary characters (quotes, newlines) that would break "
             "the command line.",
    )
    args = ap.parse_args()

    # hypothesis:l3w3-advisor-brief addendum after L3.12 — thread the advisor's
    # pinned --goal into the assembled brief through the env (see
    # apply_advisor_goal_env). Set before any build_command runs.
    apply_advisor_goal_env(args.goal)

    # hypothesis:l3-dispatch-role-default — a bare --tier parent must mean
    # role parent (so it resolves the parent ladder row, never the tier-0
    # kid model). An explicit --role always wins over the tier-derived
    # default.
    if args.role is None:
        args.role = _default_role_for_tier(args.tier)

    # hypothesis:l4b23-promptfile-drop — `--prompt-file` is the per-KID
    # carry-forward channel (see _read_prompt_file and the --prompt-file
    # help: "threaded into the spawned kid's brief"). A PARENT's brief is
    # built fresh from its target node every dispatch and consumes no
    # carry-forward (brief.assemble() threads addendum into _kid but never
    # into _parent), so `--tier parent --prompt-file X` read X's bytes and
    # silently threw them away. Refuse loudly at argument-parsing time
    # instead of accept-and-drop. The parent says --prompt-file on the KID
    # spawns it cuts, not on its own dispatch.
    if args.tier == "parent" and args.prompt_file is not None:
        print("--prompt-file is a per-KID carry-forward channel and does not "
              "reach a parent's brief (a parent's brief is built fresh from "
              "its target node every dispatch). Pass it to the KID spawns "
              "the parent cuts, not to the parent dispatch itself. Refusing "
              "rather than silently discarding "
              "(hypothesis:l4b23-promptfile-drop).", file=sys.stderr)
        return 2

    # goal:g11.1 — resolve the given path the way every entry point resolves
    # cwd, rather than demanding it already BE the graph root. Identity on a
    # legacy root (phase 1), so no existing project resolves differently.
    given = Path(args.project_root).resolve()
    root = locations.find_project_root(given)
    # hypothesis:l3w4-parent-branch-merge-up — recursion fix (L3.30 defect):
    # when THIS dispatch is itself a spawned --branch parent running in its
    # worktree, AGI_TREE_PROJECT_ROOT names that worktree, and any kid it
    # spawns heredits it as the working tree instead of collapsing back to
    # the main checkout. Re-rooting uses project_root_from_env's seam (the
    # env dispatch itself exports to --branch children) and only fires when
    # it names a DIFFERENT graph than the passed path resolved to, so a
    # top-level dispatch from the seat/cron resolves exactly as before.
    _spawner_env_root = os.environ.get(locations.PROJECT_ROOT_ENV_VARS[0])
    root = child_working_graph(passed_root=root,
                               spawner_env_root=_spawner_env_root)
    cfg_path = locations.config_path(root) if root is not None else None
    if cfg_path is None:
        print(f"ERR: not an agi project: {given}", file=sys.stderr)
        return 1
    cfg = json.loads(cfg_path.read_text())

    # hypothesis:l3w4-seat-registry — a named seat overrides the (tier, role)
    # ladder class table with the seat's own row. Resolved here, after `root`
    # exists and before the harness block reads the ladder.
    if args.seat is not None:
        seat_spec = resolve_seat_spec(
            spawn_gate.read_seat_registry(root / "nodes" if root else None),
            args.seat)
        if seat_spec is None:
            print(f"seats: no row for seat '{args.seat}'; falling back to "
                  f"ladder/config", file=sys.stderr)
        else:
            # Reuse the (tier, role) override branch below by substituting the
            # seat's cells for the ladder spec's. The model cell is keyed to
            # the adapter's tier string later, so the seat's model wins.
            _seat_override = dict(seat_spec)
            _seat_override["from_ladder"] = True
            _seat_override["from_seat"] = True
            args._seat_override = _seat_override
            print(f"seats: seat {args.seat} -> "
                  f"{seat_spec['harness'] or '-'}/{seat_spec['model'] or '-'}/"
                  f"effort={seat_spec['effort'] or '-'}/"
                  f"thinking={seat_spec.get('thinking') or '-'}/"
                  f"settings={seat_spec['settings'] or '-'}")

    # hypothesis:l3w0-ladder-roles-table — dry print: resolve every declared
    # role row and exit without spawning anything. Nothing is written.
    if args.list_rows:
        return _list_rows(root, cfg)

    # goal:g4.6 — the harness is resolved ONCE, from config, and everything
    # below spawns through it. This function no longer knows what a pi flag
    # looks like. Adding a harness is a config entry plus one file in
    # bin/adapters/; if it ever needs an edit here, the seam is wrong.
    try:
        harness_name, harness = adapters.resolve(cfg, args.harness)
        # hypothesis:l3w0-ladder-roles-table — a declared (tier, role) row
        # overrides harness/model/effort/settings, resolved from the ladder;
        # config harnesses.* remains the fallback when the ladder has no row.
        ladder_roles = spawn_gate.read_ladder_roles(
            root / "nodes" if root else None)
        tier_eff = (args.ladder_tier if args.ladder_tier is not None
                    else _default_tier_for_role(args.role))
        _spec = resolve_role_spec(cfg, ladder_roles, tier_eff, args.role)
        # hypothesis:l3w4-seat-registry — a named seat's row replaces the
        # ladder spec; the seat's harness/model/effort/settings win.
        if getattr(args, "_seat_override", None):
            _spec = args._seat_override
        dispatch_harness = harness
        explicit_harness = args.harness is not None
        from_seat = bool(_spec.get("from_seat"))
        if _spec["from_ladder"]:
            if _spec["harness"] and _spec["harness"] != harness_name:
                if from_seat or not explicit_harness:
                    # A seat row, or no explicit flag: the declared
                    # (seat/ladder) harness wins, as it always has.
                    harness_name, dispatch_harness = adapters.resolve(
                        cfg, _spec["harness"])
                    dispatch_harness = dict(dispatch_harness)
                else:
                    # hypothesis:l3-dispatch-harness-flag-overridden — an
                    # explicit --harness beats a ladder row that names a
                    # different harness. The row's model/effort/settings
                    # belong to THAT harness, so drop them and take this
                    # harness's own tier model. One notice naming both.
                    print(f"harness: --harness {harness_name} overrides "
                          f"ladder row harness {_spec['harness']} (using "
                          f"{harness_name} models for tier {args.tier})")
            else:
                dispatch_harness = dict(harness)
            if (from_seat or not explicit_harness
                    or _spec["harness"] == harness_name):
                _models = dict(dispatch_harness.get("models") or {})
                if _spec["model"]:
                    # Keyed by the adapter's tier string so model_args(harness,
                    # args.tier) returns the ladder row's model.
                    _models[args.tier] = _spec["model"]
                dispatch_harness["models"] = _models
                if _spec["effort"]:
                    dispatch_harness["effort"] = {args.tier: _spec["effort"]}
                # hypothesis:l3w4-director-kids-on-glm — flat, not tier-keyed:
                # pi_adapter.model_args reads `harness["thinking"]` directly
                # (no tier key) and emits `--thinking <val>`. Absent means the
                # harness's own default stands.
                if _spec.get("thinking"):
                    dispatch_harness["thinking"] = _spec["thinking"]
                if _spec["settings"]:
                    dispatch_harness["settings"] = _spec["settings"]
        else:
            print(f"roles: no ladder row for (tier={tier_eff}, "
                  f"role={args.role}); falling back to config "
                  f"harnesses.{harness_name}.models[{args.tier}]")
        if _spec["from_ladder"]:
            print(f"roles: tier={tier_eff} role={args.role} -> "
                  f"{_spec['harness']}/{_spec['model'] or '-'}/"
                  f"effort={_spec['effort'] or '-'}/"
                  f"thinking={_spec['thinking'] or '-'}/"
                  f"settings={_spec['settings'] or '-'}")
            # hypothesis:l4-a-model-change-is-one-write — when a ladder row
            # wins the model, a config that still carries the legacy inputs is
            # a NON-INPUT: ONE stderr warning naming the winning row, never a
            # silent read. The stale cells are read nowhere after this line.
            _legacy_model_srcs = []
            _h = (cfg.get("harnesses") or {}).get(harness_name) or {}
            if _h.get("models"):
                _legacy_model_srcs.append(f"harnesses.{harness_name}.models")
            if (cfg.get("agent_dispatch") or {}).get("model"):
                _legacy_model_srcs.append("agent_dispatch.model")
            if _legacy_model_srcs:
                print(f"warn: {' and '.join(_legacy_model_srcs)} is/are "
                      f"NON-INPUTS (hypothesis:l4-a-model-change-is-one-write); "
                      f"ladder row (tier={tier_eff}, role={args.role}, "
                      f"harness={_spec.get('harness')}) wins -> "
                      f"model={_spec.get('model') or '-'}",
                      file=sys.stderr)
        # hypothesis:l3-workflow-model-crosses-harness-namespace — the guard
        # workflow.py has carried since the incident, now on the spawn path
        # too. Every source of a model (ladder row, seat row, config fallback)
        # has landed in `dispatch_harness["models"]` by this line, so this is
        # the one place that sees all three. Refuse BEFORE a credential is
        # minted or a process starts: a Claude alias resolved onto an
        # OpenRouter provider bills Anthropic against an OpenRouter key, and
        # the failure looks like a bill, not like a wrong flag.
        _eff_model = (dispatch_harness.get("models") or {}).get(args.tier)
        if _eff_model:
            adapters.assert_model_in_provider_namespace(
                str(_eff_model), str(dispatch_harness.get("provider") or ""))
        # hypothesis:l4-dispatch-model-allowlist -- the fail-closed allowlist
        # gate, same position and same reason as the namespace guard above:
        # this is the one line every model source (ladder row, seat row,
        # config fallback) has landed in `dispatch_harness["models"]`, so it
        # is the single place a refusal is a refusal everywhere. A `--seat`
        # override is not an exemption: its model is in this same dict by
        # this line and gets the same check. No AGI_MODEL resolves for a tier
        # with no model, so there is nothing to refuse there.
        # hypothesis:l4-a-model-change-is-one-write -- the allowlist gate is
        # the SAME fail-closed gate as before, but the ALLOWED set is now
        # DERIVED: {every ladder row's model for this harness} U
        # harnesses.<h>.allowed_extra (legacy `allowed_models` still unions in
        # for one cut-over round and is warned once). A NEW model written into
        # a ladder row is allowed WITHOUT an `allowed_models` edit -- the
        # four-cells-in-three-files defect the hypothesis measures. A model no
        # row, no extra and no legacy entry names is still refused.
        _derived_allowed = adapters.derived_allowed_models(
            ladder_roles, harness_name, dispatch_harness)
        if dispatch_harness.get("allowed_models"):
            print(f"warn: config harnesses.{harness_name}.allowed_models is "
                  f"legacy; allowed models are now DERIVED from ladder rows + "
                  f"harnesses.{harness_name}.allowed_extra "
                  f"(hypothesis:l4-a-model-change-is-one-write)",
                  file=sys.stderr)
        _assert_allowed_model(harness_name,
                              {**dispatch_harness,
                               "allowed_models": sorted(_derived_allowed)},
                              _eff_model)
        adapter = adapters.load(dispatch_harness["adapter"])
    except adapters.AdapterError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 1
    n = adapters.parallelism(cfg)
    # goal:g4.8 item 3 — the bound that survives a tier. `n` is this
    # invocation's slot count; `cap` is the whole tree's live population, and
    # a parent's own dispatch hits the same leases this one does.
    cap = spawn_budget.max_live(cfg)
    # goal:g1.11 -- per-spawn credentials, when this project can issue them.
    # Absence is a supported state: with no provisioning key every agent
    # inherits the shared runtime key exactly as before, and nothing here
    # changes shape.
    cred_limit, cred_ttl = provisioning.settings(cfg)
    cred_ws = provisioning.workspace(cfg)
    issuing = provisioning.available(root)
    if issuing:
        print(f"credentials: minting per spawn, limit=${cred_limit} "
              f"ttl={cred_ttl}min"
              + (f" workspace={cred_ws}" if cred_ws else " workspace=(default)"))
    big_split = float(cfg.get("big_idea_vs_small_idea_split", 0.3))
    timeout_min = int(cfg.get("agent_timeout_mins", 10))
    pipeline_template = args.template or cfg.get("pipeline_template")

    # hypothesis:l2w2-writer-stamps — read season from ladder for AGI_SEASON
    current_season = spawn_gate.read_ladder_season(
        root / "nodes" if root else None)
    if current_season is None:
        current_season = 1
        print(f"season: ladder not found, defaulting to {current_season}")
    else:
        print(f"season: ladder current_season={current_season}")

    # hypothesis:l4-seat-session-iter-dirs (half a) — iter-<id>/ session dirs
    # (per-agent `agent.json`, the iteration `manifest.json`, `output.log`)
    # resolve to the WORKTREE that made them, so a seat harvests its own
    # round from its own tree. This REVERSES the L3.38 `l3-cli-done-worktree-
    # manifest` rule that routed every agent's record into the MAIN checkout
    # through `shared_project_root`. Only the spawn budget, comms root and
    # meter pins stay on `shared_project_root` (they are a tree-wide bound and
    # must not fork); the graph a kid edits stays `root`/`child_graph` (forked).
    sess_root = root
    iter_dir = locations.iteration_dir(sess_root, args.iter_n)
    # Deferred `.mkdir()` until AFTER the dry-run return: a dry-run must not
    # create a session dir (hypothesis:l3-dispatch-dry-run).

    # Two-agent research pipeline: architect (slot 0) + builder (slot 1)
    # Slot 1 waits for slot 0 to produce a node, then implements it.
    if pipeline_template == "research" and n < 2:
        print(f"ERR: pipeline_template=research requires claude_max_parallel>=2, got {n}", file=sys.stderr)
        return 1

    if args.target:
        if pipeline_template == "research":
            print("ERR: --target and pipeline_template=research both choose the "
                  "targets; pass one or the other", file=sys.stderr)
            return 1
        targets = _explicit_targets(args.target, args.level, args.strategy, n)
        print(f"aimed: {n} slot(s) at {args.target} "
              f"(level={targets[0][0]}, strategy={args.strategy})")
    elif pipeline_template == "research":
        targets = _research_pipeline_targets(root, n, iter_dir)
    else:
        targets = _pick_targets(root, n)

    # hypothesis:l3w4-push-further-loops — the mechanical stop at the quorum.
    # `--push-further --target <id>` is REFUSED before any slot is admitted
    # when <id> is an overview/vision/moral node (the quorum-judged tiers),
    # so a push-further chain can re-dispatch at the same target id through
    # the kid/parent/director tiers but can never auto-continue INTO that
    # territory. Exit 2, before iter_dir.mkdir (no session dir) and before
    # any spawn_budget lease.
    if args.push_further:
        refused = _push_further_gate(root, args.target)
        if refused:
            code, msg = refused
            print(msg, file=sys.stderr)
            return code

    # hypothesis:l3-dispatch-dry-run — a dry run resolves everything the live
    # path resolves (target, tier, role, ladder tier, brief tier via
    # `_brief_tier_for`, model and effort rows, env exports) then assembles the
    # brief, prints a compact report and exits 0 — without spawning, let a
    # single spawn-budget slot, write a manifest or session dir, or call
    # Popen. It also must not create the iteration dir — hence the deferred
    # `.mkdir()` above.
    if args.dry_run:
        return _dry_run_report(
            root=root, cfg=cfg, harness_name=harness_name,
            dispatch_harness=dispatch_harness, adapter=adapter,
            args=args, targets=targets, tier_eff=tier_eff)
    iter_dir.mkdir(parents=True, exist_ok=True)

    # goal:s28 — merge into existing manifest rather than overwriting.
    # A parent dispatch into the same iter dir must not clobber its own
    # entry (or any other agent's). Read old manifest first; new agents
    # are merged in by agent id. Write atomically via temp file + rename.
    manifest_path = iter_dir / "manifest.json"
    manifest = {
        "iter": args.iter_n,
        "started_at": int(time.time()),
        "timeout_seconds": timeout_min * 60,
        "agents": [],
        "pipeline_template": pipeline_template,
    }
    if manifest_path.exists():
        try:
            old = json.loads(manifest_path.read_text())
            manifest["agents"] = old.get("agents", [])
            manifest["started_at"] = old.get("started_at", manifest["started_at"])
        except (json.JSONDecodeError, OSError):
            print(f"warn: corrupt manifest at {manifest_path}, starting fresh", file=sys.stderr)

    # Records created by THIS invocation. The authoritative merge happens once,
    # at the end, under lock and against a fresh read -- see `_merge_manifest`.
    new_records: list[dict] = []
    # goal:g4.8 item 3 — slots the budget refused. Recorded rather than
    # dropped: a slot that silently did not spawn is indistinguishable from
    # one that spawned and died, which is the same invisibility the manifest
    # race produced.
    unadmitted: list[dict] = []

    # hypothesis:l3-openrouter-key-headroom-invisible AND l4-the-floor-guards-
    # the-key-that-drains — pre-flight BEFORE any slot takes a budget lease.
    # l3: the runtime sub-key's remaining balance (which OpenRouter reports as
    # "401 API key expired" when crossed) surfaces as a named refusal. l4:
    # rounds bill to MINTED per-spawn keys, so the floor must ALSO consult the
    # outstanding engine-minted keys, or it reads a number that cannot move.
    # Both checks are fail-open on absence or a network error — an unreachable
    # API must never block a round — and both apply only to an openrouter
    # harness, whose keys carry their own dollar caps.
    if dispatch_harness.get("provider") == "openrouter":
        # this round's REQUIRED (d)/(e): the provisioning-ABSENT gate. With
        # provisioning LIVE this short-circuits True (the spawn mints its own
        # key, so a dead runtime key must not block -- L4.98). With it ABSENT,
        # the runtime key IS the spawn's credential, so a 401 makes the pre-
        # flight refuse here, BEFORE any budget slot below is taken.
        _rtk_ok, _rtk_msg = provisioning.check_runtime_key_usable(cfg, root)
        if not _rtk_ok:
            print(f"ERR: {_rtk_msg}", file=sys.stderr)
            return 1
        _hkey_ok, _hkey_msg = provisioning.check_key_floor(cfg, root)
        if not _hkey_ok:
            print(f"ERR: {_hkey_msg}", file=sys.stderr)
            return 1
        # hypothesis:l4-the-floor-must-watch-the-account — ADDITIVE to the key
        # floor, never replacing it. Rounds bill to the ACCOUNT, which the key
        # floor cannot see, so a drained account must refuse a spawn the same
        # way a drained key does. Fail-closed on a present reading below,
        # fail-open on absence or a network error (see check_account_floor).
        _acc_ok, _acc_msg = provisioning.check_account_floor(cfg, root)
        if not _acc_ok:
            print(f"ERR: {_acc_msg}", file=sys.stderr)
            return 1

    for slot, target_entry in enumerate(targets):
        if len(target_entry) == 4:
            level, target, strategy, role = target_entry
        else:
            level, target, strategy = target_entry
            role = None
        # Decide big-vs-small based on config split when "auto"
        if level == "auto":
            level = "big" if random.random() < big_split else "small"
            if level == "small" and target is None:
                level = "big"  # no target → fall back to big

        agent_id = f"a{slot:02d}-{uuid.uuid4().hex[:8]}"
        sess_dir = iter_dir / agent_id
        sess_dir.mkdir(parents=True, exist_ok=True)

        # goal:g4.8 item 3 — admission BEFORE any work is done for this slot.
        # Taken here rather than immediately before `Popen` so a refused slot
        # costs no zoom render and leaves no orphan scaffold behind; the lease
        # is released on every path below that gives up on spawning.
        lease = spawn_budget.acquire(
            root, cap, agent_id, tier=args.tier, iter_n=args.iter_n)
        if lease is None:
            # hypothesis:l3-reaper-restarts-through-stop — a refused lease
            # while paused is not "full"; "0/25, refused" read as a budget
            # message is exactly the confident-wrong-number shape this
            # loop has been chasing all day.
            paused = spawn_budget.is_paused(root)
            if paused:
                reason = paused.get("reason") or "owner stop order"
                print(f"unadmitted {agent_id} slot={slot}: dispatch paused "
                      f"({reason}) — skipping, not waiting", file=sys.stderr)
                unadmitted.append({
                    "id": agent_id,
                    "slot": slot,
                    "tier": args.tier,
                    "target": target,
                    "status": "unadmitted",
                    "reason": f"dispatch paused ({reason})",
                    "at": int(time.time()),
                })
                continue
            live = spawn_budget.live_count(root)
            print(f"unadmitted {agent_id} slot={slot}: spawn budget full "
                  f"({live}/{cap} live tree-wide) — skipping, not waiting",
                  file=sys.stderr)
            unadmitted.append({
                "id": agent_id,
                "slot": slot,
                "tier": args.tier,
                "target": target,
                "status": "unadmitted",
                "reason": f"spawn budget full ({live}/{cap})",
                "at": int(time.time()),
            })
            continue

        # hypothesis:l3w4-parent-branch-merge-up — `--branch` gives this
        # spawn its own git worktree on loop/<slug>-<agent8>@s<N>, cut from
        # the SPAWNER's checked-out branch. The kid edits only that worktree
        # (child_graph for zoom/scaffold, cwd + AGI_TREE_PROJECT_ROOT for the
        # process), and the lease + agent record carry branch/base_branch/
        # worktree so season.py merge-up knows which base this climbs into.
        # Shared state (budget dir, comms, meter pins) resolves to the MAIN
        # checkout through git_common_root, so the concurrency bound and the
        # rooms stay ONE directory even with N worktrees live.
        child_graph = root
        # hypothesis:l3-branch-source-paths-never-rerooted part 3 -- a plain
        # (non-`--branch`) spawn previously got `branch_root = root`, where
        # `root` is the `.agi` GRAPH DIR, not the checkout. That born the kid
        # in `<graph>/.agi` with no `extensions/` beside it, so every relative
        # source instruction its own brief gave it resolvers nothing while
        # every graph reference resolved. The checkout root is what relative
        # source paths resolve against -- and what the agent-git commit guard
        # compares to `git rev-parse --show-toplevel`. Under `--branch`
        # `branch_root` is already the worktree checkout root below.
        branch_root = locations.source_root(root)
        branch_ref: dict = {}
        if args.branch:
            base = spawner_base_branch(Path.cwd())
            if not base:
                print(f"ERR {agent_id} slot={slot}: --branch requires a "
                      f"checked-out branch (detached HEAD?) to cut a child "
                      f"from", file=sys.stderr)
                spawn_budget.release(lease)
                return 1
            # hypothesis:l4-a-round-is-cut-from-the-branch-you-are-on
            # HALF A — freshness guard: a round is only as fresh as this base.
            # Refuse to cut the worktree when the base is behind the
            # integration branch, unless an explicit --allow-stale-base reason
            # makes it a conscious override. fail-open: an unreachable origin
            # is a note, never a block (an unreachable remote is not a
            # workflow issue).
            stale = _stale_base_spawn(Path.cwd(), current_season)
            if stale["status"] == "behind" and not args.allow_stale_base:
                print(json.dumps(_stale_base_record(stale, current_season)),
                      file=sys.stderr)
                spawn_budget.release(lease)
                return 3  # must-pick: no resolving choice, no spawn
            elif stale["status"] == "unchecked":
                print(f"note {agent_id} slot={slot}: freshness of base "
                      f"unchecked (origin season/s{current_season} "
                      f"unreachable); spawn proceeds", file=sys.stderr)
            branch = loop_branch_name(target, agent_id, current_season)
            try:
                wt = branch_worktree_for_spawn(root, branch, agent_id, base)
            except RuntimeError as exc:
                print(f"ERR {agent_id} slot={slot}: {exc}", file=sys.stderr)
                spawn_budget.release(lease)
                return 1
            branch_root = wt
            child_graph = locations.find_project_root(wt) or wt
            branch_ref = {
                "branch": branch,
                "base_branch": base,
                "worktree": str(wt),
            }
            if stale["status"] == "behind":
                # An allowed stale base is a conscious override: record the
                # user-supplied reason and the measured gap on the branch_ref
                # so merge-up and the round record show WHY it was cut stale.
                branch_ref["stale_base_reason"] = args.allow_stale_base
                branch_ref["behind_base"] = stale["behind"]
            spawn_budget.attach_branch(lease, branch_ref)

        # hypothesis:l3-branch-source-paths-never-rerooted parts 1-2 -- the
        # GRAPH is re-rooted above; re-root the ENGINE paths to the same child
        # checkout (the `--branch` worktree, or the checkout-rooted plain
        # spawn) so one argv no longer mixes a worktree node path with
        # main-absolute source paths. Fallbacks inside preserve the pre-fix
        # constants when the child's source tree has no engine.
        engine_paths = child_engine_paths(child_graph)

        zoom_cmd = zoom_command(child_graph, args.iter_n, agent_id, level, target,
                               push_further=args.push_further)
        try:
            ctx_path = subprocess.run(
                zoom_cmd, capture_output=True, text=True, check=True
            ).stdout.strip()
        except subprocess.CalledProcessError as exc:
            # An aimed run is the case where this is a typo rather than a bug:
            # scoring can only return ids it just read out of the graph, but a
            # hand-passed `--target` can name anything. Say which id failed
            # instead of surfacing a CalledProcessError traceback.
            print(f"ERR: no context for target {target!r} at level {level}: "
                  f"{(exc.stderr or '').strip()}", file=sys.stderr)
            if branch_ref:
                drop_branch_worktree(root, branch_ref["worktree"])
            spawn_budget.release(lease)
            return 1

        # Scaffold a node file before agent starts — agent fills body only
        # goal:s27 -- a parent authors nothing of its own. Its artefact is the
        # kids' nodes it is responsible for, the way a real parent is
        # responsible for its children rather than for a separate object.
        # Scaffolding used to run for EVERY tier, so a parent briefed "you do
        # not write the node yourself" had to author a `hypothesis` anyway to
        # pass `cli.py done` -- and that report then counted in
        # `scoring_hypothesis_count`, so running a parent LOWERED
        # `outcome_coverage` (measured 0.284 -> 0.280 on the first parent run).
        if args.tier == "parent":
            scaffold_info = None
            print("tier=parent: no scaffold — a parent's artefact is its kids' "
                  "nodes (goal:s27)")
        else:
            # hypothesis:l3-scaffold-stamps-spawner-env — a dispatch-spawned
            # scaffold used to be stamped from the DISPATCHER's os.environ
            # (node_writer reads AGI_LOOP/AGI_MODEL/AGI_PROFILE/AGI_ROLE/
            # AGI_SEASON at write time), so a kid or advisor spawned under a
            # parent was born role=parent model=<parent's model> loop=<the
            # parent's loop>. The child's true identity was computed only
            # later, into spawn_env, and never reached the scaffold. Resolve
            # the child's row HERE, before scaffold, and hand it to
            # node_writer so the node is stamped with the agent it is FOR,
            # not the agent that made it. Same sources as the spawn_env
            # exports below, so the node and the running agent agree.
            child_stamp = {
                "role": args.role,
                "loop": f"{target or 'explore'}@s{current_season}",
                "model": dispatch_harness.get("models", {}).get(args.tier, ""),
                "profile": dispatch_harness.get("profiles", {}).get(args.tier, "balanced"),
                "season": str(current_season),
            }
            extra_fm = ({"pushed_from": args.target}
                        if args.push_further and args.target else None)
            scaffold_info = _scaffold_node_for_agent(
                child_graph, args.iter_n, agent_id, level, target, role,
                stamp=child_stamp, extra_fm=extra_fm)
            if scaffold_info:
                print(f"scaffolded {scaffold_info['node_type']} node: {scaffold_info['node_id']}")
                if args.push_further:
                    print(f"push-further: {args.target} -> "
                          f"{scaffold_info['node_id']}")

        # Spawn pi (detached). Output -> sess_dir/output.log
        minted = None  # set iff a per-spawn credential was minted for THIS slot
        try:
            spawn_args = adapter.build_command(
                harness=dispatch_harness,
                tier=args.tier,
                # hypothesis:l3w3-advisor-brief — a tier-3 parent spawn
                # aimed at a vision node must get the ADVISOR brief (vision
                # body, tier3-quorum seat, perpetual-director spawn), not the
                # generic parent one. The model/role stay parent-tier; only
                # the assembled brief changes.
                brief_tier=_brief_tier_for(args.tier, tier_eff, target),
                context_file=ctx_path,
                agent_id=agent_id,
                iter_n=args.iter_n,
                sess_dir=sess_dir,
                scaffold=scaffold_info,
                cli_py=engine_paths["cli_py"],
                skill_prompt=engine_paths["skill_prompt"],
                # goal:g1.9 / goal:g4.8 -- a parent brief needs the spawn
                # command, its aim, and the concurrency bound. A kid brief
                # ignores all three; passing them unconditionally keeps the
                # call site tier-blind, which is the point of the assembler.
                dispatch_py=engine_paths["dispatch_py"],
                # hypothesis:l3-branch-source-paths-never-rerooted part 4 --
                # tell the agent, out loud, which checkout it owns.
                source_root=engine_paths["source_root"],
                target=target,
                parallel=adapters.parallelism(cfg),
                max_live=cap,
                # hypothesis:l3-parent-never-told-to-iterate -- the
                # per-dispatch kid ceiling threaded to the parent brief.
                kid_ceiling=spawn_budget.parent_max_kids(cfg),
                # hypothesis:l3-parent-never-told-to-iterate, carry-forward
                # axis (SD.12) -- the per-kid brief channel. Read once per
                # invocation so the same text threads the whole batch.
                addendum=_read_prompt_file(args.prompt_file),
                # hypothesis:l3-cc-tools-by-tier -- who this agent is on the
                # ladder selects its tool bundle (kids keep the closed list;
                # advisors/directors add the ultracode/loop tools).
                role=args.role,
                ladder_tier=tier_eff,
            )
            spawn_env = adapter.child_env(harness=dispatch_harness, base=scrubbed_env(),
                                           tier=args.tier)
            # hypothesis:l4-spawn-paths-export-the-reaper-knob -- the harness
            # reaps "background" shells on a Bun memoryPressure signal; the
            # only gate is CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP (read
            # verbatim from the installed claude-code bundle). Set it
            # UNCONDITIONALLY to defeat it for every spawn: an inherited "0"
            # would otherwise re-arm the reaper silently, and an inherited
            # value is one tmux restart from gone. This is the spawn surface;
            # it must not live in config, nodes, or a shell profile.
            spawn_env["CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP"] = "1"
            # goal:l2-agent-git-commit-guard -- belt: refuse git write for
            # automated agent tiers (kid, parent).  AGI_TIER distinguishes
            # machine from human; GIT_CONFIG tells git to use our hooks
            # directory (agent-git/) which exits 1 for tier kid/parent.
            # Only the director or a human session can write to git.
            spawn_env["AGI_TIER"] = args.tier
            # hypothesis:l3w0-ladder-roles-table — claim the role and ladder
            # tier in the environment so node_writer stamps `role:` and the
            # portal knows which level of the ladder this agent sits at.
            spawn_env["AGI_ROLE"] = args.role
            spawn_env["AGI_LADDER_TIER"] = str(tier_eff)
            # hypothesis:l2w2-writer-stamps — stamp season / loop / model /
            # profile into child env so node_writer can pick them up at mint.
            spawn_env["AGI_SEASON"] = str(current_season)
            loop_ref = target or "explore"
            spawn_env["AGI_LOOP"] = f"{loop_ref}@s{current_season}"
            model_val = dispatch_harness.get("models", {}).get(args.tier, "")
            if model_val:
                spawn_env["AGI_MODEL"] = str(model_val)
            profile_val = dispatch_harness.get("profiles", {}).get(
                args.tier, "balanced")
            spawn_env["AGI_PROFILE"] = str(profile_val)
            # hypothesis:l3-agent-id-never-exported — tell every agent its own
            # name: export the id dispatch minted and the actor under which it
            # records provenance, so send.py and write.py resolve the same
            # identity the engine already wrote into agent.json, instead of
            # inventing a per-tool fallback (tmux window name / $USER).
            spawn_env["AGI_AGENT_ID"] = agent_id
            spawn_env["AGI_ACTOR"] = agent_id
            # hypothesis:l4-dispatch-exports-seat — the seat under which this
            # agent records provenance must exist in the env, or the write-log
            # `seat` key L4.06 added is empty for every dispatched agent.
            # Precedence: --seat wins; an inherited AGI_SEAT (from the manual
            # export the help text documents) survives when --seat is absent.
            # base=scrubbed_env() already carries an inherited AGI_SEAT, so
            # only the --seat override must be written here.
            seat_val = _resolved_seat(args.seat)
            if seat_val:
                spawn_env["AGI_SEAT"] = seat_val
            if args.tier in ("kid", "parent"):
                plugin_root = Path(__file__).resolve().parent.parent
                hooks_dir = plugin_root / "hooks" / "agent-git"
                spawn_env["GIT_CONFIG_COUNT"] = "1"
                spawn_env["GIT_CONFIG_KEY_0"] = "core.hooksPath"
                spawn_env["GIT_CONFIG_VALUE_0"] = str(hooks_dir)
                # hypothesis:l2-commit-guard-scope — the hooks compare
                # toplevel with AGI_PROJECT_ROOT to scope the refusal to
                # only the project repo, so test repos under /tmp are
                # allowed even under AGI_TIER=kid
                spawn_env["AGI_PROJECT_ROOT"] = str(branch_root.resolve())
            # hypothesis:l3w4-parent-branch-merge-up — under `--branch` the
            # child is told (cwd AND AGI_TREE_PROJECT_ROOT, which
            # project_root_from_env and the bash half check first) that its
            # project root is the WORKTREE, so its node writes and grid ops
            # edit only that tree while shared budget/comms/meter resolve to
            # the main checkout through git_common_root.
            if args.branch:
                spawn_env["AGI_TREE_PROJECT_ROOT"] = str(branch_root.resolve())
            # goal:g1.11 -- mint AFTER the brief is assembled and BEFORE the
            # process exists, so a key is never issued for a slot that then
            # fails to spawn for some other reason. The secret goes into the
            # child environment and nowhere else: not the lease, not the
            # manifest, not the log. Only the hash is recorded, and it is
            # recorded on the lease, because the lease's liveness is already
            # what governs the slot -- so reclaiming the slot and revoking the
            # key are one event rather than two that can disagree.
            # goal:s34 item 2 -- only mint for harnesses whose adapter needs
            # a credential; CC kids authenticate through their own channel.
            if issuing and adapters.needs_credential(dispatch_harness):
                minted = provisioning.mint(
                    iter_n=args.iter_n, agent_id=agent_id, tier=args.tier,
                    limit_usd=cred_limit, ttl_minutes=cred_ttl,
                    workspace_id=cred_ws, root=root)
                if minted is not None:
                    spawn_env[provisioning.RUNTIME_KEY_VAR] = minted.secret
                    spawn_budget.attach_credential(lease, minted.key_hash)
        except provisioning.ProvisioningError as exc:
            # A mint that FAILS with a provisioning key present is a real
            # fault, not a reason to quietly fall back to the shared key --
            # falling back would spend the balance this feature exists to
            # protect, while reporting success.
            print(f"ERR: could not mint a credential for {agent_id}: {exc}",
                  file=sys.stderr)
            if branch_ref:
                drop_branch_worktree(root, branch_ref["worktree"])
            spawn_budget.release(lease)
            return 1
        except (KeyError, NotImplementedError) as exc:
            # A tier with no model, or a declared-but-unimplemented harness.
            # Both are config errors and both must name what is missing rather
            # than surfacing a traceback from inside an adapter.
            print(f"ERR: harness {harness_name!r} cannot spawn tier "
                  f"{args.tier!r}: {exc}", file=sys.stderr)
            if branch_ref:
                drop_branch_worktree(root, branch_ref["worktree"])
            spawn_budget.release(lease)
            return 1
        log_file = sess_dir / "output.log"
        try:
            with open(log_file, "wb") as logf:
                proc = subprocess.Popen(
                    spawn_args,
                    stdout=logf,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                    cwd=str(branch_root),
                    env=spawn_env,
                )
        except BaseException:
            # Nothing was started, so nothing holds the slot. Give it back
            # now rather than leaving it to expire with this process, and if
            # a `--branch` worktree was cut for this agent, drop it so a
            # botched spawn does not leak a worktree and its branch.
            if branch_ref:
                drop_branch_worktree(root, branch_ref["worktree"])
            spawn_budget.release(lease)
            raise
        # goal:g4.8 item 3 — the lease changes hands the instant a pid exists.
        # Until this line the reservation is held by THIS process; after it,
        # by the agent. That is what makes the bound survive a dispatcher
        # dying mid-spawn without either leaking a slot or freeing a live
        # agent's.
        spawn_budget.commit(lease, proc.pid)
        agent_record = {
            "id": agent_id,
            "slot": slot,
            "level": level,
            "target": target,
            "strategy": strategy,
            "role": role,
            "pid": proc.pid,
            "started_at": int(time.time()),
            "status": "running",
            "context_file": ctx_path,
            "log_file": str(log_file),
            "harness": harness_name,
            "tier": args.tier,
            "command": " ".join(shlex.quote(a) for a in spawn_args),
            # hypothesis:l4-a-round-alarms-its-dispatcher-by-default --
            # WHO must be alarmed when this round finishes, stamped at spawn
            # with NO flag. The dispatcher is the resolved seat (-x-exported
            # AGI_SEAT, else an inherited one); absent both, the key is
            # present-but-null and the completion/dm path prints ONE stderr
            # line naming the gap rather than guessing a pane identity. Never
            # inferred from a tmux window name or $USER (identity supplied).
            "dispatched_by": _resolved_seat(args.seat),
        }
        if branch_ref:
            # hypothesis:l3w4-parent-branch-merge-up — the recorded
            # base_branch is what season.py merge-up targets (ADDENDUM item
            # 2), so this agent's branch climbs into the layer that cut it,
            # one rung at a time. Season.py reads these from --record.
            agent_record["branch"] = branch_ref["branch"]
            agent_record["base_branch"] = branch_ref["base_branch"]
            agent_record["worktree"] = branch_ref["worktree"]
        if scaffold_info:
            agent_record["node_id"] = scaffold_info.get("node_id", "")
            agent_record["parent"] = scaffold_info.get("parent", "")
        (sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))
        # hypothesis:l4-dispatch-echoes-less-than-it-knows -- LOW-DOX debug
        # artifact, not a stdout dump. Everything a debugger needs (the full
        # child env, the full brief, the argv) that the one-line spawn
        # contract deliberately OMMITS from stdout is recorded here, in the
        # session dir, where a reader opens it on purpose. Env values are
        # REDACTED to their last 4 chars by name-pattern and value-shape; the
        # child's real env is untouched. A failure here must never take the
        # spawn down -- the spawn is the contract, this is a debugger's nicety.
        try:
            import brief as _brief_dbg
            _segs = _brief_dbg.assemble(
                tier=_brief_tier_for(args.tier, tier_eff, target),
                agent_id=agent_id, iter_n=args.iter_n,
                cli_py=engine_paths["cli_py"],
                dispatch_py=engine_paths["dispatch_py"],
                scaffold=scaffold_info,
                source_root=engine_paths["source_root"],
                target=target,
                parallel=adapters.parallelism(cfg),
                max_live=cap,
                kid_ceiling=spawn_budget.parent_max_kids(cfg),
                addendum=_read_prompt_file(args.prompt_file),
                session_dir=sess_dir)
            _brief_text = "\n\n".join(s.rstrip("\n") for s in _segs)
        except BaseException as exc:  # never let the debug artifact break spawn
            _brief_text = f"<spawn.json brief assemble failed: {exc}>"
        (sess_dir / "spawn.json").write_text(json.dumps({
            "agent_id": agent_id,
            "argv": spawn_args,
            "env": _redact_env_map(spawn_env),
            "brief": _brief_text,
        }, indent=2))
        # hypothesis:l3-meter-own-transcript -- once the child prints its
        # first stream-json event, capture its session_id into this agent's
        # `.meter` pin so its OWN rotate meter reads its OWN transcript and
        # never the newest foreign `.jsonl` in the shared project dir. The
        # pin helper is a generic adapter capability (only the claude harness
        # defines it -- pi children write no CC transcript), so dispatch stays
        # harness-agnostic: an adapter that exposes no pinner just skips it.
        pin_background = getattr(adapter, "pin_child_transcript_in_background", None)
        if pin_background is not None:
            pin_background(sess_dir=sess_dir, agent_id=agent_id, cwd=str(root),
                           log_file=log_file, timeout=300)
        # goal:s28 — merge by agent id rather than append.
        # When re-dispatching the same agent (e.g. healing), update in place.
        existing = [i for i, a in enumerate(manifest["agents"]) if a.get("id") == agent_id]
        if existing:
            manifest["agents"][existing[0]] = agent_record
        else:
            manifest["agents"].append(agent_record)
        new_records.append(agent_record)
        # hypothesis:l4-dispatch-echoes-less-than-it-knows -- the ONE-LINE
        # spawn contract: everything a pi PARENT (reading this as a tool
        # result) or a Claude seat needs to poll one spawn, in one line,
        # with the per-spawn credential named by NAME and CAP, never by value
        # or prefix. The env, the brief and the argv are in spawn.json, not
        # here. (pid/level/strategy kept: the reaper and the pane both read
        # them, and removing them is a contract break for zero dox win.)
        spawn_line = (f"spawned {agent_id} pid={proc.pid} tier={args.tier} "
                      f"iter={args.iter_n} target={target or '-'} "
                      f"harness={harness_name} model={model_val or '-'}")
        if branch_ref:
            spawn_line += f" branch={branch_ref['branch']}"
        if minted is not None:
            spawn_line += (f" key={minted.name} cap=${minted.limit_usd}")
        spawn_line += f" level={level} strategy={strategy}"
        print(spawn_line)

    # The one authoritative write, under lock and against a fresh read
    # (goal:s28 for the merge, goal:g4.8 for surviving concurrency). The
    # unique temp name lives inside `_merge_manifest`; it is still spelled
    # `.manifest.json.*` so `test_dispatch_no_longer_touches_the_node_tree_
    # at_all` keeps seeing a named session artefact rather than a variable
    # hiding its target — the assertion was right and the old bare `tmp` name
    # was what defeated it.
    manifest = _merge_manifest(iter_dir, manifest, new_records,
                               unadmitted=unadmitted)
    print(f"manifest: {manifest_path}")
    if unadmitted:
        print(f"budget: {len(unadmitted)} of {len(targets)} slot(s) unadmitted "
              f"at cap {cap} — see manifest.unadmitted", file=sys.stderr)

    if not args.detach:
        # goal:g4.7 — continuous reaper phase. After spawn, poll agent pids via
        # adapter.is_alive() until all agents are terminal or the config timeout
        # expires (was bounded at 30s — now runs for the full agent lifecycle.
        # This replaces heal.py's out-of-process pid monitoring with an inline
        # pass that detects and records failure (or restarts) before the loop
        # exits.
        # With --detach, the caller (e.g. a parent) owns polling via cli.py
        # status; they get the kid's agent id back in seconds rather than
        # waiting for the full lifecycle.
        #
        # hypothesis:l4-the-reaper-is-one-persistent-service part 3 — the
        # inline reaper is OPTIONAL and OFF by default once the persistent
        # service is live. The switch is read from config
        # `agent_dispatch.inline_reaper`, NOT the service's stamp in the
        # manifest: the decision to arm an inline reaper happens at dispatch
        # time, BEFORE the service has any chance to claim this round, so a
        # manifest stamp would be a chicken-and-egg read (nothing has stamped
        # the round yet the instant we must decide). A config key is a
        # one-edit static decision made in the same place the service toggle
        # lands, and defaults to True so current behaviour is unchanged until
        # the prime disables it at the service merge-up.
        _inline_reaper = True
        try:
            _ad_cfg = cfg.get("agent_dispatch") or {}
        except AttributeError:
            _ad_cfg = {}
        if _ad_cfg.get("inline_reaper") is False:
            _inline_reaper = False
        if not _inline_reaper:
            print("reaper: inline reaper off (agent_dispatch.inline_reaper=false); "
                  "persistent service owns reaping", file=sys.stderr)
        else:
            _reaper_phase(
            root=root,
            iter_dir=iter_dir,
            adapter=adapter,
            timeout_s=int(manifest.get("timeout_seconds", 600)),
            max_wait_s=int(manifest.get("timeout_seconds", 600)),
            cap=cap,
            cfg=cfg,
        )

    return 0


def _reaper_phase(
    root: Path,
    iter_dir: Path,
    adapter: object,
    timeout_s: int = 600,
    max_wait_s: int = 600,
    cap: int = 1,
    cfg: dict | None = None,
) -> None:
    """Poll agent pids inline after spawn. Detect dead agents, mark failed.

    `goal:g4.7`. Runs inside dispatch.py's main() after all agents are
    spawned, blocking until all agents reach a terminal status or the config
    timeout expires (was bounded at 30s — now runs for the full agent
    lifecycle). Uses `adapter.is_alive(pid)` so detection works across any
    harness.

    **Continuous monitor, not a bounded phase.** The previous `max_wait_s=30`
    window meant agents dying mid-run (after the first 30s) were invisible to
    the reaper — heal.py marked them failed but had no restart path. The
    `timeout_s` bound covers the full agent lifecycle, matching the window
    heal.py uses for its own timeout handling. A restarted agent completing
    within this window IS harvested by `post_wire` (called after dispatch.py
    returns to driver.sh).

    **Restart is wired now (`goal:g4.7`), and the order of the two checks is
    the whole design.** A dead pid is not the same fact as lost work:

    1. **Check the filesystem first.** Kids routinely die *after* their node
       file landed, losing only the report. The 2026-08-31 field note
       ("check the filesystem before resuming") paid for itself twice in one
       session. Such an agent is recorded `done-unreported` and is **not**
       restarted — respawning it would re-do finished work and, worse, hand a
       second agent the same scaffolded node.
    2. **Only then restart**, bounded by `reaper.max_restarts` (default 1) and
       admitted through the same `spawn_budget` lease as any other spawn. A
       restart is a new process; a recovery path that ignores the concurrency
       bound is a recovery path that can cause the outage it is recovering
       from.

    Still simpler than heal.py: no healer subagent, no SIGKILL cascade.

    hypothesis:l4-the-reaper-is-one-persistent-service — this is the LOOP;
    the per-round work moved to `_reap_pass` so the SAME pass also runs in
    the persistent service (`heal.py watch`). The loop owns the deadline and
    the give-up alarm; a pass has neither. The inline reaper is optional and
    off by default once the service is live — see main() for the switch.
    """
    import time

    deadline = time.time() + max_wait_s
    while time.time() < deadline:
        outcome = _reap_pass(root, iter_dir, adapter, cap=cap, cfg=cfg)
        if outcome["terminal"]:
            break
        time.sleep(5)

    _reaper_give_up(root, iter_dir)
    print("reaper: finished")


def _reap_pass(root, iter_dir, adapter, cap=1, cfg=None,
               restart_ok: bool = True) -> dict:
    """ONE reaper pass over one round's manifest. NO deadline inside.

    hypothesis:l4-the-reaper-is-one-persistent-service — the per-round pass
    extracted from `_reaper_phase`'s loop so the SAME code path runs in
    dispatch.py's inline loop and the persistent service (`heal.py watch`,
    one call per discovered round). A pass reads the manifest, records
    stalls, reaps any agent whose pid is dead, and writes terminal states
    back to the manifest it read. Returns:

        `{"marked":  [agent ids reaped this pass],
          "still":   [agent ids still `running`],
          "died":    [agent ids reaped as DEATHS this pass],
          "terminal": bool}`

    `restart_ok` is the lane switch: dispatch's inline reaper calls with
    `restart_ok=True` (a dead pid may be respawned through the adapter); the
    service (`heal.py watch`) calls with `restart_ok=False` — it has no
    harness, never restarts, and records a dead pid as an honest DEATH, so
    `died` is populated only in the service lane.

    Callers own the deadline (the loop), the timeout-vs-orphaned marks and
    the dm (the watcher), never this function. The `if status != "running"`
    guard is KEPT ON PURPOSE — it catches any status nobody has thought of
    yet, which is exactly the tolerance that kept the old loop working while
    the status set was wrong. Do not "simplify" it away.
    """
    import json

    manifest_path = iter_dir / "manifest.json"
    if not manifest_path.exists():
        return {"marked": [], "still": [], "terminal": True, "died": []}
    try:
        manifest = json.loads(manifest_path.read_text())
    except (json.JSONDecodeError, OSError):
        return {"marked": [], "still": [], "terminal": True, "died": []}

    # hyp:l4-stalled-is-a-state-the-harness-can-see — record, don't repair.
    # The reaper already reads every live `agent.json`; this is where a
    # parent whose kids are all terminal but whose own record still reads
    # `running` (mtime untouched, worktree dirty, past T) becomes a
    # first-class RECORDED `stalled` state. `stall_detect` stamps that
    # state and neither kills, restarts, nor commits — a stalled parent
    # is still alive and still holds its lease, so it never joins
    # `spawn_budget.TERMINAL`. The reap guard below (`if status != "running"`)
    # then skips it on the next pass exactly as designed, so wiring this
    # in changes none of the reaper's commit-based completion logic.
    stall_detect.record_stalled_in_iteration(iter_dir)
    all_terminal = True
    updated = False
    marked: list[str] = []
    still: list[str] = []
    died: list[str] = []
    for entry in manifest.get("agents", []):
        agent_id = entry.get("id", "")
        agent_json_path = iter_dir / agent_id / "agent.json"
        if not agent_json_path.exists():
            continue
        try:
            rec = json.loads(agent_json_path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        status = rec.get("status", "running")
        if status in TERMINAL:
            continue
        if status != "running":
            continue
        all_terminal = False
        still.append(agent_id)

        pid = int(rec.get("pid", 0))
        if pid > 0 and not adapter.is_alive(pid):
            outcome = _reap_one(root, iter_dir, adapter, rec, agent_id, pid,
                                cap=cap, cfg=cfg, restart_ok=restart_ok)
            rec.update(outcome["record"])
            agent_json_path.write_text(json.dumps(rec, indent=2))  # session artefact: agent.json
            entry["status"] = rec["status"]
            # hypothesis:l3w4-branch-visibility — the commit count is on
            # the record and must reach the manifest too, so the round
            # file and the manifest agree on how far the branch climbed.
            if "commits_ahead" in rec:
                entry["commits_ahead"] = rec["commits_ahead"]
            if rec.get("pid"):
                entry["pid"] = rec["pid"]
            # A RESTART MUST BE VISIBLE WHERE THE ROUND IS READ (prime's
            # ruling, 2026-09-10). This copy was a three-key whitelist —
            # status, commits_ahead, pid — so a restart wrote its
            # bookkeeping into the session `agent.json` and none of it
            # reached the manifest: the manifest showed `status: running`
            # with a silently swapped pid and no trace that anything had
            # been restarted, while `spawn_budget` leased the same process
            # as `<id>-r1`. Two identities for one process, and the only
            # way to notice was that the two disagreed. Measured on
            # iter-L4.57 and iter-L4.58 before this line existed.
            for k in ("restart_count", "restart_of", "restarted_at",
                      "fail_reason", "finished_at"):
                if k in rec:
                    entry[k] = rec[k]
            updated = True
            marked.append(agent_id)
            # The SERVICE lane records a dead pid as DEATH (status failed from
            # `_reap_one`'s restart_ok=False branch). Those ids are surfaced
            # separately so the watcher can dm ONE death per agent and never
            # let a dead pid be re-interpreted as a timeout later in the pass.
            if not restart_ok and rec.get("status") == "failed" \
                    and outcome["record"]["fail_reason"].startswith(
                        f"pid {pid} died"):
                died.append(agent_id)
            print(f"reaper: {outcome['message']}")

    if updated:
        manifest_path.write_text(json.dumps(manifest, indent=2))  # session artefact: manifest.json

    return {"marked": marked, "still": still, "died": died,
            "terminal": all_terminal}


def _reaper_give_up(root, iter_dir):
    """hypothesis:l4-a-round-alarms-its-dispatcher-by-default — the reaper's
    GIVE-UP. `finished:` with agents still running is a terminal event for
    this round: every still-running agent's dispatcher gets exactly ONE dm
    naming which agents were still running. No flag; no crash if a dm is
    undeliverable or a stamp absent. A still-running agent is one the
    manifest does NOT list as terminal (the reaper's own guard: `if status
    not in TERMINAL`).
    """
    import json

    manifest_path = iter_dir / "manifest.json"
    still: list[str] = []
    try:
        rows = json.loads(manifest_path.read_text()).get("agents", [])
    except (json.JSONDecodeError, OSError):
        rows = []
    for a in rows:
        if (a.get("status") or "running") not in TERMINAL and a.get("id"):
            still.append(a.get("id"))
    if still:
        for a in rows:
            if not a.get("id") or a.get("id") not in still:
                continue
            dispatcher = a.get("dispatched_by")
            if not dispatcher:
                print(f"warn: no dispatcher stamp for {a.get('id')}; no "
                      "give-up dm (l4-a-round-alarms-its-dispatcher-)",
                      file=sys.stderr)
                continue
            try:
                import send as _send
                _send.send(root, dispatcher,
                           f"iter={iter_dir.name} still-running={','.join(still)}",
                           a.get("id"))
            except Exception as exc:
                print(f"warn: give-up dm to {dispatcher} failed: {exc}",
                      file=sys.stderr)


def _commits_ahead(root, rec):
    """How far a `--branch` agent's branch is ahead of its base, or None.

    hypothesis:l3w4-branch-visibility — the commit count is COMPUTED via
    `git rev-list --count base_branch..branch` from the main checkout
    (`locations.git_common_root`), never hand-counted, so the round record
    and the manifest agree on how far the branch climbed even though the
    reaper runs in the main checkout while the branch lives in a worktree.
    Zero and positive both stamp; a record with no branch/base_branch is left
    untouched (None), so a non-branch agent's record is unchanged.
    """
    branch = rec.get("branch")
    base = rec.get("base_branch")
    if not (branch and base):
        return None
    main = locations.git_common_root(root)
    commits = 0
    try:
        r = subprocess.run(
            ["git", "-C", str(main), "rev-list", "--count",
             f"{base}..{branch}"],
            capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            commits = int(r.stdout.strip())
    except (subprocess.TimeoutExpired, ValueError, OSError):
        commits = 0
    return commits


def _restart_iter_id(iter_dir, rec):
    """The iteration a restart belongs to.

    A manifest record carries no `iter` key, so reading one yields 0 and the
    restart registers as `iter=0` — invisible to any sweep filtered by the
    round. The round's own directory is named `iter-<id>`, which is the
    authoritative source; the record is only a fallback.
    """
    name = getattr(iter_dir, "name", "") or ""
    if name:
        try:
            # iteration_id strips the `iter-` prefix itself and normalises the
            # type — int for the numeric scheme, str for a loop-scoped id — so
            # the lease carries exactly the shape every other caller writes.
            return locations.iteration_id(name)
        except ValueError:
            pass
    return locations.iteration_id(rec.get("iter", 0) or 0)


def _branch_has_done_commit(root, rec, agent_id) -> bool:
    """True when the round's branch has advanced past its base.

    The completion signal for a PARENT, which authors no node of its own and
    whose manifest status the reaper cannot see (the parent updates its
    worktree's copy; the reaper reads the main checkout's).

    **The signal is the COMMIT, never the commit's subject** (prime's ruling,
    2026-09-10). The previous version of this function matched
    `line.startswith(f"{agent_id} done:")` — a string a language model types
    by convention, and the convention is not fixed. Measured the day it was
    replaced: three rounds dispatched by one director inside one hour, one
    parent typed its own id and was correctly spared, two typed their KID's
    id and were restarted onto rounds that were already committed with clean
    worktrees. Roughly $0.9 of key burned re-doing finished work, and the
    branch was carrying `commits_ahead: 1` in the same manifest the whole
    time — the truth was already computed, one call too late to be consulted.

    A `loop/…-<agent_id>@s2` branch is cut for exactly one round and nothing
    else commits to it, so *any* commit after its base is that round's agent's
    work landing. That is the ruling's "authored by the round's agent" made
    checkable: git authorship itself cannot serve, because every agent commits
    as the shared `agi <agi@local>` identity.

    Never raises: an unreadable branch is not evidence of completion, and
    returning False sends the caller down the ordinary restart path. A parent
    killed mid-round has a branch level with its base, reads False here, and
    still restarts — recovery is preserved and asserted directly by
    `test_a_parent_with_no_commit_on_its_branch_is_still_restarted`.
    """
    if not agent_id:
        return False
    return (_commits_ahead(root, rec) or 0) > 0


def _reap_one(root, iter_dir, adapter, rec, agent_id, pid, cap=1, cfg=None,
             restart_ok: bool = True):
    """Decide what a dead agent's death means. Returns `{record, message}`.

    **The filesystem is consulted before the restart, and that ordering is the
    load-bearing part** (`goal:g4.7`). A kid that died after writing its node
    lost only its report; respawning it would redo finished work and hand a
    second agent the same scaffolded node.

    `restart_ok` is the lane switch: True for dispatch's inline reaper (a
    dead pid may be respawned), False for the service watcher (`heal.py
    watch`), which never restarts and records the dead pid as an honest
    DEATH. See `_reap_pass`.

    hypothesis:l3w4-branch-visibility — the returned record also carries
    `commits_ahead` for a `--branch` agent (computed in `_commits_ahead`), so
    whatever the reap decided, the round file records how far the branch had
    climbed.
    """
    out = _reap_one_impl(root, iter_dir, adapter, rec, agent_id, pid,
                         cap=cap, cfg=cfg, restart_ok=restart_ok)
    commits = _commits_ahead(root, rec)
    if commits is not None:
        out["record"]["commits_ahead"] = commits
    return out


def _reap_one_impl(root, iter_dir, adapter, rec, agent_id, pid, cap=1, cfg=None,
                   restart_ok: bool = True):
    import completion

    node_id = rec.get("node_id") or ""
    if node_id:
        try:
            if completion.is_complete(root, node_id):
                return {
                    "record": {
                        "status": "done-unreported",
                        "finished_at": int(time.time()),
                        "fail_reason": (
                            f"pid {pid} disappeared, but {node_id} is complete "
                            f"— the work landed and only the report was lost"),
                    },
                    "message": (f"agent {agent_id} died with {node_id} already "
                                f"complete — NOT restarted"),
                }
        except Exception as exc:
            # An unreadable node is not evidence of completion. Fall through to
            # the restart path and say why, rather than guessing either way.
            print(f"reaper: could not check {node_id}: {exc}", file=sys.stderr)

    # A PARENT AUTHORS NO NODE, so the check above never fires for one: its
    # manifest record carries `node_id: None` because it signals with
    # `cli.py done --owns <kid-node-id>`. Its completion signal is the COMMIT
    # it makes on its own branch, and the reaper reads the MAIN checkout's
    # manifest while the parent updated the one in its worktree — so status
    # stays "running" here however cleanly it finished. The result was that
    # every parent which committed a finished round and exited got respawned
    # to redo it: measured 2026-09-10, $2.01 of key burned in ~30 minutes
    # across four rounds, plus fresh kids writing over committed work.
    # A commit on the agent's branch is proof the work landed.
    if _branch_has_done_commit(root, rec, agent_id):
        return {
            "record": {
                "status": "done-unreported",
                "finished_at": int(time.time()),
                "fail_reason": (
                    f"pid {pid} disappeared, but {agent_id} had already "
                    f"committed on its branch — the work landed and only the "
                    f"report was lost"),
            },
            "message": (f"agent {agent_id} died with its round already "
                        f"committed — NOT restarted"),
        }

    # hypothesis:l4-the-reaper-is-one-persistent-service — the SERVICE lane
    # (`heal.py watch`, restart_ok=False) never restarts: it has no harness,
    # a resume would be a second writer on the manifest, and there is no
    # spawn budget behind it. A dead pid here is DEATH, recorded honestly —
    # status `failed`, fail_reason naming the death — NOT the bogus
    # "restart unavailable" scalar that previously masked the crash (the
    # watcher was never going to restart, so a missing restart path was not
    # the reason it failed). The inline reaper (restart_ok=True) keeps the
    # full paused/restart/budget decision below.
    if not restart_ok:
        return {
            "record": {
                "status": "failed",
                "finished_at": int(time.time()),
                "fail_reason": f"pid {pid} died (detected by reaper)",
            },
            "message": (f"agent {agent_id} failed (pid {pid} died — death "
                        f"recorded by the reaper service)"),
        }

    # hypothesis:l3-reaper-restarts-through-stop — a dead pid is not
    # evidence the reaper should restart it; a pid killed as part of an
    # owner stop order looks identical to a crash from here; checked BEFORE
    # the restart budget so a paused tree never spends a restart slot.
    paused = spawn_budget.is_paused(root)
    if paused:
        reason = paused.get("reason") or "owner stop order"
        return {
            "record": {
                "status": "failed",
                "finished_at": int(time.time()),
                "fail_reason": (f"pid {pid} disappeared; NOT restarted — "
                                 f"dispatch paused ({reason})"),
            },
            "message": (f"agent {agent_id} not restarted: dispatch paused "
                        f"({reason})"),
        }

    restarts = int(rec.get("restart_count", 0))
    max_restarts = int(((cfg or {}).get("reaper") or {}).get("max_restarts", 1))
    failed = {
        "status": "failed",
        "finished_at": int(time.time()),
        "fail_reason": f"pid {pid} disappeared (detected by inline reaper)",
    }
    if restarts >= max_restarts:
        return {"record": failed,
                "message": (f"agent {agent_id} failed (pid {pid} gone, "
                            f"{restarts}/{max_restarts} restarts used)")}

    # A restart is a new process and must be admitted like one. A recovery
    # path that ignores the concurrency bound can cause the outage it is
    # recovering from.
    # hypothesis:l3-killed-agent-restarts-unattributed — a restart is a new
    # PROCESS but the SAME round. The `-rN` lease must inherit the round's
    # iteration id, or the survivor shows `iter=None` in `spawn_budget status`
    # and the round's stop-condition (a loop on the live count, filtered by
    # iter) never sees it. A deliberate kill is distinguishable from a crash
    # elsewhere; when a restart IS legitimate it must be attributable.
    # The record has NO `iter` key — measured against a real manifest — so
    # `rec.get("iter", 0)` silently yielded 0 and every restart registered as
    # `iter=0`. A sweep filtered by the round's iteration then reported the
    # round CLEAR while a restart was live in its worktree. `iter_dir` is the
    # round's own directory (`iter-L4.41`), so its name is the iteration id
    # this restart belongs to; fall back to the record only if that fails.
    lease = spawn_budget.acquire(root, cap, f"{agent_id}-r{restarts + 1}",
                                 tier=rec.get("tier", "kid"),
                                 iter_n=_restart_iter_id(iter_dir, rec))
    if lease is None:
        return {"record": failed,
                "message": (f"agent {agent_id} failed (pid {pid} gone; spawn "
                            f"budget full, not restarted)")}

    try:
        # hypothesis:l2-dispatch-restart-twin-node — Fix A: pass scaffold
        # info to restart so the restarted agent reuses its existing
        # scaffolded node instead of minting a second one.
        scaffold_info = None
        existing_nid = rec.get("node_id") or ""
        if existing_nid:
            # find_node_file expects the graph root (contains nodes/)
            graph_root = root / ".agi" if (root / ".agi" / "nodes").is_dir() else root
            nf = node_writer.find_node_file(graph_root, existing_nid)
            scaffold_info = {
                "node_id": existing_nid,
                "parent": rec.get("parent", ""),
                "node_type": existing_nid.split(":", 1)[0],
                "path": str(nf) if nf else "",
            }
        new_pid = adapter.restart(
            harness=rec.get("harness_spec") or {},
            tier=rec.get("tier", "kid"),
            context_file=rec.get("context_file", ""),
            agent_id=agent_id,
            iter_n=locations.iteration_id(rec.get("iter", 0) or 0),
            sess_dir=Path(iter_dir) / agent_id,
            target=rec.get("target"),
            scaffold=scaffold_info,
            agent_record=rec,
        )
    except (NotImplementedError, Exception) as exc:   # noqa: B014
        spawn_budget.release(lease)
        return {"record": dict(failed, fail_reason=f"{failed['fail_reason']}; "
                               f"restart unavailable: {exc}"),
                "message": f"agent {agent_id} failed; restart unavailable ({exc})"}

    if not new_pid:
        spawn_budget.release(lease)
        return {"record": failed,
                "message": f"agent {agent_id} failed (restart returned no pid)"}

    spawn_budget.commit(lease, new_pid)
    return {
        "record": {"status": "running", "pid": new_pid,
                   "restart_count": restarts + 1,
                   # The lease name spawn_budget actually shows, so a reader
                   # of the manifest and a reader of `spawn_budget status`
                   # are looking at the same process under the same name.
                   "restart_of": f"{agent_id}-r{restarts + 1}",
                   "restarted_at": int(time.time()),
                   "fail_reason": f"pid {pid} disappeared; restarted"},
        "message": (f"agent {agent_id} restarted as pid {new_pid} "
                    f"({restarts + 1}/{max_restarts})"),
    }


def _research_pipeline_targets(root: Path, n: int, iter_dir: Path) -> list[tuple[str, str | None, str]]:
    """Two-agent pipeline: slot 0 = research, slot 1 = implementation.

    Both agents work on the SAME parent node in parallel:
    - Slot 0 (research): extends parent hypothesis → creates experiment → verdict
    - Slot 1 (implementation): extends SAME parent hypothesis → creates mvp pseudocode

    After both complete, post_wire handles wiring both children to the parent.

    Returns list of (level, target, strategy, role).
    """
    import sys as _sys
    plugin_root = Path(__file__).resolve().parent.parent
    proj_src = root / "src"
    if (proj_src / "graph_core").is_dir():
        _sys.path.insert(0, str(proj_src))
    _sys.path.insert(0, str(plugin_root / "src"))

    from graph_core.loader import load_directory
    from graph_core.edge import Edge
    from collections import defaultdict

    # Load closed chains
    closed_chains: set[str] = set()
    ccf = root / "closed_chains.txt"
    if ccf.exists():
        for line in ccf.read_text().splitlines():
            if line := line.strip():
                closed_chains.add(line)

    # Build graph
    cfg_path = config_path(root)
    use_sqlite = False
    if cfg_path is not None:
        cfg = json.loads(cfg_path.read_text())
        use_sqlite = cfg.get("persistence", {}).get("type") == "sqlite"

    if use_sqlite:
        from graph_core.persistence.sqlite_backend import SQLiteBackend
        from graph_core.db_loader import DBLoader
        db_path = root / cfg["persistence"]["path"]
        g, loaded = DBLoader(SQLiteBackend(db_path)).load_directory()
    else:
        g, loaded = load_directory(root / "nodes")

    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                try:
                    g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id, relation="spawns"))
                except Exception:
                    pass
                pn = g.get_node(parent_id)
                if pn is not None:
                    pn.children.add(ln.node.id)

    # Find best hypothesis node (closed-chain filtered)
    hypothesis_nodes = [
        nid for nid in g.node_ids
        if nid not in closed_chains
        and g.get_node(nid) is not None
        and g.get_node(nid).type in ("hypothesis", "Hypothesis")
    ]

    if not hypothesis_nodes:
        # Fallback: any non-closed node
        candidates = [nid for nid in g.node_ids if nid not in closed_chains]
        if not candidates:
            return [("big", None, "explore_new", "research")]
        parent = candidates[0]
    else:
        # Score by descendant count (more children = more active chain)
        def _score(nid):
            n = g.get_node(nid)
            if n is None:
                return 0
            # Prefer nodes with experiment children (active chain)
            has_exp = any(
                g.get_node(c).type in ("experiment", "Experiment")
                for c in (n.children or [])
                if g.get_node(c) is not None
            )
            return (10 if has_exp else 0) + len(n.children or [])

        hypothesis_nodes.sort(key=_score, reverse=True)
        parent = hypothesis_nodes[0]

    # Slot 0: research agent extends parent → experiment/verdict
    # Slot 1: implementation agent extends SAME parent → mvp pseudocode
    # Both use "small" zoom on the same target
    result = [
        ("small", parent, "extend_existing", "research"),
    ]
    if n >= 2:
        result.append(("small", parent, "extend_existing", "implementation"))

    return result


def _explicit_targets(
    target: str, level: str | None, strategy: str, n: int
) -> list[tuple[str, str | None, str]]:
    """Aim every slot at one node, instead of letting scoring choose.

    `_pick_targets` answers "what is most attractive right now"; this answers
    "work on THIS". Both are needed and they are different questions. Without
    it a single-slot run is not steerable at all: `_pick_targets` short-circuits
    at `n <= 1` to `("big", None, "explore_new")`, so the one kid you dispatch
    gets no target, `_node_type_for` scaffolds a parentless `idea`, and the run
    explores wherever scoring points rather than where you aimed.

    `small` is the default level because a target only means something to a
    zoom that reads it -- `zoom.py --level big` ignores `--target` entirely, so
    defaulting to `big` here would silently discard the aim. `auto` is accepted
    and left for `main()` to resolve against `big_idea_vs_small_idea_split`,
    which is the one case where discarding the aim is what was asked for.

    The target is NOT validated here. `zoom.py --level small --target` already
    exits non-zero rather than serving the whole graph for an id it cannot
    find, and one validator beats two that can disagree.
    """
    return [(level or "small", target, strategy)] * n


def _attractiveness(desc: int, recency_boost: float, diversity: float,
                   node_type: str) -> float:
    """Attractiveness score for one node (dispatch chain-ranking).

    The recency leaf boost used to be `desc * 1.2` — and `_descendant_count`
    returns 0 for a leaf, so `0 * 1.2 == 0.0` and the boost never fired:
    every chain tip scored 0 and sorted last (idea:frontier-invitation
    measured this at dispatch.py:1466). Flooring the descendant term at 1
    is what lets a leaf's boost mean anything: a leaf scores 1.2 (not 0.0)
    and can rank. The floor is identity for every non-leaf, which already
    has desc >= 1, so nothing else changes.
    """
    type_weight = {"hypothesis": 1.4, "experiment": 1.2, "verdict": 1.1}.get(
        node_type, 1.0
    )
    return max(desc, 1.0) * recency_boost * type_weight * (1.0 + 0.1 * diversity)


def _pick_targets(root: Path, n: int) -> list[tuple[str, str | None, str]]:
    """Choose (zoom_level, target_node_id, strategy) for each of N slots.

    Attractiveness-based chain picking v2:
    - Loads the node graph directly (not just INJECTION.md)
    - Scores chains by: descendant count + recency bonus + type diversity
    - Three branching strategies: explore_new | extend_existing | branch_fork
    - Two-agent pipeline: architect (big) + builder (small)

    Returns list of (level, target_id_or_None, strategy).
    """
    import sys as _sys
    plugin_root = Path(__file__).resolve().parent.parent
    proj_src = root / "src"
    if (proj_src / "graph_core").is_dir():
        _sys.path.insert(0, str(proj_src))
    _sys.path.insert(0, str(plugin_root / "src"))

    from collections import defaultdict
    from graph_core.loader import load_directory
    from graph_core.edge import Edge

    out: list[tuple[str, str | None, str]] = []

    # --- Load closed chains ---
    closed_chains: set[str] = set()
    closed_chains_file = root / "closed_chains.txt"
    if closed_chains_file.exists():
        for line in closed_chains_file.read_text().splitlines():
            if line := line.strip():
                closed_chains.add(line)

    # --- Build graph ---
    cfg_path = config_path(root)
    use_sqlite = False
    if cfg_path is not None:
        cfg = json.loads(cfg_path.read_text())
        use_sqlite = cfg.get("persistence", {}).get("type") == "sqlite"

    if use_sqlite:
        from graph_core.persistence.sqlite_backend import SQLiteBackend
        from graph_core.db_loader import DBLoader
        db_path = root / cfg["persistence"]["path"]
        g, loaded = DBLoader(SQLiteBackend(db_path)).load_directory()
    else:
        g, loaded = load_directory(root / "nodes")

    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                try:
                    g.add_edge(Edge(source_id=parent_id, target_id=ln.node.id, relation="spawns"))
                except Exception:
                    pass
                pn = g.get_node(parent_id)
                if pn is not None:
                    pn.children.add(ln.node.id)

    # --- Compute attractiveness scores ---
    # Score = weighted_descendants * recency_boost * type_diversity_bonus
    scores: dict[str, float] = {}

    def _descendant_count(node_id: str, seen: set[str] | None = None) -> int:
        if seen is None:
            seen = set()
        if node_id in seen:
            return 0
        seen.add(node_id)
        n = g.get_node(node_id)
        if n is None or not n.children:
            return 0
        return 1 + sum(_descendant_count(c, seen) for c in n.children if c != node_id)

    def _type_diversity(node_id: str, seen: set[str] | None = None) -> float:
        """Types in subtree / total types. Normalized diversity bonus."""
        if seen is None:
            seen = set()
        if node_id in seen:
            return 0.0
        seen.add(node_id)
        n = g.get_node(node_id)
        if n is None:
            return 0.0
        types = {n.type}
        for c in (n.children or []):
            if c != node_id:
                types |= {_type_diversity(c, seen) > 0}  # just presence flag
        # Simple: count unique types in subtree
        sub_types: set[str] = set()
        stack = [node_id]
        while stack:
            cid = stack.pop()
            if cid in seen:
                continue
            seen.add(cid)
            cn = g.get_node(cid)
            if cn:
                sub_types.add(cn.type)
                stack.extend(cn.children or [])
        return len(sub_types) / max(len(list(g.nodes)), 1)

    for node_id in g.node_ids:
        node = g.get_node(node_id)
        # Recency: leaf nodes with no children get a small boost.
        recency_boost = 1.2 if (node and not node.children) else 1.0
        scores[node_id] = _attractiveness(
            _descendant_count(node_id),
            recency_boost,
            _type_diversity(node_id),
            node.type if node else "",
        )

    # Sort nodes by attractiveness (descending)
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # --- Determine branching strategy per slot ---
    def _pick_strategy(idx: int, total: int) -> str:
        """Decide strategy based on position in the dispatch batch."""
        if idx == 0:
            return "explore_new"  # Always start with fresh exploration
        if idx <= total * 0.3:
            return "extend_existing"  # First 30%: extend best chains
        if idx <= total * 0.6:
            return "branch_fork"  # Next 30%: fork from a mid-ranked chain
        return "explore_new"  # Final 30%: fresh exploration

    # --- Build target list ---
    # Slot 0: big/explore_new (architect agent)
    out.append(("big", None, "explore_new"))

    if n <= 1:
        return out

    # Gather candidates by strategy, excluding closed chains
    extend_candidates = [nid for nid, _score in ranked if nid not in closed_chains and g.get_node(nid) and not g.get_node(nid).is_leaf][:5]
    fork_candidates = [nid for nid, _score in ranked if nid not in closed_chains and g.get_node(nid) and g.get_node(nid).children][:8]

    while len(out) < n:
        strategy = _pick_strategy(len(out), n)

        if strategy == "extend_existing":
            candidates = extend_candidates
        elif strategy == "branch_fork":
            candidates = fork_candidates
        else:
            candidates = [nid for nid, _ in ranked[:10] if nid not in closed_chains]

        if candidates:
            # Round-robin through candidates to spread agents across chains
            t = candidates[(len(out) - 1) % len(candidates)]
            out.append(("small", t, strategy))
        else:
            out.append(("big", None, "explore_new"))

    return out


# hypothesis:l3w4-push-further-loops — the node types a push-further chain
# is mechanically refused to auto-continue into: the quorum-judged tiers.
PUSH_FURTHER_REFUSED_TYPES = frozenset({"overview", "vision", "moral"})


def _target_node_type(root: Path, target: str) -> str | None:
    """The `type:` of the node `target` names, or None when unresolved.

    Resolves through node_writer's id index so an abbreviated id
    (`hypothesis:l3w4-push-further-loops@...`) resolves the same way an aimed
    dispatch's zoom render does. Reads the leading frontmatter line; absent
    type (odd hand-written file) reads as None and is NOT the quorum stop.
    """
    f = node_writer.find_node_file(root, target)
    if not f:
        return None
    try:
        txt = f.read_text()
    except OSError:
        return None
    # frontmatter `type:<sp><value>` — first non-`-` line of the `---` block
    for line in txt.splitlines():
        line = line.strip()
        if line.startswith("type:"):
            return line.split(":", 1)[1].strip()
    return None


def _push_further_gate(root: Path, target: str | None):
    """The push-further refusal, as (exit_code, stderr_msg) or None (allowed).

    hypothesis:l3w4-push-further-loops — a push-further re-dispatch is the
    mechanical stop at the quorum: it needs a --target, and it is refused
    outright when that target is an overview/vision/moral node so the chain
    can never auto-continue INTO quorum-judged territory via the flag. Pure
    and deterministic so the gate is unit-testable without a spawn.
    """
    if not target:
        return (2, "ERR: --push-further requires --target (re-dispatch at the "
                   "same node id)")
    ttype = _target_node_type(root, target)
    if ttype in PUSH_FURTHER_REFUSED_TYPES:
        return (2, f"ERR: --push-further refuses {target}: node type "
                   f"'{ttype}' is quorum-judged; push stops at the quorum")
    return None


def _node_type_for(level: str, target: str | None, role: str | None) -> str:
    """Which chain step this agent is being asked to write.

    Type names are the canonical underscore spellings
    (`context/schemas/[shape].md`); this function used to hold a private
    `NODE_TYPES` tuple that still said `bigger-outcome` / `app-purpose`, which
    is how the corpus ended up with 2 nodes of each hyphenated spelling beside
    17 and 15 of the underscore one. The table now lives in
    `node_writer.CANONICAL_NODE_TYPES` and nowhere else.

    Big zoom writes an `idea`, not a `hypothesis`. `_pick_targets` returns
    `("big", None, ...)` -- a big-zoom agent has no target and therefore no
    parent, and `[hypothesis].md` says `min_parents: 1`, so every big-zoom
    scaffold was an illegal spawn the old un-gated copy wrote anyway. `idea` is
    one of the exactly three parentless-legal shapes in `[shape].md`, and it is
    what the skill already calls slot 0: "a fresh idea or top-level fork".
    """
    if role == "research":
        return "experiment"
    if role == "implementation":
        return "mvp"
    if not target:
        return "idea" if level == "big" else "hypothesis"
    if level == "big":
        return "hypothesis"
    # small zoom: extend from target — the step follows the target's type.
    step = {
        "hypothesis": "experiment",
        "experiment": "verdict",
        "verdict": "mvp",
        "mvp": "outcome",
        "outcome": "bigger_outcome",
    }
    return step.get(target.split(":", 1)[0], "hypothesis")


def _scaffold_node_for_agent(
    root: Path, iter_n: int, agent_id: str, level: str, target: str | None,
    role: str | None = None, stamp: dict | None = None,
    extra_fm: dict | None = None,
) -> dict | None:
    """Decide what node type to scaffold and pre-create the file skeleton.

    Returns `node_writer.NodeWrite.as_info()`, or None when nothing was
    written — a rejected spawn, or a file that already holds real content.

    `stamp` is the resolved identity of the agent this scaffold is FOR
    (hypothesis:l3-scaffold-stamps-spawner-env), forwarded to node_writer so
    the mint stamps the child's row -- role/model/loop/profile/season --
    rather than the DISPATCHER's os.environ a parent handset. Absent means
    node_writer falls back to the env (a hand scaffold).

    goal:s17 -- this function used to carry a duplicated copy of `cli.py
    scaffold`: its own type tuple, its own body prompts and its own
    `write_text()`. That copy was never gated, so a pi-runtime run
    (`driver.sh --max-iters N`) wrote nodes the spawn gate never saw. It now
    calls the one node-writing routine like every other writer. A rejection is
    NOT fatal: the agent is dispatched without a scaffold and writes its own
    node through `cli.py done`, which is gated too.
    """
    import uuid

    node_type = _node_type_for(level, target, role)
    slug = f"{agent_id}-{(uuid.uuid4().hex[:6])}"
    res = node_writer.write_node(
        root, node_type, slug, [target] if target else [],
        stamp=stamp,
        extra_fm=extra_fm,
        on_exists=node_writer.REUSE_SCAFFOLD,
    )
    if not res.written:
        print(f"no scaffold for {agent_id}: {res.status} — {res.reason}",
              file=sys.stderr)
        return None
    return res.as_info()


def _build_pi_args(
    cfg: dict,
    context_file: str,
    agent_id: str,
    iter_n: int,
    sess_dir: Path,
    scaffold_info: dict | None = None,
) -> list[str]:
    """LEGACY SHIM — the pi command now lives in `adapters/pi_adapter.py`.

    Same reasoning as `pi_model_args` above: `tests/test_dispatch.py` asserts
    on this name and its assertions must keep passing unchanged, which is
    `mvp:unified-spawn-path`'s third falsifier. The body moved; the behaviour
    did not.

    **Not the live path.** `main()` goes through `adapters.load(...)`.
    """
    _name, harness = adapters.resolve(cfg)
    return adapters.load(harness["adapter"]).build_command(
        harness=harness,
        tier="kid",
        context_file=context_file,
        agent_id=agent_id,
        iter_n=iter_n,
        sess_dir=sess_dir,
        scaffold=scaffold_info,
        cli_py=CLI_PY,
        skill_prompt=PLUGIN_ROOT / "lib" / "agent-prompt.md",
    )


if __name__ == "__main__":
    sys.exit(main())
