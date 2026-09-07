---
id: goal:g1.6
mint_id: 2fde0822cd974042b6876cd06003ac0d
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.6
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G1.6: Every action is a one-word command, inside the project"
---
**No more reaching for a file whose path you have to know.** Today an agent runs
`python3 agi/extensions/agi/bin/zoom.py "$PWD" 9006 kid-a --level small --target
goal:g6.3`. Every element of that except `goal:g6.3` is ceremony — an interpreter,
a four-segment path, a redundant cwd, an iteration number and an agent id the
harness already knows. The agent spends motion on the invocation instead of the
question, and gets the path wrong sometimes, which is worse.

**Target: one or two words, options optional, discoverable from inside the
project.** `agi zoom goal:g6.3`. `agi node new hypothesis --parent goal:g6.3`.
`agi resume <grid-ref>`. `agi audit`. Installed as part of adding agi to any
project (**G1.5**), so the command surface exists the moment the project does and
is identical in every project.

The list worth having, drawn from what actually cost tool calls in the 2026-08-23
run:
- **navigate** — zoom to a node, widen, step to a neighbour, raise LOD (**G10**)
- **write** — create or edit a node without hand-assembling frontmatter, which is
  where kids currently spend their first three tool calls and where they get
  `evidence_runs` shapes wrong
- **resume** — pick up from any point in the grid, which is the crash-recovery
  story the two-cadence cron already half-implements
- **audit** — what is unevidenced, what is orphaned, what fails to parse. Every
  one of those was a bespoke Python one-liner this session

**The measurable is the point, not the ergonomics:** fewer tool calls and fewer
tokens burned on recon *and* on acting. This is the Design Ethic's ratio attacked
from the second side — G1.3 and G10 reduce the recon a task needs, this reduces
what each action costs once you know what to do.

Note the reflexive risk and avoid it: these commands are engine surface, so under
**G6.8** they arrive from nodes rather than being written directly. Absorbs
**S1**'s rename (`bin/` is invisible to GitNexus) — do them together, since both
touch every entry point.

Falsifier: take the transcript of any completed iteration and count invocations
that needed an absolute path or an interpreter prefix. Not done until that is zero.