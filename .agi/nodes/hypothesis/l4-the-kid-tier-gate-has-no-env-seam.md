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
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: the kid-tier gate's record root is not a production env var a kid can point elsewhere
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-kid-tier-gate-has-no-env-seam

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (ix) L4.162's parent measured: `_record_root()` returns `AGI_AGENT_SESSIONS_ROOT` verbatim and the AGI_* strip is a session fixture that runs AFTER `pytest_cmdline_main`, so `env -u AGI_TIER AGI_AGENT_SESSIONS_ROOT=/tmp/empty pytest extensions/agi/tests/` collects 2887 from inside a kid. CLAIM: the fixture root reaches the gate through a pytest plugin option / monkeypatch in tests only; at gate time the record root is derived from the tree (`<worktree>/.agi/sessions` and the shared sessions dir), and `AGI_AGENT_SESSIONS_ROOT` is stripped inside `pytest_cmdline_main` before the tier is derived. TESTS: the L4.162 tests re-pointed through the plugin option; the empty-dir override no longer clears the gate. FALSIFIER: a bare directory run from inside a kid succeeding with any env var set. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py + test_tier_gate.py.

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.176, 2026-09-11 09:59Z). Kept the parent's DEMOTION of both kids to inconclusive_lean_disproved:65 -- measured, not argued: a planted running kid record + `PYTEST_CURRENT_TEST=spoofed::test` + `--agent-records-root=/tmp/empty` collects 2929 (exit 0) while the same command without the flag refuses (exit 4); the guard on the new option is itself an env var, which is the claim's own falsifier. Merged the bytes anyway because they are strictly narrower and never looser: pre-fix `_record_root()` with `AGI_AGENT_SESSIONS_ROOT=/tmp/empty-seam` returned `/tmp/empty-seam`; round bytes return the tree's own `.agi/sessions` (probe from each tree's conftest, 09:59Z); 201 passed with neighbours on the round bytes (test_tier_gate/dispatch/locations), test_tier_gate + test_dispatch green on the merged seat bytes. OPEN: the node stays unproved. Fix-only re-dispatch claim (what is already done: the env read is gone, the var is popped, the option exists): drop the cross-process re-root entirely -- `_record_root()` takes no option and no env; the in-process tests monkeypatch `_default_record_root`; the subprocess falsifier tests plant their record under the REAL tree's sessions dir in a throwaway iter dir and clean it up. Serial with g15-36a (`l4-the-kid-tier-gate-scans-every-root-it-can-reach`) on conftest.py -- one round can carry both once the budget allows.

DIRECTOR 2026-09-11 12:11Z: the test seam this node's half left open was removed by L4.187 (hypothesis:l4-the-record-root-has-no-test-seam-either): no option, no global, no PYTEST_CURRENT_TEST guard; _record_root() is tree-derived only. The experiments here keep their lean_disproved:65 as the honest record of the half.
