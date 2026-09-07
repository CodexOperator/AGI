---
id: hyp:schema-registry-r5
mint_id: fefc3c46128c41068cd11c2990a27beb
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
  - R5
testable_claim: Auto-Discovery Cascade
thought_session: season
title: "schema-registry/R5: Auto-Discovery Cascade"
---
**Description:** When a directory of files is encountered, the registry resolves its node type using a documented cascade: bracketed schema match, then fingerprint similarity against registered schemas, then language-model fallback to propose a new schema, then a generic fallback with a warning.

**Acceptance Criteria:**
- [ ] When a bracketed schema matches the directory by name, that schema is selected and later steps are skipped
- [ ] When no name match exists, the registry compares observed frontmatter shape against registered schemas and selects the best match if its similarity score is at least 0.7
- [ ] When similarity is below the threshold and a language-model hook is available, the hook proposes a schema and the proposal is written without brackets pending user review
- [ ] When all earlier steps fail, the directory is loaded under a generic schema and a warning lists each unmatched file

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r5-by-citation` citing `build:src-schema-registry-cascade`, `build:src-schema-registry-fingerprint`, `build:tests-schema-registry-test-cascade-step-1`, `build:tests-schema-registry-test-cascade-step-2`: `cascade.py` (`cascade_step_1`, `discover_schema`, `register_extra_step`) and `fingerprint.py` (`cascade_step_2`) are the auto-discovery cascade, with a test per step.
<!-- THOUGHT:END -->