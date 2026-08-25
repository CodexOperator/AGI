---
acceptance_criteria:
  - R7.1 (each indexer in own file under indexers dir)
  - R7.2 (each registers new schema with registry or references existing built-in)
  - R7.3 (each documents inputs/outputs/limitations in header)
  - R7.4 (removing indexer file removes only that command)
blocked_by:
  - task:t-033
  - task:t-034
  - task:t-037
  - task:t-039
  - task:t-041
cavekit_req: environment-indexers/R7
effort: S
id: "task:t-042"
mint_id: 5d2c34137ef74fe18202dff538492ad7
origin: build-site
parents:
  - hyp:environment-indexers-r7
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-042: One-file-per-indexer layout enforcement"
type: task
---

**Description:** Lint pass / structural test that each file under `agi-tree/src/environment_indexers/` (excluding cli/registry/queries) (a) exposes exactly one indexer, (b) declares its schemas, (c) has a header docstring with inputs/outputs/limitations.

**Files:** `agi-tree/tests/environment_indexers/test_layout.py`, header docstring updates as needed

**Test Strategy:** Test reads each file, parses module-level docstring, asserts presence of three sections (Inputs/Outputs/Limitations) and that exactly one `@register_indexer` decorator is used.
