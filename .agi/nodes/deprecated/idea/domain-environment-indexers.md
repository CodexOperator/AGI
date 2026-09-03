---
id: idea:domain-environment-indexers
mint_id: 9fcdef758ca7454ab44442eca8695996
type: idea
next_edges:
  - hyp:environment-indexers-r1
confidence: 1.0
edited_by: l1.09-execution-parent
origin: build-site
scale: big
status: deprecated
tags:
  - domain
  - seed
thought_session: L1.09
title: "Domain: environment-indexers"
---
Pluggable indexers that consume an external source (a directory tree, a code repository, a Python project, an OpenAPI specification, a running container) and emit nodes into the graph through graph-core and the schema-registry. Indexers are on-demand: nothing scans automatically until invoked. Each indexer is one self-contained file with documented internals so future replacements can be made surgically.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §B/§D/§E): zero real implementation of any kind exists and its R1 closure is hollow (§F R1); this is the domain that did not survive `goal:g11`, and no goal is minted for it (§B).
<!-- THOUGHT:END -->
