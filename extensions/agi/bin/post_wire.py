#!/usr/bin/env python3
"""post_wire.py — wire agent results back into the node graph after an iteration.

After agents complete (or after heal.py finishes retrying), this script:
1. Reads all agent.json records from the iteration session dir
2. For each agent that returned a verdict:
   - Updates the target node's frontmatter with verdict + confidence
   - Appends the next_edge suggestion to the parent's next_edges list
   - Creates a verdict node if one doesn't already exist for this experiment
3. Emits a wiring report (nodes updated, edges added, conflicts)

Usage:
    post_wire.py <project_root> <iter_n>
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SRC_GRAPH = PLUGIN_ROOT / "src" / "graph_core"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence_gate  # noqa: E402
import locations  # noqa: E402
import node_writer  # noqa: E402
import spawn_gate  # noqa: E402

# --- reuse snapshot-goals.py's write_frontmatter --------------------------
# Loaded by file path (not `import`) because the filename has a hyphen and is
# not a valid module name. Same pattern as decompose-engine.py and
# backfill-mint-ids.py. This is the actual function, never a copy: goal:s14
# swept the duplicate serializers and `test_snapshot_goals.py` asserts
# snapshot-build-site.py never re-grows one -- but the sweep missed this file,
# which kept a private one until 2026-09-01.
_SNAPSHOT_GOALS_PATH = Path(__file__).resolve().parent / "snapshot-goals.py"
_sg_spec = importlib.util.spec_from_file_location("snapshot_goals", _SNAPSHOT_GOALS_PATH)
snapshot_goals = importlib.util.module_from_spec(_sg_spec)
_sg_spec.loader.exec_module(snapshot_goals)
write_frontmatter = snapshot_goals.write_frontmatter


def _find_root(cwd: Path | None = None) -> Path:
    """The graph root for `cwd`, via the one shared resolver (goal:g11.1)."""
    root = locations.find_project_root(cwd)
    if root is None:
        raise SystemExit(f"ERR: no agi project found from {cwd or Path.cwd()}")
    return root


def _load_graph_core():
    """Ensure graph_core is on sys.path."""
    import sys as _sys
    plugin_root = Path(__file__).resolve().parent.parent
    proj_src = Path(_find_root()) / "src"
    if (proj_src / "graph_core").is_dir():
        _sys.path.insert(0, str(proj_src))
    _sys.path.insert(0, str(plugin_root / "src"))
    from graph_core.loader import load_directory
    from graph_core.edge import Edge
    from graph_core.node import Node
    return load_directory, Edge, Node


def _slug_from_node_id(node_id: str) -> str:
    """Extract slug (everything after the type: prefix)."""
    if ":" in node_id:
        return node_id.split(":", 1)[1]
    return node_id


def _node_file_path(root: Path, node_id: str) -> Path | None:
    """Find the .md file for a node_id.

    goal:s17 -- the one lookup, in `node_writer`, beside the one write. This
    copy tried two exact paths and gave up, so it could not resolve **417 of
    the 781 corpus ids** -- 270 of which `cli.py`'s separate copy resolved
    fine. That mattered more here than anywhere: the branch this feeds treats
    "not found" as "no verdict node exists yet" and **creates one**, so every
    unresolved id minted a duplicate instead of updating the node it meant to
    update. 56 of the 270 were verdicts.
    """
    return node_writer.find_node_file(root, node_id)


def _read_frontmatter(body: str) -> tuple[dict, str]:
    """Split YAML frontmatter (between --- markers) from body."""
    if "---\n" not in body and "---\r\n" not in body:
        return {}, body
    parts = body.split("---", 2)
    if len(parts) < 3:
        return {}, body
    import yaml
    fm = yaml.safe_load(parts[1]) or {}
    return fm, parts[2]


def _write_node(path: Path, fm: dict, body: str) -> None:
    """Write frontmatter + body back to a node file.

    Delegates to the one serializer (goal:s14). The private serializer this
    replaced round-tripped every node it wired into a *different* YAML style
    than the corpus is written in: list items lost their two-space indent
    (`- goal:g4` for `  - goal:g4`), `id:` lost its quotes, `title:` was
    re-quoted single, and `"---\\n" + body` on a body that already opens with a
    blank line added a third.

    That is five cosmetic diffs riding along with the one real change, on every
    node wired. It cost more than noise: **the grid records a version per
    changed node**, so wiring an edge minted versions whose entire content was
    quote style, and `grid.py diff` -- which the project reads as a changelog
    of reasoning -- filled with re-indentation. Found 2026-09-01 when a kid's
    one-line `next_edges` addition to `goal:g4.3` arrived as a six-line diff.
    """
    write_frontmatter(path, fm, body)


def _merged_agent(iter_dir: Path, entry: dict) -> dict:
    """Dispatch-time record overlaid with what the kid actually reported.

    This module's own docstring has always said it "reads all agent.json
    records"; the loop read `manifest["agents"]` instead, and the two are not
    the same record. `dispatch.py` writes the manifest **once**, at spawn, so
    its entries carry only dispatch-time fields. `cli.py done` writes the
    kid's results to `<agent_id>/agent.json`. `heal.py` bridges them by
    syncing exactly one field -- `status` -- with a comment saying it does so
    "so post_wire sees current state".

    Everything else the kid reported stayed in `agent.json` and was never
    read: **`verdict`, `confidence`, `evidence_runs` and `notes` were silently
    dropped on every pi run.** The node kept whatever the scaffold gave it,
    which is `verdict: pending`.

    Invisible for as long as it existed because every observed pi verdict
    *was* `pending`, so the dropped value equalled the default. Found
    2026-09-01 the first time a pi kid returned something else: it reported
    `inconclusive_lean_proved:65`, the driver printed that from `agent.json`,
    and the node on disk said `pending`.

    The quiet part is worse than the lost field. `post_wire` applies the
    evidence gate to the verdict it reads here, so a gate fed `None` has
    nothing to demote -- meaning `unevidenced_decisive_verdicts: 0` was never
    evidence of discipline on the pi path, only evidence that no pi verdict
    ever arrived. Same for `evidence_fraction`.

    Merge direction: `agent.json` wins, because it is written later and is the
    only record of what the kid claimed. Falls back to the manifest entry
    alone when there is no `agent.json` -- and reading it here rather than
    relying on `heal.py`'s sync also makes `--no-heal` runs wire correctly,
    which they previously did not.
    """
    agent_id = entry.get("id")
    if not agent_id:
        return entry
    path = iter_dir / str(agent_id) / "agent.json"
    if not path.exists():
        return entry
    try:
        rec = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"WARN: unreadable agent record {path}: {exc}", file=sys.stderr)
        return entry
    if not isinstance(rec, dict):
        return entry
    return {**entry, **{k: v for k, v in rec.items() if v is not None}}


def _gate(agent: dict, fm: dict, corpus):
    """Apply the H4 evidence gate to one agent record (post_wire writer path).

    Evidence count comes from the agent record first (written by `cli.py done`),
    falling back to the node's own `evidence_runs` frontmatter. `corpus` is
    the set of real node ids (`evidence_gate.build_corpus`) evidence_runs
    entries are resolved against (H4c / goal:g3.1).
    """
    runs = agent.get("evidence_runs")
    if runs is None:
        runs = fm.get("evidence_runs")
    res = evidence_gate.apply_gate(
        agent.get("verdict") or "pending",
        runs,
        bypass=str(agent.get("evidence_gate", "")) == "bypassed",
        corpus=corpus,
    )
    evidence_gate.announce(res)
    return res


def cmd_wire(args: argparse.Namespace) -> int:
    root = _find_root()
    iter_dir = root / "sessions" / f"iter-{args.iter_n:03d}"
    manifest_path = iter_dir / "manifest.json"

    if not manifest_path.exists():
        print(f"WARN: no manifest at {manifest_path}, nothing to wire", file=sys.stderr)
        return 0

    manifest = json.loads(manifest_path.read_text())
    load_directory, Edge, Node = _load_graph_core()

    # H4c / goal:g3.1 — the corpus evidence_runs entries resolve against.
    # Built once per wire pass; the node set doesn't change mid-loop (no
    # verdict's own evidence_runs can name a node this same pass creates).
    corpus = evidence_gate.build_corpus(root / "nodes")

    # goal:s17 -- the spawn gate, on post_wire's own node-creating path. Loaded
    # once per pass for the same reason as `corpus`: the schemas do not change
    # mid-loop, and neither does the type of any node this pass reads.
    spawn_rules, type_index = spawn_gate.gate_for_root(root)
    spawn_gate.announce_schema_errors(spawn_rules)

    # Build current graph
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

    updated_nodes: list[str] = []
    added_edges: list[str] = []
    skipped: list[str] = []
    demoted: list[str] = []
    rejected: list[str] = []

    for agent in (_merged_agent(iter_dir, a) for a in manifest.get("agents", [])):
        if agent.get("status") != "done":
            continue
        verdict = agent.get("verdict")
        confidence = agent.get("confidence", 0.5)
        node_id = agent.get("node_id")
        parent = agent.get("parent", "")
        notes = agent.get("notes", "")
        strategy = agent.get("strategy", "unknown")

        if not node_id:
            skipped.append(f"{agent['id']}: no node_id")
            continue

        # 1. Update the node file with verdict
        node_path = _node_file_path(root, node_id)
        if node_path and node_path.exists():
            content = node_path.read_text(encoding="utf-8")
            fm, body = _read_frontmatter(content)
            # H4 evidence gate — this is the second writer path, and it must
            # enforce the same rule as cli.py done.
            gate = _gate(agent, fm, corpus)
            if gate.rejected:
                # H4c: a taxonomy violation (e.g. 'synthetic') is worse than
                # no evidence — reject the whole write, same as cli.py done's
                # exit 2. Nothing about this node or its next_edges changes.
                rejected.append(f"{node_id}: {gate.reason}")
                continue
            verdict = gate.verdict
            if gate.demoted:
                demoted.append(f"{node_id}: {gate.original} -> {gate.verdict}")
            fm["verdict"] = verdict
            fm["confidence"] = confidence
            evidence_gate.stamp(fm, gate)
            fm["wired_at"] = int(time.time())
            fm["wired_from"] = agent["id"]
            if notes:
                body = body.rstrip() + f"\n\n## Agent Notes\n{notes}\n"
            _write_node(node_path, fm, body)
            updated_nodes.append(node_id)
        else:
            # No file yet — create a minimal verdict node. Its slug is the
            # agent id, which is what its `id:` has always been built from; the
            # old code named the FILE after the parent's slug instead, so the
            # path and the id disagreed and two agents wiring verdicts for one
            # parent in the same pass overwrote each other's file while
            # carrying different ids. Deriving both from one slug is what
            # routing through `node_writer` buys.
            gate = _gate(agent, {}, corpus)
            if gate.rejected:
                rejected.append(f"verdict:{agent['id']}: {gate.reason}")
                continue
            verdict = gate.verdict
            if gate.demoted:
                demoted.append(f"verdict:{agent['id']}: {gate.original} -> {gate.verdict}")
            # goal:s17 -- the only place post_wire *creates* a node rather than
            # updating one, so it is the only place a spawn rule can be broken
            # here. It goes through `node_writer.write_node` like every other
            # writer, which runs the gate before touching the filesystem and
            # mints the `mint_id` goal:s14 requires (this path minted none, so
            # every verdict it wrote was skipped by `grid.py commit --all`).
            # `node_id` is the parent; it is the id whose file was not found
            # above, so it very often resolves to nothing, which the gate
            # reports as `unverified` (write, warn) rather than rejecting --
            # inferring a parent is inventing one (G7.1).
            extra = {
                "verdict": verdict,
                "confidence": confidence,
                "wired_from": agent["id"],
                "wired_at": int(time.time()),
            }
            evidence_gate.stamp(extra, gate)
            res = node_writer.write_node(
                root, "verdict", agent["id"], [node_id] if node_id else [],
                extra_fm=extra, body=notes or "",
                rules=spawn_rules, type_index=type_index,
                bypass=str(agent.get("spawn_gate", "")) == "bypassed",
            )
            if res.rejected:
                rejected.append(f"{res.node_id}: {res.reason}")
                continue
            updated_nodes.append(res.node_id)

        # 2. Update parent's next_edges if parent exists
        if parent:
            parent_path = _node_file_path(root, parent)
            if parent_path and parent_path.exists():
                pcontent = parent_path.read_text(encoding="utf-8")
                pfm, pbody = _read_frontmatter(pcontent)
                next_edges = pfm.get("next_edges", [])
                if isinstance(next_edges, list):
                    # Must be plain node ID string for find_chains() compatibility
                    if node_id not in next_edges:
                        next_edges.append(node_id)
                        pfm["next_edges"] = next_edges
                        _write_node(parent_path, pfm, pbody)
                        added_edges.append(f"{parent} -> {node_id} [{strategy}]")
                        # Also update graph in memory for downstream use
                        if g.has_node(parent) and g.has_node(node_id):
                            try:
                                g.add_edge(
                                    Edge(
                                        source_id=parent,
                                        target_id=node_id,
                                        relation="next",
                                    )
                                )
                            except Exception:
                                pass

    # 3. Persist updated graph back (so subsequent iterations see wired edges)
    #    We write a .graph.json snapshot alongside the manifest
    graph_path = iter_dir / f"iter-{args.iter_n:03d}-graph.json"
    graph_data = {
        "nodes": [
            {
                "id": n.id,
                "type": n.type,
                "parents": list(n.parents),
                "children": list(n.children),
                "tags": list(n.tags),
            }
            for n in g.nodes
        ],
        "edges": [
            {"source": e.source_id, "target": e.target_id, "relation": e.relation}
            for e in g.edges
        ],
    }
    graph_path.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")

    # 4. Emit wiring report
    print(f"[post_wire] iter={args.iter_n}")
    print(f"  nodes updated: {len(updated_nodes)}")
    for n in updated_nodes:
        print(f"    - {n}")
    print(f"  edges added: {len(added_edges)}")
    for e in added_edges:
        print(f"    - {e}")
    if demoted:
        print(f"  evidence-gate demotions: {len(demoted)}")
        for d in demoted:
            print(f"    - {d}")
    if rejected:
        # Two gates feed this list now: the evidence gate (H4c taxonomy
        # violation) and the spawn gate (goal:s17). Each entry carries its own
        # reason string naming which rule and which schema file, so the label
        # stays generic rather than claiming a cause it cannot know.
        print(f"  gate rejections (nothing written): {len(rejected)}")
        for r in rejected:
            print(f"    - {r}")
    if skipped:
        print(f"  skipped: {len(skipped)}")
        for s in skipped:
            print(f"    - {s}")
    print(f"  graph snapshot: {graph_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Wire agent verdicts back into the node graph.")
    ap.add_argument("project_root", nargs="?")
    ap.add_argument("iter_n", type=int)
    args = ap.parse_args()

    if args.project_root:
        import os
        os.chdir(args.project_root)

    return cmd_wire(args)


if __name__ == "__main__":
    sys.exit(main())
