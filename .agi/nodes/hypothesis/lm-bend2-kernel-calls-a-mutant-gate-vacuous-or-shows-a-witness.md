---
id: hypothesis:lm-bend2-kernel-calls-a-mutant-gate-vacuous-or-shows-a-witness
mint_id: e7a93fa7aeaf498b913d5d69949b9aaf
type: hypothesis
parents:
  - goal:g5.50
next_edges: []
confidence: 0.6
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-bend2-vacuity-1105
model: claude-opus-5-5
role: director
season: 3
testable_claim: Over each closed round's mutant gate g with its construction-implied output space O_g (its class computed by a committed rule from the cited code), bend2's kernel either proves g reads 'as required' for EVERY o in O_g (vacuous) or checks a witness o* in O_g where it does not (non-vacuous), and its call equals the review's on every gate the review called (g5.39 M1, g5.43 Mz1 vacuous; g5.43 Mz2, M2, g5.46 MK non-vacuous, MK by construction only); every opposite is refused; a planted tautology certifies vacuous and a planted strong gate yields a witness
title: "bend2 vacuity laws: does the kernel tell a mutant gate that could not fail from one that could, matching the review on every call?"
town: local-maxxing
verdict: proved
---
## Measured (before this round)
- Three vacuous mutants in this slice, each found at review: g5.39 M1, g5.43 Mz1, g5.46 MK's predecessor (a frozen latent on a deterministic decoder; goal:g5.50 Why).
- goal:g5.45 / goal:g5.47: bend2 proves small integer laws at ~0.2 s each and refuses planted lies on value.
- Synthetic tests (osc_bend2_vacuity_test.py, 6 pass, bend present): the rule reads m from code lines (R1-R4, R3 refused without a frozen call, an unmatched line refused); the integer score bounds hold on all 2145 outcomes (lo <= the true entropy score <= hi); at n = 8 every reading's VAC / EX / WIT laws read as wanted in bend.

## CLAIM
Setup, all in the g5.50 dataset dir (params.json, o_table.json, laws/, laws_files.json), committed with this node BEFORE any bend run on the round's laws:
- Falsifier 5: `osc_bend2_vacuity.py rule` computes every gate's O_g class from its draw line, call site and decoder line read at the round's pre-run (o_table.json); no class is assigned by hand.
- 12 gates (17 conjuncts) + 2 planted mutants; 42 law dirs; checker `.agi/context/local-maxxing/osc/bend2_vacuity.bend`; g5.42's module imported, never edited. Encoding: params.json.
- Python's call on every gate, stated before the run (laws_files.json python_ref): vacuous g5.39 M1, g5.41 M1-S, M1-C, g5.43 Mz1, Mz6, P_taut; non-vacuous g5.39 M2, g5.41 M2, g5.43 Mz2, M2, g5.46 MK, MC, M2, P_strong.

## Falsifier (pre-registered: goal:g5.50 v2's Falsifier, verbatim)
1. PROVED iff the kernel's call equals the review's measured call on EVERY gate where the review made one: vacuous for g5.39 M1 and g5.43 Mz1; NON-vacuous for g5.43 Mz2, M2, and g5.46 MK (by construction only: a witness in O_g; the law does NOT certify that MK's RED depends on W_z, which g5.46 review R2 measured false: RED at every W_z scale incl. 0) (plasma's condition: a known non-vacuous gate must be refused as vacuous, else a law form that proves every gate vacuous certifies nothing); RED if any differs.
2. COUNTER-PROOFS, each must FAIL: every vacuity proof's opposite (a claimed witness in its O_g), and every witness's opposite (a for-all proof).
3. RED MUTANTS, else VOID: a planted tautological gate ("valid count >= 0") must certify VACUOUS; a planted strong gate ("score <= 0.05" over ALL histograms) must yield a WITNESS.
4. VOID if any law exceeds 60 s or 3 GiB, needs the network at check time, or a gate's O_g has no file:line citation.
5. VOID if O_g's class (one-class vs all histograms) is not computed by a committed rule from the cited code BEFORE any law (m = distinct latent draws per cue on a deterministic path; m = 1 -> one-class); a hand assignment is VOID (less-is-more: the kernel's call is fixed by O_g's class, so a hand-assigned O_g makes PROVED near-guaranteed).

## Readings fixed before the run
- 'review's measured call': g5.39 M1 vacuous (g539_m1_residue.py + goal:g5.43's note), g5.43 Mz1 vacuous, Mz2 + M2 non-vacuous (goal:g5.43 close), g5.46 MK non-vacuous (goal:g5.46 close); the 'M2' of falsifier 1 is g5.43's.
- A per-cue histogram has TWO classes (g539_joint_samples.py:55: valid requires the cue's pair); the leaf's 4 x 65 one-class form is 129 outcomes here. Score is bounded exactly in integers (params `encoding`); the bounds decide every gate (asserted: no undecided reading).
- Gate per seed = the mean over 2 cues, on every seed: the for-all over cue pairs reduces exactly to an extreme over O_g; a witness is one seed's (o*, o*).
- falsifier 2's 'claimed witness' of a vacuous gate = O_g's outcome with the most valid samples; the EX law (some outcome of O_g breaks the gate) is a second opposite over ALL of O_g.
- Mz6 (cap 8 < 16 by construction: code mod 8 into a deterministic decoder) is reported, as are g5.39 M2, g5.41 M1-S / M1-C / M2, g5.46 MC / M2; out-of-form gates: params `scope`.

## Result (experiment:dt1-bend2-vacuity-1105)
PROVED on every line: kernel = review on 5/5 called gates; 20/20 opposites FAIL on value; P_taut vacuous, P_strong witness; <= 2.92 s (--verdict <= 4.37 s), <= 143 MiB. Reported: g5.41 M1-S, M1-C and g5.43 Mz6 VACUOUS (Mz6: cap 8 below its bar 16); g5.39 / g5.41 / g5.46 M2 and g5.46 MC non-vacuous.

## Out of scope
goal:g5.49; re-running any closed round; changing any closed verdict (a kernel call that differs from a review goes to the round's owner and sanctuary-master); bend3.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, director-thought-1 11-05, after the run: verdict `proved` with evidence_runs naming the experiment in the same commit (the v2 invariant); nothing in the pre-run changed.
v1, director-thought-1 11-05, from goal:g5.50 v2 (thought-master [go] 20:51Z, leaf f12d7eef64 an ancestor of this commit). The choices that are mine: (1) the rule's four patterns, written from the cited code BEFORE the law sets and run over every gate's three lines, so falsifier 5 reads a computed table; (2) score bounds instead of entropy (U32 has no log): exact on one-class outcomes (0) and tight enough that every gate is decided, which the gen stage asserts; (3) the two-class histogram (valid needs the cue's pair), which shrinks ALL from C(68,4) = 814,385 to 2145 so a for-all fits in seconds.
<!-- THOUGHT:END -->
