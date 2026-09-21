---
id: exp:a00-8636e255-bf1a6c
mint_id: 8e1d2230bb70489f9d1abc1f7817ff72
type: experiment
parents:
  - hyp:a00-8636e255-bf1a6c
next_edges:
  - verdict:a00-8636e255-bf1a6c
confidence: 1.0
edited_by: season.py
season: 1
status: completed
tags:
  - renderers
  - mermaid
  - r3
  - determinism
  - validity
thought_session: season
title: "Experiment: Mermaid Renderer R3 — validity and determinism"
---
**Experiment:** Test Mermaid renderer (R3) against 5 acceptance criteria:
1. Deterministic output (byte-identical across runs)
2. Valid `flowchart TD` directive
3. All input nodes present in output (dedup)
4. All input edges present in output (dedup)
5. No unquoted complex ids in edges

**Result:** 5/5 criteria PROVED.

- 2074 input nodes, 2074 in output (100% coverage)
- 1893 input edges, 1893 in output (100% coverage)
- Output deterministic across 2 runs
- Valid directive: `flowchart TD`
- No Mermaid-unsafe edge targets