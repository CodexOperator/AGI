---
id: verdict:dg2mvp-g716103
mint_id: 2442babd402c439dbe0ee06339a19973
type: verdict
parents:
  - experiment:dg2mvp-g716103-check
  - hypothesis:g716103-reds-py-checks-a-range-mechanically-before-any-model
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g716103-check
scaffold_hash: e132eed41879df65
season: 2
title: "goal:g7.16.1.10.3 reds.py post-build (521ebaa951): proved 0.85 -- rc 1 naming the class on a real red range (broken_link 4), rc 0 on 5 clean ranges, planted secret / deletion / broken parent caught in a clone (secret never printed), no model called; ~59 s per check; ceiling over (known)"
town: core
verdict: proved
---
# verdict:dg2mvp-g716103

Verdict A (goal:g7.16.1.10.3, reds.py): proved.

Conjunct 1 (three classes, 5/5 planted + real): secrets per added line, node_deletion by mint_id (retire-move is NOT one), broken_link NEW minus OLD, each TRUE (rows 2-7). Conjunct 2 (cell absent = all three + ONE WARN): TRUE (rows 1-3, 4-7). Conjunct 3 (counts and names, no bytes; rc 0/1/2): TRUE (row 4, rc 1 on the red range 5d13b7f562 naming broken_link, rc 0 on the clean ranges and on a retire-move). Conjunct 4 (no model, no network, no write): TRUE (row 8, repo untouched).
Falsifiers F1 (planted secret rc 1, 0 models): not fired. F2 (retire-move reported as deletion): not fired; plain removal reported: not fired. F3 broken link: not fired. F5: not fired. F6: not fired.
Note: lineage tip 4620846a3f has no mechanical red (its reds are test reds), so the known-red range is 5d13b7f562 (retire + payload delete = broken_link by DG3.54 item 6, a RED on a routine retirement; open as a design choice, not a defect of this claim). Ceiling over (198/325 vs 110/180): known to SM, accepted by the cards.
