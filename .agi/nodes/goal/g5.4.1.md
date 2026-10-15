---
id: goal:g5.4.1
mint_id: 0a7143dc607b49579fc880895237063e
type: goal
parents:
  - goal:g5.4
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G5.4.1
goal_kind: subgoal
origin: goal
seeds: []
tags: []
season: 3
status: active
title: "G5.4.1: the end-of-season report is ONE standard HTML template node; the season rollover scripts render it for the season just closed, filling every number and table from the graph, and only the narrative is written by a model"
town: core
---
# goal:g5.4.1

## OWNER 2026-10-15 19:2xZ, verbatim
"ok report looks lovely. [...] Can we also standardize that end of season report format as some sort of config or standardized HTML node that we can just run our season rollover skill/scripts and have it display everything updated for the latest season automatically ish outside of things that need to be specified generatively."
(The whole message, with its start / stop and sign / push paragraphs, is verbatim on goal:g7.16.1.11.44.8.)

## Why this exists
goal:g5.4 (the season review and rollover, end to end): the season-2 -> 3 rollover report was built by hand at the end of the run (belam 10-15, published as the claude.ai artifact FpDnKNzsTQFP4ug5sit9kt, "Season 3 rollover"). The owner liked it and asked for that format as a standard, so that the next rollover renders it instead of rebuilding it. Seed: the hand-built page, copied to /data/work/belam-media/pipeline/report/season3-rollover.html (timeline, SVG branch map, heads and archives tables, graph stats, commit flow, engine pieces, open items, song player).

## Target end-state
The owner's ask, as stated; the council designs how, first (owner 10-15: "we always let council do design work first to simplify and streamline everything"):
- The end-of-season report format is standardized as a config or a standard HTML node.
- Running the season rollover skill / scripts displays it updated for the season just closed, automatically, except the parts that have to be written generatively.

## Invariants
- No spend on a provider or scale the owner did not name.
- Retire, never delete.

## Falsifier
None yet: the council cuts them with its design in season 3.

## Out of scope
goal:g7.16.1.11.44.8 (agi.sh start / stop) · goal:g5.13 (rollover side-quests)

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (belam 19:3xZ 10-15): the owner said "we always let council do design work first", so belam's own design in v1 (template slots, byte-equal reruns, digit-grep falsifier) is out. Only the owner's ask remains, assigned to the council. The seed page path in Why stays, as the input the owner pointed at.
<!-- THOUGHT:END -->
