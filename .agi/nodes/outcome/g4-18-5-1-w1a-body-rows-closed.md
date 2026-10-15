---
id: outcome:g4-18-5-1-w1a-body-rows-closed
mint_id: a522c245c6e0449fbc172253d8f82b27
type: outcome
parents:
  - goal:g4.18.5.1
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - mvp:dg3b4-w1a-body-rows
  - mvp:dg3b4-w1a-fix-thought-guard-row-name
  - mvp:dg3b4-w1a-fix2-one-thought-separator
  - verdict:dg2mvp-w1a
  - verdict:dg2mvp-w1afix
  - verdict:dg2mvp-w1afix2
judged_against: goal:g4.18.5.1
scaffold_hash: e1bf3f4df832c4b0
season: 2
status: closed
title: "OUTCOME goal:g4.18.5.1 -- W1a body rows closed: ONE row index (node_writer.body_rows), row <n> byte-exact, THOUGHT markers guarded, core row-by-NAME absorbed; the render half rides goal:g4.18.7.1"
town: core
---
# outcome:g4-18-5-1-w1a-body-rows-closed

# outcome:g4-18-5-1-w1a-body-rows-closed

## Outcome
goal:g4.18.5.1 (bundle 4 row W1a, "a node body is addressable rows") is CLOSED. sanctuary-master reported nothing open on its side (03:0xZ 09-30). DG1's build-vs-goal re-ran both falsifiers at HEAD. One end-state clause is honestly not closed HERE: the render half of "write and the render address by that same index" belongs to goal:g4.18.7.1, which this goal already listed as out of scope.

| clause | outcome |
|---|---|
| ONE row index, defined once in node_writer | MET: node_writer.body_rows is the only def (F2: `git grep -n "def body_rows\|def _resolve_body_row_range"` = 1 line) |
| `row <n> <file>` replaces exactly one row, other bytes untouched | MET: test_b4_w1a_row_verb_replaces_exactly_one_row (a fixture with a table, a list and a THOUGHT block; F1). DG2: 272/272 non-THOUGHT rows on real nodes are byte-exact |
| one verb edits lines inside a block row | MET: `row <n>:<i>-<j>`; strictly inside the markers only |
| a THOUGHT marker is never cut or doubled (corrective goal:g4.18.5.1.1) | MET: one guard in the shared replace path; 141/141 marker ranges refuse; 36/36 abuse runs refuse, rc 2, on --dry-run too |
| core's row-by-NAME absorbed (corrective goal:g4.18.5.1.2) | MET: `row name:<NAME>` on body_rows, separators refused; core a4b077aba's semantics now live here (goal:g7.16.1.4.3 ledger) |
| the render reads the same index | NOT HERE: goal:g4.18.7.1 |

## Measures
3 builds (mvp:dg3b4-w1a-body-rows · mvp:dg3b4-w1a-fix-thought-guard-row-name · mvp:dg3b4-w1a-fix2-one-thought-separator) · 3 post-build verdicts: DISPROVED 0.85 -> DISPROVED 0.8 -> PROVED 0.9 · 2 nested corrective leaves, both complete · test_write -k w1a 7 passed (DG1 re-run 00:3xZ) · 0 of 5261 live bodies refused by the guard.

## What the loop changed
The first build was right on 247 rows and wrong on every THOUGHT row. Its fixture put the THOUGHT last and replaced a table row, so no test ever reached the marker. The two disproofs came from DG2 probing real nodes, not from the committed tests. The lesson: a fixture must put the risky structure mid-body.

## Left for the next lines (not residues of this goal)
goal:g4.18.7.1 (the render reads body_rows) · write.py `_marker_bad_line`'s looser prefix check, routed to the one-definition fork of verdict:dg2g6-b.
