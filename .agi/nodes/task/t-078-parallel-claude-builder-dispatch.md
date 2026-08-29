---
acceptance_criteria:
  - R3.1 (iteration dispatches at most 5 agents in parallel)
  - R3.2 (fewer eligible candidates than max → run only that many)
  - R3.3 (kit explicitly documents Ollama dispatch as v2 scope item
  - not required)
  - R3.4 (failure of one agent does not abort others; partial results collected and reported)
blocked_by:
  - task:t-077
cavekit_req: autoresearch-tree-skill/R3
effort: M
id: "task:t-078"
mint_id: 0aa08c0c224648c48c8c57acea2bcdc8
origin: build-site
parents:
  - hyp:autoresearch-tree-skill-r3
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-078: Parallel Claude builder dispatch (≤5)"
type: task
---

**Description:** Implement `dispatch_builders(briefings)` using `asyncio.gather(..., return_exceptions=True)` capped at 5 concurrent. Document Ollama-as-v2 in `agi-tree/skills/autoresearch-tree/references/dispatch.md`. Failure → structured per-agent result, others continue.

**Files:** `agi-tree/src/skill/dispatch.py`, `agi-tree/skills/autoresearch-tree/references/dispatch.md`, `agi-tree/tests/skill/test_dispatch.py`

**Test Strategy:** Stub builder pool: 7 candidates → 5 dispatched. 3 candidates → 3 dispatched. One stub raises; others complete and the iteration reports the failure.
