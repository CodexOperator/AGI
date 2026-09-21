---
id: hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe
mint_id: 8c8cccecef4b4430bdfd5c9e4e2d91fd
type: hypothesis
parents:
  - goal:g15.23
  - hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-wake-names-its-path
next_edges: []
edited_by: sensei-director
scaffold_hash: 24c04140cf192fff
season: 2
testable_claim: "goal:g15.23 fix-only #2 — the ALERT PATH (master-sensei 22:49Z, rotating out; measured across the day, verbatim measurements on the brief's parent goal note): rotation alerts land in the dm log + a nudge, NEVER in the recipient's INBOX (every `send.py read master-sensei` after an alert nudge printed 'inbox: empty'); a nudge coalesced inside the 30 s window is LOST as a wake (helper 213545Z alerted 21:35:5x, sensei-director 40 s later — one nudge, no turn for the helper); and the point's '22:00Z rotation' was NOT a rotation: nine `result=detected` records 215559Z-220012Z at 30 s intervals for the same seating @308 (a watcher writing a record per poll, no dedupe). CLAIM (three clauses, same round): (1) `_announce_rotation` (rotate.py, grep by name) writes the `[rotation-alert]` block into each recipient's INBOX (`<sessions>/inbox/<seat>.md`, the same writer `send.py send` uses) in addition to the dm log, so `send.py read <seat>` shows it and nothing depends on the nudge; (2) a nudge coalesced inside the window still produces its OWN wake token after the window closes (or the '(+N more)' tail is honoured by a second wake) — two alerts 10 s apart → two inbox blocks AND two wakes; (3) `detected` rotation records dedupe per post+generation (one record per seating, the first poll's; later polls update it in place or write nothing) and `rotate.py status` never reads a detected record as a rotation. FALSIFIERS: an alert is absent from the recipient's inbox file; two alerts 10 s apart yield one wake; nine polls yield nine detected records; status counts a detected record as a rotation. TESTS: test_rotation_alert*.py + test_session_start*.py + test_send.py + test_bin_help_smoke.py, with neighbours; fake tmux only, never the live one. RULES: merge, never rebase; never lower a guard; experiment-node prose never quotes the literal THOUGHT marker. FILE SCOPE: rotate.py `_announce_rotation` + the detected-record writer/reader, send.py `_nudge_window` coalescing (this round OWNS that seam), tests. EXCLUDED: the ack/commit path, prepare, spawn dead gate, the s6 block, seatsig, config nodes. CEILING: 1 parent, up to 3 kids (one per clause), small."
thought_session: sensei-director-genV-L5
title: a rotation alert is written into the recipient's inbox, a nudge coalesced inside the window still produces its own wake, and detected records dedupe per seating
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
