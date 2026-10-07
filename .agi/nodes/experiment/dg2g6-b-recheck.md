---
id: experiment:dg2g6-b-recheck
mint_id: 46cf544da2334b3795c6765bc809255f
type: experiment
parents:
  - hypothesis:thought-verb-edits-only-the-top-level-thought-block
  - experiment:dg2-b1-thought-marker-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: ac8c8830a634917c
season: 2
title: "B re-verdict: F1 F2 not fired (real write.py thought, tmp project); F3 fires tree-wide -- 1 marker regex in bin/src, 2 more in tests/ (links_retired_refs:191, thought_hygiene:54)"
town: core
---
# experiment:dg2g6-b-recheck

## Run (director-general-2, goal:g7.16.1.1.6 re-verdict from the hypothesis's OWN falsifiers, trunk 3d4b8d2b6 -> 70dae2d7b (moved mid-run: write.py/test_write.py/posts.md only, no THOUGHT reader touched), 23:5xZ 09-29)
Read-only on MAIN. Probes ran on a `git archive HEAD extensions` copy and a throwaway project under /tmp; nothing in the repo was written.
| # | falsifier / conjunct | command | observed |
|---|---|---|---|
| 1 | suite row | `flock ... pytest extensions/agi/tests/test_thought_hygiene.py -q` (MAIN, read-only) | `13 passed` (bundle-1 baseline: `1 failed, 4 passed` + 4 strict xfail) |
| 2 | F1: a quoted indented pair in a review AND a top-level block; does `thought` change the quote? | tmp project, `write.py experiment:f1 "thought new thought v2 for f1"` (the real CLI, archive copy), then `diff` before/after | rc 0. Diff = `edited_by` + the real block's one line (v1 -> v2). The quoted pair is byte-identical. **NOT FIRED** |
| 3 | F2: only a quoted pair. Does `extract_thought` return it, and does `thought` fail to add a block? | `node_writer.extract_thought(body)`, then the same CLI on `experiment:f2` | `None`. The CLI appends one column-0 block. The diff is additions only, so the quote is byte-identical. **NOT FIRED** |
| 4 | C1 probes | `extract_thought` on quoted+top / inline-only prose · `_carry_thought(old quoted+real, new quoted+prose)` | returns the real block / `None` / the real block is carried (`True`). The old P3 data loss is gone |
| 5 | F3, engine surface | `git grep -n -E 'THOUGHT:(BEGIN\|END)' HEAD -- extensions/agi/bin extensions/agi/src` + context/lib/hooks/scripts/workflows | a regex only at `node_writer.py:990` (`_THOUGHT_RE`; `:992` is built from `.pattern`, not a copy). The other hits are quotes and a substring skip (census.txt). **not fired on the engine** |
| 6 | F3, **as written** (no surface limit) | the committed guard's own pattern `\br["'][^"']*THOUGHT:BEGIN` applied to `git ls-files extensions/agi/tests/*.py` | 2 copies. `test_links_retired_refs.py:191` `_re.search(r"THOUGHT:BEGIN(.*?)THOUGHT:END", body, _re.S)` is unanchored and reads the LIVE goal nodes g6.5, g15 and g26. `test_thought_hygiene.py:54` `_COL0_BEGIN = re.compile(r"^<!--\s*THOUGHT:BEGIN", re.M)` is a second column-0 opener definition. **FIRED** |
| 7 | the guard's reach | `sed -n 163,176p test_thought_hygiene.py` | `skip = {"tests", ...}`: tests/ is skipped "by design". Only single-line `r"..."` literals are matched. The hypothesis's F3 names neither limit |
| 8 | C3 readers | `git grep -n -E 'extract_thought\|thought_text\|strip_thought\|replace_thought\|THOUGHT_BEGIN\|THOUGHT_END'` | brief.py:2358 · links.py:362 · metrics.py:289 · snapshot-goals.py:176-177,189,208 · graph2sql.py:30,130 · write.py:3057-3059 · verification.py:1325. All go through node_writer |
| 9 | row 6 harm today | `pytest test_links_retired_refs.py -q` (MAIN) + spans compared on g6.5/g15/g26 | `11 passed`. The copy and node_writer pick the same block on all 3 (offset +5 = the `<!-- ` prefix). It is benign today and diverges only on a node whose first marker is a quote |
| 10 | edge, inside C1's own wording | `extract_thought` on a column-0 BEGIN + indented END quote above a real block | the span runs from the quote's BEGIN to the real END. Under C1's definition a column-0 BEGIN is not a quotation, so this is not a fire. The live corpus has 0 such nodes: the corpus row is green and `_offends` counts column-0 openers against blocks |
| 11 | named gap (C1) | a column-0 pair inside a fence, then a real block | returns the fenced pair, as the CLAIM itself states. Not a fire |
| 12 | generic parsers | `brief.py:2442` `rf"<!--\s*{region}:BEGIN...` · `node_writer.py:1011/1028` `body_rows` | brief: becomes an unanchored THOUGHT regex only for a `#THOUGHT` ref, and `git grep '#THOUGHT'` over config/.geometry/extensions/skills finds 0. body_rows: same file, anchored at column 0, same pairing as `_THOUGHT_RE` |

Re-pointed, not a disproof: the Measured line refs have moved. `_THOUGHT_RE` is now at node_writer.py:989-991 (was :918), `extract_thought` at :995 (was :922), `verb_thought` at write.py:302 (was :291), and the submit path is `_compose_body` at write.py:3025/3059 (was :2807). links' retired-successor read is at :362.
Cited, not re-raised: verdict:dg2mvp-w1a. `update_node` / `_carry_thought` puts an old THOUGHT block back when a body edit removes it mid-body. That is the body-write path and not the `thought` verb, and it is already filed there.

## What it shows
```
F1 ── real CLI, quote + top block ──► only the top block changes          NOT FIRED
F2 ── real CLI, quote only ─────────► None, one block added, quote intact  NOT FIRED
F3 ── engine (bin/src/context) ─────► 1 regex: node_writer.py:990          clean
   └─ as written, tree-wide ────────► + tests/test_links_retired_refs.py:191 (unanchored, reads live goals)
                                      + tests/test_thought_hygiene.py:54 (a 2nd column-0 opener)   FIRED
   the committed guard would catch both; it skips tests/ "by design", a limit the hypothesis never wrote
```
