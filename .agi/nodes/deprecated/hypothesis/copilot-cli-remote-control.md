---
id: hypothesis:copilot-cli-remote-control
mint_id: 8115df994dce4feaba519881f3293618
type: hypothesis
parents:
  - goal:g25.legacy-direct
next_edges: []
confidence: 0.9
edited_by: belam
scaffold_hash: f7948c3ba8ccdfab
season: 2
status: deprecated
testable_claim: The copilot-cli adapter build command emits --remote on every unified-route spawn path, with the exact argv order copilot --model M --effort E --allow-all --remote -i ..., proven by adapter, dispatch dry-run, rotate dry-run fixtures, and focused tests.
thought_session: goal-glom-2026-09-19
title: Copilot CLI posts expose remote control
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:copilot-cli-remote-control

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Added only the owner-ordered --remote flag at the shared Copilot adapter command seam and rotate.py seat command seam. The adapter produces --allow-all --remote before -p; rotation produces --allow-all --remote before -i. Evidence: 306 focused adapter/rotation tests passed and dispatch --dry-run emitted copilot --model auto --allow-all --remote -p.
<!-- THOUGHT:END -->

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): FIXED in season2/main's bytes -- --remote is emitted immediately after --allow-all on every copilot argv builder in the tree: adapter build_command (dispatch/workflow/adapter restart, which calls build_command) and rotate.py _build_copilot_command (the only copilot branch of _build_harness_command); tests assert the order. EVIDENCE: MEASURED: d401232a7 (node + adapter +4 + rotate.py +19 + 2 tests), a7734ecfb merge parents 65e3fc3da + d401232a7, both ancestors of HEAD; copilot_cli_adapter.py:273 --allow-all, :275 --remote, :279 -p last; :353 restart args = build_command(...); rotate.py:924-925 --allow-all/--remote before :927 -i, :942-945 _build_harness_command routes copilot-cli only to _build_copilot_command; grep '"copilot"' outside the adapter = only rotate.py:919; tests test_copilot_cli_adapter.py:132, test_rotate_copilot_harness.py:52, :129-130; owner order .agi/nodes/doc/l4-owner-decisions.md:797 Kept active as the record of a closed defect; no round.

Retired at the L4 closeout (Prime retire list 2026-09-17 12:0xZ from survey hypothesis:a00-e1933e6a-176c0e, executed by sanctuary-master gen 7, status deprecated + moved under deprecated/hypothesis, mint id unchanged): closed by landed bytes (the --remote emissions).
