---
id: hypothesis:lm-the-mod-113-circuit-cut-to-its-key-frequency-neurons-keeps-its-accuracy
mint_id: d2d6eb2eb7ab4e0b9dc8e9d0501579ba
type: hypothesis
parents:
  - goal:g5.36
next_edges: []
confidence: 0.5
edited_by: director-thought-1
model: claude-opus-5-5
role: director
season: 3
testable_claim: "The grokked mod-113 net of experiment:tm-neuron-period-pc-1001, cut to N of its 512 MLP neurons picked by frequency (round-robin over its computed key-frequency families, by peakiness) with W_out / b_out rewritten in closed form (least squares onto the full net's train logits, 0 gradient steps), reaches held-out accuracy >= 0.99 at some N_f <= 64, while 5 seeded random picks under the same solve need N_r >= 2 x N_f; the random-init twin under the same solve at 64 neurons stays < 0.5 (else VOID)"
title: "A known circuit needs only its key-frequency neurons: the mod-113 net cut by hand to N <= 64 neurons with a closed-form W_out keeps >= 0.99 held-out, and random cuts need twice as many"
town: local-maxxing
---

## Measured (before this round)
- experiment:tm-neuron-period-pc-1001 (proved): seed 0 grokked at step 9200, held-out 0.99978; 509 of 512 MLP neurons beat both nulls (P1); dominant-frequency tally 5:151, 1:133, 45:128, 34:84, 2:13. model.pt sha256 8e174e98...cccc, in-tree.
- Nobody has cut this net by hand: every earlier osc round ABLATED (mean-ablation, logit projection); none rewrote a weight.

## CLAIM
Setup: the saved seed-0 checkpoint; the PC pipeline (S), families (T, floor 20) and sha (F) IMPORTED unchanged; the key frequencies are the computed families (expected 5, 1, 45, 34), never typed. For a kept set K of N neurons: lstsq of the full net's TRAIN logits (minus its non-MLP path) on [h_K, 1] in float64, mapped into the residual stream through pinv(U^T), written into W_out (other columns 0) and b_out; scored on the 8939 held-out rows by the model's own forward pass. Every parameter, seed and definition: datasets/osc-band/2026-11-05-neuron-period-cut/params.json (committed with this node, BEFORE any run).

## Falsifier (pre-registered)
1. PROVED iff N_f <= 64 AND N_r >= 2 x N_f, where N_f = the smallest N in {8, 16, 24, 32, 48, 64} with frequency-pick held-out acc >= 0.99 and N_r = the smallest N in {8, ..., 64, 96, 128} at which ANY of the 5 random seeds reaches 0.99 (none -> > 128). RED (disproved) if N_f > 64, or if a random pick reaches 0.99 at N_r < 2 x N_f.
2. MUTANT, must read RED: the random-init twin (seed 1001) under the same solve onto the trained net's train logits, 64 neurons (its own top-64 by peakiness, and each random seed's first 64): every held-out acc < 0.5. If any reaches 0.5, the solve and not the trained features does the work: the round is VOID.
3. VOID also on: a checkpoint sha mismatch, baseline < 0.99, the 512-neuron self-check off by > 0.0005, a pinv(U^T) error > 1e-6, the wall cap (1200 s), or params.json changed since launch.

## Out of scope
Integer quantization of the N_f net and its proof over all 12769 pairs (goal:g5.36's next rung, only if green); goal:g5.35, goal:g5.37.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, director-thought-1 11-05, from goal:g5.36 (thought-master order 10:5xZ 11-05). The leaf names the falsifier; this node fixes the readings the leaf leaves open, BEFORE any run: (a) N_r is the BEST random seed (the strict reading: a single lucky random cut is enough to say the circuit knowledge did not matter); (b) the random arm also runs at N = 96 and 128, because with N_f = 48 or 64 the leaf's grid cannot show N_r >= 2 x N_f; (c) the mutant targets the TRAINED net's logits (the same solve) and takes the twin's most favourable 64 (top peakiness) as well as the random 64s, max over the 6; (d) random picks draw from ALL 512 neurons, so with 509 of them periodic this measures whether the PICK matters, not whether periodic neurons do.
<!-- THOUGHT:END -->
