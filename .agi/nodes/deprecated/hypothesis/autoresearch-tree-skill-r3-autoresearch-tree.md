---
id: hyp:autoresearch-tree-skill-r3
mint_id: 5f7a4fa4354a46609cb192129280f9df
type: hypothesis
parents:
  - idea:domain-autoresearch-tree-skill
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - autoresearch-tree-skill
  - R3
testable_claim: Parallel Claude Builder Dispatch
thought_session: season
title: "autoresearch-tree-skill/R3: Parallel Claude Builder Dispatch"
---
**Description:** Each iteration dispatches up to five builder agents in parallel using a Claude-class model. Equivalent Ollama dispatch is explicitly deferred.

**Acceptance Criteria:**
- [ ] An iteration dispatches at most five builder agents in parallel
- [ ] When fewer candidates are eligible than the maximum, the iteration runs only that many agents
- [ ] The kit explicitly documents that Ollama-based dispatch is a v2 scope item and is not required here
- [ ] Failure of one agent does not abort the others; partial results are collected and reported

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r3-by-citation` citing `build:bin-dispatch`: `dispatch.py` is real parallel dispatch with a configurable concurrency cap (`spawn_budget.max_live`, `adapters.parallelism`) and restart/reaper handling for partial failure -- adapted (configurable, not a hardcoded 5) but the intent holds.
<!-- THOUGHT:END -->