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


def zoom_command(root: Path, iter_n: int, agent_id: str,
                 level: str, target: str | None) -> list[str]:
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
    return cmd


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


def resolve_role_spec(cfg: dict, roles: list | None, tier: int,
                      role: str) -> dict:
    """Resolve (tier, role) to {harness, model, effort, settings, from_ladder}.

    A row in `roles` matching both keys wins; its empty/short cells resolve
    to None (no flag). With no row (or no table at all) the historical
    config path answers: `harness` from `adapters.resolve`, `model` from
    `harnesses.<h>.models[role]`, `effort` from `harnesses.<h>.effort[role]`.
    `from_ladder` distinguishes the source so callers can report it.
    """
    row = None
    for r in (roles or []):
        try:
            if int(r.get("tier")) == int(tier) and r.get("role") == role:
                row = r
                break
        except (TypeError, ValueError):
            continue
    if row is not None:
        return {
            "harness": row.get("harness") or None,
            "model": (row.get("model") or "").strip() or None,
            "effort": (row.get("effort") or "").strip() or None,
            "settings": row.get("settings") or None,
            "from_ladder": True,
        }
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
        "settings": None,
        "from_ladder": False,
    }


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
        "--list-rows",
        action="store_true",
        help="Dry print: resolve every role in the ladder's roles table and "
             "exit without spawning (hypothesis:l3w0-ladder-roles-table)",
    )
    ap.add_argument(
        "--detach",
        action="store_true",
        help="Skip the reaper phase and return immediately after spawn. "
             "The caller (e.g. a parent agent) polls cli.py status to "
             "detect completion. Without this flag dispatch blocks until "
             "all agents finish or the timeout expires.",
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

    # goal:g11.1 — resolve the given path the way every entry point resolves
    # cwd, rather than demanding it already BE the graph root. Identity on a
    # legacy root (phase 1), so no existing project resolves differently.
    given = Path(args.project_root).resolve()
    root = locations.find_project_root(given)
    cfg_path = locations.config_path(root) if root is not None else None
    if cfg_path is None:
        print(f"ERR: not an agi project: {given}", file=sys.stderr)
        return 1
    cfg = json.loads(cfg_path.read_text())

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
        dispatch_harness = harness
        if _spec["from_ladder"]:
            if _spec["harness"] and _spec["harness"] != harness_name:
                # A ladder row may name a different harness (e.g. an opus
                # parent on claude-code while the invocation defaulted to pi).
                harness_name, dispatch_harness = adapters.resolve(
                    cfg, _spec["harness"])
                dispatch_harness = dict(dispatch_harness)
            else:
                dispatch_harness = dict(harness)
            _models = dict(dispatch_harness.get("models") or {})
            if _spec["model"]:
                # Keyed by the adapter's tier string so model_args(harness,
                # args.tier) returns the ladder row's model.
                _models[args.tier] = _spec["model"]
            dispatch_harness["models"] = _models
            if _spec["effort"]:
                dispatch_harness["effort"] = {args.tier: _spec["effort"]}
            if _spec["settings"]:
                dispatch_harness["settings"] = _spec["settings"]
        else:
            print(f"roles: no ladder row for (tier={tier_eff}, "
                  f"role={args.role}); falling back to config "
                  f"harnesses.{harness_name}.models[{args.tier}]")
        if _spec["from_ladder"]:
            print(f"roles: tier={tier_eff} role={args.role} -> "
                  f"{_spec['harness']}/{_spec['model'] or '-'}/"
                  f"effort={_spec['effort'] or '-'}/settings={_spec['settings'] or '-'}")
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

    iter_dir = locations.iteration_dir(root, args.iter_n)
    iter_dir.mkdir(parents=True, exist_ok=True)

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

        zoom_cmd = zoom_command(root, args.iter_n, agent_id, level, target)
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
            scaffold_info = _scaffold_node_for_agent(
                root, args.iter_n, agent_id, level, target, role)
            if scaffold_info:
                print(f"scaffolded {scaffold_info['node_type']} node: {scaffold_info['node_id']}")

        # Spawn pi (detached). Output -> sess_dir/output.log
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
                cli_py=CLI_PY,
                skill_prompt=PLUGIN_ROOT / "lib" / "agent-prompt.md",
                # goal:g1.9 / goal:g4.8 -- a parent brief needs the spawn
                # command, its aim, and the concurrency bound. A kid brief
                # ignores all three; passing them unconditionally keeps the
                # call site tier-blind, which is the point of the assembler.
                dispatch_py=Path(__file__).resolve(),
                target=target,
                parallel=adapters.parallelism(cfg),
                max_live=cap,
                # hypothesis:l3-cc-tools-by-tier -- who this agent is on the
                # ladder selects its tool bundle (kids keep the closed list;
                # advisors/directors add the ultracode/loop tools).
                role=args.role,
                ladder_tier=tier_eff,
            )
            spawn_env = adapter.child_env(harness=dispatch_harness, base=scrubbed_env(),
                                           tier=args.tier)
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
                spawn_env["AGI_PROJECT_ROOT"] = str(root.resolve())
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
            spawn_budget.release(lease)
            return 1
        except (KeyError, NotImplementedError) as exc:
            # A tier with no model, or a declared-but-unimplemented harness.
            # Both are config errors and both must name what is missing rather
            # than surfacing a traceback from inside an adapter.
            print(f"ERR: harness {harness_name!r} cannot spawn tier "
                  f"{args.tier!r}: {exc}", file=sys.stderr)
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
                    cwd=str(root),
                    env=spawn_env,
                )
        except BaseException:
            # Nothing was started, so nothing holds the slot. Give it back
            # now rather than leaving it to expire with this process.
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
        }
        if scaffold_info:
            agent_record["node_id"] = scaffold_info.get("node_id", "")
            agent_record["parent"] = scaffold_info.get("parent", "")
        (sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))
        # goal:s28 — merge by agent id rather than append.
        # When re-dispatching the same agent (e.g. healing), update in place.
        existing = [i for i, a in enumerate(manifest["agents"]) if a.get("id") == agent_id]
        if existing:
            manifest["agents"][existing[0]] = agent_record
        else:
            manifest["agents"].append(agent_record)
        new_records.append(agent_record)
        print(f"spawned {agent_id} pid={proc.pid} harness={harness_name} "
              f"tier={args.tier} level={level} target={target or '-'} "
              f"strategy={strategy}")

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
    """
    import json
    import time

    TERMINAL = {"done", "pending", "hung-healed", "failed"}
    deadline = time.time() + max_wait_s

    while time.time() < deadline:
        manifest_path = iter_dir / "manifest.json"
        if not manifest_path.exists():
            break
        try:
            manifest = json.loads(manifest_path.read_text())
        except (json.JSONDecodeError, OSError):
            break

        all_terminal = True
        updated = False
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

            pid = int(rec.get("pid", 0))
            if pid > 0 and not adapter.is_alive(pid):
                outcome = _reap_one(root, iter_dir, adapter, rec, agent_id, pid,
                                    cap=cap, cfg=cfg)
                rec.update(outcome["record"])
                agent_json_path.write_text(json.dumps(rec, indent=2))  # session artefact: agent.json
                entry["status"] = rec["status"]
                if rec.get("pid"):
                    entry["pid"] = rec["pid"]
                updated = True
                print(f"reaper: {outcome['message']}")

        if updated:
            manifest_path.write_text(json.dumps(manifest, indent=2))  # session artefact: manifest.json
        if all_terminal:
            break
        time.sleep(5)

    print("reaper: finished")


def _reap_one(root, iter_dir, adapter, rec, agent_id, pid, cap=1, cfg=None):
    """Decide what a dead agent's death means. Returns `{record, message}`.

    **The filesystem is consulted before the restart, and that ordering is the
    load-bearing part** (`goal:g4.7`). A kid that died after writing its node
    lost only its report; respawning it would redo finished work and hand a
    second agent the same scaffolded node.
    """
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
    lease = spawn_budget.acquire(root, cap, f"{agent_id}-r{restarts + 1}",
                                 tier=rec.get("tier", "kid"))
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
        desc = _descendant_count(node_id)
        node = g.get_node(node_id)
        # Recency: leaf nodes with no children get a small boost (untested = potential)
        recency_boost = 1.2 if (node and not node.children) else 1.0
        diversity = _type_diversity(node_id)
        # Type weighting: hypothesis and experiment are high-value chain starts
        type_weight = {"hypothesis": 1.4, "experiment": 1.2, "verdict": 1.1}.get(
            node.type if node else "", 1.0
        )
        scores[node_id] = desc * recency_boost * type_weight * (1.0 + 0.1 * diversity)

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
    root: Path, iter_n: int, agent_id: str, level: str, target: str | None, role: str | None = None
) -> dict | None:
    """Decide what node type to scaffold and pre-create the file skeleton.

    Returns `node_writer.NodeWrite.as_info()`, or None when nothing was
    written — a rejected spawn, or a file that already holds real content.

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
