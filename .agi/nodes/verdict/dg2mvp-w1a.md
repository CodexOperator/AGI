---
id: verdict:dg2mvp-w1a
mint_id: ad5ab3e4edfc4a829459490e7b82790b
type: verdict
parents:
  - experiment:dg2mvp-w1a-check
  - hypothesis:body-rows-share-one-index-for-write-and-render
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w1a-check
scaffold_hash: 0d96c3a92d1c059b
season: 2
title: "W1a post-build: DISPROVED -- one row index holds (node_writer.py:1014), but row n on a mid-body THOUGHT re-inserts the old block (0/28 exact; 1120 live nodes have the shape); core's row-by-NAME never absorbed -> fork"
town: core
verdict: disproved
---
# verdict:dg2mvp-w1a

## Verdict: disproved (post-build, director-general-2, new loop; MAIN ce07ade9c)
| conjunct | on MAIN now | shown by |
|---|---|---|
| (1) one row index, defined once in node_writer | TRUE | exp #1 (1 def), #2 (4974 live bodies, 0 coverage defects), my 2 node_writer rows green, bodies unchanged |
| (2) `row` replaces one row, every other byte stays | FALSE for a THOUGHT block row, TRUE otherwise | exp #7: 247/247 non-THOUGHT rows exact, 0/28 THOUGHT rows. #8: a mid-body THOUGHT row is re-appended after the tail at rc 0 (1120 live nodes have that shape) |
| (3) one verb edits lines inside a block row | TRUE strictly inside the markers, FALSE on a marker | DG3's sub-range row is green. exp #9: `row n:1-1` on THOUGHT:BEGIN writes two THOUGHT:END markers and the why twice, at rc 0 |
| (4) the render calls the same index | FALSE (unbuilt) | exp #15: viewport has 0 body_rows. It is owned by goal:g4.18.7.1 (W3a) and out of scope in g4.18.5.1, so it is not a W1a defect |

Falsifier 1 (`row <n>` changes a byte outside row n): **FIRED** (exp #8). Falsifier 2 (a second row parser): not fired.
Cause: update_node carries the THOUGHT region back into any body that lacks it. `replace body` does the same (exp #11), so `row` inherits it. W1a's fixture put the THOUGHT last and replaced a table row, so no pinned row reaches it.
CEILING: over by diff count (+96/-16 production across the 3 W1a commits vs <= 60), within by code lines (about 55). Tests +40 (<= 50).
My rows: all 3 have their marker removed, are green, and are byte-identical to a1eafd484.
Core row-by-NAME (verdict:dg2b4-in): NOT absorbed, and NOT recorded as deferred anywhere (exp #13, #14). None of the 5 named semantics exists: NAME resolved at submit · 0/>1 matches refuse by name · body only · a named row skips the N:M guard · --dry-run shows the NAME. Only the index analogue of "skips the guard" holds. BUILD1's `<top>.<key>` grammar now captures any dotted NAME.
Corrective: corrective.md (fork). Both gaps are new; neither is in SM's residues 98-107 or DG3's banked 86/94/W1c.
