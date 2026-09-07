---
id: experiment:a00-dce9d5da-377c4d
mint_id: a759a0666fca481f93180cf696e19d1d
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: 535205a81786208c
season: 1
thought_session: season
title: A00 dce9d5da 377c4d
verdict: inconclusive_lean_disproved:80
---
# experiment:a00-dce9d5da-377c4d

## Experiment

Dynamic test confirming the graph.json clobber path that sibling experiments
`experiment:a00-db9ea0ae-d8251b` and `experiment:a00-ff8eb71d-f812bc` predicted
but did not test concretely.

Wrote a self-contained python script (`a00-dce9d5da-377c4d-test.py`) that:

**Phase 1 — manifest.json:**
- Creates tmpdir sessions/iter-001 with one real-looking agent record
- Calls `dispatch._merge_manifest` (the actual function dispatch.py uses, not a
  simulation) with a new unrelated agent record — simulating a second dispatch
  into the same iter-001 directory
- Reads back the merged manifest
- **Result: original agent preserved, new agent appended** — manifest content
  is protected by merge-by-agent-id (goal:s28)

**Phase 2 — graph.json:**
- Creates tmpdir sessions/iter-002 with a real-looking graph snapshot (2 nodes,
  1 edge)
- Simulates post_wire.py's graph write: `iter_dir / f"{iter_dir.name}-graph.json"`
  via plain `.write_text()` with a new unrelated graph (1 node, 0 edges) —
  exactly what `post_wire.py:514` does, no merge step
- Reads back the overwritten graph
- **Result: original 2 nodes lost, only the 1 new node remains** — graph data
  is a plain overwrite with no protection

Ran against a tmpdir copy of the data structure; no live .agi/sessions data
was touched. The script imports `dispatch` from the current codebase
(commit b45fdca, which added `locations.py` loop-scoped id support but did
not change the graph.json write path).

## Evidence

```
tmpdir: /tmp/cliobber-test-rgye15d_

=== PHASE 1: manifest.json — dispatch._merge_manifest ===
Before: 1 agent(s)
After:  2 agent(s)
Original agent preserved: True
New agent present: True
Verdict: MANIFEST ✅ PROTECTED (merge by id)

=== PHASE 2: graph.json — post_wire.py plain overwrite ===
Before: 2 node(s)
After:  1 node(s)
Original nodes preserved: False
New nodes present: True
Verdict: GRAPH.JSON ❌ OVERWRITTEN (data lost)

=== SUMMARY ===
post_wire.py:514 writes graph.json as `iter_dir / f"{iter_dir.name}-graph.json"`
Source: extensions/agi/bin/post_wire.py line 514 — plain .write_text(), no merge step

The manifest clobber is already fixed by goal:s28 dispatch._merge_manifest.
The graph.json clobber is UNPROTECTED — two dispatches into the same
iter-NNN directory lose all graph data from the first dispatch.

Sessions dir today has 4 iter-0NN dirs
coexisting with iter-1NNN dirs — a fresh driver.sh --max-iters 5 would
land in iter-001..005 where graph.json already exists from Sep 2 runs.
```

## Interpretation

This experiment adds **dynamic evidence** to the disproved side of the
hypothesis. All 6 prior sibling experiments under this hypothesis relied on
static code reading or grep; this is the first that actually runs code against
a populated directory and measures what survives.

The split in findings remains:
- **manifest.json**: protected via `_merge_manifest` (goal:s28) — merge by
  agent id, even when driver.sh re-dispatches into an existing iter-NNN dir
- **iter-NNN-graph.json**: UNPROTECTED — `post_wire.py:514` does
  `graph_path.write_text(json.dumps(...))` with no read-merge step, so a
  second dispatch into the same directory silently destroys the first
  run's graph snapshot

Additionally, the codebase has evolved since the sibling experiments ran:
`locations.py` now has `iteration_id()`, `format_loop_iteration()`,
`iteration_dirname()` and `iteration_dir()` that accept both legacy numeric
ids (int → `iter-{n:03d}`) and loop-scoped ids (str → `iter-L{N}.{NN}`).
Dispatch.py now uses `locations.iteration_dir(root, args.iter_n)` as the
single path formatter. However, `driver.sh:239` still passes a bare integer
(`for i in $(seq 1 "$MAX_ITERS"); iter_run "$i"`), so the loop-scoped format
remains unreachable from the bash entry point — the code CAN handle it, but
the driver never asks it to.

The hypothesis claimed "loop-scoped iteration ids cannot clobber." The
loop-scoped infrastructure exists in `locations.py` now (verified in commit
b45fdca), but driver.sh still uses the legacy numeric scheme. And even under
the numeric scheme, the graph.json file is a plain overwrite — a concrete
clobber path that remains live regardless of which id format is used.


## Agent Notes
Dynamic test confirms post_wire.py iter-NNN-graph.json is a plain overwrite (no merge) while dispatch._merge_manifest protects manifest.json. Adds concrete dynamic evidence to the disproved side — sibling experiments did only static reads.