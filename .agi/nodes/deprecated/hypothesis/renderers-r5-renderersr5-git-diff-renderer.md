---
id: hyp:renderers-r5
mint_id: 57ebda5a4768406c862274666d23b32a
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
  - R5
testable_claim: Git-Diff Renderer
thought_session: L1.09
title: "renderers/R5: Git-Diff Renderer"
---
**Description:** A renderer produces a diff view between two experiment runs along the same chain so progression and regression are visible side by side.

**Acceptance Criteria:**
- [ ] The renderer accepts exactly two run identifiers belonging to the same chain and rejects mismatched pairs with a structured error
- [ ] Added, removed, and changed fields appear with conventional diff markers
- [ ] When two runs are identical, the output is an empty diff with a one-line note rather than a blank string
- [ ] The output uses only printable ASCII characters

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:renderers-r5-by-citation` citing `build:src-renderers-git-diff`, `build:tests-renderers-test-git-diff`: `git_diff.py` is the two-run diff renderer with an empty-diff note and `test_git_diff.py` its suite.
<!-- THOUGHT:END -->
