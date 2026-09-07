---
id: idea:domain-schema-registry
mint_id: 8d9dbe32b28646c5861fb3c6b828ea69
type: idea
next_edges:
  - hyp:schema-registry-r2
confidence: 1.0
edited_by: season.py
origin: build-site
scale: big
season: 1
status: deprecated
tags:
  - domain
  - seed
thought_session: season
title: "Domain: schema-registry"
---
A registry of schemas that define what node types exist, what their frontmatter must contain, and how directories of files are interpreted as nodes. Schemas are themselves graph nodes, so the registry is observable from inside the graph. New schemas can be added by dropping a file. When data is encountered that no schema explains, a hook can ask a language model to propose a new schema. This kit is how the autoresearch domain (and any future domain) plugs in without touching graph-core.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §B/§D/§E): the domain is built at `extensions/agi/src/schema_registry/` (`idea:engine-schema-registry` is the live counterpart) and `goal:s17` already tracks the one real gap, spawn-time enforcement; no new goal (§B).
<!-- THOUGHT:END -->