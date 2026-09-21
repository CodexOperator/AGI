---
id: hypothesis:l2-dispatch-restart-twin-node
mint_id: a7f0850d1dbc4c2b914f6dd735b7f384
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: 47dcee2e73594fc5
season: 1
testable_claim: When a kid pi process dies mid-run, heal.py/dispatch.py's restart reuses the original scaffolded node id instead of minting a second node for the same agent slot, and cli.py done persists evidence_runs into frontmatter so self-cited evidence survives the grid-commit gate
title: L2 dispatch restart twin node
---
# hypothesis:l2-dispatch-restart-twin-node

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED L2.12 (parent a00-403a3639, target hypothesis:l2w6-telemetry-rollup): kid a00-6856367d died mid-run (pid 1316280, ~08:25); the reaper restarted it and heal.py/dispatch.py scaffolded a SECOND node for the same agent slot (experiment:a00-6856367d-7b307d, the original, vs experiment:a00-6856367d-telemetry-rollup, the restart's twin). The restarted kid filled both files and done-signaled the twin; the twin's self-cited evidence_runs resolved to 0 at the grid-commit gate (evidence not yet in frontmatter when cited) and was demoted proved->inconclusive_lean_proved:50, while the canonical original (linked from the hypothesis's next_edges) had no verdict until the reviewing parent wrote one by hand. FIX A: on restart, the scaffold/resume path reuses the original agent's already-scaffolded node id (from the manifest) instead of calling scaffold again -- find where heal.py or dispatch.py's restart path calls cli.py scaffold and gate it on manifest already having a node for that agent_id. FIX B (belt and suspenders, independent of A): cli.py done should persist evidence_runs into the node's own frontmatter at signal time, not only pass it to the gate in-memory, so a node citing itself as evidence survives a later grid-commit re-check. VERIFY: red-first test simulating a kid restart (kill mid-scaffold, invoke the restart path twice) asserting exactly one experiment node is scaffolded for the agent; a second test asserts a done --evidence-runs <self> node's frontmatter contains evidence_runs after write and after grid commit. Source note: .agi/autoresearch.ideas.md line 1 (delete that file once this hypothesis captures it -- it duplicates this note and should not accumulate as a second untracked ideas log). Suite green via commands.py run tests.
