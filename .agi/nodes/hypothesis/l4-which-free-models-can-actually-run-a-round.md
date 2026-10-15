---
id: hypothesis:l4-which-free-models-can-actually-run-a-round
mint_id: c6524117e20a4b4fa81605e82bdba166
type: hypothesis
parents:
  - hypothesis:l4-the-floor-must-watch-the-account
  - goal:g1.11
next_edges: []
edited_by: sanctuary-director
scaffold_hash: afdb0f428e964a52
season: 2
status: pending
tags:
  - l4
  - g1.11
  - openrouter
  - spend
  - owner-order
testable_claim: "WHICH FREE OPENROUTER MODELS CAN ACTUALLY RUN A ROUND, AND WHAT HAPPENS WHEN ONE REFUSES MID-ROUND. OWNER ORDER, verbatim: *\"several models on Open Router offer free use... The problem is a little bit that the training data can be used and all of that, but I'm not as worried about it right now because each parent gets such a small slice of the whole. So if you want to explore and run some experiments dispatch, some kids or some parents yourself to a helper or the director to run some tests to see what free keys are available or what free models are available and what their rate limits are because they are rate limited, but there are several free models available.\"* 🔴 THE TRAINING-DATA EXPOSURE IS THE OWNER'S CALL AND HE HAS MADE IT. Do not re-litigate it, do not weigh it, do not add a caveat recommending against. WHY IT IS URGENT: the account is at **$3.59 of $92**, about 39 rounds at the measured $0.092. SIX PARTS, and (4) is the one that decides everything. (1) ENUMERATE FROM AUTHORITY, NOT MEMORY: `GET https://openrouter.ai/api/v1/models`, filter `pricing.prompt == \"0\" AND pricing.completion == \"0\"`. A name merely ending in `:free` is a GUESS -- do not shortlist on the suffix. Report the count and the filter you ran. (2) REACHABLE WITH OUR KEY: one MINIMAL probe per candidate (one token out), recording the HTTP STATUS and the error body if any -- a status, never an impression. Use the runtime key; mint nothing. (3) LIMITS TWICE: as REPORTED -- any `X-RateLimit-*` headers and any documented per-minute/per-day cap -- and as EXPERIENCED -- probe until 429 and record the count reached and the reset signalled. 🔴 MEASURE WHETHER THE FREE DAILY ALLOWANCE DEPENDS ON THE ACCOUNT CREDIT BALANCE, and do not assume either way; ours is $3.59 and falling, so the answer changes what the shortlist is worth. (4) 429 END TO END, THE HALF THAT DECIDES: what does a pi PARENT DO when the model refuses mid-round? Retry? Die silently? Spin? MEASURED, and this is the arithmetic: a failed round costs **$0.2156** against **$0.0977 / $0.0749 / $0.0911** for rounds that produced -- **a free model that dies mid-round is more expensive than a paid one that finishes.** If you cannot test this without spending, say so and say what it would take. (5) THE ENGINE SURFACE, name the exact cells: `agent_dispatch.model` in `.agi/config.json`; the allowlist gate at `dispatch.py:1096` which judges the RESOLVED pair; and the seat-row override that beat `--harness` before (L4.39). Say what changes and what does not. (6) DELIVERABLE: a RANKED SHORTLIST for PARENT tier and for KID tier SEPARATELY -- they are different jobs and a model that reviews well may not drive a loop -- with measured limits and the exact config diff, NOT applied. 🔴 CHANGE NO CONFIG AND SWITCH NO MODEL. This round reports; adopting a free model is a spend decision above it. NAME THE CONVERGENCE in your node: a weaker free model raises stall probability, which is exactly what `stall_detect.py` now records (L4.78) and what the parent's closing-line self-check mitigates (L4.77) -- the safety net landed one merge-up before it is needed. PROVED BY: (a) the enumeration command and its result count; (b) a status per candidate from a real probe; (c) both limit readings, reported and experienced, with the 429 evidence; (d) a plain answer on the credit-balance dependence, or an explicit \"could not determine and here is why\"; (e) the 429 mid-round behaviour, or what testing it would cost; (f) the two ranked shortlists and the unapplied config diff. DISPROVED IF: a model is shortlisted on its NAME rather than its pricing fields; any config or model is changed; a key is minted; the owner's decision on training data is re-argued; or a limit is reported without a measurement behind it. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: commit as soon as your work is reviewable. A parent that spawns no kid within ~15 minutes, or idles at ~0.4% CPU with work staged, gets killed by the director watching -- and this round is about the models most likely to cause exactly that."
thought_session: sanctuary-director-genIV-L4
title: A free model that dies mid-round costs more than a paid one that finishes
---
<!-- BODY:BEGIN -->
# hypothesis:l4-which-free-models-can-actually-run-a-round

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
AN OWNER ORDER, and it outranks the queue I was on -- I had just minted `hypothesis:l4-the-mode-is-declared-not-remembered` (plan L4.26) and left it undispatched to take this. It stays minted as a candidate; nothing is lost by pausing it.

THE FIRST THING I DID WAS DECIDE NOT TO ARGUE. The owner weighed the training-data exposure out loud -- "each parent gets such a small slice of the whole" -- and accepted it. A round that returns a shortlist with a caveat recommending against would be re-litigating a decision already made, so the brief forbids it by name rather than trusting that a kid will not helpfully add one.

PART (4) IS THE ROUND AND THE REST IS PREPARATION, which is only obvious because of numbers this seat measured today. A failed round costs $0.2156; rounds that produced cost $0.0977, $0.0749 and $0.0911. **A free model that dies mid-round is more expensive than a paid model that finishes.** So the interesting question is not which models are free -- that is a filter on two JSON fields -- but what a pi parent DOES when the model refuses at token N of a review. Without this morning's instrument that sentence would have been a plausible worry; with it, it is arithmetic, and the brief leads with it.

I ALSO FORBADE THE SHORTCUT THE TASK INVITES: shortlisting on a `:free` suffix. That is a guess dressed as a filter, and the authority is `pricing.prompt` and `pricing.completion` on the models endpoint. Same class as everything else that has gone wrong today -- a name someone typed standing in for a fact a machine can check.

THE CONVERGENCE IS WORTH SAYING OUT LOUD AND THE BRIEF ASKS FOR IT IN THE NODE: a weaker free model raises stall probability, which is precisely what `stall_detect.py` began recording one merge-up ago (L4.78) and what the parent's closing-line self-check mitigates (L4.77). The safety net landed the morning before the change that needs it. That was not planning; it was the seam pulling in one direction all day. But it does mean this round can be run with a detector watching, which it could not have been yesterday.

Split as the prime allowed: the helper has the two engineering gaps -- the SUITE REQUIRED check and stall-BEFORE-work as its own state -- and I have the owner order. That is the right division, not just the fast one: the owner asked me.
<!-- THOUGHT:END -->

## Agent Notes
PART (1) MEASURED BY THE DIRECTOR BEFORE THE ROUND COULD SPEND A KID ON IT, and delivered to the live parent's inbox. `GET https://openrouter.ai/api/v1/models`, filtered on `pricing.prompt == "0" AND pricing.completion == "0"`, 2026-09-10:

    436 models total · 21 free by pricing fields · 18 ids ending `:free`
    3 free models do NOT end in `:free`: google/lyria-3-pro-preview, google/lyria-3-clip-preview, openrouter/free
    0 ids end in `:free` without being free by pricing

SO THE SUFFIX HEURISTIC HAS NO FALSE POSITIVES AND MISSES 14% -- three of twenty-one. The brief forbade shortlisting on the name before I ran this; the number is now the reason rather than the principle. `openrouter/free` (ctx 200000) is the sharpest case: a generic free endpoint that a suffix filter hides completely.

All 21 declare text output, so modality does not narrow the field -- but 'free' is not 'usable' and the shortlist must say why, not just list: `nvidia/nemotron-3.5-content-safety:free` is a safety classifier, the two `lyria` entries are music models that happen to emit text, and `cohere/north-mini-code:free` is code-shaped. By context length the field is `thinkingmachines/inkling:free` and `inkling-small:free` at 1048576, `nvidia/nemotron-3-ultra-550b-a55b:free` and `nemotron-3.5-lightning:free` at 1000000, `dots-studio/dots-3-note-preview:free` at 512000, then a band of eight at 262144.

The round's kids are now free to spend themselves on parts (2), (3) and (4) -- reachability with our key, the two limit readings, and what a pi parent DOES when the model refuses mid-round. That last one is the only part whose answer I cannot get from a JSON endpoint, and it is the part the arithmetic turns on.

BATCHING FOLDED INTO THIS ROUND (owner, part 2 of the same direction), and question one is ANSWERED FROM AUTHORITY -- measured by the director with our own authenticated key, 2026-09-10:

    GET /api/v1/batches -> 404, body is a Next.js HTML error page
    GET /api/v1/batch   -> 404, same HTML
    GET /api/v1/files   -> 200 {"_shape":"openrouter","data":[],"has_more":false,...}
    GET /api/v1/key     -> 200

AUTHENTICATION IS NOT THE CONFOUNDER, and that is what makes this conclusive rather than a guess: the SAME key gets a real 200 API response on `/files` and an HTML 404 on `/batches`. An unauthenticated probe would have proved nothing. **OpenRouter exposes no batch route at the OpenAI-compatible path.** One nuance worth carrying rather than dropping: `/files` DOES exist, and a files endpoint is normally the INPUT side of a batch API -- so they may be building toward one, but there is nothing to call today.

CONSEQUENCE, stated rather than designed around: capturing a 50% batch discount means going DIRECT to a provider that runs its own Batch API, i.e. a NEW CREDENTIAL ON A DIFFERENT ACCOUNT. That is an owner spend decision, banked, and not the round's to take.

THE DESIGN POINT, which sharpens the owner's reading rather than agreeing with it. He is right that our workflow is asynchronous and latency is rarely the constraint -- but we have TWO classes of work and batching pays in only one. The ROUND CHAIN is narrow and DEPENDENT: merge-ups land every twenty-odd minutes and each round's result shapes the next brief, so a 24-hour turnaround does not fit it at any discount. The WIDE WORK is independent and is where half rate is nearly free money -- per-node analyses across 1,963 nodes, the schema sweep across 18 types of which exactly one declares `written_by`, the envelope-debris sweep done by hand at every merge-up, the L4.05 roles report, any classifier over the verdict corpus. Hundreds of identical independent calls, no ordering constraint. So the recommendation is not *batch the loop*, it is **BATCH THE SWEEPS**.

AND IT IS A CHOICE, NOT A PLAN: free and batched are probably mutually exclusive, because a free model has no price to halve. Both arms get numbers so the owner picks against arithmetic.

🔴 CAVEAT THE ROUND DID NOT RAISE AND NOBODY SHOULD BENCHMARK WITHOUT (prime, 2026-09-10): **`openrouter/free` looks like a META-ROUTE**, and the 0.3-to-21-second latency spread measured across 30 identical one-token calls is the most likely evidence of it -- a rotating backend, not a single model with variable load. **A rotating backend is NOT REPRODUCIBLE.** Use it for WORK; never for MEASUREMENT. An experiment whose numbers came off a rotating backend cannot be re-run, and this project's evidence gate assumes a run can be repeated -- so a benchmark on `openrouter/free` would produce `evidence_runs` that certify nothing, which is worse than no benchmark because it looks like one.

🔴 AND THE ROUND MEASURED AVAILABILITY, NOT CAPABILITY. Thirty rapid one-shot calls with `max_tokens: 1` are not a round: no long context, no tool use, no multi-turn state, no node to write. The shortlist stays UNAPPLIED until one real round runs `openrouter/free` at KID TIER ONLY with the paid parent unchanged, and reports whether the kid LANDED ITS NODE or emptied out. That is the cheapest possible test of the only thing still unknown, and it costs one kid slot.

THE `/files` NUANCE IS A RE-PROBE, NOT A CONCLUSION. `/api/v1/files` returning 200 while `/api/v1/batches` returns an HTML 404 says OpenRouter has the input half of a batch API and not the batch half. That is a snapshot of one afternoon. Re-probe it at each season rollover rather than treating 'no batch route' as permanent.

🔴 CORRECTION TO PART (5), THE ENGINE SURFACE — written here in place, where the next reader will look, on the prime's ruling that an answer wrong about the PRIMARY surface is worse than an incomplete one. This round named `agent_dispatch.model`, the allowlist gate at `dispatch.py:1096`, and the seat-row override. **IT MISSED THE LADDER, WHICH IS THE PRIMARY SURFACE.**

`.agi/nodes/.geometry/ladder.md:81` says it in the node's own words: *"`dispatch.py` resolves a spawn by row here; config `harnesses.*.models` is the fallback when there is no row."* Row `:37` is `{"tier": 0, "role": "kid", "harness": "pi", "model": "~deepseek/deepseek-v4-flash-latest"}` and it wins. **`harnesses.pi.models` is dead config while a ladder row exists.**

HOW IT WAS CAUGHT, because the method matters more than the fact: I widened the two config cells this round named, dispatched L4.84, and then read the kid's REAL spawn command out of the manifest rather than trusting my own edit. It said `--model '~deepseek/deepseek-v4-flash-latest'`. The kid resolved the PAID model and the round would have measured nothing. Killed at ~3 minutes, ~$0.005.

THE ALLOWLIST HALF OF (5) WAS RIGHT: the gate judges the RESOLVED pair, so widening `allowed_models` is genuinely required — it is the model CELL that was the wrong lever. A correct config diff for adopting any model therefore touches THREE cells, not two, and the ladder row is the one that decides.

This is a correction to the round, not a defect in it: the surfaces it named are real and it answered from the code it read. The lesson is the one the whole seam keeps teaching — the authority is the thing the machine actually resolves, and the only way to know it is to make the machine resolve it and read the result.
