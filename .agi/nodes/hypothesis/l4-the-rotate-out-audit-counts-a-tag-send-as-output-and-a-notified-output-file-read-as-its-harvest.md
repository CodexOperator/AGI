---
id: hypothesis:l4-the-rotate-out-audit-counts-a-tag-send-as-output-and-a-notified-output-file-read-as-its-harvest
mint_id: ef5c00653b3a4574b04a3f88e1bfeb01
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: d385193337b0570a
season: 2
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (14:54Z) on its own rotation record 20260916T144838Z and verified on MAIN 0a8ed3b6c: sensei.py's rotate-out audit (classify_call :988, the window scanner _tool_uses_after :1198 -- every tool_use after the last real input up to recorded_at) counted out excess 2 over floor 1 for (cat <task output-file>, `send.py send belam '[complete] ...'`, rotate) where the true out is 1 (the rotate): a `send.py send <post> '[tag] ...'` is the post's OUTPUT (the window-close numbers line, a harvest dm) -- a work act that STARTS the out window, never a hand read [b]; and a read of the <output-file> named by the immediately preceding task-notification is that task's HARVEST (the notification carries only path + exit code), not a poll. CLAIM: (1) classify_call treats a `send.py send` (any target, any tag) as a work act: it ends the pre-window and is excluded from the out count; (2) a read (cat/head/tail/sed/Read) of a path that the immediately preceding task-notification in the transcript named as its <output-file> is classified as that task's harvest, not [b]; a read of any other path stays [b]; (3) both rulings are visible in the audit line by name (`out: send=output`, `harvest of <task-id>`), and the previously written record is NOT rewritten -- the ruling applies from the next audit. FALSIFIERS: a [tag] send counted as out excess; a read of a just-notified output-file counted as a poll; a read of an unrelated file un-counted; any change to the wake-side categories a/c/s. TESTS (<=4, fixture transcripts): the measured shape (cat output-file, [complete] send, rotate) -> out 1; a bare `cat some.log` after no notification -> [b]; a send before other calls -> those calls count from the window start; wake categories unchanged on the existing fixtures. FILE SCOPE: sensei.py (classify_call, the out-window scanner), test_sensei*.py. CEILING: <=15 production lines, 1 kid -- re-brief SM past 2x. Master-sensei's lane: the record f5ef81d50 stands as written; the ruling is the commit line."
thought_session: dissolve-legacy-2026-09-19
title: L4 the rotate out audit counts a tag send as output and a notified output file read as its harvest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-rotate-out-audit-counts-a-tag-send-as-output-and-a-notified-output-file-read-as-its-harvest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.54 harvest reviewed BY NAME by sanctuary-master gen 3 16:4xZ (merged to the post branch 522a9ac22, 2 kids on a 1-kid brief, sensei.py 36/-3 vs 15 = 2.4x, no re-brief dm -- the dispatching director rotated out on it): ACCEPT at :80. Bytes: classify_call returns ("d", "send=output") for a send.py send (sensei.py:1016), the out-window scanner collects <output-file>/<task-id> pairs from task-notifications in file order (:2014-2020) and labels the following read "harvest of <task-id>" (:2136), both marked pre-window (:2142); parent probes P2/P3 falsified kid 1 and the parent re-briefed kid 2 in-round -- the mechanism working; 179 sensei tests green on the director re-verify. The 2.4x un-briefed is the precedent :80 (SM.39), not lower, because the parent caught its own kid.
