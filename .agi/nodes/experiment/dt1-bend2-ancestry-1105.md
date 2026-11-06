---
id: experiment:dt1-bend2-ancestry-1105
mint_id: 573a2eae600445de9336447b34bf827d
type: experiment
parents:
  - hypothesis:lm-bend2-kernel-certifies-ancestry-and-its-disproof
next_edges: []
confidence: 0.9
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-bend2-ancestry-1105
model: claude-opus-5-5
role: director
season: 3
title: "bend2 over commit ancestry: line 1 PROVED (22/22 pairs, the kernel's verdict = git's, 19 proofs and 3 disproofs CHECK, 22/22 opposites and 66/66 mutants refused on value, <= 0.34 s, <= 95 MiB); L-ASYM RED (median disproof literal 414 B vs proof 528 B, 0.78x, bar 10x)"
town: local-maxxing
verdict: disproved
---

## Experiment
**Question:** goal:g5.47 v2 (council lap 5, E3; thought-master [go] 13:17Z 11-05): git's answer to "is Y an ancestor of X?" for the closed rounds' (results -> pre-run) and (pre-run -> pin) pairs, as a bend2 LAW over commit records; a disproof (a closed, level-cut ancestor set, every parent listed with its level and checked) on equal footing with a proof (a listed parent path).
**Commits:** pre-run `57831d36ac` (leaf v2 f409f32928 and thought-master's tip aa58318f86 ancestors): hypothesis + Falsifier, params.json sha256 `83354174fc3c...`, records.json `8046ae8c1588...` (two extracts byte-identical), the 129 law dirs + laws_files.json `98189c452c80...`, checker `bend2_ancestry.bend`, code `osc_bend2_ancestry.py` + `_test.py` (7 pass, bend present); g5.42's module imported, never edited. Results: check.json `7bd6208c6891...`, verdict.json `b25dbc6a7dfb...` (scored by the committed `score`), check.stdout.
**Environment:** box local-town, CPU, ONE process; the g5.42 install reused (bend 2.0.39, Lean 4.34.0), no download; the RSS watchdog at 2.4 GiB. Whole check stage 34 s. 0 USD.

## STEP A (records.json; git + Python, before any law)
22 pairs from 13 closed rounds, n stated in the pre-run: 19 ancestor, 3 non-ancestor = exactly the frozen residues (e952001d88 vs 3b499a36bc g5.38; e952001d88 vs 7b75964aea g5.39; 86567311db vs cee90e7bff g5.41). Python's reachability over the records agrees with `git merge-base --is-ancestor` on 22/22 (asserted at extract). g5.35 r2, g5.36, g5.37 and g5.40 r2 name no pin in their pre-run bytes: no (pre-run -> pin) pair, stated. Residue shapes: g5.38's and g5.41's pins sit at the pre-run's OWN generation level (siblings; R = [X]); g5.39's pin is 8 levels ABOVE its pre-run (R = [X], every parent below the cutoff).

## Results (check.json, verdict.json)
- **Line 1 PROVED.** All 22 honest laws CHECK under --check-only AND --verdict (19 proofs, 3 disproofs); all 22 opposites FAIL (19 honest closures claimed non-ancestor: Y in R; 3 offered paths claimed ancestor: the last step is no listed edge); the kernel's verdict equals git's on 22/22. Every law <= 0.34 s, <= 95 MiB (caps 60 s, 2.4 GiB): no VOID.
- **Mutants 66/66 FAIL:** Me1a 19 (an edge deleted), Me1b 19 (a parent swapped), Me2 3 (a fake edge to Y), Me3 3 (Y inserted), Me4 22 (19 ancestor closures with Y dropped while its edge is still listed; 3 residues with X dropped). Every FAIL, all 88 with the opposites, is a refusal ON VALUE at the law's `{==}` (expected 0, observed 1), never a type error.
- **Line 2 L-ASYM RED:** median honest disproof literal 414 B (410 / 414 / 420) vs median honest proof 528 B (519 .. 1283): 0.78x, bar >= 10x. Time, reported only: proofs 0.22-0.23 s, disproofs 0.22-0.23 s.
- **Reported P_omit:** 19/19 CHECK, as stated pre-run: a record with a parent DELETED (not a member dropped from R) passes, because the kernel certifies the logic over the records, not their completeness against git. Provenance is extract's (records re-derived from `git rev-list --parents`) and a reviewer's re-extraction.

## Reading
On this graph a disproof is not dearer than a proof: every residue's non-ancestry is witnessed by ONE record (the pre-run and its parents, all below or at the pin's level), because the misses are near-misses in generation, siblings or a pin minted after the pre-run's line; a proof must walk its path. So L-ASYM's 10x premise (plasma: a disproof must enumerate a closure) fails here, and the leaf files it as a fact for idea:an-evidenced-disproof-scores-as-a-proof: certified disproofs of ancestry are cheap exactly when the level cut is tight. The kernel check itself is equal-cost (0.22 s each way) and sound on value for every planted lie, with completeness of a record's parent list as the one trusted input.

## Out of scope
goal:g5.46, goal:g5.48; repairing the residues; bend3.
