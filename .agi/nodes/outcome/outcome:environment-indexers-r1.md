---
id: outcome:environment-indexers-r1
mint_id: 5c464e2b5448400ba53a43c8311138e4
type: outcome
parents:
  - mvp:environment-indexers-r1
  - verdict:environment-indexers-r1
next_edges:
  - bigger_outcome:environment-indexers-r1
edited_by: season.py
judged_against: goal:g6.1
lens: goal:g6
season: 1
tags:
  - environment-indexers
  - R1
thought_session: season
title: "Outcome: environment-indexers R1"
---
**Outcome:** Indexer invocation command available and working.

**Input:** Target path + indexer name
**Output:** Graph nodes emitted for indexed resources
**Behavior:** Runs only the specified indexer on the specified path
**Edge cases:** Unknown indexer returns structured error, non-zero exit on failure