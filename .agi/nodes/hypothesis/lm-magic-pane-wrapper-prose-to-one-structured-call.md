---
id: hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call
mint_id: 65f4aa69e3dd4a14987be01e33986a22
type: hypothesis
parents:
  - idea:lm-magic-pane-llm-autocorrect-and-autofill
  - goal:g14.8.3
next_edges: []
confidence: 0.4
edited_by: belam
scaffold_hash: b8b2dbb65fd7aa81
season: 2
tags:
  - local-maxxing
  - track-iii
  - magic-pane
  - jev
testable_claim: "Given a real town message segment (dm, note, merge-up line, dispatch command, or bench-jsonl append) captured with its full prose, a wrapper -- the resident Qwen3.5-9B or deepseek-v4.1-flash acting as jev judge -- converts the prose into exactly ONE correctly-typed structured call (right form AND correctly populated required fields: target node/recipient/path as named in the prose) at >= 0.75 end-to-end accuracy on >= 100 held-out real segments, judged by an independent jev pass (not the same regex census that produced the label), against a majority-class-plus-empty-fields baseline. Gated precondition: MP.01 found the currently-recorded pi-stream corpus has ZERO dm and ZERO merge_up examples (goal:g14.10.2 is the fix); this hypothesis cannot be dispatched for a real measurement -- only mined for a first chunk -- until at least one of (a) goal:g14.10.2 lands enough director-session capture to supply real dm/merge_up prose, or (b) an existing on-disk claude-code harness session log is confirmed to already carry usable dm/merge_up examples without needing the full capture pipeline. Falsified if end-to-end accuracy stays < 0.5 on whatever corpus eventually qualifies, or if the corpus gate is never clearable, in which case the wrapper is tested on the four classes MP.01 DID find real examples for (write_set, dispatch, bench_jsonl, node_write) as a reduced-scope fallback, explicitly not the full form list."
title: "MP.02 (the wrapper, TMM.22): prose -> one correctly-typed+populated structured call, judged by jev, on real town messages -- BLOCKED at dispatch time on real dm/merge_up examples existing anywhere captured (MP.01: zero in the current corpus); reduced-scope fallback on the four classes MP.01 did find"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call

## Hypothesis

**Claim:** given a real town message segment (dm, note, merge-up line, dispatch
command, or bench-jsonl append) captured with its full prose, a wrapper -- the
resident Qwen3.5-9B or deepseek-v4.1-flash acting as jev judge -- converts the
prose into exactly ONE correctly-typed structured call (right form AND
correctly populated required fields: target node/recipient/path as named in
the prose) at >= 0.75 end-to-end accuracy on >= 100 held-out real segments,
judged by an independent jev pass, against a majority-class-plus-empty-fields
baseline.

**Gated precondition (why this is minted but not yet dispatchable):** MP.01
(`experiment:a00-5b80b456-eda3d8`) found the currently-recorded pi-stream
corpus has ZERO `dm` and ZERO `merge_up` examples -- directors emit both, but
director-level sessions are not captured anywhere in `datasets/`, which is
exactly the gap `goal:g14.10.2` commits to closing. This hypothesis is not
dispatchable for a real measurement until EITHER (a) `goal:g14.10.2` lands
enough director-session capture to supply real dm/merge_up prose, OR (b) an
existing on-disk claude-code harness session log is confirmed to already carry
usable dm/merge_up examples without needing the full capture pipeline -- an
open question, not yet checked, and cheap to check before waiting on (a).

**Falsifier:** end-to-end accuracy stays < 0.5 on whatever corpus eventually
qualifies. If the corpus gate is never clearable, the fallback is a
REDUCED-SCOPE test on the four classes MP.01 did find real examples for
(`write_set`, `dispatch`, `bench_jsonl`, `node_write`) -- explicitly not the
full seven-class form list, and reported as reduced scope, not silently
substituted.

**Not claimed here:** MP.03 (replacing send.py's own argument grammar for one
post pair, delivery measured) or MP.04 (own tiny model vs jev) -- both wait on
this chunk clearing its own bar first, per the chain on `goal:g14.8`.

**Deliverable:** a held-out labelled+judged set under `datasets/magic-pane/`
(distinct from MP.01's census-only `segments.jsonl`), the wrapper harness under
`.agi/context/local-maxxing/magic-pane/`, one experiment node with the
end-to-end accuracy table and the jev-judge disagreement cases named.

**Cost:** 0 USD for the wrapper itself (local 9B or the same jev judge already
in use); the dispatching parent runs on `pi`/deepseek (cap $1) per the usual
round shape, once the corpus gate clears.

## Agent Notes
director-thought 03:3xZ 09-21 -- checked precondition (b) immediately, cheap: claude-code harness session logs DO exist on disk today, per-post, as well-formed jsonl (e.g. this own director session: /home/belam/.claude/projects/-data-work-agi--agi-worktrees-post-director-thought/<session>.jsonl, 4288 lines, 549 Bash tool_use entries this session alone). Confirms goal:g14.10.2 own premise (session jsonl lives under the harness dir today, uncaptured). A narrow reader over these files for real send.py send/dm tool_use entries (prose = the assistant text immediately preceding the tool_use block) is plausible WITHOUT waiting for the full G14.10.2 capture+scrub+index round -- a much cheaper unblock than first assumed. Not attempted here (out of this note scope, no spend); named as the likely first real chunk once dispatched.
