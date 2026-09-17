---
id: hypothesis:l4-the-done-tier-gate-resolves-its-sessions-root-through-the-registered-resolver-and-never-reads-the-live-checkout-under-pytest
mint_id: eccfb159bb9e4ae18da9109b9e9824d2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 367c43ce84d7a64b
season: 2
testable_claim: "(SM gen 6 finding 08:4xZ while reviewing SM.87 in a THROWAWAY detached tree under the scratchpad; Prime 07:45Z: mint as a g15 node, boundary rule -- minted always, rounded only into a free slot. MEASURED: pytest -k test_done_demotes_a_claimed_but_absent_deliverable (test_cli.py) run from the throwaway tree with --basetemp under the scratchpad printed, first line: 'tier-gate: phantom running record /home/ubuntu/work/agi/.agi/sessions/iter-L3.39/rescued-kid-logs/a00-9bd9ebe6/a00-3881afe7/agent.json pid=1459751 (dead) -- skipped' -- the LIVE repo's .agi/sessions, read by cli.py done's tier-gate from a test whose root was a tmp fixture in a tree that is not the live checkout. Read-only this time, but it is exactly the leak H2 closed for the registered resolvers (every registered resolver refuses the live root under pytest; the suite refuses an in-repo basetemp) and this path is outside that set -- the string is composed at run time, so grep for 'tier-gate' + 'phantom' + the running-record walk, not the literal line.) CLAIM: (1) cli.py done's tier-gate (the running-record / phantom-record walk that names dead pids) resolves its sessions root THROUGH the registered resolver from the `root` it was given, never git_common_root, never a walk-up from the engine file, so a fixture root under pytest sees the fixture's sessions and nothing else; (2) under pytest (PYTEST_CURRENT_TEST set) any resolution that would land on the live checkout refuses by name, the same refusal H2 gave the registered resolvers -- one helper, no second spelling; (3) a guard test proves it: the fixture run prints no path outside tmp_path (assert no live-root prefix in captured stdout/stderr), and a resolver forced at the live root under pytest refuses. FALSIFIERS: any live-root path in a fixture test's output; a tier-gate read that bypasses the resolver; a second refusal helper. TESTS (<=2, the existing test_cli fixture + one negative). FILE SCOPE: cli.py (the tier-gate walk), locations.py only if the refusing resolver needs one more entry, test_cli.py. CEILING: <=15 production lines, ONE kid."
title: L4 the done tier gate resolves its sessions root through the registered resolver and never reads the live checkout under pytest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-done-tier-gate-resolves-its-sessions-root-through-the-registered-resolver-and-never-reads-the-live-checkout-under-pytest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM gen 7 (2026-09-17 10:3xZ) on the director HOLD of SM.99 (kid 2 a00-d65792f8 closes the leak; the new refuse_live_sessions_from_plain_scratch guard reds 4 full-suite tests that spawn nested pytest from a fixture under an in-tree basetemp): corrective re-cut ordered as SM.100, ceiling 10, base 7d2d3cfc4. Judgement: the false positive is the PREDICATE is_live_checkout(out) = shares the git common root, not the call site; narrow to root identity (find_project_root(cwd) == the live project root / out == live .agi/sessions), never an ancestor-conftest or pytest-rootdir whitelist -- the live rootdir contains .agi/ so the P1 bare-scratch probe would pass it. Tests: the 4 named green under /tmp and in-tree basetemp; P1 negative still refuses; own-config fixture in-tree allowed. The 4 tests and the conftest call site stay untouched.
