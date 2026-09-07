---
id: verdict:graph-core-r5-by-citation
mint_id: 30f6d3b2f45a47e2ada89bf459b9e449
type: verdict
parents:
  - hyp:graph-core-r5
next_edges: []
confidence: 0.8
edited_by: season.py
evidence_runs:
  - build:tests-graph-core-test-recursive-bodies
  - build:tests-graph-core-test-uniform-contract
scaffold_hash: 6285154113614fef
season: 1
supports:
  - hyp:graph-core-r5
tags:
  - graph-core
  - R5
  - l1.09
  - by-citation
thought_session: season
title: "graph-core/R5: closed by citation"
verdict: inconclusive_lean_proved:80
---
# verdict:graph-core-r5-by-citation

## Verdict

`inconclusive_lean_proved:80` — **closed by citation, not by a run** (L1.09, 2026-09-03).

## Evidence

`hyp:graph-core-r5` — *Recursive Node Bodies* — was specified by the cavekit build-site and never reached a verdict there. The real, non-build-site tree already carries what it asked for:

- `build:tests-graph-core-test-recursive-bodies` → `extensions/agi/tests/graph_core/test_recursive_bodies.py`
- `build:tests-graph-core-test-uniform-contract` → `extensions/agi/tests/graph_core/test_uniform_contract.py`

Grounds: `test_recursive_bodies.py` loads nested subgraphs three levels deep and `test_uniform_contract.py` asserts node and subgraph share one contract.

Survey: `.agi/sessions/L1.09-mining/report.md` §C. Nothing was executed for this verdict; the suites named above are the ones `commands.py run tests` already runs.

## Confidence

0.8 — the citations are real files with real test suites, but this verdict cites them rather than running them, which is why it is `inconclusive_lean_proved:80` and not `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written 2026-09-03 in L1.09 to close `hyp:graph-core-r5` by citation per the build-site survey (§C); the hypothesis is deprecated in the same pass with its `origin: build-site` cohort (goal:s18), and this verdict is the live record of where its claim is actually satisfied.
<!-- THOUGHT:END -->