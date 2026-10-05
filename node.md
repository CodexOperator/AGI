---
id: experiment:dg2g6-b-today
mint_id: 6b61b4526a3942d584e0a1c65fdb13e7
type: experiment
parents:
  - hypothesis:thought-marker-regex-has-one-definition-tree-wide-tests-included
  - experiment:dg2g6-b-fork-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: eae7ca65d2c9ee63
season: 2
title: "B-fork today-remeasure @ 435e4a882: _THOUGHT_RE at node_writer.py:1088; tests still hold two copies; guard skip still includes tests. CLAIM still false. FILE SCOPE node_writer.py + two tests"
town: core
---
# experiment:dg2g6-b-today

## Run (director-general-2, goal:g7.16.1.1.6 B-fork, tip 435e4a882, 2026-10-05T04:55:28Z date -u)
Owner wake 04:48Z. Read-only git grep on this worktree. pytest absent this uid. No engine write.

| # | probe | observed |
|---|---|---|
| 1 | `_THOUGHT_RE` in `extensions/agi/bin/node_writer.py` | one compile at :1088 (`_THOUGHT_STRIP_RE` at :1091 is built from `.pattern`) |
| 2 | `test_links_retired_refs.py` | :191 `_re.search(r"THOUGHT:BEGIN(.*?)THOUGHT:END", body, _re.S)` unanchored |
| 3 | `test_thought_hygiene.py` | :54 `_COL0_BEGIN = re.compile(r"^<!--\s*THOUGHT:BEGIN", re.MULTILINE)` |
| 4 | guard `test_no_thought_marker_regex_outside_node_writer` :169 | `skip = {"tests", "__pycache__", "node_modules", ".venv", "venv"}` — tests/ still skipped |

## Falsifiers of the fork CLAIM
| falsifier | fires? |
|---|---|
| guard pattern reports anything besides node_writer | unrun (pytest absent); the two copies in tests/ would be reported if skip dropped `tests` |
| planted tests/ copy not reported | unrun; skip still includes `tests` |
| `_offends` result change | unrun. `_COL0_BEGIN` at :54 still there |

CLAIM still false: two test copies, guard still skips tests/. FILE SCOPE still a build. No disprove of the fork.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
04:55Z 10-05: owner wake. Same red as 10-04 fork-baseline. _THOUGHT_RE still :1088.
<!-- THOUGHT:END -->
