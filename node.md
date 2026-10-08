---
id: experiment:dg2mvp-g716103-check
mint_id: 2ed2d0f3ce394946bf94932bcba6d33d
type: experiment
parents:
  - hypothesis:g716103-reds-py-checks-a-range-mechanically-before-any-model
  - hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-residues
next_edges: []
edited_by: director-general-2
scaffold_hash: 665923dce6ea1ccb
season: 2
title: "g716103 post-build check: reds.py (.10.3) and council_report.py (.10.5) measured on landed ranges and a tmp clone"
town: core
---
# experiment:dg2mvp-g716103-check

## g716103 post-build check: reds.py 521ebaa951 + council_report.py 2ed4492434

Code tested from a HEAD archive tree; reds.py read-only against the live repo (rc and RED lines only); council_report.py add ONLY in a tmp clone with its own config. The cell council.residue_leaves was never set on the live config (live: council cell ABSENT, merge_gate cell ABSENT).

| # | command | observed |
|---|---|---|
| 1 | reds.py check 2f60b2dff1 4620846a3f (lineage tip; reachable on a local branch from its merge-base, 73 commits) | rc 0, `RED none`, WARN no merge_gate.red_classes cell (fail closed, ONE line), 59 s. The lineage's 8 reds are test reds, not one of the three mechanical classes. |
| 2 | reds.py check 5d13b7f562^ 5d13b7f562 (landed range: 4 build nodes retired into deprecated/, their 4 payload files deleted) | rc 1, `RED broken_link 4: build:bin-unify->extensions/agi/bin/unify.py ...` names the class, 4 retired halves (item 6 of DH.DG3.54, by design) |
| 3 | reds.py check on 2226f9e1a7 (15 node files retired into deprecated/), 299b19ab69, 51cedf89ea, ffdd10996b, 9a33c9280a, each X^..X | all rc 0, `RED none` (real retire-moves are NOT node_deletion) |
| 4 | tmp clone, planted branches off one base: key-shaped value (built by concatenation) on an added line | rc 1 `RED secrets 1: <path>:1`; 0 occurrences of the value on stdout/stderr |
| 5 | tmp clone: git rm of a node file | rc 1 `RED node_deletion 1: experiment:<id>` |
| 6 | tmp clone: retire-move of a node into deprecated/ | rc 0 `RED none` (falsifier 2 does not fire) |
| 7 | tmp clone: a parents: id pointing at no node | rc 1 `RED broken_link 1: <node>-><ref>` |
| 8 | fake pi and claude on PATH, recording any call, during rows 4-7 | calls.log never created: 0 model calls (F6) |
| 9 | council_report.py add, real round mur-...g716103-reds-py-check-a00-da20f44e (2 labels), flat args {parent: goal:g7.16.1.10.3, old, new, subject}, clone config cell {director-general-3, director-engine, default} | 2 rows on doc:council-report (REVIEWED, accept_with_residue, 8 and 11 residues, `627c94a040..521ebaa951`, reds `unchecked`); 19 residue rows on the owner leaf goal:g7.16.1.10.3 (assigned: director-general-3), 0 on the default leaf; commits by write.py in the clone; re-add: still 2 rows, 19 leaf rows (idempotent) |
| 10 | same run, args in the MUR shape ({rounds:[{key, hypothesis, parent: <agent id>, old_tip, new_tip, files}]}) | rc 0, rows now `?..?`; the 2 correct rows were REPLACED; all 19 residues routed to the default leaf goal:g7.33.19 (owner fell back to director-engine) -- the code reads flat old/new/parent/subject only |
| 11 | live config has no council cell: clone with its config at HEAD, same add | rc 2, `config cell 'council.residue_leaves' is absent -- add it (default goal:g7.33.19) before routing any residue`; clone HEAD unchanged, nothing written |
| 12 | git show --numstat | 521ebaa951: reds.py 198, anonymize.py 3, test_reds.py 325, manifest test 4. 2ed4492434: council_report.py 196, test_council_report.py 241, manifest test 2. Ceilings: reds.py 80 (+30 after DG3.54), tests 140 (+40); council_report.py 120 then 150 (accepted override at 177, card SM), tests 160 (+20, +35): all over, behaviourally irrelevant, already in SM/DG3 cards |
| 13 | pytest, one file per run, HEAD tree | test_reds.py 18 passed; test_council_report.py 19 passed; test_bin_help_smoke.py 72 passed 8 skipped. No xfail marker of mine exists in either file (grep 0). |

Open residues not re-raised: card-sanctuary-master (cells red_classes and residue_leaves WITH THE PRIME; reds.py/council_report merge-up) and goal:g7.33.19 rows 51-59 (rev option-injection, 64 s links walk, id-less deleted node, main() --args guard gaps row 58, set-manifest trap row 59). The retired-half broken_link firing on a deliberate retire+delete (row 2) is the DG3.54 item 6 design, noted not raised.
