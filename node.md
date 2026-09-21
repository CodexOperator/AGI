---
id: outcome:exporters-r1
mint_id: 5432bd58a77d4f71aea9114ed111735d
type: outcome
parents:
  - mvp:exporters-r1
next_edges:
  - bigger_outcome:exporters-r1
confidence: 1.0
edited_by: season.py
judged_against: goal:g9.3
lens: goal:g9
season: 1
status: open
tags:
  - exporters
  - R1
  - outcome
thought_session: season
title: "Outcome: Exporters R1"
---
# Outcome: Markdown Chain Exporter

## Input Shape

- Graph with nodes (id, type, tags, parents, children)
- Chain list from `find_chains()` (list of node ID lists)

## Output Shape

- Markdown files in target directory
- Each file: YAML frontmatter + Markdown body
- Wikilinks `[[node-id]]` for adjacency navigation

## Behavior

1. Loads capillary DAG graph
2. Finds all chains via `find_chains()`
3. For each node in chain:
   - Creates YAML frontmatter with required fields
   - Adds wikilinks to prev/next nodes
   - Writes `.md` file with unique filename

## Edge Cases

- Empty graph: returns empty list (handled gracefully)
- Single-node chain: exports with no wikilinks
- Unicode in node IDs: escaped in filenames
- Long filenames: truncated to filesystem limits

## Confidence

1.0 (5/5 tests passed)