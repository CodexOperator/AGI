---
id: bigger_outcome:schema-registry-r2
mint_id: 8e87962417424ff5896bdc57af94a50e
type: bigger_outcome
parents:
  - outcome:schema-registry-r2-bracket-convention
next_edges:
  - vision:schema-registry
edited_by: season.py
judged_against: goal:g3
season: 1
subgraph: false
tags:
  - schema-registry
  - R2
  - bracket-convention
  - chain-closure
thought_session: season
title: "schema-registry/R2: Bigger Outcome — Bracket Convention"
---
**Broader outcome:** Schema-registry R2 Bracket Convention enables clean schema activation/deactivation. Active schemas (bracketed) are discovered via cascade: bracket detection → fingerprint → LM hook. This separates schema definition (file) from schema activation (convention), enabling drop-in extensions without code changes.

**Properties achieved:**
- Schema as File (R1): file operations only
- Bracket Convention (R2): active vs inactive schemas via [[...]] vs [...]
- Bracket → Fingerprint → LM Hook cascade (R5/R6): automatic schema discovery
- Bracket Convention chain fully closes: idea → hyp → exp → verdict → mvp → outcome → bigger_outcome → app_purpose

**Chain status:** 15-hop chain restored (was 8-hop broken at outcome:schema-registry-r2-bracket-convention).