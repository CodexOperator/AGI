---
id: hyp:environment-indexers-r4
mint_id: 716cc2b88a0c4c23a7bc887def997858
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
  - R4
testable_claim: Python Dependency Indexer
thought_session: L1.09
title: "environment-indexers/R4: Python Dependency Indexer"
---
**Description:** An indexer emits nodes for Python packages a project depends on, plus internal-import edges between modules.

**Acceptance Criteria:**
- [ ] Running this indexer on a Python project emits one node per declared package dependency
- [ ] Edges record which internal module imports which other internal module
- [ ] Both `requirements.txt`-style and `pyproject.toml`-style dependency declarations are supported
- [ ] When neither declaration file exists, the indexer reports a structured error and emits no nodes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
