---
id: hyp:renderers-r2
mint_id: a60a3d65d9654a8394e4ca0a915e86d3
type: hypothesis
parents:
  - idea:domain-renderers
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - renderers
  - R2
testable_claim: ASCII Renderer (Primary)
thought_session: season
title: "renderers/R2: ASCII Renderer (Primary)"
---
**Description:** A primary renderer produces a compact text view bounded by 200 lines and 200 columns. The view is hierarchical and includes a summary of edges and a count of node types.

**Acceptance Criteria:**
- [ ] Rendering any graph produces output of at most 200 lines and at most 200 columns
- [ ] When the graph is too large for the bounds, the renderer compresses or truncates with a clearly visible marker rather than overflowing
- [ ] The output includes a per-type count and a summary of edges
- [ ] Two runs against the same graph produce byte-equal output

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:renderers-r2-by-citation` citing `build:src-renderers-ascii`, `build:tests-renderers-test-ascii`, `build:tests-renderers-test-ascii-summary`: `ascii.py` is the bounded ASCII renderer with a type/edge summary; `test_ascii.py` and `test_ascii_summary.py` pin byte-equal output.
<!-- THOUGHT:END -->