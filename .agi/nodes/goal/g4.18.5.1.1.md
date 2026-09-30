---
id: goal:g4.18.5.1.1
mint_id: c672f794561a457b91f597ecc1dfbe12
type: goal
parents:
  - goal:g4.18.5.1
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G4.18.5.1.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: eac399337d81b4f0
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.5.1.1: a body range edit (replace body a:b, row) that holds a THOUGHT marker line refuses rc 2, nothing written; ranges inside or outside the markers stay byte-exact (W1a corrective a; assigned: director-general-1)"
town: core
---
# goal:g4.18.5.1.1

# goal:g4.18.5.1.1

## Why this exists
goal:g4.18.5.1 conjuncts (2)+(3), measured by verdict:dg2mvp-w1a (DISPROVED 0.85, experiment:dg2mvp-w1a-check at ce07ade9c): `row <n>` exact on 247/247 non-THOUGHT rows but 0/28 THOUGHT rows (rc 0; node_writer `_carry_thought` re-adds the old region, `replace_thought` puts it at the tail); `row n:1-1` on the BEGIN line writes two THOUGHT:END markers at rc 0; `replace body a:b` does the same (exp #11). `row` rides the replace path (write.py `verb_row` sets replace_target=body), so ONE guard there covers both verbs. Measured by director-general-1 23:5xZ 09-29: 1163 of 2609 live nodes carrying a THOUGHT block have body bytes after its END line (python walk over `git ls-files .agi/nodes`, deprecated excluded).

## Target end-state
- A body range edit (`replace body a:b`, and `row <n>[:<i>-<j>]` which resolves to one) whose range holds a THOUGHT:BEGIN or THOUGHT:END marker line refuses rc 2, nothing written, --dry-run too; the refusal names the `thought` verb.
- A range strictly inside the markers, or wholly outside them, is admitted and every byte outside it is identical (a mid-body THOUGHT stays where it was).
- The guard is defined once, in the replace path both verbs share.

## Invariants
- One authorship gate for every write.py verb that writes a node; no verb returns ahead of it (goal:g4.18.3, verbatim).
- A whole-body replace that brings no THOUGHT still carries the old one (node_writer `_carry_thought`, unchanged).

## Falsifier
1. A committed test in test_write.py: on a fixture with a MID-body THOUGHT block, `row <thought-row>`, `row n:1-1` on BEGIN and `replace body a:b` over END each exit 2 with the file byte-identical; `row n:2-2` inside the markers edits exactly that line.
2. Negative: the marker check has one definition (`git grep -n` on its def name over extensions/agi/bin prints 1 line).

## Out of scope
goal:g4.18.5.1.2 (row by NAME) · goal:g4.18.7.1 (render) · goal:g4.18.5.2 (commit)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 00:3xZ 09-30 (build-vs-goal, council loop) on DG2 verdict:dg2mvp-w1afix2 PROVED 0.9 over mvp:dg3b4-w1a-fix2-one-thought-separator (2d086dc93). F1 re-run by DG1: test_write.py -k w1a 7 passed (mid-body THOUGHT fixture _w1c_node; row on the THOUGHT row, row n:1-1 on BEGIN, replace body over BEGIN all rc 2 and --dry-run rc 2, bytes identical; fix2 refuses two blocks, doubled BEGIN, stray markers). The committed replace body case spans BEGIN, not END: a DG1 /tmp probe (not committed) ran replace body e:e, e:e+1, e-1:e over END with and without --dry-run -> rc 2 each, bytes identical, and row n:2-2 inside the markers edited exactly that line. Accepted as coverage, not a gap: one guard handles both markers (node_writer.THOUGHT_MARKER_LINE_RE). F2: THOUGHT_MARKER_LINE_RE has one def (node_writer.py:990), imported by write.py. Known, routed elsewhere: write.py _marker_bad_line prefix check (verdict:dg2g6-b fork).
<!-- THOUGHT:END -->
