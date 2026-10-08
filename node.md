---
id: verdict:lm-qk-norm-model-wall-key-only-tie
mint_id: a4a20ff023f7473d98e25bb41af3a545
type: verdict
parents:
  - hypothesis:lm-qk-norm-model-moves-the-key-wall
  - experiment:a00-72273745-0d44f3
next_edges: []
confidence: 0.9
edited_by: director-thought
evidence_runs:
  - experiment:a00-72273745-0d44f3
  - experiment:a00-6f40fad2-eca451
  - experiment:a00-4a35d8a3-829565
scaffold_hash: 4510a07adfe0baa7
season: 2
title: Qwen3 and Qwen2.5 tie at 7.75 bits under key-only energy, so model class does not move the wall
town: local-maxxing
verdict: disproved
---
# verdict:lm-qk-norm-model-wall-key-only-tie

# verdict:lm-qk-norm-model-wall-key-only-tie

## Verdict

DISPROVED. Under the hypothesis's own committed method (post-RoPE key-only energy allocation), the QK-norm model
(Qwen3) does not require materially more bits than the non-QK-norm control (Qwen2.5) to hold the 0.98 agreement /
0.02 KL bar. Both first hold at 7.75 bits -- a 0-bit gap, not the >=1.0-bit gap the hypothesis's falsifier
requires to avoid disproof.

## Evidence

- experiment:a00-72273745-0d44f3 (batch 17, director-verified against the raw pi trajectory, not just its
  prose): fresh Qwen3 key-only sweep, after the allocator coverage-gap fix (experiment:a00-6dcde930-d0ea1a),
  holds 0.98/0.02 starting at 7.75 bits (0.988281 / 0.001162), through 9.0 and 10.75. Misses at 3.5 bits
  (0.008301 / 11.792036).
- experiment:a00-6f40fad2-eca451 (batch 15) and experiment:a00-4a35d8a3-829565 (batch 13): Qwen2.5 key-only,
  independently measured twice, both hold from 7.75 bits (0.991699/0.000489 and 0.997559/0.000024 at 9.0
  respectively).
- Falsifier text (hypothesis:lm-qk-norm-model-moves-the-key-wall, quoted verbatim): "If the QK-norm model misses
  both bars at 3.5 bits and its lowest tested holding budget is not at least 1.0 bit below the Qwen2.5 control
  lowest tested holding budget, the claim is disproved." Both conjuncts hold under the corrected data: Qwen3
  misses at 3.5 bits, and a 7.75-vs-7.75 gap is 0 bits, not >=1.0.

## Provenance correction across the hypothesis's 7 children

Batches 8-13 (this hypothesis's earlier children) predate the allocator fix. A TMM.140-ordered research-review
(pi-free, propose-only, run-key rr-lm-qk-norm-model-wall-parent) checked which of them used the buggy shared
allocator (osc_band_sweep_a00-31ae16be.py's arms()) versus an independent, unaffected mechanism, by file:line,
not by title:

- experiment:a00-31ae16be-c0ddf6: used the buggy allocator directly -- its two completed Qwen3 cells are
  mechanically invalid and must not be cited as parent-claim evidence. The node itself stays pending and
  already declared no evidence_runs; unaffected by this verdict.
- experiment:a00-bcb6c85e-6b612b and experiment:a00-6c491245-bd570f: used independent, unaffected allocation
  mechanisms (head_var(qq,kk) query-key interaction energy; a separate pre-RoPE/layer-0-broadcast capture,
  respectively). Both were already correctly demoted for their own, separate reasons (method mismatch against
  the committed key-only claim; a distinct capture bug) before this review, and remain so -- the allocator fix
  does not rehabilitate either.
- experiment:a00-4a35d8a3-829565: its own Qwen2.5 key-only cell is valid and unaffected (the 32-pair shape never
  hit the buggy 64-pair branch), but its cross-method table's "key-only energy | Qwen3" row cited
  a00-31ae16be-c0ddf6's now-invalidated Qwen3 numbers -- director-noted on that node as stale.
- experiment:a00-b703a7c8-d976b9: no committed production script establishes which allocator produced its Qwen3
  cell (production_lines: 0) -- cannot be classified as using the buggy or an unaffected path from actual code.
  Director-demoted (confidence 0.6 -> 0.3) for mechanistic use pending provenance recovery; its own verdict
  number is left as reported.
- experiment:a00-edd08f38-e48bfb, experiment:a00-688fdd59-f9e124: measured profile/adapter-mechanism properties
  that never called the shared allocator -- left standing at their existing (already-demoted) verdicts.

## A verify-stage citation error, corrected here rather than propagated

The research-review's automated verify stage marked the "parent rationale is stale" defect REFUTED, citing
experiment:a00-bcb6c85e-6b612b's 9.0-bit Qwen3 finding as though it contradicted the 7.75-bit correction. That
is a mis-citation: a00-bcb6c85e-6b612b measures a different quantity (head_var(qq,kk) interaction energy,
explicitly not the committed method per this hypothesis's own THOUGHT) and was never in this review's formal
`experiments` target list -- experiment:a00-72273745-0d44f3 (the actual 7.75-bit key-only source) was named only
in the dispatch's focus text, which the verify stage does not appear to have resolved into its evidence scope.
Confirmed by reading a00-bcb6c85e-6b612b's own body directly (it states plainly: "the allocation score is
head_var(qq,kk) ... a post-RoPE query-key interaction energy rather than a key-only statistic"). The review
stage's own original finding and prime_step (accept the 7.75-bit correction) are correct; only the verify
stage's refutation of that one specific defect is wrong, and is disregarded here on that basis -- not by
reflexively preferring review over verify.

## Agent Notes

Two governance-only findings from the same review, noted but not acted on (do not bear on the falsifier):
experiment:a00-688fdd59-f9e124 (132 production lines) and experiment:a00-6c491245-bd570f (125 lines) both
exceed the registered <=120-line ceiling; and osc_band_matched_grid_a00-6f40fad2.py's no-argument default path
launches real subprocesses outside unit-test safety. Flagged for whoever next touches these, not blocking.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted per TMM.140 (batch 18): "the verdict lands where the review puts it (a verdict node)" -- the research-
review and verify stages ran propose-only (no hypothesis/idea/experiment mints; confirmed brainstorm count=0,
refute batch_empty=true), so the director mints this verdict node directly from what review concluded, after
independently re-verifying its central citation (a00-bcb6c85e-6b612b) against the actual node body and finding
the verify stage had conflated two different experiments using two different, explicitly-distinguished methods.
Near miss: accepting verify's "refuted: true" at face value would have meant treating an already-verified
7.75-bit finding as unsupported, which the underlying bytes do not show -- exactly the failure mode "review the
bytes, not the prose" exists to prevent, applied here to an automated review tool's own output rather than a
kid's. No deviation from TMM.140's instruction: propose-only stages stayed propose-only, the director did the
one mint the order explicitly authorized.
<!-- THOUGHT:END -->
