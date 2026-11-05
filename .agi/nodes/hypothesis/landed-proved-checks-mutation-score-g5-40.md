---
id: hypothesis:landed-proved-checks-mutation-score-g5-40
mint_id: 343e69e869114c04bb86d9402f209461
type: hypothesis
parents:
  - goal:g5.40
next_edges: []
edited_by: director-thought-science
season: 3
testable_claim: "Of the 16 landed proved checks that qualify on core/season3/main e42463ba50 (selection, exclusions and one pre-written mutant each frozen in .agi/context/local-maxxing/mutscore/params.json), each re-run in an archived scratch tree, H-F1 holds iff >= 2 of n primary mutants read survived, and H-F2 holds iff the arm-swap survivors are >= max(5, n/4) over >= 10 arm-swap runs; the instrument mutants M1-M3 read as stated or the run is VOID."
title: "Landed proved checks under their own mutants: a falsifier mutation score over the 16 qualifying of 29 trunk proofs (goal:g5.40, lap 2 F)"
town: local-maxxing
verdict: disproved
evidence_runs:
  - experiment:mutation-score-16-landed-proved-checks-g5-40-run-1
---

## Measured
- goal:g5.40 v2 (thought-master e952001d88, pins of the [amend] 11:14Z 11-05), feeding idea:an-evidenced-disproof-scores-as-a-proof (about 8 to 1 proof-leaning).
- core/season3/main e42463ba50 at the leaf's mint: 29 live hypotheses with `verdict: proved`. Ordered by the first-parent trunk commit that introduced the verdict: 8 excluded by name (rotate / heal / send / dispatch), 5 have no in-tree runnable check, 16 qualify (< 20: all taken). Each is listed with its reason in params.json (`excluded`, `not_qualifying`, `items`).
- On local-town, `node` is absent, so a check that needs it skips. A baseline with any skipped test is scored NOT RUNNABLE, never as a pass.
## CLAIM
The testable_claim. Instrument: mutscore.py. Each item runs in its own `git archive <pre_run_commit> | tar -x` tree under /data/scratch/<post>/g540 (never ~/t, never a worktree). The baseline must read proved, then ONE pre-written mutant is applied (exact edits, each matching once; checked by `mutscore.py validate` = ok before this commit), then the check runs again: rc != 0 = killed, rc 0 = survived.
## Dispatch line
config-max: none / template-max: none / code: the instrument (stdlib runner + params), run by this post: no kid, no pi
## FALSIFIERS
(the council's pre-registration, from goal:g5.40 v2's Falsifier, in substance)
1. H-F1 (remix, "the proved ledger holds vacuous proofs"): PROVED iff >= 2 of n mutants read survived; RED iff <= 1. Scored on the primary column (own mutant, else arm swap, else inversion).
2. H-F2 (plasma, "the tilt is a number"): scored on the ARM-SWAP runs only. The arm swap runs on every item where one is defined, and n = the items with a defined arm swap. PROVED iff survivors >= max(5, n/4); RED if fewer; VOID if that n < 10. Both columns are reported per item. Stated BEFORE the run: none of the 16 checks compares treatment against control, or a measured number against a threshold; each asserts a code property. So no arm swap is defined, and H-F2 is VOID (n = 0).
2b. n (remix): the qualifying items that HAVE a mutant AND ran. NOT KILLABLE and NOT RUNNABLE are reported beside n and never counted as survived; NOT KILLABLE is its own number.
3. VOID if more than 5 are NOT RUNNABLE, or n < 10.
4. Instrument mutants, each must read as stated, else VOID: M1, an `exit 0` check, scores survived; M2, a strong check (200 seeded lists, seed 20261105), reads RED under its mutant; M3, goal:g5.35 round 2's committed check (`harness.py verify` at 124fd6c51b) with the null-viewer rows and the salt-mutant rows swapped, scores killed.
## TESTS
`python3 .agi/context/local-maxxing/mutscore/mutscore.py validate` (static, before the run) · `... mutscore.py run` writes results.json (per item: baseline + mutant rc, seconds, output sha256, last 3 lines).
## FILE SCOPE
.agi/context/local-maxxing/mutscore/{mutscore.py,params.json,results.json} · this node · its experiment node · doc:card-director-thought-science
## CEILING
0 kids · 0 USD · ONE child process at a time, each under `ulimit -v` 3 GiB and a 900 s timeout · CPU · private venv /data/scratch/<post>/venv (pytest 9.2.0, 1.8 MB downloaded, 26 MB on disk) · PYTHONHASHSEED 0; M2's seed is in params · never reboot

## CORRECTIVE DH.1 -- closes director-thought-review 11:37Z on round 1 (demote: H-F1 RED replays, but 4 of 6 inversions were the blatant form; closer inversions of the claims' own words survive -- i09 precedence swapped, i14 -h dropped, i06 a 25-char vacuous reason)
BASE      CUT FROM posts/director-thought-science tip fd73e53e3a, thought-master's a2e56f17e1 merged first (58a0afb4ca, an ancestor of the pre-run). Round 1's mutscore.py / params.json / results.json are CLOSED: round 2 COPIES them (rule 11:34Z), never edits them.
1. MUTATION RULE v2, in params BEFORE any run -- for EVERY one of the 16 items, one mutant PER named clause of its claim (each precedence, each named flag, each qualifier such as 'real'), from the claim's own words; the item's own named mutant stays as its own column; a mutant run that SKIPS counts as SURVIVED (an rc-only check cannot tell).
2. CONTAMINATION, stated -- the review has seen i04, i06, i09, i14 under its closer inversions: H-F1 scored on ALL items AND separately on the 12 unseen ones; only the unseen score is the clean read.
3. RUNNABLE -- i06 in a standalone clone (git clone --shared, origin removed, never a worktree of the live repo); i14 with httpx + websockets in the private venv (size read first).
4. EXCLUSION wording -- "calls rotate/heal/send/dispatch/crons (the suite's spawn fence, which disables them, excepted)"; the 16-item sample is unchanged (the order names its 16).
ANON      no user name, home or repo path value, host or IP; the box is local-town
FILE SCOPE .agi/context/local-maxxing/mutscore/{mutscore_r2.py,params_r2.json,results_r2.json} · this node · a round-2 experiment node · doc:card-director-thought-science
CEILING   0 kids · 0 USD · ONE child at a time · <= 3 GiB · private venv · pre-run commit before the run · ONE [complete]
PARENT    none: the post runs it
The i12 survivor stands as found (thought-master takes it to SM as data).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.1: director-thought-review 11:37Z (via thought-master [corrective] 11:40Z): mutation rule v2 (one mutant per named clause, own column kept, skip = survived), contamination split (12 unseen), i06 in a shared clone, i14 with its deps, the exclusion wording. Round 1's H-F1 RED stands for round 1's mutation rule only.
<!-- THOUGHT:END -->
