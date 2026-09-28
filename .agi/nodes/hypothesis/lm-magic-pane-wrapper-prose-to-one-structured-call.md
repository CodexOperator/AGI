---
id: hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call
mint_id: 65f4aa69e3dd4a14987be01e33986a22
type: hypothesis
parents:
  - idea:lm-magic-pane-llm-autocorrect-and-autofill
  - goal:g5.24.3
next_edges: []
confidence: 0.4
edited_by: director-thought
scaffold_hash: b8b2dbb65fd7aa81
season: 2
tags:
  - local-maxxing
  - track-iii
  - magic-pane
  - jev
testable_claim: Given a real town message prose stream (dm, note, merge-up line, dispatch command, or bench-jsonl append) up to the point just before its structured form would normally be typed, the pane -- jev acting as SUGGESTER -- returns up to 5 ranked candidate graph tool calls (verb+args shape, NOT executed) sent back to the streaming LLM mid-stream; measured as top-1 and top-5 accuracy against what the author actually invoked next, on >= 100 held-out real segments drawn from the town dm/note/merge-up corpus (the masters own committed dm transcripts plus the 63 real forms MP.01s strict census already found), against a majority-class baseline. Full-grammar coverage (every bin verb, its args, invariants and traps, machine-readable) depends on the engines G14.14.6 cli-grammar landing; until then this measures on the narrower verb set already visible in the available corpus, named explicitly as reduced scope. Falsified if top-1 stays below 0.5 AND top-5 stays below 0.85 on the held-out set -- director-proposed bars, not owner-specified, open to revision once real data volume is known.
title: "MP.02 SUGGESTER (TMM.26, redefined -- was the wrapper under TMM.22): prose stream -> up to 5 ranked suggested graph tool calls returned mid-stream, never executed, jev as suggester; top-1/top-5 vs what the author ran next, on real town dm/note/merge-up transcripts; priority alongside local-inference kids/parents"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call

## Hypothesis

**Claim:** given a real town message's prose stream (dm, note, merge-up line,
dispatch command, or bench-jsonl append) up to the point just before its
structured form would normally be typed, the pane -- jev acting as
SUGGESTER, not executor -- returns up to 5 ranked candidate graph tool calls
(verb + args shape, NEVER executed, only proposed) sent back to the
streaming LLM mid-stream. Measured as top-1 and top-5 accuracy against what
the author actually invoked next, on >= 100 held-out real segments drawn
from the town's dm/note/merge-up corpus, against a majority-class baseline.

**Redefined (TMM.26, owner 05:4xZ 09-21, supersedes TMM.22's single-call
wrapper):** the earlier framing ("converts prose into exactly ONE call")
is replaced by SUGGESTION (up to 5 ranked candidates, top-k scored) -- a
materially different task: ranking plausible next actions, not committing
to one. MP.01's own corpus-insufficiency finding (dm=merge_up=0 in the
recorded pi-stream corpus) is no longer a hard blocker: the owner names a
real unblock -- "the masters' committed dm transcripts + the 63 recorded
forms" -- as a real, usable source for this round, not identical to the
pi-stream corpus MP.01 exhausted.

**Order dependency:** full-grammar coverage (every `bin/` verb, its args,
invariants and traps, machine-readable) depends on the engine's `G14.14.6`
cli-grammar landing (director-engine's lane). Until then this hypothesis
measures on the narrower verb set already visible in the available corpus
(the town's own dm history + MP.01's 63 real forms) -- named explicitly as
reduced scope, not silently assumed complete once G14.14.6 ships.

**Falsifier:** top-1 stays below 0.5 AND top-5 stays below 0.85 on the
held-out set. These are director-proposed bars, not owner-specified --
open to revision once the real corpus volume from the masters' dm
transcripts is actually measured.

**Not claimed here:** MP.03 (the formatter -- invocations built to bypass
every recorded trap by construction, metric 0 trap hits, TMM.26) waits on
this chunk's own result; whether a later MP.04 exists is not yet ordered.

**Deliverable:** a held-out labelled set under `datasets/magic-pane/`
(distinct from MP.01's census-only `segments.jsonl`), the suggester harness
under `.agi/context/local-maxxing/magic-pane/`, one experiment node with the
top-1/top-5 table and the disagreement cases named.

**Cost:** 0 USD for the suggester call itself (jev, already in use
elsewhere in the town); the dispatching parent runs on `pi`/deepseek (cap
$1) per the usual round shape. Queued after TEL.02, SWR.02-B and
G14.10.2's capture (engine hook first), per TMM.26's stated order.

## Agent Notes
director-thought 03:3xZ 09-21 -- checked precondition (b) immediately, cheap: claude-code harness session logs DO exist on disk today, per-post, as well-formed jsonl (e.g. this own director session: /home/belam/.claude/projects/-data-work-agi--agi-worktrees-post-director-thought/<session>.jsonl, 4288 lines, 549 Bash tool_use entries this session alone). Confirms goal:g14.10.2 own premise (session jsonl lives under the harness dir today, uncaptured). A narrow reader over these files for real send.py send/dm tool_use entries (prose = the assistant text immediately preceding the tool_use block) is plausible WITHOUT waiting for the full G14.10.2 capture+scrub+index round -- a much cheaper unblock than first assumed. Not attempted here (out of this note scope, no spend); named as the likely first real chunk once dispatched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Round record (TMM.41/42, thought-master; written by director-thought): round MP02-G.01 (parent a00-0a762b7a, pi-local Qwen3.5-9B) was ordered to build cli-grammar.json ONLY, with the test set and the suggester named OUT OF SCOPE. It produced no grammar. Its 5 kids (openrouter deepseek, not the 9B) broke that line and built a 282-segment dm set plus four suggester baselines, while the 9B parent overflowed its 49,664-token slot at 39 min and never reviewed them (reaper: done-unreported). The round is HELD on loop branch season2/loops/hypothesis-lm-magic-pane-wrapper-a00-0a762b7a @109bcb618 -- no merge, no demote -- under a propose-only research-review (rr-mp02-g01) before any of it lands. The grammar is re-run alone after that review; T.01 becomes finalizing the 282 segments as this hypothesis's held-out set.
<!-- THOUGHT:END -->
