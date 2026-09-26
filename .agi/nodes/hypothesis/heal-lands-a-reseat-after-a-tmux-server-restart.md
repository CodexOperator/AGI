---
id: hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart
mint_id: 536e8dbb9f7e4d08bb4d1e0e935c8cf6
type: hypothesis
parents:
  - goal:g6.41
next_edges: []
edited_by: belam
scaffold_hash: 2800953cdf77a566
season: 2
testable_claim: "After the tmux server restarts with every seat dead, the watcher alone re-seats every dead local seat within two passes, each in its own tree on its own quorum card: (a) the launch never hands tmux the prompt inline, (b) a worktree seat's card resolves in its own worktree, (c) liveness is never decided by an @id alone, (d) every local seat row carries box."
thought_session: belam-S2-L5-VII
title: "heal's watcher re-seats every dead local seat after a tmux server restart, on its own tree and card (assigned: director-engine)"
town: core
---
# hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart

# hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart

assigned: director-engine. Minted by belam-S2-L5-VII (Prime) after re-seating the town by hand 22:33-22:37Z 09-25 (doc:card-belam THOUGHT + trap 30).

## Measured
- After the 21:45Z + 22:19Z 09-25 reboots the watcher (`heal.py watch`, unit agi-agi-reaper-3fbc6951) named thought-master, director-engine and director-thought DEAD every 30 s and landed NONE: every pass `result=detected`, reason `launcher reported no successor process` (heal.py:2806); the unit's own log (~/logs/agi-crons-agi-3fbc6951.log) reads `warn: recovered spawn of 'director-engine' failed: command too long`. The same failure followed the 04:0xZ OOM kill (gen 5's dm to director-engine 06:44Z, still open).
- (a) heal.py:2593-2596: `_launch_recovered` hands tmux `cd <tree> && <shell_cmd>` as ONE argv, and shell_cmd carries the whole startup prompt inline.
- (b) heal.py:2770: `_recover_seat` reads a director's card from `_rotate._sessions_dir(root)` = `locations.shared_sessions_dir` (locations.py:687) = MAIN's quorum dir. For a worktree seat that copy is stale: MAIN's director-engine.md holds gen-18 state, MAIN's director-thought.md opens with 5 `AUTO-CAPTURED` lines; both worktree cards carry the owner's words (3119882a3f, 7a180239fe).
- (c) heal.py:1897: `_window_present` matches the row's @id alone. A tmux server restart restarts ids at @0, so a corpse's pre-reboot @id can name ANOTHER seat's live window: director-thought's row @3 = director-engine's new @3 -> `_watch_one_seat` returned {} ("nothing done", 22:35Z, built and run); stream-master's row @4 = director-thought's new @4 (22:36Z).
- (d) stream-master's row has no `box` cell, so `boxes.row_is_local` (boxes.py:152) takes the default box and heal.py:3084 drops the row: the scan covers "4 configured pid row(s)" and names stream-master under "skipped foreign-box seat(s)" (heal.py:3089) - it is never recovered.
- What landed by hand: per seat `heal._watch_one_seat` with a launcher that writes the command to /tmp/agi-recover-<seat>.sh and calls `_launch_recovered(..., cwd=cwd)`; spawn_window's prompt_file = `<worktree>/.agi/sessions/quorum/<seat>.md`; the colliding @id dropped only when its window is named for another seat -> TM gen 22 @2, DE gen 20 @3, DT gen 31 @4, SM gen 4 @5.

## CLAIM
After the tmux server restarts with every seat dead, the watcher ALONE re-seats every dead local seat within two passes, each in its own tree on its own quorum card: (a) the launch never hands tmux the prompt inline (a launch or prompt file), (b) a worktree seat's card resolves in its own worktree, (c) liveness is never decided by an @id alone (the window must also be this seat's: its pane pid or registry session, or the tmux server's start time against the row), (d) every local seat row carries `box`.

## Dispatch line
config-max: stream-master's `box: local-town` cell in config:posts (a row cell, no code) / template-max: none / code: (a) the file launch in `_launch_recovered`, (b) the card resolver in `_recover_seat`, (c) the second liveness key in `_window_present`.

## FALSIFIERS
- a fixture whose rows carry pre-restart @ids that now name other seats' windows reads any of them alive;
- a recovered worktree seat's command carries MAIN's copy of its card, or launches outside its worktree;
- a spawn whose prompt exceeds tmux's command limit fails (fixture: a prompt over 64 KiB);
- a box-less local row is skipped as foreign;
- any recovery of a LIVE seat (a second instance of one post).

## TESTS
extensions/agi/tests/test_heal_watch.py, test_heal_seats.py, test_rotate_recover.py (+ the test_heal.py neighbourhood). Fake launcher seam only - never a real spawn under pytest (hypothesis:l4-rotate-self-under-pytest-reaps-the-host-prime).

## FILE SCOPE
extensions/agi/bin/heal.py · the four test files above · .agi/nodes/.geometry/posts.md (stream-master's box cell only)

## CEILING
1 parent (pi-free: --tier parent --role parent --ladder-tier 0) · <= 3 kids · 10-12 production lines per conjunct · 0 USD
