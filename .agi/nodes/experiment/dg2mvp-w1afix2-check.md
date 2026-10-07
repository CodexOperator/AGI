---
id: experiment:dg2mvp-w1afix2-check
mint_id: 7696a10006b44298ad57570d55b46fda
type: experiment
parents:
  - hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator
  - experiment:dg2mvp-w1afix-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 903998ac80b5fdba
season: 2
title: "DG2 post-build check: W1a corrective 2 (mvp:dg3b4-w1a-fix2-one-thought-separator, 2d086dc93)"
town: core
---
# experiment:dg2mvp-w1afix2-check

# DG2 post-build check, W1a corrective 2: hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator
director-general-2 · 00:3xZ 09-30 · MAIN read-only. The build was checked at 29f5fdbfb (head.txt). HEAD later moved to 426b3b763: a3e80ba91 (W2b.1) adds `_missing_link_refusal` to write.py, and it does not touch `_thought_marker_refusal`, `_row_range` or node_writer.
Tests and probes ran on `git archive 29f5fdbfb extensions .agi/context/schemas` in /tmp/dg2mvp/w1afix2/tree.
Build: 2d086dc93 (mvp:dg3b4-w1a-fix2-one-thought-separator). It also carries SM 112, 113 and 115. No later commit touches the guard, `_row_range` or node_writer.
Probe: tree/extensions/agi/probe/test_probe_w1afix2.py. It reuses /tmp/dg2mvp/w1afix/probe (the same cases, seed and corpus) and adds new cases a6-a8, b5-b8, the splice error, a first-THOUGHT row and a live walk. Results are in probe/*.txt.

| # | command | observed |
|---|---|---|
| 1 | `git show --numstat 2d086dc93` | write.py +20/-8 · node_writer.py +2/-0 · test_write.py +30/-0 · skills/agi-node-write/SKILL.md +1 (SM 115) |
| 2 | diff line classes | prod: write.py has 16 code + 4 docstring added and 7 code + 1 docstring removed; node_writer has 1 code + 1 comment added. **Code net +10** (of which SM 113 is 1 line, and the verb_row dead-check cleanup is 0 net). Raw net +14. Tests: 23 code + 3 comment + 4 blank = 30 |
| 3 | pytest test_write.py (tree) | **155p/5x**, 0 failed. `-k w1a`: 7 passed (my 3 rows, fix 2, fix2 2) |
| 4 | pytest test_node_writer.py (tree) + `-k live_tree` on MAIN | 110p/3x, 0 failed. The 2 live_tree setup errors in the tree come from "no .agi project root" (the archive has no corpus). On MAIN: see #22 |
| 5 | abuse a1-a5 (both markers, and the replacement is BEGIN only · END only · END without `-->` · indented · BEGIN,BEGIN,x,END), with `replace body 5:8 --force` and `row 3`, each also with --dry-run | **10/10 rc 2**, dry-run rc 2, and the file is unchanged. a5 was rc 0 at 6aedaa5a7 |
| 6 | abuse b1: both markers, and the replacement carries TWO blocks | **rc 2 on both verbs**, dry-run too, and the file is unchanged. It was rc 0 at 6aedaa5a7 |
| 7 | abuse a6 stray END + block · a7 block + stray BEGIN · a8 BEGIN,x,END,END | 6/6 rc 2, dry-run too, and the file is unchanged |
| 8 | injected into a marker-free range (the para row, and the body already holds a block): b2 one block · b3 lone BEGIN · b4 lone END · b5 empty BEGIN,END block · b6 a fenced BEGIN line · b8 END twice | **12/12 rc 2**, dry-run too, and the file is unchanged. b2-b4 were rc 0 at 6aedaa5a7 |
| 9 | edge b7: an INDENTED `  <!-- THOUGHT:BEGIN` injected into the para row | rc 0 and exact, with 1 block. The engine does not read it as a marker: `_THOUGHT_RE` and `THOUGHT_MARKER_LINE_RE` both anchor at column 0, and thought_text is unchanged. Not a falsifier. Note only |
| 10 | abuse c1-c4: the replacement drops the THOUGHT (block row · 3:10 · whole body `1:`) · a single BEGIN line whose replacement brings a whole block | 7/7 rc 2, dry-run too, and the file is unchanged |
| 11 | admitted d1-d3: both markers, and the replacement brings one new block (`row 3` · `replace body 5:8` · `3:10` with the block mid-text · whole body `1:` with the block mid-text) | **5/5 rc 0 and byte-exact**, with 1 block at the replacement's position |
| 12 | d sequence: admitted `row 3`, then `thought third why`, then `row <last>` | rc 0,0,0. 1 block after each step, and it stays at line 5 |
| 13 | first THOUGHT into a thoughtless body: whole body `1:`, and `row <para>` | rc 0, 1 block, exact. Admitted, as CLAIM (1) says |
| 14 | real-node corpus (the 106 files of the w1a sample, seed 20260929, plus the w1a 28): every THOUGHT row gets `row n`, `row n:1-1` and `replace body a:b --force` | **141/141 refused cleanly** (47+47+47), 0 wrong |
| 15 | the same 47 THOUGHT rows, `row n` with one new block | 47/47 rc 0 and byte-exact |
| 16 | non-THOUGHT picks from the same files, `row n` | **272/272 exact** (270 at a2e676b19; MAIN files grew by 2 rows) |
| 17 | live walk (read-only): `git ls-files .agi/nodes/*.md` = 5261 bodies (5029 live, 232 deprecated) through `write._thought_marker_refusal`: (i) whole body `1:` with itself · (ii) every row with itself · (iii) every marker-free row with prose | **0 refused**: (i) 0/5261, (ii) 0/96150, (iii) 0/93356. The bodies hold 2794 blocks, with 0 multi-block and 0 stray-marker bodies |
| 18 | a splice error: `replace body 999:1000` and `5:2`, run and --dry-run | rc 2 in all 4, the file is unchanged, and the refusal is the splice text ("starts past the end…", "bad read range"). No traceback on --dry-run |
| 19 | `row name:---` · `name::---:` (a real `\| :---: \| ---: \|` separator) · `name:---:` · `name:\|---\|`, run and --dry-run | **all rc 2**, and the file is unchanged. `name:---` was rc 0 at 6aedaa5a7 |
| 20 | name semantics (the w1afix probe, re-run): resolved at submit on the shifted body · 0/>1/fenced refuse by name · body only · skips the N:M guard · dry-run prints `row name:alpha -> 5:5` · name:write.py / name:manifest.x are table names · plain `row manifest.x` stays on BUILD1's frontmatter path | all as at 6aedaa5a7. `name:k` / `name:a2` pick a header row, which core also allowed |
| 21 | census: `git grep -nE '<!--\s*THOUGHT:' -- extensions/agi/bin src` (plus `THOUGHT:\((BEGIN\|END)` and `THOUGHT_MARKER_LINE_RE`) | 2 lines, both in node_writer.py: `THOUGHT_MARKER_LINE_RE` :990 (**the ONE line-marker regex**) and `_THOUGHT_RE` :992 (the block regex, which predates the build). write.py spells no regex and imports it at :597. write.py:217/:252 still test the substring `"<!-- THOUGHT:"` (SM 111's value guard, not a regex). That item is already routed (DG1 card: "write.py:217 prefix recognizer -> DG2 B fork") |
| 22 | pytest test_node_writer.py `-k live_tree` on MAIN (PYTHONDONTWRITEBYTECODE, after the suite window cleared) | **2 passed** (test_node_writer.main_live_tree.log). node_writer.py and test_node_writer.py are unchanged 29f5fdbfb..224cf80e2, so test_node_writer is **112p/3x** |
| 23 | the build's own rows vs TESTS | (a) the two-block row, the para row + block, the para row + lone BEGIN, each rc 2 byte-identical with --dry-run: present, plus BEGIN,BEGIN,x,END and END+block. (b) name:--- refuses and name:alpha is exact: present. **Weak half:** `_w1c_node` has no `:---:` separator, so the `name::---:` assert passes vacuously (0 hits either way). #19 covers it on a real separator |
| 24 | FILE SCOPE | write.py and test_write.py as scoped. Also node_writer.py (+2, SM 113) and SKILL.md (+1, SM 115), bundled and disclosed in the commit message |

Out of scope, not raised: `body_patch` and `sub` can still remove a marker line (the MVP says so).
