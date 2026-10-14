---
id: goal:g7.16.1.11.4
mint_id: ca5cccbeed484dbb984b0d15ab7602d3
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.4
goal_kind: subgoal
origin: owner
scaffold_hash: fa5058a90aec157e
season: 2
seeds: []
status: horizon
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.4: the CAPSULE: k-of-n signed, always-encrypted, popped only by the weighted MUTUAL quorum straight into one destination; the passkey code route O.5; one GitHub deploy key held in a capsule"
town: core
---
# goal:g7.16.1.11.4

## Why this exists
Parent goal:g7.16.1.11: §O / §P / O.5-O.8 of doc:radically-simple-engine (capsule-pop 1,194 B, capsule-login 692 B, se-wrap 1,277 B; T1-T8, P1-P11, Q1-Q6 PASS on scratch); owner BUILD GO 05:45Z.
## Target end-state
the CAPSULE: k-of-n signed, always-encrypted, popped only by the weighted MUTUAL quorum straight into one destination; the passkey code route O.5; one GitHub deploy key held in a capsule.
## Invariants
no single holder can view a sealed secret; a replay loses (one ref CAS); the destination is the only reader at pop.
## Falsifier
1. capsule-pop installed on the box and Q1-Q6 re-run PASS on it; the town repo's deploy key exists only as a capsule
2. negative: a plaintext deploy key on disk: zero hits
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"One deploy key in a capsule for now. I don't have enterprise access." (owner 07:2xZ) · "So my capsule only pops with you all, yours only with mine" (owner 05:45Z; both verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
held by goal:g7.16.1.11.11 HOLD; re-activated when it lifts (director-general-3 10-11, SM gen 38 placement on belam's check: idle since 10-01, key / identity / signing)
v+ (director-general-3 10-14): COUNCIL 3/3 06:53Z 10-14 (SM [rule] to all posts, g7.16.1 bundle DEFERs): DEFER to season 3 -> status horizon; target and falsifier untouched. Already horizon on the trunk at e9b10a5b9d; this commit only records the verdict.
<!-- THOUGHT:END -->
