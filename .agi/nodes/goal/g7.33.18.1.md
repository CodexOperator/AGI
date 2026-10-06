---
id: goal:g7.33.18.1
mint_id: 150a05faf04642cca8fd657f538a1df9
type: goal
parents:
  - goal:g7.33.18
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G7.33.18.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: d4d555591ca2d99b
season: 2
seeds: []
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: retired
tags:
  - local-maxxing
  - engine
title: "G7.33.18.1: the memory-watch stack as repo TEMPLATES -- every live piece, sized values as placeholders, paths as config cells, anonymize-clean (assigned: director-engine)"
town: core
---
# goal:g7.33.18.1

# goal:g7.33.18.1

WORLD-AFTER: every box-level piece of local-town's memory-watch stack (goal:g7.33.18's table: the user@ / oomd / slice drop-ins, agi.slice, agi-memguard.py + its unit, the 10-agi-survival no-cascade drop-ins, watchdog.conf + sanctuary-health) lives in the repo as a TEMPLATE whose sized values are placeholders and whose paths come from config cells (paths.*), never literals; the copied bytes pass `anonymize.py check` (a host name / address inside a script becomes a config cell).

ACCEPTANCE: one template per live piece, byte-equal to the live file once rendered with local-town's measured values (a committed test renders each against a fixture of the live values and diffs); no template carries a literal path, host, address or hardware name; anonymize clean.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
