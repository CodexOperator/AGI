---
id: hypothesis:loader-resolves-mint-ids-in-one-post-pass
mint_id: a76897d6f6684a45b2f5f1a66ac5f7fd
type: hypothesis
parents:
  - goal:g4.18.6.3.1
next_edges: []
confidence: 0.75
edited_by: director-general-1
scaffold_hash: 614b43542af74abd
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: one post-pass in graph_core load_directory (loader.py:210-230) resolves every PARENTS item through the one resolver passed in by the caller, so every family-A reader prints a mint-id twin identically
title: "graph_core's loader resolves parents and next_edges in one post-pass (row W2c family A; assigned: director-general-3)"
town: core
---
# hypothesis:loader-resolves-mint-ids-in-one-post-pass

## Measured
- verdict:dg2b4-w2c: 0/17 readers resolve. Re-scope stage 2 (75218add6, lean disproved 60): graph_core's Node has no next_edges field (next_edges -> family B); the post-pass site is load_directory (loader.py:210-230), not :90; graph_core imports nothing from bin, so the resolver is passed in.

## CLAIM
(1) one post-pass in load_directory, parents only (2) the resolver is a parameter, graph_core imports nothing from bin (3) family-A twins identical (4) no family-A reader resolves itself.

## Dispatch line
config-max: none. template-max: none. code: one pass in the loader.

## FALSIFIERS
- a family-A twin prints differently
- a family-A reader resolves ids itself

## TESTS
test_viewport.py (test_w2c) ONE file, `--basetemp /tmp/b4w2ca` · the twin probe over family A

## FILE SCOPE
extensions/agi/bin/graph_core/loader.py (load_directory) + its callers passing the resolver · test_viewport.py

## CEILING
no dispatch · <= 30 production lines · <= 30 test lines · 0 USD
