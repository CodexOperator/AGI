---
acceptance_criteria:
  - R3.2 (graph contains relationship edges sufficient to answer "callers of X" and "callees of X")
blocked_by:
  - task:t-034
cavekit_req: environment-indexers/R3
effort: M
id: "task:t-035"
mint_id: ccf089260b524a61a57c7741dda5ff76
origin: build-site
parents:
  - hyp:environment-indexers-r3
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-035: Code symbol indexer — caller/callee relationship edges"
type: task
---

**Description:** Augment T-034 with `calls` edges from caller symbol to callee symbol (best-effort name resolution within the indexed project; cross-package calls flagged as `external_call`). Add `callers_of(id)` and `callees_of(id)` query helpers.

**Files:** `agi-tree/src/environment_indexers/code_symbols.py`, `agi-tree/src/environment_indexers/code_symbol_queries.py`, `agi-tree/tests/environment_indexers/test_call_edges.py`

**Test Strategy:** Fixture with `a()` calling `b()` calling `c()`; assert `callers_of('c')` returns `b` and `callees_of('a')` returns `b`.
