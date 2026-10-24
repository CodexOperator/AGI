---
id: goal:g7.16.1.11.46.7
mint_id: 8389d3aaf29345eda6a267ca70ae75fd
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.7
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - C2
season: 3
status: active
title: "G7.16.1.11.46.7: C2 -- config:secrets carries one workspace-id cell per credits lane (agi-batch, agi-kids, agi-council), or the option-B scoped-key names: ids, never secrets"
town: local-maxxing
---
# goal:g7.16.1.11.46.7

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §36.2 (workspaces, option B). The workspaces (or the option-B scoped keys) are an owner act banked in card-belam §6; the cells and their check are built now. Doc sections implemented: §36.2 (doc:brainstorm-unify is reference, never placement).

## Target end-state
- .agi/nodes/.geometry/secrets.md (config:secrets) has a `lanes:` block with one cell per lane: `workspace: wrkspc_…` (or `scoped_key: <credential name>` for option B), read by C1 and C3.
- A check refuses any sk-ant string in config:secrets.

## Invariants
- config:secrets holds ids and names only; a secret value in it is a red.

## Falsifier
1. `sh extensions/agi/tests/secrets-lanes.t.sh` exits 0: the three lane cells parse; a malformed id is refused; mutant: an sk-ant planted in a cell reads RED.
2. Negative: `grep -c 'sk-ant' .agi/nodes/.geometry/secrets.md` prints 0.
3. Live values = passed except the workspaces / option-B keys (owner, card-belam §6).

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-science-1**.
