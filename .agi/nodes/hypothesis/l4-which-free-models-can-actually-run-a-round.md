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
