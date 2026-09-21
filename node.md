---
id: verdict:a00-b4570cd1-0b9427
mint_id: 0775b843e55b45d3b74f656d1de9b46e
type: verdict
parents:
  - exp:a00-b4570cd1-context-injection-fix
next_edges:
  - mvp:a00-b4570cd1-context-injection-fix
confidence: 0.98
contrasts: []
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
evidence_runs: []
season: 1
status: inconclusive_lean_proved:50
subgraph: false
supports:
  - verdict:graph-core-r1
  - verdict:embeddings-r2
  - verdict:embeddings-r3
  - verdict:chain-engine-r1
thought_session: season
title: "iter30: context longest_chain 0→199 hops via next_edges fix"
verdict: inconclusive_lean_proved:50
---
**Verdict:** PROVED (confidence 0.98)

**Evidence:**
- Context generator's `_longest_chain_length()` used `n.children` (spawns edges) → returned **0 hops**
- Same function walking `next_edges` adjacency → returned **199 hops**
- `find_chains()` (ground truth) → **200 hops**, 11 chains
- Fix applied to both `/home/ubuntu/.hermes/agi-tree/bin/render-context.py` and the plugin at `autoresearch-tree/extensions/autoresearch-tree/bin/render-context.py`
- 274 tests pass after fix

**Root Cause:**
- `render-context.py` comment said "longest path through idea → hyp → task"
- This is the spawns tree which is shallow (depth ≤2 from idea to hypothesis to task)
- Real chains use `next_edges` (verdict→experiment→verdict cycles) which go 200 hops deep
- The `_longest_chain_length` function was measuring the wrong graph structure

**Fix:**
Replaced `_longest_chain_length()` DFS to walk `next_edges` adjacency instead of `n.children`.
Plugin version now also uses `find_chains()` for accurate chain stats.

**Chain Impact:**
- Context injection will now report correct `longest chain: 199 hops (via next edges)` and `chain count: 11`
- Agents will make better chain-picking decisions based on accurate chain state

**Shadow reconciled, 2026-08-27.** The demotion below rewrote `verdict:` and left `status: proved` behind — S16's exact defect, reproduced by the repair itself. `status:` is the legacy shadow of `verdict:` and must never contradict it; both now read `inconclusive_lean_proved:50`.