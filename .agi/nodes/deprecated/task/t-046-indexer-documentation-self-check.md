---
id: task:t-046
mint_id: 5fd9c1c3aaa341e49d1bc4865d67f956
type: task
parents:
  - hyp:environment-indexers-r9
acceptance_criteria:
  - R9.4 (self-check command lists each indexer and reports whether it has at least one upgrade marker)
blocked_by:
  - task:t-045
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
title: "T-046: Indexer documentation self-check command"
---
**Description:** Implement `agi-tree self-test indexer-docs`. Lists each registered indexer and reports `OK` if at least one upgrade marker is present; `MISSING` otherwise.

**Files:** `agi-tree/src/environment_indexers/cli.py`, `agi-tree/tests/environment_indexers/test_self_check.py`

**Test Strategy:** CLI test runs the command and asserts each indexer reports `OK`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R9` under `hyp:environment-indexers-r9`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
