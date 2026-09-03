---
id: idea:domain-graph-core
mint_id: 8f731f3bc4984fefbb39e96289869c65
type: idea
next_edges:
  - hyp:graph-core-r1
  - hypothesis:a01-144a1c04-8ba9b7
  - hypothesis:a01-92759282-8e21ce
  - hypothesis:a01-eb185005-a7478c
confidence: 1.0
edited_by: l1.09-execution-parent
origin: build-site
scale: big
status: deprecated
tags:
  - domain
  - seed
thought_session: L1.09
title: "Domain: graph-core"
---
Generic, domain-agnostic graph primitives: nodes, edges, identity, persistence, recursive bodies, directory-walking auto-discovery, and a portable bootstrap path. This kit is the substrate every other domain stands on. It contains nothing autoresearch-specific; the same primitives could be reused for any DAG memory product.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §B/§D/§E): the domain is substantially already built at `extensions/agi/src/graph_core/` (`idea:engine-graph-core` is the live counterpart); no new goal (§B), and retiring this 68-descendant attractor lets target selection fall through to `idea:engine-tests` and siblings (§D).
<!-- THOUGHT:END -->
