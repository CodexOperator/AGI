---
acceptance_criteria:
  - R3.1 (emits at minimum function
  - class
  - method
  - module nodes for supported language)
blocked_by:
  - task:t-032
  - task:t-031
cavekit_req: environment-indexers/R3
effort: L
id: "task:t-034"
mint_id: b286a306305648b7a44a830bf9cf84f3
origin: build-site
parents:
  - hyp:environment-indexers-r3
status: pending
tags:
  - L
  - tier--1
tier: -1
title: "T-034: Code symbol indexer — node emission for functions/classes/methods/modules"
type: task
---

**Description:** Python-first AST-based parser (use stdlib `ast`). Emits `module`, `class`, `function`, `method` node types. Inspired by `agi/graph_builder.py` lru_cache pattern but re-implemented under schema-registry contracts. Documented as Python-only for v1.

**Files:** `agi-tree/src/environment_indexers/code_symbols.py`, `agi-tree/src/environment_indexers/schemas/[module].md`, `[class].md`, `[function].md`, `[method].md`, `agi-tree/tests/environment_indexers/test_code_symbols_emit.py`

**Test Strategy:** Index a fixture Python project with one of each symbol type; assert all four are present in the output graph.
