---
id: task:t-022
mint_id: 171de2ae24c9414c94ff04cad24ab021
type: task
parents:
  - hyp:schema-registry-r3
acceptance_criteria:
  - R3.1 (one meta_node per registered schema; id derived from schema name)
  - R3.2 (meta-node frontmatter exposes declared fields/defaults/rules)
  - R3.4 (removing schema removes meta-node and validating edges next load)
blocked_by:
  - task:t-021
  - task:t-001
  - task:t-005
cavekit_req: schema-registry/R3
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
title: "T-022: Schemas as `meta_node` in graph"
---
**Description:** During registry load, synthesize one node of `type=meta_node` per registered schema. Use the schema's name to mint a deterministic id. The meta-node's frontmatter mirrors the schema's declared fields, defaults, and validation rule references.

**Files:** `agi-tree/src/schema_registry/meta_nodes.py`, `agi-tree/tests/schema_registry/test_meta_nodes.py`

**Test Strategy:** Load registry; assert each schema name has a corresponding meta_node in the output graph, with frontmatter containing fields/defaults/rules.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R3` under `hyp:schema-registry-r3`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r3-by-citation` citing `build:src-schema-registry-meta-nodes`, `build:tests-schema-registry-test-meta-nodes`: `meta_nodes.py` (`schema_to_meta_node`, `synthesize_meta_nodes`, `diff_meta_nodes`) is the schema-as-node surface.
<!-- THOUGHT:END -->