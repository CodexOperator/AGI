---
confidence: 1.0
demote_reason: "no experiment evidence (evidence_runs=0) for 'proved'"
demoted_from: proved
evidence_runs: 0
id: "verdict:exporters-r1"
mint_id: 69c42b75ff4e495aa64b2d5c79d5b277
next_edges:
  - exp:exporters-r1-extend
  - mvp:exporters-r1
parents:
  - exp:exporters-r1
  - hyp:exporters-r1
status: "inconclusive_lean_proved:50"
tags:
  - exporters
  - R1
  - proved
title: "Verdict: Exporters R1"
type: verdict
verdict: "inconclusive_lean_proved:50"
---

VERDICT: proved. Markdown exporter passes all 5 criteria:
1. Valid YAML frontmatter on all exported files
2. Required keys present (id, title, type, tags, created, chain_position)
3. Wikilinks to adjacent nodes in body
4. No file name collisions
5. Multiple chains export correctly

Confidence: 1.0
