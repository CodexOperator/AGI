---
acceptance_criteria:
  - R7.1 (second load returns within noise floor)
  - R7.2 (modifying any node file invalidates cache)
  - R7.3 (cache key includes content-addressed digest so renaming is detected)
blocked_by:
  - task:t-011
cavekit_req: graph-core/R7
effort: M
id: "task:t-013"
mint_id: 36fb93b04fef4201b12c1b8cba5e6e31
origin: build-site
parents:
  - hyp:graph-core-r7
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-013: Warm-load cache with content-addressed digest"
type: task
---

**Description:** Wrap the loader in an `lru_cache`-style memoizer keyed on `(directory_path, content_digest)`. The digest is computed by hashing a sorted list of `(relative_path, sha256(file_bytes))` tuples. Second load with unchanged source yields the cached graph object.

**Files:** `agi-tree/src/graph_core/cache.py`, `agi-tree/tests/graph_core/test_warm_load.py`

**Test Strategy:** Time first vs second load via `time.perf_counter`; second-call elapsed must be at most an order of magnitude over no-op (define a 1ms ceiling for the test fixture). Mutate one file and assert the next load takes more than the noise threshold.
