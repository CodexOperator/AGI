---
id: verdict:dg2-h2-key-row
mint_id: 6060e03a1cb943fdbcf6fc098ddaa289
type: verdict
parents:
  - experiment:dg2-h2-key-row-baseline
  - hypothesis:posts-key-row-write-never-inserts-a-lone-row
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-h2-key-row-baseline
scaffold_hash: bfdf3016f3b1889f
season: 2
title: "H2: lean proved at 80 -- the first-seating insert lands after trailing keys (lone row + unloadable file, e4aaef794); refuse-or-whole-set + one load check"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2-h2-key-row

## Verdict: inconclusive_lean_proved:80 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-h2-key-row-baseline) | decided by |
|---|---|---|
| (1) a key-row push for a post absent on the target refuses by name or writes the whole row set | FALSE: first seating inserts the one row (:10560-10568). e4aaef794 wrote dg-3 alone, with 0 of the dg-1/-2 rows | `test_rotate_key_authority.py::test_h2a_absent_post_refuses_by_name_never_a_lone_row` |
| (2) every config:posts write is yaml.safe_load-ed before commit, and a file that does not load is never committed | FALSE: 0 load checks before `commit-tree` (:10591). e4aaef794's file raised ScannerError and was live for 1h40m | `test_rotate_key_authority.py::test_h2b_posts_md_that_fails_yaml_load_is_never_committed` |

Lean proved: both conjuncts are small additions to one function. One refusal branch plus one `yaml.safe_load` of the composed frontmatter is about 8 lines, under the 12-line ceiling. The lean is 80 and not higher because conjunct (1) as the CLAIM section words it ("absent -> refuse", always) contradicts the existing `test_c4_first_seating_appends_its_new_row` (:524), which asserts OK on an append. DG3 has to either scope the refusal (refuse unless the whole new row set lands) or rewrite test_c4 inside the 40-line test budget.
CORRECTION: the line refs :10477/:10498/:10568/:10593 are exact. The Measured section omits the root cause: `_insert_row_into_frontmatter` inserts before the CLOSING `---`, and on season2/main two keys (`scaffold_hash`, `thought_session`) follow `posts:`. So the row landed outside the list, and the result was both a lone row and an unloadable file. It was repaired by dcd06014e.
