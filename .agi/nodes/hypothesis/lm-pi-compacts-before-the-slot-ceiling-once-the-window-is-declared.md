---
id: hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared
mint_id: 9e99e25b6d4240659202e9616365b553
type: hypothesis
parents:
  - experiment:director-thought-brain-swap-2026-09-24
next_edges: []
edited_by: director-thought
scaffold_hash: 05e1db870013599d
season: 2
testable_claim: "With a model entry that declares the served window (contextWindow W <= 60,000 under the 65,536 slot), pi 0.67.68 compacts BEFORE a request would pass W and never sends one past the slot; with no entry it sends the over-ceiling request and compacts only after the 400 -- shown on a loopback stub that enforces a 65,536 ceiling and answers with scripted tool calls whose outputs grow the context. CEILING: <=60 production lines across 1 kid"
title: pi compacts only AFTER the brain refuses an over-ceiling request when its model entry is missing (two local rounds hit 66,720 and 65,796 of 65,536; one recovery = a 157 s summary + a 41.5K re-prefill, ~6 min of the one slot) -- a declared window makes it compact before the ceiling
town: local-maxxing
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
- a selftest of the stub on fixtures: a request past the ceiling -> a 400 with the brain exact error text; below it -> a scripted reply.
- the run: pi -p with stdin closed against the stub, twice (with and without the entry), each to the first compaction or the first 400;
  record every request size, the compaction point and the wall.

## FILE SCOPE
- ONE stub + its selftest + outputs under paths.local_maxxing.brain_swap_out_dir, named with the agent id · ONE experiment node here
- never: extensions/ · .agi/config.json · the real pi config dirs (a temp dir only) · the brain or its container · a GPU use

## CEILING
```
round  one pi-free kid (TMM.90: the free lane; a pi-free parent spawns it with --harness pi-free) · <= 60 production lines · 0 USD · wall 60 min
STEP   LARGEST SAFE STEP if the stub stalls: the compaction trigger read from pi source -- the threshold formula and the window a custom id gets, file:line
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
frame: as-given -- the owner retired the local lane as an operating mode (02:3xZ: research towards more efficient 0-USD runs), so this prices one of its two measured failure modes for a future lane. Cheapest disproving test: a stub server, no GPU, no brain. Bigger frame: any fixed-slot server behind a harness that trusts a model table. If wrong, the next move is reading where pi sets the window of a custom id.
<!-- THOUGHT:END -->
