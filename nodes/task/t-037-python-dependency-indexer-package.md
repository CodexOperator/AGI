---
acceptance_criteria:
  - R4.1 (one node per declared package dependency)
  - R4.3 (both requirements.txt-style and pyproject.toml-style supported)
  - R4.4 (neither file present → structured error
  - no nodes)
blocked_by:
  - task:t-032
  - task:t-031
cavekit_req: environment-indexers/R4
effort: M
id: "task:t-037"
mint_id: 97be46a30a21426da53c8c4b3e8245e3
origin: build-site
parents:
  - hyp:environment-indexers-r4
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-037: Python dependency indexer — package nodes from declarations"
type: task
---

**Description:** Parse `requirements.txt` (line-based) and `pyproject.toml` (`[project.dependencies]`, `[tool.poetry.dependencies]`). Emit `package` node per dependency. Missing both files → `NoDependencyDeclarationError`.

**Files:** `agi-tree/src/environment_indexers/python_deps.py`, `agi-tree/src/environment_indexers/schemas/[package].md`, `agi-tree/tests/environment_indexers/test_python_deps_packages.py`

**Test Strategy:** Three fixtures: one with `requirements.txt`, one with `pyproject.toml`, one with neither. Assert correct emission and error.
