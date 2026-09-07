---
id: task:t-038
mint_id: 373c74d7badb443fa96ca812a06fa187
type: task
parents:
  - hyp:environment-indexers-r4
acceptance_criteria:
  - R4.2 (edges record which internal module imports which other internal module)
blocked_by:
  - task:t-037
  - task:t-034
cavekit_req: environment-indexers/R4
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-038: Python dependency indexer — internal-import edges"
---
**Description:** Walk Python files, parse `import`/`from ... import` statements. For modules that resolve within the project, emit `imports` edges between module nodes (reuse module nodes from T-034 if present, otherwise emit lightweight stand-ins).

**Files:** `agi-tree/src/environment_indexers/python_deps.py`, `agi-tree/tests/environment_indexers/test_python_deps_imports.py`

**Test Strategy:** Fixture with two internal modules; assert one `imports` edge in the right direction.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R4` under `hyp:environment-indexers-r4`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->