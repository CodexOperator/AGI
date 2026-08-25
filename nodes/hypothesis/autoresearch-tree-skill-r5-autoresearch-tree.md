---
confidence: 0.5
id: "hyp:autoresearch-tree-skill-r5"
mint_id: 4c92a2c3e36a4d56b021452267779129
origin: build-site
parents:
  - idea:domain-autoresearch-tree-skill
subgraph: false
tags:
  - autoresearch-tree-skill
  - R5
testable_claim: Verdict Emission From Experiment Results
title: "autoresearch-tree-skill/R5: Verdict Emission From Experiment Results"
type: hypothesis
---

**Description:** After running an experiment, an agent emits a verdict node whose values conform to the verdict taxonomy.

**Acceptance Criteria:**
- [ ] An emitted verdict node passes schema-registry validation against the built-in verdict schema
- [ ] An emitted verdict's state is exactly one of the five taxonomy values and any inconclusive form carries a numeric `N` between 0 and 100
- [ ] An emitted verdict carries `confidence`, `evidence_runs`, `contradicts`, and `supports` fields
- [ ] An invalid verdict emission is rejected with a structured error and does not modify the graph

**Dependencies:** chain-engine (R8 verdict taxonomy), schema-registry (R4 validation)
