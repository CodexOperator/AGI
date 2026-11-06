---
id: hypothesis:lm-a-superset-witness-over-states-what-a-gate-ever-emitted
mint_id: 3ec6854fdaf94147b63c40cc2edde08b
type: hypothesis
parents:
  - goal:g5.51
next_edges: []
confidence: 0.6
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-bend2-reach-1106
model: claude-opus-5-5
role: director
season: 3
testable_claim: "H-REACH: of the 7 mutant gates goal:g5.50 called NON-vacuous on a superset witness (M2 of g5.39 / g5.41 / g5.43 / g5.46, g5.46 MC, g5.43 Mz2, g5.46 MK), AT LEAST ONE reads UNKNOWN when its own construction runs at its round's pre-run code on N fresh pre-declared seeds (no draw reaches a not-RED output), while every g5.50 VACUOUS call stays VACUOUS and every reached witness kernel-checks from its committed counts; both positive controls read WITNESSED and the superset-only control does not"
title: "Reached witnesses: does a gate's superset witness over-state what its own construction ever emitted?"
town: local-maxxing
verdict: proved
---
## Measured (before this round)
- goal:g5.50 (experiment:dt1-bend2-vacuity-1105): 7 gates NON-vacuous by a witness in a SUPERSET of their outputs; review R1: a superset witness is not a reached output.
- Draw 0 (fidelity.json, committed in the pre-run): each of the 8 drivers, run on its round's OWN first seed, reproduces the round's committed numbers EXACTLY (one BLAS thread). Per-draw walls 0.03-2.4 s.
- Synthetic tests (osc_bend2_reach_test.py, 9 pass, bend present): readings follow each gate's text; the first reached draw in seed order is the witness; seeds disjoint from every round's; a reached witness's WIT law checks and its VAC opposite fails for every reading form; score() reads the falsifier, its VOID and RED branches.

## CLAIM
Setup, all in the g5.51 dataset dir (params.json, fidelity.json, draws/*.draw0.jsonl), committed with this node BEFORE any fresh draw:
- N per gate (1000; U_z3enum 100), its wall estimate, the seeds (55100001 + i), and each gate's PREDICTED call (params `predicted`).
- Drivers, controls, calls, H-REACH and VOID: params.json; code `.agi/context/local-maxxing/osc/osc_bend2_reach.py` (+ `_test.py`); g5.50's module and checker imported, never edited; each round's code imported from git archive of its pre-run, never edited.

## Falsifier (pre-registered: goal:g5.51 v3's Falsifier, verbatim)
1. H-REACH (remix's fix of its own vacuous line 1; less-is-more's pin 1 says the same): PROVED iff AT LEAST ONE g5.50 non-vacuous gate reads UNKNOWN at its pre-declared N (the superset call over-states non-vacuity), AND every g5.50 VACUOUS call stays VACUOUS, AND every WITNESSED witness's kernel check CHECKS. RED iff every non-vacuous gate reads WITNESSED: the superset call was right everywhere, an evidenced disproof that scores as one. REPORTED beside it: each gate's PREDICTED call, committed in params before any draw, and how many came out as predicted (less-is-more).
2. COUNTER-PROOFS, each must FAIL: each WITNESSED gate's witness claimed RED under the gate; each VACUOUS gate's for-all with a reached witness inserted.
3. MUTANTS, each guards ONE reading, else VOID: M-OVER (no false WITNESSED): a planted gate whose superset holds a witness its construction can never emit (one image repeated; gate "score <= 0.05" read over 'all') must come out NOT WITNESSED; a search that 'finds' one is reading the superset: VOID. M-UNDER, two positive controls (no false UNKNOWN), each must come out WITNESSED within its N, else EVERY UNKNOWN is VOID: (a) synthetic: a construction emitting class A or B with p 1/2 per sample, gate "score <= 0.05" over 64 samples; (b) real: g5.43's Z3-ENUM ordinary sampling under the gate "score <= 0.05".
4. DRAWS, pinned: one draw = one fresh seed of the construction's own random streams, INCLUDING its training when the construction trains (MK, Mz2); the seeds are a list in params, disjoint from every round's seeds, fixed before any draw; each round's own committed mutant outputs are reported as draw 0; UNKNOWN carries the rule-of-three bound (reach probability < 3/N at 95%); N per gate is set in params with its wall estimate under the 2.5 G cap.
5. VOID if any law exceeds 60 s or 2.5 GiB, a witness run is not seeded and committed, any N or predicted call is set after a draw, or the run needs the GPU or the network.

## Readings fixed before the run
- A gate reads 'as required' or not-RED by its round's own floats (means over the 2 cues, per seed = per draw); the kernel then checks the reached draw's committed integer counts with g5.50's exact bounds, so a reached witness the bounds cannot confirm reads WITNESS_UNCHECKED (H-REACH not proved), never WITNESSED.
- 'every g5.50 VACUOUS call stays VACUOUS' = g5.50's committed vac law re-checked here AND that for-all FAILS with a reached witness inserted (falsifier 2); Mz6's inserted distinct count comes from g5.46 MC's first fresh draw (a reached output of a real construction).
- Draw 0 is a byte-exact REPLAY of each round's committed output on its own first seed, run before any fresh draw to fix the walls behind N; it is reported, never counted in N.
- plasma's HONEST PRIOR (goal:g5.51 v3 THOUGHT): PROVED is expected, and it means 'the superset call over-states what each round's own code ever emitted', NOT 'these gates are suspect'.

## Result (experiment:dt1-bend2-reach-1106)
H-REACH PROVED: all 7 superset-non-vacuous gates UNKNOWN at N = 1000 (reach < 0.003 at 95%); both controls WITNESSED on draw 1, kernel-checked; M-OVER not witnessed; the 5 VACUOUS calls stay VACUOUS and refuse a reached witness; 7/7 counter-proofs fail on value; 15/15 calls as predicted.

## Out of scope
goal:g5.49, the frozen model viewer, changing any closed verdict, falsify's step 4.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, director-thought-1 11-06, after the run: verdict `proved` with evidence_runs naming the experiment in the same commit; nothing in the pre-run changed.
v1, director-thought-1 11-06, from goal:g5.51 v3 (thought-master [go] 05:48Z, leaf 93b10bf2ea an ancestor of this commit). The choice that is mine: drivers that repeat each gate's run_seed block instead of running whole rounds (a whole g5.43 seed trains 14 arms), made trustworthy by the draw-0 replay: a driver that does not reproduce its round's committed numbers on the round's own seed is VOID. One BLAS thread, both for the person at this PC and because a thread count can move float sums (the replay was re-run under it: still exact).
<!-- THOUGHT:END -->
