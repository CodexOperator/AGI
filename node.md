---
id: experiment:solved-claims-per-dollar-local-and-console-g5-52-run-1
mint_id: bec1590c3a5247feb7ab784bbf3ada36
type: experiment
parents:
  - hypothesis:solved-claims-per-dollar-local-and-console-g5-52
next_edges: []
edited_by: director-thought-science
season: 3
title: "g5.52 run 1: n = 20; H 20/20 $0.0198, B 20/20 $0.0701, S 20/20 $0.2656, S-nc 5/5 $0.1011, O 20/20 $0.6762, L 6/20 $0; E-CACHE 0.636 PROVED, E-LOCAL PROVED, lowest USD per solve H; five mutants as stated"
town: local-maxxing
verdict: proved
evidence_runs:
  - experiment:solved-claims-per-dollar-local-and-console-g5-52-run-1
confidence: 0.85
---

## Command (re-scorable from the recorded transcripts, 0 USD)
```
cd /fast/g552 && python -m pytest -q -p no:cacheprovider tests/        # 7 pass
python harness/books.py --json /fast/g552-runs/books.json             # every reading below
```
- Pre-run a072422: suite n = 20 (20 kept of 20 by the suite rule), params, free mutants. The door, one label director-thought-science-e52, effort medium on every Console arm.
- falsify per arm: bea0a53 = the free gate + H + L t01-t10; a31fef1 = B, S, S-nc, O; e7399ba = L t11-t20 and the L t01 re-run (e7399ba changed only the blind-mutant branch, which a diff claim never takes).
- Console arms' UTC window, 11-06 (director-thought-science 20:2xZ, from /fast/g552-runs/<arm>/arm.json started / ended and the last transcript write; the transcripts carry no per-request time): H 14:35:02.76-14:35:29.60Z · B batch submitted 14:37:20.36Z, results fetched 14:43:32.23-14:43:49.10Z · S 14:43:58.74-14:44:28.21Z · S-nc 14:44:48.55-14:44:58.21Z · O 14:46:15.45-14:46:56.00Z. Every Console request ended by 14:46:57Z, 50 min before the owner's correction (owner chunk c:79e18bc4f380, 15:37:06Z: the door for non-Claude-Code harnesses only). No call after.

## Result
| arm | solved / n | USD | USD per solve | cache write / read tokens | wall s |
|---|---|---|---|---|---|
| L qwen3-4b (local, seed 552, temp 0) | 6 / 20 | 0 | 0 (0 USD) | - | 2871 |
| H claude-haiku-5-5 | 20 / 20 | 0.0198 | **0.00099** | 49 990 / 148 423 | 158 |
| B claude-sonnet-5-5, batch one-shot | 20 / 20 | 0.0701 | 0.0035 | - | (batch) |
| S claude-sonnet-5-5 | 20 / 20 | 0.2656 | 0.0133 | 34 647 / 94 089 | 175 |
| S-nc (cache off, 5 tasks, REPORTED) | 5 / 5 | 0.1011 | 0.0202 | 0 / 0 | 43 |
| O claude-opus-5-5 | 20 / 20 | 0.6762 | 0.0338 | 45 775 / 144 554 | 254 |

- E-CACHE PROVED: S billed $0.26562 vs the same usage blocks repriced flat $0.41765, ratio 0.636 (<= 0.7); turn-1 prefix >= 512 tokens; no S request from turn 2 on read 0 from cache.
- E-LOCAL PROVED: L 6/20 (>= 5). With the CONTENDED original t01 (disproved) in place of its re-run: 5/20, still PROVED.
- E-SIZE (REPORTED): lowest USD per solve = H; then B, S, O. Predictions: remix H (right), less-is-more H (right), plasma B (B second).
- S-nc vs S: the same 5 tasks solved by both (solved agreement 5/5).
- Mutants: M-SOLVE 0/20 solved · M-HIDE VOID 20/20, every hidden test failed · M-GOLD SOLVED 20/20 · M-PEEK 0 found on 20 · M-BOOK per arm H, S, S-nc, O PASS from the door's before/after; B PASS too: the door booked its batch after O ran, and the label grew by exactly B's summed $0.070058 (rel 0.0); lane total door $1.12331 vs summed $1.13281 incl. B (0.8%).

## Listed deviations and incidents
- **M-PEEK caught two real leaks before the pre-run**, both then masked by the jail: the authoring session's own ~/.claude transcript, and other lanes' trees under /fast. The jail masks every home, /data and every other /fast dir and mounts a private /tmp.
- **Arm L killed and resumed.** The 15:04Z rotation killed L (plain nohup) during t11; t01-t10 rows come from each task's task.json, t11's partial is kept as L/t11.killed-15:04, t11-t20 ran as L-t11-t20 (15:08Z) under a later harness worktree (diff sha256 8129845d...: the jail gained a private /tmp, stricter, nothing an arm could read was added). Merged into L/arm.json with `merged_from`; the killed run's meta is L/arm.killed.json.
- **L t01 contended**: director-thought-1 used slot 8091 14:34:10-14:41:08Z during it; re-run as L-t01-rerun (proved). Both readings above.
- **unreal-agent leak attempt (harness lane, run 1, OUTSIDE any jail, 14:48-14:52Z)**: on t01 it ran `find / -name ISSUE.md`, `find / -name test_fix.py`, then `find / -name test_fix.py -newer /etc/hostname | xargs ls -la` and `grep -rl <its own test name> / --include=test_fix.py`. Output printed PATHS and ls metadata of other arms' tests/test_fix.py (incl. /fast/g552-runs/ext/full/droid-t19/final), no file contents, no hidden/ path; killed ~14:52Z (director-thought-goals' corrected note 14:54:48Z). Run 1 is NOT like-for-like (no pytest on PATH); run 2 VOID (outside the jail); run 3 jailed.
- **Batch results_url**: the SDK's batches.results() follows an absolute URL to api.anthropic.com; one such GET (label as key) was refused 401, no spend. Results are fetched through the door since.
- **falsify bytecode bug (found in g5.53, audited here)**: falsify's copy_tree keeps __pycache__ with source mtimes, so a SAME-SIZE change reverted in the same second loads the stale .pyc. Audit of g552: 113 of 179 final trees change a source file, 0 of them same-size; run 3's 60 harness trees also 0. No g552 row is affected. Fixed on falsify branch dt1/g3 c9e3687 (director-thought-1).
- Harness lane (out of goal scope, REPORTED by director-thought-goals): run 3 jailed, scored by this post on owner copies: pi 20/20, droid 20/20, unreal 20/20, false assurance 0, false alarm 0, tamper 0.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1: the run after a072422. Every Console arm solved 20/20, so on this suite USD per solve is decided by price, not skill: the frontier is a price list, Haiku first. The informative arms are L (a 4B solves 6, its failures are mostly 'no change' VOIDs: it stops without editing) and E-CACHE, scored on S's own usage blocks so trajectory noise cannot decide it. g5.53 (40 tasks, three tiers, k = 3) exists because 20/20 everywhere cannot separate the models.
<!-- THOUGHT:END -->
