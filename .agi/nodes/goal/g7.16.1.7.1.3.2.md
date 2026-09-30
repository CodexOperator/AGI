---
id: goal:g7.16.1.7.1.3.2
mint_id: 9057cb134e6d4cec852d44ef2cbf2610
type: goal
parents:
  - goal:g7.16.1.7.1.3
next_edges: []
edited_by: director-general-1
goal_id: G7.16.1.7.1.3.2
goal_kind: subgoal
scaffold_hash: 230ec9b8e9ccc72e
season: 2
status: complete
thought_session: director-general-5
title: "G7.16.1.7.1.3.2: config.json declares ONE pi template (rows as JSON, one free default, aliases for the old ids)"
town: core
---
# goal:g7.16.1.7.1.3.2

## Why this exists
goal:g7.16.1.7.1.3: the owner verbatim there ("Just standard pi template that lists all the different model + thinking level + extendable to other harness settings as rows containing jsons"); goal:g7.16.1.7.1.3.1 makes every reader template-aware first.

## Target end-state
- .agi/config.json declares ONE pi harness: adapter, bin, forward_env once; `rows` = JSON objects (free, paid, local ...), exactly one `default: true` (the free row); `aliases` pi-free -> free, pi-local -> local.
- spawn.harness and workflows.*.provider name pi (or pi:<row>); the pi-free / pi-local blocks are gone. NOT HELD (council coverage review, self-perpetuating 05:4xZ 09-30; DG1 re-read 08:4xZ): spawn.harness and the workflows review / drafting / deep-search `provider` cells still read pi-free (.agi/config.json:104,181,186,191), as does .geometry/workflows.md default_harness; they move with the alias retirement, goal:g7.16.1.7.1.3.3.

## Invariants
- Exactly one default row and it is zero_usd; a dispatch that resolved pi-free before resolves the same model + provider after.

## Falsifier
1. A test reads the live config through adapters.harness_block: pi -> the free row's model; pi-free and pi-local -> their rows.
2. Negative: grep for `"pi-free": {` or `"pi-local": {` in .agi/config.json = 0.

## Out of scope
goal:g7.16.1.7.1.3.1 · goal:g7.16.1.7.1.3.3

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:4xZ 09-30, routed by sanctuary-master from self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ): target bullet 2 marked NOT HELD, measured by DG1 in the bytes: spawn.harness and three workflows provider cells still pi-free (config.json:104,181,186,191) plus .geometry/workflows.md default_harness. Status left complete on the council's instruction (record, not reopen); the move rides goal:g7.16.1.7.1.3.3's alias retirement.
<!-- THOUGHT:END -->
