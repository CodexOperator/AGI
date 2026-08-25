---
confidence: 1.0
goal_id: G7.3
goal_kind: subgoal
heading_level: 3
id: "goal:g7.3"
mint_id: aa7f005bc80244729b3cdc87218dd8d1
order: 39
origin: goals-doc
parents:
  - goal:g7
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G7.3: `evidence_runs` as a bare integer is still unverifiable"
type: goal
---

Residual left open by G3.1 and named here so it is not forgotten. After the
H4c fix a list entry must resolve to a real node, but an integer
(`evidence_runs: 3`) is still accepted as direct attestation and counts 3.
Writing an integer is exactly as cheap as writing the `synthetic` sentinel was.

Not closed immediately on purpose: many honest nodes legitimately record a
count rather than ids, and forcing ids everywhere would break the honest path
in order to close a hole nobody has yet exploited. Decide deliberately — the
H4c lesson is that any unverifiable field eventually gets gamed, so the
question is when, not whether.
