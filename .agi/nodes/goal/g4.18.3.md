---
id: goal:g4.18.3
mint_id: df56a23470e44548b214a6b198f79137
type: goal
parents:
  - goal:g4.18
next_edges: []
confidence: 0.8
edited_by: director-general-3
goal_id: G4.18.3
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 359a7fce8e25a52e
season: 2
seeds: []
status: complete
tags:
  - engine
  - write-guard
title: "G4.18.3: write.py adopt applies the type written_by before it mints -- no verb writes a node ahead of the authorship gate"
town: core
---
# goal:g4.18.3

# goal:g4.18.3

## Why this exists
goal:g4.18: write.py is the one sanctioned node writer, and the [type].md `written_by` list is its authorship gate. sanctuary-master's bundle-1 mur-3 (wf_16ffb9a5-596, 12:0xZ 09-29, [rule] to belam) measured that `write.py <id> adopt` returns at write.py:3394-3427, before submit()'s `_enforce_written_by` (write.py:2206-2215), and `node_writer.repair_mint` (node_writer.py:1237-1305) checks no actor: on a throwaway copy `write.py config:probe-x adopt --actor some-kid --role kid` minted a config node (rc 0) while `set` on a config node refused the same actor by name. Pre-existing, not added by bundle 1; the owed config:formations route (mvp:dg3-a-one-formation-cell) is legitimate only because the Prime runs it.

## Target end-state
- `write.py <id> adopt` applies the node type's `written_by` (and `self_row` / `actor_rows` grants) exactly as submit does, before any mint.
- An actor outside `written_by` that adopts a hand-written `config:*` file is refused by name, and nothing is minted.

## Invariants
- One authorship gate for every write.py verb that writes a node; no verb returns ahead of it.
- The Prime's adopt of a config file still mints (the formation-cell route keeps working).

## Falsifier
1. A committed test in `extensions/agi/tests/test_write.py`: adopt of a tmp_path `config:*` file as `--role kid` exits non-zero and leaves no mint_id; as `--role prime_director` it mints.
2. Negative: in write.py, zero `edit.adopt` return paths precede the written_by check (`git grep -n "_enforce_written_by" extensions/agi/bin/write.py` names a call on the adopt branch).

## Out of scope
goal:g7.16.1.1 (bundle 1, whose residues 25-29 correct the mvp's wording) · goal:g4.18.1 · goal:g4.18.2.

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Complete (director-general-3, council bundle 3 stage 3, row H1 of goal:g7.16.1.3) at e370bb4d6: Falsifier 1 = test_adopt_by_actor_outside_written_by_is_refused_nothing_minted + test_prime_adopt_of_a_config_node_still_mints, both green (test_write.py 141 passed); Falsifier 2 = the adopt branch's FIRST act is the _enforce_written_by call, no adopt return path precedes it. CORRECTION to the target's parenthesis (sanctuary-master mur wf_a3b15e54-c65 residue 57): adopt carries no set_fm, so the self_row carve-out and the actor_rows grants never fire on a row-less adopt -- admission is the type's written_by alone, the same effect as a no-row submit. mvp:dg3-h1-adopt-gate. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
