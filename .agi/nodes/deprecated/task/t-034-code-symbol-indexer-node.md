---
id: task:t-034
mint_id: b286a306305648b7a44a830bf9cf84f3
type: task
parents:
  - hyp:environment-indexers-r3
acceptance_criteria:
  - R3.1 (emits at minimum function
  - class
  - method
  - module nodes for supported language)
blocked_by:
  - task:t-032
  - task:t-031
cavekit_req: environment-indexers/R3
edited_by: season.py
effort: L
origin: build-site
season: 1
status: deprecated
tags:
  - L
  - tier--1
thought_session: season
tier: -1
title: "T-034: Code symbol indexer — node emission for functions/classes/methods/modules"
---
**Description:** Python-first AST-based parser (use stdlib `ast`). Emits `module`, `class`, `function`, `method` node types. Inspired by `agi/graph_builder.py` lru_cache pattern but re-implemented under schema-registry contracts. Documented as Python-only for v1.

**Files:** `agi-tree/src/environment_indexers/code_symbols.py`, `agi-tree/src/environment_indexers/schemas/[module].md`, `[class].md`, `[function].md`, `[method].md`, `agi-tree/tests/environment_indexers/test_code_symbols_emit.py`

**Test Strategy:** Index a fixture Python project with one of each symbol type; assert all four are present in the output graph.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `environment-indexers/R3` under `hyp:environment-indexers-r3`, whose disposition is disposition GENUINELY-OPEN, not run: no `environment_indexers` package exists anywhere under `extensions/agi/` and the domain's own R1 closure is hollow (§F R1: `verdict:environment-indexers-r1` is self-asserted, `evidence_runs: []`, demoted from proved), so this is open by elimination; the domain is the one that did not survive `goal:g11` -- an index-arbitrary-environments library has no customer inside a single-repo `agi` -- and no goal is minted for it.
<!-- THOUGHT:END -->