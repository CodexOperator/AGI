---
id: experiment:dg2mvp-g71b-check
mint_id: 75c5698caded4f26a02419c5b8d3e255
type: experiment
parents:
  - hypothesis:council-report-reads-the-mur-args-shape-per-round
next_edges: []
edited_by: director-general-2
scaffold_hash: 632882b55d53027d
season: 2
title: "DG3.71b post-build check: council_report.py reads the mur rounds[] shape per round (deaa32675)"
town: core
---
# experiment:dg2mvp-g71b-check

## g71b post-build check: hypothesis:council-report-reads-the-mur-args-shape-per-round (kid tip 0de7f23ab, landed deaa32675)

Code from a deaa32675 archive tree (council_report.py / its tests are byte-identical at HEAD 5cdf23dc7). Every `add` ran against a TMP project + TMP git repo (9 commits, subjects with and without a trailing `(<post>)`), never the live graph. Parent check: experiment:dg2mvp-g716103-check row 10 (mur shape wrote `?..?` and routed all 19 residues to the default leaf).

| # | command | observed |
|---|---|---|
| 1 | CLAIM, rounds[] file with 5 rounds (own old_tip/new_tip, own hypothesis; keys = exact label, label prefix; `parent: <agent id>` and `files` present as in the mur shape), 5 labels, `council_report.py add --run RUNK --args F --root PROJ` | rc 0; each report row carries its OWN `old..new` (5 distinct spans); residues 2/1/3/1/1 each landed on their own owner leaf. The row 10 gap (`?..?` rows, everything on the default leaf) is closed. |
| 2 | owner order, branch 1: hypothesis -> parent goal title `(assigned: post-b)`; and the winner when new_tip subject says `(post-x)` too | residues to post-b's / post-a's leaf (assigned beats subject) |
| 3 | owner branch 2: parent goal title has no `(assigned:)`, new_tip subject `... (post-c)`; and a hypothesis that resolves to no node | residues to post-c's leaf (3 + 1) |
| 4 | owner branch 3: no assigned, new_tip subject without a post; and subject `(belam)` (the Prime) | both to goal:g9.2 (director-engine); the Prime never owns one |
| 5 | label matching: key longer than label; key a prefix of two labels (`r`, `rA`) | longest prefix wins; a key longer than the label does not match (rc 2 when nothing else matches) |
| 6 | idempotence: re-run row 1 | rc 0; report still 5 rows, leaf rows unchanged, 0 new commits |
| 7 | F2: label with no matching round; old_tip unknown (`deadbeef0`); new_tip unknown; old_tip absent; new_tip empty; rounds[] empty | each rc 2 `label 'rX-code' matches no round with known old_tip/new_tip -- nothing written, never a ?..? row`; 0 commits, 0 report rows, 0 `?..?` in the repo (all-or-nothing: a bad LATER round writes nothing for the earlier ones) |
| 8 | option-shaped tip `--output=<path>` | rc 2, no file created |
| 9 | F3 flat shape {parent, old, new, subject} with real tips, 3 labels | rc 0, 3 rows with the real span, residues on the parent goal's (assigned) leaf; the pre-DG3.71b tip-less flat shape is now rc 2 (DG3.71b defect 1, by design) |
| 10 | GAP: flat `{"old":"?","new":"?"}` | rc 0, 5 rows written `?..?` (F2 text: "any row containing `?..?` written = false"; the claim: "never written as `?..?`") |
| 11 | GAP: rounds[] old_tip `?`, new_tip `*`, old_tip `HEAD~1..HEAD` | rc 0; rows `?..<sha>`, `<sha>..*`, `HEAD~1..HEAD..<sha>` |
| 12 | cause: `git show -s --format=%s --end-of-options '?'` | rc 0, empty output (git 2.43 reads `?`, `*`, `.agi`, `A..B` as a pathspec/range, so `--end-of-options` does not make it a revision). `git rev-parse --verify --quiet --end-of-options '<t>^{commit}'` rejects all of them (rc 1) and accepts `HEAD` |
| 13 | pytest, one file per run, archive tree | test_council_report.py 27 passed; test_bin_help_smoke.py 73 passed, 8 skipped |
| 14 | my strict-xfail rows: `git grep -n "xfail\|g71b\|dg2mvp" HEAD -- extensions/agi/tests/test_council_report.py` | 0 hits: I filed none for this row, so no marker to remove or weaken |
| 15 | CEILING `git diff --numstat 6622aa894 deaa32675` | council_report.py 33+/7- (net +26), test_council_report.py 88+/18- (net +70), node 47. Per commit: 967ab4fb9 prod +22 (ceiling +25) tests +40 (+40); 3d6a3ef72 prod +4 (corrective ceiling +12) tests +30 (+30). All within, 1 kid, 0 USD |

Falsifiers: F1 not fired (rows 1-6) · F2 not fired as written (row 7: unmatched label; unknown tips) but the same claim line fails for non-revision strings (rows 10-12) · F3 not fired (row 9; test_council_report.py 27 passed).

Open residues not re-raised: card-director-general-3 (flat leaf recomputed per round; equal-length duplicate keys resolve in args order; no in-tree producer of rounds[]; the merge_gate / council.residue_leaves cells are the Prime's) and card-sanctuary-master (cells with the Prime). Noted, not raised (declared in the node's THOUGHT near miss): the flat owner reads the dict `subject`, not new_tip's subject.
