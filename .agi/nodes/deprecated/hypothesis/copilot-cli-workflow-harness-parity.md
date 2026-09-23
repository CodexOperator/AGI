---
id: hypothesis:copilot-cli-workflow-harness-parity
mint_id: b2d85ecbebe34484b15d13412d830b15
type: hypothesis
parents:
  - goal:g25.legacy-direct
next_edges: []
confidence: 0.9
edited_by: belam
season: 2
status: deprecated
testable_claim: "The copilot-cli harness is declared and resolved through config: adapters.load validates its adapter contract, needs_credential is false for GitHub-authenticated children, model_listing and transcript_path expose adapter-owned diagnostics, and workflow.py --harness accepts only declared harness names while resolving models from the selected harness namespace; proven by the focused adapter/workflow test suite and dry-run output."
thought_session: goal-glom-2026-09-19
title: Copilot cli workflow harness parity
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:copilot-cli-workflow-harness-parity

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director-built slice from the owner 14:5xZ re-seating order. The implementation is intentionally limited to Copilot CLI adapter/config parity and workflow harness validation, avoiding the in-flight rotation/meter/cwd/trust/models work. Evidence: 81 focused adapter and workflow tests passed, plus a Copilot workflow dry-run and undeclared-harness refusal.
<!-- THOUGHT:END -->

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): FIXED in season2/main's bytes -- All claim conjuncts are in season2/main bytes and named by commits; residue: model_listing/transcript_path are dead seams (MEASURED: grep across extensions/agi/bin + tests finds zero callers and zero tests; copilot_cli_adapter.py defines neither list_models nor transcript_path, so both fall back to config models / output.log) and _resolve_harness_model + the "invalid harness override" refusal have no test (MEASURED: grep in extensions/agi/tests/ = 0 hits). EVIDENCE: MEASURED: 2fc62f55f (workflow.py +42, adapters/__init__.py +33, config.json, adapter), f4b44c2de (adapter retained), 626314757 (node), 317b27663 = real merge commit, parents 9d9505bcf + f4b44c2de, all four `git merge-base --is-ancestor` HEAD; adapters/__init__.py:36 REQUIRED, :68-74 load check, :113-116 resolve refuses undeclared, :270 model_listing, :289 transcript_path; copilot_cli_adapter.py:386-389 needs_credential False (tested test_copilot_cli_adapter.py:117-121); workflow.py:1601-1606 adapters.resolve on --harness, :841-858 _resolve_harness_model, :1622-1625 non-pi models from harness_c Kept active as the record of a closed defect; no round.

Retired at the L4 closeout (Prime retire list 2026-09-17 12:0xZ from survey hypothesis:a00-e1933e6a-176c0e, executed by sanctuary-master gen 7, status deprecated + moved under deprecated/hypothesis, mint id unchanged): closed by landed bytes (adapter/config parity, tests passed).
