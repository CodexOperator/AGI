---
id: hypothesis:copilot-cli-workflow-harness-parity
mint_id: b2d85ecbebe34484b15d13412d830b15
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 16b0892489b83dc6
season: 2
testable_claim: "The copilot-cli harness is declared and resolved through config: adapters.load validates its adapter contract, needs_credential is false for GitHub-authenticated children, model_listing and transcript_path expose adapter-owned diagnostics, and workflow.py --harness accepts only declared harness names while resolving models from the selected harness namespace; proven by the focused adapter/workflow test suite and dry-run output."
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
