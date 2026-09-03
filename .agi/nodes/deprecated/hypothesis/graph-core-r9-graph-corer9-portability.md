---
id: hyp:graph-core-r9
mint_id: 2ca2807126e14fe6a5f208048e113f94
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - graph-core
  - R9
testable_claim: Portability Contract
thought_session: L1.09
title: "graph-core/R9: Portability Contract"
---
**Description:** All graph state lives inside a single project-local context directory. The graph is movable by copying that directory.

**Acceptance Criteria:**
- [ ] No node file, cache file, or configuration file references an absolute path outside the project root
- [ ] Copying the context directory to a fresh checkout reproduces the same graph on load
- [ ] The graph loads with no environment variables set beyond an optional model selector for downstream hooks
- [ ] A self-test command verifies portability by re-loading from a temporary copy and comparing node counts and ids

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-SMALL-EXPERIMENT, not run: no dedicated portability self-test exists (no `test_portability.py`); the small experiment is an absolute-path audit plus copying `.agi/` to a tempdir and reloading it through the real loader -- hours, not architecture.
<!-- THOUGHT:END -->
