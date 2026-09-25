---
id: goal:g5
mint_id: 71c02192f832480f85cb075ad649a451
type: goal
parents:
  - vision:self-perpetuating
confidence: 1.0
edited_by: belam
goal_id: G5
goal_kind: perpetual
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - exp:g5-lifecycle-enforcement
  - goal:g5.1
  - idea:engine-schema-registry
  - idea:engine-snapshot-build-site
  - idea:engine-snapshot-goals
  - mvp:strict-goal-refs
status: horizon
tags:
  - goal
  - root
thought_session: belam-S2-L5-II
title: "G5: Local-maxxing"
---
# goal:g5

## Why this exists
**Parent `vision:self-perpetuating`.** The local-maxxing town's umbrella (perpetual; absorbs the old G4 and G14, G24 folded 2026-09-19): research that gets the most out of the local hardware on local-town. Owner 09-24: "Goals are project trackers" — the town's ops, research bundle and what's left live on `town:local-maxxing`; this node only tracks them.

## Target end-state
- every live local-maxxing line of work is a subgoal `goal:g5.N` or a hypothesis under one, listed in the GOAL BUNDLE of `town:local-maxxing`
- the town's board and trajectory live on the town node (the trajectory node once minted), the owner's lines in the grid versions of this node — never in this body

## Invariants
- this body keeps the schema's fixed order and holds no notes: rules → HEAD / templates / configs / role docs, facts → their own nodes, the board → `town:local-maxxing` (owner 09-24, the HEAD's notes line)

## Falsifier
1. `python3 extensions/agi/bin/snapshot-goals.py --render --check` exits 0 with this body under 40 lines
2. negative: a `## ` heading in this body outside the fixed order → FAILED

## Out of scope
- the pre-renumbering G5 prose (goal lifecycle enforcement: retired goals stop scoring, the three-depths invariant, `--strict-goals`, L5 / L15 / L18; landed 08-23, revised 09-01, landed 09-02): verbatim in `doc:g5-lifecycle-history`, the landed work in its seeds `exp:g5-lifecycle-enforcement` and `mvp:strict-goal-refs`
- sibling towns' goals (`town:core`, `town:sanctuary`, `town:streaming-suite`, `town:web-app-suite`)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 4 closed on the PASS 3 tooling unchanged (build/launch/verdicts copied to /tmp/belam-pass4 with BASE/TIP/OS and p4 run keys); the capped launch never bound (2 chunks). No deviation from section 2 of the crons file.
<!-- THOUGHT:END -->

## Agent Notes
Assigned to **thought-master** (the local-maxxing town master); a perpetual umbrella (absorbs the old G4 / G14; G24 folded in 2026-09-19).

PASS 3 09-24 (belam-S2-L5-III): trunk @9fec96488 -> season2/main 6f5ee34e5c · BASE ebae4adde · 838 commits · 150 exp files -> 102 hypothesis + 8 engine-delta = 110 rounds · 22 chunks · pi-free · 04:57-06:09Z (71 min) · 0 USD · 8 accept · 64 accept_with_residue · 38 demote · 0 RED · gates: links 0 · goals identical · smoke 4019+226 = 4245 = TIP · node D 1 = move (mint_id live) · residues: hypothesis:pass3-0924-residue-batch + 11 code-defect hypotheses -> director-engine

PASS 4 09-24 (belam-S2-L5-III): trunk @3b0c4e8e8 -> season2/main ad81688a0b · BASE 9fec96488 · 146 commits · 10 exp files -> 5 hypothesis + 1 engine-delta = 6 rounds · 2 chunks · pi-free · 13:47-14:05Z (18 min) · 0 USD · 1 accept · 3 accept_with_residue · 2 demote · 0 RED · gates: tree == TIP · links 0 · goals identical · smoke 4043+226 = 4269 = TIP · node D 0 · residues: hypothesis:pass4-0924-residue-batch
