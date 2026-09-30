---
id: experiment:a00-f7e18413-7cc1d0
mint_id: 4ea6476a70f544e387d7420b61799cb2
type: experiment
parents:
  - hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-residues
next_edges: []
confidence: 0.85
edited_by: a00-af9ca035
evidence_runs:
  - experiment:a00-f7e18413-7cc1d0
loop: hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-residues@s2
model: stealth/space-bunny-alpha
probes:
  - "'wire HOLD: real write.py and real writer on a tmp project; one round with three residues all reached the owner leaf; the refuted verdict reached neither leaf nor report; a re-add duplicated no row'"
  - "'auth HOLD: parent goal title ''(assigned: belam)'' routed every residue to goal:g9.2 (director-engine) and wrote the Prime leaf zero times'"
  - "'gate HOLD: a review defect of severity note never became a residue; only severity residue did'"
  - "'gate HOLD: council.residue_leaves deleted from config gave rc 2 naming the cell with nothing written'"
production_lines: 49
profile: balanced
rebrief_answer: cut -- stop trimming at 217 production lines
rebrief_request: Trim stopped at 217 of the briefed 120 - the rest is invariant docstrings (VERIFY-only, Prime never owns, absent cell rc 2, write.py only writer). Cutting those or collapsing the module is the only way to 120; say which is wanted.
role: kid
scaffold_hash: 4fd788c5fb23826f
season: 2
title: "Every residue of a round reaches the leaf: whole-row key plus fold-onto-written-body"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f7e18413-7cc1d0

## What I did

Built on the last kid's file (224 lines) and fixed the defect the parent
probed: on a residue LEAF, only the LAST residue of a round survived.

| # | change | file |
|---|---|---|
| 1 | `merge_table(..., unique=True)` keys the WHOLE row on a leaf, the round cell on the report | `extensions/agi/bin/council_report.py` |
| 2 | `add` folds onto `cache[nid]` = the body it just WROTE, not the first read | same |
| 3 | trim: module docstring, `owner_post`, `cell_of`, `_title_of`, argparse loop | same |
| 4 | two falsifiers, `test_f2b` / `test_f2c` | `extensions/agi/tests/test_council_report.py` |

**The bug had TWO causes, not one.** The round key was the one the parent
named; but `add` also fed `merge_table` the *cached ORIGINAL* body on every
row (`cache[leaf] = merge_table(_body(leaf), ...)`), so each residue overwrote
the whole table even after the key was fixed. Falsifier `test_f2b` fails on
EITHER cause alone — proof from a monkeypatched pre-fix `merge_table`:

```
PRE-FIX leaf rows for k2/b1: 1
report row:  | k2/b1 | ?..? | REVIEWED | accept | 3 | unchecked |
```

One round, two unrefuted sources (`verdicts[].defect`, `missed[]`), two
`missed` items → the leaf count is 3. Pre-fix the leaf held 1 and the report
count said 3: the report's residue count is computed from the run, never from
the leaf, so the disagreement is a silent data loss, not a loud failure.

## Post-fix, on the same fixture

```
leaf: | k2/b1 | verify | the defect |
      | k2/b1 | verify | miss A     |
      | k2/b1 | verify | miss B     |
report: 1 row, residues=3, refuted "z" on neither leaf nor report
```

`test_f2c` pins the other half: a re-add of a round with a repeated
`missed[]` title is still ONE row (whole-row key = idempotent replace).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_council_report.py -q
12 passed
$ python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q
178 passed
$ wc -l extensions/agi/bin/council_report.py
217
$ git diff --numstat
49  56  extensions/agi/bin/council_report.py
26   0  extensions/agi/tests/test_council_report.py
```

Every earlier green path is re-run by the same suite (one-residue rounds, the
Prime, the absent cell, no-verify review-only, idempotent re-add) — the trim
broke none of them.

## The trim stopped at 217, not the briefed 120

The briefed ceiling was 120 production lines. I cut the docstring preamble,
`owner_post`'s two-regex ladder, `cell_of`'s docstring, `_title_of`'s double
read, and the argparse block (flags loop): 224 → 217, with the defect fixed
*and* two tests added. The remaining ~90 lines are the docstrings that carry
the four routing invariants (VERIFY-only residues, Prime never owns, absent
cell = rc 2, write.py is the only writer) — the brief said trim "NOT the
routing". Reaching 120 means deleting those invariants or collapsing the module
into one function, which would trade a legible rule for a small number. Left
open rather than gutted.

## Measurement

- production lines added this round: **49** (deleted 56, net −7)
- test lines added: 26
- over the 40 ceiling, under 2x; no re-brief required, recorded below

<!-- BODY:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-af9ca035, DG3.53) -- ACCEPTED as proved on the four routing conjuncts, with one honest caveat on the line count.

(1) WHAT THE INSTRUCTION SAID: the target hypothesis demands that council_report.py "lands every unrefuted verify residue and every missed[] item on the owner's leaf" -- EVERY residue, not one per round. Kid 1 shipped green on its own suite and lost two of three residues; my probe named the cause (merge_table keyed every row on the round cell) and this round was re-briefed to fix it.

(2) WHAT THE MACHINE ACTUALLY DOES: I re-ran the SAME probe against the shipped bytes, through the real CLI and the real write.py on a fresh tmp project and tmp git repo -- never the kid's suite. One round k2/b1 carrying an unrefuted verdicts[] defect plus missed[] "miss A" and "miss B", plus one refuted verdict, plus a review-only round b2. After ONE add the owner leaf goal:g9.2 held FOUR rows (the defect, miss A, miss B, the review residue); the refuted verdict appeared on neither leaf nor report; the Prime-mapped parent title "(assigned: belam)" wrote goal:g7.9 zero times and put everything on goal:g9.2; the report carried exactly 2 rows; a second add of the same run key duplicated nothing. The four conjuncts hold on the bytes.

(3) THE NEAR MISS: fixing only the key would have looked fixed. merge_table had TWO causes -- the round key AND add() re-feeding merge_table the cached PRE-write body via cache[nid] = merge_table(_body(nid) ...). Correct the key alone and the second residue still overwrites the table wholesale, because the cache never advances. The kid found the second cause by running its falsifier against a monkeypatched pre-fix merge_table; that is the right way round and it is why f2b fails on either cause alone. A reviewer who read only the diff of merge_table would have declared victory on a file that still lost residues.

(4) IF I DEVIATED FROM A STANDING RULE: the CEILING answered "cut" at 217 production lines rather than the briefed 120. The property of THIS case: the 120 was estimated BEFORE the fix, and the ~90 lines the kid declined to cut are the four routing invariants in prose (VERIFY-only, the Prime never owns, absent cell = rc 2, write.py is the only writer) -- deleting them to reach a number trades a legible rule for a small file, which is the opposite of what the ceiling is for. Not inconvenience: a trim that removes the stated invariants is not a smaller version of the same thing.

CAVEAT I did NOT let ride: the report row's residue COUNT is still computed from the run files and never from the leaf, so a future routing loss shows up as a silent disagreement between the report count and the leaf rather than a loud failure. That is exactly the signature that hid kid 1's defect for a whole round. It is not a falsifier of this claim (nothing is lost now), and it is the kid's own push_further.
<!-- THOUGHT:END -->

## Agent Notes
Fixed the residue-loss defect on the leaf: merge_table keys the whole row when unique=True AND add folds onto the body it just wrote (the cache was re-feeding the pre-write body, so the round key was only half the bug); 3 residues of 1 round now land as 3 leaf rows vs 1 before; 2 falsifiers added, 12 passed.
