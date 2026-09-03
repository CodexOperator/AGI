---
id: task:t-043
mint_id: b1de159abd8340f7b0536ffe9960fd37
type: task
parents:
  - hyp:environment-indexers-r8
acceptance_criteria:
  - R8.1 (second invocation on unchanged path returns within noise floor)
  - R8.2 (modifying any source file under path invalidates cache)
  - R8.3 (cache state under context dir
  - portable)
  - R8.4 (force fresh re-run via documented flag)
blocked_by:
  - task:t-032
  - task:t-013
cavekit_req: environment-indexers/R8
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-043: Per-path result caching with invalidation and force-refresh"
---
**Description:** Wrap each indexer's main entrypoint with a content-digest-keyed cache stored at `context/.cache/indexers/<indexer_name>/<digest>.pkl`. Add `--no-cache` CLI flag.

**Files:** `agi-tree/src/environment_indexers/cache.py`, `agi-tree/tests/environment_indexers/test_cache.py`

**Test Strategy:** Time second run; assert noise floor. Mutate a fixture file and assert next run is slower. `--no-cache` always rebuilds.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R8` under `hyp:environment-indexers-r8`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
