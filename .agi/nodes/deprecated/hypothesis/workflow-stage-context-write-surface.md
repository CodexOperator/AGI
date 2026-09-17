---
id: hypothesis:workflow-stage-context-write-surface
mint_id: b79c4a308dbf482a982e72c2a56e7c1a
type: hypothesis
parents:
  - goal:g15
next_edges: []
confidence: 0.9
edited_by: sanctuary-master
scaffold_hash: c848f4e7b0186d41
season: 2
status: deprecated
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

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): FIXED in season2/main's bytes -- Context/write surface is in the bytes and minted+merged; the copilot-cli half of "either pi or copilot-cli" cannot be exercised because non-pi harnesses only resolve+describe, and that is the live claim of sibling hypothesis:workflow-stages-dispatch-as-kids (MEASURED: .agi/nodes/hypothesis/workflow-stages-dispatch-as-kids.md exists, live). _stage_context takes no harness argument, so it applies unchanged once the sibling lands. EVIDENCE: MEASURED: dd42ec8be (node + workflow.py +53 + test_workflow.py +33), 0a3ee2791 merge commit parents be781300b + dd42ec8be, both ancestors of HEAD; workflow.py:1273 _stage_context, :1285-1289 viewport --emit llm --depth 3, :1294-1297 brief.py head --tier, :1303-1309 write.py-only route contract, :1693 sole caller (pi path), :1638-1648 non-pi resolve+describe only, :474-513 list_workflows HARNESS/LEVEL column via _resolve_default_harness (:507); tests test_workflow.py:261 test_stage_context_uses_shared_viewport_and_brief_surfaces, :281 asserts write.py Kept active as the record of a closed defect; no round.

Retired at the L4 closeout (Prime retire list 2026-09-17 12:0xZ from survey hypothesis:a00-e1933e6a-176c0e, executed by sanctuary-master gen 7, status deprecated + moved under deprecated/hypothesis, mint id unchanged): closed by landed bytes (unified context/write surface).
