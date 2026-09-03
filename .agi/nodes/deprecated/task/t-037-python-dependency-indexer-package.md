---
id: task:t-037
mint_id: 97be46a30a21426da53c8c4b3e8245e3
type: task
parents:
  - hyp:environment-indexers-r4
acceptance_criteria:
  - R4.1 (one node per declared package dependency)
  - R4.3 (both requirements.txt-style and pyproject.toml-style supported)
  - R4.4 (neither file present → structured error
  - no nodes)
blocked_by:
  - task:t-032
  - task:t-031
cavekit_req: environment-indexers/R4
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-037: Python dependency indexer — package nodes from declarations"
---
**Description:** Parse `requirements.txt` (line-based) and `pyproject.toml` (`[project.dependencies]`, `[tool.poetry.dependencies]`). Emit `package` node per dependency. Missing both files → `NoDependencyDeclarationError`.

**Files:** `agi-tree/src/environment_indexers/python_deps.py`, `agi-tree/src/environment_indexers/schemas/[package].md`, `agi-tree/tests/environment_indexers/test_python_deps_packages.py`

**Test Strategy:** Three fixtures: one with `requirements.txt`, one with `pyproject.toml`, one with neither. Assert correct emission and error.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R4` under `hyp:environment-indexers-r4`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->
