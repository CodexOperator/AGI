---
confidence: 1.0
id: "idea:domain-renderers"
mint_id: 49fc7f1d1f56476f8c28178f1322a3ab
next_edges:
  - hyp:renderers-r1
origin: build-site
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: renderers"
type: idea
---

Multi-format renderers that turn a graph into human-readable views. All renderers consume a single shared internal representation, so a new renderer is one class implementing a single method. The same representation is also consumed by the embeddings kit, which is what keeps visualization and embedding isomorphic. Renderers are pure functions: same input, same output, no side effects.
