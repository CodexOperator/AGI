---
id: hypothesis:l4-dispatch-model-allowlist
mint_id: 09df6c4430264026bb1484569fb7a425
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: b1a3e8c843e9c0df
season: 2
status: pending
tags:
  - l4
  - g15
  - spend
  - dispatch
  - fail-closed
testable_claim: "`dispatch.py` REFUSES to spawn with an `AGI_MODEL` the config does not allow, fail-closed, so the engine can never be the unexplained line on an OpenRouter bill. 🔴 STATE THE LIMIT HONESTLY IN THE VERDICT: this does NOT explain or stop the `openai/gpt-5.1-codex` spend the owner reported. That spend does not come from this code path -- see the node's THOUGHT for the three candidates already eliminated. This round is defence in depth and instant attribution, and the verdict must say so rather than imply a fix. THE ALLOWLIST IS DATA: add `allowed_models` to each harness in `.agi/config.json`, seeded with EXACTLY the models this project names today and not one more. I enumerated them across `.agi/config.json`, `.agi/nodes/.geometry/seats.md` and `.agi/nodes/.geometry/ladder.md`; there are exactly five and no others: `harnesses.pi.allowed_models` = [`~deepseek/deepseek-v4-flash-latest`, `~z-ai/glm-flash-latest`]; `harnesses.claude-code.allowed_models` = [`claude-sonnet-5`, `claude-opus-5`, `claude-fable-5-1`]. Verify that census yourself before writing it -- if you find a sixth, the census is wrong and the round stops to report it rather than seeding a list that breaks a live seat. THE CHECK SITES, all four, because a check at one is a check that lies: the live spawn env (`dispatch.py:1423-1425`), the dry-run env mirror (`:725-727`), the effective-model resolution after a `--seat` override lands (`:1018-1023`, `:1047-1052`), and the agent record written at `:1348`. A `--seat` override MUST pass the same check -- a seat row is config, not an exemption. FAIL-CLOSED, AND THIS IS THE POINT: an ABSENT or EMPTY `allowed_models` REFUSES EVERY model for that harness. It never means 'allow everything'. A default that opens on absence is a gate that disappears exactly when someone deletes it. THE REFUSAL MESSAGE names the model that was refused, the harness, and the allowed list, and the dry run reports the refusal the SAME way the live path does. PROVED BY: (1) a dispatch with an allowed model still spawns -- show a `--dry-run` env line carrying `AGI_MODEL`; (2) a dispatch whose resolved model is not in the list REFUSES with a non-zero exit and a message naming model, harness and list -- show it; (3) the same refusal through a `--seat` override whose row names a disallowed model, proving a seat row is not an exemption; (4) an EMPTY `allowed_models` refuses, and an ABSENT one refuses -- both tested, because these are the two ways a gate silently turns off; (5) `pytest extensions/agi/tests/test_dispatch_dry_run.py -q` plus whatever file you add, green, NO assertion weakened, removed or retargeted. DISPROVED IF: absent or empty allows anything, a `--seat` override bypasses the check, the dry run and the live path disagree about whether a model is allowed, or the seeded list omits any of the five and breaks a live seat. HARD CEILING: 2 kids. Run `pytest extensions/agi/tests/test_dispatch_dry_run.py -q` and the file you add, NOTHING else -- do NOT run the full suite, and say so. Do NOT touch `.agi/nodes/.geometry/*`. Do NOT change any model any harness or seat uses -- this round adds a gate, it does not re-point anything."
thought_session: sanctuary-director-genII-L4
title: dispatch will spawn with any AGI_MODEL at all, so the engine cannot prove it is not the unexplained line on an OpenRouter bill
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-model-allowlist

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE ROUND IS WORTH RUNNING AND IT IS NOT THE ANSWER TO THE QUESTION THAT PROMPTED IT. The owner reported roughly $12.4 of unexplained `openai/gpt-5.1-codex` spend on OpenRouter over 08-31..09-09. The Prime measured that it is not the engine's; I did not take that on trust and checked independently, and it holds -- `.agi/config.json` and every `bin/*.py` name no such model, and the full census across config, `seats.md` and `ladder.md` is exactly five models, none of them a GPT.

I ALSO ELIMINATED THE TWO OUTSIDE SUSPECTS THE PRIME NAMED, PLUS ONE OF MY OWN, and the negative results are the useful part:
  - The Codex CLI at `~/.codex`: DORMANT. Every file's mtime is April or May 2026, the latest being 2026-05-23. Nothing in the 08-31..09-09 window.
  - My own lead, cavekit's `codex-review.sh` (`ck:judge` / `ck:peer-review-loop` delegate to Codex, and this box's git user is CodexOperator, so it looked promising): it shells out to the `codex` CLI with `--model` defaulting to `o4-mini`, carries no OpenRouter reference at all, and authenticates through `~/.codex/auth.json` -- an OpenAI account, not OpenRouter. Wrong provider AND wrong model.
  - `~/.hermes/belam-codex` and `~/.openclaw/workspace`: mtime 2026-08-15, nothing newer than 09-07 anywhere under `~/.hermes`.
So the spend is on a key that is neither the engine's runtime key nor `agi-2` -- neither of which is anywhere near $12.4 -- and it left no trace in this box's filesystem. That is where the search should continue, and it is the owner's console, not this repo.

WHY FAIL-CLOSED ON ABSENCE IS THE WHOLE DESIGN. The obvious implementation gives `allowed_models` a default of 'anything' when the key is missing, because that cannot break an existing project. It also means the gate vanishes the moment anyone deletes the key, and it vanishes silently -- which is the same failure mode as the spend nobody can account for. Refusing on absence is loud and recoverable; allowing on absence is quiet and is how a gate becomes decoration.

WHY THE SEED LIST IS ENUMERATED IN THE CLAIM RATHER THAN LEFT TO THE KID. A fail-closed allowlist seeded from an incomplete census does not fail loudly in a test -- it fails the next time a seat with an unlisted model tries to dispatch, which could be a seat nobody is watching. I read all three sources myself and there are exactly five models; the kid is asked to re-verify and to STOP and report if it finds a sixth, rather than quietly widen the list to make its own run pass.
<!-- THOUGHT:END -->
