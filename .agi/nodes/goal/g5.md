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
09-24 03:4xZ, owner (the Prime's pane, verbatim): "Edit the g5 body to put it mostly into the local-town town node in knowledge graph. Thoughtmaster piled it full of stuff. Ping him when done. Distribute notes where appropriate according to rules" -- with the 03:3xZ line thought-master acted on (verbatim in v52): "Now move the notes added to g5 to the town board or individual role docs where they belong. Belam already had to add the standing rule to prime role doc might need in the head instead. Notes go into templates or configs, then individual role docs, then town board node. Goals are project trackers". The Prime's version (belam-S2-L5-II): thought-master's v52 had already moved the 131 Agent Notes (its THOUGHT maps each note to its home; grid.py log goal:g5, v52). What remained was the pre-renumbering G5 body (goal lifecycle enforcement, 117 lines) under the new title. It is engine history, not the town's ops, so by the rules it did NOT go onto town:local-maxxing: it moved VERBATIM to doc:g5-lifecycle-history (extracted by line range, never retyped); its landed work already lives in its seeds. The body is now the fixed-order tracker of [goal].md (Why this exists, Target end-state, Invariants, Falsifier, Out of scope, Agent Notes). Near miss: pasting the old prose into the town node satisfies the words 'mostly into the town node' and breaks the rule that a town board carries only the town's ops.
<!-- THOUGHT:END -->

## Agent Notes
Assigned to **thought-master** (the local-maxxing town master); a perpetual umbrella (absorbs the old G4 / G14; G24 folded in 2026-09-19).
