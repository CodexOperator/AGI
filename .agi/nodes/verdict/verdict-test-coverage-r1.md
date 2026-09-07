---
id: verdict:test-coverage-r1
mint_id: 2505427d31594df6a4880dcf44c78043
type: verdict
parents:
  - hyp:test-coverage-r1
confidence: 0.41
demote_reason: no experiment evidence (evidence_runs=0) for 'disproved'
demoted_from: disproved
domain: test-coverage
edited_by: season.py
evidence_runs:
  - exp:test-coverage-r1
season: 1
status: inconclusive_lean_disproved:50
tags:
  - tests
  - coverage
  - R1
thought_session: season
title: "R1: Test coverage analysis of node types, edge relations, and graph operations"
verdict: inconclusive_lean_disproved:50
---
**Verdict:** DISPROVED

**Coverage Metrics:**
- Overall: 41.4%
- Node types: 20.0% (2/10)
- Operations: 90.0% (9/10)
- Hypotheses with verdicts: 14.1% (9/64)

**Evidence:**
- 258 test functions across 38 files
- Threshold: 80.0%

**Interpretation:**
Coverage (41%) below threshold (80.0%)

**Categories by test count:**
- other_tests: 215
- graph_operations: 17
- schema_tests: 11
- chain_tests: 5
- core_tests: 3
- environment_tests: 3
- embedding_tests: 2
- render_tests: 2