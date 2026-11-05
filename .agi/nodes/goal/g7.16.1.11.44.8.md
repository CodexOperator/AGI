---
id: goal:g7.16.1.11.44.8
mint_id: 43e635ecabe54c5b9b756afa6325319c
type: goal
parents:
  - goal:g7.16.1.11.44
next_edges: []
confidence: 0.5
edited_by: director-goals-1
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

## OWNER 2026-10-15 19:5xZ, verbatim (answers to the council's five questions, relayed by belam)
"1. Both is good
2. That works 
3. You that works
4. Generate each time 
5. Yup by hand is fine"
The questions, in the council's order: (1) .44.8 acceptance: an nspawn container on this box with claude stubbed, AND the owner's next real fresh box -> BOTH. (2) .44.8 skill name: one skill, agi-town -> YES. (3) g5.4.1 template: a build node gated like code -> YES (belam reads "You that works" as "Yup that works"). (4) g5.4.1 song: generated each season, not only from an owner-handed file -> GENERATE EACH TIME. (5) g5.4.1 publish: the Prime by hand -> YES.

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
The council's falsifier (3/3, alive 10-22 08:4xZ; it replaces the 10-15 draft). F0 is the part a post can run: stubs only, no town stop, 0 USD. F1 and F2 are the OWNER's two acceptance runs (owner 10-15 19:5xZ Q1, "Both is good") and stay BANKED until he runs them.
F0. Both town lanes exit 0 on a bare environment, and the stop -> start round trip is a named row with its three mutants (this command exits non-zero until the round-trip row is in the lane):
`o=$(mktemp -d) && env -i PATH=/usr/bin:/bin sh extensions/agi/tests/agi-town.t.sh >$o/a 2>&1 && env -i PATH=/usr/bin:/bin sh extensions/agi/tests/agi-town-start.t.sh >$o/b 2>&1 && grep -q '^ok st-the-town-is-down ' $o/a && [ "$(grep -c '^ok st2-RT2-' $o/b)" = 4 ]`
 - The 10-15 draft's F2 (0 agi-post@ units and 0 marked cron lines after a stop) is the S1 row `st-the-town-is-down` in agi-town.t.sh.
 - The round trip is `st2-RT2-same-set-same-crons-one-town-line-each` in agi-town-start.t.sh: a fixture town up -> `agi.sh stop` -> `agi.sh start` gives the SAME active agi-post@ set, `crons.py show` unchanged (read from the fake's log), and the town line once per active post (the box calls, logged).
F0 negative: three mutants, each RED (the row passes only when the clean property breaks): `st2-RT2-mutant-start-drops-a-post-RED` (start leaves one post down), `st2-RT2-mutant-stop-leaves-a-cron-line-RED` (stop leaves one cron line), `st2-RT2-mutant-double-town-line-RED` (a post gets two town lines).
F1 (OWNER, BANKED). The same stop -> start in an nspawn container on this box with claude stubbed. `systemd-container` is not installed (dpkg: un); installing it is a host act, belam's on the owner's GO.
F2 (OWNER, BANKED). The same stop -> start on the owner's next real fresh box. This is the SAME owner event as the live half of goal:g7.16.1.11.44.7 (the first real box move = the owner's next fresh box).
This leaf stays active until the owner closes or keeps it; F0 green is "built and stub-proven", not complete.

## Out of scope
goal:g7.16.1.11.44.7 (box-move.sh calls the capsule verbs) · season-2 close and rollover (goal:g7.16.1)

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v4 (director-goals-1 10-22, on the council's .44.8 decision 3/3 08:4xZ, placed by SM 08:47Z): the 10-15 draft falsifier is replaced by the real one (F0 / F1 BANKED / F2 BANKED). Why not closing it "superseded by the binds": the owner set the acceptance on 10-15 19:5xZ (Q1, "Both is good": an nspawn container with claude stubbed AND his next real fresh box), so a close without those two runs would report it done against his own words. The binds that landed under this goal are L31 (S2a + R1: the host act folds into agi.sh host, host.done = the pin), L35 (S2b: agi.sh start, main host posts crons units blast, + skill agi-town), L36 (S2b follow-up: B-6, R-d, B1 order, ring line, titles line), L39 (S2b BIND: B-7 trigger skip, H1 answered by removal) and L42 (S2b (iii): a oneshot with RemainAfterExit=no is never recorded or stopped; the pid row); the other stacks in L31-L50 belong to other goals. The only build left is the round-trip row. F2's remainder points at the same owner event as goal:g7.16.1.11.44.7's live half, per the council's .44.7 ruling relayed through SM. For the owner's report, verbatim from the council: ".44.8: built and stub-proven (F0, incl. the stop -> start round trip); your two acceptance runs (nspawn: needs your GO for the systemd-container install; your next fresh box) are yours. It stays active until you close or keep it." Before this, v3 (belam 19:3xZ 10-15): the owner said the council designs first, so the target holds only his asks; status stays active as season 3's next work.
<!-- THOUGHT:END -->
