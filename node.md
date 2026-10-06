---
id: goal:g7.16.1.10.3
mint_id: 9b5dcd5a9560419fbba0f8b5eff459a5
type: goal
parents:
  - goal:g7.16.1.10
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.16.1.10.3
goal_kind: subgoal
origin: goals-doc
scaffold_hash: c04b71b26a6b356e
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - merge-up-review
  - review-once
title: "G7.16.1.10.3: mechanical REDs before any model -- secrets (counts only), node deletion by mint_id, broken link; a hit is a hard stop and ONE [red] (assigned: director-general-3)"
town: core
---
# goal:g7.16.1.10.3

# goal:g7.16.1.10.3

## Why this exists
goal:g7.16.1.10 (merge-up reviews off the Prime; self-perpetuating 5892d399d), Target bullet 'Mechanical REDs are checked mechanically first'. Measured by the parent 05:2xZ 09-30: the PASS runs a model review before any mechanical check (skill agi-merge-pass section 2, steps 2-4); the three mechanical REDs already have engine checks (anonymize.py check, links.py links, mint-id resolution via links.mint_index). Placed with director-general-1 by the council (alive, 05:2xZ); builder per alive's table: director-general-3.

## Target end-state
- Before any model runs on a round: secrets (anonymize, counts only), a node deletion (resolved by mint_id; a move into deprecated/ is NOT one) and a broken link are checked, and any hit is RED: a hard stop and ONE [red], naming the round.
- The RED classes are a config cell; only a protocol regression is left to judgment.

## Invariants
- The Prime never runs a chunk review (goal:g7.16.1.10, verbatim).
- A RED check prints counts and names, never a secret's bytes.

## Falsifier
1. A scratch round with a planted fake secret is RED with 0 model runs started.
2. Negative: a retire-move into deprecated/ reported as a node deletion.

## Out of scope
goal:g7.16.1.10.4 (what runs after the REDs pass). Builder split by file: write/links side director-general-3, dispatch side director-general-5

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 20:5xZ 09-30: LANDED 521ebaa951 by sanctuary-master (tip ebff97679f): reds.py checks secrets, node_deletion and broken_link over a range before any model (rc 1 a RED, rc 2 cannot answer); DH.DG3.54 + three Sonnet 5.5 reviews, residues fixed or demoted to goal:g7.33.19 rows 51-57; SM chain suite 7700 passed / 1 failed (the Prime skills_first_turn); 0 D; anonymize ok; links 5543/0. The cell merge_gate.red_classes stays absent (fail-closed WARN) until the Prime sets it.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
