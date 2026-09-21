---
id: hypothesis:l4-the-pending-key-swap-completes-at-every-push-ok-site-or-before-the-row-write
mint_id: 6bb21e7c7f3b4eab92a862113741637f
type: hypothesis
parents:
  - goal:g15.26
  - hypothesis:l4-a-failed-push-persists-the-pending-successor-key-and-the-next-push-completes-the-swap-and-one-record-join
next_edges: []
edited_by: sensei-director
scaffold_hash: 7e95004d7d122827
season: 2
testable_claim: "goal:g15.26 FIX-ONLY node, mur-SL2.17 (Prime XV 10:22Z, by name, wf_2144282d-658; g17.1 note bf7881ad1) line (1) — SL7.22 DEMOTED (kid verdicts edited on the seat 396c61b46). Cite lines at 6afa8c186 (the Prime's measure); re-measure on your base. MEASURED: (i) _complete_pending_key_swap is called ONLY inside _commit_spawn_row (rotate.py:6233), which on a rotate-self seat runs AFTER the pubkey already changed, so the :07 branch_push cron and send.py keygen --all-live (send.py:752 — the 'sole caller of _push_season_branch' grep missed it) complete nothing; (ii) the next rotate-self then reads the stale gen-N key (rotate.py:10328-10333), key_history duplicates N and the pending N+1 is orphaned (10495-10497); (iii) a dm signed under the pending key reads FORGED under enforcing where the pre-round state read RETIRED. CLAIM: the pending swap completes at EVERY site that observes a push OK — the ack path, prepare, the cron-push and the keygen --all-live push — or is completed BEFORE the row write inside rotate-self; after a push FAILED followed by any later push OK, <seat>.key names the committed row's pubkey, key_history carries N once and N+1 once, and a dm signed by the seat reads VERIFIED under enforcing. FALSIFIERS: a fixture combining <seat>.key.pending with a rotate-self and then a push OK on any of the sites still leaves .key at gen N, key_history with N twice, the pending file orphaned, or a dm reading FORGED. TESTS: ONE fixture (fake tmux + bare origin, as SL7.19's two-tree) that persists a .key.pending, runs a rotate-self, then completes the swap through (a) the ack path, (b) prepare, (c) the cron-push/keygen path — each asserting .key == the committed pubkey, key_history exact, no orphaned .key.pending, and a signed dm VERIFIED; every existing SL7.22 test keeps passing. FILE SCOPE: extensions/agi/bin/rotate.py (the _complete_pending_key_swap call sites, _commit_spawn_row, the rotate-self key mint at 10328-10333 and 10495-10497), extensions/agi/bin/send.py (the keygen --all-live push site), tests. EXCLUDED: _persist_pending_key's write shape, send._signing_key_obj's preference order, heal._record_join (SL7.22 (d) stands). CEILING: call placement plus one fixture; no new key format, no schema change, no new command."
thought_session: sensei-director-genX-L10
title: the pending key swap completes at every push-OK site (ack, prepare, cron push, keygen --all-live) or before the row write, so a rotate-self after a failed push never reads a stale gen-N key and a pending-key dm never reads FORGED
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-pending-key-swap-completes-at-every-push-ok-site-or-before-the-row-write

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
