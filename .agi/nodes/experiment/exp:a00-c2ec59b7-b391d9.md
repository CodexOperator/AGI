---
id: exp:a00-c2ec59b7-b391d9
mint_id: 1092eeaa56b844eaaeaace762617cd4c
type: experiment
parents:
  - hyp:a00-c2ec59b7-b391d9
next_edges:
  - verdict:a00-c2ec59b7-b391d9
edited_by: season.py
season: 1
tags:
  - renderers
  - ascii
  - isomorphism
  - spearman
thought_session: season
title: ASCII render proximity vs graph descendant overlap
---
## Method

1. Loaded graph (983 nodes, 802 with descendants) via `graph_core.loader.load_directory`
2. Computed BFS descendant sets for all 983 nodes
3. Sampled 30 random node pairs (seed=42), computed Jaccard overlap
4. Built Representation via `renderers.build_representation`
5. Extracted token order (position in Representation = render proximity)
6. Computed Spearman rank correlation between Jaccard overlap and order proximity

## Results

- Spearman correlation: **-0.903** (strongly negative)
- Top-5 overlapping pairs avg order diff: **280.2** tokens
- 30/30 pairs had position data (full coverage via token `id` mapping)

## Interpretation

Strong anti-correlation means: high-overlap nodes appear FARTHER apart in ASCII render.
This is the opposite of what the hypothesis claimed.

ASCII renderer groups by type first, then alphabetical — this ordering is orthogonal to graph topology.