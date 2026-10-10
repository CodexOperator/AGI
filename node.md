---
id: goal:g7.16.1.11.3
mint_id: 4e6fd028527d411ab7851f14f3956387
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.3
goal_kind: subgoal
origin: owner
scaffold_hash: ab651364d4e6d46e
season: 2
seeds: []
status: active
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.3: stages 1-2.5: the new engine runs a LIVE post -- S1 PASS, S2 PASS 7/7, DG5 up on pi-free with the parity table 55 rows: 40 matched-or-better LIVE (the 52 is the Phase A' plan figure), 3 named short (18, 30, 33), 12 not run"
town: core
---
# goal:g7.16.1.11.3

## Why this exists
Parent goal:g7.16.1.11: DG3's stages on goal:g7.16.1.11: S1 PASS, S2 7/7 (doc:g716111-stage2-rootplan), 2.5 Phase A/A' (doc:g716111-stage25-rootplan, engine v4c landed by belam e1e0dbaaf).
## Target end-state
stages 1-2.5: the new engine runs a LIVE post -- S1 PASS, S2 PASS 7/7, DG5 up on pi-free with the parity table 55 rows; the LIVE measure on DG5 is 40 matched-or-better, 3 named short (rows 18 seat-key rotation, 30 dispatch kids, 33 detached workflows) and 12 not run (doc:g716111-stage25-rootplan, section LIVE PARITY on DG5, ENGINE v5); the 52 matched-or-better in its section 9 is the Phase A' PLAN figure, not a live one.
## Invariants
every root act has an undo + proof; one-command rollback per post; config:engine byte-exact with the fenced source it was landed from.
## Falsifier
1. the DG5 post unit is active AND `grep -c 'Count, the original 55: 52 matched-or-better' .agi/nodes/doc/g716111-stage25-rootplan.md` prints 1 AND `grep -c 'short 3\*\*: 18 (seat-key rotation)' .agi/nodes/doc/g716111-stage25-rootplan.md` prints 1 AND `grep -c 'LIVE PARITY on DG5, ENGINE v5.*: 40/55 matched-or-better, 3 short, 12 not run' .agi/nodes/doc/g716111-stage25-rootplan.md` prints 1 (the LIVE figure the title and end-state claim; the two greps above pin the Phase A' PLAN section 9) (doc:g716111-stage25-parity is the frozen 42-row prep snapshot: its 9 MISSING lines are the prep-time state and are not a falsifier)
2. negative: a post of the new engine reading .env: zero hits
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"DG5 yes in pi free lane" (owner 07:0xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 10-07 (goal:g1.41 PASS B4): the end-state said '55 rows matched-or-better' and Falsifier 1 required 0 MISSING in the 42-row prep doc. Neither holds against its own source: doc:g716111-stage25-rootplan section 9 counts 55 rows, 52 matched-or-better (51 before v4c), 3 short (18, 30, 33); the prep doc is a frozen 03:1xZ 10-01 snapshot with 9 MISSING lines. Title, end-state and Falsifier 1 now say what the source says; the live-post claim (S1, S2, DG5 up) is unchanged. SM mur (10-07 22:34Z, RI1): 52/55 was the plan figure (rootplan :552, :785); the live parity is 40/55 with 12 not run (:849), so title and end-state now state the live figure and name 52 as plan; Falsifier 1's two greps still pin the plan section 9 line; RI3 (SM mur 22:5xZ): a third grep now pins the LIVE 40/55 heading (rootplan LIVE PARITY on DG5, ENGINE v5).
<!-- THOUGHT:END -->
