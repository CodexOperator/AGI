---
id: hyp:schema-registry-r4
mint_id: c964ce4786844df0b614553a17d880d6
type: hypothesis
parents:
  - idea:domain-schema-registry
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - schema-registry
  - R4
testable_claim: Optional Validation Hooks
thought_session: season
title: "schema-registry/R4: Optional Validation Hooks"
---
**Description:** A schema may declare a validation rule. When set, the rule checks node frontmatter on load.

**Acceptance Criteria:**
- [ ] A schema without a validation rule loads its nodes without per-field checks
- [ ] A schema with a validation rule rejects nodes whose frontmatter violates the rule and emits a structured error per offending node
- [ ] Validation errors do not abort the rest of the load
- [ ] The set of validation results is queryable after load (for example, count of failures per schema)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r4-by-citation` citing `build:src-schema-registry-dsl`, `build:src-schema-registry-validation`, `build:tests-schema-registry-test-validation`: `dsl.py` and `validation.py` are the optional validation hooks with per-schema failure reporting.
<!-- THOUGHT:END -->