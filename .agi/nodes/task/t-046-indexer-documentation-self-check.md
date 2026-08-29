---
acceptance_criteria:
  - R9.4 (self-check command lists each indexer and reports whether it has at least one upgrade marker)
blocked_by:
  - task:t-045
cavekit_req: environment-indexers/R9
effort: S
id: "task:t-046"
mint_id: 5fd9c1c3aaa341e49d1bc4865d67f956
origin: build-site
parents:
  - hyp:environment-indexers-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-046: Indexer documentation self-check command"
type: task
---

**Description:** Implement `agi-tree self-test indexer-docs`. Lists each registered indexer and reports `OK` if at least one upgrade marker is present; `MISSING` otherwise.

**Files:** `agi-tree/src/environment_indexers/cli.py`, `agi-tree/tests/environment_indexers/test_self_check.py`

**Test Strategy:** CLI test runs the command and asserts each indexer reports `OK`.
