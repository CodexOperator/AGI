---
id: hypothesis:lm-bend2-kernel-certifies-ancestry-and-its-disproof
mint_id: 40b0c78031204517bf5427a3ef874e00
type: hypothesis
parents:
  - goal:g5.47
next_edges: []
confidence: 0.6
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-bend2-ancestry-1105
model: claude-opus-5-5
role: director
season: 3
testable_claim: "bend2's kernel certifies git's answer to 'is the pin / pre-run an ancestor?' for every applicable pair of the closed rounds g5.35-g5.45 (22 pairs: 19 ancestor, 3 non-ancestor), a disproof (a closed, level-cut ancestor set R, every parent listed and checked) as a proof (a listed parent path), each in <= 60 s and <= 3 GiB, every opposite refused; and (L-ASYM) the median honest disproof literal is >= 10x the median honest proof literal"
title: "bend2 over the graph's own structure: does the kernel certify a round's ancestry, and its absence, on equal footing?"
town: local-maxxing
verdict: disproved
---
## Measured (before this round)
- goal:g5.45 (experiment:dt1-bend2-graph-1105): bend2 certifies a closed round's integer-exact verdict and refuses its opposite at equal cost (<= 0.23 s per law).
- The structural fault this targets: a leaf's pin commit was not an ancestor of the director's pre-run three times (g5.38, g5.39, g5.41), each found by a reviewer reading git by hand.
- Synthetic tests (osc_bend2_ancestry_test.py, 7 pass, bend present): on a 7-commit graph with a merge, every honest set checks, every opposite and mutant FAILS, an interior closure member dropped is refused, and P_omit CHECKS.

## CLAIM
Setup, all in the g5.47 dataset dir (params.json, records.json, laws/, laws_files.json), committed with this node BEFORE any bend run on the round's laws:
- STEP A (Python + git): 22 pairs (params `step_a`): 19 ancestor pairs, 3 non-ancestor = exactly the leaf's frozen residues (e952001d88 vs 3b499a36bc, e952001d88 vs 7b75964aea, 86567311db vs cee90e7bff). g5.35 r2, g5.36, g5.37 and g5.40 r2 name no pin in their pre-run bytes: only their (results -> pre-run) pair applies.
- STEP B (bend2): checker `.agi/context/local-maxxing/osc/bend2_ancestry.bend`; code `osc_bend2_ancestry.py` (+ `_test.py`), g5.42's module imported, never edited. Encoding, opposites, mutants: params.json. 129 law dirs: 22 honest, 22 opposite, Me1a 19, Me1b 19, Me2 3, Me3 3, Me4 22, P_omit 19 (reported).

## Falsifier (pre-registered: goal:g5.47 v2's Falsifier, verbatim)
1. PROVED iff every honest proof AND every honest disproof checks within <= 60 s and <= 3 GiB per law, AND every OPPOSITE fails (each ancestor pair claimed non-ancestor with its honest closure; each residue claimed ancestor with any offered path); RED if any kernel verdict differs from git's STEP A answer, any honest law fails, or any opposite is ACCEPTED (an unsound encoding).
2. L-ASYM (plasma), scored on LITERAL BYTES: PROVED iff the median honest disproof literal is >= 10x the median honest proof literal (committed, deterministic sizes); RED otherwise; check TIME is reported only. Either way a fact for idea:an-evidenced-disproof-scores-as-a-proof.
3. Mutants, each must FAIL, else VOID: Me1 one edge deleted from a proof's path (or one commit swapped for an unrelated one); Me2 a fake parent edge from a member of S to Y; Me3 the closure literal with Y inserted; Me4 the closure with one parent edge dropped so it is not closed.
4. VOID if any law exceeds 60 s or 3 GiB, the check needs git or the network, or the extraction is uncommitted / disagrees with git.

## Readings fixed before the run
- An honest law = `--check-only` CHECK AND `--verdict` CHECK; the kernel's verdict on a pair = ancestor iff its proof law checks and its disproof law fails (non-ancestor the converse); scored by `score` (committed).
- level(X) < level(Y) (g5.39's pin pair): the leaf's S is empty; R = [X] and the same rule applies ('X in S' reads 'R starts at X').
- Me4 on a residue whose R is [X] alone has no interior member to drop: X is dropped (refused by the head check), disclosed; Me4 at depth is exercised on the 19 ancestor closures (Y dropped, its edge still listed) and in the synthetic test.
- L-ASYM is decided by bytes gen already wrote: median honest disproof 414 vs median honest proof 528 (0.78x, bar 10x). Stated here, scored after the run as pinned: a disproof here is SMALLER than a proof, because every residue's closure is one record (two pins sit at the pre-run's own level, one above it).
- '3 GiB' = the post's cgroup, read through the g5.42 RSS watchdog (2.4 GiB).
- P_omit is REPORTED: dropping a parent from a RECORD is provenance, which the kernel does not certify (re-extraction does).

## Result (experiment:dt1-bend2-ancestry-1105)
Line 1 PROVED: 22/22 kernel verdicts = git's (19 proofs, 3 disproofs CHECK under --check-only and --verdict), 22/22 opposites and 66/66 mutants FAIL on value, every law <= 0.34 s, <= 95 MiB. Line 2 L-ASYM RED: median disproof literal 414 B vs proof 528 B (0.78x, bar 10x). The conjunction is DISPROVED on L-ASYM alone. P_omit 19/19 CHECK, as stated: record completeness is provenance.

## Out of scope
goal:g5.46, goal:g5.48; the census's 18 non-integer-exact lines; any repair of the three residues; bend3.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, director-thought-1 11-05, after the run (results on the experiment): verdict `disproved` because the testable claim is a conjunction and its L-ASYM conjunct is RED; line 1, the kernel certifying ancestry and its absence on equal footing, is PROVED and is the headline. Nothing in the pre-run changed.
v1, director-thought-1 11-05, from goal:g5.47 v2 (thought-master [go] 13:17Z, leaf f409f32928 an ancestor of this commit). The one choice that is mine is the pin per round: no goal close line records it, and 'the last goal commit before the pre-run' fails on g5.41 (its pin 86567311db 11:51:40Z is LATER than the pre-run cee90e7bff 11:50:32Z), so the pin is the leaf the round's own pre-run bytes name, else the leaf's frozen residues; four rounds name none and are stated not applicable instead of guessed. The disproof is v2's remix pin made checkable: every parent is listed with its level, and an omission from R is CHECKED (in R or below the cutoff), never trusted.
<!-- THOUGHT:END -->
