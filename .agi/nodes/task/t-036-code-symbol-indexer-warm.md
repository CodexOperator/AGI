---
acceptance_criteria:
  - R3.3 (warm-loads in time indistinguishable from no-op on unchanged repo)
  - R3.4 (inline comments flag at least one upgrade point per major parsing stage)
blocked_by:
  - task:t-035
  - task:t-013
cavekit_req: environment-indexers/R3
effort: M
id: "task:t-036"
mint_id: 790b2f46007e4a68bf65566a784da60c
origin: build-site
parents:
  - hyp:environment-indexers-r3
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-036: Code symbol indexer — warm-load and upgrade markers"
type: task
---

**Description:** Reuse T-013 warm-load cache for the indexer's per-path output. Add inline `# UPGRADE-MARKER:` comments naming the upgradable concern in each parsing stage (lex, parse, symbol-resolve, edge-emit) — at least one per stage.

**Files:** `agi-tree/src/environment_indexers/code_symbols.py`, `agi-tree/tests/environment_indexers/test_code_symbols_warm.py`

**Test Strategy:** Time second run on unchanged fixture; must be within noise floor. Grep `UPGRADE-MARKER:` and assert >= 4 hits.
