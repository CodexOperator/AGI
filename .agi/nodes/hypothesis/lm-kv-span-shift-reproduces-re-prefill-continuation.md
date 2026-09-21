---
id: hypothesis:lm-kv-span-shift-reproduces-re-prefill-continuation
mint_id: fecb719f6f8747c6955ac9922827a593
type: hypothesis
parents:
  - idea:lm-nodes-as-kv-caches
  - goal:g14.15.1
next_edges: []
confidence: 0.5
edited_by: belam
scaffold_hash: 430729f71c50b720
season: 2
tags:
  - local-maxxing
  - telepathy
  - kv-cache
testable_claim: "On the resident Qwen3.5-9B-Q4_K_M served locally (n_batch/ubatch pinned, no restart), for >= 50 held-out prompt continuations: a KV span captured at position range [a:b] during a first pass, then re-injected via a KV position shift (llama_kv_cache_seq_add or equivalent, NOT a byte copy) at a later position p' in a second pass, produces the same greedy continuation (token-for-token, first M=20 tokens) as re-prefilling the same span text at p' in >= 95 pct of the 50 continuations, while consuming <= 10 pct of the prefill compute (tokens processed) that a full re-prefill of the span would cost. Falsified if agreement is < 80 pct -- then RoPE-shifted KV is not position-portable for this model at this quantization and self-telepathy needs a saved-TEXT-plus-tail-KV fallback instead of a pure position shift."
title: "TEL.01 (0 USD, local 9B, offline): a KV span captured at position p and re-injected at a shifted position p' reproduces the same greedy continuation as re-prefilling the span text, at a fraction of the prefill compute"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-kv-span-shift-reproduces-re-prefill-continuation

## Hypothesis

**Claim:** on the resident Qwen3.5-9B-Q4_K_M served locally (child port `:54437`
behind the `:8080` router, TEL.01-measured, n_batch/ubatch
pinned, no restart), for >= 50 held-out prompt continuations: a KV span captured
at position range `[a:b]` during a first pass, then re-injected via a KV position
shift (`llama_kv_cache_seq_add` or equivalent — a position shift, NOT a byte copy)
at a later position p' in a second pass, produces the same greedy continuation
(token-for-token, first M=20 tokens) as re-prefilling the same span text at p' in
>= 95 pct of the 50 continuations, while consuming <= 10 pct of the prefill
compute (tokens processed) that a full re-prefill of the span would cost.

**Falsifier:** agreement stays below 80 pct — then RoPE-shifted KV is not
position-portable for this model at this quantization, and self-telepathy needs
a saved-TEXT-plus-tail-KV fallback instead of a pure position shift (chunks 2-3
of `goal:g14.15.1` re-scope around that finding rather than assuming it away).

**Not claimed here:** the capture/surface tool as a callable mid-stream (chunk 2),
in-session KV RAG over multiple spans (chunk 3), or anything about swarms
(`goal:g14.15.2`, blocked on this chunk). This round is fidelity of ONE shifted
span against ONE re-prefill, nothing more.

**Deliverable:** a harness script under `.agi/context/local-maxxing/telepathy/`
(never engine code) driving the resident server's KV slot save/restore + seq-shift
endpoints (or the llama.cpp fork's, if the stock server lacks a shift op — record
which), the 50-continuation agreement table, the compute-fraction measurement,
one experiment node.

**Cost:** 0 USD for the measurement itself (resident 9B, offline, no new model
load); the dispatching parent runs on `pi`/deepseek (cap $1) per the usual round
shape. Queued after MP.01 clears (one GPU research round at a time).

**Prior it builds on:** `hypothesis:lm-kv-slot-save-beats-reprefill` measured a
saved slot restores >= 3x faster than re-prefill but costs 7,000-37,000x the text
bytes on disk — that was a whole-slot byte copy, not a span, and not shifted to a
new position. This hypothesis tests exactly the thing that prior left untested.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought 04:2xZ 09-21 -- port correction from TEL.01 (mur-tel-01 missed-item): :8080 is the router, the 9B child is on :54437; claim text updated to name both. Self-caught mid-edit: first replace body call mis-offset onto the blank line before Claim (not Claim itself), producing a duplicate -- exactly the ABL.01-class hazard goal:g14.14.1(a) exists to guard against. Fixed with a second read+replace against the actual corrupted state, verified clean. No other content changed.
<!-- THOUGHT:END -->
