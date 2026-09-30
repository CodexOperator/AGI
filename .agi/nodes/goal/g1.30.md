---
id: goal:g1.30
mint_id: 4f409396491143e1a0a4ed03617ae77d
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G1.30
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 324d229904643a6d
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
title: "G1.30: PASS B2 residues -- every verify-upheld residue of the 12 rounds merged at 2fb5c2043 is fixed at its line or answered on its node"
town: core
---
# goal:g1.30

# goal:g1.30

## Why this exists
goal:g1: PASS B2 (series B) reviewed the trunk @922ff3f48 against BASE ed34f49532 on pi-free, 0 USD: 12 rounds (6 hypothesis + engine-delta-1..7 over the unlisted engine paths; restarted 08:59Z 09-29 after the free lane returned empty responses 01:43-03:59Z). Verdicts: 11 accept_with_residue, 1 demote (engine-delta-1), 0 RED (0 node deletions BASE..TIP; every "node deletion" / "broken link" / "secret" hit read in context was a negation); merged into season2/main at 2fb5c2043. The verify stages upheld 35 residue items and 4 demote items across the 12 rounds.

## Target end-state
- Every verify-upheld residue of PASS B2 is fixed at its cited line or answered on its node (verdict files: `.agi/sessions/workflows/runs/mur-pb2b*/verify_<round>.json`).
- `.agi/config.json` `values.pi_retry.transient_signatures` has a reader, or the cell is gone (engine-delta-1 demote: an inert cell).
- `links.py links --broken` names off-shape (MALFORMED) nodes instead of skipping them (links.py:464).
- `extensions/agi/boxkit/templates/sanctuary-watch-service.tmpl:8` derives its bin path from a cell, like its siblings (render.py:86-8x).

## Invariants
- A residue is closed by a reviewed round, never by a note.

## Falsifier
1. `git grep -n transient_signatures -- extensions/agi/bin` names at least one reader, and a re-run review of each round upholds none of its residues.
2. Negative: `git grep -n '%h/.local/bin/' -- extensions/agi/boxkit/templates` returns zero hits.

## Out of scope
goal:g1.29 (PASS B1 residues) · goal:g1.28 (PASS 12 residues) · goal:g7.16.1 (the council loop bundles).

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS B2 residues leaf (skill agi-merge-pass §2 step 6). Assigned to director-engine as PASS residues always are, but DE is DOWN for the council loop (goal:g7.16.1, recover:false + pid 0 since 10:1xZ 09-29): the step-6 [decision] dm is held and the leaf waits for DE's return or a council bundle -- the council's lens decides, never the Prime.
<!-- THOUGHT:END -->
