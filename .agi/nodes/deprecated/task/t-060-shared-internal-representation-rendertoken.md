---
id: task:t-060
mint_id: 7dd8400cba604d838ecb9f8287e21ab3
type: task
parents:
  - hyp:renderers-r1
acceptance_criteria:
  - R1.1 (RenderToken exposes id/label/type/depth/x/y/edges)
  - {"R1.2 (build is deterministic": "identical graphs \u2192 identical token sequences)"}
  - R1.3 (representation accepted by every renderer without conversion shims)
  - R1.4 (representation is a documented contract for external consumers — embeddings)
blocked_by:
  - task:t-001
  - task:t-003
cavekit_req: renderers/R1
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-060: Shared internal representation (RenderToken)"
---
**Description:** Define `RenderToken` dataclass with seven fields. Implement `build_representation(graph)` that traverses deterministically (sorted ids), assigns a default depth via BFS from roots, default x/y as zero (overridden later by embeddings), and edges = list of `(target_id, relation)`. Document the contract in a header docstring.

**Files:** `agi-tree/src/renderers/representation.py`, `agi-tree/tests/renderers/test_representation.py`

**Test Strategy:** Tests for field surface, determinism (same graph twice), contract test (each renderer accepts the representation without conversion).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R1` under `hyp:renderers-r1`, whose disposition is already closed by `verdict:renderers-r1` before this pass; deprecated with its domain (`idea:domain-renderers`).
<!-- THOUGHT:END -->
