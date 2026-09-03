---
id: task:t-023
mint_id: ce2fc7037838499d83f70771b882f238
type: task
parents:
  - hyp:schema-registry-r3
acceptance_criteria:
  - R3.3 (edges from meta_node instances to ordinary nodes record which schema validated which node)
blocked_by:
  - task:t-022
  - task:t-003
cavekit_req: schema-registry/R3
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-023: Validating edges from meta-nodes to ordinary nodes"
---
**Description:** After validating a node against its schema, insert a `validated_by` edge from the meta-node to the ordinary node.

**Files:** `agi-tree/src/schema_registry/validation_edges.py`, `agi-tree/tests/schema_registry/test_validation_edges.py`

**Test Strategy:** Load fixture; for each ordinary node, assert exactly one validated_by edge from the corresponding meta-node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R3` under `hyp:schema-registry-r3`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r3-by-citation` citing `build:src-schema-registry-meta-nodes`, `build:tests-schema-registry-test-meta-nodes`: `meta_nodes.py` (`schema_to_meta_node`, `synthesize_meta_nodes`, `diff_meta_nodes`) is the schema-as-node surface.
<!-- THOUGHT:END -->
