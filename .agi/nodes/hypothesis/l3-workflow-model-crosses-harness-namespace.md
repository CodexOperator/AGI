---
id: hypothesis:l3-workflow-model-crosses-harness-namespace
mint_id: a88bd3f815724d87b8f7f5aeefff320c
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: e7ad6b68845087ed
season: 2
testable_claim: "After the change, no workflow stage can spawn a pi child whose --model is outside the provider's namespace: the pi harness resolves its model from harnesses.pi.models (or an explicit per-harness key) rather than from the harness-agnostic workflows.<name>.model, and a model the provider cannot own is a loud refusal before any network call, proven red-first."
thought_session: belam-S1-L3-XI
title: workflow.py hands a Claude Code model alias to --provider openrouter, so every pi-harness workflow stage silently bills Anthropic Sonnet at 33x the loop's declared model
---
<!-- BODY:BEGIN -->
# hypothesis:l3-workflow-model-crosses-harness-namespace

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done.

FOUND BY THE OWNER LOOKING AT A BILL, 2026-09-08: "I'm seeing sonnet4.6 use on my openrouter key doesn't make sense needs to be investigated before it drains the account". It was real, it was this, and it is measured below. Nothing about this was found by reading the code — the code reads fine.

THE DEFECT, IN ONE LINE. `extensions/agi/bin/workflow.py` `_run_stage_pi` builds:
    pi -p --provider <harnesses.pi.provider> --model <workflows.NAME.model> --thinking T
`harnesses.pi.provider` is `openrouter`. `workflows.review.model`, `workflows.deep-search.model` and `workflows.drafting.model` are all the string `sonnet`, and `workflow.py:56` sets `_DEFAULT_MODEL = "sonnet"` as the fallback. `sonnet` is a CLAUDE CODE SUBSCRIPTION alias. Handed to OpenRouter it resolves to `anthropic/claude-sonnet-4.6`.

THE PRICE, read live from `https://openrouter.ai/api/v1/models` on 2026-09-08:
    anthropic/claude-sonnet-4.6    $3.00 / $15.00 per Mtok  (prompt / completion)
    deepseek/deepseek-v4-flash     $0.09 /  $0.18
    z-ai/glm-5.3-flash             $0.07 /  $0.25
33x the prompt price, 60-83x the completion price, against the models this project actually declares.

THE PART THAT MAKES IT A DESIGN DEFECT AND NOT A TYPO. `.agi/config.json` ALREADY declares the correct slugs, in the same file, one block away: `harnesses.pi.models` = `{kid: ~deepseek/deepseek-v4-flash-latest, parent: ~z-ai/glm-flash-latest}`. `_pi_harness_cfg` reads `bin`, `provider` and `thinking` out of that block and never reads `models`. The one place the right models are written is the one place this code path ignores. Meanwhile `workflows.NAME.model` is a SINGLE field read by TWO harnesses whose model namespaces are disjoint — `sonnet` is correct for `provider: claude-code` (drafting) and catastrophic for `provider: pi`. One field cannot mean both.

EVIDENCE ON DISK, not inference. Belam X's scratchpad holds the actual spawn line from the first live deep-search run:
    /home/ubuntu/.npm-global/bin/pi -p --provider openrouter --model sonnet --thinking high ...
`--thinking high` is `workflows.deep-search.effort: high` through `_effort_to_thinking`, which identifies the run.

WHAT IT COST, measured from the OpenRouter API the same day. The `.env` key (label `backup`, created 2026-09-08T00:18) reads `limit: 5`, `usage: 5.016`, `limit_remaining: 0` — it burned its entire monthly cap in that one run and now returns 402 on everything. The `/api/v1/activity` feed shows ZERO anthropic rows on every day it covers through 2026-09-07; all prior spend in this project's life is qwen, deepseek, glm and codex. So this had never happened before, and the only thing that stopped it was a $5 cap that the owner had set for an unrelated reason.

WHAT TO BUILD.
1. Per-harness model resolution. The pi path must resolve its model from the pi harness's own declaration, not from the harness-agnostic `workflows.NAME.model`. Decide the shape yourself and say why: reading `harnesses.pi.models` by stage role is the obvious candidate; an explicit `model_pi` / `model_claude_code` pair on the workflow row is another. `--args {model: ...}` must keep overriding, because that is how a human deliberately asks for an expensive model.
2. FAIL CLOSED. A model string the target provider cannot own must be a loud refusal BEFORE the network call, naming both the model and the provider. Silent spend is the whole defect; a wrong model that errors costs nothing and a wrong model that runs costs the account. This guard is worth more than item 1 and outlives it.
3. `_DEFAULT_MODEL = "sonnet"` at line 56 is the same bug wearing a default's clothes. Remove the cross-namespace default. There should be no fallback that spends money on a name nobody chose.
4. Repair `.agi/config.json` so the three workflow rows say what each harness should spend. Do not change what any manifest MEANS — stages and prompts are settled and other work depends on them.

PROVE IT, RED FIRST. A test that resolves the pi model for `review` and `deep-search` and asserts it is an OpenRouter slug, verified red by stashing the fix. A test that the guard refuses `sonnet` under `provider: openrouter` and does not spawn. A test that an explicit `--args` model override still wins. Then one real `workflow.py run <name> --harness pi --dry-run` with the resolved command pasted into your node, showing the model that would now be spent. Paste actual output, not a description of it.

DO NOT run a live paid workflow to check your work — the `.env` key is at its cap and every call 402s, and raising it is the owner's decision, not yours. `--dry-run` is your gate.

DO NOT touch `dispatch.py`, `brief.py`, `rotate.py`, `cli.py` or `zoom.py`. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window. The serial-execution and missing-lease defects in the same file belong to `hypothesis:l3-workflow-run-serial-and-unleased` and are NOT yours — if you touch them you collide with a future round.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by Belam XI within twenty minutes of the owner reporting an unexplained Sonnet 4.6 charge. Split out of l3-workflow-run-serial-and-unleased deliberately: that brief owns how the route EXECUTES stages (serial, unleased) and this one owns what the route SPENDS. They collide on workflow.py so they can never share a round, and this half is the one with a dollar figure on it, so it goes first. The narrower framing is also the honest one — the cost defect is not a symptom of the serial defect, it is an independent namespace error that would survive a perfect fix to the other.
<!-- THOUGHT:END -->

HARNESS CONSTRAINT FOR THIS ROUND (Belam XI, 2026-09-08, operational — not part of the claim). The `.env` OpenRouter runtime key is at its cap (`remaining $-0.02`, floor $1.00), so `dispatch.py` refuses every pi spawn with `ERR: runtime key ... below the configured floor`. Spawn your kid on the subscription instead:

    python3 extensions/agi/bin/dispatch.py . L3.41 --target <this node> --level small --tier kid --harness claude-code

Measured: `--harness claude-code` on the PARENT invocation does not reach the kid — the parent's own `dispatch.py` call falls back to the ladder row (pi) and hits the key floor. Pass the flag explicitly on the kid dispatch. Do NOT raise the key limit or edit `.env` to get around this; that is the owner's decision and it is banked. Do NOT treat the blocked spawn as a reason to do the kid's work yourself.

OWNER DECISION, 2026-09-08, verbatim as received (voice transcription, lightly noted where a word is clearly a homophone): "I'm fine deep search being Claude and review I just want it to work the other way as well. When using The sonic [Sonnet] subscription model or the Opus subscription model, I wanted to show up the same way all the workflows show up and call code interactively. And then if I use the black [pi] harness, I still wanted to show up and look the same as the workflow does in Claude code if at all possible. I'm fine using the weaker models on open router or honestly just sawn it [Sonnet] on the review. And then using Opus high on the research one."

WHAT THIS SETTLES FOR THIS NODE. The banked question (cheap slugs vs premium vs subscription) is answered and it is NOT "pick one": BOTH directions must work. The per-harness resolution this brief asks for is exactly the mechanism the owner is describing, so build it as specified. What changes is only the VALUES, and the director sets those at review time, not you:

  review       -> weak OpenRouter models are fine, or Sonnet. Owner is explicitly relaxed here.
  deep-search  -> Opus at HIGH effort. This is the research loop and the owner wants it strong.
  drafting     -> unchanged.

So do NOT "fix" the cost defect by making everything cheap. The defect is that a model name crosses a namespace silently, not that a model is expensive. An expensive model chosen deliberately, per harness, is the correct outcome; an expensive model arrived at by accident is the bug. Your fail-closed guard must let a deliberate premium choice through and refuse only a model the target provider cannot own.

The owner's other half - that a workflow should PRESENT identically on both harnesses - is a separate build and is NOT yours: it is minted as `hypothesis:l3-workflow-surface-identical-across-harnesses`. Do not attempt it here.
