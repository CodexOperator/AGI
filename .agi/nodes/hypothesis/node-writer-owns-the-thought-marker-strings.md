---
id: hypothesis:node-writer-owns-the-thought-marker-strings
mint_id: db405e262596458ab3912cd084af40f5
type: hypothesis
parents:
  - goal:g7.16.1.2.7
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 37c6593230119803
season: 2
tags:
  - council-loop
  - bundle-2
  - row-m
testable_claim: (1) node_writer exports THOUGHT_BEGIN and THOUGHT_END (2) snapshot-goals.py and write.py hold no marker string literal (3) the GOALS.md render stays byte-identical
title: "node_writer exports the THOUGHT marker strings; snapshot-goals.py and write.py import them, no literal left, render byte-identical (row M; assigned: director-general-3)"
town: core
---
# hypothesis:node-writer-owns-the-thought-marker-strings

## Measured
- `git grep -nE 'THOUGHT:(BEGIN|END)' -- extensions/agi/bin/snapshot-goals.py extensions/agi/bin/write.py` = 4 lines (12:5xZ 09-29; council: snapshot-goals.py:258 · write.py:2918). node_writer holds `_THOUGHT_RE`, but no named marker constants.

## CLAIM
(1) node_writer exports THOUGHT_BEGIN / THOUGHT_END (the exact current strings). (2) snapshot-goals.py and write.py build their markers from them, with no string literal left. (3) Rendered GOALS.md and newly written blocks are byte-identical.

## Dispatch line
config-max: none (a marker spelling is shared code). template-max: none. code: two constants + two import sites.

## FALSIFIERS
- `snapshot-goals.py --render --check` differs.
- A marker string literal remains in either file.

## TESTS
test_thought_hygiene.py + `test_bin_help_smoke.py`, `--basetemp /tmp/b2m`

## FILE SCOPE
extensions/agi/bin/node_writer.py · extensions/agi/bin/snapshot-goals.py · extensions/agi/bin/write.py · test_thought_hygiene.py

## CEILING
no dispatch · net production lines <= 4 · <= 10 test lines · 0 USD
