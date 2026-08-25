---
acceptance_criteria:
  - R6.1 (hook target selectable via config/env
  - not hard-coded)
  - R6.2 (no target/unreachable → cascade proceeds to generic without raising)
  - R6.3 (hook failure logged with offending input; does not abort load)
  - R6.4 (hook outputs validated before written)
blocked_by:
  - task:t-021
cavekit_req: schema-registry/R6
effort: M
id: "task:t-028"
mint_id: 2f3d4c645d004691af440da150f374c2
origin: build-site
parents:
  - hyp:schema-registry-r6
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-028: Pluggable LM hook with graceful degradation"
type: task
---

**Description:** Implement `LanguageModelHook` Protocol with `propose_schema(samples)` returning a candidate dict. Implementations chosen via `context/config/schema-registry.toml` `hook=` value (claude/ollama/none). Wrap calls in `try/except` with structured logging and a strict YAML schema validator on outputs.

**Files:** `agi-tree/src/schema_registry/hooks/protocol.py`, `agi-tree/src/schema_registry/hooks/claude.py`, `agi-tree/src/schema_registry/hooks/none.py`, `agi-tree/tests/schema_registry/test_hooks.py`

**Test Strategy:** Unit tests injecting (a) None hook → cascade reaches generic, (b) failing hook → error logged, load continues, (c) malformed output → rejected by validator.
