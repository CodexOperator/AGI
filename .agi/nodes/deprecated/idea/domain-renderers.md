---
id: idea:domain-renderers
mint_id: 49fc7f1d1f56476f8c28178f1322a3ab
type: idea
next_edges:
  - hyp:renderers-r1
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
title: "Domain: renderers"
---
Multi-format renderers that turn a graph into human-readable views. All renderers consume a single shared internal representation, so a new renderer is one class implementing a single method. The same representation is also consumed by the embeddings kit, which is what keeps visualization and embedding isomorphic. Renderers are pure functions: same input, same output, no side effects.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §B/§D/§E): the domain is partially built at `extensions/agi/src/renderers/` (`idea:engine-renderers` is the live counterpart); the three unbuilt pieces (R4 git-tree, R6 recursive, R7 plugin contract) are recorded on their hypotheses' THOUGHTs, the plugin generality being part of the abandoned package framing; no new goal (§B).
<!-- THOUGHT:END -->