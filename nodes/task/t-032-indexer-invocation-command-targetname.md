---
acceptance_criteria:
  - R1.1 (command accepts target path + indexer name; runs only that one)
  - R1.2 (listing without invocation → summary with name + one-line description)
  - R1.3 (unknown indexer name → structured error
  - runs nothing)
  - R1.4 (non-zero exit when failure prevented node emission)
blocked_by:
  - task:t-018
  - task:t-019
cavekit_req: environment-indexers/R1
effort: M
id: "task:t-032"
mint_id: 9918ae7912ef422ba7ee984b5ed1e46f
origin: build-site
parents:
  - hyp:environment-indexers-r1
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-032: Indexer invocation command (target+name, listing, error handling)"
type: task
---

**Description:** Implement `agi-tree index <name> <path>` and `agi-tree index --list`. Indexers register themselves with name + description via a decorator. Unknown name → `UnknownIndexerError`. Failures during emission propagate as non-zero CLI exits.

**Files:** `agi-tree/src/environment_indexers/cli.py`, `agi-tree/src/environment_indexers/registry.py`, `agi-tree/tests/environment_indexers/test_cli.py`

**Test Strategy:** CLI tests covering each criterion. Mock indexer registration to simulate failure path.
