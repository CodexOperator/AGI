---
id: task:t-036
mint_id: 790b2f46007e4a68bf65566a784da60c
type: task
parents:
  - hyp:environment-indexers-r3
acceptance_criteria:
  - R3.3 (warm-loads in time indistinguishable from no-op on unchanged repo)
  - R3.4 (inline comments flag at least one upgrade point per major parsing stage)
blocked_by:
  - task:t-035
  - task:t-013
cavekit_req: environment-indexers/R3
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
title: "T-036: Code symbol indexer — warm-load and upgrade markers"
---
**Description:** Reuse T-013 warm-load cache for the indexer's per-path output. Add inline `# UPGRADE-MARKER:` comments naming the upgradable concern in each parsing stage (lex, parse, symbol-resolve, edge-emit) — at least one per stage.

**Files:** `agi-tree/src/environment_indexers/code_symbols.py`, `agi-tree/tests/environment_indexers/test_code_symbols_warm.py`

**Test Strategy:** Time second run on unchanged fixture; must be within noise floor. Grep `UPGRADE-MARKER:` and assert >= 4 hits.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R3` under `hyp:environment-indexers-r3`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->