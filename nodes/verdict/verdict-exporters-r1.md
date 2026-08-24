---
id: verdict:exporters-r1
title: "Verdict: Exporters R1"
type: verdict
status: proved
verdict: inconclusive_lean_proved:50
confidence: 1.0
parents:
  - exp:exporters-r1
  - hyp:exporters-r1
tags:
  - exporters
  - R1
  - proved
next_edges:
  - exp:exporters-r1-extend
  - mvp:exporters-r1
evidence_runs: 0
demoted_from: proved
demote_reason: 'no experiment evidence (evidence_runs=0) for ''proved'''
---

VERDICT: proved. Markdown exporter passes all 5 criteria:
1. Valid YAML frontmatter on all exported files
2. Required keys present (id, title, type, tags, created, chain_position)
3. Wikilinks to adjacent nodes in body
4. No file name collisions
5. Multiple chains export correctly

Confidence: 1.0
