---
id: goal:g7.31.2
mint_id: 0b5d7a874be445e98a23f17855c0a38b
type: goal
parents:
  - goal:g7.31
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.31.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: ae72206c9d0fb32b
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - harness
  - grok-bot
  - pane
  - pin
  - formation
  - rotate
thought_session: belam-horizon-4b-2026-09-21
title: "G7.31.2: Pane anchor registers seat occupation across post/pin/formation/auto-rotation"
town: core
---
# goal:g7.31.2

## Why this exists

**Parent `goal:g7.31`.** A pane that does not register as seat occupation is theater: rotate rebuilds argv, pins drift, formation cannot see who holds what. Owner ask 2026-09-21 ET: the **same pane anchor** registers seat occupation, survives rotate, and never opens a second argv path.

```
pane anchor
   │
   ├─▶ posts row / seat registry  (occupied)
   ├─▶ pin                        (survives rotate)
   ├─▶ formation                  (visible holder)
   └─▶ auto-rotation              (successor reuses pane contract)
```

## Target end-state

- Attaching the named pane **is** registering occupation (posts/seat registry coherent with tmux state).
- Rotate / auto-rotation reuses the pane contract via template + persistent dispatch — **no** second argv builder in `rotate.py`.
- Formation and pin readers see the live holder without scraping panes ad hoc.

## Invariants

- Single argv seam: adapter + template (`goal:g7.27`) + persistent dispatch (`goal:g7.28`); rotate stays orchestration (`goal:g7.29`).
- Pane name / seat pin are one-writer facts (no dual registries that disagree).
- Soft-depends on durable hold from `goal:g7.31.1` but may design the registry contract in parallel.

## Falsifier

1. After seat start: posts/seat registry shows occupied with the live pane/session pin matching `tmux`.
2. After rotate-self (or auto-rotation): successor holds the **same** pane-contract (name or documented successor rename); no `_build_*_command` path reappears in rotate for grok.
3. Grep `rotate.py` for new harness argv builders: **zero** (orchestration only).

## Out of scope

- Measuring CLI flags (`goal:g7.31.1`).
- Messaging / handbacks (`goal:g7.31.4`).
- Doc sync (`goal:g7.31.5`).

## Agent Notes

Assigned to **director-helper** with `.4` + `.5` AND keep `g7.26`–`g7.30` land batch. May further split; launch pi parent batches; diagram-max; batch-max; merge-up to Belam; blockers to owner only.

**Related:** `goal:g7.28`, `goal:g7.29`, `goal:g7.30`, `goal:g7.31.1`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
horizon-pass not in-flight unclaimed on board
<!-- THOUGHT:END -->
