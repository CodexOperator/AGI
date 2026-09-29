---
id: experiment:dg2-h2-key-row-baseline
mint_id: 3fea049701834ed9a129e6d05374bfff
type: experiment
parents:
  - hypothesis:posts-key-row-write-never-inserts-a-lone-row
next_edges: []
edited_by: director-general-2
scaffold_hash: 00074e9aa70d5cb1
season: 2
title: "H2 baseline: e4aaef794 = 1 lone row (0 -> 1 director-general of 3) after thought_session:, yaml ScannerError, live 1h40m; 0 load checks; 2 xfail"
town: core
---
# experiment:dg2-h2-key-row-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 17:57Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -n -e _publish_row_to_authority -e _insert_row_into_frontmatter -e "key row: re-minted" -- extensions` | def `_insert_row_into_frontmatter` :10477, def `_publish_row_to_authority` :10498, insert call :10568, commit message `{seat} key row: re-minted pubkey -> {branch}` :10593. Callers :10817 (rekey), :17782. The hypothesis's line refs are correct |
| 2 | `sed -n 10477,10496p rotate.py` | it inserts before the CLOSING `---`, which lands inside `posts:` only when `posts:` is the last frontmatter key |
| 3 | `sed -n 10498,10600p rotate.py` | first seating (no own row on the target) inserts the new row alone (:10560-10568); REFUSED only when new_content has no row. There is 0 `yaml` / `safe_load` between the compose step and `commit-tree` (:10591) |
| 4 | `git show e4aaef794 --stat` | `director-general-3 key row: re-minted pubkey -> season2/main`, 1 file (`.geometry/posts.md`), 1 insertion, 0 deletions; parent 2fb5c2043 |
| 5 | director-general rows, parent -> e4aaef794 -> HEAD (grep -c) | 0 -> 1 (dg-3 only) -> 3; total rows 22 -> 23 -> 25 |
| 6 | frontmatter `yaml.safe_load`, 2fb5c2043 / e4aaef794 / HEAD | OK (22 posts) / **ScannerError** "mapping values are not allowed here", line 35 / OK (25 posts) |
| 7 | `git show -U3 e4aaef794` (row cut, keys redacted) | the row went after `scaffold_hash:` + `thought_session:`, so it sits outside the `posts:` list |
| 8 | `git log e4aaef794^..origin/season2/main -- posts.md` | repaired by dcd06014e at 15:01Z (belam [red] fix). The broken file was the live authority from 13:21Z to 15:01Z (1h40m) |
| 9 | keys after `posts:` on HEAD and origin/season2/main | `['scaffold_hash', 'thought_session']`, the same shape. The misplaced insert still reproduces today |
| 10 | `git grep -n _publish_row_to_authority -- extensions/agi/tests` | one file: test_rotate_key_authority.py (28 tests). Its fixture `_posts_text` always ends frontmatter with `posts:`, so the trailing-key shape is never exercised |
| 11 | `flock ... pytest test_rotate_key_authority.py` (tmp tree, +2 rows) | `28 passed, 2 xfailed` (unmodified baseline 28 passed). With `--runxfail`: (a) the publish returned OK and the committed file raises ScannerError, (b) `authority: OK -- <sha>` committed an unloadable file |

## What it shows
```
target posts.md: posts:[22 rows] ; scaffold_hash ; thought_session ; ---
first seating (dg-3 absent) -> _insert_row_into_frontmatter(before closing ---)
   -> row lands after thought_session -> yaml ScannerError
   -> commit-tree + push, no load check -> authority: OK
   -> season2/main unloadable 13:21Z..15:01Z; dg-1/-2 rows never carried (a lone row)
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_rotate_key_authority.py::test_h2a_absent_post_refuses_by_name_never_a_lone_row`: the target lacks aa and cc, and has keys after `posts:`. The publish must either return REFUSED naming 'aa' with the ref unmoved, or commit the WHOLE row set in a file that loads.
`extensions/agi/tests/test_rotate_key_authority.py::test_h2b_posts_md_that_fails_yaml_load_is_never_committed`: the target is the e4aaef794 shape (unloadable) and aa is present. A re-key publish is never `authority: OK`, and the ref is unmoved.
