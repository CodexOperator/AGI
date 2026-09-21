---
id: task:t-035
mint_id: ccf089260b524a61a57c7741dda5ff76
type: task
parents:
  - hyp:environment-indexers-r3
acceptance_criteria:
  - R3.2 (graph contains relationship edges sufficient to answer "callers of X" and "callees of X")
blocked_by:
  - task:t-034
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
title: "T-035: Code symbol indexer — caller/callee relationship edges"
---
**Description:** Augment T-034 with `calls` edges from caller symbol to callee symbol (best-effort name resolution within the indexed project; cross-package calls flagged as `external_call`). Add `callers_of(id)` and `callees_of(id)` query helpers.

**Files:** `agi-tree/src/environment_indexers/code_symbols.py`, `agi-tree/src/environment_indexers/code_symbol_queries.py`, `agi-tree/tests/environment_indexers/test_call_edges.py`

**Test Strategy:** Fixture with `a()` calling `b()` calling `c()`; assert `callers_of('c')` returns `b` and `callees_of('a')` returns `b`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R3` under `hyp:environment-indexers-r3`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->