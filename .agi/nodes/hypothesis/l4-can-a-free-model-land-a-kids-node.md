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
status: active
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

## Agent Notes
🔴 FIRST ATTEMPT KILLED AT ~3 MINUTES: IT WAS NOT TESTING WHAT IT WAS MEANT TO TEST, and the reason is a finding that CORRECTS L4.80's engine-surface answer. I widened `harnesses.pi.models.kid` and `harnesses.pi.allowed_models`, dispatched, and then read the kid's actual spawn command out of the manifest rather than trusting the config edit: `--model '~deepseek/deepseek-v4-flash-latest'`. The kid resolved the PAID model.

THE SURFACE IS THE LADDER, NOT THE CONFIG CELL, and the ladder node says so in its own words -- `.agi/nodes/.geometry/ladder.md:81`: *"`dispatch.py` resolves a spawn by row here; config `harnesses.*.models` is the fallback when there is no row."* Row `:37` is `{"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest"}` and it wins. **`harnesses.pi.models` is dead config while a row exists.** L4.80 named `agent_dispatch.model`, the allowlist gate and the seat-row override as the engine surface and MISSED the ladder, which is the primary one -- that is a correction to that round, not a defect in it, and it is recorded here rather than left to be rediscovered.

THE ALLOWLIST HALF WAS RIGHT: the gate judges the RESOLVED pair, so widening `allowed_models` is still required. It is the model cell that was the wrong lever.

🔴 THE REVERT NOW COVERS THREE CELLS, and this note is committed BEFORE the ladder is touched, for the same reason the first two were:
    .agi/config.json  harnesses.pi.models.kid     -> "~deepseek/deepseek-v4-flash-latest"
    .agi/config.json  harnesses.pi.allowed_models -> ["~deepseek/deepseek-v4-flash-latest", "~z-ai/glm-flash-latest"]
    .agi/nodes/.geometry/ladder.md  row tier=0 role=kid  model -> "~deepseek/deepseek-v4-flash-latest"
The ladder edit goes through `write.py`, never by hand. `harnesses.pi.models.parent` and every other ladder row are untouched.

COST OF THE MISTAKE: about $0.005, and it bought the finding. Reading the kid's real spawn command instead of trusting my own config edit is the same discipline as building the 21-arg command to check what lands last -- MECHANISM, NOT WORDING, applied to my own change.

🔴 RESULT: NO — AND IT TOOK UNDER TWO MINUTES. `openrouter/free`, the single best candidate from L4.80's probes (30/30 answered, zero 429, cost 0), returned this to a REAL round:

    404 This model is unavailable for free. The paid version is available now -- use this slug instead: z-ai/glm-4.5-air

**AVAILABILITY IS NOT CAPABILITY, and this is the sharpest possible demonstration of it.** Thirty one-token probes said 100% reliable. One real round says 404. The prime's guard (1) was not caution, it was the difference between a shortlist and a wrong shortlist -- and it is also the meta-route suspicion confirmed from the other side: `openrouter/free` routes to whatever is free at that moment, and for a real request it resolved to a model whose free tier is gone.

MEASUREMENT (a) -- DID THE KID LAND ITS NODE? No. It left a bare SCAFFOLD, `experiment:a00-d0a67d4f-1afd8c`, carrying `model: openrouter/free` and NO verdict and NO confidence -- created at spawn by the scaffold path, never filled. Its whole `output.log` is one line: the 404.

🔴 MEASUREMENT (b) -- WHAT DID THE PARENT DO? THIS IS THE BIGGER FINDING, and it is not the empty-completion path we predicted. It is more basic and less handled. The causal chain, each step observed:
  1. the free model 404s and the kid's pi process DIES immediately;
  2. the kid's `agent.json` still reads `status: running`, `finished_at: null`, `verdict: null` -- and it STILL read that two minutes after the process was confirmed dead;
  3. `cli.py status L4.85` from the parent's own tree reports `a00-d0a67d4f: status=running`;
  4. the parent, whose brief tells it to poll until every kid is `done` or `failed`, polls a dead kid FOREVER. I killed it at ~9 minutes, still at 1.2% CPU.
**NOTHING MARKS A DEAD DETACHED KID TERMINAL.** The parent spawns its kids with `--detach` (its brief says so), which means no reaper phase watches them; the only reaper in play is the dispatcher's, and it watches the PARENT. So a kid that dies without signalling is invisible forever, and its parent cannot terminate by construction.

THAT IS THE THIRD FACE OF THE STALL, and it explains a shape `stall_detect` does not yet see: L4.78 detects a stalled parent whose kids are all TERMINAL; here the kid never becomes terminal, so condition (1) is never satisfied and the detector stays silent on a round that is definitively dead. That is not a defect in L4.78 -- its four conditions describe a different, real shape -- it is a second detector's worth of work, and it is the highest-value thing this round produced.

COST: the whole experiment, including the mis-targeted first attempt, cost about $0.04. It bought a 404 that invalidates the leading free candidate and a fully observed stall chain.

REVERT DONE, gated on terminal as ruled: parent killed, two consecutive clean sweeps by PID, THEN all three cells restored and read back --
    harnesses.pi.models = {'kid': '~deepseek/deepseek-v4-flash-latest', 'parent': '~z-ai/glm-flash-latest'}
    harnesses.pi.allowed_models = ['~deepseek/deepseek-v4-flash-latest', '~z-ai/glm-flash-latest']
    ladder roles tier=0 role=kid model = '~deepseek/deepseek-v4-flash-latest'
8 role rows and 4 tier rows intact; `verify` 8/8. The fail-closed gate is closed again.
