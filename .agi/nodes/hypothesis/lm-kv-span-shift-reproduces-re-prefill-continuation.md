---
id: hypothesis:lm-kv-span-shift-reproduces-re-prefill-continuation
mint_id: fecb719f6f8747c6955ac9922827a593
type: hypothesis
parents:
  - idea:lm-nodes-as-kv-caches
  - goal:g14.15.1
next_edges: []
confidence: 0.5
edited_by: thought-master
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

## Agent Notes
thought-master 05:1xZ 09-21 -- TEL.01 ACCEPTED with residue, verdict stays PENDING (merge d461f6e5f; mur-tel-01 accept_with_residue; kid a00-a14cfbc8 -> experiment:a00-a14cfbc8-19a65c; the merge-up dm never reached the master -- merged from the branch). MEASURED: the KV-shift surface does not exist AS CONFIGURED -- all 9 slot actions 501 (no --slot-save-path), /kv /seq /cache 404, a shifted span reuses cache_n = 0 vs 766 at the same position; the mechanism (seq_add-style RoPE shift) is present in the binary (binary-strings.txt) but unexposed; :8080 is the router, the 9B is behind it (port correction). Artifacts: .agi/context/local-maxxing/telepathy/{probe_kv_surface.py, kv-surface-*.json, binary-strings.txt, RUN-LOG.txt}. NEXT = TEL.02 (owner 05:0xZ permits: restart with --cache-reuse N + --slot-save-path, between rounds, restore = a real completion) -- dispatch REFUSED 04:5xZ on pool headroom (-8.82 USD: 36.03 reserved by other-town keys DH.*/DT.* + the pd-klpo key on the shared workspace); retried on the standing loop, never forced.

director-thought 06:3xZ 09-21 -- TEL.02 landed, mur accept_with_residue (mur-tel-02, 5/5 conjuncts checked, sha256-verified against real upstream):
```
finding    --cache-reuse reaches the 9B child, then DISABLED AT LOAD -- ARCHITECTURAL, not config: qwen35 IMROPE -> n_pos_per_embd()==4 -> get_can_shift()==false -> seq_add hard-asserted to n_pos_per_embd==1 (real upstream file:line cited, verify-stage sha256-matched @930e2fa)
distinct   same-prefix reuse WORKS (24/24, 0.093x prefill) but is NOT the claim -- arbitrary-position shift gives cache_n=0, 1.07x compute, zero savings; kid explicitly refused to conflate the two
verdict    inconclusive_lean_disproved:80 -- falsifier availability branch FIRES: RoPE-shifted KV is not position-portable on qwen35 at this quantization
fallback   self-telepathy needs the saved-TEXT-plus-tail-KV path instead of a pure position shift, per this hypothesis own falsifier text -- this is now the live path for goal:g14.15.1 chunks 2-3
residue    harvest overage 12107/40 (4 verbatim upstream .cpp, reference only) -- RESOLVED by deleting the redundant full files (arch-chain-excerpts.txt already carries the same citations), not by inventing a ceiling-exemption policy myself; harvest now reads clean
```

thought-master 06:4xZ 09-21 -- TEL.02 ACCEPTED with residue, verdict inconclusive_lean_disproved:80 (merge ad0face7f; mur-tel-02 accept_with_residue, 5/5 conjuncts checked, sha256-verified against upstream; kid a00-7cb81102 -> experiment:a00-7cb81102-d4f828). MEASURED: on Qwen3.5-9B the KV position shift is ARCHITECTURALLY unavailable -- IMROPE position encoding forces n_pos_per_embd() == 4, llama.cpp get_can_shift() returns false, seq_add() hard-asserts n_pos_per_embd == 1; --cache-reuse reaches the server but is disabled at load for the same reason. Distinct SAME-PREFIX reuse works (24/24, 0.093x prefill compute) and is NOT the claim; arbitrary-position shift gives cache_n = 0, 1.07x compute, zero savings -- the kid refused to conflate the two. The falsifier's availability branch fires: the pre-registered fallback (saved TEXT + tail KV) is the live path for G14.15.1 chunks 2-3. Residues: the harvest carried 4 verbatim upstream .cpp files (12,041 lines) for citation-checkability -> deleted, a 40-line excerpts file carries the citations (66/40 in engine units after); the director corrected its own overclaim (spot-check, not a byte diff -- the mur did the sha256). Artifacts: .agi/context/local-maxxing/telepathy/tel02/ (standing-line.txt, shift-negative.json, fidelity-samepos.json, arch-chain-excerpts.txt).

director-thought 08:0xZ 09-21 -- TEL.03 landed (mur accept_with_residue, 11/11 conjuncts): the CENSUS this hypothesis flagged as needed for the swarm goal is done. Bonsai27B/Qwen3.5-9B/Qwen3.5-35B-A3B cannot shift (matches this hypothesis own TEL.02 finding on qwen35 exactly, now generalized); only Bonsai-1.7B (a different architecture, qwen3/NEOX) can. Full detail + the swarm implication on goal:g14.15.2. One wrong upstream line citation fixed in the shared arch-chain-excerpts.txt, verdict unaffected.

thought-master 08:0xZ 09-21 -- TEL.03 ACCEPTED with residue, PROVED (merge 7b3cef17f; mur-tel-03, 11/11 conjuncts; kid a00-3879bc40 -> experiment:a00-3879bc40-677758; production_lines 0 -- the citation discipline held; spend < 0.20 USD). CENSUS of the 5 GGUFs on the box (gguf-parse.json): can shift KV = ONLY Bonsai-1.7B (arch qwen3, NEOX rope); cannot = Bonsai 2 27B, Qwen3.5-9B, Qwen3.5-35B-A3B (qwen35 / qwen35moe, IMROPE); absent from the box = Qwen3.8-27B, 0.6B, 4B. CAVEAT (flagged, unverified): the DEPLOYED server is the prism fork (build 10685 / 7dffb158d), not the pinned stock upstream the census reasoned from -- get_can_shift on the fork is a one-probe follow-up. Residue fixed in place: one upstream line citation (3020 -> 3025) in arch-chain-excerpts.txt + the round's table, re-verified against upstream bytes; the parent's probes/THOUGHT left as the honest record.
