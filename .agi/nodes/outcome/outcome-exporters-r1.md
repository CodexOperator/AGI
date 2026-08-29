---
confidence: 1.0
id: "outcome:exporters-r1"
mint_id: 5432bd58a77d4f71aea9114ed111735d
next_edges:
  - bigger_outcome:exporters-r1
parents:
  - mvp:exporters-r1
status: open
tags:
  - exporters
  - R1
  - outcome
title: "Outcome: Exporters R1"
type: outcome
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
