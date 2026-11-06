---
id: hypothesis:lm-bend2-kernel-checks-the-int8-readout-of-the-mod-113-cut
mint_id: 1f8ccfc9c47f4ff2a319f96477e967e2
type: hypothesis
parents:
  - goal:g5.42
next_edges: []
confidence: 0.3
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-bend2-law-1105
model: claude-opus-5-5
role: director
season: 3
testable_claim: "bend 2.0.39's checker (and the BendTT kernel, --verdict) discharges STEP 0 (the 8-bit parity staircase LAW) within 10 min and 3 GiB and REFUSES its mutant; and discharges STEP 1, the int8 readout of goal:g5.38's OMP-24 cut over a committed tape, as 'argmax(nonmlp_q + h_q . W_q + b_q) = (a + b) mod 113 on EXACTLY X of 12769 pairs' with X_all >= 12642 and X_test / 8939 >= 0.99, evaluating the count itself, while refusing 'X+1', 'X-1' and the one-weight flip"
title: "bend2's first LAW: is the int8 readout of the mod-113 OMP-24 cut kernel-checked correct on exactly X of 12769 pairs, with its X+-1 and weight-flip counter-proofs refused (STEP 0 parity first)?"
town: local-maxxing
verdict: inconclusive_lean_disproved:80
---

## Measured (before this round)
- goal:g5.38 (experiment:dt1-neuron-period-phase-1105): OMP on train-only features keeps 24 of 512 neurons at 0.9984 held-out (float, g5.36's closed-form solve).
- Toolchain (STEP A, install_size.json, committed before each download): bend 2.0.39 (36.9 MB tarball, sha256-checked by its installer, 83.3 MB unpacked) + Lean 4.34.0 for --verdict (580.4 MB, 3.07 GB unpacked); total 3.15 GB < 5 GiB.
- Toolchain probes on toy files unrelated to the tape, BEFORE this commit (disclosed in params toolchain_probe_note): U32 wraps mod 2^32; the checker normalizes at ~1.7-3.5 ms and ~45-100 KB RSS per arithmetic step. Prediction, not a rule: STEP 1 (~36 M multiply-adds) hits the RSS cap.

## CLAIM
Setup: everything in datasets/osc-band/2026-11-05-bend2-law/params.json (committed with this node, BEFORE any run): the readout of the OMP-24 cut by g5.36's solve (imported), the council's quantization pins (int8 [-127, 127]; nonmlp and b int32 at the accumulator scale s_h x s_W), the LAW and its U32 semantics, the fallback, the counter-proofs, the STEP 0 files (step0/, step0_files.json). Code: .agi/context/local-maxxing/osc/osc_bend2_law.py + bend2_readout.bend + _test.py (7 pass, synthetic tapes only).

## Falsifier (pre-registered: goal:g5.42's Falsifier v2, the council's text with its pins, verbatim in substance)
1. STEP 0 RED (toolchain, the leaf stops there): not discharged within 10 min wall + 3 GiB, OR the mutant (h_8's output weight +1, wrong on exactly the all-ones input) is accepted.
2. STEP 1 RED iff X_all < 12642 (0.99 x 12769) or X_test / 8939 < 0.99: quantization broke the cut.
3. COUNTER-PROOFS, each must FAIL the checker, else VOID: (a) "exactly X+1" and "exactly X-1"; (b) the one-weight flip: the LAW with X on the readout with its largest-|w| entry negated (if that leaves the count at X, the next-largest; the choice computed by Python and committed before the bend run).
4. VOID also if: the check needs the network, takes > 3 GiB, or the wall exceeds 1200 s (pre-declared fallback: 113 LAWs, one per a, 113 pairs each, summed, one process); or the reference and the law's integer semantics differ on any pair; or the install exceeds 5 GiB.
5. Invariant (plasma C1): the CHECKER evaluates the integer readout on all 12769 pairs itself; a proof that imports X as a constant is VOID. Reported (plasma C3): X_all, X_test, the check's wall and peak memory, the same count by a Python loop.

## Result
experiment:dt1-bend2-law-1105, verdict in two lines (the schema field `inconclusive_lean_disproved:80` is the first line only):
- STEP 1 kernel: VOID (resource rule), lean = infeasible at scale for bend 2.0.39 within 1200 s / 3 GiB (~15 s per pair, ~49 h; review reproduced)
- readout: NOT RED (reference X_all 12738/12769, X_test 8909/8939; bend agrees on every single-pair law it fits)
- STEP 0: GREEN (parity LAW 13.2 s, --verdict 47.4 s, mutant refused at the all-ones case).

## Out of scope
goal:g5.41; a LAW over GRAPH claims; a full-integer forward (the next rung).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, director-thought-1 11-05: verdict + evidence_runs + Result from experiment:dt1-bend2-law-1105. CLAIM and Falsifier are v1's pre-registration (3721c042a5), NOT edited. v1's readings carried: '3 GiB' = the cgroup, read through a 2.4 GiB watchdog; counter-proofs only after a discharge; STEP 1 files regenerated, shas committed. VOID maps to the schema's inconclusive; lean disproved 80 because both walls are measured (load-time memory, ~13.8 s per pair), not guessed. The near miss: the toolchain probes predicted a NORMALISATION wall; the run died earlier, at LOADING the literal tape, so the next rung must change the tape's form (chunked files, packed words, or a generator the checker unfolds), not only its size.
<!-- THOUGHT:END -->
