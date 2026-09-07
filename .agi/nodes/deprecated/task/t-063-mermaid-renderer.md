---
id: task:t-063
mint_id: bb0fe348cd6f4e32869ae932b99f5463
type: task
parents:
  - hyp:renderers-r3
acceptance_criteria:
  - R3.1 (output begins with recognized Mermaid directive
  - e.g. `graph TD` or `flowchart`)
  - R3.2 (parses without error in Mermaid 10+)
  - R3.3 (every node and edge in input appears at most once)
  - R3.4 (two runs → byte-equal output)
blocked_by:
  - task:t-060
cavekit_req: renderers/R3
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
title: "T-063: Mermaid renderer"
---
**Description:** Implement `MermaidRenderer.render(rep) -> str`. Outputs `flowchart TD` followed by node and edge declarations. Deduplicates by id and edge triple.

**Files:** `agi-tree/src/renderers/mermaid.py`, `agi-tree/tests/renderers/test_mermaid.py`

**Test Strategy:** Validate output via the `mermaid-cli` (npx mmdc) parse step in CI; idempotency test; uniqueness test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R3` under `hyp:renderers-r3`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:renderers-r3-by-citation` citing `build:src-renderers-mermaid`, `build:tests-renderers-test-mermaid`: `mermaid.py` emits a valid Mermaid directive with de-duplicated edges and `test_mermaid.py` pins it.
<!-- THOUGHT:END -->