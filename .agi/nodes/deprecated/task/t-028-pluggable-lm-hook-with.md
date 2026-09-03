---
id: task:t-028
mint_id: 2f3d4c645d004691af440da150f374c2
type: task
parents:
  - hyp:schema-registry-r6
acceptance_criteria:
  - R6.1 (hook target selectable via config/env
  - not hard-coded)
  - R6.2 (no target/unreachable → cascade proceeds to generic without raising)
  - R6.3 (hook failure logged with offending input; does not abort load)
  - R6.4 (hook outputs validated before written)
blocked_by:
  - task:t-021
cavekit_req: schema-registry/R6
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-028: Pluggable LM hook with graceful degradation"
---
**Description:** Implement `LanguageModelHook` Protocol with `propose_schema(samples)` returning a candidate dict. Implementations chosen via `context/config/schema-registry.toml` `hook=` value (claude/ollama/none). Wrap calls in `try/except` with structured logging and a strict YAML schema validator on outputs.

**Files:** `agi-tree/src/schema_registry/hooks/protocol.py`, `agi-tree/src/schema_registry/hooks/claude.py`, `agi-tree/src/schema_registry/hooks/none.py`, `agi-tree/tests/schema_registry/test_hooks.py`

**Test Strategy:** Unit tests injecting (a) None hook → cascade reaches generic, (b) failing hook → error logged, load continues, (c) malformed output → rejected by validator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `schema-registry/R6` under `hyp:schema-registry-r6`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r6-by-citation` citing `build:src-schema-registry-hooks-protocol`, `build:src-schema-registry-hooks-claude-hook`, `build:src-schema-registry-hooks-ollama-hook`, `build:src-schema-registry-hooks-none-hook`, `build:tests-schema-registry-test-hooks`: `hooks/protocol.py` plus three real backends (`claude_hook`, `ollama_hook`, `none_hook`) -- an exact match for a pluggable LM hook with graceful degradation.
<!-- THOUGHT:END -->
