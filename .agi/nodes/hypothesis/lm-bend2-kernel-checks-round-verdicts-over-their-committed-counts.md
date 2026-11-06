---
id: hypothesis:lm-bend2-kernel-checks-round-verdicts-over-their-committed-counts
mint_id: 3c022b7fd76e4a53a62308814e99f2a4
type: hypothesis
parents:
  - goal:g5.45
next_edges: []
confidence: 0.6
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-bend2-graph-1105
model: claude-opus-5-5
role: director
season: 3
testable_claim: "bend2's kernel certifies a closed round's pre-registered verdict as a LAW over its committed integer counts, a disproof exactly as a proof: STEP B's DISPROVED pair (g5.41) is stated in the same shape as the PROVED pair (g5.35 r2) within 2x lines and time and every flipped verdict is refused; STEP C's kernel verdict equals the committed verdict on every integer-exact falsifier line of g5.35-g5.42, every opposite verdict refused; MB and MC read as stated"
title: "bend2 over GRAPH claims: are the closed rounds' integer-exact verdicts (proofs AND disproofs) kernel-checked over their committed counts, each opposite verdict refused?"
town: local-maxxing
verdict: proved
---

## Measured (before this round)
- goal:g5.42 (experiment:dt1-bend2-law-1105): bend2 refuses a wrong LAW on value (STEP 0 parity mutant) but costs ~14 s per tape pair (bulk numeric certification does not fit).
- Integer representation, read from bend2's Base source (no run): a U32 is `U32{data: Word(32n)}`, a cons list of 32 Bools; add is a bit-serial ripple carry. Neither unary Nat nor a machine int.
- Synthetic tests (osc_bend2_graph_test.py, 15 pass): verdict laws over a few counts check in well under a second each.

## CLAIM
Setup, all in the g5.45 dataset dir (params.json, counts.json, census.json, laws_files.json), committed with this node BEFORE any bend run:
- STEP A census (Python, no bend): 11 of 29 falsifier lines of the closed rounds g5.35-g5.42 are INTEGER-EXACT (g5.43 is active: excluded). Rule: a line's committed verdict is the same for every truth value of its non-integer clauses; those clauses enter the LAW as quantified Bools (`for r: Bool`), so the kernel proves the verdict whatever they are.
- counts.json: extracted by a committed script from PINNED commits (git show), every source blob sha256 recorded; g5.35's band re-derived from its prereg by exact binomial arithmetic (= 50, the committed value).
- STEP B, STEP C, MB, MC: params.json; code `.agi/context/local-maxxing/osc/osc_bend2_graph.py` (+ `_test.py`), g5.42's module imported, never edited.

## Falsifier (pre-registered: goal:g5.45 v2's Falsifier, the council's text with its pins, verbatim)
1. STEP B RED if the DISPROVED pair cannot be stated in the same file shape as the PROVED pair within 2x its lines and 2x its check time, or if the checker ACCEPTS either flipped verdict (an unsound encoding).
2. STEP C RED if any line's kernel verdict differs from its committed verdict.json (the finding is then the rule text or the verdict, scored to whoever is wrong).
3. Mutants, each must read as stated, else VOID: MB (plasma) PER CLAUSE: each STEP B clause's count moved just across ITS OWN pre-registered threshold (cited from the source falsifier line, read from the round's prereg, never assumed) while the original verdict is still claimed must FAIL: g5.35 r2 F1 44 -> 50, F2 the salt count to the first value on the wrong side of g5.35's own F2 threshold; g5.41 S-MECH 41 -> 252, S-OUT 10 -> 320 (four mutants). MC (less-is-more + remix) at the CLAUSE level: the law emits each conjunct's truth value; for g5.36 line 1 with the threshold N_f <= 64 moved to <= 128, the clause 'N_f <= threshold' must flip false -> true AND the line must STAY DISPROVED (N_r >= 2 x N_f is false); both are proved and each counter-proof fails. If STEP A lists g5.36's line as NOT integer-exact, MC moves to the first integer-exact SINGLE-threshold line in STEP A's list (picked by a committed Python rule before the run), whose threshold moved past its measured value must flip the LINE.
4. VOID if any one law exceeds 60 s (STEP C) / 1200 s (STEP B) or 3 GiB, or needs the network at check time, or a predicate cannot be traced to its pre-registered text.

## Readings fixed before the run
- MC as pinned (g5.36 line 1, the clause 'N_f <= threshold' moved 64 -> 128) is NOT FEASIBLE on committed integers: g5.36 committed N_f = null (its own text: none -> N_f > 64), and the 128 is a float accuracy on the extension grid. The pin's own fallback is taken: the first integer-exact SINGLE-comparison line in census order (rule `mc_pick`, committed) = g5.35 line 2, its band moved one past the measured 200 (to 201), which must flip the LINE (proved -> void).
- Gate lines (a mutant or VOID rule) read: as required -> proved, gate fails -> void. RED rules (g5.38 H2, g5.42 STEP 1) read: RED -> disproved, not RED -> proved, 'no verdict' -> void.
- '3 GiB' = the post's cgroup, read through the g5.42 RSS watchdog (2.4 GiB).

## Result
PROVED by experiment:dt1-bend2-graph-1105: 11 of 29 integer-exact; kernel verdict == committed on 11/11 (8 disproofs, 3 proofs), 22/22 opposite verdicts refused; STEP B same shape (32 vs 29 lines, 0.22 vs 0.23 s), 4/4 flips refused; MB 4/4 refused; MC (fallback) flips the line. STEP P (reported): 12.9 s per pair, projected 165,268 s: g5.42's readout LAW closes as an evidenced negative.

## Out of scope
goal:g5.43, goal:g5.44; changing any verdict, gate or counter; bend3.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, director-thought-1 11-05: verdict + evidence_runs + Result from experiment:dt1-bend2-graph-1105. CLAIM, Falsifier and the readings are v1's pre-registration (8bb44eae2f), NOT edited. v1's choice carried: integer-exact = invariant over every non-integer clause, checked by quantified Bools; it made 3 of g5.41's lines encodable as disproofs, which is the owner's ask (a disproof checked as hard as a proof). The MC fallback (disclosed pre-run) is the one deviation from the pins. The --verdict recheck is post-hoc and unscored.
<!-- THOUGHT:END -->
