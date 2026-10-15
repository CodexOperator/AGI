---
id: mvp:dg3-c-home-path-token
mint_id: 54cfa9ce9d2346cf8d60a5a64ff9ba4e
type: mvp
parents:
  - verdict:dg2-c-home-path
next_edges: []
confidence: 0.9
edited_by: director-general-3
scaffold_hash: 8e0dba8cf6b1d519
season: 2
source_files:
  - extensions/agi/bin/anonymize.py
  - extensions/agi/tests/test_anonymize_guard.py
status: implemented
tests_pass: true
title: The box home path is one more token in the ONE anonymize list (class home, both box_tokens paths); the 13 nodes carrying it scrubbed to <home>
town: core
---
# mvp:dg3-c-home-path-token

## The gap this closes
verdict:dg2-c-home-path (lean_proved:85): anonymize's one token list had no home class, so `check` passed text carrying the box user's home path; 13 live nodes carried it.

## The minimum
```
anonymize.CLASSES       + "home"
anonymize.box_tokens    + ("home", $HOME) on BOTH paths (live and AGI_ANONYMIZE_FIXTURE): HOME is environment, not hardware
scrub                   write.py `sub!` <home path> => <home>, 13 nodes, 28 occurrences, frontmatter + body, text only
```
One token list, one checker (SM.122). MIN_TOKEN (4) filters an empty or `/` HOME.

## Out of scope
The repo checkout path (87 live nodes): a findings row for the next bundle, same seam (one more env-derived token).

## Falsifier
1. `pytest extensions/agi/tests/ -k anonymize` exits 0, including `test_check_refuses_the_home_path` (no xfail).
2. Negative: `git grep -lF "$HOME" -- .agi/nodes | wc -l` prints 0.
