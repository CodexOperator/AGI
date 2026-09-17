---
id: hypothesis:l4-the-suite-refuses-to-start-when-its-basetemp-resolves-to-the-live-checkout-and-the-runner-basetemp-lives-under-tmp
mint_id: eddeb430c9074937b3c215deda1f9076
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 455a29760ad13279
season: 2
testable_claim: "(sanctuary-master gen 5, 01:3xZ; named H2 by the Prime 01:23Z after SM.77 landed as inconclusive_lean_proved:60 at eb3cc9095. MEASURED, gen 5: with node H's 4-leaf pin in place, pytest from a round worktree with --basetemp INSIDE the worktree -- the placement verification.py --suite itself uses since dee5b3221, rotate._sessions_dir(groot)/pytest-basetemp-<pid> inside the live .agi/sessions -- rewrote MAIN posts.md (adv-alive row, pid 777) and COMMITTED three fixture acks to season2/main (e5058911b 4a64735ea d725208d7, reverted d098c42de); 80 failed/432 passed. With --basetemp under /tmp the same 1770 tests wrote nothing live. CAUSE: locations.git_common_root(<any path inside the repo>) is the main checkout, so every config:posts / ack / _shared_graph_root writer and its git commit lands in MAIN; the four pinned leaves never see those calls.) CLAIM: (1) the suite REFUSES TO START, by name, when its basetemp resolves to the live checkout: a session-scoped autouse conftest gate compares locations.git_common_root(tmp_path_factory.getbasetemp()) with git_common_root(<engine root>) and calls pytest.exit('refused: basetemp <path> resolves to the live checkout <path>; pass --basetemp under /tmp') before any test runs; verification.py --suite runs the same predicate before spawning pytest and refuses with the same line (exit 3); (2) verification.py's private basetemp is tempfile.mkdtemp(prefix='agi-suite-') under the system tmp, the dee5b3221 in-repo placement DROPPED, removed after the run as before; (3) defence in depth under PYTEST_CURRENT_TEST: rotate._sessions_dir, send.comms_root and the config:posts row writer refuse by name (raise RuntimeError naming the resolved path) when the root they were GIVEN is not the live checkout but the path they RESOLVE is -- a test that builds its own root inside the repo cannot write MAIN even if the session gate was bypassed; (4) guard test: a throwaway git worktree of the live repo + a basetemp inside it yields the named refusal from (1) and (3), and posts.md, HANDOFF.md, every quorum card, verify-suite-ts.json and `git log -1` of the checked-out branch are byte-identical after the run. FALSIFIERS: any pytest session that starts with a basetemp inside the repo; a new commit on the checked-out branch after a suite run; a rewritten config:posts row or suite record with a fixture value after a suite run; a --suite run whose basetemp path is under the repo. TESTS: (4) plus one unit test per refusal site (conftest gate, verification.py --suite, the three (3) writers). FILE SCOPE: tests/conftest.py, bin/verification.py, bin/locations.py (one predicate is_live_checkout(root)), bin/rotate.py + bin/send.py (the (3) guards only), tests. CEILING: <=50 production lines, ONE kid, re-brief SM past 2x. INTERIM RULE until this lands (Prime 01:23Z): every pytest anywhere passes --basetemp under /tmp explicitly; no rotate/heal/send/posts test file runs."
title: L4 the suite refuses to start when its basetemp resolves to the live checkout and the runner basetemp lives under tmp
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-suite-refuses-to-start-when-its-basetemp-resolves-to-the-live-checkout-and-the-runner-basetemp-lives-under-tmp

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
