---
confidence: 1.0
id: "idea:domain-schema-registry"
mint_id: 8d9dbe32b28646c5861fb3c6b828ea69
next_edges:
  - hyp:schema-registry-r2
origin: build-site
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: schema-registry"
type: idea
---

A registry of schemas that define what node types exist, what their frontmatter must contain, and how directories of files are interpreted as nodes. Schemas are themselves graph nodes, so the registry is observable from inside the graph. New schemas can be added by dropping a file. When data is encountered that no schema explains, a hook can ask a language model to propose a new schema. This kit is how the autoresearch domain (and any future domain) plugs in without touching graph-core.
