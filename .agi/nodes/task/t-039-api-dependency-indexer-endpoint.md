---
acceptance_criteria:
  - R5.1 (valid spec → one node per endpoint)
  - R5.2 (each endpoint node carries method/path/summary in frontmatter)
  - R5.4 (invalid spec → structured error naming offending file; no nodes)
blocked_by:
  - task:t-032
  - task:t-031
cavekit_req: environment-indexers/R5
effort: M
id: "task:t-039"
mint_id: 2958206ed28240a599f351cd89355779
origin: build-site
parents:
  - hyp:environment-indexers-r5
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-039: API dependency indexer — endpoint nodes"
type: task
---

**Description:** Parse OpenAPI/Swagger 2.0 + 3.x. For each path × method, emit one `endpoint` node with `method`, `path`, `summary` in frontmatter. Invalid spec → `InvalidOpenApiError(path, parser_message)`.

**Files:** `agi-tree/src/environment_indexers/api_deps.py`, `agi-tree/src/environment_indexers/schemas/[endpoint].md`, `agi-tree/tests/environment_indexers/test_api_deps_endpoints.py`

**Test Strategy:** Three fixtures: petstore.yaml (valid), invalid.yaml; assert 5 endpoint nodes and clear error.
