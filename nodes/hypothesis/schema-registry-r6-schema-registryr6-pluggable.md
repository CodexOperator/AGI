---
confidence: 0.5
id: "hyp:schema-registry-r6"
mint_id: cdec9bd30b024a569642eb18df1bf7a0
origin: build-site
parents:
  - idea:domain-schema-registry
subgraph: false
tags:
  - schema-registry
  - R6
testable_claim: Pluggable Language-Model Hook
title: "schema-registry/R6: Pluggable Language-Model Hook"
type: hypothesis
---

**Description:** The schema-proposal hook is selected by configuration and degrades gracefully when no model is available.

**Acceptance Criteria:**
- [ ] The hook target is selectable through configuration or environment, not hard-coded
- [ ] When no hook target is configured or reachable, the cascade proceeds to the generic fallback without raising
- [ ] A hook failure (timeout, error response, malformed output) is logged with the offending input and does not abort the load
- [ ] Hook outputs are validated before being written as schema files
