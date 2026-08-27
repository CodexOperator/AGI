---
confidence: 1.0
goal_id: G3.1
goal_kind: subgoal
heading_level: 3
id: "goal:g3.1"
mint_id: dd0c5de790b849f39e88f5b89566858d
order: 19
origin: goals-doc
parents:
  - goal:g3
seeds:
  - exp:evidence-gate-resolution-r1
  - idea:engine-evidence-gate
  - idea:engine-post-wire
status: active
tags:
  - goal
  - subgoal
title: "G3.1: `evidence_runs` must resolve to a real node"
type: goal
---

🔴 **The evidence metric was itself gamed, and by the cheapest possible move.**
`normalize_evidence_runs` returns `len(value)` for any list, so
`evidence_runs: [synthetic]` — the literal string — satisfies `evidence_runs >= 1`
and the gate passes a `proved` verdict that ran nothing. Measured on this
corpus before the padding offload: 2,842 of 2,869 verdicts carrying
`evidence_runs` used that sentinel; 16 cited a resolvable `exp:` id.

Fix: count only entries that resolve to a real node in the corpus; treat a
non-id string as a taxonomy violation that fails closed, not a silent pass.
Then re-measure and record a corrected baseline on both live projects.

**Until this lands, no `evidence_fraction` reading means anything** — including
the post-offload 0.365, of which 33 of 121 surviving verdicts are still
sentinel-backed. Owns TODO **H4c**.
