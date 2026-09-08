---
id: hypothesis:l3-workflow-run-serial-and-unleased
mint_id: 5ce2142f887b41f7ba1abf37698b2f08
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-X
scaffold_hash: 0b3bc71128d7c27b
season: 2
testable_claim=Measured: "live 2026-09-08: workflow.py run deep-search --harness pi kept exactly one pi child alive at a time while spawn_budget.py status showed none of them. After the change, stages the manifest declares independent are spawned concurrently under a declared cap, every workflow-spawned agent takes a spawn_budget lease so status counts it, and the two properties are proven by a red-first test asserting concurrent children for an independent stage and a lease count that rises for the duration of a run"
thought_session: belam-S1-L3-X
title: The unified workflow route runs its independent stages serially and takes no spawn lease, so a fan-out costs N times the wall clock and spawn_budget reports an idle box while it works
---
<!-- BODY:BEGIN -->
# hypothesis:l3-workflow-run-serial-and-unleased

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

FOUND BY USING IT, NOT BY READING IT. `workflow.py` is the unified route every workflow now dispatches through (owner, 2026-09-08: "always dispatched from the unified route. As always everything unified"). The first real run through it — `workflow.py run deep-search --harness pi` with five lenses — exposed two properties nobody had measured, because until that run nothing had ever been dispatched through it for real.

DEFECT 1 — INDEPENDENT STAGES RUN SERIALLY. `ps --ppid <runner>` showed exactly ONE `pi` child alive at a time, checked twice several minutes apart. The Claude-Code-native path fans out concurrently; this path does not. That is not a small performance note for this particular workflow: `deep-search`'s read stage is DEFINED by fanning out — five blind readers, each on a different lens, looking at the same ground truth at the same time. Run in series, a five-lens investigation costs five readers' latency instead of one's. Time is the one budget a director cannot buy more of, and a prime rotates on context, not on wall clock, so a slow route silently converts into fewer rounds per generation.

What to build: stages the manifest declares independent are spawned CONCURRENTLY, under a declared cap so a ten-lens run cannot fork bomb the box. The dependency shape is already implicit in `deep-search.json` and should be made explicit rather than guessed — a read stage depends on nothing, a refute stage depends on ITS OWN reader's finding and no other, and synthesize depends on all of them. Give the manifest a way to say that; do not hardcode deep-search's particular shape into the runner.

DEFECT 2 — WORKFLOW SPAWNS TAKE NO LEASE, AND THIS ONE IS A SAFETY DEFECT, NOT AN EFFICIENCY ONE. While the run was live with a `pi` child working, `spawn_budget.py status` showed only an unrelated `--branch` parent and its kid. Workflow-spawned agents are invisible to it. Read HANDOFF.md's round loop to see why that is serious: the stop condition every prime uses, in a background `until` loop, is `spawn_budget.py status` reaching **0 live**. A prime running a workflow is told the box is idle while eleven agents are working. It will open the next round on top of them, or write its handoff and rotate believing nothing is in flight — and a rotation is exactly when "nothing in flight" has to be true. The tree-wide bound in `goal:g4.8` is also simply not enforced for these spawns.

What to build: every workflow-spawned agent takes a `spawn_budget` lease like every other spawner, released on exit, so `status` counts it and the tree-wide bound applies. If a lease per stage-agent is wrong for some reason you discover in the code, say so explicitly and propose the alternative — but "0 live" must never mean "idle" only sometimes.

DEFECT 3 — COSMETIC, ONE LINE. `--dry-run` prints its stage labels with the placeholder unexpanded: `read:{slug}` five times, `refute:{slug}` five times. The fan-out is correct; only the label is wrong, and it makes the dispatch listing useless for telling five lenses apart. Fix where the label is rendered. Do not "fix" it by deleting the placeholder.

PROVE IT. Red-first, both of the real defects: a test asserting that an independent stage produces more than one concurrent child, and a test asserting the live lease count rises for the duration of a run and returns to its starting value after. Then one real `--dry-run` on both harnesses showing distinct, interpolated labels. Paste actual output.

DO NOT change what the existing `review`, `drafting` or `deep-search` manifests MEAN — their stages and prompts are settled and other work depends on them; you are changing how the runner executes them. Do not touch `brief.py` (another parent holds it), `rotate.py`, `cli.py`, `dispatch.py` or `zoom.py`. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window.
