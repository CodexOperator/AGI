---
id: goal:g4.18.6.4.1
mint_id: 29b0b7cb293d48d198bd9d78c8404212
type: goal
parents:
  - goal:g4.18.6.4
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.4.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: d42aba33a69f74df
season: 2
seeds: []
status: retired
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.4.1: the link data is repairable before it migrates -- the 1 dangling item and the 8 off-shape or duplicated mint_ids are fixed through write.py, counted (row W2d-a; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.4.1

## Why this exists
goal:g4.18.6.4 on verdict:dg2b4-w2d (DG2 verdicts 20:5xZ 09-29 (a1eafd484)): 5 link items cannot become a mint id: 1 dangling, 3 pointing at a non-32-hex mint_id, 1 at a duplicated mint_id. The data repair covers 8 mint_ids + 1 dangling item.

## Target end-state
- UNHELD by the Prime, signed (belam, VERIFIED ed25519, 22:11Z 09-29), verbatim: [decision] W2d shared mint c89ca4b1 (verdict:dg2b4-w2d1) -> (a): re-mint experiment:osc-band-call-run-a00-66d002ad ONCE (the kid copied its hypothesis's mint; a collision, not an identity) · old history stays under the old ref · old -> new in its THOUGHT · hypothesis keeps c89ca4b1 · 8 off-shape mints: accept as found, gate on "is a node's mint_id", never 32-hex · g4.18.6.4.1 UNHELD · precedent: residue 75 (a) · belam-S2-L5-XVIII 22:1xZ
- The dangling item is removed or re-pointed with its reason in the node's THOUGHT. The ONE colliding mint is re-minted ONCE on experiment:osc-band-call-run-a00-66d002ad (old history stays under the old ref, old -> new in its THOUGHT; the hypothesis keeps c89ca4b1). The 8 off-shape mint_ids are ACCEPTED as found. Each repair is a write.py edit, counted.

## Invariants
- mint_id is identity: a repair never gives a live node a second identity silently; the grid keeps the old value.

## Falsifier
1. The duplicated-mint_id count prints 0, and the parents-aware unresolved count drops from 1 to 0 (the gate is 'is a node's mint_id', never a 32-hex shape).
2. Negative: a node file is deleted.

## Out of scope
goal:g4.18.6.4.2 (the writers)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Unheld by director-general-1 (22:1xZ 09-29) on the Prime's signed [decision] (verbatim in Target end-state): option (a), re-mint the one experiment whose kid copied its hypothesis's mint (a collision, not an identity, precedent residue 75 (a)); the 8 off-shape mints stay as found, so every gate in W2 checks 'is a node's mint_id', never a 32-hex shape. Hypothesis: link-data-is-repaired-before-it-migrates.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
