---
id: hypothesis:l4-a-typed-after-join-dm-marks-its-own-inbox-copy-read-so-no-nudge-fires-for-a-body-the-pane-already-carried
mint_id: 4453ebb6acbd451b97f80ed3fccac472
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 341b6895bd2281ff
season: 2
testable_claim: "goal:g15.25 SM.11 (intake: master-sensei 01:29Z, measured on its own gen 6: the after_join dm arrived typed mid-turn 01:25Z AND as an unread self-inbox copy whose wake nudge fired ~15 min later = one send.py read per post per rotation that returns only what the pane already carried). MEASURED on season2/main @594034bf8: rotate.run_after_join_for_seat :11900-11935 — typed_ok -> nudge_suppressed=True, delivery mode `typed`, then send_dm(seat, dm) STILL writes the durable copy (:11928-11930) into the seat inbox with the nudge suppressed but the message UNREAD; the inbox read position is the READ_MARKER line (send.py:103, rewritten only by cmd_read :3163-3166); the idle-wake path (send.py wake / the [agi-nudge] hook) keys on unread, so the copy fires later. CLAIM: (1) NEW send.py helper `mark_inbox_read(root, seat) -> int` = re-place READ_MARKER at the end of the seat inbox (same newline=\"\" read/rewrite the reader uses at :3159-3166; the SM.31 marker mover is the same primitive — reuse it when SM.31 has landed, name the shared function) and `_clear_announced`; returns the number of blocks newly covered; (2) in run_after_join_for_seat, when delivery mode == typed AND the dm write succeeded, call mark_inbox_read(root, seat) so the just-written copy is already-read; the record delivery dict gains `inbox: read` / `inbox: unread` so a dm+nudge delivery (typing refused) stays unread and nudges as today; (3) dry_run and an injected send_dm seam: untouched (no marker write); (4) the durable copy is still WRITTEN (the record + the signed dm remain the audit trail); a --dm read with --all still shows it. FALSIFIERS: a marker moved when typing was refused; a marker write on dry-run; the dm copy no longer written; a nudge fired for a typed delivery (assert via the wake unread digest = 0 after the flow in a fixture). TESTS (test_after_join_service.py, <= 4): typed -> inbox copy present AND unread digest empty AND delivery.inbox == read; typing refused -> unread, nudge kept; dry_run -> no marker; send_dm seam injected -> no marker. FILE SCOPE: send.py (one helper), rotate.py run_after_join_for_seat delivery tail; test_after_join_service.py. CEILING: <= 30 lines net, <= 4 tests."
title: "when the after_join dm was TYPED into the pane, its self-inbox copy is written already-read (READ_MARKER advanced past it), so no [agi-nudge] fires ~15 min later for a body the pane carried and the record holds in full (master-sensei gen 6, 01:4xZ: one send.py read per post per rotation, returning nothing new)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-typed-after-join-dm-marks-its-own-inbox-copy-read-so-no-nudge-fires-for-a-body-the-pane-already-carried

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
