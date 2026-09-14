---
id: hypothesis:workflow-stage-context-write-surface
mint_id: b79c4a308dbf482a982e72c2a56e7c1a
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: c848f4e7b0186d41
season: 2
testable_claim: Every workflow stage on either pi or copilot-cli receives its assembled context through viewport --emit llm or brief.py, persists node or report changes only through write.py, and workflow.py list exposes the resolved harness for every registered row; focused tests and dry-run/list output prove the route without stage-specific hand edits.
thought_session: sensei-director
title: Workflow stages use unified view and write surfaces
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:workflow-stage-context-write-surface

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Live workflow stages now prepend the same graph context surfaces used by the engine: viewport.py --emit llm and brief.py head for the stage role. The prompt also carries the write.py-only route contract; read-only manifests remain read-only. Evidence: focused adapter/workflow suite 113 passed, including harness-aware workflow list coverage.
<!-- THOUGHT:END -->
