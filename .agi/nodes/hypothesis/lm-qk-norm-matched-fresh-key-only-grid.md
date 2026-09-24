---
id: hypothesis:lm-qk-norm-matched-fresh-key-only-grid
mint_id: fe6b6343ebc84ec0895abe5850be35e8
type: hypothesis
parents:
  - idea:lm-why-key-only-grid-not-self-contained
next_edges: []
FILE SCOPE: ".agi/context/local-maxxing/osc/ (repo-tracked) and a fresh dated dir under datasets/osc-band/ only -- no router changes, no engine edits, NO new downloads (both models already resident: paths.local_maxxing.osc03_hf_dir, paths.local_maxxing.osc15_hf_dir)."
ceiling: "kids: <=120 production lines, ONE kid. pi parent. $0 expected (CPU-only); <=1 USD hard ceiling if GPU compute is required; no live provider spend without a fresh owner yes; no new downloads."
edited_by: director-thought
falsifier: Qwen2.5 fails to hold the 0.98/0.02 bar by 7.75 bits, OR Qwen3 holds it at or before 10.75 bits, OR any of the 8 primary cells (4 widths x 2 models, each with key-only + matched uniform + matched random) is missing, inherited from a prior experiment or node, or captured with a pre-RoPE/layer-0-broadcast method instead of the fixed post-RoPE per-layer capture.
scaffold_hash: 228a01a7ced90993
season: 2
testable_claim: "Running one self-contained key-only energy measurement -- fixed post-RoPE, per-layer capture (not layer-0 broadcast), one model per process with a memory check before each load -- for Qwen2.5 and Qwen3 at 3.5, 7.75, 9.0, and 10.75 bits, each width with matched uniform and random controls under identical allocator and control definitions, every one of the 8 primary cells measured fresh in this round (no cell inherited from a prior experiment), will show Qwen2.5 first holding the 0.98 agreement / 0.02 KL bar at 7.75 bits while Qwen3 remains below it through 10.75 bits, so the committed falsifier remains met. A pre-RoPE/layer-0-broadcast capture, if run at all, is a separately labeled control arm, never the measurement the verdict rests on. CEILING: <=120 production lines."
tests: "ONE pi parent + ONE kid. Steps: (1) run the committed regression at .agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e_test.py unmodified first as a sanity check on the reused fixed-capture mechanism; (2) for Qwen2.5 then Qwen3, sequential, one model per process, checking available memory before each load: profile once, then sweep key-only energy + matched uniform + matched random controls at 3.5/7.75/9.0/10.75 bits; (3) persist a self-contained results.json per model with all 4 widths x 3 arms; (4) add and run one new committed test asserting all 8 primary cells are present with no None/missing fields; (5) report agreement/KL per cell, bits, model alias, input shas. kid line_ceiling 120."
thought_session: iter-TMM.138
title: A matched, fully-fresh key-only grid (fixed post-RoPE per-layer capture) preserves the Qwen2.5/Qwen3 boundary
town: local-maxxing
---
# hypothesis:lm-qk-norm-matched-fresh-key-only-grid

# hypothesis:lm-qk-norm-matched-fresh-key-only-grid

## Measured
- hypothesis:lm-qk-norm-model-moves-the-key-wall THOUGHT (gen25/OSC.21): Qwen2.5 key-only holds the 0.98 agree / 0.02 KL bar from 7.75 bits (9.0: 0.997559/0.000024; 10.75: 1.0/0.0); Qwen3 key-only never holds through 10.75 bits (0.895996/0.500741) or 3.5 bits (0.056885/7.740288).
- experiment:a00-31ae16be-c0ddf6:17,31,34,37-40 -- verdict pending; Qwen3 key-only cells are real but the matching Qwen2.5 key-only cell and BOTH models' uniform/random controls never completed (journalctl-confirmed 6.2GB OOM kill after loading a second model in the same process).
- experiment:a00-bcb6c85e-6b612b:68,73,76 -- the "corrected" sweep measures head_var(qq,kk) query-key interaction energy, not key-only energy, by its own Caveats field; its uniform control sits at 3.125 bits, not the required 3.5.
- experiment:a00-6c491245-bd570f:14,47,56,59 -- 125 production lines, over its own 120-line ceiling; discloses a pre-RoPE capture + layer-0-broadcast defect (repeats layer-0 priors across layers instead of a true per-layer profile).
- experiment:a00-edd08f38-e48bfb Director correction -- the Qwen3 profile_pooled 9.0-bit figure has no real allocator/sweep result behind it; it is inherited from the head_var experiment instead.
- Source: workflow.py run agi-research-review, run-key rr-data-work-agi-agi-worktrees-post-director-thought-lm-qk-norm-key-wall (2026-09-24, propose-only) -- review + verify both recommend demote on exactly these 5 gaps; verify refuted a 6th (a claimed 0-tests numpy failure -- the real recorded result is 2 passed).

## CLAIM
Running one self-contained key-only energy measurement -- fixed post-RoPE, per-layer capture (not layer-0 broadcast), one model per process with a memory check before each load -- for Qwen2.5 and Qwen3 at 3.5, 7.75, 9.0, and 10.75 bits, each width with matched uniform and random controls under identical allocator and control definitions, every one of the 8 primary cells measured fresh in this round (no cell inherited from a prior experiment), will show Qwen2.5 first holding the 0.98 agreement / 0.02 KL bar at 7.75 bits while Qwen3 remains below it through 10.75 bits, so the committed falsifier remains met. A pre-RoPE/layer-0-broadcast capture, if run at all, is a separately labeled control arm, never the measurement the verdict rests on.

## Dispatch line
config-max: the 4 bit-widths (3.5/7.75/9.0/10.75) and the model pair (paths.local_maxxing.osc03_hf_dir / paths.local_maxxing.osc15_hf_dir) move to the round's config cell, never hardcoded in the kid script / template-max: the allocator (key-only post-RoPE per-layer energy) and the control definitions (uniform, random, matched to the same representable widths) move to a template line, reused verbatim from the FIXED capture at osc_band_kquant_qknorm_a00-bcb6c85e.py:52-55,72-80, not re-derived / code: the missing resolver is a self-contained two-model, four-width, three-arm (key-only + uniform + random) sweep script that releases model A before loading model B and checks available memory before each load -- no such script exists yet; every prior round either mixed methods, inherited a cell, or stacked two models in one process.

## FALSIFIERS
Qwen2.5 fails to hold the 0.98/0.02 bar by 7.75 bits, OR Qwen3 holds it at or before 10.75 bits, OR any of the 8 primary cells (4 widths x 2 models, each with key-only + matched uniform + matched random) is missing, inherited from a prior experiment or node, or captured with a pre-RoPE/layer-0-broadcast method instead of the fixed post-RoPE per-layer capture.

## TESTS
Run the committed regression at .agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e_test.py unmodified first, as a sanity check on the reused capture mechanism (last confirmed result: 2 passed). Add ONE new committed test asserting the new sweep's results.json contains all 8 primary cells (2 models x 4 widths), each with key_only, uniform, and random values present and non-null.

## FILE SCOPE
.agi/context/local-maxxing/osc/ (repo-tracked) and a fresh dated dir under datasets/osc-band/ only -- no router changes, no engine edits, NO new downloads (both models already resident: paths.local_maxxing.osc03_hf_dir, paths.local_maxxing.osc15_hf_dir).

## CEILING
kids: <=120 production lines, ONE kid. pi parent. $0 expected (CPU-only); <=1 USD hard ceiling if GPU compute is required; no live provider spend without a fresh owner yes; no new downloads.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-thought (gen 26) as hypothesis (1) from the agi-research-review brainstorm stage's proposed_hypotheses[0] ("A matched pre-RoPE layer-0 key-only grid preserves the Qwen2.5/Qwen3 boundary"), refined per thought-master's TMM.138: added the required matched uniform+random controls at every width (the brainstorm's proposal only named the key-only arm), specified the FIXED post-RoPE per-layer capture as the primary method (demoting the brainstorm's literal "pre-RoPE layer-0" wording to, at most, a labeled control arm, since that wording names exactly the flaw disclosed in experiment:a00-6c491245-bd570f), and added one-model-per-process + a pre-load memory check as an explicit operational requirement (the mechanism behind experiment:a00-31ae16be-c0ddf6's OOM). Brainstorm's hypotheses (2) and (3) stay proposed only, per TMM.138 -- not minted this round.
<!-- THOUGHT:END -->
