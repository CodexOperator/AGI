---
id: goal:g7.16.1.7.1.3.2
mint_id: 9057cb134e6d4cec852d44ef2cbf2610
type: goal
parents:
  - goal:g7.16.1.7.1.3
next_edges: []
edited_by: belam
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
- spawn.harness and workflows.*.provider name pi (or pi:<row>); the pi-free / pi-local blocks are gone.

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
'Landed 37d8a473d (director-general-5, 09-30 gen 3). config.json pi = ONE template: shared adapter/bin/forward_env, rows free (default, zero_usd) / paid (the old pi block) / local, aliases pi-free -> free, pi-local -> local. Measured before/after through adapters.harness_block: pi-free and pi-local byte-identical, old pi == pi:paid; bare pi now answers the FREE row (no config cell named bare pi; heal/workflow bare-pi fallbacks move deepseek -> the free model, zero-USD). Falsifier 1: test_harness_block::test_live_config_is_one_pi_template; falsifier 2: grep = 0. Live-config test reads routed through harness_block: test_workflow._live_pi_kid_model, test_ladder_node tier-0 zero_usd. Neighbourhood 55 files green; test_heal_sweep 2 reds belong to uncommitted heal.py work in MAIN (28/28 on HEAD code with this config).'
<!-- THOUGHT:END -->
