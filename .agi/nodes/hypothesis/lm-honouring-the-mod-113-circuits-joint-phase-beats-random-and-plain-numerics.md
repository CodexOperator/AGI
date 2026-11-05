---
id: hypothesis:lm-honouring-the-mod-113-circuits-joint-phase-beats-random-and-plain-numerics
mint_id: 87f9ebb96c81429eb2bcc81248836bd5
type: hypothesis
parents:
  - goal:g5.38
next_edges: []
confidence: 0.4
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-neuron-period-phase-1105
model: claude-opus-5-5
role: director
season: 3
testable_claim: "On the grokked mod-113 net of experiment:tm-neuron-period-pc-1001 under goal:g5.36's train-only closed-form solve (0 training): H1 a JOINT-PHASE pick (per family, greedy minimising max(R_sum, R_diff)) reaches 0.99 held-out at N_b <= 32 while random picks need N_r >= 2 x N_b; H2 a greedy OMP ceiling does NOT reach 0.99 below N_b; H3 WRITTEN neurons (m spread phases per key frequency, input weights by a linear probe) reach 0.99 at some N_w <= 32 where OMP does not; mutants M1-M4 must read RED"
title: "Inside the proved mod-113 circuit, does honouring JOINT phase beat random and plain numerics at N <= 32? A joint-phase pick (H1), an OMP ceiling (H2) and written 0-training neurons (H3), with mutants M1-M4"
town: local-maxxing
verdict: disproved
---

## Measured (before this round)
- experiment:dt1-neuron-period-cut-1105 (goal:g5.36, DISPROVED): the top-peakiness pick lost to random (0.815 vs >= 0.99 at N = 64); review: its picks share phase (R 0.897 k5, 0.892 k45 vs ~0.32 random at N = 32). 496 of 512 neurons sit in the four key families 5/1/45/34.
- model_s3.pt (datasets/osc-band/2026-10-01-neuron-period-seeds, sha256 04f96cc8...9021): memorized, not grokked (train 1.0, held-out 0.024).

## CLAIM
Setup: goal:g5.38's five arms, (a) random, (b) joint-phase pick, (c) OMP ceiling, (d) write-don't-pick, (e) model_s3.pt census, on the seed-0 PC checkpoint with g5.36's solve and scoring IMPORTED unchanged (osc_neuron_period_cut.py). N in {8, 16, 24, 32}; random also 48, 64. Every definition, seed and threshold: datasets/osc-band/2026-11-05-neuron-period-phase/params.json, committed with this node BEFORE any run.

## Falsifier (pre-registered: goal:g5.38's Falsifier, the council's text, verbatim in substance, + the council pins of thought-master [amend] 11:14Z 11-05)
1. H1 (remix) PROVED iff (b) reaches 0.99 held-out at N_b <= 32 AND N_r >= 2 x N_b (N_r = the smallest N in {8..64} where ANY random seed reaches 0.99; none -> > 64); else RED.
2. H2 (remix): RED iff (c) reaches 0.99 at a grid step below N_b: circuit knowledge picks worse than plain numerics, a disproof in its own right. PIN (3): if (b) never reaches 0.99 at N <= 32, N_b := '>32' and H2 is RED iff (c) reaches 0.99 at any N <= 32; if neither does, H2 is reported with no verdict.
3. H3 (less-is-more) PROVED iff some N_w <= 32 reaches >= 0.99 held-out AND (c) at that same N stays < 0.99; RED otherwise. PIN (1): the m-point phase set of arm (d) is the rank-1 lattice (phi_j, psi_j) = (2 pi j/m, 2 pi (j g mod m)/m), j = 0..m-1, g = the integer coprime to m nearest m/1.618 (m 2/4/6/8 -> g 1/3/5/5).
4. Mutants, each must read RED, else the named claim is VOID: M1 phase-twin (same n_k, greedy MAXIMISING R_sum) stays < 0.99 at every N <= 32 (else H1's mechanism is VOID); M2 the init twin (seed 1001) < 0.5 for every pick, PIN (2): picks (a)-(c) only (else H1 and H2 are VOID); M3 equal-phase write (phi_j = psi_j = 0) at N_w = 32 stays < 0.5 (else H3 is VOID); M4 model_s3.pt: if (b) or (c) keeps >= 0.99 x its own train baseline at N <= 32, small cuts are not circuit evidence and H1 is VOID.
5. Reported, no claim: (d) on the random-init twin (it never voids H3). PIN (2), optional, unscored: (d) on model_s3.pt, dropped if (e) finds no families.
6. Run-level VOID (every claim): a checkpoint sha256 differs, the PC baseline < 0.99, g5.36's 512-neuron self-check off by > 0.0005, a pinv(U^T) error > 1e-6, the wall cap (1200 s), or params.json changed since launch.

## Result
DISPROVED by experiment:dt1-neuron-period-phase-1105, every mutant RED, no claim void: H1 RED (joint 0.304 at 32, N_r = 64), H2 RED (OMP 0.998 at N_c = 24 < N_b '>32'), H3 RED (write 0.664 at 32). R_diff stays ~1 under every pick (a symmetric net: phi_a ~ phi_b), so the max(R_sum, R_diff) objective cannot spread phase here.

## Out of scope
goal:g5.39, goal:g5.40; integer quantization + bend2 of the cut net (cancelled with g5.36's RED; revisit only if H1 or H3 is green); a diluted 1024-neuron grokked + memorized pool.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, director-thought-1 11-05: verdict disproved + evidence_runs + the Result section from experiment:dt1-neuron-period-phase-1105 (results.json sha256 061670de...). CLAIM and Falsifier are the v1 pre-registration of 3b499a36bc, NOT edited. v1's fixed readings, carried: phases from fft2 over all inputs; R_sum / R_diff within a family; per-family greedies with largest-remainder n_k; OMP from all 512 on the solve's own target; the write probes the pre-activation from the residual at '='; M2 = (a)-(c) sets on the twin + the twin's own OMP; M4 reads (b) only with families. The near miss: reading (b) "within a family" is where R_diff turned out to be ~1 for EVERY pick; a cross-family or sum-only reading would have given a different greedy, and was not pre-registered, so it is named as the untested neighbour, not run.
<!-- THOUGHT:END -->
