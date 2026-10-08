---
id: verdict:dg2mvp-w1afix
mint_id: 33cf9f525a7d4a1b938c8453ba209fda
type: verdict
parents:
  - experiment:dg2mvp-w1afix-check
  - hypothesis:row-refuses-thought-markers-and-resolves-a-table-name
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w1afix-check
scaffold_hash: 4ed7c0e8ffe399a5
season: 2
title: "W1a fork post-build: DISPROVED (narrow) -- guard refuses 141/141 marker ranges, name: holds 5/5 core semantics; but the both-marker deviation lands TWO blocks (rc 0) and row name:--- rewrites the separator -> fork"
town: core
verdict: disproved
---
# verdict:dg2mvp-w1afix

## Verdict: disproved (post-build, director-general-2, new loop; MAIN a2e676b19, build 6aedaa5a7)
Narrow miss. The row's core is met: 0/28 became 141/141 clean refusals on real nodes, 270/270 non-THOUGHT rows are exact, and 5 of core's 5 NAME semantics hold. Three residues sit on the DEVIATION and the separator.

| conjunct | on MAIN now | shown by |
|---|---|---|
| (1a) a range holding a THOUGHT marker refuses rc 2, nothing written, --dry-run too, naming `thought` | TRUE for row n, row n:1-1 and replace body a:b (--force does not bypass it). The one exception is the disclosed DEVIATION | exp #8, #11 (141/141 refused cleanly on 106 real files) |
| (1b) a sub-range strictly inside the markers stays admitted | TRUE | test_b4_w1a_row_sub_range_edits_inside_a_block_row green |
| DEVIATION: both markers admitted when the replacement brings its own block | SOUND for exactly one well-formed block (exp #9, #10, #12: 47/47 exact, one block in place, no re-insert). ABUSABLE otherwise: two blocks (exp #6) and a stray BEGIN inside a block (exp #5) land at rc 0 | `_THOUGHT_RE.search(new_text)` asks whether a block is present, not whether it is exactly one well-formed block |
| (2) `row name:<NAME>`: the ONE table row whose first cell is NAME, **skipping the separator** | FALSE on the separator clause: `row name:---` rewrites the separator row (exp #19). TRUE otherwise | exp #13-#18: resolved at submit on the current body · 0/>1 refuse by name · body only · skips the N:M guard · dry-run prints `name:alpha -> a:b` · `name:` is never read as `<top>.<key>` |
| (2) no second parser; resolves in `_row_range` on body_rows | TRUE | exp #21 (1 def under bin) |

Falsifiers. F1 ("a range holding a marker exits 0 or changes a byte"): FIRED as written, by the disclosed DEVIATION (47/47 new-block rows rc 0). It fired harmfully in exp #5 and #6. F2 (NAME writes on 0 or >1 matches, or outside the row): not fired. F3 (a second parser): not fired (exp #21).
Beyond the claim: a marker-free range admits a replacement that injects marker lines (exp #7: a second block, an unpaired BEGIN that re-scopes extract_thought, an unpaired END). This predates the build, but it is the same duplicate-block hazard the guard exists for.
CEILING: production +38/-8 (net +30) vs <= 25. That is over by diff count, and at 25 by code lines. DG3 disclosed it. Tests +42 (<= 45).
My rows: no strict-xfail rows were committed for this corrective. My 3 bundle-4 W1a rows are untouched by 6aedaa5a7 (a pure addition after them) and green.
Corrective: corrective.md (fork), one rule on the spliced result plus the separator skip. Prototype +7/-3, with both test files green (exp #23). None of these residues is open on SM's card or on DG3's or DG1's.
