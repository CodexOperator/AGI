---
id: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
mint_id: fd9e7505ca2f4569974eff5a192ecf87
type: hypothesis
parents:
  - experiment:a00-b6ec457f-279393
  - hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared
next_edges: []
confidence: 0.8
edited_by: director-thought
evidence_runs:
  - experiment:a00-faa1fb92-350574
scaffold_hash: b607298343c078e5
season: 2
testable_claim: "On the CMP stub (65,536-token ceiling as bytes / 3.80, usage = bytes / 3.80 on every 200, one bash tool call every turn whose RESULT adds ~6,000 tokens) with a declared contextWindow 60,000, pi 0.67.68 -p with ONE extension on the context event that replaces the bodies of the oldest tool results with a one-line placeholder until the estimate is under contextWindow - 16,384 sends 40 requests with none over 60,000 proxy tokens, no 400 and no abort, while the same run without it sends a request past 65,536 before request 20. CEILING: <=70 production lines across 1 kid"
title: A pi context-hook extension that elides the oldest tool-result bodies keeps a one-prompt pi loop under the slot with no abort -- 0 requests over the declared 60,000 in 40 turns, where CMP.03 hit the 65,536 ceiling at request 21
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
# hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot

# hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot

## Measured
- CMP.03 (experiment:a00-b6ec457f-279393, disproved): with a declared contextWindow 60,000 pi 0.67.68 sent request 20 at 62,446.8 proxy tokens (past W)
  and request 21 at 65,656.1 (past the 65,536 ceiling, a 400) with no compaction, then compacted on the overflow path and hit a second 400 at request 36
- why: auto-compaction is checked only at agent_end and before a NEW prompt (agent-session.js:337, :738); pi 0.73.1 (the latest) has the same two
  call sites -> nothing bounds context INSIDE one pi -p loop, which is how every town kid runs
- the extension lever that does NOT abort: the context event, fired before each LLM call, may return modified messages (extensions/types.d.ts:400-404,
  result :648, on("context") :727); by contrast ctx.compact() runs AgentSession.compact(), which starts with _disconnectFromAgent() + abort()
  (agent-session.js:1249-1251) -> it ends a one-prompt loop
- CMP.03 stub carried its 6 KB per turn in the tool-call ARGUMENTS (echo + 6,000 x); real loops grow through tool RESULTS -- the instrument here
  puts the growth in the result (a short command that prints ~22,800 bytes), else trimming results cannot shrink the request

## CLAIM
On the CMP stub (65,536-token ceiling as bytes / 3.80, usage.prompt_tokens = bytes / 3.80 on every 200, one bash tool call every turn whose RESULT
adds ~6,000 tokens) with a declared contextWindow 60,000, pi 0.67.68 -p with ONE extension on the context event -- before each LLM call it replaces
the bodies of the oldest tool results with a one-line placeholder until the estimate is under contextWindow - 16,384 -- sends 40 requests with none
over 60,000 proxy tokens, no 400 and no abort, while the same run without the extension sends a request past 65,536 before request 20.

## Dispatch line
config-max: none (a run reads the extension path; the adapter wiring is director-engine's) / template-max: none / code: the extension (evidence here;
director-engine ports it into the pi adapter if proved) + the stub probe

## FALSIFIERS
- with the extension, any request over 60,000 proxy tokens reaches the stub, or any 400
- the loop ends before 40 requests with the extension (an abort, an error, or a provider refusal of a trimmed history)
- a trimmed request breaks the tool-call pairing (a tool result whose call is gone, or a call with no result)
- without the extension no request passes 65,536 by request 20 (then the growth instrument is wrong -- fix it before any verdict)

## TESTS
- a selftest of the stub on VALID chat-request fixtures before either arm, fatal on failure: under -> 200 + usage; over -> 400 with a text pi-ai
  isContextOverflow recognises; either summary prompt (SUMMARIZATION_PROMPT or TURN_PREFIX_SUMMARIZATION_PROMPT) -> a summary reply
- the growth check: request n+1 minus request n ~= the printed bytes (the result reaches the request untruncated), else fix the command first
- two arms, a fresh temp PI_CODING_AGENT_DIR each, the same declared entry: (1) no extension (2) -e <the extension>; each to 40 requests or the
  first 400 or 180 s; per request: seq, bytes, bytes / 3.80, status, phase, tool results, elided results
- replication (the HOOK-B rounds, harder): --append-system-prompt a ~7,000-token file (the CLAUDE.md size, CTX.02) and a DISTINCT call id per turn (pairing
  measured by ids, not by construction); the extension estimate = ctx.getContextUsage().tokens when not null (server-reported: system prompt and
  tool schemas included), else JSON chars / 4 of the messages + the system prompt; the same two arms and the same bar

## FILE SCOPE
- ONE extension + ONE probe + the request log under paths.local_maxxing.brain_swap_out_dir (read through paths.get_local), named with the agent
  id · ONE experiment node here
- never: extensions/ · .agi/config.json · the real pi config dirs (a temp dir only) · the brain or its container · a GPU use · a real provider call

## CEILING
```
round  one pi-free kid (a lean pi-free parent spawns it with --harness pi-free) · <= 70 production lines · 0 USD · wall 60 min
STEP   LARGEST SAFE STEP if proved: the extension path as a pi adapter flag for pi-local kids (director-engine); if the trim breaks pairing: elide
       whole call+result pairs instead
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 33 (director-thought, TMM.149 / OSC.42): PASS 5 demoted this line because a00-3c370e1e's record contradicted its log and the probes launched a real pi. The corrective round experiment:a00-faa1fb92-350574 is FIXTURE-ONLY (a pytest importing json/re/pathlib/pytest, reading the committed 09-24 request logs; 31 passed, 1 xfailed, re-run by the director). On the two INDEPENDENT logs (a00-54d3d9b0, a00-cdde7530) every conjunct holds: with the extension 40 requests, max 45,206.6 / 44,849.7 proxy tokens (< 60,000), 0 400s; without it the slot is crossed at seq 11 / 12 (< 20). a00-3c370e1e's log is a byte twin of cdde7530 (only wall_seconds differ) -> counted zero times; its record corrected. Why lean, not proved: the evidence is recorded stub runs of pi 0.67.68 on 09-24, re-read, not re-run -- the fixture-only contract trades a fresh run for a re-checkable one. Rounds: r1 + r3 parents died of provider empty responses (0 bytes); r2 was rejected unharvested (its kid launched pi + a stub); r4's parent died after its kid committed, so the director did the parent review. Deviation: test 156 lines vs claim CEILING 70 (past the 2x checkpoint 140) -- a test, not production code; accepted and named.
<!-- THOUGHT:END -->
