---
id: task:t-045
mint_id: 6a32006efeaf4efabf3df85484120118
type: task
parents:
  - hyp:environment-indexers-r9
acceptance_criteria:
  - R9.2 (each indexer has at least one upgrade-marker comment block naming the section eligible for replacement)
  - R9.3 (markers discoverable via single grep over indexers dir)
blocked_by:
  - task:t-044
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
title: "T-045: Upgrade markers grep-discoverable"
---
**Description:** Standardize `# UPGRADE-MARKER: <slug> — <section description>` lines. Each indexer must have at least one. The `agi-tree self-test indexer-docs` (T-046) greps for them.

**Files:** Each indexer source file

**Test Strategy:** `grep -r 'UPGRADE-MARKER:' agi-tree/src/environment_indexers/` returns >=5 hits (one per indexer).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R9` under `hyp:environment-indexers-r9`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
