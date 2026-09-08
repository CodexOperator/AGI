---
id: hypothesis:l3-cli-done-worktree-manifest
mint_id: 82a10dff567545489abb812ce807e9c8
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: de24bb130510b6fa
season: 2
testable_claim: After the change, a parent running inside a --branch worktree completes 'cli.py done --owns <experiment-id>' from its own cwd with no copying and no cd to the main checkout, and the same call from the main checkout for a non-branch agent behaves exactly as it does today; proven by a red-first test for each half, with the node stating explicitly whether iteration session state was made SHARED (main-only, like the spawn budget and comms root) or FORKED (per-worktree, like the graph a kid edits) and why.
thought_session: belam-S1-L3-XI
title: The manifest, agent.json and cli.py's resolver disagree about where a --branch agent's session state lives, so no parent can be right
---
<!-- BODY:BEGIN -->
# hypothesis:l3-cli-done-worktree-manifest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

MEASURED ON THREE OF FOUR PARENTS IN ONE ROUND (L3.38, 2026-09-08), independently, each in its own worktree, none aware of the others. Their own words:
  `a00-e1fc33bf`: "cli.py resolves the session manifest from cwd's `.agi/`; run from worktree it failed (`no manifest`, then `no agent record`) and I had to run `done` from `/home/ubuntu/work/agi` — the dispatch/worktree split costs every parent a turn."
  `a00-e4beee9f`: "cli.py done rejected the parent's agent record in the worktree session dir and had to be run from the main repo root".
  `a00-75ccbeaa`: "my own `agent.json` was written to the main repo's session dir, not the worktree `cli.py` resolves — `done` failed until I copied the record into the worktree path."

READ THOSE THREE TOGETHER, BECAUSE THEY DISAGREE AND THE DISAGREEMENT IS THE BUG. Two parents had to run `done` from the MAIN checkout because the record was there; one had to copy the record INTO the worktree because `cli.py` was looking there. That is not one consistent rule being violated, it is two halves of the system disagreeing about where a `--branch` agent's session state lives, so a parent cannot be right by following any rule at all. The manifest, the per-agent `agent.json` and `cli.py`'s resolver must agree on ONE location.

THIS IS THE SAME CLASS OF DEFECT THE ROUND BEFORE IT FIXED, and that is the strongest argument for fixing it properly rather than patching a symptom. L3.37 found that `--branch` isolation broke because `pi_adapter.restart()` and `heal.py` derived a cwd from the main checkout while the spawn derived it from the worktree — two derivations of one thing, disagreeing, on a path only some agents reach. This is that same shape in the session-state layer. The project already has the right primitive for it: `locations.shared_project_root` climbs to the main checkout through `git_common_root` and is the identity outside a worktree, and it is already what the spawn budget, the comms root, the meter pins and `.env` resolve through. **The question this brief must answer explicitly, and state its reasoning for, is whether iteration session state is SHARED (main-only, like the budget and the comms root) or FORKED (per-worktree, like the graph a kid edits).** Pick one, make every reader agree with it, and write the reason into the node — a future reader needs the reason more than the diff.

PROOF CONDITION: red-first tests that a parent running inside a `--branch` worktree can complete `cli.py done --owns <experiment-id>` from ITS OWN cwd, with no copying and no `cd` to the main checkout, and that the same call from the main checkout for a non-branch agent behaves exactly as it does today. Then say plainly in the node whether the choice was shared or forked and why.

COST, so the priority is legible: one wasted turn per parent per round, on the sanctioned completion path, paid by every `--branch` parent forever. `--branch` is the mechanism the whole seat plan rests on, so this tax scales with everything wave 4 is trying to build.

DO NOT: touch `.agi/nodes/.geometry/seats.md`; start or populate any seat (owner gate, HANDOFF §6 item 47); or change what `--branch` does to the code worktree.

HARNESS CONSTRAINT FOR THIS ROUND (Belam XI, 2026-09-08, operational — not part of the claim). The `.env` OpenRouter runtime key is at its cap, so `dispatch.py` refuses every pi spawn with `ERR: runtime key ... below the configured floor`. Spawn your kid on the subscription:

    python3 extensions/agi/bin/dispatch.py . L3.42 --target <this node> --level small --tier kid --harness claude-code

Measured this session: `--harness claude-code` on the PARENT invocation does NOT reach the kid — the parent's own dispatch call falls back to the ladder row's pi harness and is refused. Pass the flag explicitly. Do NOT raise the key limit or edit `.env`; that is the owner's decision and it is banked. Do NOT do the kid's work yourself because the spawn was refused — report `pending` and say so, as two parents correctly did earlier this session.

YOU HOLD A BRANCH. You were dispatched with `--branch`, so you are working in your own git worktree on your own `loop/...@s2` branch, cut from the spawner's tip. Commit your kid's work there — a `--branch` parent that lands nothing leaves `merge-up` merging an empty branch and reporting green, which is exactly the defect fixed at L3.40 and never yet exercised live. You are the live proof of that fix. Do not push, do not merge, do not touch `season/s2`; the director merges.

HARNESS CORRECTION — SUPERSEDES THE claude-code CONSTRAINT NOTE ABOVE (Belam XI, 2026-09-08). Owner instruction, verbatim: "Use openrouter" / "Subscription will get drained". The runtime key cap was raised to $15 (usage $5.02, headroom ~$9.98) and pi spawns resolve again. **Run on pi/OpenRouter, not on the subscription.** Your kid:

    python3 extensions/agi/bin/dispatch.py . L3.42 --target <this node> --level small --tier kid --harness pi

Ignore the earlier paragraph telling you to pass `--harness claude-code`; it was written while the key was at its cap and is no longer true. `dispatch.py` resolves the correct cheap OpenRouter slugs by itself (`~z-ai/glm-flash-latest` parent, `~deepseek/deepseek-v4-flash-latest` kid) — that path was never the leaky one.

DO NOT run `workflow.py run` on the pi harness in this round for any reason. The fail-closed model guard that makes it safe landed minutes ago and is not yet merged into your branch. A workflow run before that guard is what burned an entire monthly key cap on `anthropic/claude-sonnet-4.6` (`hypothesis:l3-workflow-model-crosses-harness-namespace`). Rounds are cheap; workflows currently are not.

The BRANCH paragraph above still applies in full: you hold a worktree, commit your kid's work to your own `loop/...@s2` branch, never push, never touch `season/s2`.
