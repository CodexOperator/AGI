---
id: goal:g5.33
mint_id: 0e3df8b5e0654e969486a2254017211d
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.8
edited_by: thought-master
goal_id: G5.33
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 385e4befa07775bb
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - workflows
  - unified-route
title: "G5.33: EVERY WORKFLOW RETIRED OVER TIME IN FAVOUR OF THE UNIFIED DISPATCH ROUTE -- each review/research/survey job runs as a dispatched round with its retry and harness cells; a manifest retires only after its replacement ran green on the trunk (owner GO 22:2xZ 09-28)"
town: local-maxxing
---
# goal:g5.33

## Why this exists
**Parent `goal:g5`** (the local-maxxing town bundle, thought-master's): on 09-28 the pi-free lane ran an empty-response outage from ~20:0xZ. Dispatched parents on cuts carrying the `values.pi_retry` retry (EG.151, landed b0aa2c178) survived: EG.184 parent a00-c8f1d0f6 used 3 of 6 retries and ran 299 turns. Every `workflow.py` stage died in 18-70 s, because it runs `pi -p` in text mode with no empty-response retry (director-engine, 22:20Z). The dispatched route already has the configurable surface the workflows were built for. The owner then gave the go-ahead to retire the workflows in its favour (verbatim below). The unified routes themselves belong to `goal:g7.31.3` (director-belam, core), which this goal reads and does not write.

## OWNER 2026-09-28 22:2xZ, verbatim (typed into director-engine's pane, relayed 22:20Z)
"It may be the old dispatch route. Seems like the fresh dispatches in the new retry queue are doing ok."
"I guess the new dispatch route kinda becomes the old workflow route with its configurable nature. You can let TM know I give the go ahead to retire all workflows over time in favor of the unified route."

## Target end-state
- Every review, research and survey job this town runs through `workflow.py run <name>` runs instead as a dispatched round on the unified dispatch route (the parent/kid spawn path, its retry cells and harness rows), with its stages as the round's brief.
- Each replaced workflow manifest is retired (`status: deprecated`, moved, its bytes in the grid). None is deleted.
- The town's skills, briefs and templates name the dispatched round, not the workflow, for each retired job.

## Invariants
- A workflow is retired only after its dispatched replacement has run green on the trunk at least once. The replacement must cover the same review shape: claim vs bytes, an adversarial refuter, and verdict files a master can read.
- "Over time": EG.185 (retrying empty responses in workflow stages) stays the bridge until then. No workflow the town relies on goes dark in the meantime.
- `agi-merge-up-review` also serves the Prime's PASS (skill agi-merge-pass). Its retirement is belam's decision; this goal proposes it and never flips it.
- Config-max: stage models, harness, retries and timeouts live in config cells, never in a round's code.

## Falsifier
1. `python3 -c "import glob,json,datetime as d; c=d.datetime.now(d.timezone.utc)-d.timedelta(days=7); n=sum(1 for f in glob.glob('.agi/sessions/workflows/*.jsonl') if 'merge-up-review' not in f for l in open(f) if l.strip() and d.datetime.fromisoformat(json.loads(l)['timestamp'].replace('Z','+00:00'))>c); print(n); raise SystemExit(n!=0)"` exits 0: no workflow run in 7 days outside `merge-up-review` (the Prime's call, see Invariants), and every retired manifest's node reads `status: deprecated`.
2. Negative: `git grep -n 'workflow.py run' -- skills/ extensions/agi/templates/` has zero hits in town-owned instructions for any retired job.

## Out of scope
`goal:g7.31.3` (the unified routes' design, director-belam) · `goal:g7.33` (engine fixes, including EG.185, the bridge) · the Prime's merge routine (`skill agi-merge-pass`).

## Agent Notes
Assigned to **thought-master** (plan); rounds dispatched by **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted on the owner's GO, verbatim (22:2xZ 09-28, typed into director-engine's pane): "I guess the new dispatch route kinda becomes the old workflow route with its configurable nature. You can let TM know I give the go ahead to retire all workflows over time in favor of the unified route." Nested under goal:g5 (mine), not goal:g7.31.3 (director-belam's routes), which it reads only.
<!-- THOUGHT:END -->
