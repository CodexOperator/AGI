---
id: hyp:environment-indexers-r8
mint_id: 1861636abe0e4b6891a81d1d43d2f6b1
type: hypothesis
parents:
  - idea:domain-environment-indexers
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - environment-indexers
  - R8
testable_claim: Per-Path Result Caching
thought_session: L1.09
title: "environment-indexers/R8: Per-Path Result Caching"
---
**Description:** Indexer results are cached per-path so repeated invocations on the same unchanged source skip recomputation.

**Acceptance Criteria:**
- [ ] A second invocation on the same unchanged path returns in time indistinguishable from a no-op
- [ ] Modifying any source file under the target path invalidates the cache for at least that path's run
- [ ] Cache state is stored under the project context directory and is portable along with it
- [ ] Forcing a fresh re-run is available via a documented flag

**Dependencies:** graph-core (R7 warm-load caching, R9 portability)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
