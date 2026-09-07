---
id: exp:schema-registry-r1
mint_id: 66a2e5da1e5d4bcfb2d712754a2c5a8b
type: experiment
parents:
  - hyp:schema-registry-r1
next_edges:
  - verdict:schema-registry-r1
edited_by: season.py
season: 1
subgraph: false
tags:
  - schema-registry
  - R1
testable_claim: Schema as File
thought_session: season
title: "schema-registry/R1: Experiment"
---
**Description:** Run schema-registry test suite + validate R1 acceptance criteria.

**Method:**
- Run pytest on tests/schema_registry/ (41 tests)
- Validate R1.1–R1.4 programmatically
- Validate bracket convention (R2.1–R2.4)