---
id: verdict:a01-7031af17-449ecb-r11
mint_id: 4dbf150c06ce4e89ba769d39d1e59e51
type: verdict
parents:
  - hyp:a01-7031af17-449ecb
next_edges:
  - mvp:a01-7031af17-449ecb-r11
confidence: 0.95
contradicts: []
edited_by: season.py
evidence_runs:
  - exp-a01-7031af17-449ecb-r11-path-safety
season: 1
status: pending
supports: []
tags:
  - graph-core
  - R11
  - path-safety
  - sandboxing
thought_session: season
title: "graph-core/R11: PathValidator Not Wired Into Loader"
verdict: inconclusive_lean_disproved:35
---
# verdict:a01-7031af17-449ecb-r11

## Result: inconclusive_lean_disproved:35

**Key finding:** PathValidator class is implemented correctly (5/7 criteria pass), but the `load_directory` function does NOT call `safe_path()` before opening files. A node with `payload_ref: "../../../etc/passwd"` is accepted without error.

## Evidence

Experiment `exp-a01-7031af17-449ecb-r11-path-safety.py` ran 7 checks:

| Criterion | Result |
|---|---|
| PathValidator.validate() rejects escape paths | PASS |
| PathValidator.validate() accepts internal paths | PASS |
| PathValidator.validate_relative() rejects absolute | PASS |
| PathValidator.validate_relative() accepts relative | PASS |
| safe_path() module function rejects escapes | PASS |
| Loader calls safe_path() (source inspection) | **FAIL** — not wired in |
| payload_ref escape raises PathOutsideProjectError | **FAIL** — loader accepts it |

## Interpretation

The PathValidator class is correct and testable. The sandboxing contract is not enforced in the loader. A future MVP could wire `safe_path()` into `load_node_file()` or `load_directory()` to fix this gap.

**Lean strength: 35** — partial proof that PathValidator itself works, but the integration claim fails. The gap is a concrete, fixable implementation detail.