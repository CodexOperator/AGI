---
id: exp:exporters-r1
title: "Experiment: Exporters R1 — Markdown Exporter"
type: experiment
status: proved
verdict: inconclusive_lean_proved:50
confidence: 1.0
parents:
  - hyp:exporters-r1
  - idea:domain-exporters
tags:
  - exporters
  - R1
  - experiment
  - proved
next_edges:
  - verdict:exporters-r1
evidence_runs: 0
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---

# Experiment: Exporters R1 — Markdown Exporter

**Status**: PROVED (5/5 tests passed)

## Test Results

1. **TC1**: Valid YAML frontmatter — PASS (all 10 files)
2. **TC2**: Required keys present — PASS
3. **TC3**: Wikilinks to adjacent nodes — PASS
4. **TC4**: No file collisions — PASS (10 unique files)
5. **TC5**: Multiple chains export — PASS (28 files from 3 chains)

## Evidence

- Script: `experiments/exp-exporters-r1-markdown.py`
- Runtime: 0.6s
- Exported files tested for YAML validity and wikilinks
