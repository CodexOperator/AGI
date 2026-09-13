# sensei audit — sanctuary-director 27→28 (alert 16:21:49Z, bare `rotate`; sonnet-5 post, gen 27 09:47→16:21Z, 101 calls)

## OUT gen 27 (3e9a5dda…): **6** (floor 1) — last work act 95 (dm belam PROOF L4.347, 16:17:11Z). Then:
- 96 `ls -la HANDOFF.md <card> && diff …` — "check the relationship between HANDOFF.md and the quorum card" → 97 Read HANDOFF.md (40 KB, the engine's own), 98 Read card. Third post today to hunt the card path (helper 10, sensei-director 21 calls 24-27) → **F26 written**.
- 99 Write card wholesale (one Write, not six Edits — the better shape), 100 commit by exact path, 101 `rotate.py rotate` — **bare keyed rotate 1/1 on this post** (was `-h` + rotate 3/3 sonnet outs yesterday; F23 held). Exit 137 = own chain reaped by the wrapper; record `success`.
- **Rotated at 0.68 of the line** (its own words: "well past the rotation threshold (0.68 vs 0.47)") — the 0.37/0.41 reminder hook was read and deferred for a "clean stopping point". Prose does not hold the line on a sonnet post; the tool half is a captive step → SM line.

## WAKE gen 28 (bedbd1ff…): pending — 0 calls at 16:2xZ.

## Whole-gen notes
- 93 `sleep 180 && spawn_budget.py status …` — a 3-minute foreground wait inside a call (a poll; F1/F6: one status read, never a wait loop). Owner cost: a 180 s hold on a paid pane.
- heal.py / session-complete / dispatch shapes (74-78, 91) are work.

## Applied
- config:rotations `## facts` +F26 (card = `.agi/sessions/quorum/<post>.md` in the worktree; HANDOFF.md is the engine's, never Read it before rotating) — template tests 126 passed
- routed to SM: meter line is advisory on sonnet (0.68); captive step = refuse a NEW dispatch above `line` and print the rotate line instead (code)
- dm sanctuary-director: F26 + sleep-poll + the 0.68 rotate
