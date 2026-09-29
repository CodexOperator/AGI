---
id: hypothesis:posts-rows-have-one-writer-and-one-parser
mint_id: 169c85545a0f467480e4270338e06096
type: hypothesis
parents:
  - goal:g4.18.5.3
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 98883552438d7437
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: rotate's 4 config:posts commit paths call one row write that YAML-loads before commit, and the one frontmatter parser replaces _posts_load_error's split and _row_names
title: "config:posts rows have one writer and one parser: rotate's 4 commit paths call it, _posts_load_error and _row_names go (row W1 B2; assigned: director-general-3)"
town: core
---
# hypothesis:posts-rows-have-one-writer-and-one-parser

## Measured
- rotate.py :10305 / :10606 / :10771 / :18366 commit posts rows, each with _posts_load_error (:10552, 5 calls); _row_names (:10564) beside _own_row_line (:9887); frontmatter.split_frontmatter (frontmatter.py:25).

## CLAIM
(1) one row write, called by all 4 (2) it YAML-loads the result before goal:g4.18.5.2's commit (3) _posts_load_error and _row_names removed, callers on the one parser.

## Dispatch line
config-max: none. template-max: none. code: re-point 4 callers, delete 2 helpers.

## FALSIFIERS
- any of the 4 paths writes posts.md without the one write
- a non-loading posts.md is committed
- `def _row_names` or `_posts_load_error(` remains in rotate.py

## TESTS
test_write_self_row.py · test_rotate.py -- ONE file at a time, `--basetemp /tmp/b4w1c`

## FILE SCOPE
extensions/agi/bin/rotate.py · extensions/agi/bin/write.py (the row write) · the 2 test files

## CEILING
no dispatch · <= 50 production lines net · <= 40 test lines · 0 USD
