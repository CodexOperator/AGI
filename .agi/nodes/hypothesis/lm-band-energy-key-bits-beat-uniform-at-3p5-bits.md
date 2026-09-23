---
id: hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits
mint_id: 4039dd65a373493d903f02658d01c9e1
type: hypothesis
parents:
  - goal:g5.22
  - experiment:a00-fa4bb880-d965dd
next_edges: []
edited_by: director-thought
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
