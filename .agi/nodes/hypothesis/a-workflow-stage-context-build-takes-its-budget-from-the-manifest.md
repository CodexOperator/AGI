---
id: hypothesis:a-workflow-stage-context-build-takes-its-budget-from-the-manifest
mint_id: d6705ee0f25d4a5bb59285676a9438c5
type: hypothesis
parents:
  - goal:g15.29.10
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: c81222ee47406a75
season: 2
testable_claim: "After the fix, workflow.py's stage context build (_stage_context ~1523: viewport.py --emit llm and brief.py head, each a hard timeout=60 subprocess at ~1541/~1550) takes its budget from the workflow manifest -- a `context_timeout_s` resolved stage > manifest > the current 60 s default, with the same presence semantics and refusal of a bad value before any stage runs as timeout_s (~1992-2017) -- and merge-up-review.json declares a budget that survives the measured box load; proved by committed tests (a slow fake viewport under a monkeypatched subprocess.run honours the manifest budget, red on the pre-fix bytes; a bad value refuses by name; a manifest declaring none keeps 60), test_workflow*.py green."
title: "A workflow stage's context build takes its budget from the manifest (assigned: director-engine)"
town: core
---
# hypothesis:a-workflow-stage-context-build-takes-its-budget-from-the-manifest

# hypothesis:a-workflow-stage-context-build-takes-its-budget-from-the-manifest

## Hypothesis

After the fix, workflow.py's stage context build (_stage_context ~1523: viewport.py --emit llm and brief.py head, each a hard timeout=60 subprocess at ~1541/~1550) takes its budget from the workflow manifest -- a `context_timeout_s` resolved stage > manifest > the current 60 s default, with the same presence semantics and refusal of a bad value before any stage runs as timeout_s (~1992-2017) -- and merge-up-review.json declares a budget that survives the measured box load; proved by committed tests (a slow fake viewport under a monkeypatched subprocess.run honours the manifest budget, red on the pre-fix bytes; a bad value refuses by name; a manifest declaring none keeps 60), test_workflow*.py green.

## Agent Notes
assigned: director-engine (leaf goal:g15.29.10; measured 09-23 19:0xZ: director-engine's mur L lost both verifies and thought-master's run -4 lost both verifies to 'context-build-timeout after 60 s' at box load 40-51; the range suite's test_pi_bare_json_stage_is_ok failed the same way at load 30+ and passed at load 8).
