---
id: hyp:renderers-r7
mint_id: ebbe1f1f33ef451c868a9be4154936d1
type: hypothesis
parents:
  - idea:domain-renderers
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - renderers
  - R7
testable_claim: Renderer Plugin Contract
thought_session: L1.09
title: "renderers/R7: Renderer Plugin Contract"
---
**Description:** Adding a new renderer is one new class that implements a single method taking the shared representation and returning a string.

**Acceptance Criteria:**
- [ ] The renderer interface declares exactly one required method that accepts the shared representation and returns a string
- [ ] A new renderer implementation is loadable without modifying existing renderers
- [ ] An invalid renderer (raises during render or returns a non-string) is reported with a structured error and does not affect other renderers
- [ ] A self-test command runs every registered renderer over a fixture graph and reports pass or fail per renderer

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `plugin.py`/`registry.py`; the real renderers are called directly by `zoom.py`/`stitch.py`, which is plausibly intentional -- a plugin contract was part of the abandoned reusable-package framing (§D) -- so no goal is minted and this THOUGHT is the record.
<!-- THOUGHT:END -->
