---
id: goal:g2.4
mint_id: 9ffd95c01c5743dab4969860d8dbe1e9
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.4
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G2.4: Embeddings into the production renderer path"
---
gensim + UMAP embeddings exist and are not on the renderer path (**H7**).
Relevant to this goal rather than to G9 because a projection is a zoom
operation: it is how level 1 and 2 get a spatial layout that is stable as the
graph grows, which is what G9.4's viewport needs to pan across without the graph
rearranging itself under the reader.

Note `.gitnexus/meta.json` reports `embeddings: 0` — nothing is generated today,
and `npx gitnexus analyze` without `--embeddings` deletes any that exist.