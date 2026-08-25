---
acceptance_criteria:
  - R9.4 (self-test command verifies portability by reloading from temporary copy and comparing node counts and ids)
blocked_by:
  - task:t-016
cavekit_req: graph-core/R9
effort: S
id: "task:t-017"
mint_id: aa96b648a8714befa5e4f5f2b860cd00
origin: build-site
parents:
  - hyp:graph-core-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-017: Portability self-test command"
type: task
---

**Description:** Implement `agi-tree self-test portability` CLI subcommand. Copies `context/` to a tempdir, loads from there, compares node counts and id lists with the original. Exit code 0 on match, non-zero with diff on mismatch.

**Files:** `agi-tree/src/graph_core/cli/self_test.py`, `agi-tree/tests/graph_core/test_self_test_portability.py`

**Test Strategy:** Invoke the subcommand on a fixture context dir; assert exit 0 and a "portable: yes" line in stdout.
