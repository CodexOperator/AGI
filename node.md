---
id: goal:g7.31.5
mint_id: df1021547878404ab83dad1bc3483cb4
type: goal
parents:
  - goal:g7.31
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.31.5
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 1038c716b8cbf405
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - write
  - sync
  - profile
thought_session: magic-pane-2026-09-21
title: "G7.31.5: Graph↔harness-doc sync — write route keeps Grok Bot profile/settings driftless"
town: core
---
# goal:g7.31.5

## Why this exists

**Parent `goal:g7.31`.** Graph carries growth; Grok Bot profile/settings surfaces can drift from instruction/routine/standing/todo nodes. Owner ask 2026-09-21 ET: `write.py` (and the pane **write** route) to those node kinds also updates linked Grok Bot profile/settings; reverse when harness docs change if a bridge exists — **no drift**.

```
graph nodes (instruction / routine / standing / todo)
        │ write.py  +  pane write route
        ▼
Grok Bot profile / settings surfaces
        │ reverse bridge (if exists)
        ▼
graph nodes   ◄── no durable drift
```

## Target end-state

- A write to a linked instruction/routine/standing/todo node updates the corresponding Grok Bot profile/settings artefact in the same action (or a tightly coupled follow-up that cannot be skipped silently).
- If a reverse bridge exists (harness doc → graph), harness-side edits reconverge to the node; if not, the missing bridge is documented on this node as an explicit gap with a falsifier for when it lands.
- Drift check is measurable (hash / content equality / `drift_check` style), not vibes.

## Invariants

- Graph remains SoT for goal/contract content; profile surfaces are projections.
- Never invent a second SoT — if conflict, graph wins and profile is repaired.
- Uses the unified **write** route (`goal:g7.31.3`); no side-channel editor that bypasses `write.py`.

## Falsifier

1. Edit a linked standing/instruction node via `write.py`; linked Grok Bot profile/settings bytes change to match (or a named sync command exits 0 with proof).
2. (If reverse bridge claimed) edit harness doc; linked node updates — or the node explicitly records "reverse bridge absent" and falsifier 2 is N/A until built.
3. A deliberate desync is detected by an automated check (exit non-zero) before the next seat rotation.

## Out of scope

- Authoring the five routes (`goal:g7.31.3`).
- Pane hold / pin wiring (`.1` / `.2`).
- Handback transport (`.4`).
- Replacing `doc:standing-llm-ops` itself as the ops contract.

## Agent Notes

Assigned to **director-helper** with `.2` + `.4` AND keep `g7.26`–`g7.30` land batch. May further split; launch pi parent batches; diagram-max; batch-max; merge-up to Belam; blockers to owner only.

**Related:** `write.py`, pane write route (`goal:g7.31.3`), `goal:g7.26` (post briefs / custom instructions), `doc:standing-llm-ops`.
