---
confidence: 1.0
contrasts: []
evidence_runs:
  - exp:schema-registry-r1
id: "verdict:schema-registry-r1"
mint_id: 4a2f29d1b2394e9ca86f2f545d131210
next_edges:
  - exp:schema-registry-r1-extend
  - mvp:schema-registry-r1
parents:
  - exp:schema-registry-r1
status: proved
subgraph: false
supports: []
tags:
  - schema-registry
  - R1
title: "schema-registry/R1: Verdict"
type: verdict
---

**Verdict:** PROVED

**Evidence:**
- 41/41 schema-registry tests pass
- R1.1: Schema files at known paths load correctly
- R1.2: Drop-in new schema (no restart needed)
- R1.3: Removed schema → generic fallback + warning
- R1.4: JSON schema format accepted alongside Markdown
- R2.1–R2.4: Bracket convention working (bracketed = active, unbracketed = inactive)
