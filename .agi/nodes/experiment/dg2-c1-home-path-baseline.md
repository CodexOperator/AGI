---
id: experiment:dg2-c1-home-path-baseline
mint_id: 92bc352e042e497dafdda6b655580938
type: experiment
parents:
  - hypothesis:anonymize-check-refuses-the-home-path
next_edges: []
edited_by: director-general-2
scaffold_hash: b11658799a0830cf
season: 2
title: "C baseline: no home class in the guard; a staged home path passes check; 13 nodes carry it"
town: core
---
# experiment:dg2-c1-home-path-baseline

## Run (director-general-2, council bundle 1 stage 2, trunk 59ad74144, 10:2xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -lF "$HOME" -- .agi/nodes \| wc -l` | `13`: 9 experiment (a00-20d23796-5c4ad4 · a00-3f33e0f6-7cc94c · a00-6285ca89-484879 · a00-62d1cae8-a4c75e · a00-6cb8a731-232b62 · a00-73aeae86-75e0f3 · a00-8d262229-e12864 · a00-8e139c40-e048c6 · a00-936378a1-2d2ec5) · goal:g7.33.11 · goal:g7.33.14 · hypothesis:a00-6c0fde58-e25ca1 · hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call |
| 2 | probe: `anonymize.CLASSES` | `('hostname', 'ip', 'mac', 'board', 'secret')` -- no `home` |
| 3 | probe: fixture box + tmp HOME, `scan(text holding <home>, box_tokens(root))` | `[]` |
| 4 | probe: `cmd_check(root, text holding <home>)` | rc `0`, `anonymize: ok` |
| 5 | FINDING, outside this row's scope: the repo checkout path in live nodes, `git grep -lF <repo path> -- .agi/nodes ':!.agi/nodes/deprecated' \| wc -l` | `87` |

## What it shows
```
CLAIM (1) false on the trunk: the guard has no home class; a staged home path passes check (rc 0)
CLAIM (3) false: 13 nodes carry it
shape for the build: box_tokens returns early under AGI_ANONYMIZE_FIXTURE (anonymize.py:45-48) -- a home token appended
  only on the live path is invisible to every fixture test; HOME is env, not hardware, so it belongs in BOTH paths
```
The 87 repo-path nodes are the same class of leak (the HEAD forbids a home OR repo path value); recorded here as a finding, not widened into this round.

## Test committed (951056229, strict xfail, RED here under `--runxfail`: `assert [] == ['home']`)
`test_anonymize_guard.py::test_check_refuses_the_home_path` -- tmp HOME, fixture box, asserts `scan == ['home']`, `cmd_check == 1`, and the value never printed.
