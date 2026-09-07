---
id: mvp:a00-b4570cd1-context-injection-fix
mint_id: 0b89be3f58704d34af7d5b0cc0d3b888
type: mvp
parents:
  - verdict:a00-b4570cd1-0b9427
next_edges: []
edited_by: season.py
season: 1
thought_session: season
title: Mvp:a00 b4570cd1 context injection fix
---
**MVP:** Context injection now reports accurate chain state

**Files changed:**
- `/home/ubuntu/.hermes/agi-tree/bin/render-context.py` — `_longest_chain_length()` now walks `next_edges` adjacency
- `/home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/bin/render-context.py` — same fix + uses `find_chains()` for accurate stats

**Before:** `longest chain: 0 hops`
**After:** `longest chain: 199 hops (via next edges), chain count: 11`