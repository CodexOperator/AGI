---
id: task:t-044
mint_id: 3989d2ab48d2488b8b8615ef2a9a3d1c
type: task
parents:
  - hyp:environment-indexers-r9
acceptance_criteria:
  - R9.1 (each indexer file has comments explaining parsing strategy
  - schema mapping
  - caching behavior)
blocked_by:
  - task:t-042
cavekit_req: environment-indexers/R9
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-044: Per-indexer documentation (parsing/schema-mapping/caching comments)"
---
**Description:** Audit and add comment blocks per indexer covering: (a) parsing strategy, (b) schema mapping, (c) caching behavior. Three labeled sections per file.

**Files:** `agi-tree/src/environment_indexers/filesystem_tree.py`, `code_symbols.py`, `python_deps.py`, `api_deps.py`, `container_observation.py`

**Test Strategy:** Documentation lint test asserts each indexer file contains all three labeled comment sections.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R9` under `hyp:environment-indexers-r9`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
