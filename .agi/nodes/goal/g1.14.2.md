---
id: goal:g1.14.2
mint_id: daa86834f6a941c28f1ad288c7f16eb7
type: goal
parents:
  - goal:g1.14
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G1.14.2
goal_kind: subgoal
origin: goal
seeds: []
tags: []
season: 3
status: horizon
title: "G1.14.2: our own workflow tool -- every workflow agent is a graph spawn on the ONE spawn / rotate route through the matrix, and a workflow template per role (post, parent, kid) says what that agent does"
town: core
---
# goal:g1.14.2

## OWNER 2026-10-14 ~20:1xZ, verbatim
"And also as far as integrated workflows every workflow is just a subagent spawn using our new matrix math system but thay use it in a more limited way we can do that next season though"

## OWNER 2026-10-14 ~20:3xZ, verbatim
"That’s fine let’s go ahead and do the rollover and bank the thing I said above regarding workflows where we create our own workflow tool using graph spawn/rotate unified route with custom workflow templates describing what a given workflow agent post/parent/kid whatever role works best should do"

## Why this exists
goal:g1.14 (ONE workflow router, every workflow dispatched through it): the owner named the next form of that router for season 3. Measured 20:3xZ 10-14 at 0c4f901759: workflows run through `extensions/agi/bin/workflow.py` (3229 lines) over 30 files in `extensions/agi/workflows/` (14 .js scripts + 16 .json manifests); posts are spawned and rotated by `rotate.py` (23418 lines) and `dispatch.py` (4543 lines); engine.md's `### matrix` piece has 4 rows and no workflow row. A workflow agent today is not a graph spawn on the post route.

## Target end-state
- A workflow is our own tool: each workflow agent is a subagent spawn on the ONE graph spawn / rotate route, through the matrix, used in a more limited way than a post (a smaller slice, a shorter life).
- A custom workflow template per role (post, parent, kid, or whichever role fits) describes what that workflow agent does; a workflow is a template plus its args, not a hand-written script.
- workflow.py's separate runner retires (retire, never delete) once every live workflow runs on that route.

## Invariants
- Retire, never delete: the old .js / .json workflows stay in git history and on their retired path.
- No spend on a provider or scale the owner did not name.

## Falsifier
Draft, banked on the owner's word; the council cuts the real ones in season 3 ("we can do that next season").
1. A named workflow (one of today's 14) runs from its role template alone through the spawn / rotate route, and its run record names the template, the role and the matrix row.
2. Negative: 0 live workflows dispatched by workflow.py's own runner at the season-3 close.

## Out of scope
goal:g1.14.1 (a round stage chains a parent dispatch into its review) · goal:g7.16.1.10.7 (the merge gate; owner 10-14: it reads the town board and runs its checks as .sh / .py)

## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (belam 20:3xZ 10-14): minted on the owner's word to BANK, not cut: status horizon, season 3, so the council's season-3 board derivation (horizon AND 'season 3') lists it. Parented under goal:g1.14 because that goal already owns "ONE workflow router"; the owner's two lines are its next form. Assigned to the council, which cuts goals; belam assigns no design or build.
<!-- THOUGHT:END -->
