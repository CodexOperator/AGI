---
id: hypothesis:workflow-stages-dispatch-as-kids
mint_id: 349ea19efd4a4e87bd74d087d2034b64
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 11e822cb4011291f
season: 2
testable_claim: workflow.py pi and copilot-cli stages execute through dispatch.py child spawns, each with a spawn_budget lease, provisioning credential, session directory under .agi/sessions/iter-<run_key>/, manifest timeout_s, and completion events feeding the shared RunView; fixtures prove one lease and one completion record per stage without minting during tests, and a real merge-up-review copilot-cli dry/live path is observable without a raw pi subprocess.
title: Workflow stages dispatch as kids
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:workflow-stages-dispatch-as-kids

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Not landed: workflow.py:7 docstring still promises "dispatch.py kid per stage on the pi harness" while _run_stage_pi (def :1413) runs `cmd = [hc["bin"], "-p", "--provider", ...]` through `subprocess.run` at workflow.py:1464; non-pi branch at :1639-1649 only resolves-and-describes then `return 0`; MEASURED `grep -c spawn_budget workflow.py` = 0. EVIDENCE: workflow.py:7, :1413, :1448-1467, :1639-1649 Never rounded at close (owner 14:1xZ).
