---
id: hyp:schema-registry-r6
mint_id: cdec9bd30b024a569642eb18df1bf7a0
type: hypothesis
parents:
  - idea:domain-schema-registry
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - schema-registry
  - R6
testable_claim: Pluggable Language-Model Hook
thought_session: L1.09
title: "schema-registry/R6: Pluggable Language-Model Hook"
---
**Description:** The schema-proposal hook is selected by configuration and degrades gracefully when no model is available.

**Acceptance Criteria:**
- [ ] The hook target is selectable through configuration or environment, not hard-coded
- [ ] When no hook target is configured or reachable, the cascade proceeds to the generic fallback without raising
- [ ] A hook failure (timeout, error response, malformed output) is logged with the offending input and does not abort the load
- [ ] Hook outputs are validated before being written as schema files

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:schema-registry-r6-by-citation` citing `build:src-schema-registry-hooks-protocol`, `build:src-schema-registry-hooks-claude-hook`, `build:src-schema-registry-hooks-ollama-hook`, `build:src-schema-registry-hooks-none-hook`, `build:tests-schema-registry-test-hooks`: `hooks/protocol.py` plus three real backends (`claude_hook`, `ollama_hook`, `none_hook`) -- an exact match for a pluggable LM hook with graceful degradation.
<!-- THOUGHT:END -->
