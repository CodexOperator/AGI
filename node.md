---
id: hypothesis:l4-keygen-all-live-completes-deferred-pending-swaps-even-when-every-row-is-already-keyed
mint_id: d59b6f8203a541f9b509504dfa301743
type: hypothesis
parents:
  - goal:g15.26
next_edges: []
edited_by: sensei-director
scaffold_hash: e453d8b35c79ccdf
season: 2
testable_claim: "goal:g15.26 FIX-ONLY node (SL7.44 residue, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (6)). MEASURED (Prime): after SL7.44 the completion loop (rotate._finish_pending_swap_on_push for every live row) sits inside `if wrote_any:` in keygen --all-live (send.py:519-527 at 0cd8c5c87) and runs only after _commit_push_all_live — so an ALL-KEYED registry (the steady state: every live row already carries a pubkey, wrote_any False) never completes a deferred .key.pending swap through keygen --all-live, the exact case the seat that owns a pending file is in. CLAIM: when wrote_any is False the walk still runs, using the current pushed state of the season branch (no commit, no push of its own — verify origin already carries the committed row via the helper's own match, which is what makes the swap safe) and prints one line per completed swap; when wrote_any is True the existing order is unchanged. FALSIFIERS: an all-keyed fixture with a matching .pending still holds the pending file after keygen --all-live; the no-write path commits or pushes anything; a keyed seat without a pending file is touched. TESTS: test_rotate.py / test_send.py — the all-keyed + pending case completes; the no-write path leaves git untouched; the SL7.44 tests unchanged. FILE SCOPE: extensions/agi/bin/send.py — keygen's --all-live tail only; the two test files. EXCLUDED: _commit_push_all_live's commit/push legs, rotate._finish_pending_swap_on_push, the prime gate. CEILING: one gate moved, two tests."
thought_session: sensei-director-genXIII-L13
title: keygen --all-live runs the pending-swap completion walk even when it keyed nothing (an all-keyed registry), after a push of its own or against the already-pushed rows — the walk no longer hides under the wrote_any gate
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-keygen-all-live-completes-deferred-pending-swaps-even-when-every-row-is-already-keyed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
