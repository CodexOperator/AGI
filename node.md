---
id: goal:g7.16.1.11.44.8
mint_id: 43e635ecabe54c5b9b756afa6325319c
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G7.16.1.11.44.8
goal_kind: subgoal
origin: goal
seeds: []
tags: []
season: 3
status: horizon
title: "G7.16.1.11.44.8: the town starts and stops as a whole from the matrix -- agi-start unpacks the graph slice onto a fresh machine and brings every post and cron up, agi-stop packs it and brings them down, each a short set of shell commands"
town: core
---
# goal:g7.16.1.11.44.8

## OWNER 2026-10-14 14:4xZ, verbatim
"Oh 33 pieces huh? Thats kinda neat from a numerology standpoint considering everything else. Is everything integrated into projections/matrix math? I was curious if the matrix system could be used to streamline how the crons are activated and deactivated (they can still use python underneath for this season so we can close it), and same with stopping and starting work for everyone as a whole via a process of packing up and unpacking that is just extension of the graph slice and allows me to restart on a fresh machine by just running the agi-start skill and stop things as needed with agi-stop that is just a simple set of commands. It could include automated message blasts to everyone active via shell scripts"

"Yes record but not cut it yet we need to reset the town bundle to a fresh bundle for the next season we will need a few rounds on it next season."

## Why this exists
goal:g7.16.1.11.44 (ONE pack format moves any graph slice; season rollover and box moves are the same pack / unpack): the owner asked to extend that pack / unpack to the whole town. Measured 14:4xZ 10-14 at ccabe03f0f: engine.md's `### matrix` piece has 4 rows (boot reads the engine via sect, boot projects the post units via agi-project, a post builds ~/bin via sect, a post builds its brief from its card). Crons are NOT a row: `.agi/nodes/.geometry/crons.md` reaches the crontab through `crons.py apply` (Python, every 5 min), outside the projection. Start and stop are per post (systemd units; after a reboot only the boot:true rows start, the rest by hand). No `agi-start` or `agi-stop` skill exists (skills/ listing at that time).

## Target end-state
- The matrix carries crons and town start / stop as rows: ONE projection turns the crons on and off, the way agi-project writes the post units.
- `agi-start` on a fresh machine unpacks the town's graph slice (the .44 pack format) and brings every post and every cron up; `agi-stop` packs it and brings them down. Each skill is a short set of shell commands.
- A start or a stop sends one message to every active post (a shell broadcast over `box`).
- Season 2 closes on the Python crons as they are; this lands in season 3.

## Invariants
- Retire, never delete: a packed town is a graph slice, every node and grid ref kept.
- No spend on a provider or scale the owner did not name.

## Falsifier
Draft, recorded on the owner's word; the council cuts the real ones in season 3 (owner 14:4xZ: "record but not cut it yet").
1. On a scratch box: `agi-stop` then `agi-start` from the pack alone gives the same running post set and the same crontab as before (`crons.py show` diff empty), and every active post received the broadcast once.
2. Negative: after `agi-stop`, 0 agi-post@ units running and 0 agi cron lines in any uid's crontab.

## Out of scope
goal:g7.16.1.11.44.7 (box-move.sh calls the capsule verbs) · season-2 close and rollover (goal:g7.16.1)

## Agent Notes
Assigned to **belam**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (belam 14:4xZ 10-14): minted on the owner's word to RECORD, not cut: status horizon, season 3. The owner also said the town bundle resets to a fresh bundle for season 3, so this leaf is re-parented (renumber, mint_id kept) under that bundle when it is cut; the council cuts its leaves there, over a few rounds. Assigned to belam only as the holder until that cut; belam assigns no design or build.
<!-- THOUGHT:END -->
