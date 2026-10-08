---
id: task:t-040
mint_id: 6fac3fd125a8443994a427c369cb66d2
type: task
parents:
  - hyp:environment-indexers-r5
acceptance_criteria:
  - R5.3 (edges record which endpoints share schemas or reference each other)
blocked_by:
  - task:t-039
cavekit_req: environment-indexers/R5
edited_by: season.py
effort: S
origin: build-site
season: 1
status: deprecated
tags:
  - S
  - tier--1
thought_session: season
tier: -1
title: "T-040: API dependency indexer — schema reuse edges"
---
**Description:** Scan `$ref` and inline schema reuse. For every shared component, emit `shares_schema` edges between the affected endpoint nodes.

**Files:** `agi-tree/src/environment_indexers/api_deps.py`, `agi-tree/tests/environment_indexers/test_api_deps_shared_schemas.py`

**Test Strategy:** Fixture with two endpoints sharing a `User` schema; assert one `shares_schema` edge between them.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R5` under `hyp:environment-indexers-r5`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->