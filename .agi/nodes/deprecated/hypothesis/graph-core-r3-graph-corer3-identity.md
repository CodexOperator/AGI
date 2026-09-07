---
id: hyp:graph-core-r3
mint_id: 32d35fb88dda4a7aadef91eb1c780d26
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - graph-core
  - R3
testable_claim: Identity Scheme
thought_session: season
title: "graph-core/R3: Identity Scheme"
---
**Description:** Node ids follow a stable, human-legible scheme that is compact enough to render in ASCII frames.

**Acceptance Criteria:**
- [ ] Each id matches the pattern `<type-prefix>:<short-slug>` where `short-slug` is kebab-case of two to five words
- [ ] When two nodes would otherwise collide, the second receives a `:n` numeric suffix starting at `:2`
- [ ] Ids exceeding 40 characters trigger a non-fatal warning but are still accepted
- [ ] Ids are stable across rebuilds: regenerating the graph from the same source files produces the same ids

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r3-by-citation` citing `build:src-graph-core-identity`, `build:tests-graph-core-test-identity`: `identity.py` is the identity scheme (slug plus `mint_permanent_id`, the goal:g2.5 mint id) and `test_identity.py` is its suite.
<!-- THOUGHT:END -->