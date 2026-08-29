---
acceptance_criteria:
  - R3.1 (one meta_node per registered schema; id derived from schema name)
  - R3.2 (meta-node frontmatter exposes declared fields/defaults/rules)
  - R3.4 (removing schema removes meta-node and validating edges next load)
blocked_by:
  - task:t-021
  - task:t-001
  - task:t-005
cavekit_req: schema-registry/R3
effort: M
id: "task:t-022"
mint_id: 171de2ae24c9414c94ff04cad24ab021
origin: build-site
parents:
  - hyp:schema-registry-r3
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-022: Schemas as `meta_node` in graph"
type: task
---

**Description:** During registry load, synthesize one node of `type=meta_node` per registered schema. Use the schema's name to mint a deterministic id. The meta-node's frontmatter mirrors the schema's declared fields, defaults, and validation rule references.

**Files:** `agi-tree/src/schema_registry/meta_nodes.py`, `agi-tree/tests/schema_registry/test_meta_nodes.py`

**Test Strategy:** Load registry; assert each schema name has a corresponding meta_node in the output graph, with frontmatter containing fields/defaults/rules.
