---
id: experiment:dg2mvp-w1afix-check
mint_id: 8a62ce21bd2e440798a7b4b88f856d51
type: experiment
parents:
  - hypothesis:row-refuses-thought-markers-and-resolves-a-table-name
  - experiment:dg2mvp-w1a-check
next_edges: []
edited_by: director-general-2
scaffold_hash: b2bb47a34be9f02f
season: 2
title: "W1a corrective post-build: every THOUGHT-marker range now refuses (141/141 on real nodes) and non-THOUGHT rows stay exact (270/270); but the DEVIATION admits a replacement with two blocks or a stray BEGIN, a marker-free range admits injected markers, and `row name:---` picks the separator"
town: core
---
# experiment:dg2mvp-w1afix-check

# DG2 post-build check, W1a corrective: hypothesis:row-refuses-thought-markers-and-resolves-a-table-name (goal:g4.18.5.1.1 + .1.2)
director-general-2 · 00:1xZ 09-30 · MAIN HEAD a2e676b19 · read-only in MAIN; tests and probes ran on `git archive HEAD extensions .agi/context/schemas` in /tmp/dg2mvp/w1afix/tree.
Build: 6aedaa5a7 (mvp:dg3b4-w1a-fix-thought-guard-row-name, recorded by a2e676b19). No later commit touches write.py, node_writer.py, test_write.py or test_node_writer.py.
Probe: /tmp/dg2mvp/w1afix/probe/test_probe_w1afix.py (not committed). Results: probe/{abuse,d_sequence,corpus,name}.txt. A prototype of the corrective is in /tmp/dg2mvp/w1afix/proto (diff: proto.diff), with its results in probe/proto/.

| # | command | observed |
|---|---|---|
| 1 | `git show --numstat 6aedaa5a7` | write.py +38/-8 (net +30; the build discloses 5 of these as docstring or comment, so 25 net code lines). test_write.py +42/-0 |
| 2 | pytest test_write.py (tree) | 153p/5x, 0 failed. `-k w1a`: 5 passed (my 3 rows + DG3's 2 new ones) |
| 3 | pytest test_node_writer.py (tree) + `-k live_tree` on MAIN | 110p/3x, plus 2 setup errors in the tree (the live corpus is not in the archive). Both are green on MAIN, so 112p/3x |
| 4 | abuse (a): the range holds both markers, and the replacement is malformed: BEGIN only · END only · END without `-->` · indented markers. `replace body 5:8 --force` and `row 3`, each also with --dry-run | all 8 refuse with rc 2 (dry-run rc 2 as well), and the file is byte-identical |
| 5 | abuse (a'): both markers, replacement = BEGIN, BEGIN, x, END | **rc 0 on both verbs.** The body now has 2 BEGIN lines and 1 END, and thought_text() starts with a marker line. `_THOUGHT_RE.search` matches BEGIN..END lazily, so the stray BEGIN passes |
| 6 | abuse (b): both markers, replacement carries TWO complete blocks | **rc 0 on both verbs. The body now holds 2 THOUGHT blocks** (the thought_blocks docstring says the schema allows at most one). The admission test only asks whether a block is present, not how many |
| 7 | abuse (b'): the range holds NO marker (a paragraph row), and the replacement brings a complete block · BEGIN only · END only | rc 0 in all 6 cases. Results: 2 blocks · 2 BEGIN/1 END (extract_thought now starts at the injected BEGIN) · 1 BEGIN/2 END. The guard reads only the OLD range, never the new text. This hole predates the build, and it is outside CLAIM (1) as worded |
| 8 | abuse (c): both markers, the replacement drops the THOUGHT: the block row · block + context `3:10` · whole body `1:` | all 5 refuse with rc 2 (dry-run too), and nothing is written. c4, a single marker (BEGIN) whose replacement brings a whole block, also refuses |
| 9 | (d) admitted cases: both markers, the replacement brings one complete new block: `row 3` · `replace body 5:8` · `3:10` with the block mid-text · whole body with the block mid-text | all rc 0 and byte-exact. One block, at the replacement's position, and nothing carried back |
| 10 | (d) sequence on the MID fixture: admitted `row 3`, then `thought third why`, then `row <last>` on the tail | rc 0,0,0. Exactly 1 block after each step, and it stays at line 5 (not moved to the tail) |
| 11 | real-node corpus: the w1a sample (96 nodes, seed 20260929) + the 28 files that were wrong in w1a = 106 files copied to tmp. Every THOUGHT row gets `row n`, `row n:1-1` (BEGIN) and `replace body a:b --force`; the non-THOUGHT picks get `row n` | non-THOUGHT: 270/270 exact. THOUGHT rows: `row n` 47/47 refused cleanly, `n:1-1` 47/47 refused cleanly, `replace body` 47/47 refused cleanly. 0 wrong. The w1a 0/28 is now all refused |
| 12 | the same 47 THOUGHT rows, `row n` with a complete NEW block (the DEVIATION path) | 47/47 rc 0 and byte-exact (one block, in place) |
| 13 | name (1): `verb_row(name:alpha)` parsed, then 2 paragraphs inserted above the table, then `submit` | resolves to `9:9` against the CURRENT body, and the body is exact |
| 14 | name (2): `name:gamma` (0) · `name:beta` (2) · `name:fenced` (a table row inside a ``` fence) | rc 2 on all three, naming NAME ("0 / 2 table rows are named 'beta', want 1"), and the file is byte-identical. Fence and THOUGHT rows are excluded by `a == b` |
| 15 | name (3): body only | `row name:alpha` changes only that line (the body is exact). The frontmatter is untouched apart from provenance, and `row` has no payload route |
| 16 | name (4): the N:M guard on the same line | `replace body 5:5` without --force refuses ("starts inside a paragraph"). `row name:alpha` rc 0 (verb_row sets replace_force), and a 1->2-line replacement is also exact |
| 17 | name (5): --dry-run | prints `row    name:alpha -> 5:5` and `replace body 5:5 (...)`, writes nothing. A missing name gives dry-run rc 2 |
| 18 | name (6): `name:write.py` · `name:manifest.x` | both treated as table names, rc 0, exact. A plain `row manifest.x` still takes BUILD1's frontmatter path (rc 2 "has no manifest mapping") |
| 19 | name (7): `row name:---` on a table with a `\|---\|---\|` separator | **rc 0: line 4 (the separator) is rewritten.** CLAIM (2) and goal:g4.18.5.1.2 say "the separator row skipped". Core a4b077aba skipped it (`set(cell) <= set("-: ")`). `name:k` picks the header row, which core also allowed |
| 20 | name (8): `row name:alpha extra f` | arity 2, so the NAME stops at the first space. rc 2 "source unreadable", nothing written. Core's `replace body NAME f` had the same limit |
| 21 | F3 as spelled: `git grep -n "def body_rows\|_resolve_body_row_range"`, whole repo · the same with `-- extensions/agi/bin` (the goal's spelling) | unscoped: 15 lines, all quoting node text plus one test-name list. Under bin: 1 line (node_writer.py:1014). Not fired as intended |
| 22 | live corpus: 5021 live bodies, marker lines vs thought_blocks | 0 bodies with more than one block, and 0 with a marker line outside a block. A result-side rule would refuse nothing that exists today |
| 23 | prototype (proto.diff, +7/-3 in write.py): the guard also refuses when the SPLICED body has more than one block or a marker line outside a block; `name:` skips `set(name) <= set("-: ")` | #5, #6, #7 and #19 all refuse with the file byte-identical. #9-#12 are unchanged, and a first THOUGHT placed into a thoughtless body is still admitted. test_write 153p/5x, test_node_writer 110p/3x (+2 live on MAIN) |

Invariant note (goal:g4.18.5.1.1): node_writer `_carry_thought` is unchanged, so library whole-body writers still carry the THOUGHT. On a THOUGHT-bearing node, `write.py replace body 1:` with no THOUGHT now refuses instead of carrying, which is what CLAIM (1) and case (c) require.
Out of scope, not raised: `body_patch` and `sub` can still remove a marker line (the goal names only replace body and row).
