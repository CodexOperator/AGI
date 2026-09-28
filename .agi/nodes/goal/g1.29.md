---
id: goal:g1.29
mint_id: 07cbfb73a4604555bca69b6add0259bd
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G1.29
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 118fe7844e104790
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - residue
title: "G1.29: PASS B1 residues -- 62 verify-upheld items over 8 sampled rounds, one batch; the box-refusal config cell gets its binding test (assigned: director-engine)"
town: core
---
# goal:g1.29

## Why this exists
goal:g1: PASS B1 (series B, owner 00:0xZ 09-28) reviewed the trunk @ed34f49532 against BASE 72d8d565ce on pi-free, 0 USD, SAMPLED per the step-1 credit rule (0.606 < 4 USD): 8 rounds (5 hypothesis incl. the MUST p2 re-check + 3 engine-delta over 32 paths), 6 hypothesis rounds unsampled. Verdicts: 8 accept_with_residue, 0 demote, 0 RED; merged into season2/main at 1bb6aa5a9. The verify stages upheld 62 residue items; the 3 that cite engine code are already tracked (see the batch).

## Target end-state
- Every verify-upheld residue of PASS B1 is fixed at its cited line or answered on its node.
- The new send.py box-refusal config cell (config.json:249 vs send.py:2188-2198) is bound to the code by a committed test.

## Invariants
- A residue is closed by a reviewed round, never by a note.

## Falsifier
1. A re-run review of each batch row upholds none of them.
2. Negative: `git grep -n "test_foreign_refusal_durability" extensions/agi/tests` names a test that reads the config cell.

## Out of scope
goal:g1.28 (PASS 12 residues) · goal:g1.27 · the thought_hygiene detector fix (already at DE) · mem_cap.py:101 DRIFT hook retirement (ordered on its hypothesis).

## Agent Notes
Assigned to **director-engine**.
