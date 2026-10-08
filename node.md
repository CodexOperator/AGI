---
id: idea:domain-exporters
mint_id: 1feed57b3b594ce6a108f4926e46f2a0
type: idea
next_edges:
  - hyp:exporters-r1
edited_by: season.py
season: 1
status: open
tags:
  - domain
  - fresh-idea
  - iter13
thought_session: season
title: "Domain: Exporters"
---
# Big Idea: Exporters — Capillary DAG to External Formats

Export capillary DAG chains to existing knowledge management tools (Obsidian, Logseq) and structured formats (JSON Schema, Mermaid).

## Motivation

The capillary DAG stores research chains (idea → hypothesis → experiment → verdict → MVP → outcome → bigger_outcome → app_purpose) but currently has no interoperability with external tools. Exporting enables:

1. **Obsidian/Logseq compatibility** — generate Markdown files with proper frontmatter that these tools understand
2. **JSON Schema output** — structured data for programmatic consumers
3. **Mermaid diagrams** — chain visualization for documentation
4. **Git diff friendly** — export format that plays well with version control

## Hypotheses

- **R1 (Markdown Exporter)**: Markdown files with YAML frontmatter matching Obsidian/Logseq spec
- **R2 (JSON Schema Exporter)**: JSON export with full chain structure
- **R3 (Mermaid Exporter)**: Mermaid flowchart format from chains
- **R4 (Incremental Export)**: Only export changed chains since last export

## Success Criteria

- [ ] Exported files are valid Obsidian/Logseq readable
- [ ] JSON Schema validates against known structure
- [ ] Mermaid output renders correctly
- [ ] Incremental export is faster than full export

## Dependencies

- graph-core (Node/Edge primitives)
- chain-engine (find_chains)
- renderers (Representation)