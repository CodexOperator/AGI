---
id: verdict:graph-core-r4-by-citation
mint_id: cd7360d04bae4bcba55d256646995d15
type: verdict
parents:
  - hyp:graph-core-r4
next_edges: []
confidence: 0.8
edited_by: l1.09-execution-parent
evidence_runs:
  - build:src-graph-core-persistence-frontmatter
  - build:src-graph-core-persistence-lazy-body
  - build:tests-graph-core-test-frontmatter
  - build:tests-graph-core-test-frontmatter-errors
  - build:tests-graph-core-test-lazy-body
scaffold_hash: c46f17eb4df1df82
supports:
  - hyp:graph-core-r4
tags:
  - graph-core
  - R4
  - l1.09
  - by-citation
thought_session: L1.09
title: "graph-core/R4: closed by citation"
verdict: inconclusive_lean_proved:80
---
# verdict:graph-core-r4-by-citation

## Verdict

`inconclusive_lean_proved:80` — **closed by citation, not by a run** (L1.09, 2026-09-03).

## Evidence

`hyp:graph-core-r4` — *Frontmatter File Persistence* — was specified by the cavekit build-site and never reached a verdict there. The real, non-build-site tree already carries what it asked for:

- `build:src-graph-core-persistence-frontmatter` → `extensions/agi/src/graph_core/persistence/frontmatter.py`
- `build:src-graph-core-persistence-lazy-body` → `extensions/agi/src/graph_core/persistence/lazy_body.py`
- `build:tests-graph-core-test-frontmatter` → `extensions/agi/tests/graph_core/test_frontmatter.py`
- `build:tests-graph-core-test-frontmatter-errors` → `extensions/agi/tests/graph_core/test_frontmatter_errors.py`
- `build:tests-graph-core-test-lazy-body` → `extensions/agi/tests/graph_core/test_lazy_body.py`

Grounds: `persistence/frontmatter.py` is the round-tripping reader/writer with one failure class (`FrontmatterError`) and `lazy_body.py` the lazy body read; the three suites cover round-trip, error isolation and laziness.

Survey: `.agi/sessions/L1.09-mining/report.md` §C. Nothing was executed for this verdict; the suites named above are the ones `commands.py run tests` already runs.

## Confidence

0.8 — the citations are real files with real test suites, but this verdict cites them rather than running them, which is why it is `inconclusive_lean_proved:80` and not `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written 2026-09-03 in L1.09 to close `hyp:graph-core-r4` by citation per the build-site survey (§C); the hypothesis is deprecated in the same pass with its `origin: build-site` cohort (goal:s18), and this verdict is the live record of where its claim is actually satisfied.
<!-- THOUGHT:END -->
