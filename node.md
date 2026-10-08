---
id: idea:domain-test-coverage
mint_id: c299a41ead33404c9d2d0c5f74e84ee4
type: idea
next_edges:
  - hyp:test-coverage-r1
domain: test-coverage
edited_by: season.py
season: 1
tags:
  - tests
  - pytest
  - coverage
  - meta
  - quality
thought_session: season
title: "Test Coverage: Meta-Analysis of the 257 Pytest Tests"
---
# Domain: Test Coverage Analysis

## Concept
Meta-analysis of the pytest test suite that validates the agi-tree graph system. Understand what the 257 tests cover, find gaps, and measure coverage quality.

## Motivation
- The AGENTS.md mentions "241 pytest tests" (stale number — actually 257)
- Tests are critical for preventing regressions in graph operations
- Coverage analysis reveals untested edge cases
- Meta-level: testing the testing infrastructure

## Child Hypotheses

1. **hyp:test-coverage-r1**: What percentage of node types, edge relations, and graph operations are covered by tests?
2. **R2**: Which hypothesis nodes have no corresponding experiment/verdict?
3. **R3**: Are there critical paths (chain discovery, next_edge persistence) with insufficient tests?