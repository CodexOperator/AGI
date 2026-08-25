---
acceptance_criteria:
  - R3.1 (output begins with recognized Mermaid directive
  - e.g. `graph TD` or `flowchart`)
  - R3.2 (parses without error in Mermaid 10+)
  - R3.3 (every node and edge in input appears at most once)
  - R3.4 (two runs → byte-equal output)
blocked_by:
  - task:t-060
cavekit_req: renderers/R3
effort: M
id: "task:t-063"
mint_id: bb0fe348cd6f4e32869ae932b99f5463
origin: build-site
parents:
  - hyp:renderers-r3
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-063: Mermaid renderer"
type: task
---

**Description:** Implement `MermaidRenderer.render(rep) -> str`. Outputs `flowchart TD` followed by node and edge declarations. Deduplicates by id and edge triple.

**Files:** `agi-tree/src/renderers/mermaid.py`, `agi-tree/tests/renderers/test_mermaid.py`

**Test Strategy:** Validate output via the `mermaid-cli` (npx mmdc) parse step in CI; idempotency test; uniqueness test.
