---
id: "app-purpose:exporters"
mint_id: 03558d7608d34dd486827f08807f2248
parents:
  - bigger-outcome:exporters-r1
status: open
tags:
  - exporters
  - app_purpose
title: "App Purpose: Exporters"
type: app_purpose
---

# App Purpose: Exporters

**Mission**: Make the capillary DAG accessible to external tools and workflows.

## Purpose

The capillary DAG stores research chains (idea → hypothesis → experiment → verdict → MVP → outcome → bigger_outcome → app_purpose) but currently exists in isolation. Exporters enable:

1. **Knowledge portability** — export chains to Obsidian, Logseq, Notion
2. **Data interoperability** — JSON/JSON Schema for programmatic access
3. **Visualization** — Mermaid diagrams for documentation and presentations
4. **Collaboration** — standard Markdown formats for team sharing

## Core Value

Researchers invest time building capillary DAG chains. Exporters ensure this investment isn't locked into one tool. The same chain can live in the DAG, Obsidian vault, and JSON API simultaneously.

## Success Metrics

- [ ] Chains export to Obsidian without data loss
- [ ] JSON Schema validates all exported chains
- [ ] Mermaid renders correctly in GitHub/GitLab
- [ ] Incremental export < 100ms for typical changes
