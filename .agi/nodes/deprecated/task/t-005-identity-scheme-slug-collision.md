---
id: task:t-005
mint_id: 8950ac3ce15644079eec01ac36aa98cb
type: task
parents:
  - hyp:graph-core-r3
acceptance_criteria:
  - R3.1 (`<type-prefix>:<short-slug>`
  - slug is kebab-case 2..5 words)
  - R3.2 (collision gets `:n` starting at `:2`)
  - R3.3 (>40 chars triggers non-fatal warning)
  - R3.4 (stable across rebuilds from same source files)
blocked_by:
  - task:t-001
cavekit_req: graph-core/R3
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-005: Identity scheme (slug + collision suffix + length warning)"
---
**Description:** Implement `mint_id(type_prefix, source_text)` and `IdRegistry`. Slug derivation is deterministic: lowercase, strip punctuation, split on whitespace, take first 2–5 tokens (configurable cap), join with `-`. Registry tracks issued ids; on collision, append `:2`, `:3`, ... in stable insertion order. Warn (via Python `warnings`) when the resulting id exceeds 40 chars but still return it. Stability comes from feeding the same source-text deterministically.

**Files:** `agi-tree/src/graph_core/identity.py`, `agi-tree/tests/graph_core/test_identity.py`

**Test Strategy:** Unit tests: same input twice yields same id; collision yields `:2` then `:3`; long input raises a `UserWarning`. Stability test: feed a sorted list of source texts twice and compare id sequences for byte equality.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R3` under `hyp:graph-core-r3`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r3-by-citation` citing `build:src-graph-core-identity`, `build:tests-graph-core-test-identity`: `identity.py` is the identity scheme (slug plus `mint_permanent_id`, the goal:g2.5 mint id) and `test_identity.py` is its suite.
<!-- THOUGHT:END -->
