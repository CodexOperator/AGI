---
id: task:t-024
mint_id: 0a763c835bc94c57819ea50c8e5d6522
type: task
parents:
  - hyp:schema-registry-r4
acceptance_criteria:
  - R4.1 (no rule → no per-field checks)
  - R4.2 (rule → reject violators with structured per-node error)
  - R4.3 (validation errors do not abort rest of load)
  - R4.4 (validation results queryable
  - e.g. failure counts per schema)
blocked_by:
  - task:t-021
cavekit_req: schema-registry/R4
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
title: "T-024: Optional validation hook engine"
---
**Description:** Schema frontmatter may include a `validation` rule (declarative DSL — required-fields, type-checks, regex). Loader runs the rule against each candidate node. Each failure becomes a `ValidationError(node_id, schema, reason)` collected into the load result. Provide `registry.failures_by_schema()` query.

**Files:** `agi-tree/src/schema_registry/validation.py`, `agi-tree/src/schema_registry/dsl.py`, `agi-tree/tests/schema_registry/test_validation.py`

**Test Strategy:** Two fixtures (one with rules, one without). With rules, assert violators are listed but valid nodes still load. Without rules, no per-field checks. `failures_by_schema()` returns expected counts.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R4` under `hyp:schema-registry-r4`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r4-by-citation` citing `build:src-schema-registry-dsl`, `build:src-schema-registry-validation`, `build:tests-schema-registry-test-validation`: `dsl.py` and `validation.py` are the optional validation hooks with per-schema failure reporting.
<!-- THOUGHT:END -->