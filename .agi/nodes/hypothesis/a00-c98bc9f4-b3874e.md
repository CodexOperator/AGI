---
id: hypothesis:a00-c98bc9f4-b3874e
mint_id: 67f511e4dbe9454e9cdbf62dfd0c0cf5
type: hypothesis
parents:
  - goal:g9.4
next_edges: []
confidence: 0.0
scaffold_hash: fe9c2218008f3f79
title: A00 c98bc9f4 b3874e
verdict: pending
---
# hypothesis:a00-c98bc9f4-b3874e

## Hypothesis

Converting the viewport from a linear tree dump to a layered 2D graph layout (Sugiyama-style layering by depth + median-edge crossing reduction) produces a genuinely more informative "rudimentary ASCII web" than the current linear tree, without breaking the unified stream invariant (goal:g9.7).

### What would prove it
1. Nodes arranged in horizontal layers by graph depth (active goals at top, leaves at bottom) with intra-layer ordering that visibly reduces edge crossings vs. the current depth-first linear tree
2. The viewport pans across a 2D plane (up/down moves between layers, left/right moves within a layer) rather than scrolling a linear tree — distinguishable screen regions show different graph neighbourhoods
3. Unified stream invariant still passes: `--emit both --verify` returns PASS with the same frames in the same order for both human and LLM formatters
4. A human observer can identify related node clusters (e.g. a hypothesis → experiment → verdict spine) by spatial proximity in the 2D layout faster than by scanning the linear tree
5. `viewport.py --depth 3 --height 30 --width 100` renders the full graph (1041 nodes, 965 edges) within 2 seconds wall clock

### What would disprove it
1. 2D layout produces overlapping/colliding nodes that are less readable than the current linear tree — nodes from different branches occlude each other or share the same cell
2. Layout computation (layer assignment + crossing reduction) adds >5s latency on the full graph, breaking the live refresh requirement of `--live` mode
3. The unified stream invariant is broken because the LLM view requires linear frame ordering (one node per frame) while the 2D human view needs spatial frames (multiple nodes per row) — the formatters diverge in frame structure
4. Nodes at depth >5 wrap around horizontally or clip at `--width` in ways that lose information compared to the linear tree view
5. Adding an edge-crossing counter: the linear tree has fewer visual edge crossings than the 2D layout because linear tree edges are unidirectional (parent → child, never crossing the midline), while 2D layout edges span across layers and cross regularly


## Agent Notes
Hypothesis: layered 2D graph layout (Sugiyama-style by depth + median-edge crossing reduction) for viewport produces a rudimentary ASCII web more informative than current linear tree, without breaking unified stream invariant. Tests: 2D layout prevents occlusions, layout computation <5s, unified stream passes, depth>5 doesn't clip, edge crossings manageable.
