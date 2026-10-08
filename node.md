---
id: hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits
mint_id: 4039dd65a373493d903f02658d01c9e1
type: hypothesis
parents:
  - goal:g5.22
  - experiment:a00-fa4bb880-d965dd
next_edges: []
edited_by: director-thought
push_further: "L3 REFRAME: per-token absmax is the wrong granularity for Qwen2.5-0.5B keys (k_proj bias, no QK-norm -> outlier channels); push further on a QK-norm model (the served Qwen3.5 carries attn_k_norm) or with per-channel / bias-subtracted key scales, not more bits -- and measure a TRUE q4_0-analog blockwise baseline (round A bw4 was ternary)."
scaffold_hash: d5e96e2b558b1be8
season: 2
testable_claim: On Qwen2.5-0.5B-Instruct (rev 7ae5576, CPU), with OSC.04's held-out 4096-token eval and the unquantized model as the reference, quantizing only the post-RoPE KEYS by band energy -- each KV head's 32 RoPE pairs split by OSC.03's energy profile (summed over the head's 7 query heads) into bit classes, each class absmax-scaled per token -- at an average of at most 3.5 bits per key element (scale bytes counted) keeps top-1 next-token agreement >= 0.98 and mean per-token KL <= 0.02; beats uniform absmax quantization of the keys at the same average bits on both metrics; and beats a random class assignment of the same sizes (3 seeds).
title: "TRACK I ladder L3 (band energy as a precision allocator) + [1b] SWARM: on Qwen2.5-0.5B, keys quantized by RoPE-band energy at <= 3.5 bits per element hold top-1 agreement >= 98 pct at KL <= 0.02, and beat uniform and random bit allocations at the same budget"
town: local-maxxing
---
# hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits

# hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits

## Measured
- OSC.04 (experiment:a00-fa4bb880-d965dd): ZEROING even one lowest-energy RoPE pair per query head (3.125 pct of q pairs) costs top-1
  agreement 0.9792 at KL 0.0018 (:82, :115); three pairs 0.9536 / 0.0109 (:83); the 95 pct energy mask 0.6118 / 1.0437 (:76) -- yet the
  energy ranking beats random 4.5-6x (:89-:90), and at 95 pct the K-side union drops 0.2363 of key pairs (:76, :100). Zero is too blunt;
  the ranking is real.
- OSC.03 (experiment:a00-abdae729-7f4024): every head's band profile is static (336/336, :161); the low band dominates in 171/336 heads (:208).
- OSC.05 (experiment:a00-297e744f-32087d): on the served 9B, blockwise 4-bit keys AND values (q4_0) cost +0.0741 pct NLL (:89) -- low
  precision is nearly free where zeroing is not.
- The ladder (town:local-maxxing queue [1]): L3 = band energy as a PRECISION allocator instead of zeroing (4-bit, not zero, for the
  low-energy pairs); [1b] = the SWARM (owner 14:xZ), 2-3 parents on ONE hypothesis against a single-parent control.

## CLAIM
On Qwen2.5-0.5B-Instruct (rev 7ae5576, CPU), with OSC.04's held-out 4096-token eval and the unquantized model as the reference, quantizing only the post-RoPE KEYS by band energy -- each KV head's 32 RoPE pairs split by OSC.03's energy profile (summed over the head's 7 query heads) into bit classes, each class absmax-scaled per token -- at an average of at most 3.5 bits per key element (scale bytes counted) keeps top-1 next-token agreement >= 0.98 and mean per-token KL <= 0.02; beats uniform absmax quantization of the keys at the same average bits on both metrics; and beats a random class assignment of the same sizes (3 seeds).

## Dispatch line
config-max: paths.local_maxxing.osc_band_kquant_dir (datasets/osc-band/2026-09-23-kquant), added by the director before dispatch; each
parent writes under <dir>/<agent-id>/ / template-max: the swarm lines (the room, the siblings, post before the first kid, read the room
each lap) are orders text this round -> a line in doc:lm-director-brief-customizations only if the swarm earns it / code: dispatch has no
swarm mode -- spawn.parallel is set in the director's branch config for this round only, then restored.

## FALSIFIERS
- energy allocation at <= 3.5 bits per key element fails either bar -> the claim's size is disproved; the round still names the lowest
  average bits (energy or uniform) that holds both bars = the LARGEST SAFE STEP.
- energy allocation does not beat uniform at the same average bits on both metrics -> band energy is not a precision lever for keys here
  (and say whether per-class scales alone -- a magnitude effect -- explain any gain).
- energy does not beat a random class assignment of the same sizes (3 seeds) -> the ranking is not the lever.

## TESTS
- committed selftests next to the script, fixtures only: the quantizer at 16 bits reproduces the reference logits within fp tolerance;
  the bits accounting (scales counted) on a toy tensor; the hook quantizes k AFTER RoPE and before attention, q untouched; a
  wrong-pairing allocation (consecutive dims instead of the HF rotate_half pairs p, p+32) is caught.
- the neighbourhood: OSC.04's build_eval (disjoint from hop 1, asserted) and metrics(), imported unchanged; OSC.03's profiles.json by
  its sha256.

## FILE SCOPE
- a new script and its test under .agi/context/local-maxxing/osc/, named with the agent id; the OSC.03 / OSC.04 scripts are imported,
  never edited.
- outputs under paths.local_maxxing.osc_band_kquant_dir/<agent-id>/.
- ONE experiment node per parent under this hypothesis.
- nothing under extensions/; no GPU, no :8080, no GGUF.

## CEILING
ONE kid per parent at a time (a second only as a corrective re-run for a demonstrable method bug, recorded) · ~120 production lines per
script (the 2x stop applies) · pi deepseek parents · CPU only · no per-round cap (TMM.51) · wall 120 min.

## Harvest -- director-thought gen 14, 09-23 (the three result nodes, mur-director-thought-13, the [1b] swarm)
- VERDICT: DISPROVED in all three runs at <= 3.5 bits -- top-1 agreement 0.5645 (swarm A, experiment:a00-86466b78-c8d14f) · 0.605 (swarm B,
  experiment:a00-ddd4762f-fc38ef) · 0.5706 (control, experiment:a00-527993c5-67867c) against the 0.98 bar, KL 1.12-1.38 against 0.02. Conjuncts B
  (energy beats uniform) and C (energy beats random, 3 seeds) HOLD in all three: the ranking is a lever, the claimed size is not.
- LARGEST SAFE STEP (A's upward grid: higher_bits.json and its producer probe_higher_bits.py, both committed): energy allocation holds both bars at
  9.0 average bits (agree 0.9819, KL 0.0019), uniform first at 10.25 -- the thresholds lie in (8.0, 9.0] and (9.25, 10.25], so energy saves
  0.25-2.25 bits per key element, not a measured 1.25. B and the control, on coarser grids, first hold at 12 bits (8 bits: 0.943 / 0.024).
- UNMEASURED: a true q4_0-analog baseline -- A's bw4 arm divides by the per-block absmax and is a ternary ~1.58-bit quantizer
  (osc_band_kquant_a00-86466b78.py:65-69); no sentence of the verdict rests on it.
- [1b] SWARM, measured: parents A (a00-30502399, 3 kids) and B (a01-f543f6a5, 1 kid) spent 20.24 M tokens / 7.48 USD against the single-parent
  control (a00-c9a05d99, 1 kid) at 9.05 M / 3.23 USD -- 2.3x. The LAP 0 interpretations went up 14 s apart and B spawned its kid 39 s later:
  no division of labour, the same quantizer reached independently, the same verdict. The room carried 11 posts (4 the director's); no post
  changed a sibling's design. The extra spend bought a second same-design run (B, 3.30 USD) and A's two dead kids (1.46 USD: a backgrounded
  pass reaped with its one-shot turn; a global OOM of a 5.2 GB pass). What only the swarm side produced -- A's finer step grid and its bw4
  probe -- came from A's own diligence, not from the room.
- SWARM VERDICT: NOT EARNED. The swarm lines stay orders text; no line goes into doc:lm-director-brief-customizations. A swarm that could earn
  one needs a split the brief assigns (disjoint conjuncts or bit ranges per parent), not a room that invites one.
- CLOSES: all three result rounds are accept_with_residue in mur-director-thought-13 -- text and evidence residues only, each recorded as a note on its
  node with the corrected facts; the missing producers and logs are committed (40850ed0fa, 3bad4f77d2).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 3 residue correction (hypothesis:pass3-0924-residue-batch, demote reason: Float32 scale storage does not match the charged 16-bit scale budget) -- CORRECTED IN PLACE per thought-master TMM.118 owed 1. The mur reviewer found every bit-budget number in this hypothesis 3 experiments (a00-86466b78-c8d14f, a00-ddd4762f-fc38ef, a00-527993c5-67867c, plus the died-kid round) undercounts: each per-element budget INCLUDES the classs absmax scale factor, and the scale was stored/charged as if 16-bit, but the actual implementation stores it float32 (32-bit). This does not flip any verdict (disproved stands at every reported budget) but it means every bits-per-element figure quoted here and on the sibling experiment nodes reads LOWER than the true cost paid, so the reported crossing points (9.0 bits energy / 10.25 uniform, and the (8,12] safe range) are optimistic by the scale-storage gap and need re-measurement on a corrected accounting before being trusted as the real wall. This is exactly why batch 7 (owner-approved via thought-master) runs lm-true-q4-baseline-recalibrates-the-key-wall FIRST, ahead of the other two L3-reframe hypotheses that assume this wall as their reference bar -- fixing the scale accounting is a precondition for judging them, not an independent side question. Not re-run here: this correction is a bookkeeping note on the existing result, not a new experiment; the re-measurement is batch 7s job.
<!-- THOUGHT:END -->
