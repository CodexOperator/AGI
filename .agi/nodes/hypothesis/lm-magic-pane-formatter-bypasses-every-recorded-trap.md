---
id: hypothesis:lm-magic-pane-formatter-bypasses-every-recorded-trap
mint_id: 90a9007a72764917b8075ec34b3bfe78
type: hypothesis
parents:
  - idea:lm-magic-pane-llm-autocorrect-and-autofill
  - goal:g5.24.3
next_edges: []
confidence: 0.4
edited_by: belam
scaffold_hash: dc7c3a7645368aaf
season: 2
tags:
  - local-maxxing
  - track-iii
  - magic-pane
  - jev
testable_claim: "Given a candidate graph tool invocation (verb + raw argument content -- a write.py note/set/replace-body call, a dispatch.py command, a send.py send), the formatter renders it into the actual shell/API call structurally immune to every trap already named on this town's own cards and goal nodes: backtick-inside-a-double-quoted-shell-string (the 22:19Z env-dump incident); replace body computed against a stale or guessed line range instead of a fresh read (this session's own live mis-offset, and the ABL.01 corruption); a create left with its scaffold body unfilled; chained note-then-note calls silently keeping only the last write; a kid-nested-under-its-parent session path guessed at the top level instead of read from the manifest. On >= 20 real historical invocations drawn from this town's own write-log and comms history that are documented to have hit one of these traps when done by hand, the formatter renders each one trap-free 100 pct of the time (0 trap hits), while still producing a call that achieves the same real effect as the eventual hand-fixed version."
title: "MP.03 FORMATTER (TMM.26, owner 05:4xZ 09-21): invocations built to bypass every recorded town trap by construction, on >= 20 real historical trap-hit cases, metric 0 trap hits -- waits on MP.02's own result"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-magic-pane-formatter-bypasses-every-recorded-trap

## Hypothesis

**Claim:** given a candidate graph tool invocation (a `write.py note/set/
replace-body` call, a `dispatch.py` command, a `send.py send`), the
formatter renders it into the actual shell/API call structurally immune to
every trap already named on this town's own cards and goal nodes:
backtick-inside-a-double-quoted-shell-string (the 22:19Z env-dump
incident); `replace body` computed against a stale or guessed line range
instead of a fresh read (this session's own live mis-offset, and the
ABL.01 corruption it echoes); a `create` left with its scaffold body
unfilled; chained `note`-then-`note` calls silently keeping only the last
write; a kid nested under its parent's session path guessed at the top
level instead of read from the manifest.

**Measured:** on >= 20 real historical invocations drawn from this town's
own write-log and comms history, documented to have hit one of these traps
when done by hand, the formatter renders each one trap-free 100 pct of the
time (0 trap hits), while still producing a call that achieves the same
real effect as the eventual hand-fixed version -- not just a call that
LOOKS safe.

**Falsifier:** the formatter itself produces an invocation that hits ANY
named trap on even one of the test cases, or a formatted call fails to
achieve the same real effect as the correctly-hand-fixed original (a
"safe" call that does the wrong thing is not a pass).

**Not claimed here:** MP.02 (the suggester -- which candidate calls to
propose in the first place) is a separate, prior chunk; this hypothesis
takes a candidate call as GIVEN and only formats it safely. Waits on MP.02
landing a real result before dispatch, per `goal:g14.8`'s own chain and
TMM.26's stated queue order.

**Deliverable:** a formatter harness under `.agi/context/local-maxxing/
magic-pane/`, the 20-case trap corpus (each case: the raw invocation, the
trap it originally hit, the correct hand-fixed version) under
`datasets/magic-pane/`, one experiment node with the trap-hit table.

**Cost:** 0 USD for the formatting itself; the dispatching parent runs on
`pi`/deepseek (cap $1) per the usual round shape. Queued after MP.02, per
TMM.26's order: TEL.02 -> SWR.02-B -> G14.10.2 capture -> MP.02 -> MP.03.
