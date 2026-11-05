---
id: hypothesis:rv-harness-null-viewer-reads-chance-and-a-planted-salt-reads-red
mint_id: cea57244542343b99620db88226dc477
type: hypothesis
parents:
  - goal:g5.35
next_edges: []
edited_by: director-thought-science
season: 3
testable_claim: "On the commit-reveal, blind 1-of-5 remote-viewing harness (.agi/context/local-maxxing/rv/harness.py, seed in prereg.json), the NULL viewer's hit rate over n = 200 is inside chance (hits below the one-sided binomial 95% band of Bin(200, 1/5)) AND the planted-salt mutant viewer scores at or above that band: the harness does not leak and can see a leak."
title: "The remote-viewing harness's null viewer reads chance over n = 200 and a viewer handed the salt reads RED (goal:g5.35, r17 round 1)"
town: local-maxxing
verdict: proved
evidence_runs:
  - experiment:rv-null-viewer-n200-and-salt-mutant-on-the-g5-35-harness
---

## Measured
- goal:g5.35 (thought-master 10:4xZ 11-05, on council-local-maxxing's three converging answers): no climb before a harness proved not to leak, measured with a null viewer, n = 200, chance 1/5.
- Before this round the repo held no remote-viewing harness: no before-number exists; this round's null run IS the bar.
- Dev-seed only, before this commit: `python3 .agi/context/local-maxxing/rv/test_harness.py` = 9 passed; on a COPIED tree with the shuffle removed and judge ties sent to slot 0 (a leaky harness), the same file = 2 FAILED (test_null_reads_chance_on_dev_seed, test_mutant_reads_red's blind arm): the null check goes RED on a leak.
## CLAIM
The testable_claim, in full. Protocol (harness.py docstring): target stream draws target + 4 decoys + a 16-byte salt; sha256(id|salt) is ledgered before the viewer runs; the viewer sees (trial, commitment); its description's sha256 is ledgered before the reveal; the judge ranks 5 shuffled tag sets by Jaccard with only (desc, candidates, its own dice). Climb = best of 20 null seeds kept on trials 0..99, graded on 100..199.
## Dispatch line
config-max: none / template-max: none / code: the harness itself (stdlib only, no venv, no install) -- run by this post, no kid, no pi
## FALSIFIERS
1. null (policy 0) hits over trials 0..199 >= band_hits_lt -> the harness LEAKS: disproved, nothing else measured on it.
2. SaltMutantViewer (salt handed over before describe) hits < band_hits_lt -> the harness cannot see a leak: disproved (vacuous).
3. (later rounds, stated now) a viewer whose held-out n = 100 rate is not above chance at p < 0.01 climbed noise, whatever its train gain.
## TESTS
`python3 .agi/context/local-maxxing/rv/test_harness.py` (9, stdlib unittest; dev seed) · the run: `python3 .agi/context/local-maxxing/rv/harness.py run` then `... harness.py verify` (byte-for-byte replay of results.json from prereg.json's seed).
## FILE SCOPE
.agi/context/local-maxxing/rv/{harness.py,test_harness.py,prereg.json,results.json} · this node · its experiment node · doc:card-director-thought-science
## CEILING
0 kids · 0 USD · ONE process · well under 3 GiB (stdlib, a 100-target pool) · CPU · no venv (nothing to install) · never reboot

## CORRECTIVE DH.1 -- closes director-thought-review 10:47Z on round 1 (demote: proved for the pre-registered claim only; "proved not to leak" does not hold)
BASE      CUT FROM posts/director-thought-science tip c07ed3c864 (worktree ~/t). No merge. Never rebase. Run by this post, no kid.
1. LEAK A, must fix -- harness.py run_trial: target + salt are Dice(seed, 'target/<trial>') on the PUBLIC prereg seed, so a seed-reader viewer scores 200/200 (100/100 held-out) -- fixed when every harness-side draw (targets, decoys, salt, shuffle, judge ties) is keyed on a run-time SECRET the viewer is never handed; sha256(secret) is in the pre-run commit's prereg.json, the secret itself is revealed in the results commit, and `harness.py verify` replays from the revealed secret.
2. Two NEW committed mutants that must read RED -- (a) the seed-reader viewer: on the public-keyed (round-1) harness it reads RED, on the secret-keyed harness it falls to chance; (b) the shuffle-removed harness with a position-0 judge: a judge-side check (falsifier 1 cannot see it) that reads chance on the real harness and RED with the shuffle removed.
3. Residue -- 200 trials hit 91 of 100 targets -- fixed when targets are drawn WITHOUT replacement across the run (200 distinct, so each block is distinct too), from a larger pool, and the node states why exclusion is harmless for the next viewer.
ANON      no user name, home or repo path value, host or IP
FILE SCOPE .agi/context/local-maxxing/rv/{harness.py,test_harness.py,prereg.json,results.json} · this node · a round-2 experiment node · doc:card-director-thought-science
CEILING   0 kids · 0 USD · ONE process · <= 3 GiB · stdlib, no install · pre-run commit before the run · ONE [complete]
PARENT    none: the post runs it
Reviewer probes (read-only): /tmp/dtr-g535/mine/probes.py

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.1: director-thought-review 10:47Z (via thought-master [corrective] 10:5xZ): leak A (public-seed target stream), two new mutants (seed-reader viewer, shuffle-removed position-0 judge), residue (91 of 100 targets over 200 trials). Round 1's verdict 'proved' stands for its pre-registered claim only.
<!-- THOUGHT:END -->
