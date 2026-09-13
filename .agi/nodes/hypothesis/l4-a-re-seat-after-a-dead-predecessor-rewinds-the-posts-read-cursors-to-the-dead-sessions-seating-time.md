---
id: hypothesis:l4-a-re-seat-after-a-dead-predecessor-rewinds-the-posts-read-cursors-to-the-dead-sessions-seating-time
mint_id: 049f7f333bb842dda264ae083fb4eb7a
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: a5a018ea1d035844
season: 2
testable_claim: "goal:g15.25 SM.03 (intake: master-sensei 23:39Z line 2). MEASURED: send.py read state is a per-conversation `<file>.state.json` holding {participant: read_count} (send.py:1043-1054 _load_state/_save_state; _past :1057 advances the count on commit; boundary split _MSG_BOUNDARY_RE :99 on `---\\ts: … from:`); my killed 22:59Z session (belam-S1-L4-XIX) read master-sensei two intake dms (state master-sensei--sanctuary-master.md.state.json = {\"sanctuary-master\": 12}) so the re-seat STARTUP [inbox] carried nothing and gen 1 paid calls 2-3 grepping the dm log. cmd_spawn already knows the predecessor died: the autopsy branch rotate.py:1783 (`dead and not --no_autopsy`) with pred_pid + pred_death (:1770 _death_timestamp). CLAIM: (1) a NEW send.py function `rewind_read_cursors(root, seat, since_ts) -> list[tuple[str,int,int]]` — for every conversation file the seat participates in (its inbox + every dm/room state carrying the seat key), recount the blocks whose ts < since_ts and, when that count is LOWER than the stored cursor, set the cursor to it; returns (conversation, old, new) per change; rooms and other participants keys untouched; (2) cmd_spawn calls it in the dead-predecessor branch ONLY (:1783 region), with since_ts = the dead session seating/rotation record recorded_at (fall back to pred_death; when neither resolves print one line and skip — never rewind to 0); prints one line per rewound conversation `[seating] rewound <conv> <old>-><new>`; (3) a live predecessor, --no-autopsy, --dry-run: no state file touched; (4) the STARTUP [inbox] entry runs AFTER the rewind (measure the order in cmd_spawn and say the line). FALSIFIERS: a rewind that touches another participant key; a rewind below the count of messages older than since_ts; any state write on a live-predecessor spawn or dry-run; a run that reads dm bodies (count blocks only). TESTS (new test_send_rewind.py <= 5 + 1 in test_rotate_autopsy.py): cursor 12, since_ts before msgs 11-12 -> 10; cursor already lower -> untouched; other participant key intact; room state untouched unless seat is a key; dead-predecessor spawn dry-run prints the would-rewind lines and writes nothing. FILE SCOPE: send.py (new function), rotate.py cmd_spawn dead branch, two test files. CEILING: <= 60 lines net, <= 6 tests."
title: "a re-seat after a DEAD predecessor rewinds the post read cursors to the dead session seating time, so STARTUP [inbox] re-carries what the killed session consumed (intake: master-sensei 23:39Z line 2; measured: SM re-seat paid 2 calls hunting two dms)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-re-seat-after-a-dead-predecessor-rewinds-the-posts-read-cursors-to-the-dead-sessions-seating-time

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
