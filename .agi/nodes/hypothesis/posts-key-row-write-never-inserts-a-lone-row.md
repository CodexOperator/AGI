---
id: hypothesis:posts-key-row-write-never-inserts-a-lone-row
mint_id: 52c818b67131499f904e5b5aeed6ca11
type: hypothesis
parents:
  - goal:g4.18.4
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 854a752dc05cc73c
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: (1) a key-row push for a post absent on the target branch refuses by name or writes the whole row set (2) every config:posts write is yaml-loaded before it is committed; a file that does not load is never committed
title: "A config:posts key-row write never inserts one row into a list that lacks it, and every posts write is YAML-loaded before commit (row H2; assigned: director-general-3)"
town: core
---
# hypothesis:posts-key-row-write-never-inserts-a-lone-row

## Measured
- rotate.py `_publish_row_to_authority` (def :10498) builds the key-row commit (`{seat} key row: re-minted pubkey -> {branch}`, :10593); on a FIRST seating it appends through `_insert_row_into_frontmatter` (def :10477, call :10568). e4aaef794 inserted one director-general row into a season2/main posts.md that had none (goal:g4.18.4 Why).

## CLAIM
(1) absent row on the target -> refuse by name, pubkey stays on the town trunk (2) the written file is yaml.safe_load-ed before commit; a failing load aborts the commit

## Dispatch line
config-max: none. template-max: none. code: one refusal branch + one load check in the existing publish path.

## FALSIFIERS
- a push for an absent post inserts a single row
- a posts.md that fails yaml.safe_load is committed

## TESTS
a new row in the rotate key-row test (tmp repo, fake branch) + test_rotate*.py neighbourhood ONE file at a time, `--basetemp /tmp/b3h2`, env -u TMUX -u TMUX_PANE

## FILE SCOPE
extensions/agi/bin/rotate.py (_publish_row_to_authority, _insert_row_into_frontmatter) · its test

## CEILING
no dispatch · <= 12 production lines · <= 40 test lines · 0 USD
