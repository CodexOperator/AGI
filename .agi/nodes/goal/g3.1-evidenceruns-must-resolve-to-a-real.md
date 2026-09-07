---
id: goal:g3.1
mint_id: dd0c5de790b849f39e88f5b89566858d
type: goal
parents:
  - goal:g3
confidence: 1.0
edited_by: season.py
goal_id: G3.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - exp:evidence-gate-resolution-r1
  - idea:engine-evidence-gate
  - idea:engine-post-wire
status: complete
tags:
  - goal
  - subgoal
thought_session: season
title: "G3.1: `evidence_runs` must resolve to a real node"
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked complete in the 2026-09-01 sweep. `evidence_runs` resolves against a
real corpus: `build_corpus` builds the id set and `normalize_evidence_runs`
counts only entries that are node-id-shaped AND present in it. A bare int
resolves to 0 by design, because a count nobody can check certifies nothing.

Extended the same day rather than merely confirmed: the resolution rule had a
hole this goal's own logic implies — a node citing ITSELF resolves, because the
node exists. `goal:g7.3` closed `evidence_runs: 3` for being "exactly as cheap
to write"; `[<my own id>]` was exactly as cheap and bought a decisive verdict,
and it fired unprompted on the first kid that reached for `proved`. Now an
`experiment` may cite itself (it IS the run) and no other type may.
<!-- THOUGHT:END -->