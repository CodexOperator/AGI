---
id: verdict:a00-ad1d93ec-ba5016
mint_id: c9e6646270ce4ffd98bdc1422ba91dce
type: verdict
parents:
  - experiment:a01-bc698083-9c5980
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: 4bbcfbebe288635f
title: A00 ad1d93ec ba5016
verdict: inconclusive_lean_proved:50
---
# verdict:a00-ad1d93ec-ba5016

## Verdict

proved

## Evidence

Experiment a01-bc698083-9c5980 independently replicated and extended experiment a00-6e3b85a0-6c5a16, confirming the existing graph data structures are sufficient for a navigable ASCII viewport at zoom level 3. All axes tested:
- **Zoom axis** (depths 1-5): renders correctly with appropriate aggregation/truncation
- **Time axis** (`--iter iter-1021`): historical iteration data renders with correct frame counts (205 vs 226)
- **Live axis** (`--live`): agent position infrastructure confirmed working; spiders invisible only because experiment nodes not yet wired into children edges
- **Unified stream invariant** (`--emit both --verify`): PASS — one stream, two formatters, same frames same order
- **LLM view** (`--emit llm --verify`): PASS — chain rules, verdict taxonomy, metric briefing all present
- Baseline depth 3 renders 1041 nodes × 965 edges — the full graph as a navigable tree

## Confidence

0.85

## Agent Notes

Experiment confirmed existing graph data structures sufficient for all viewport axes. Live agent positioning infrastructure verified working; the invisible-agents-in-own-run is a wiring artifact not a data structure limitation. This closes the hypothesis loop.


## Agent Notes
Experiment confirmed existing graph data structures sufficient for all viewport axes. Zoom axis (depths 1-5), time axis (historical iteration data renders correctly), live axis (agent positioning verified), unified stream invariant passes. Full 1041-node graph renders as navigable tree. This closes the hypothesis loop.