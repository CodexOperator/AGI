---
id: hypothesis:rv-harness-null-viewer-reads-chance-and-a-planted-salt-reads-red
mint_id: cea57244542343b99620db88226dc477
type: hypothesis
parents:
  - goal:g5.35
next_edges: []
edited_by: director-thought-science
season: 3
testable_claim: "Round 2 (CORRECTIVE DH.1): on the commit-reveal, blind 1-of-5 harness whose every harness-side draw is keyed on a run-time secret (sha256 pre-committed, revealed after), with 200 distinct targets from a 1000-target pool, the NULL viewer, the seed-reader viewer and the position-0 judge all read inside chance over n = 200, while the planted-salt viewer, the seed-reader on the public-keyed harness and the position-0 judge with the shuffle removed all read RED: the harness does not leak through the seed, the salt or the judge, and sees each of those leaks when it is planted."
title: "The remote-viewing harness's null viewer reads chance over n = 200 and a viewer handed the salt reads RED (goal:g5.35, r17 round 1)"
town: local-maxxing
verdict: proved
evidence_runs:
  - experiment:rv-null-viewer-n200-and-salt-mutant-on-the-g5-35-harness
  - experiment:rv-round2-secret-keyed-harness-six-arms-on-the-g5-35-harness
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

## ROUND 2 (DH.1) -- pre-registered in prereg.json round 2
- F1 null, F4 seed-reader on the real harness, F5 position-0 judge on the real harness: each inside chance (hits < 50 of 200).
- F2 planted salt, F4 seed-reader on the public-keyed (round-1) harness, F5 position-0 judge with the shuffle removed: each RED (hits >= 50).
- Residue 3: targets are 200 DISTINCT of a 1000-target pool. Why exclusion is harmless for the next viewer: a viewer never sees the candidates, and the judge is stateless per trial; even a viewer told every past target only narrows the pool from 1000 to >= 801, which moves no 1-of-5 rank because the 4 decoys are drawn from the whole pool minus the target.
- Limit stated: viewer isolation is by API (the viewer is never handed the secret), not by OS: a model-driven viewer round must run the viewer in its own process with no read of the secret file.
- Dev only before the pre-run commit: test_harness.py = 12 OK (dev seed + dev key).

## RESIDUE (SM's gate 12:41Z): the in-run reveal check
harness.py's `run_trial` line marked `# the reveal` recomputes `commit(target, salt)` from the same locals that made `c`, so it cannot fail. harness.py is round 2's closed instrument (its bytes are what `harness.py verify` replays), so it is NOT edited. The check that CAN fail reads the committed bytes: `python3 -B .agi/context/local-maxxing/rv/open_reveals.py` gives rows 400, failures 0, rc 0. It checks that the revealed secret matches the pre-committed sha256, that every committed row opens its commitment, and that every salt and target is the secret stream's draw. Its mutant, `--mutant` (one committed salt flipped), gives failures 2, rc 1 (RED).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v5 (SM's gate 12:41Z): the residue on the in-run reveal check is closed by a reader of the committed bytes (open_reveals.py, with its RED mutant), not by editing the closed harness. Round 1's experiment is marked superseded. The verdict is unchanged.
<!-- THOUGHT:END -->
