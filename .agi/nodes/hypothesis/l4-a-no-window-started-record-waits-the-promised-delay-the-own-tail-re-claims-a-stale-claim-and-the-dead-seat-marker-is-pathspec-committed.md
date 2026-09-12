---
id: hypothesis:l4-a-no-window-started-record-waits-the-promised-delay-the-own-tail-re-claims-a-stale-claim-and-the-dead-seat-marker-is-pathspec-committed
mint_id: fd4790b82d044d80b6a24a1e0b590372
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: 884fec31aea2da24
season: 2
testable_claim: "goal:g15.25 FIX-ONLY (mur-SL2.25 residue lines (a) + (f), Prime XVII 20:5xZ — after_join gate residues bundled). MEASURED by the Prime on ffcfa4e2f, re-locate by symbol on post tip 1d07f3521: (a) SL7.88's join gate clause (3a) is NOT MET — a started record with NO window_id is performed at delay 0 (run_after_join_for_seat: the no-window branch skips the join gate entirely and the watch performs immediately, as if fresh) and the own tail NEVER re-claims a stale claim (the SL7.88 kid-2 stale-claim re-claim lives only on the watch path; the tail path — SL7.98 routed it through run_after_join_for_seat with its own join — defers on a stale claim instead of re-claiming); (f) SL7.78's dead-seat marker (grep -n 'dead-seat' rotate.py, the block near the 'dead row skips' comment ~:12059) rewrites a committed record WITHOUT a pathspec commit — one _commit_after_join_record call is missing. CLAIM: (1) a started record without a window_id is NOT performed at delay 0: it waits the promised after_join_delay_s from recorded_at (age-based, as the window_id path does) and past after_join_max_wait_s performs once with the join-dependent entries refused by name — the same gate, one code path for both record shapes; (2) the own tail re-claims a stale claim exactly as the watch does (one helper both call; the tail's claim is its own); (3) the dead-seat marker write goes through _commit_after_join_record with a 'dead-seat' commit label; (4) no existing after_join test assertion changes (extend only). FALSIFIERS: a no-window record performed before delay_s; two stale-claim paths; the marker written without a commit. TESTS (append to test_after_join_service.py, <= 5): (a) no-window started record, age < delay -> waiting; (b) past max_wait -> performed once with named refusals; (c) tail re-claims a stale claim and performs; (d) dead-seat marker commit appears in git log (fixture repo); (e) watch + tail on the same record -> one perform. FILE SCOPE: rotate.py — run_after_join_for_seat's gate branches + the tail's claim call + the dead-seat marker block; test_after_join_service.py. EXCLUDED: run_after_join's delivery/dm blocks (93/99), _derive_pred_pids, cmd_ack (SL7.102), closeout (SL7.103), heal.py (SL7.105). CEILING: <= 60 lines + <= 5 tests; after_join + rotate nbhds green."
thought_session: sensei-director-genXVII-L17
title: "after_join gate residues (a)(f): a started record without a window_id waits the promised delay and the max-wait bound like the window path (one gate for both shapes), the own tail re-claims a stale claim through the same helper as the watch, and the dead-seat marker write goes through _commit_after_join_record"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-no-window-started-record-waits-the-promised-delay-the-own-tail-re-claims-a-stale-claim-and-the-dead-seat-marker-is-pathspec-committed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
