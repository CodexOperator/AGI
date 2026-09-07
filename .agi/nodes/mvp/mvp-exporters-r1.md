---
id: mvp:exporters-r1
mint_id: 0108a4dfb3f74530b278afb92d3749f8
type: mvp
parents:
  - verdict:exporters-r1
next_edges:
  - outcome:exporters-r1
confidence: 1.0
edited_by: season.py
season: 1
status: open
tags:
  - exporters
  - R1
  - mvp
thought_session: season
title: "MVP: Exporters R1 — Markdown Exporter"
---
# MVP: Markdown Chain Exporter

Exports capillary DAG chains as Markdown files with YAML frontmatter.

## Script

`experiments/exp-exporters-r1-markdown.py`

## Usage

```python
from experiments.exp_exporters_r1_markdown import export_chain_to_markdown
from graph_core.loader import load_directory
from chain_engine.chains import find_chains

graph, _ = load_directory('nodes')
chains = find_chains(graph)
export_chain_to_markdown(chains[0], graph, '/tmp/exported')
```

## Features

- Valid YAML frontmatter (Obsidian/Logseq compatible)
- Wikilinks to adjacent chain nodes
- Chain position metadata
- No file collisions across multiple chains