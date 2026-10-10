---
id: goal:g7.16.1.11.19
mint_id: c2e8935893d64369b7be9e982d7905f1
type: goal
parents:
  - goal:g7.16.1.11
  - goal:g7.16.1.11.16
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.19
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: ea245e72bc8c0c05
season: 2
seeds:
  - goal:g7.16.1.11
  - goal:g7.16.1.11.16
status: complete
tags:
  - council
  - v5
  - verify
  - g7.16.1.11
title: "G7.16.1.11.19: verify runs as a v5 uid -- commands.py run verify skips what another uid owns (with a reason) instead of crashing, then one full run including the pytest suite; Python kept this season"
town: core
---
# goal:g7.16.1.11.19

## Why this exists
goal:g7.16.1.11: the owner keeps the old Python verify suite and tests THIS season (shell rewrites are season 3, owner 10-07 14:4xZ); the council placed the one open build (alive 14:54Z, owner aio): `python3 extensions/agi/bin/commands.py run verify` CRASHES when run as a v5 uid: PermissionError at verification.py:1376, reading another uid's transcript.
goal:g7.16.1.11.16: the shell-tests leaf says the old-setup Python tests retire WITH the old-setup Python; the owner's bypass moves that retirement to season 3, so the verify suite must keep running meanwhile, as the uid that now runs the posts.

## OWNER 2026-10-07 14:4xZ, verbatim (relayed by belam gen 27)
"we will keep reusing the old python based key system, metric system, and verify suite/tests unless most of those got rewritten into shell which is awesome."

## Target end-state
- `commands.py run verify` as a v5 uid never raises on a file it cannot read: an other-uid read SKIPs and prints the path and the reason; .env is read through the root-projected env file, or SKIPs with a reason.
- The pytest step on a uid with no pytest SKIPs with the reason 'no pytest for this uid' (never a pass, never a crash); the FULL run including the pytest suite is read from the uid that has pytest (SM's gate: 7,914 passed) and its numbers go to the town node, not the card.
- Python edits only: verification.py and commands.py are kept, not rewritten.

## Invariants
- A SKIP is never a pass: the run's verdict names every skipped read; no check turns green by skipping its own input.
- The run as belam (the uid that reads MAIN .env) gives the same verdict as before the change.

## Falsifier
1. As a v5 uid: `python3 extensions/agi/bin/commands.py run verify` exits 0 (or its own named non-zero verdict), prints one SKIP line per unreadable path with a reason, and the pytest step prints its SKIP reason when the uid has no pytest.
2. Negative: the same run prints zero `PermissionError` and zero Python tracebacks.

## Out of scope
goal:g7.16.1.11.16 (the shell-test rewrite, season 3) · provisioning.py and the key issue half (belam; K1 mint half season 3) · goal:g7.16.1.11.17 (verify gates that move only if the council says so).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-07 15:3xZ: active = worked now (lanes order to DG2 sent 15:3xZ). The pytest wording follows the measurement: a v5 uid has no pytest, so the step SKIPs with a reason and the full run is read from the uid that has it.
director-general-1 10-10 09:2xZ: COMPLETE, the two FAIL-not-crash bounds kept as RULED (10-07), not open. RE-RUN by me as the v5 uid director-general-1 on the trunk 751ec1fda0 (verify6 bb75aef045 is an ancestor), in a shm clone with no real links.py scan on E: `python3 extensions/agi/bin/commands.py run verify` (level=rotation, suite=off) ends RESULT: FAIL (1 of 13), 0 tracebacks, 0 PermissionError; 12 PASS (links broken=0, write-guard, smoke 5,647 active, viewport-verify, dispatch-help, budget, anonymize, seat-model, node-dirs, formation, census, node-count). The ONE FAIL is bin-suite-fresh 'SUITE REQUIRED: no suite has EVER run (no recorded timestamp)': ruled bound 1 (the stamp lives in MAIN's sessions dir; a writer uid runs --suite), a named FAIL, not a crash. seat-model prints 'skipped=4' with each seat's reason ('no pin-to-transcript (skipped)'), the SKIP-with-reason this goal asked for; node-count prints 'NOT STAMPED: not on integration branch'. Ruled bound 2 (crons reads FAIL from a LINKED worktree uid) did not fire in this clone. NOT exercised by this run: the pytest step (suite=off), whose 'no pytest for this uid' SKIP is covered by the lane verify-v5-uid.t.sh, 71 ok / 0 FAIL, run by me at the trunk 08:2xZ; the full pytest count (7,914 passed) is SM's gate, not read by me.
<!-- THOUGHT:END -->

10-07 16:1xZ built + run (dg3-verify5 23a6591f72, DG2 lanes 520c9c722, with SM), then DEMOTED at SM's gate 16:22Z (runs/mur-sm21-dg3-verify5: a skipped suite read rc 0 through _merge_up_suite, the pytest-import test is a substring, a stale stamp survives a red run; owner-aware SKIP and the write-failure rc are residues), NOT LANDED; the re-cut follows DG2's lanes. Two FAIL-not-crash BOUNDS stay as ruled: bin-suite-fresh reads FAIL on a v5 uid until a writer uid runs --suite (the stamp lives in MAIN's sessions dir); crons reads FAIL from a LINKED worktree uid (crons.py's own guard); the full pytest count is read from the uid that has pytest (SM's gate).
