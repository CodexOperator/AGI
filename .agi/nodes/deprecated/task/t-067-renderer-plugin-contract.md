---
id: task:t-067
mint_id: c708abb7508a4c6e8bdc487a5cf7c015
type: task
parents:
  - hyp:renderers-r7
acceptance_criteria:
  - R7.1 (interface declares exactly one required method accepting shared representation
  - returning string)
  - R7.2 (new renderer implementation loadable without modifying existing renderers)
  - R7.3 (invalid renderer reported with structured error
  - does not affect others)
blocked_by:
  - task:t-061
  - task:t-063
  - task:t-064
  - task:t-065
cavekit_req: renderers/R7
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-067: Renderer plugin contract"
---
**Description:** Define `RendererPlugin` Protocol with `render(rep) -> str`. Implement `RendererRegistry.register(plugin)` and `agi-tree self-test renderers` command. Wrap each render call in try/except → structured `RendererError(name, exc)`.

**Files:** `agi-tree/src/renderers/plugin.py`, `agi-tree/src/renderers/registry.py`, `agi-tree/src/renderers/cli.py`, `agi-tree/tests/renderers/test_plugin.py`

**Test Strategy:** Drop a stub renderer in; self-test reports pass. Make it raise; self-test reports fail with the offender name.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `renderers/R7` under `hyp:renderers-r7`, whose disposition is disposition GENUINELY-OPEN, not run: no `plugin.py`/`registry.py`; the real renderers are called directly by `zoom.py`/`stitch.py`, which is plausibly intentional -- a plugin contract was part of the abandoned reusable-package framing (§D) -- so no goal is minted and this THOUGHT is the record.
<!-- THOUGHT:END -->
