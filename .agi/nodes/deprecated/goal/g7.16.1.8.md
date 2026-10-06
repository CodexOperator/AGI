---
id: goal:g7.16.1.8
mint_id: 8eede4c80072443da617fa1b94649b4a
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: self-perpetuating
goal_id: G7.16.1.8
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: b013e4b4d03de2f1
season: 2
seeds: []
status: retired
tags:
  - sanctuary
  - init
  - standup
  - council-loop
title: "G7.16.1.8: one init pass + one captive stand-up script walk a user through a sanctuary box, every value read from the graph"
town: core
---
# goal:g7.16.1.8

## OWNER 2026-09-30 00:1xZ, verbatim (Prime pane)
"Sweet go ahead and do the changes and add it in then symlink it like the rest. Then we will need an ini pass and ideally one simple script that guides a user through sanctuary standup via one captive flow."

## Why this exists
goal:g7.16.1 (the council loop): the owner's line (00:1xZ 09-30) has two halves. The first, the guard into the graph and symlinked like the other global handles, landed with the Prime: build nodes for guard-init.sh, sanctuary-health, sanctuary-watch and GUARD.md, plus config:guard. This goal is the second half. Today a sanctuary box is stood up by hand across QUICKSTART.md, guard-init.sh (root, five layers), crons.py apply, the envfile check, provisioning and a hand-made /etc/sanctuary-guard/box. Nothing walks a new user through it end to end, and every value lives in a different file. Seen from the council's lens: standing up a BOX is the same act as standing up a POST (goal:g7.16.1.7), one scale up. So it reuses that line's formation template and link walk rather than growing a second stand-up machine.

## Target end-state
```
box formation template (link rows -> null): guard · crons · posts · env keys · provisioning · the repo clone
   └─ INIT PASS = goal:g7.16.1.7's link walk over those rows ─▶ per row: done · missing · needs-the-user   (idempotent)
        └─ CAPTIVE SCRIPT = a thin loop over the pass: show the step ─▶ ask only for rows the graph cannot fill ─▶ act ─▶ re-walk
             ends VERIFIED: guard --status all ok · crons applied · node count readable · links 0 broken
             ─▶ then ONE formation activation stands up the town's posts (goal:g7.16.1.7)
```
- **ONE init pass.** It reads every setting the stand-up needs from the graph (config:guard, config:crons, config:posts, the .env key check) through the box formation's link rows, and reports per row done / missing / needs-the-user. It is safe to re-run. It is also the "ini routine" of the owner's 21:0xZ 09-26 line on goal:g7.32.6 ("have the local box name be a global env variable that gets set as part of the ini routine"): the pass writes AGI_BOX, a LOGICAL label (the box name the captive script asks for), never the raw host name. AGI_BOX is the ONE source of box identity that every locality check reads, and goal:g7.32.6 cites it.
- **ONE captive script.** It is the flow a user runs on a fresh box. It asks only what the graph cannot know (box name and class, the user's accounts and keys), shows each step before it acts, and ends with the box verified. The human sees the walk as ONE live diagram (done / missing / needs-you rows) and is asked only for the needs-you rows, never a wall of prompts. The LLM reads the same walk through `viewport.py --emit llm`: one render, two readers (goal:g2.19).
- **A new box inherits the town.** A fresh box plus a clone plus the flow plus ONE formation activation gives a running town. The next box, or the next owner, stands the system up from the graph alone.
- **The prose follows the graph.** The stand-up steps live in the box formation; QUICKSTART.md and GUARD.md point at the flow and never restate a step the flow does not run or check.

## Invariants
- The flow never applies a root step without showing it first and getting a yes.
- Re-running the flow on a finished box changes nothing: every row reports done.
- Nothing the flow writes names a host, an address or hardware (the box is named by its box name and class), and no secret enters the graph: key rows record presence, never values.
- ONE walker: the init pass calls goal:g7.16.1.7's walk and never carries a second template reader.

## Falsifier
1. On a box that is already stood up, the flow run end to end reports done for every row and exits 0.
2. COLD START on a scratch box or container, never the live box: a clean clone plus the flow ends verified, and ONE formation activation brings up a post.
3. Negative: 0 stand-up steps documented only in prose (QUICKSTART.md, GUARD.md) that the flow does not run or check · `anonymize.py check` exits 0 over everything the flow writes · 0 template readers in the flow other than the walk.

## Out of scope
goal:g7.16.1.7 (the formation template, the link walk and the guard's build nodes this goal reuses; its walk goal:g7.16.1.7.2.1 lands first) · per-post user accounts and stricter key templates (season 3).

## Agent Notes
Assigned to **the council** (placement).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Owner 00:5xZ 09-30 via belam, verbatim: "I want them to use this step also as an opportunity to apply their lenses and zoomed out thinking at my words to see how they could be formed into goal wording even more optimally". Rewritten by self-perpetuating (council writer for .8; alive + all-is-one lens lines taken whole); OWNER section untouched. The lens (vision:self-perpetuating: a new box, and the next owner, stand the system up from the graph alone) changed: (1) MERGE with goal:g7.16.1.7: standing up a BOX is standing up a POST one scale up, so the init pass is that line walk over a box formation link rows (done / missing / needs-the-user) and the captive script is a thin loop over it: ONE walker, no second stand-up machine; (2) new target: a new box inherits the town (fresh box + clone + flow + ONE activation); (3) the human sees the walk as one live diagram and the LLM reads it through viewport --emit llm (alive: one render, two readers); (4) the init pass is the owner 21:0xZ 09-26 "ini routine" that writes AGI_BOX, a logical label and the ONE source of box identity (all-is-one, cross-goal with g7.32.6); (5) new invariant: no secret enters the graph; (6) the cold start runs on a scratch box, never the live one. Depends on goal:g7.16.1.7.2.1 (the walk).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
