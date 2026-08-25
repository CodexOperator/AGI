---
confidence: 0.5
id: "hyp:embeddings-r6"
mint_id: 7c0147827da54752a3d344ac0b6959f1
origin: build-site
parents:
  - idea:domain-embeddings
subgraph: false
tags:
  - embeddings
  - R6
testable_claim: Scatter Rendering Plugin
title: "embeddings/R6: Scatter Rendering Plugin"
type: hypothesis
---

**Description:** A renderer plugin produces an ASCII scatter view directly from UMAP coordinates, sharing the renderer plugin contract.

**Acceptance Criteria:**
- [ ] The plugin is registered through the same renderer plugin contract used by the renderers kit
- [ ] The plugin places each node at coordinates derived from its UMAP `(x, y)` without re-projecting
- [ ] Output respects the ASCII renderer's bounds (at most 200 lines and 200 columns) and degrades visibly when bounds are exceeded
- [ ] When two nodes overlap at the same character cell, the cell shows a documented overlap marker

**Dependencies:** renderers (R7)
