---
id: "bigger-outcome:schema-registry-r2"
mint_id: 8e87962417424ff5896bdc57af94a50e
next_edges:
  - app-purpose:schema-registry
parents:
  - outcome:schema-registry-r2-bracket-convention
subgraph: false
tags:
  - schema-registry
  - R2
  - bracket-convention
  - chain-closure
title: "schema-registry/R2: Bigger Outcome — Bracket Convention"
type: bigger_outcome
---

**Broader outcome:** Schema-registry R2 Bracket Convention enables clean schema activation/deactivation. Active schemas (bracketed) are discovered via cascade: bracket detection → fingerprint → LM hook. This separates schema definition (file) from schema activation (convention), enabling drop-in extensions without code changes.

**Properties achieved:**
- Schema as File (R1): file operations only
- Bracket Convention (R2): active vs inactive schemas via [[...]] vs [...]
- Bracket → Fingerprint → LM Hook cascade (R5/R6): automatic schema discovery
- Bracket Convention chain fully closes: idea → hyp → exp → verdict → mvp → outcome → bigger_outcome → app_purpose

**Chain status:** 15-hop chain restored (was 8-hop broken at outcome:schema-registry-r2-bracket-convention).
