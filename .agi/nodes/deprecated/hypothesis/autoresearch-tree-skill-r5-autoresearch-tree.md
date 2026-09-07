---
id: hyp:autoresearch-tree-skill-r5
mint_id: 4c92a2c3e36a4d56b021452267779129
type: hypothesis
parents:
  - idea:domain-autoresearch-tree-skill
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - autoresearch-tree-skill
  - R5
testable_claim: Verdict Emission From Experiment Results
thought_session: season
title: "autoresearch-tree-skill/R5: Verdict Emission From Experiment Results"
---
**Description:** After running an experiment, an agent emits a verdict node whose values conform to the verdict taxonomy.

**Acceptance Criteria:**
- [ ] An emitted verdict node passes schema-registry validation against the built-in verdict schema
- [ ] An emitted verdict's state is exactly one of the five taxonomy values and any inconclusive form carries a numeric `N` between 0 and 100
- [ ] An emitted verdict carries `confidence`, `evidence_runs`, `contradicts`, and `supports` fields
- [ ] An invalid verdict emission is rejected with a structured error and does not modify the graph

**Dependencies:** chain-engine (R8 verdict taxonomy), schema-registry (R4 validation)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r5-by-citation` citing `build:bin-evidence-gate`: `evidence_gate.py` is precisely the verdict-emission gate with no-mutate-on-reject; `goal:s16` is about this gate's behaviour.
<!-- THOUGHT:END -->