---
id: exp:renderers-r1
mint_id: 976fa4109bb44ba99bd34b65e285c932
type: experiment
parents:
  - hyp:renderers-r1
next_edges:
  - verdict:renderers-r1
edited_by: season.py
season: 1
subgraph: false
tags:
  - renderers
  - R1
testable_claim: Shared Internal Representation
thought_session: season
title: "renderers/R1: Experiment"
---
**Description:** Run renderers test suite + validate R1 acceptance criteria.

**Method:**
- Run pytest on tests/renderers/ (31 tests)
- Validate R1.1–R1.4 programmatically
- Create 8-hop chain nodes