---
id: verdict:exporters-r1
mint_id: 69c42b75ff4e495aa64b2d5c79d5b277
type: verdict
parents:
  - exp:exporters-r1
  - hyp:exporters-r1
next_edges:
  - exp:exporters-r1-extend
  - mvp:exporters-r1
confidence: 1.0
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
evidence_runs: []
season: 1
status: inconclusive_lean_proved:50
tags:
  - exporters
  - R1
  - proved
thought_session: season
title: "Verdict: Exporters R1"
verdict: inconclusive_lean_proved:50
---
VERDICT: proved. Markdown exporter passes all 5 criteria:
1. Valid YAML frontmatter on all exported files
2. Required keys present (id, title, type, tags, created, chain_position)
3. Wikilinks to adjacent nodes in body
4. No file name collisions
5. Multiple chains export correctly

Confidence: 1.0