---
id: hyp:autoresearch-tree-skill-r7
mint_id: e7e1705e912f44bd958e9ed4397cd8d0
type: hypothesis
parents:
  - idea:domain-autoresearch-tree-skill
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - autoresearch-tree-skill
  - R7
testable_claim: Driver Script
thought_session: L1.09
title: "autoresearch-tree-skill/R7: Driver Script"
---
**Description:** A driver script orchestrates one or more loop iterations analogously to the predecessor project's driver.

**Acceptance Criteria:**
- [ ] A single command starts the driver and runs at least one full iteration end-to-end
- [ ] The driver exits with a non-zero status when any iteration fails to record metrics
- [ ] The driver writes a per-iteration summary to a documented location inside the project context directory
- [ ] The driver respects the configuration file's parameters without code changes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:autoresearch-tree-skill-r7-by-citation` citing `build:driver.sh`: `driver.sh` is the single-command end-to-end driver.
<!-- THOUGHT:END -->
