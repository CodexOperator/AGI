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
status: active
title: "G7.16.1.11.44.8: ONE script agi.sh (routes start and stop) brings the whole town up on a fresh box with a fresh Claude install from a single skill call, and down again; every trap in the start / stop skills is code, and every input it needs is asked step by step in a captive flow"
town: core
---
# goal:g7.16.1.11.44.8

## OWNER 2026-10-15 19:2xZ, verbatim
"ok report looks lovely. I'm fine with doing whole town start-stop as one simple script next so the town can be started on a fresh claude completely fresh install on a fresh box with just a single skill call. We already have the relevant agi start/stop skills we're just gonna turn all the traps and things in that skill into code so its just a matter of running agi-start.sh and answering all the things it needs input custom step by step via a captive flow. Same with agi-stop.sh . Or just have agi.sh and it has both start and stop routes.

Also fix the issue between yourself only being able to sign but not push, and human can push but not sign. For now we just let you have both the power to sign and the power to push so you're technically matching the human owner in authority over the system and must therefore use it wisely.

Can we also standardize that end of season report format as some sort of config or standardized HTML node that we can just run our season rollover skill/scripts and have it display everything updated for the latest season automatically ish outside of things that need to be specified generatively."

## OWNER 2026-10-14 14:4xZ, verbatim
"Oh 33 pieces huh? Thats kinda neat from a numerology standpoint considering everything else. Is everything integrated into projections/matrix math? I was curious if the matrix system could be used to streamline how the crons are activated and deactivated (they can still use python underneath for this season so we can close it), and same with stopping and starting work for everyone as a whole via a process of packing up and unpacking that is just extension of the graph slice and allows me to restart on a fresh machine by just running the agi-start skill and stop things as needed with agi-stop that is just a simple set of commands. It could include automated message blasts to everyone active via shell scripts"

"Yes record but not cut it yet we need to reset the town bundle to a fresh bundle for the next season we will need a few rounds on it next season."

## Why this exists
goal:g7.16.1.11.44 (ONE pack format moves any graph slice; season rollover and box moves are the same pack / unpack): the owner asked to extend that pack / unpack to the whole town. Measured 14:4xZ 10-14 at ccabe03f0f: engine.md's `### matrix` piece has 4 rows (boot reads the engine via sect, boot projects the post units via agi-project, a post builds ~/bin via sect, a post builds its brief from its card). Crons are NOT a row: `.agi/nodes/.geometry/crons.md` reaches the crontab through `crons.py apply` (Python, every 5 min), outside the projection. Start and stop are per post (systemd units; after a reboot only the boot:true rows start, the rest by hand). No `agi-start` or `agi-stop` skill exists (skills/ listing at that time).

## Target end-state
The owner's asks of 10-15, as stated (the council designs how, first; owner 10-15: "we always let council do design work first to simplify and streamline everything"):
- ONE script, `agi.sh`, with a `start` and a `stop` route, run from a single skill call.
- `agi.sh start` brings the whole town up on a fresh box with a fresh Claude install, asking what it needs step by step in a captive flow; `agi.sh stop` brings it down.
- The traps and rules in today's start / stop text become code. That text is skill agi-post, skill agi's seating sequence, QUICKSTART.md section 2 and the sanctuary README; no `agi-start` / `agi-stop` skill exists as such (skills/ at b7b2962a6f).
The 10-14 bullets below are the earlier asks; the council's design decides how they and the 10-15 asks fit together.
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
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (belam 19:3xZ 10-15): the owner said mid-write "lets have the council run it first to design it better ... remember the rule we always let council do design work first to simplify and streamline everything". v2 had added belam's own design (an input list and a credential line in the target) and assigned SM to place. v3 keeps only the owner's asks in the target and assigns the council: it designs first, then SM places and gates. Status stays active, since the owner named this as season 3's next work. g7.16.1.12 (the fresh council bundle) is retired, so the parent stays .44; a re-parent is the council's call.
<!-- THOUGHT:END -->
