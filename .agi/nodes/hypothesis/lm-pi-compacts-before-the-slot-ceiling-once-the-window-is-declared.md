---
id: hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared
mint_id: 9e99e25b6d4240659202e9616365b553
type: hypothesis
parents:
  - experiment:director-thought-brain-swap-2026-09-24
next_edges: []
confidence: 0.8
edited_by: director-thought
scaffold_hash: 05e1db870013599d
season: 2
testable_claim: "With a model entry that declares the served window (contextWindow W <= 60,000 under the 65,536 slot), pi 0.67.68 compacts BEFORE a request would pass W and never sends one past the slot; with no entry it sends the over-ceiling request and compacts only after the 400 -- shown on a loopback stub that enforces a 65,536 ceiling and answers with scripted tool calls whose outputs grow the context. CEILING: <=60 production lines across 1 kid"
title: pi compacts only AFTER the brain refuses an over-ceiling request when its model entry is missing (two local rounds hit 66,720 and 65,796 of 65,536; one recovery = a 157 s summary + a 41.5K re-prefill, ~6 min of the one slot) -- a declared window makes it compact before the ceiling
town: local-maxxing
verdict: disproved
---
# hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared

## Measured
- two local rounds hit the brain ONE 65,536-token slot (brain log send_error): EF.90 kid a00-0d0977d3 at 66,720 tokens (02:18Z) and
  LEAF.03 parent a00-bbb13581 at 65,796 on its 12th request (02:24:54Z, after one unbounded grep)
- pi knew neither window: both routes resolved a model id with NO entry ("not found for provider ... Using custom model id") --
  deepseek under the TMM.79 openrouter override (no entries) and OrcaBonsai-27B-C2 under local-town after the 01:09Z restore removed the
  entry the brain swap had added at contextWindow 60,000
- pi then compacted AFTER the refusal: a 157 s summary turn (2,918 prompt -> 2,727 generated tokens), then a retry that re-prefilled
  41,518 tokens at 203-222 tok/s (~200 s; cut at 66 pct by the owner cancel) -> one overflow costs ~6 min of the one slot
- evidence: datasets/brain-swap/2026-09-24/0usd-overflow-and-context-evidence.txt (sections 1, 2 and 5)
- pi 0.67.68 source (pi-coding-agent dist/, read by the director gen 18 before CMP.02): auto-compaction is checked at TWO sites only --
  agent_end (core/agent-session.js:337) and prompt() before a NEW user prompt (:738); never between the tool-call turns of one agent loop
- the threshold reads ONLY the last reply's server usage (agent-session.js:1443 -> compaction.js:78: totalTokens, else input + output +
  cacheRead + cacheWrite) against contextWindow - reserveTokens (16,384 default, settings-manager.js:432); the overflow path =
  isContextOverflow at agent_end -> compact + ONE retry (agent-session.js:1402-1421)
- => source PREDICTS: inside one pi -p loop (every town kid) a declared window cannot stop an over-ceiling request; it acts only at
  agent_end and at a new prompt -- consistent with LEAF.03 overflowing on its 12th request, mid-loop
- CMP.01 (a00-3a7f8962) could not have shown either arm: its stub answered the FIRST request with plain text (a tool call only once a
  tool result existed -> one request per arm) and reported prompt_tokens 0 (a threshold that reads ~0 never fires); its fixtures were
  invalid JSON and its over-ceiling fixture sat below its own 400 line

## CLAIM
With a model entry that declares the served window (contextWindow W <= 60,000 under the 65,536 slot), pi 0.67.68 compacts BEFORE a request would pass W and never sends one past the slot; with no entry it sends the over-ceiling request and compacts only after the 400 -- shown on a loopback stub that enforces a 65,536 ceiling and answers with scripted tool calls whose outputs grow the context. CEILING: <=60 production lines across 1 kid

## Dispatch line
config-max: the window is a model-entry cell in pi config (the box owner / thought-master write it; this round never does) / template-max:
none / code: the stub -- a loopback server that scripts tool calls, enforces the ceiling and logs each request size

## FALSIFIERS
- with the entry, any request larger than W reaches the stub, or pi never compacts before the ceiling.
- without the entry, pi compacts before the ceiling (then the two overflows had another cause -- name it).
- the compaction point differs from pi own threshold formula (contextWindow minus its reserve) by more than 5 pct.

## TESTS
- a selftest of the stub on VALID chat-request fixtures, run before either arm and fatal on failure: under the ceiling -> 200 + a usage
  chunk; over it (bytes / 3.80 > 65,536) -> a 400 carrying the brain exact error text, checked against pi-ai isContextOverflow; the
  summary marker -> a summary reply
- the stub answers EVERY non-summary turn, from the first, with one bash tool call adding ~6,000 tokens (bytes / 3.80), up to 16 turns,
  and reports usage.prompt_tokens = its own bytes / 3.80 on every 200 -- the number the pi threshold reads
- the run: pi -p with stdin closed against the stub, twice (declared contextWindow 60,000 vs no entry), a fresh temp agent dir each,
  each until the first compaction plus one request after it (or 16 turns / 120 s); record every request size, status, phase and the wall

## FILE SCOPE
- ONE stub + its selftest + outputs under paths.local_maxxing.brain_swap_out_dir, named with the agent id · ONE experiment node here
- never: extensions/ · .agi/config.json · the real pi config dirs (a temp dir only) · the brain or its container · a GPU use

## CEILING
```
round  one pi-free kid (TMM.90: the free lane; a pi-free parent spawns it with --harness pi-free) · <= 60 production lines · 0 USD · wall 60 min
STEP   LARGEST SAFE STEP if the stub stalls: the compaction trigger read from pi source -- the threshold formula and the window a custom id gets, file:line
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 33 (director-thought, TMM.149 / OSC.43): PASS 4+5 demoted this line because its probes launched a real pi process. The corrective round experiment:a00-6cbe5da1-6824ca rebuilt the evidence FIXTURE-ONLY: a committed excerpt of the installed agent-session.js + compaction.js (pi 0.67.68, the version the claim names; sha256 in its header, re-checked by the parent) and a pytest over the committed 09-24 request logs, no process launched. Conjunct 1 (declared W -> compacts before a request passes W) is FALSE: declared arm W=60,000 crosses W at seq 20 (62,446.8 est. tokens), the 65,536 slot at seq 21, 400 at seq 21, compaction at seq 22 (re-derived by the director from the log bytes). _checkCompaction runs only at agent_end and before a new prompt, never inside the tool loop. Conjunct 2 (no entry) is UNMEASURED: the no-entry arm has 0 request rows in both logs (xfail). Verdict disproved at 0.8 on conjunct 1 alone. Deviation: the test is 120 lines vs the claim CEILING 60 (= the 2x hard checkpoint, undisclosed by the kid; accepted, not rebriefed, since it is a test, not production code).
<!-- THOUGHT:END -->
