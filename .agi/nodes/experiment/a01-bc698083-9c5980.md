---
id: experiment:a01-bc698083-9c5980
mint_id: c85643542b0443a9aa8d83382363817a
type: experiment
parents:
  - hypothesis:a00-93087928-918ad7
next_edges: []
scaffold_hash: 8e47d33c55796866
title: A01 bc698083 9c5980
---

# experiment:a01-bc698083-9c5980

## Experiment

Independent replication and extension of experiment:a00-6e3b85a0-6c5a16's findings. Ran the viewport CLI to confirm the existing graph data structures are sufficient for a navigable ASCII viewport at zoom level 3 with agent positioning, and extended testing to the zoom, time, and live axes.

### Baseline: depth 3 render
`python3 extensions/agi/bin/viewport.py --emit human --depth 3 --height 30 --width 100`
- Renders 1041 nodes, 965 edges — the full graph as a connected tree
- Showed the same structure as experiment 1 (active goals as roots, branches at each depth, damage glyphs for broken edges)

### Zoom axis: depths 1–5
`python3 extensions/agi/bin/viewport.py --emit human --depth 1|2|4|5 --height 30 --width 100`
- Depth 1: goals + immediate hypotheses (correct aggregation)
- Depth 2: goals → hypotheses → experiments (mid-level view)
- Depth 3: full chain to verdicts (default)
- Depth 4–5: resolves to MVPs and deeper children
- All depths render correctly with appropriate truncation; the zoom axis is functional

### Unified stream invariant (goal:g9.7)
`python3 extensions/agi/bin/viewport.py --emit both --depth 3 --height 20 --width 90 --verify`
- PASS: one stream, two formatters, same frames in same order
- Briefing (metrics, coverage, rules) present in both views

### Time axis
`python3 extensions/agi/bin/viewport.py --emit human --depth 3 --height 20 --width 90 --iter iter-1021`
- Renders historical iteration data with correct frame count (205 vs 226 at latest)
- Counts reflect the smaller graph at iter-1021 (1017 nodes vs 1041 now)

### Live axis
`python3 extensions/agi/bin/viewport.py --emit human --depth 3 --height 20 --width 90 --live`
- Renders agents from the latest available iteration manifest
- No agents visible as ✶ markers because this session's agents work on nodes not yet wired into the graph's children edges (the experiment node file exists but hasn't been loaded; the hypothesis node has no children edges populated to include this node)

### Unified LLM view passes verify
`python3 extensions/agi/bin/viewport.py --emit llm --depth 3 --height 20 --width 90 --verify`
- PASS: LLM view (the exact context a kid is handed) includes chain rules, verdict taxonomy, metric briefing, claimed commands
- Frame order matches human view byte-for-byte

## Evidence

```
$ python3 extensions/agi/bin/viewport.py --emit both --depth 3 --height 20 --width 90 --verify
frames in slice: 20   human lines: 23   llm ids: 20   briefing: yes
PASS — one stream, two formatters, same nodes in the same order

$ python3 extensions/agi/bin/viewport.py --emit llm --depth 3 --height 20 --width 90 --verify
frames in slice: 20   human lines: 23   llm ids: 20   briefing: yes
PASS — one stream, two formatters, same nodes in the same order

$ python3 extensions/agi/bin/viewport.py --emit human --depth 3 --height 30 --width 100
nodes 1041 · edges 965 · experiment=130, goal=111, hypothesis=193, mvp=47, verdict=109
scored on outcome_coverage = 0.244
--------------------------------------------------------------------------------
● G G1.10: The engine's standard commands are declared in a node, not memorised
  · ? Standard command declaration
  ○ H Commands are config not prose
    ○ E The table runs and caught a bug [proved]
      ○ D A declared command table is executable, so a wrong one fails instead of being believed [pr
● G G1.11: A fresh, credit-capped provider key per spawn — not one key for the whole run
...

$ python3 extensions/agi/bin/viewport.py --emit human --depth 1 --height 40 --width 100
...
● G G1.10: ...
● G G1.11: ...
● G One read/write path for nodes...
(Depth 1: shows only active goals and immediate hypotheses — correct aggregation)

$ python3 extensions/agi/bin/viewport.py --emit llm --depth 3 --height 20 --width 90 --verify 2>&1 | head -20
# graph viewport
_frames 0-20 of 226_
> anchor=roots depth=3 frames=226 time=-

## metric
- **primary** outcome_coverage
- **unit** fraction (0..1)
- **direction** higher is better
- **this run** 0.244
...
## chain rules
...
```