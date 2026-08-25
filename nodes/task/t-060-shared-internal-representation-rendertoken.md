---
acceptance_criteria:
  - R1.1 (RenderToken exposes id/label/type/depth/x/y/edges)
  - R1.2 (build is deterministic: identical graphs → identical token sequences)
  - R1.3 (representation accepted by every renderer without conversion shims)
  - R1.4 (representation is a documented contract for external consumers — embeddings)
blocked_by:
  - task:t-001
  - task:t-003
cavekit_req: renderers/R1
effort: M
id: "task:t-060"
mint_id: 7dd8400cba604d838ecb9f8287e21ab3
origin: build-site
parents:
  - hyp:renderers-r1
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-060: Shared internal representation (RenderToken)"
type: task
---

**Description:** Define `RenderToken` dataclass with seven fields. Implement `build_representation(graph)` that traverses deterministically (sorted ids), assigns a default depth via BFS from roots, default x/y as zero (overridden later by embeddings), and edges = list of `(target_id, relation)`. Document the contract in a header docstring.

**Files:** `agi-tree/src/renderers/representation.py`, `agi-tree/tests/renderers/test_representation.py`

**Test Strategy:** Tests for field surface, determinism (same graph twice), contract test (each renderer accepts the representation without conversion).
