---
id: hyp:a00-b4570cd1-0b9427
mint_id: 04fb5b18c5ff4b1d9d6c9bf822e9e01d
type: hypothesis
parents: []
next_edges:
  - exp:a00-b4570cd1-context-injection-fix
edited_by: season.py
season: 1
thought_session: season
title: Context injection longest_chain reports 0 hops because _longest_chain_length walks spawns not next_edges
---
# hyp:a00-b4570cd1-0b9427

## Hypothesis

**Claim**: The context injection's `longest_chain` field reports 0 hops because `_longest_chain_length()` in `render-context.py` walks `n.children` (populated by `spawns` edges: idea→hypothesis→task tree). The real chains are built on `next_edges` (verdict→experiment→verdict cycles), which produce 200-hop chains. The spawns-based walk gives depth ≤2 since ideas only directly spawn hypotheses, not the extended verdict nodes.

**Proof**: Modify `_longest_chain_length()` to walk `next_edges` instead of `children`. The reported length jumps from 0 to 200.

**Disproof**: Even with `next_edges` walk, longest chain is still 0 → next_edges arrays are empty in node files (but we know they're populated from experiment data above).

## Evidence

- Context reports: `longest chain: 0 hops (via next edges)` despite graph having 11 chains at 200 hops
- `_longest_chain_length()` DFS uses `n.children` (spawns tree) not `next_edges`
- `find_chains()` (which uses next_edges): 11 chains, max 200 hops
- `_longest_chain_length()` (which uses spawns): 0 hops

## Fix

Modify `render-context.py`'s `_longest_chain_length()` to:
1. Build a `next_edges` adjacency dict from verdict and experiment nodes
2. DFS that adjacency instead of `n.children`
3. Report correct longest chain length

## Experiment

```python
# Before fix
longest_via_spawns = _longest_chain_length(g)  # → 0

# After fix: walk next_edges
def longest_chain_via_next_edges(g):
    next_adj = {}
    for n in g.nodes:
        if hasattr(n, 'next_edges') and n.next_edges:
            next_adj[n.id] = n.next_edges
    # DFS...
```

Expected: 200 hops reported.