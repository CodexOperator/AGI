---
confidence: 1.0
contrasts: []
evidence_runs:
  - exp:renderers-r1
id: "verdict:renderers-r1"
mint_id: 1d87f0b5e9104526bedeb49bc1f26000
next_edges:
  - exp:renderers-r1-extend
  - mvp:renderers-r1
parents:
  - exp:renderers-r1
status: proved
subgraph: false
supports: []
tags:
  - renderers
  - R1
title: "renderers/R1: Verdict"
type: verdict
---

**Verdict:** PROVED

**Evidence:**
- 31/31 renderers tests pass (ASCII, Mermaid, Git-diff, Representation)
- R1.1: RenderToken exposes id, label, type, depth, x, y, edges (7 fields)
- R1.2: build_representation is deterministic — same graph yields same tokens
- R1.3: ASCII renderer accepts representation without conversion shims
- R1.4: Empty graph yields empty representation
