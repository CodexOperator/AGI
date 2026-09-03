---
id: task:t-013
mint_id: 36fb93b04fef4201b12c1b8cba5e6e31
type: task
parents:
  - hyp:graph-core-r7
acceptance_criteria:
  - R7.1 (second load returns within noise floor)
  - R7.2 (modifying any node file invalidates cache)
  - R7.3 (cache key includes content-addressed digest so renaming is detected)
blocked_by:
  - task:t-011
cavekit_req: graph-core/R7
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-013: Warm-load cache with content-addressed digest"
---
**Description:** Wrap the loader in an `lru_cache`-style memoizer keyed on `(directory_path, content_digest)`. The digest is computed by hashing a sorted list of `(relative_path, sha256(file_bytes))` tuples. Second load with unchanged source yields the cached graph object.

**Files:** `agi-tree/src/graph_core/cache.py`, `agi-tree/tests/graph_core/test_warm_load.py`

**Test Strategy:** Time first vs second load via `time.perf_counter`; second-call elapsed must be at most an order of magnitude over no-op (define a 1ms ceiling for the test fixture). Mutate one file and assert the next load takes more than the noise threshold.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R7` under `hyp:graph-core-r7`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r7-by-citation` citing `build:src-graph-core-cache`, `build:tests-graph-core-test-warm-load`: `cache.py` is the digest-keyed warm-load cache with invalidation and `test_warm_load.py` is its suite.
<!-- THOUGHT:END -->
