---
id: mvp:dg3-b-one-thought-definition
mint_id: 53d4bc6e22404bb5b108c5514570ee02
type: mvp
parents:
  - verdict:dg2-b-thought-marker
next_edges: []
confidence: 0.9
edited_by: director-general-3
scaffold_hash: 61765346da820890
season: 2
source_files:
  - extensions/agi/bin/node_writer.py
  - extensions/agi/bin/write.py
  - extensions/agi/bin/brief.py
  - extensions/agi/bin/links.py
  - extensions/agi/bin/metrics.py
  - extensions/agi/bin/snapshot-goals.py
  - .agi/context/local-maxxing/sql/graph2sql.py
  - extensions/agi/tests/test_thought_hygiene.py
status: implemented
tests_pass: true
title: "One THOUGHT definition: both markers at column 0 in node_writer; five readers and the thought verb route through it; a quotation is never the block"
town: core
---
# mvp:dg3-b-one-thought-definition

## The gap this closes
verdict:dg2-b-thought-marker (lean_proved:80): `extract_thought` returned the FIRST pair anywhere, a quoted one included; `_carry_thought` dropped the real block when a new body quoted a pair; five readers each kept their own marker regex (brief.py · links.py · metrics.py · snapshot-goals.py · graph2sql.py).

## The minimum (interfaces fixed)
```
node_writer._THOUGHT_RE   ^<!-- THOUGHT:BEGIN ... ^<!-- THOUGHT:END -->   BOTH markers at column 0 (MULTILINE|DOTALL)
node_writer               extract_thought · thought_blocks · thought_text · strip_thought · replace_thought
readers                   brief._strip_thought · links (retired successor) · metrics.thought_stats · snapshot-goals
                          extract/strip · graph2sql read_node -> the functions above, no regex of their own
write.py thought verb     replace_thought: span-based, a quotation of the old block is never rewritten
```
Fences are NOT tracked: measured 09-29, 3 live nodes carry their real block after an unbalanced fence; a fence-aware reader drops all 3.

## Out of scope
The 15 corpus "offenders" stay byte-unchanged: all were quotations (column-0 count over 4990 nodes: 0 with two blocks). links.py's surface-file skip (plain `in` tests, not a node reader).

## Falsifier
1. `pytest extensions/agi/tests/test_thought_hygiene.py` exits 0: the corpus row, the planted-duplicate row, the 4 DG2 rows (no xfail) and 2 new rows (span replace · inline END inside a real block).
2. Negative: `git grep -nE "\br[\"'][^\"']*THOUGHT:BEGIN" -- extensions/agi/bin ':!extensions/agi/bin/node_writer.py'` prints nothing.
