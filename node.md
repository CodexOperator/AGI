---
id: goal:g7.32.2
mint_id: d1a01e938c1d442b9ddb4d340984c8e3
type: goal
parents:
  - goal:g7.32
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.32.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: f7e2e4fc9ba22145
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - magic-pane
  - messaging
thought_session: owner-ask-2026-09-21
title: "G7.32.2: Magic-pane messaging — grok↔grok native; grok→claude/pi nudge→send"
town: core
---
# goal:g7.32.2

## Why this exists

**Parent `goal:g7.32`.** Owner vision: **magic-pane messaging** —
- **grok↔grok** native (same harness, pane-to-pane)
- **grok→claude/pi** via **nudge→send** (cross-harness; never pretend native)

g7.31.1 is the durable pane **precursor**; this child is the **messaging product** on that pane.

## Target end-state

```
        ┌── native ──┐
   grok A             grok B
        └── nudge ──▶ send.py ──▶ claude / pi
```

- Native path never shells out to `send.py` for same-harness.
- Cross-harness always: nudge (pane intent) → `send.py` (transport).
- Diagram-max every messaging design note.

## Invariants

- Does not re-spec g7.31.1 hold or g7.31.3 five routes — messaging **uses** them.
- Cross-harness never claims "native".
- No formation/policy inside the messaging adapter (that stays seats/rotate).

## Falsifier

1. Same-harness grok↔grok demo path documented + scripted without invoking send.py transport.
2. Cross-harness path shows nudge artifact then send.py invocation in one measured trace.
3. Grep: messaging module does not import rotate/dispatch internals.

## Out of scope

- send.py implementation details (g7.32.4).
- Optional pane method shape on the adapter (g7.32.3).
- Five engine routes list (g7.31.3).

## Agent Notes

**Extends:** `goal:g7.31.1` (pane precursor). **Feeds:** `goal:g7.32.4`. Session: `owner-ask-2026-09-21`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
standing body whole-replace owner-ask-2026-09-21
<!-- THOUGHT:END -->
