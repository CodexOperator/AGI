#!/usr/bin/env python3
"""dispatch.py — spawn N pi agents in parallel with zoom-targeted contexts.

Reads <project>/agi-tree.config.json for parallelism + model.
Writes session manifest at <project>/sessions/iter-NNN/manifest.json so
heal.py can detect timeouts.

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
import json
import os
import random
import shlex
import subprocess
import sys
import time
import uuid
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent  # extensions/agi
ZOOM_PY = PLUGIN_ROOT / "bin" / "zoom.py"
CLI_PY = PLUGIN_ROOT / "bin" / "cli.py"

# Canonical name first; the legacy name stays accepted during the rename window.
CONFIG_NAMES = ("agi-tree.config.json", "autoresearch-tree.config.json")


def config_path(root: Path) -> Path | None:
    """First existing config file in `root`, or None if it is not a project."""
    for name in CONFIG_NAMES:
        p = root / name
        if p.exists():
            return p
    return None


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
)


def _scrubbed_env() -> dict[str, str]:
    """Inherited env minus Claude-Code-injected Anthropic credentials."""
    env = {k: v for k, v in os.environ.items() if k not in ENV_VARS_TO_SCRUB}
    return env


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=int)
    ap.add_argument(
        "--template",
        default=None,
        help="Override pipeline_template from config (e.g. 'research', 'builder-first')",
    )
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    cfg_path = config_path(root)
    if cfg_path is None:
        print(f"ERR: no {CONFIG_NAMES[0]} in {root}", file=sys.stderr)
        return 1
    cfg = json.loads(cfg_path.read_text())

    n = int(cfg.get("agent_dispatch", {}).get("claude_max_parallel", 1))
    big_split = float(cfg.get("big_idea_vs_small_idea_split", 0.3))
    timeout_min = int(cfg.get("agent_timeout_mins", 10))
    pipeline_template = args.template or cfg.get("pipeline_template")

    iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"
    iter_dir.mkdir(parents=True, exist_ok=True)

    # Two-agent research pipeline: architect (slot 0) + builder (slot 1)
    # Slot 1 waits for slot 0 to produce a node, then implements it.
    if pipeline_template == "research" and n < 2:
        print(f"ERR: pipeline_template=research requires claude_max_parallel>=2, got {n}", file=sys.stderr)
        return 1

    if pipeline_template == "research":
        targets = _research_pipeline_targets(root, n, iter_dir)
    else:
        targets = _pick_targets(root, n)

    manifest = {
        "iter": args.iter_n,
        "started_at": int(time.time()),
        "timeout_seconds": timeout_min * 60,
        "agents": [],
        "pipeline_template": pipeline_template,
    }

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

        # Build zoom context
        zoom_cmd = ["python3", str(ZOOM_PY), str(root), str(args.iter_n), agent_id, "--level", level]
        if level == "small" and target:
            zoom_cmd.extend(["--target", target])
        ctx_path = subprocess.run(zoom_cmd, capture_output=True, text=True, check=True).stdout.strip()

        # Scaffold a node file before agent starts — agent fills body only
        scaffold_info = _scaffold_node_for_agent(root, args.iter_n, agent_id, level, target, role)
        if scaffold_info:
            print(f"scaffolded {scaffold_info['node_type']} node: {scaffold_info['node_id']}")

        # Spawn pi (detached). Output -> sess_dir/output.log
        pi_args = _build_pi_args(cfg, ctx_path, agent_id, args.iter_n, sess_dir, scaffold_info)
        log_file = sess_dir / "output.log"
        with open(log_file, "wb") as logf:
            proc = subprocess.Popen(
                pi_args,
                stdout=logf,
                stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
                cwd=str(root),
                env=_scrubbed_env(),
            )
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
            "command": " ".join(shlex.quote(a) for a in pi_args),
        }
        if scaffold_info:
            agent_record["node_id"] = scaffold_info.get("node_id", "")
            agent_record["parent"] = scaffold_info.get("parent", "")
        (sess_dir / "agent.json").write_text(json.dumps(agent_record, indent=2))
        manifest["agents"].append(agent_record)
        print(f"spawned {agent_id} pid={proc.pid} level={level} target={target or '-'} strategy={strategy}")

    (iter_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"manifest: {iter_dir / 'manifest.json'}")
    return 0


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


def _scaffold_node_for_agent(
    root: Path, iter_n: int, agent_id: str, level: str, target: str | None, role: str | None = None
) -> dict | None:
    """Decide what node type to scaffold and pre-create the file skeleton.

    Returns a dict with node_type, node_id, parent, slug or None if nothing to scaffold.
    """
    import uuid

    NODE_TYPES = ("hypothesis", "experiment", "verdict", "mvp", "outcome", "bigger-outcome", "app-purpose")

    # Pick node type based on target type, or override via role
    if role == "research":
        node_type = "experiment"
    elif role == "implementation":
        node_type = "mvp"
    elif level == "big":
        node_type = "hypothesis"
    else:
        # small zoom: extend from target — decide step based on target type
        if target:
            if target.startswith("hypothesis:"):
                node_type = "experiment"
            elif target.startswith("experiment:"):
                node_type = "verdict"
            elif target.startswith("verdict:"):
                node_type = "mvp"
            elif target.startswith("mvp:"):
                node_type = "outcome"
            elif target.startswith("outcome:"):
                node_type = "bigger-outcome"
            else:
                node_type = "hypothesis"
        else:
            node_type = "hypothesis"

    # Generate slug
    slug = f"{agent_id}-{(uuid.uuid4().hex[:6])}"
    node_id = f"{node_type}:{slug}"
    parent = target or ""

    # Write the scaffold file
    type_dir = node_type.replace("-", "_")
    node_dir = root / "nodes" / type_dir
    node_dir.mkdir(parents=True, exist_ok=True)
    node_file = node_dir / f"{slug}.md"

    prompts = {
        "hypothesis": "## Hypothesis\n\nWhat is the testable claim?\nWhat would prove it? What would disprove it?\n\n",
        "experiment": "## Experiment\n\nWhat did you do? What happened?\nInclude command/inputs and actual outputs.\n\n## Evidence\n\nRaw output, logs.\n\n",
        "verdict": "## Verdict\n\nproved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N\n\n## Evidence\n\nWhat supports this?\n\n## Confidence\n\n0.0 – 1.0\n\n",
        "mvp": "## MVP\n\nWhat does this do?\n\n## Inputs\n\nWhat does it take?\n\n## Outputs\n\nWhat does it produce?\n\n",
        "outcome": "## Outcome\n\nInput shape:\n\nOutput shape:\n\nBehavior:\n\nEdge cases:\n\n",
        "bigger-outcome": "## Bigger Outcome\n\nWhat purpose does this serve?\n\n",
        "app-purpose": "## App Purpose\n\nTop-level mission?\n\n",
    }

    # Check if file exists and has real content (not just scaffold prompts)
    if node_file.exists():
        existing = node_file.read_text()
        # Split on second --- to get body content
        parts = existing.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()
            # If body is just the scaffold prompt (empty/minimal), overwrite it
            # Otherwise content exists → return None to preserve it
            if body not in prompts.get(node_type, ""):
                return None
        else:
            # Malformed file, overwrite with fresh scaffold
            pass

    body = prompts.get(node_type, "")
    fm = [
        "---",
        f"id: {node_id}",
        f"type: {node_type}",
        f"parents:\n  - {parent}",
        "next_edges: []",
        "---",
        "",
        f"# {node_id}",
        "",
    ]
    node_file.write_text("\n".join(fm) + body)
    return {"node_type": node_type, "node_id": node_id, "parent": parent, "slug": slug, "path": str(node_file)}


def _build_pi_args(
    cfg: dict,
    context_file: str,
    agent_id: str,
    iter_n: int,
    sess_dir: Path,
    scaffold_info: dict | None = None,
) -> list[str]:
    dispatch_cfg = cfg.get("agent_dispatch", {})
    pi_bin = os.environ.get("PI_BIN", "/home/ubuntu/.npm-global/bin/pi")
    args = [
        pi_bin,
        "--append-system-prompt", f"@{context_file}",
        "--append-system-prompt", (
            f"You are agent {agent_id} on iteration {iter_n}. "
            f"Your job: fill in the scaffolded node file below, then signal done."
        ),
    ]
    if scaffold_info:
        args.extend([
            "--append-system-prompt", (
                f"SCAFFOLDED NODE FILE: {scaffold_info['path']}\n"
                f"Node type: {scaffold_info['node_type']}  "
                f"Node ID: {scaffold_info['node_id']}  "
                f"Parent: {scaffold_info['parent']}\n"
                f"FILL IN the body of that file. Do NOT rewrite frontmatter.\n"
                f"When done, run: python3 {CLI_PY} done {iter_n} {agent_id} "
                f"--verdict <state> --confidence <0..1> --node-id {scaffold_info['node_id']} "
                f"--parent {scaffold_info['parent']}"
            ),
        ])
    else:
        args.extend([
            "--append-system-prompt", (
                f"When complete, run: python3 {CLI_PY} done {iter_n} {agent_id} "
                f"--verdict <state> --confidence <0..1> --node-id <id> --parent <parent>"
            ),
        ])
    # Allow extra prompt-from-skill
    skill_prompt = (PLUGIN_ROOT / "lib" / "agent-prompt.md")
    if skill_prompt.exists():
        args.extend(["--append-system-prompt", f"@{skill_prompt}"])
    # Initial user message: the task
    args.append(f"Begin iteration {iter_n} as agent {agent_id}. Read your zoom context, do the work, signal done.")
    return args


if __name__ == "__main__":
    sys.exit(main())
