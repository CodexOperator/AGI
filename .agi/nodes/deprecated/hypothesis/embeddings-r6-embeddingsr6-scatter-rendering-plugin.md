---
id: hyp:embeddings-r6
mint_id: 7c0147827da54752a3d344ac0b6959f1
type: hypothesis
parents:
  - idea:domain-embeddings
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - embeddings
  - R6
testable_claim: Scatter Rendering Plugin
thought_session: L1.09
title: "embeddings/R6: Scatter Rendering Plugin"
---
**Description:** A renderer plugin produces an ASCII scatter view directly from UMAP coordinates, sharing the renderer plugin contract.

**Acceptance Criteria:**
- [ ] The plugin is registered through the same renderer plugin contract used by the renderers kit
- [ ] The plugin places each node at coordinates derived from its UMAP `(x, y)` without re-projecting
- [ ] Output respects the ASCII renderer's bounds (at most 200 lines and 200 columns) and degrades visibly when bounds are exceeded
- [ ] When two nodes overlap at the same character cell, the cell shows a documented overlap marker

**Dependencies:** renderers (R7)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `scatter.py`, and the renderer plugin contract it was blocked on (`hyp:renderers-r7`) does not exist; scoped by `goal:s32`.
<!-- THOUGHT:END -->
