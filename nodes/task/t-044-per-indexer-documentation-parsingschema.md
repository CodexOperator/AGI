---
acceptance_criteria:
  - R9.1 (each indexer file has comments explaining parsing strategy
  - schema mapping
  - caching behavior)
blocked_by:
  - task:t-042
cavekit_req: environment-indexers/R9
effort: S
id: "task:t-044"
mint_id: 3989d2ab48d2488b8b8615ef2a9a3d1c
origin: build-site
parents:
  - hyp:environment-indexers-r9
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-044: Per-indexer documentation (parsing/schema-mapping/caching comments)"
type: task
---

**Description:** Audit and add comment blocks per indexer covering: (a) parsing strategy, (b) schema mapping, (c) caching behavior. Three labeled sections per file.

**Files:** `agi-tree/src/environment_indexers/filesystem_tree.py`, `code_symbols.py`, `python_deps.py`, `api_deps.py`, `container_observation.py`

**Test Strategy:** Documentation lint test asserts each indexer file contains all three labeled comment sections.
