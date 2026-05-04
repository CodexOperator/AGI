---
id: hyp:lru-saturates-warm-load
parents:
- idea:capillary-dag-memory
tags:
- performance
- warm-load
title: LRU cache on builder object saturates warm load at hardware noise floor
type: hypothesis
---

The hypothesis: caching the GraphBuilder object via lru_cache makes warm
load O(1) regardless of node count. Predecessor iter 21 confirmed.
