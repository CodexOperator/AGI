---
id: "app-purpose:schema-registry"
mint_id: 59709ef186e34a1ca1eafb5c355fd4b9
next_edges: []
parents:
  - bigger-outcome:schema-registry-r1
subgraph: false
tags:
  - schema-registry
  - root
title: "App Purpose: schema-registry"
type: app_purpose
---

**App Purpose:** Drop-in schema registry enabling the graph to extend its type system without code changes. Schemas live as files, bracket convention controls activation, and the cascade (bracket → fingerprint → LM hook) handles auto-discovery. Every future domain plugs in by dropping schema files — zero code required.
