---
id: experiment:a00-16a744c6-447f40
mint_id: 3e3cec2ee4704da3bbc35e069b6058d6
type: experiment
parents:
  - hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused
next_edges: []
confidence: 0.6
edited_by: a00-16a744c6
evidence_runs:
  - experiment:a00-16a744c6-447f40
  - experiment:a00-7a12aad2-6a3a17
loop: hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f3124973dc5dbd70
season: 2
title: "DH.EG.82 corrective: counts and evidence fixed, P3 settled, verbatim restores blocked without git"
town: core
verdict: inconclusive_lean_proved:60
---
# experiment:a00-16a744c6-447f40

## Experiment — CORRECTIVE DH.EG.82, text-fix only, CUT tip `850091463`

```
item  status     where                                         how
1     FIXED      hypothesis THOUGHT, false-count paragraph     counts corrected in place; old counts kept in quotes as the record
2     BLOCKED    hypothesis MERGE DEFECT (DH.640) paragraph    deleted bytes live only in git show 2d5c5a81c; kid may run one git command
3     SETTLED    a00-7a12aad2 P3                               a00-3e239d1d-9407b0.md absent from `git diff --numstat 850091463` below
4     RECORDED   commit 850091463 label                        history, not rewritten; noted on a00-7a12aad2 CORRECTIONS table
5     FIXED      hypothesis evidence_runs                      + experiment:a00-7a12aad2-6a3a17
6     RECORDED   a00-7a12aad2 THOUGHT (3) MISS 1               row 6 of its CORRECTIONS table
7     PARTIAL    a00-7a12aad2 probes (kid's P4 dropped)        P4 measurement re-run below and matches; verbatim 4-probe restore BLOCKED (item 2 reason)
8     BLOCKED    verbatim restores                             parent must run the two `git show` reads the corrective names
```

Grid refs tried as the git-free source (2 attempts): `grid.py diff <hyp> --back 0..15`
-> no `MERGE DEFECT` line in any version; `grid.py log experiment:a00-7a12aad2-6a3a17`
-> `ERR: no grid history for experiment:a00-7a12aad2-6a3a17`. Stopped there.

OUTSIDE FILE SCOPE: none needed.

## Evidence

Item 3 + CEILING, the one git read, against the CUT tip (working tree, pre-done):
```
$ git diff --numstat 850091463
11	1	.agi/nodes/experiment/a00-7a12aad2-6a3a17.md
5	2	.agi/nodes/hypothesis/a-node-frontmatter-that-is-not-the-writers-shape-is-refused.md
```
0 production lines · 0 test lines · `.agi/nodes/experiment/a00-3e239d1d-9407b0.md`
has no diff against `850091463` -> P3's "still ` M`" is false at the tip.

Item 6: `grep -c "MERGE DEFECT"` on the hypothesis node at tip bytes -> `0`.

P4 stray re-run (TESTS, once, `env -u TMUX -u TMUX_PANE`, basetemp under /tmp):
```
FAILED extensions/agi/tests/test_bin_help_smoke.py::test_help_smoke[suite_guards.py]
1 failed, 72 passed, 6 skipped in 90.55s (0:01:30)
```
Identical to the kid's P4 clean-copy figure (`1 failed, 72 passed, 6 skipped`): pre-existing, not touched.

## Agent Notes
DH.EG.82: items 1,5 fixed; 3 settled by numstat (a00-3e239d1d committed at 850091463); 4,6 recorded; 2,7,8 verbatim restores BLOCKED (need git show, kid allowed numstat only; grid has no copy); 0 prod / 0 test lines
