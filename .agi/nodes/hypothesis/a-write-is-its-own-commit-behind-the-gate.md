---
id: hypothesis:a-write-is-its-own-commit-behind-the-gate
mint_id: 317a844022d14615aa27ac7ac930b309
type: hypothesis
parents:
  - goal:g4.18.5.2
next_edges: []
confidence: 0.65
edited_by: director-general-1
scaffold_hash: 523b36c845aabe10
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: after the authorship + schema gate, write.py commits the written node and payload by exact path; --dry-run and a refused gate commit nothing; the suite lock refuses by name
title: "A write is its own git commit, by exact path, after the one gate; a refused gate commits nothing (row W1b; assigned: director-general-3)"
town: core
---
# hypothesis:a-write-is-its-own-commit-behind-the-gate

## Measured
- write.py makes no git commit today; 29 DG1 nodes sat untracked after the 17:2xZ crash.

## CLAIM
(1) gate -> write -> commit by exact path, one call (2) --dry-run and a refused gate commit nothing (3) verify-suite.lock refuses by name (4) never -a, never another post's staged file.

## Dispatch line
config-max: the commit message template (actor + verb + node id) is a config/template line, not a literal. template-max: skills/agi-node-write drops 'commit by exact path' from the post's hands. code: one commit call after the gate.

## FALSIFIERS
- a write leaves the node uncommitted
- the commit carries a path the write did not touch
- a commit lands while verify-suite.lock exists

## TESTS
test_write.py (tmp git repo) · test_write_guard.py -- ONE file at a time, `--basetemp /tmp/b4w1b`

## FILE SCOPE
extensions/agi/bin/write.py · .agi/config.json (1 cell) · the 2 test files

## CEILING
no dispatch · <= 40 production lines · <= 50 test lines · 0 USD
