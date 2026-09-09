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

THE LIVE RUN FAILED, AND THE FAILURE UNIFIES ALL OF IT INTO ONE DEFECT. Appended by belam-S1-L3-X after `workflow.py run deep-search --harness pi` was actually executed against the owner's grid question.

It died at the FIRST read stage:

    workflow.py: stage read:{slug} pi exited rc=1
     402 This request requires more credits, or fewer max_tokens. You requested up
     to 32000 tokens, but can only afford 26055. ... adjust the key's monthly limit
    workflow.py: workflow=deep-search failed at stage read:{slug} (rc=3)

And the resolved command it printed shows the second half:

    /home/ubuntu/.npm-global/bin/pi -p --provider openrouter --model sonnet --thinking high ...

TWO MORE CONSEQUENCES, AND THEY ARE NOT SEPARATE BUGS. Everything in this node has ONE cause: **`workflow.py` spawns pi directly instead of going through `dispatch.py`.** Every capability that lives in dispatch is therefore absent, and they are absent all at once:
- no spawn_budget lease, so `status` reports an idle box (defect 2 above);
- no concurrency, because dispatch's fan-out is where that lives (defect 1 above);
- **no per-spawn key.** `provisioning.py` mints a fresh $5/60-min OpenRouter key for each dispatched agent, which is precisely why ordinary `--branch` rounds keep running. A workflow spawn skips that and falls back to the `.env` `OPENROUTER_API_KEY` — the RUNTIME FALLBACK key, deliberately capped at $5/month since the owner rotated it (§6 item 45). Measured immediately after the failure: that key read `usage: 4.809` of `limit: 5`, `limit_remaining: 0.19`. The workflow route burned the fallback key's entire monthly cap and then 402'd, while `dispatch.py` rounds continued untouched on minted keys. **The capped fallback key is doing exactly its job here — it converted an unbounded spend into a bounded one and then stopped. The defect is that the workflow route is reaching for it at all.**
- **the model hint is never resolved for pi.** `--model sonnet` was handed to `--provider openrouter` verbatim. `sonnet` is not an OpenRouter slug; the pi harness's real rows are `~z-ai/glm-flash-latest` and `~deepseek/deepseek-v4-flash-latest`, resolved by `dispatch.py` from `.agi/config.json harnesses.pi.models[tier]`. So even with unlimited credit this stage would have been asking for a model that does not exist on that provider. A `model_hint` is a HINT and something has to resolve it per harness; nothing does.

WHAT THIS CHANGES ABOUT THE FIX. Do not patch four things. Route workflow stage spawns through `dispatch.py` the way every other spawn in this project goes, and the lease, the concurrency, the minted key and the model resolution all arrive together because that is what dispatch already does. If there is a genuine reason a workflow stage cannot be a dispatched agent, state it explicitly with file:line and propose the narrowest alternative — but the default answer is the one this project keeps arriving at: one route, no second path that happens to also work.

HONEST SCOPE NOTE FOR WHOEVER TAKES THIS. The `--dry-run` path is genuinely correct and was verified on both harnesses by two independent agents; nothing here demotes `experiment:a00-33c42478-0c0721`, whose brief asked for exactly what it delivered. What failed is the live execution path underneath it, which no brief had ever asked anyone to exercise. That is the whole reason the owner's instruction to actually USE it was worth more than another review of it.
