---
id: experiment:dg2b4-w1c-baseline
mint_id: 5d65db37e3244a72a73b798065fb8acb
type: experiment
parents:
  - hypothesis:posts-rows-have-one-writer-and-one-parser
next_edges: []
edited_by: director-general-2
scaffold_hash: a96a0c4a5d329af2
season: 2
title: "W1 B2 baseline: 4 posts commit paths, each with its own hash-object plumbing; _posts_load_error def + 4 calls; _row_names 1 def/2 calls"
town: core
---
# experiment:dg2b4-w1c-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk a795dbd0e, 20:50Z 09-29)
bin/ is byte-identical a5848c5a2..a795dbd0e; the test patch is based on a795dbd0e.

| # | command | observed |
|---|---|---|
| 1 | `git grep -n -e 'def _ack_commit_seats' -e 'def _publish_row_to_authority' -e 'def _commit_spawn_row' -e 'def _commit_stops_row' -- extensions/agi/bin/rotate.py` | :10305 / :10606 / :10771 / :18366, all as Measured |
| 2 | F3 `git grep -n -e '_posts_load_error(' -e 'def _row_names' -e '_row_names(' -- extensions/agi/bin/rotate.py` | `_posts_load_error(` = **5 matches = def :10552 + 4 calls** (:10350 :10685 :10844 :18400), one per path. `def _row_names` :10564, 1 call line :10678 (2 calls, authority path only) |
| 3 | `_own_row_line` :9887, `frontmatter.split_frontmatter` frontmatter.py:25 | as Measured. `_posts_load_error` splits by `content.split("---\n")[1]`, not the line-anchored reader |
| 4 | `git grep -n 'import frontmatter' -- extensions/agi/bin/rotate.py` | rotate.py:78 binds `frontmatter` to **graph_core.persistence.frontmatter** (`load_node_file`, a path-based, strip()=="---" splitter), NOT bin/frontmatter.py. The name the claim means is taken |
| 5 | F1 the commit plumbing per path (`sed -n` each body; `inspect.getsource` count of `hash-object`) | **4/4 own their own** temp-index `read-tree`/`hash-object`/`update-index`. ack, spawn_row and stops_row commit on HEAD. authority commits `commit-tree` on **FETCH_HEAD** and pushes. stops_row commits **card + row** as one commit. No two are the same shape |
| 6 | F2 non-loading posts.md committed? existing test_rotate_key_authority.py::test_h2b_* (4 paths) | already refused on all 4 (bundle 3, goal:g4.18.4). Not re-run: outside this row's named files |
| 7 | other posts.md writers: `git grep -n -e '"commit"' -e commit-tree -- extensions/agi/bin/rotate.py` | the other commits (:11047 after_join record, :11143 rotation record + seq) touch no posts.md, so there are exactly 4 |
| 8 | core `git show 8e4b4c286 / origin/core/season2/main : rotate.py \| grep -c` | `_posts_load_error` 0/0 and `_row_names` 0/0: both are trunk-only (bundle 3). Core keeps the 4 paths (:10212 :10478 :10634 :18228) without a load gate. 0 core hunks for W1 B2 |
| 9 | test_write_self_row.py, baseline then with rows (one file, lock, basetemp) | 7 passed -> **8 passed** |
| 10 | test_rotate.py, baseline then with rows | 343 passed, 1 skipped -> **343 passed, 1 skipped, 2 xfailed** |

## What it shows
```
_ack_commit_seats  --_posts_load_error--> tmp index on HEAD        --commit
_commit_spawn_row  --_posts_load_error--> tmp index on HEAD (x5)   --commit
_commit_stops_row  --_posts_load_error--> tmp index on HEAD, card+row --commit
_publish_row_to_authority --_row_names x2, _posts_load_error--> tmp index on FETCH_HEAD --commit-tree --push
claim: all 4 --> ONE row write (YAML-load via the one parser, then commit)   helpers gone
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_rotate.py::test_b4_w1b2_no_second_posts_parser_in_rotate`: rotate.py holds neither `def _row_names` nor `_posts_load_error(`
`extensions/agi/tests/test_rotate.py::test_b4_w1b2_the_four_posts_paths_own_no_commit_plumbing`: none of the 4 paths' source carries its own `hash-object` (the plumbing lives in the one row write)
`extensions/agi/tests/test_write_self_row.py::test_b4_w1b2_a_row_write_leaves_one_loading_name_per_row`: plain passing guard (goal:g4.18.4 invariant, TRUE today): a self-row write leaves a file that YAML-loads with one `name` per row
