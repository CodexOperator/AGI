---
id: goal:g7.16.1.7.1.4
mint_id: d0541ccaa59f46578010ebf660a24423
type: goal
parents:
  - goal:g7.16.1.7.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.7.1.4
goal_kind: subgoal
origin: council-loop
scaffold_hash: 5d15000565669563
season: 2
seeds: []
status: active
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.1.4: seat claiming needs no model act -- heal assigns a post's keys from a forgiving key template"
town: core
---
# goal:g7.16.1.7.1.4

## Why this exists
goal:g7.16.1.7.1 (7a, NOW in the council placement) under goal:g7.16.1.7: the owner, verbatim there: "Like the heal script should just automatically assign keys so no model has to do it. For now we can keep it very kind and forgiving via a template." Measured: config:posts has pubkey on 18 of 27 rows; send.py keygen is a model act today. Stricter key templates and per-post accounts are season 3 (Out of scope). goal:g1.11 (per-spawn provider keys) is a different key and stays separate.

## Target end-state
- A key template node (season 2: forgiving) names the scheme; at stand-up or recovery heal mints the post's seat key from it and writes the row's key cells through write.py.
- A post never runs send.py keygen by hand.

## Invariants
- A live post is never left without a key it can sign with.
- A key row lands on the post's own trunk too, never on one trunk alone (the Prime 23:5xZ: SM gen 7 re-mint 4f0bdf6e5 landed on season2/main only, conflicted posts.md on local-maxxing and blocked every rotate until 93f4567b5).

## Falsifier
1. A heal test on a dummy row with no pubkey leaves the row keyed per the template, and whois resolves it.
2. Negative: zero role templates or cards instruct a post to run keygen.

## Out of scope
goal:g1.11 · season-3 key templates and per-post user accounts

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 05:3xZ 09-30, build-vs-goal on DG2's verdict:dg2mvp-g717114 (2ba51e153, LEAN_PROVED 72): Falsifiers 1 and 2 hold (test_stand_up 16/16 recover/restart keyed + VERIFIED; 0 keygen instructions), and ruling (C) holds (key_template read from config:key-authority, the node cell beats the code default). Reopened complete -> active because Invariant 1 (a live post is never left without a key) is unmet on three stand-up paths DG2 measured: cmd_spawn keys through a template-free second path (residue 159), cmd_seats_launch keys nothing (tmp dummy row stays unkeyed), cmd_loop's rotate successor has no key step. Corrective nested as goal:g7.16.1.7.1.4.1 (a1c102cd1), seeded by DG2's fork hypothesis:stand-up-verb-keys-every-mode-through-key-template; this goal closes, with its OUTCOME, when that leaf does. DG5's landing (4abfee9d3 + c14815594) stands; this version's prior THOUGHT is in the grid.
<!-- THOUGHT:END -->
