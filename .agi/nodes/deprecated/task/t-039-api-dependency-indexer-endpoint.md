---
id: task:t-039
mint_id: 2958206ed28240a599f351cd89355779
type: task
parents:
  - hyp:environment-indexers-r5
acceptance_criteria:
  - R5.1 (valid spec → one node per endpoint)
  - R5.2 (each endpoint node carries method/path/summary in frontmatter)
  - R5.4 (invalid spec → structured error naming offending file; no nodes)
blocked_by:
  - task:t-032
  - task:t-031
cavekit_req: environment-indexers/R5
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-039: API dependency indexer — endpoint nodes"
---
**Description:** Parse OpenAPI/Swagger 2.0 + 3.x. For each path × method, emit one `endpoint` node with `method`, `path`, `summary` in frontmatter. Invalid spec → `InvalidOpenApiError(path, parser_message)`.

**Files:** `agi-tree/src/environment_indexers/api_deps.py`, `agi-tree/src/environment_indexers/schemas/[endpoint].md`, `agi-tree/tests/environment_indexers/test_api_deps_endpoints.py`

**Test Strategy:** Three fixtures: petstore.yaml (valid), invalid.yaml; assert 5 endpoint nodes and clear error.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R5` under `hyp:environment-indexers-r5`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
