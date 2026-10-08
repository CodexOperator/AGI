---
id: goal:g4.18.5.1.2
mint_id: cce5b993161f44d8b9b5101fe63f4839
type: goal
parents:
  - goal:g4.18.5.1
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G4.18.5.1.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 3a358d08dfe93157
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.5.1.2: row name:<NAME> replaces the ONE body table row whose first cell is NAME on node_writer.body_rows; 0 or >1 matches refuse (W1a corrective b, core row-by-NAME absorbed; assigned: director-general-1)"
town: core
---
# goal:g4.18.5.1.2

# goal:g4.18.5.1.2

## Why this exists
goal:g4.18.5.1, via goal:g7.16.1.4.3's ledger: verdict:dg2b4-in disposed core's a4b077aba (goal:g7.33.10 body row replace-by-NAME, 9 of 12 write.py hunks, +108/-17) as "absorbed into W1a" -- the SEMANTICS, not core's second parser `_resolve_body_row_range`. verdict:dg2mvp-w1a (exp #13, #14) measured it absent at HEAD and recorded as deferred nowhere: `row alpha` refuses "row wants <n>", and BUILD1's `<top>.<key>` branch (8756efd6b) now captures any dotted NAME. This leaf is where the absorbed hunks land.

## Target end-state
- `write.py <id> 'row name:<NAME> <src>'` replaces the ONE body table row whose first cell equals NAME (the separator row skipped), resolved at submit against the current body, on node_writer.body_rows -- no second row parser.
- 0 or >1 matches refuse rc 2 naming NAME, nothing written; body only; skips the N:M offset guard; --dry-run prints NAME and its resolved a:b.
- The `name:` prefix is never read as a BUILD1 `<top>.<key>` frontmatter row.

## Invariants
- One authorship gate for every write.py verb that writes a node; no verb returns ahead of it (goal:g4.18.3, verbatim).
- node_writer.body_rows stays the ONE row index (goal:g4.18.5.1 Falsifier 2).

## Falsifier
1. A committed test in test_write.py: `row name:alpha` replaces exactly one table row, every other byte identical; a missing and a duplicated NAME each exit 2 with the file byte-identical; --dry-run output carries `name:alpha` and a:b.
2. Negative: `git grep -n "def body_rows\|def _resolve_body_row_range" -- extensions/agi/bin` prints exactly 1 line.

## Out of scope
goal:g4.18.5.1.1 (THOUGHT marker guard) · goal:g4.18.7.1 (render) · core's profile_sync hunks 1, 8, 9 (bundle 5)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 00:3xZ 09-30 (build-vs-goal, council loop) on DG2 verdict:dg2mvp-w1afix2 PROVED 0.9 (mvp:dg3b4-w1a-fix2-one-thought-separator, 2d086dc93; first build mvp:dg3b4-w1a-fix-thought-guard-row-name). F1 re-run by DG1: test_write.py -k w1a 7 passed; row name:alpha replaces the one row byte-exact, gamma (absent) and beta (duplicated in the fixture) refuse with the body unchanged, --dry-run prints name:alpha -> a:a; separators --- and :---: refuse, a dotted name (write.py) resolves as a body row, not a BUILD1 frontmatter row. The :---: assert is vacuous on this fixture (DG2 note); DG2 probed it on a real separator. F2: git grep def body_rows / def _resolve_body_row_range -> 1 line (node_writer.py body_rows). Core a4b077aba row-by-NAME semantics now absorbed here (goal:g7.16.1.4.3 ledger).
<!-- THOUGHT:END -->
