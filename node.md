---
id: "mvp:tests"
mint_id: ef4c7a4a1fac4f1caa4e3fe9763bf038
parents:
  - hypothesis:l3-engine-files-outside-the-grid
tags:
  - l3
  - grid
title: "MVP: every tracked extensions/agi/tests/ engine file inside the grid"
type: mvp
---

# mvp:tests

## MVP

The **tests** subsystem of the engine — every tracked code file under `extensions/agi/tests/` — must have a build node whose `payload_ref` resolves to it, so its bytes are inside the grid (goal:g6.1/payload_boundary). This mvp specifies that class of files so `level3.py --mint-missing-only` can mint each missing build node with a legal goal:s29 parent: `parents: [mvp:tests]`.

Parent: hypothesis:l3-engine-files-outside-the-grid — the checker that closes this gap is `grid_coverage_check.py`; the remaining files this mvp names are the mint backlog, added once here rather than as one mvp per file.

Falsifier: any tracked engine file under `extensions/agi/tests/` exists without a build node and without a declared grid_coverage exclusion.
