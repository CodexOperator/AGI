#!/usr/bin/env python3
"""
Experiment: demonstrate that post_wire.py's graph.json write is a plain
overwrite (no merge) while dispatch._merge_manifest protects manifest.json.

This is the specific gap that experiment:a00-db9ea0ae-d8251b predicted
but did not test dynamically. Runs against a tmpdir copy; touches no live
.agi/sessions data.
"""

import json, os, sys, tempfile, textwrap
from pathlib import Path

os.chdir("/home/ubuntu/work/agi")

sys.path.insert(0, "extensions/agi/bin")
from dispatch import _merge_manifest

TMP = Path(tempfile.mkdtemp(prefix="cliobber-test-"))
print(f"tmpdir: {TMP}\n")

# --- phase 1: MANIFEST overwrite test (dispatch._merge_manifest) ------------
print("=== PHASE 1: manifest.json — dispatch._merge_manifest ===")

iter_dir = TMP / "sessions" / "iter-001"
iter_dir.mkdir(parents=True)

# Write an initial manifest with one agent
original_manifest = {
    "iter": 1,
    "started_at": 1000,
    "agents": [
        {"id": "a00-original-before-clobber", "status": "done", "cmd": "echo"}
    ],
}
(iter_dir / "manifest.json").write_text(json.dumps(original_manifest, indent=2))
print(f"Before: {len(json.loads((iter_dir / 'manifest.json').read_text())['agents'])} agent(s)")
before_ids = {a["id"] for a in json.loads((iter_dir / "manifest.json").read_text())["agents"]}

# Simulate a second dispatch into the same iter_dir
new_agent = [{"id": "a00-second-dispatch-agent", "status": "running", "cmd": "echo2"}]
merged = _merge_manifest(iter_dir, {"iter": 1, "started_at": 2000}, new_agent)
(iter_dir / "manifest.json").write_text(json.dumps(merged, indent=2))

after = json.loads((iter_dir / "manifest.json").read_text())
after_ids = {a["id"] for a in after["agents"]}
print(f"After:  {len(after['agents'])} agent(s)")
print(f"Original agent preserved: {before_ids.issubset(after_ids)}")
print(f"New agent present: {'a00-second-dispatch-agent' in after_ids}")
manifest_ok = before_ids.issubset(after_ids) and "a00-second-dispatch-agent" in after_ids
print(f"Verdict: MANIFEST {'✅ PROTECTED (merge by id)' if manifest_ok else '❌ DATA LOST'}")
print()

# --- phase 2: GRAPH.JSON overwrite test (post_wire.py's pattern) ------------
print("=== PHASE 2: graph.json — post_wire.py plain overwrite ===")

iter_dir2 = TMP / "sessions" / "iter-002"
iter_dir2.mkdir(parents=True)

# Write initial graph.json with nodes from the first run
original_graph = {
    "nodes": [
        {"id": "hypothesis:first-run", "type": "hypothesis", "parents": [], "children": [], "tags": []},
        {"id": "experiment:first-run-a", "type": "experiment", "parents": ["hypothesis:first-run"], "children": [], "tags": []},
    ],
    "edges": [
        {"source": "hypothesis:first-run", "target": "experiment:first-run-a", "relation": "next"},
    ],
}
(iter_dir2 / "iter-002-graph.json").write_text(json.dumps(original_graph, indent=2))
print(f"Before: {len(json.loads((iter_dir2 / 'iter-002-graph.json').read_text())['nodes'])} node(s)")
before_nodes = {n["id"] for n in json.loads((iter_dir2 / "iter-002-graph.json").read_text())["nodes"]}

# Simulate post_wire.py's write (post_wire.py:514 — plain write_text, no merge)
new_graph = {
    "nodes": [
        {"id": "hypothesis:second-run", "type": "hypothesis", "parents": [], "children": [], "tags": []},
    ],
    "edges": [],
}
(iter_dir2 / "iter-002-graph.json").write_text(json.dumps(new_graph, indent=2))

after_graph = json.loads((iter_dir2 / "iter-002-graph.json").read_text())
after_nodes = {n["id"] for n in after_graph["nodes"]}
print(f"After:  {len(after_graph['nodes'])} node(s)")
print(f"Original nodes preserved: {before_nodes.issubset(after_nodes)}")
print(f"New nodes present: {'hypothesis:second-run' in after_nodes}")
graph_ok = before_nodes.issubset(after_nodes) and "hypothesis:second-run" in after_nodes
print(f"Verdict: GRAPH.JSON {'✅ MERGED' if graph_ok else '❌ OVERWRITTEN (data lost)'}")
print()

# --- Summary ----------------------------------------------------------------
print("=== SUMMARY ===")
print(f"post_wire.py:514 writes graph.json as `iter_dir / f\"{{iter_dir.name}}-graph.json\"`")
print(f"Source: extensions/agi/bin/post_wire.py line 514 — plain .write_text(), no merge step")
print(f"")
print(f"The manifest clobber is already fixed by goal:s28 dispatch._merge_manifest.")
print(f"The graph.json clobber is UNPROTECTED — two dispatches into the same")
print(f"iter-NNN directory lose all graph data from the first dispatch.")
print(f"")
print(f"Sessions dir today has {len(list((Path('/home/ubuntu/work/agi/.agi/sessions')).glob('iter-0*')))} iter-0NN dirs")
print(f"coexisting with iter-1NNN dirs — a fresh driver.sh --max-iters 5 would")
print(f"land in iter-001..005 where graph.json already exists from Sep 2 runs.")
print(f"")
print(json.dumps({"manifest_protected": manifest_ok, "graph_overwritten": not graph_ok}))