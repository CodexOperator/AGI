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
import completion  # noqa: E402
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


class MalformedNode(Exception):
    """This text opens frontmatter and does not close it, or will not parse.

    Distinct from "has no frontmatter at all", which is a legitimate shape and
    still returns `({}, text)`. The distinction is the whole point: `cmd_wire`
    WRITES BACK what this returns, so conflating the two silently rewrites a
    node it could not read.
    """


def _read_frontmatter(body: str) -> tuple[dict, str]:
    """Split YAML frontmatter (between --- markers) from body.

    Raises `MalformedNode` rather than returning `({}, whole_text)` for input
    that opens frontmatter it cannot parse. `mvp:a00-8a013aaf-ca2434` calls
    this the right default for a *write-adjacent* caller, and the measurement
    behind that is concrete (verified 2026-09-01):

        in    ---\\nid: experiment:e1\\nmint_id: deadbeef\\n...   (no closing ---)
        old   fm={} , body = the ENTIRE file
        write ---\\nmint_id: <FRESHLY MINTED>\\nverdict: proved\\n---
              ---\\nid: experiment:e1\\nmint_id: deadbeef\\n...   (now body text)

    So the quiet branch did not lose one node's wiring -- it rewrote the node,
    **minted a new `mint_id`**, and demoted the real one into prose. `mint_id`
    is the identifier this project says never changes and the key its grid refs
    hang off, so that both invented an identity and orphaned a ref. A candidate
    mechanism for part of the 262 orphaned refs counted the same day.

    The other branch was a bare `yaml.YAMLError` escaping into `cmd_wire`,
    which is in the loop's critical path -- one malformed node lost the whole
    iteration's wiring. Both now surface as one catchable class, which is the
    MVP's "raise is ONE class" clause: a caller writes a single `except`.
    """
    if "---\n" not in body and "---\r\n" not in body:
        return {}, body          # no frontmatter at all — legitimate, not malformed
    parts = body.split("---", 2)
    if len(parts) < 3:
        raise MalformedNode("frontmatter opened but never closed")
    import yaml
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise MalformedNode(f"frontmatter is not valid YAML: {exc}") from exc
    if not isinstance(fm, dict):
        # A list or scalar reaches the caller as an AttributeError on .get()
        # otherwise — the fourth, unmodeled branch.
        raise MalformedNode(f"frontmatter parsed to {type(fm).__name__}, not a mapping")
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


def _update_via_writer(root, node_id, path, original_fm, fm,
                       original_body, body) -> None:
    """Route one wire through `node_writer.update_node` (`goal:g13`).

    `post_wire` reads a node, mutates a dict, and writes the whole thing back.
    `update_node` takes a **delta**, so the delta is computed here by diffing
    the mutated frontmatter against what was read -- rather than by listing the
    keys this function believes it changed. That distinction is load-bearing:
    `evidence_gate.stamp()` writes keys this call site does not name, and a
    hand-listed delta would silently drop exactly the demotion stamps the gate
    exists to record.

    Three things the caller gains by going through the gate instead of
    `write_frontmatter` directly:

    1. An authored `THOUGHT` cannot be lost, on the one path that rewrites a
       body (it appends `## Agent Notes`).
    2. An update that changes nothing writes nothing. This path runs on every
       completed node every iteration, so an unconditional rewrite would mint
       a grid version per node per iteration and *versions record change, not
       time* would stop being true.
    3. An edit that would REMOVE a required field is refused; one that merely
       arrives at an already-invalid node is not (`goal:s31` left 115 of
       those, and refusing to record their verdicts would punish the wrong
       write).

    Falls back to the direct serializer on rejection, with a report. A wire
    that cannot be recorded is worse than one recorded outside the gate --
    `goal:g7`'s invariant is that nothing the loop produces is silently lost,
    and it outranks this one.
    """
    unset = [k for k in original_fm if k not in fm]
    changed = {k: v for k, v in fm.items()
               if k not in original_fm or original_fm[k] != v}
    new_body = None if body == original_body else body
    if not changed and not unset and new_body is None:
        return
    res = node_writer.update_node(root, node_id, set_fm=changed,
                                  unset_fm=unset, body=new_body)
    if res.status == node_writer.REJECTED:
        print(f"warn: gated write refused for {node_id} ({res.reason}); "
              f"writing directly so the wire is not lost", file=sys.stderr)
        _write_node(path, fm, body)


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

    Verdict and evidence count come from the node's own frontmatter first
    (mvp:unified-spawn-path clause 5 — the kid writes what it claimed into its
    node, and `cli.py done` stamps the same values there at announce time),
    with the `agent.json` record as fallback. The scaffold itself never
    carries a `verdict:` or `evidence_runs:` key, so a kid that never
    reported still falls through to `pending` exactly as before; a kid that
    reported only via `cli.py done` is read identically, because `done`
    stamps the node and the record with the same gated values in one pass.
    `corpus` is the set of real node ids (`evidence_gate.build_corpus`)
    evidence_runs entries are resolved against (H4c / goal:g3.1).
    """
    # `pending` in the node is the ABSENCE of a claim, not a claim of its own,
    # so it must not outrank a verdict the agent actually reported. Written as
    # `fm.get("verdict") or agent.get(...)` this read `pending` as truthy and
    # silently discarded the agent's real verdict.
    fm_verdict = fm.get("verdict")
    if fm_verdict in (None, "", "pending"):
        fm_verdict = None
    verdict = fm_verdict or agent.get("verdict") or "pending"

    # Only a LIST in the node is a claim. `evidence_gate.stamp` writes back the
    # normalized COUNT (`evidence_runs: 1`), so on a second wire the node holds
    # an int -- and `normalize_evidence_runs` resolves an int to 0 by design
    # (goal:g7.3: a count nothing can check certifies nothing). Preferring the
    # node's int over the agent's list therefore DEMOTED an earned `proved` to
    # `inconclusive_lean_proved:50` on every re-wire. Latent only because
    # nothing re-wires today.
    runs = fm.get("evidence_runs")
    if not isinstance(runs, (list, tuple, set)):
        runs = agent.get("evidence_runs", runs)
    res = evidence_gate.apply_gate(
        verdict,
        runs,
        bypass=str(fm.get("evidence_gate") or agent.get("evidence_gate", "")) == "bypassed",
        corpus=corpus,
        # Who is claiming, and what kind of node it is: an `experiment` IS its
        # own run and may cite itself; a `verdict` must cite the experiments it
        # judges. Without these the gate cannot tell the two apart.
        self_id=fm.get("id") or agent.get("node_id"),
        node_type=fm.get("type"),
    )
    evidence_gate.announce(res)
    return res


def cmd_wire(args: argparse.Namespace) -> int:
    root = _find_root()
    iter_dir = locations.iteration_dir(root, args.iter_n)
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
    spawn_rules, type_index, _ = spawn_gate.gate_for_root(root)
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
    admitted_by_graph: list[str] = []

    for agent in (_merged_agent(iter_dir, a) for a in manifest.get("agents", [])):
        node_id = agent.get("node_id")
        # goal:g4.6 clause 5 -- completion is a GRAPH event, not a process one.
        # `status == "done"` means `cli.py done` ran, which is one way to
        # announce finishing and not the definition of it. A kid that filled
        # its node and then died -- API error, content filter, killed pid --
        # is finished, and its work was previously dropped here: `heal.py`
        # stamps `failed (pid disappeared without completion signal)` and this
        # filter skipped it, so the node sat on disk unwired.
        #
        # That is not hypothetical. On 2026-09-01 the kid that WROTE
        # `completion.py` died on a provider 403 immediately after, was marked
        # failed, and produced `nodes updated: 0` -- the loss this check
        # prevents, suffered by the change that prevents it.
        owns = agent.get("owns") or []
        finished = agent.get("status") == "done"
        if not finished and node_id and completion.is_complete(root, node_id):
            finished = True
            admitted_by_graph.append(f"{agent['id']}: {node_id}")
        # goal:s27 -- a parent authors no node, so the graph event that means
        # "this agent finished" is its KIDS' nodes acquiring content. Same
        # predicate, applied to what the parent is responsible for.
        if not finished and not node_id and completion.owns_all_complete(root, owns):
            finished = True
            admitted_by_graph.append(f"{agent['id']}: owns {', '.join(owns)}")
        if not finished:
            continue
        # A parent's record carries no verdict to wire and no node to update.
        # It is not skipped-with-an-error: it did its job, and its job left
        # its marks on its kids' nodes rather than on one of its own.
        if not node_id and owns:
            admitted_by_graph.append(
                f"{agent['id']}: parent, owns {len(owns)} node(s), nothing to wire")
            continue
        verdict = agent.get("verdict")
        confidence = agent.get("confidence", 0.5)
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
            try:
                fm, body = _read_frontmatter(content)
                original_fm, original_body = dict(fm), body
            except MalformedNode as exc:
                # Skip WITH a report, never write. Writing back what we could
                # not read is what re-headered the node and minted it a new
                # identity; crashing here would cost the whole iteration.
                skipped.append(f"{node_id}: unreadable, left untouched — {exc}")
                continue
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
            if fm.get("confidence") is not None:
                # clause 5 — the sibling of the gate's own precedence: the
                # node's own stamp beats the agent record's.
                confidence = fm["confidence"]
            fm["verdict"] = verdict
            fm["confidence"] = confidence
            evidence_gate.stamp(fm, gate)
            fm["wired_at"] = int(time.time())
            fm["wired_from"] = agent["id"]
            # Idempotent: `cli.py done` may already have written this exact
            # section. Appending unconditionally is what put the notes in
            # twice on every kid for as long as both writers have existed.
            if notes and notes.strip() not in body:
                body = body.rstrip() + f"\n\n## Agent Notes\n{notes}\n"
            _update_via_writer(root, node_id, node_path,
                               original_fm, fm, original_body, body)
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
                try:
                    pfm, pbody = _read_frontmatter(pcontent)
                except MalformedNode as exc:
                    skipped.append(
                        f"{parent}: parent unreadable, edge not written — {exc}")
                    continue
                next_edges = pfm.get("next_edges", [])
                if isinstance(next_edges, list):
                    # Must be plain node ID string for find_chains() compatibility
                    if node_id not in next_edges:
                        next_edges.append(node_id)
                        pfm["next_edges"] = next_edges
                        _update_via_writer(root, parent, parent_path,
                                           {"next_edges": None}, pfm,
                                           pbody, pbody)
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
    # `iter-007-graph.json` for a legacy id, `iter-L1.08-graph.json` for a
    # loop-scoped one: the directory name is already the formatted id.
    graph_path = iter_dir / f"{iter_dir.name}-graph.json"
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
    if admitted_by_graph:
        # Say it loudly: these kids never signalled, and were wired anyway
        # because their node is real. Silence here would hide both the
        # recovery and whatever killed the kid.
        print(f"  admitted by graph completion (no cli.py done): "
              f"{len(admitted_by_graph)}")
        for a in admitted_by_graph:
            print(f"    - {a}")
    if skipped:
        print(f"  skipped: {len(skipped)}")
        for s in skipped:
            print(f"    - {s}")
    print(f"  graph snapshot: {graph_path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Wire agent verdicts back into the node graph.")
    ap.add_argument("project_root", nargs="?")
    ap.add_argument("iter_n", type=locations.iteration_id)
    args = ap.parse_args()

    if args.project_root:
        import os
        os.chdir(args.project_root)

    return cmd_wire(args)


if __name__ == "__main__":
    sys.exit(main())
