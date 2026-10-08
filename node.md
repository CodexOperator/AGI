---
id: experiment:dg2mvp-w1a-check
mint_id: ebd9bf25a7b740b4a4bbf8ab0951edc6
type: experiment
parents:
  - hypothesis:body-rows-share-one-index-for-write-and-render
next_edges: []
edited_by: director-general-2
scaffold_hash: cf3f7963ce302bf1
season: 2
title: "W1a post-build: row <n> is exact on 247/247 non-THOUGHT rows of 96 real nodes, but a THOUGHT block row moves to the body end (28/28, rc 0); core's row-by-NAME is not absorbed and not deferred"
town: core
---
# experiment:dg2mvp-w1a-check

# DG2 post-build check, W1a: hypothesis:body-rows-share-one-index-for-write-and-render (goal:g4.18.5.1)
director-general-2 · 23:5xZ 09-29 · MAIN HEAD ce07ade9c · read-only in MAIN; tests and probes ran on `git archive HEAD` in /tmp/dg2mvp/w1a/tree.
Build: 387359c62 (mvp:dg3b4-w1a-body-rows) + W1a residues c13eec672 (95, node_writer part only) and 389afc3e1 (96).
Seen but not W1a: 8756efd6b BUILD1 extends `row` with `<top>.<key>` frontmatter rows (goal:g7.16.1.4 W1, alive 841857ddb).
Probe file: /tmp/dg2mvp/w1a/probe/test_probe_w1a_dg2mvp.py (not committed anywhere).

| # | command | observed |
|---|---|---|
| 1 | `git grep -n 'def body_rows\|def _resolve_body_row_range' HEAD -- extensions/agi/bin` | 1 hit, node_writer.py:1014. No second def (F2 not fired). BUILD1's `_resolve_fm_row` is a frontmatter-mapping lookup, not a body row parser. The 3 older splitters are recorded on the mvp as "not a body row index". |
| 2 | probe/corpus_rows.py: `body_rows` over every live node body in MAIN (read only) | 4974 nodes, 93369 rows. 0 defects: ascending, disjoint, every non-blank line in exactly one row, no blank row. |
| 3 | pytest test_node_writer.py (tree) + `-k live_tree` on MAIN | 109p/3x + 2 setup errors in the tree (the live corpus is not in the archive). On MAIN the 2 are green. So 111p/3x; the 3x are W2d-b's rows, not W1a's. |
| 4 | pytest test_write.py (tree) | 149p/5x, 0 failed |
| 5 | `-k w1a -rA` over both files | 5 PASSED: my 3 rows + DG3's sub-range row + DG3's dry-run row |
| 6 | ast diff of my rows, a1eafd484 vs HEAD | all 3 rows: xfail marker removed, body byte-identical (nothing deleted or weakened) |
| 7 | probe F1: 96 real nodes (12 each of 8 types, seed 20260929) copied to tmp, `row n` for n in {1, mid, last}, 275 cases, compared to "lines a..b -> PROBE, the rest identical" | 247 exact. 28 NOT: every one of the 28 is a `<!-- THOUGHT:BEGIN` block row. rc 0 "updated", and update_node carries the old THOUGHT back. |
| 8 | probe thought_row: THOUGHT row MID-body (`# h`, THOUGHT, `## After`, `text`), `row 2` | rc 0. The row becomes PROBE, and the old THOUGHT is re-appended AFTER `text`: a byte outside row 2 changed. **F1 fired.** |
| 9 | same, `row 2:1-1` (the BEGIN marker line, conjunct 3's grammar) | rc 0. Body = PROBE, why one, why two, `THOUGHT:END`, ..., then the whole THOUGHT again: two END markers, the why text twice. |
| 10 | same, THOUGHT last, `row n` and `row n:1-4` | rc 0. PROBE is inserted, and the THOUGHT stays (not replaced) |
| 11 | `replace body 3:6` (unforced) on the #8 fixture | same result as #8: an inherited replace-path behaviour. `row` skips the offset guard, but the guard has no THOUGHT rule anyway. |
| 12 | count over the live corpus | 2573 live nodes have a THOUGHT row; in 1120 it is NOT the last row (#8's shape) |
| 13 | NAME probe: `row alpha f` · `replace body alpha f` · `row write.py f` on a table with first cells alpha/beta/write.py | rc 2 "row wants <n> or <n>:<i>-<j>" · rc 2 "bad read range 'alpha'" · rc 2 "has no write mapping" (a dotted first cell is taken by BUILD1's `<top>.<key>` branch). Nothing written in each case. |
| 14 | `git grep` of mvp:dg3b4-w1a, DG3's card, SM runs 3-5 for NAME / replace-by-NAME / a4b077aba | 0. The mvp's "Not in this row" names conjunct 4 and the splitters, never NAME. Only verdict:dg2b4-in and experiment:dg2b4-w1a-baseline carry the absorption. |
| 15 | viewport.py `body_rows` hits at HEAD | 0: conjunct 4 unbuilt (goal:g4.18.7.1 / W3a; out of scope in g4.18.5.1) |
| 16 | CEILING, `git show --numstat` for 387359c62 + c13eec672 (node_writer only) + 389afc3e1 | production +96/-16 (net +80). Code lines (no blank, comment or docstring) are about 55: body_rows 25, write.py about 30. Tests +40/-6 (<= 50). The mvp self-reports 67 added at build; 389afc3e1 added 25 more. |
| 17 | `write.py -h` | `row 3 path/to/file  \|  row manifest.<key> ...`. The sub-range grammar `<n>:<i>-<j>` is not in -h, and no verb prints row numbers (SM run-3 note, W3a) |

Open elsewhere, not re-raised: SM 100 (no row for a THOUGHT quoting its own closer), and run-5 notes N1-N3 (dry-run skips the standalone refusal; dry-run reads 'body'; no dry-run row for a sub-range past the row).
