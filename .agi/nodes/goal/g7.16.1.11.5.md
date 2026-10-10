---
id: goal:g7.16.1.11.5
mint_id: 4b93433413834949b09316c9083ca166
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.5
goal_kind: subgoal
origin: owner
scaffold_hash: e977890a2a0c9afa
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.5: ROUND 5: the BOOTSTRAP config:engine <= 8,192 B (§Q zygote + the §R folds + agi-infer); expansions engine-post / engine-wrap may be larger; total <= 20,480 B"
town: core
---
# goal:g7.16.1.11.5

## Why this exists
Parent goal:g7.16.1.11: Round 5 on goal:g7.16.1.11 (c620220b4, b60af0b63): zygote 7,342 B, total 18,830 B; owner GO 06:1xZ.
## Target end-state
ROUND 5: the BOOTSTRAP config:engine <= 8,192 B (§Q zygote + the §R folds + agi-infer); expansions engine-post / engine-wrap may be larger; total <= 20,480 B. RULED R' (belam 10-10 08:4xZ, via SM): the 8,192 is the FENCED bytes (what boots), counted by one rule and asserted by engine-sizes b5; THOUGHT, headings and prose outside a fence are free. The 20,480 total clause is not asserted (the engine*.md files sum 82 KB).
## Invariants
every moved piece byte-exact vs v4c; parity rows unchanged.
## Falsifier
1. `sh extensions/agi/tests/engine-sizes.t.sh` exits 0 (its exit = the FAIL count) and prints `ok b5-the-fenced-bytes-are-within-the-bar` (the FENCED bytes of engine.md <= 8,192 by the ONE rule written in the lane header: the bytes of every line strictly between a ~~~ open and its close, newline included, fence lines excluded, LC_ALL=C), `ok b5-the-fences-balance` and `ok b5-measure-finds-the-fences`; engine-post + engine-wrap exist
2. negative: a v4c piece lost in the split: zero rows GONE in the Q.2 map
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"I just mean the 'bootstrap' package is under 8kb you get it?" (owner 05:38Z) · "Q is go" (06:1xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 10-10 09:0xZ. MEASURED on the trunk 74b212571e: engine.md = 9,913 B whole; FENCED = 8,191 BYTES (LC_ALL=C), 1 B under the 8,192 bar. My 08:4xZ draft said 8,099 and '93 B left': that was a CHARACTER count (ten lines inside the fences carry non-ASCII, 92 B); DG2 found it and the lane counts bytes. The F1 here was `wc -c < engine.md` (the whole file, 1,721 over); belam ruled R' (08:4xZ): the owner's 'the bootstrap package is under 8kb' is what boots = the fenced bytes. F1 is now DG2's lane 44d423b0e2 (engine-sizes b5: bar, balance, non-vacuity floors >= 8 fence lines / >= 4,000 B), RUN by me at the sha: 17 ok / 0 FAIL on the trunk; mutants: +100 B inside a fence -> bar RED (8,291); +100 B outside -> green; three ASCII chars swapped for 3-byte characters -> bar RED (8,197: a character count would pass); a closing fence removed -> balance + measure RED. THE MARGIN IS 1 B, so C1-C3 are owed (simplification, no HOLD): C1 THOUGHT blocks and prose are free under R' but the 710 B THOUGHT of engine.md is NOT in the fenced count, so C1 is dropped from the cut; C2 the 43 map descriptions (3,097 B fenced) to <= ~55 B a row; C3 fold the 519 B loop block into the diagram or the map. Report the fenced bytes before/after. C4 (agi-project's pi path to engine-wrap, -332 B, .12's BUDGET bullet) only if the margin is < 256 B after C2-C3, laned to DG3 under the HOLD.
director-general-1 10-10 09:1xZ: COMPLETE. C2+C3 (dg3-b5cut 77e920f67f, landed 592cb1e416) are on the trunk; F1 re-run by me on the merged tree 53a26cfe96: `sh extensions/agi/tests/engine-sizes.t.sh` 0 FAIL, b5-the-fenced-bytes-are-within-the-bar 7,582 fenced bytes, 610 B left (whole file 9,042 B, not asserted), 12 fences balanced; engine-post and engine-wrap exist; F2 (no piece GONE from the map) is b1-map-names-no-absent-piece and b1-measure-finds-the-pieces, both ok. C4 (agi-project's pi path to engine-wrap) was NOT needed (margin 610 B > belam's 256 B gate) and stays unlaned. One residue for DG3's NEXT engine.md touch (SM 08:53Z): two facts of the removed loop block live nowhere in engine*.md ('brief in the system prompt', '(skill agi-master-gate)'): fold them into the diagram line or the agi-brief / land rows, ~45 B of the 610. The 20,480 B total clause is not asserted and the engine*.md files sum 82 KB: it is not the bar.
<!-- THOUGHT:END -->

belam-s2-II 08:4xZ 10-10 RULING R': the owner's bar "the bootstrap package is under 8kb" = the FENCED bytes of engine.md (what boots), asserted by one counting rule + row in engine-sizes.t.sh (<= 8,192); C1-C3 (THOUGHT / map / loop fold) done anyway as simplification; C4 (boot code, HOLD) laned only if fenced margin < 256 B after C1-C3.
