---
id: bigger_outcome:schema-registry-r1
mint_id: f695c4be5cec4aa8aad40dcda01b3ea2
type: bigger_outcome
parents:
  - outcome:schema-registry-r1
next_edges:
  - vision:schema-registry
edited_by: season.py
judged_against: goal:g3
season: 1
subgraph: false
tags:
  - schema-registry
  - R1
thought_session: season
title: "schema-registry/R1: Bigger Outcome"
---
**Broader outcome:** Schema-registry enables drop-in extension of the graph's type system without code changes. Schemas live as files in `context/schemas/`, bracket convention controls activation, and the cascade (bracket → fingerprint → LM hook) handles auto-discovery. New domains can plug in by dropping schema files.

**Properties achieved:**
- Schema as File (R1): file operations only
- Bracket Convention (R2): active vs inactive schemas
- Schemas as Metanodes (R3): schema definitions are observable in the graph
- Optional Validation (R4): schema-based validation is pluggable
- Auto-Discovery Cascade (R5): bracket → fingerprint → LM hook
- Pluggable LM Hook (R6): language model can propose schemas on demand
- Generated Schemas Land Inactive (R7): LM output needs human approval
- Built-in Schemas (R8): core node types have shipped schemas