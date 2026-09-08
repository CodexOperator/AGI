---
id: hypothesis:l3-pi-context-never-delivered
mint_id: da74b7b717b94b5497d9700e619a532c
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: e9cc38b4afbdf659
season: 2
testable_claim=pi: "resolves a --append-system-prompt argument with resolvePromptInput, which is existsSync(input) ? readFileSync(input) : input, so a bare path loads the file and an @-prefixed path fails the stat and is appended as literal text; therefore pi_adapter passing @{context_file} and @{skill_prompt} delivered a pathname instead of the context to every pi agent, and removing the two prefixes delivers the file. Proven by a red-first test asserting no --append-system-prompt argument carries an @ and that the bare path appears, red before the change and green after, plus a direct existsSync measurement showing 79 bytes of pathname where the real context.md was 16654 bytes"
thought_session: belam-S1-L3-XI
title: "Every pi agent ever spawned ran without its rendered graph context: an @ prefix on --append-system-prompt made pi append the path string instead of the file"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-pi-context-never-delivered

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FOUND AND FIXED BY THE PRIME, 2026-09-08, under the standing one-line-unblocks-dispatch exception. The two-character fix is landed; this node exists for the CLASS, not the character.

HOW IT WAS FOUND, because the route matters. It was not found by looking for it. A deep-search workflow was dispatched at the owner's prompting to explain a completely different phenomenon — why a --branch kid writes source into the main checkout. One of its five readers, working the adapter lens, refuted the specific claim it was handed and then volunteered this instead, unasked, labelled "BONUS FINDING (bigger than the claim)". The lens that found it was the lens that had just been told it was wrong.

THE DEFECT. `extensions/agi/bin/adapters/pi_adapter.py` passed the rendered zoom context as `--append-system-prompt @{context_file}` and the skill prompt as `@{skill_prompt}`. pi resolves that argument through `resolvePromptInput()` in `dist/core/resource-loader.js`, which is exactly `if (existsSync(input)) return readFileSync(input); return input;`. There is no `@` spelling in that path at all — the `@` handling in pi's argument parser (`dist/cli/args.js:152`) is for POSITIONAL attachments, a different flag entirely. So `existsSync("@/abs/path/context.md")` is false, the function falls through, and pi appends the PATH STRING to the system prompt as literal text.

MEASURED, not inferred. A real kid's `context.md` from this very round is 16654 bytes. The string pi received in its place is 79 bytes. `existsSync(bare path)` is true and `existsSync("@" + path)` is false, checked directly against the same file.

WHAT THAT MEANS, stated plainly because it is easy to under-read. Every pi agent this project has ever spawned — every kid, every parent, every healer — ran WITHOUT its rendered graph context and without its skill prompt. What did arrive was the brief, because brief segments are passed inline as text on the adjacent line and were never affected. So agents got their instructions and not their map. They have been working blind and reporting struggles that were partly this, and nobody could see it because the failure is silent in the direction of looking fine: the flag was present, the path was correct, the file existed, the command ran, the agent produced work.

IT RETROACTIVELY RE-READS A FIELD NOTE THE PROJECT HAS TRUSTED SINCE L1. `skills/agi/SKILL.md` records: "Embed the map, don't reference it. Kids dropped from 11-13 tool calls to 5-7 when the rendered map was pasted into the spawn prompt." That observation is real and the inference drawn from it was wrong. Pasting the map worked not because embedding beats referencing as a matter of agent psychology, but because REFERENCING NEVER DELIVERED ANYTHING. The note should be corrected rather than deleted — the measurement stands, the explanation does not.

WHAT IS ACTUALLY LEFT TO DO, and why this is a class and not a character.
1. **The whole zoom pipeline is now unverified in the direction that matters.** Nothing ever asserted that a spawned agent RECEIVED its context, only that the file was written and the flag was passed. Build the assertion: a test, or better a runtime check, that the context actually reaches the model. Ask what the cheapest honest signal is — an echo marker planted in the rendered context that the agent is asked to quote back once, a byte count in the session record, something.
2. **Audit every other `@` spelling and every other file-vs-text argument in both adapters.** `claude_code_adapter.py` has its own conventions; do not assume they match. Any place the engine hands a harness a PATH and hopes it is read is the same hazard.
3. **The general shape, which is the reason this node is under g15 rather than closed:** the engine passes arguments to third-party binaries whose parsing it does not test against. Two harnesses, several flags, no contract test anywhere. Propose the smallest thing that would have caught this on the day it was written.
4. **Re-read `struggles:` lines across past rounds with this in hand.** Kids repeatedly reported orienting difficulty, re-reading files, and needing more tool calls than expected. Some of that was this. Do not over-claim it — say what the evidence supports.

DO NOT re-do the fix; it is landed with a red-first test in `test_brief.py` (`test_pi_gets_the_context_file_as_a_bare_path_not_an_at_prefix`), verified red before and green after, full suite 2084 passed 1 skipped. Do not edit `workflow.py`, `rotate.py`, `cli.py`, `dispatch.py` or `zoom.py` — other agents hold those. Do not write `.agi/nodes/.geometry/seats.md`. Do not kill any `belam-*` tmux window.

HARNESS CONSTRAINT FOR THIS ROUND (Belam XI, 2026-09-08, operational — not part of the claim). The `.env` OpenRouter runtime key is at its cap, so `dispatch.py` refuses every pi spawn with `ERR: runtime key ... below the configured floor`. Spawn your kid on the subscription:

    python3 extensions/agi/bin/dispatch.py . L3.42 --target <this node> --level small --tier kid --harness claude-code

Measured this session: `--harness claude-code` on the PARENT invocation does NOT reach the kid — the parent's own dispatch call falls back to the ladder row's pi harness and is refused. Pass the flag explicitly. Do NOT raise the key limit or edit `.env`; that is the owner's decision and it is banked. Do NOT do the kid's work yourself because the spawn was refused — report `pending` and say so, as two parents correctly did earlier this session.

YOU HOLD A BRANCH. You were dispatched with `--branch`, so you are working in your own git worktree on your own `loop/...@s2` branch, cut from the spawner's tip. Commit your kid's work there — a `--branch` parent that lands nothing leaves `merge-up` merging an empty branch and reporting green, which is exactly the defect fixed at L3.40 and never yet exercised live. You are the live proof of that fix. Do not push, do not merge, do not touch `season/s2`; the director merges.

HARNESS CORRECTION — SUPERSEDES THE claude-code CONSTRAINT NOTE ABOVE (Belam XI, 2026-09-08). Owner instruction, verbatim: "Use openrouter" / "Subscription will get drained". The runtime key cap was raised to $15 (usage $5.02, headroom ~$9.98) and pi spawns resolve again. **Run on pi/OpenRouter, not on the subscription.** Your kid:

    python3 extensions/agi/bin/dispatch.py . L3.42 --target <this node> --level small --tier kid --harness pi

Ignore the earlier paragraph telling you to pass `--harness claude-code`; it was written while the key was at its cap and is no longer true. `dispatch.py` resolves the correct cheap OpenRouter slugs by itself (`~z-ai/glm-flash-latest` parent, `~deepseek/deepseek-v4-flash-latest` kid) — that path was never the leaky one.

DO NOT run `workflow.py run` on the pi harness in this round for any reason. The fail-closed model guard that makes it safe landed minutes ago and is not yet merged into your branch. A workflow run before that guard is what burned an entire monthly key cap on `anthropic/claude-sonnet-4.6` (`hypothesis:l3-workflow-model-crosses-harness-namespace`). Rounds are cheap; workflows currently are not.

The BRANCH paragraph above still applies in full: you hold a worktree, commit your kid's work to your own `loop/...@s2` branch, never push, never touch `season/s2`.
