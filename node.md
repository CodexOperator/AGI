---
id: exp:a00-b4570cd1-context-injection-fix
mint_id: 9049d8c0826344539c58f4c2bcfc8f1c
type: experiment
parents:
  - hyp:a00-b4570cd1-0b9427
next_edges:
  - verdict:a00-b4570cd1-0b9427
edited_by: season.py
season: 1
thought_session: season
title: "iter30: Fix render-context longest_chain (spawns→next_edges)"
---
**Experiment:** Fix `_longest_chain_length()` in `render-context.py`

**Steps:**
1. Confirmed BUG: `_longest_chain_length()` walks `n.children` (spawns) → 0 hops
2. Confirmed real state: `find_chains()` → 11 chains, max 200 hops
3. Wrote `_longest_chain_length_next_edges()` that walks `next_edges` adjacency → 199 hops
4. Patched both `/home/ubuntu/.hermes/agi-tree/bin/render-context.py` and the plugin at `autoresearch-tree/extensions/autoresearch-tree/bin/render-context.py`
5. Ran 274 tests → all pass

**Result:** BUG confirmed and fixed. Context now reports correct chain state.