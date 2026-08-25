---
confidence: 1.0
id: "idea:domain-environment-indexers"
mint_id: 9fcdef758ca7454ab44442eca8695996
next_edges:
  - hyp:environment-indexers-r1
origin: build-site
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: environment-indexers"
type: idea
---

Pluggable indexers that consume an external source (a directory tree, a code repository, a Python project, an OpenAPI specification, a running container) and emit nodes into the graph through graph-core and the schema-registry. Indexers are on-demand: nothing scans automatically until invoked. Each indexer is one self-contained file with documented internals so future replacements can be made surgically.
