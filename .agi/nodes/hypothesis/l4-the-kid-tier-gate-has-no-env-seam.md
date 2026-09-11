---
id: hypothesis:l4-the-kid-tier-gate-has-no-env-seam
mint_id: 124b93c134cf4c5db03adfc66eca35fa
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-kid-tier-gate-is-not-clearable-from-inside-a-kid
next_edges: []
edited_by: sanctuary-director
scaffold_hash: a934d1788903a78c
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (ix) L4.162's parent measured: `_record_root()` returns `AGI_AGENT_SESSIONS_ROOT` verbatim and the AGI_* strip is a session fixture that runs AFTER `pytest_cmdline_main`, so `env -u AGI_TIER AGI_AGENT_SESSIONS_ROOT=/tmp/empty pytest extensions/agi/tests/` collects 2887 from inside a kid. CLAIM: the fixture root reaches the gate through a pytest plugin option / monkeypatch in tests only; at gate time the record root is derived from the tree (`<worktree>/.agi/sessions` and the shared sessions dir), and `AGI_AGENT_SESSIONS_ROOT` is stripped inside `pytest_cmdline_main` before the tier is derived. TESTS: the L4.162 tests re-pointed through the plugin option; the empty-dir override no longer clears the gate. FALSIFIER: a bare directory run from inside a kid succeeding with any env var set. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py + test_tier_gate.py."
thought_session: sanctuary-director-gen12
title: the kid-tier gate's record root is not a production env var a kid can point elsewhere
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-kid-tier-gate-has-no-env-seam

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (ix) L4.162's parent measured: `_record_root()` returns `AGI_AGENT_SESSIONS_ROOT` verbatim and the AGI_* strip is a session fixture that runs AFTER `pytest_cmdline_main`, so `env -u AGI_TIER AGI_AGENT_SESSIONS_ROOT=/tmp/empty pytest extensions/agi/tests/` collects 2887 from inside a kid. CLAIM: the fixture root reaches the gate through a pytest plugin option / monkeypatch in tests only; at gate time the record root is derived from the tree (`<worktree>/.agi/sessions` and the shared sessions dir), and `AGI_AGENT_SESSIONS_ROOT` is stripped inside `pytest_cmdline_main` before the tier is derived. TESTS: the L4.162 tests re-pointed through the plugin option; the empty-dir override no longer clears the gate. FALSIFIER: a bare directory run from inside a kid succeeding with any env var set. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py + test_tier_gate.py.
