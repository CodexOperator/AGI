---
id: hyp:renderers-r4
mint_id: 658337671af34e5fb20b53e5d4d2ff3e
type: hypothesis
parents:
  - idea:domain-renderers
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - renderers
  - R4
testable_claim: Git-Tree Renderer
thought_session: L1.09
title: "renderers/R4: Git-Tree Renderer"
---
**Description:** A renderer produces a view shaped like the output of a graph-style git log, where each chain corresponds to one branch shape.

**Acceptance Criteria:**
- [ ] Each chain in the input appears as one branch-shaped lane in the output
- [ ] Lane order is deterministic and rooted in the highest-scoring chain
- [ ] Merge points (where two chains share a node) render as a visible junction
- [ ] The output uses only printable ASCII characters

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `git_tree.py` anywhere in the tree; no existing goal obviously covers a git-tree renderer with lanes and merge junctions, so this THOUGHT is the record.
<!-- THOUGHT:END -->
