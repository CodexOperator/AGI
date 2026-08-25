---
acceptance_criteria:
  - R8.1 (second invocation on unchanged path returns within noise floor)
  - R8.2 (modifying any source file under path invalidates cache)
  - R8.3 (cache state under context dir
  - portable)
  - R8.4 (force fresh re-run via documented flag)
blocked_by:
  - task:t-032
  - task:t-013
cavekit_req: environment-indexers/R8
effort: M
id: "task:t-043"
mint_id: b1de159abd8340f7b0536ffe9960fd37
origin: build-site
parents:
  - hyp:environment-indexers-r8
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-043: Per-path result caching with invalidation and force-refresh"
type: task
---

**Description:** Wrap each indexer's main entrypoint with a content-digest-keyed cache stored at `context/.cache/indexers/<indexer_name>/<digest>.pkl`. Add `--no-cache` CLI flag.

**Files:** `agi-tree/src/environment_indexers/cache.py`, `agi-tree/tests/environment_indexers/test_cache.py`

**Test Strategy:** Time second run; assert noise floor. Mutate a fixture file and assert next run is slower. `--no-cache` always rebuilds.
