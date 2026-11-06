---
id: experiment:dt1-bend2-vacuity-1105
mint_id: 6e7858fb30764b78939e1746871884e1
type: experiment
parents:
  - hypothesis:lm-bend2-kernel-calls-a-mutant-gate-vacuous-or-shows-a-witness
next_edges: []
confidence: 0.9
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-bend2-vacuity-1105
model: claude-opus-5-5
role: director
season: 3
title: "bend2 vacuity laws: PROVED. The kernel's call equals the review's on 5/5 called gates (g5.39 M1, g5.43 Mz1 vacuous; g5.43 Mz2, M2, g5.46 MK non-vacuous, MK by construction only); 20/20 opposites refused on value; both planted mutants read as stated; O_g classes computed by the committed rule; every law <= 2.92 s (--verdict <= 4.37 s), <= 143 MiB"
town: local-maxxing
verdict: proved
---

## Experiment
**Question:** goal:g5.50 v2 (council lap 6, K; thought-master [go] 20:51Z 11-05): per closed round's mutant gate, its construction-implied output space O_g from the cited code, and a bend2 LAW that it is VACUOUS (as required for every o in O_g) or NON-VACUOUS (a witness o* in O_g that breaks it).
**Commits:** pre-run `55e4e8eef2` (leaf v2 f12d7eef64 and thought-master's tip ancestors): hypothesis + Falsifier, params.json sha256 `4ec3e7b7a551...`, o_table.json `fedfd7885698...` (falsifier 5's rule over the cited lines at each round's pre-run), the 42 law dirs + laws_files.json `0cdbe94b3989...` (Python's call on every gate stated), checker `bend2_vacuity.bend`, code `osc_bend2_vacuity.py` + `_test.py` (6 pass, bend present); g5.42's module imported, never edited. Results: check.json `6f35d719c3b4...`, verdict.json `5f2a721d7af6...` (scored by the committed `score`), check.stdout.
**Environment:** box local-town, CPU, ONE process; the g5.42 install reused (bend 2.0.39, Lean 4.34.0), no download; the RSS watchdog at 2.4 GiB. Check stage 60 s in all. 0 USD.

## Falsifier 5 (o_table.json, before any law)
The rule (R1 `1 if <flag> else n` + the call's flag, R2 `% mod` + the call's mod=k, R4 explicit n draws, R3 no random token under a frozen / fixed call; a deterministic `> 0` decoder) gives: ONE-CLASS for g5.39 M1 (g539:122 + call :183 frozen=True), g5.41 M1-S (g541:206, no rng, call :266 frozen=True), g5.41 M1-C (g539:122 at g5.41's pre-run, call g541:260), g5.43 Mz1 (g543:85, call :155 fixed=True); CAP 8 for g5.43 Mz6 (g543:90, call :157 mod=8); ALL for Mz2 (call :153, no flag), MK (g546:108 size=(n), MC (g546:179), and every M2 (true lines and coin: n draws). No class was assigned by hand.

## Results (check.json, verdict.json)
- **Line 1 PROVED:** kernel = review on 5/5: g5.39 M1 vacuous, g5.43 Mz1 vacuous, g5.43 Mz2 / M2 / g5.46 MK non-vacuous (witnesses: valid 64/64 vs <= 0.1; true lines 0 valid vs >= 0.9; an even split 32/32 on both cues, score lower bound 0.5 vs <= 0.05). MK's call is by construction only: a witness in O_g, nothing about W_z (g5.46 R2).
- **Line 2 counter-proofs:** 20/20 FAIL, each on value at the law's `{==}`: 7 vacuous gates x (EX over all of O_g + the claimed witness), 8 non-vacuous x the for-all (VAC).
- **Line 3 planted:** P_taut (valid >= 0) certified VACUOUS; P_strong (score <= 0.05 over all) yields a WITNESS: not VOID.
- **Line 4:** every law <= 2.92 s check-only, <= 4.37 s --verdict, <= 143 MiB; no network; every O_g cited: not VOID.
- **REPORTED (never called by a review):** g5.41 M1-S and M1-C VACUOUS (as plasma's 13:13Z gate note on g5.41 said); g5.43 Mz6 VACUOUS: at most 8 distinct images per cue by construction, so 'distinct < 16' could not fail (it was kept as an instrument check of the counter, which it cannot test); g5.39 M2, g5.41 M2, g5.46 MC and M2 non-vacuous.

## Reading
The vacuity call is the construction's, made checkable: once the rule fixes O_g from the code, the kernel proves a frozen-draw gate could not fail and shows a witness for every other, and it refuses the opposite each time. Mz6 is the new fact: a fourth vacuous gate in this slice, an instrument mutant whose cap (8) sits below its own bar (16). Scope: O_g is a trusted premise read from the code (the rule's patterns cover these 12 gates' lines, not code in general), and a non-vacuous call says the gate COULD fail, not that it failed for the right reason.

## Out of scope
goal:g5.49; re-running a round; changing a closed verdict; bend3.
