---
id: verdict:dg2b4-w1c
mint_id: 14f157c92fa546eca6dfcd061578461d
type: verdict
parents:
  - experiment:dg2b4-w1c-baseline
  - hypothesis:posts-rows-have-one-writer-and-one-parser
next_edges: []
confidence: 0.6
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w1c-baseline
scaffold_hash: 7911798ebe03de8f
season: 2
title: "W1 B2: lean proved at 55 -- 4 posts.md commit paths each with its own plumbing; one writer needs parent-ref + extra-blob params, never W1b's working-tree commit"
town: core
verdict: inconclusive_lean_proved:55
---
# verdict:dg2b4-w1c

## Verdict: inconclusive_lean_proved:55 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w1c-baseline) | decided by |
|---|---|---|
| (1) one row write, called by all 4 | FALSE: 4/4 own their plumbing (3 on HEAD, 1 on FETCH_HEAD + push; stops_row = card + row) | test_rotate.py::test_b4_w1b2_the_four_posts_paths_own_no_commit_plumbing |
| (2) it YAML-loads the result before the commit | TRUE per path today (4 hand calls of _posts_load_error) | test_rotate_key_authority.py::test_h2b_* stay green, plus test_write_self_row.py::test_b4_w1b2_a_row_write_leaves_one_loading_name_per_row (guard) |
| (3) _posts_load_error and _row_names removed, callers on the one parser | FALSE: def + 4 calls; def + 2 calls | test_rotate.py::test_b4_w1b2_no_second_posts_parser_in_rotate |

Lean slightly proved. (3) is cheap and the helper consolidation is net-negative in lines, so the ceiling of 50 net holds. The risk is (1): "goal:g4.18.5.2's commit" (W1b: an exact-path working-tree commit in write.py) is the wrong mechanism for these paths.
- They commit own-row-only content through a throwaway index, never the shared working tree.
- The authority path commits on FETCH_HEAD and pushes.
One row write needs parent-ref + extra-blob parameters, or it breaks the own-row guarantee. Also, rotate.py:78 already binds `frontmatter` to graph_core's splitter, so the one parser needs another import name.
CORRECTION: "_posts_load_error (:10552, 5 calls)" is 5 matches = the def + **4** calls (one per path). `_row_names` has 1 call site (:10678, two calls), authority path only.
