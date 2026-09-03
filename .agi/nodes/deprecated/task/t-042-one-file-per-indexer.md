---
id: task:t-042
mint_id: 5d2c34137ef74fe18202dff538492ad7
type: task
parents:
  - hyp:environment-indexers-r7
acceptance_criteria:
  - R7.1 (each indexer in own file under indexers dir)
  - R7.2 (each registers new schema with registry or references existing built-in)
  - R7.3 (each documents inputs/outputs/limitations in header)
  - R7.4 (removing indexer file removes only that command)
blocked_by:
  - task:t-033
  - task:t-034
  - task:t-037
  - task:t-039
  - task:t-041
cavekit_req: environment-indexers/R7
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-042: One-file-per-indexer layout enforcement"
---
**Description:** Lint pass / structural test that each file under `agi-tree/src/environment_indexers/` (excluding cli/registry/queries) (a) exposes exactly one indexer, (b) declares its schemas, (c) has a header docstring with inputs/outputs/limitations.

**Files:** `agi-tree/tests/environment_indexers/test_layout.py`, header docstring updates as needed

**Test Strategy:** Test reads each file, parses module-level docstring, asserts presence of three sections (Inputs/Outputs/Limitations) and that exactly one `@register_indexer` decorator is used.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R7` under `hyp:environment-indexers-r7`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
