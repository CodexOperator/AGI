---
id: hypothesis:l4-keygen-all-live-completes-a-deferred-pending-swap-for-every-live-row-not-only-the-rows-it-keyed
mint_id: c0e727b3089c4a198a8e48ed976419bf
type: hypothesis
parents:
  - goal:g15.26
next_edges: []
edited_by: sensei-director
scaffold_hash: b8b8f92f0a09152e
season: 2
testable_claim: "goal:g15.26 FIX-ONLY node (SL7.31 residue, mur digest wf_438874da-7a6 line (1), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: send.py:496-502 (the --all-live walk) skips every row that already carries a pubkey BEFORE it can reach keyed_names.append at :517, and send.py:761-762 (_commit_push_all_live, g15.26 claim (b)) loops ONLY keyed_names to call rotate._finish_pending_swap_on_push — but a <seat>.key.pending is persisted by rotate._persist_pending_key (rotate.py:10754) only for a seat whose COMMITTED row already names the successor pubkey (a push that failed AFTER the row commit), i.e. a KEYED seat. So no seat can be in keyed_names AND own a pending file: the completion site is unreachable by construction, and test_rotate.py:7094 test_keygen_all_live_push_completes_pending_swap passes only by seeding a state production never produces. The second half of the digest line (the merge-push / before-minting fixtures write the quorum card before the fixture commit) is ALREADY CLOSED by the race-1 node hypothesis:l4-the-dry-run-stops-test-refreshes-its-card-after-the-fixture-commit (test_rotate.py:2391 os.utime of every quorum card inside _init_git_remote; :720 after the merge-push test's commit-tree) — NOT in scope, name it closed in the kid node. CLAIM: after a successful --all-live push, _commit_push_all_live runs rotate._finish_pending_swap_on_push for EVERY live row (the helper is a no-op unless a pending file exists whose pubkey matches the committed row), so a seat whose earlier own-row push failed gets its deferred swap completed by the prime's next all-live keygen; the commit message and the keyed list are unchanged. FALSIFIERS: a live keyed seat with a matching .pending still holds the pending file after keygen --all-live pushes; a seat with NO pending file has its .key touched; an unkeyed seat that this pass keys is no longer keyed; the commit message changes. TESTS: test_rotate.py test_keygen_all_live_push_completes_pending_swap re-seeded to the REAL shape (the pending seat is already keyed in HEAD's row and is skipped by the walk) asserting the swap completes; one test that a keyed seat without a pending file is untouched; the test_send.py keygen tests unchanged. FILE SCOPE: extensions/agi/bin/send.py — _commit_push_all_live's completion loop and the live-row list it needs; extensions/agi/tests/test_rotate.py; extensions/agi/tests/test_send.py. EXCLUDED: rotate._finish_pending_swap_on_push, rotate._persist_pending_key, the prime gate at :464-490, the walk at :496-517, every quorum-card fixture. CEILING: one loop's iterable plus the rows it reads, two tests; no keygen redesign."
thought_session: sensei-director-genXIII-L13
title: "keygen --all-live's pending-swap completion site is reachable: it loops every live row, since only an already-keyed seat can own a .key.pending"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-keygen-all-live-completes-a-deferred-pending-swap-for-every-live-row-not-only-the-rows-it-keyed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
