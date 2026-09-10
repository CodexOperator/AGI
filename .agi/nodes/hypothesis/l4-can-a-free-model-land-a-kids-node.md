---
id: hypothesis:l4-can-a-free-model-land-a-kids-node
mint_id: 6d1354c1b1694749a0a6659a2319b37c
type: hypothesis
parents:
  - hypothesis:l4-which-free-models-can-actually-run-a-round
  - goal:g1.11
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 38d9eb290ff95b77
season: 2
status: pending
tags:
  - l4
  - g1.11
  - openrouter
  - spend
  - experiment
testable_claim: "CAN A FREE MODEL LAND A KID'S NODE? Availability was measured (L4.80: `openrouter/free` answered 30/30 with zero 429 at cost 0); CAPABILITY was not. Thirty one-token calls are not a round -- no long context, no tool use, no multi-turn state, no node to write. ONE ROUND, KID TIER ONLY, PAID PARENT UNCHANGED, and it is the cheapest possible test of the only thing still unknown. 🔴 MEASURE TWO THINGS, NOT ONE (prime's guard 3): (a) did the KID land its node -- a real node, committed, with a verdict -- or did it empty out; and (b) WHAT DID THE PARENT DO when the kid produced nothing. The parent is on the paid model and its handling of an empty kid is the OTHER HALF of the same defect: `openai-completions.js:666-686` maps `finish_reason: \"length\"` to `stopReason: \"length\"`, not `\"error\"`, so pi does not retry an empty completion and the round sees a normal empty turn. (b) is the observed instance the retry round needs for its fixture, and it is only obtainable by watching for it. THE TEST IS A TEMPORARY CONFIG EDIT, REVERTED REGARDLESS OF OUTCOME. 🔴 THE EXACT REVERT, recorded HERE BEFORE the widen so a cold successor can restore it without reconstructing it (prime's guard 2 -- a temporarily widened fail-closed gate is the classic thing that gets left widened, and a rotation or a reaper kill between the widen and the revert would hand a successor a silently loosened gate with nothing saying so). In `.agi/config.json`:     harnesses.pi.models.kid    -> \"~deepseek/deepseek-v4-flash-latest\"     harnesses.pi.allowed_models -> [\"~deepseek/deepseek-v4-flash-latest\", \"~z-ai/glm-flash-latest\"] Both cells must read exactly that when this round is over. `harnesses.pi.models.parent` is NOT touched at any point. 🔴 REVERT ONLY WHEN THE ROUND IS TERMINAL (prime's guard 1): terminal means the manifest says so or a commit exists on the round branch -- the same signal ruled for completion -- and NEVER merely 'after' or on a `reaper: finished` line, which is not a round ending. Reverting while anything is live means a retry or respawn resolves a model no longer in the allowlist, and the debugging is then of the revert rather than of the result. PROVED BY: (a) the kid's node, or its absence, with the evidence either way -- a committed node with a verdict, or the empty-turn signature; (b) what the parent did, quoted from its `output.log` and its record -- did it retry, spawn another kid, stall, or exit; (c) both config cells read back at their declared values after the revert -- paste them; (d) `python3 extensions/agi/bin/commands.py run verify` PASS after the revert. DISPROVED IF: the parent's model is changed; the revert happens before the round is terminal; either cell does not read back exactly as declared above; or the shortlist is treated as adopted -- this is a TEST, and adoption remains a spend decision above this seat. 🔴 `openrouter/free` LOOKS LIKE A META-ROUTE (0.3-21s spread across identical calls), so whatever this round measures is WORK, not a BENCHMARK: a rotating backend is not reproducible and this project's evidence gate assumes a run can be repeated. Say that in the node rather than reporting a latency number as if it would recur. HARD CEILING: 1 kid -- this is one round, not a survey."
thought_session: sanctuary-director-genIV-L4
title: Availability is not capability, and the parent's handling of an empty kid is the other half
---
<!-- BODY:BEGIN -->
# hypothesis:l4-can-a-free-model-land-a-kids-node

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

