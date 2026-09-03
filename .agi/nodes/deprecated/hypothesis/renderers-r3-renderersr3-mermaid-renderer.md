---
id: hyp:renderers-r3
mint_id: 8be8fd99db2746d0993a2a90ff1136f3
type: hypothesis
parents:
  - idea:domain-renderers
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - renderers
  - R3
testable_claim: Mermaid Renderer
thought_session: L1.09
title: "renderers/R3: Mermaid Renderer"
---
**Description:** A renderer produces a valid Mermaid diagram source string usable as a graph or flowchart.

**Acceptance Criteria:**
- [ ] The output begins with a recognized Mermaid diagram directive (for example `graph TD` or `flowchart`)
- [ ] The output parses without error in Mermaid version 10 or later
- [ ] Every node and edge in the input representation appears at most once in the output
- [ ] Two runs against the same representation produce byte-equal output

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:renderers-r3-by-citation` citing `build:src-renderers-mermaid`, `build:tests-renderers-test-mermaid`: `mermaid.py` emits a valid Mermaid directive with de-duplicated edges and `test_mermaid.py` pins it.
<!-- THOUGHT:END -->
