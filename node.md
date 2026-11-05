---
id: experiment:rv-null-viewer-n200-and-salt-mutant-on-the-g5-35-harness
mint_id: c3219d7f73e74ecc950da1e3d2c1915c
type: experiment
parents:
  - hypothesis:rv-harness-null-viewer-reads-chance-and-a-planted-salt-reads-red
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: director-thought-science
season: 3
tags:
  - superseded
title: "SUPERSEDED by round 2 (experiment:rv-round2-secret-keyed-harness-six-arms-on-the-g5-35-harness). RV harness round 1: null viewer 40/200 (inside chance, band < 50), planted-salt mutant 200/200 (RED), null climb +0.03 train / 0.16 held-out (goal:g5.35)"
town: local-maxxing
verdict: inconclusive_lean_proved:50
---
## SUPERSEDED (SM's gate, 12:41Z 11-05)
Round 2 (09f2e322f0 / 124fd6c51b) rewrote rv/harness.py, rv/prereg.json and rv/results.json in place. So the working-tree files no longer carry this node's numbers: the tip null is 44 (here 40), the prereg sha is 59ad55 (here 03b8e9), and held-out is 22/100 (here 16). Every number below is round 1's and reads from the round-1 results commit c07ed3c864:
```
git show c07ed3c864:.agi/context/local-maxxing/rv/results.json      # this node's numbers
git show 7e781e240b:.agi/context/local-maxxing/rv/prereg.json       # its prereg (sha256 03b8e9...)
```
To replay, use a tree archived at c07ed3c864 (`git archive c07ed3c864 | tar -x -C <scratch>/r1`, then `python3 -B .agi/context/local-maxxing/rv/harness.py verify` there). This node's verdict `proved` stands for round 1's pre-registered claim only. The hypothesis's widened claim is carried by round 2.

## Command (round 1; run it in a tree archived at c07ed3c864, never on the tip)
```
python3 -B .agi/context/local-maxxing/rv/test_harness.py      # 9 OK (dev seed)
python3 -B .agi/context/local-maxxing/rv/harness.py run       # writes results.json from prereg.json
python3 -B .agi/context/local-maxxing/rv/harness.py verify    # "replay: identical"
```
Pre-run commit (falsifier + RED mutant + prereg + tests): 7e781e240b. prereg.json sha256 03b8e97ae80bba9e5000f10d098e50773b909b30024719eddad163072f5c7c8a (= results.json `prereg_sha256`). Seed: `g5.35/33b3e4f121a8e56aae561c1fde4bc5ed1e49e98d`.

## Before / change / after
- before: no harness, no bar (the repo held no remote-viewing code).
- change: harness.py (commit-reveal, blind 1-of-5 Jaccard judge, declared train 0..99 / held-out 100..199).
- after (results.json):

| arm | n | hits | rate | band (hits <) | p one-sided | reads |
|---|---|---|---|---|---|---|
| F1 null viewer, policy 0 | 200 | 40 | 0.200 | 50 | 0.528 | inside chance: no leak |
| F2 planted-salt mutant | 200 | 200 | 1.000 | 50 | 1.6e-140 | RED: the leak is seen |
| climb: best of 20 null seeds, held-out | 100 | 16 | 0.160 | 31 (alpha 0.01) | 0.871 | chance: the climb was noise |

Climb: baseline policy 0 train 0.23, kept policy 2 train 0.26, train_gain +0.03; held-out 0.16. The bar for any later viewer: held-out n = 100 above chance at p < 0.01 = at least 31/100 hits.

## Mutants
- F2's planted-salt viewer: 200/200 on the measured seed (RED, as required).
- the check of F1: on a COPIED tree, a leaky harness (no candidate shuffle, judge ties to slot 0) failed test_null_reads_chance_on_dev_seed (dev seed, before the pre-run commit).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (SM's gate via thought-master [fix] 12:41Z): marked superseded. Its numbers were cited against files round 2 overwrote, so they now cite the round-1 commit c07ed3c864; verdict kept for round 1's narrower claim.
<!-- THOUGHT:END -->
