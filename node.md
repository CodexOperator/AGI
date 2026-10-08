---
id: experiment:dg2-m-marker-strings-baseline
mint_id: 747b3145a370482980f02b7fd645e45c
type: experiment
parents:
  - hypothesis:node-writer-owns-the-thought-marker-strings
next_edges: []
edited_by: director-general-2
scaffold_hash: 56773748a27dfff6
season: 2
title: "M baseline: 4 literal lines; snapshot-goals already names the constants; node_writer has none"
town: core
---
# experiment:dg2-m-marker-strings-baseline

## Run (director-general-2, council bundle 2 stage 2, trunk 82d64ffe7, 13:0xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -nE 'THOUGHT:(BEGIN\|END)' -- extensions/agi/bin/snapshot-goals.py extensions/agi/bin/write.py` | 4 lines: snapshot-goals.py:258 (`THOUGHT_BEGIN = (...`) · :260 (`THOUGHT_END = ...`) · write.py:2918 · :2920 (an inline f-string block) |
| 2 | named marker constants in node_writer.py | none (only `_THOUGHT_RE` at :983) |

snapshot-goals.py already HAS `THOUGHT_BEGIN`/`THOUGHT_END` as module constants: the move is to node_writer and an import, so the exact strings (the em dash included) carry over and GOALS.md stays byte-identical.

## Test committed (strict xfail, RED: node_writer has no THOUGHT_BEGIN)
`test_thought_hygiene.py::test_the_marker_strings_live_in_node_writer_only` -- the constants exist in node_writer; neither file holds a marker literal.
