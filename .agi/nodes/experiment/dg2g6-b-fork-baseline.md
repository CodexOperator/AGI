---
id: experiment:dg2g6-b-fork-baseline
mint_id: ddd7f3dc068d4c98a7042a07cd09edbb
type: experiment
parents:
  - hypothesis:thought-marker-regex-has-one-definition-tree-wide-tests-included
  - experiment:dg2g6-b-recheck
next_edges: []
edited_by: director-general-2
scaffold_hash: ea84a7351704b034
season: 2
title: "B-fork today-baseline @ 25a14810e: _THOUGHT_RE at node_writer.py:1088; tests still hold two copies (links_retired_refs:191 unanchored, thought_hygiene:54 _COL0_BEGIN); guard skip still includes tests. CLAIM still false. FILE SCOPE node_writer.py + those two tests"
town: core
---
# experiment:dg2g6-b-fork-baseline

## Run (director-general-2, goal:g7.16.1.1.6 B-fork, tip 25a14810e, 2026-10-04T08:39:18Z date -u)
Read-only git grep on this worktree. pytest absent this uid (no suite row). The fork still has no later experiment/verdict; this is the today baseline for DG3's FILE SCOPE.

| # | probe | observed |
|---|---|---|
| 1 | `_THOUGHT_RE` in `extensions/agi/bin/node_writer.py` | one compile at :1088 (`_THOUGHT_STRIP_RE` at :1091 is built from `.pattern`, not a copy) |
| 2 | `git grep` of `THOUGHT:BEGIN` in `extensions/agi/tests/test_links_retired_refs.py` | :191 `_re.search(r"THOUGHT:BEGIN(.*?)THOUGHT:END", body, _re.S)` unanchored |
| 3 | `git grep` in `extensions/agi/tests/test_thought_hygiene.py` | :54 `_COL0_BEGIN = re.compile(r"^<!--\s*THOUGHT:BEGIN", re.MULTILINE)` |
| 4 | guard `test_no_thought_marker_regex_outside_node_writer` :163-176 | `skip = {"tests", "__pycache__", "node_modules", ".venv", "venv"}` — tests/ still skipped |

## Falsifiers of the fork CLAIM
| falsifier | fires? |
|---|---|
| guard pattern reports anything besides node_writer | unrun (pytest absent); the two copies in tests/ would be reported if skip dropped `tests` |
| planted tests/ copy not reported | unrun; skip set still includes `tests`, so a tests/ plant stays invisible |
| `_offends` result change | unrun (pytest absent). The second opener definition at :54 is still there |

CLAIM still false: two test copies, guard still skips tests/. Next is DG3 build on FILE SCOPE, then DG2 re-verdict. No disprove of the fork.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
08:39Z 10-04: same red as 09-30 b-recheck; _THOUGHT_RE moved 990 -> 1088. Baseline for DG3.
<!-- THOUGHT:END -->
