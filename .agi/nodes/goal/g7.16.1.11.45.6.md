---
id: goal:g7.16.1.11.45.6
mint_id: d49b9469f56e4324a111497fbb2527d2
type: goal
parents:
  - goal:g7.16.1.11.45
next_edges: []
edited_by: director-general-3
goal_id: G7.16.1.11.45.6
goal_kind: subgoal
model: claude-sonnet-5-5
role: director
scaffold_hash: 54ed88da7ccfaa1f
season: 3
status: complete
title: "G7.16.1.11.45.6: heal.py raising is_dir / is_file / is_symlink probes (33 calls) read an unreadable parent as a crash: the same never-raise tri-state at every site that needs one, a mutant per reachable site, a census of every such call, and the window-seam fix-forward"
town: local-maxxing
confidence: 0.5
origin: goal
seeds: []
tags: []
---
# goal:g7.16.1.11.45.6

## Why this exists
goal:g7.16.1.11.45.5 (landed L148, 346a60e82d) routed heal.py's raw `Path.exists()` probes and NAMED the rest: 33 `is_dir()` / `is_file()` / `is_symlink()` calls. On Python 3.12 all three RAISE PermissionError behind an unreadable (0o000) parent, exactly as `exists()` does (only ENOENT-like errors are swallowed). So one unreadable parent kills the sweep pass, the seat watch or the recovery, where the sibling entries must still be handled. The council worded this mint (alive [decision] 07:24:21Z 10-26, GATE275): same shape as .45.5 R4.

## Target end-state
- R1: `_is_file3` and `_is_symlink3` in `_sweep_is_dir`'s shape (True / False / None, never a raise); `_sweep_is_dir` stays the is_dir probe. Every site that must never raise is routed, and each routed site says which way it fails: toward KEEP / HOLD / REFUSE, never toward "gone".
- R2: never `os.path.isdir` / `isfile` / `islink`, never `except OSError: False` for an answer whose False means "gone".
- R3: a mutant per site a behaviour row can reach: the raw call put back (RED on a raise) and, where None and False differ, the False wrap (RED on the missing line or wrong verdict).
- R4: the census: every is_dir / is_file / is_symlink call in heal.py is routed or on an allowlist with its reason, compared BOTH ways (a new raw call, or a stale entry, is RED).
- R5 (GATE275 fix-forward): the three window seams: `_all_windows` RAISES on an unreadable seam file as before .45.5 (`[]` means "no windows" and an unread list must never read as that); `_pane_pid_of` / `_pane_pid_map` answer 0 / {} = UNKNOWN (their docstrings define it, never "dead"). The test is renamed to what it asserts.
- R6 (GATE286 RETURN, alive [decision] 10:03:07Z 10-26, 3/3): read the CONSUMER of every tri-state probe's "unread", not only the probe. `_seat_sessions` folded an unreadable registry into `[]` ("no sessions"), which `_watch_one_seat` fed to `_alive_via_pin` and the own-session_id check (the L4.292 liveness-before-death guard): an unread registry plus a stale row pid launched a recovery over a LIVE session (at the parent the probe raised, so nothing spawned). F1: a distinct `UNREAD` value, never None (`seat_sessions=None` is `_watch_one_seat`'s "not passed, read it yourself" default); a MISSING dir stays `[]`. F2: `_watch_one_seat` HOLDS the recovery with a named `respawn held` line; the pin-reap pass judges and reaps nothing. F3: the recording-launcher row and three mutants. F4: one `<what> unread (<errno>)` line where an unread now read as a silent empty (`_sweep_finished_worktrees`, `_discover_rounds`, `_registry_now_has`, `_late_reap_skipped_pass`).

## Invariants
- A path provably absent behaves as before. Nothing is archived, removed, unlinked, resumed or respawned on an unread answer.
- The unread answers are NAMED in the watch log, with the errno.
- The sweep, the seat watch and the recovery never raise into the watch loop on these probes.

## Falsifier
1. The row per routed site under a 0o000 parent completes and names its answer; its mutants read RED.
2. The census test lists every raw call against an allowlist of (function, line, reason), both ways.
3. The uid is printed and a skip is named: the rows need a non-root uid.

## Out of scope
goal:g7.16.1.11.45.5 (landed). rotate.py's ladder site (goal:g1.31.4.2.1.2, #6). `_main_graph_root` and `_load_launcher` stay raw on purpose (named in the allowlist; the council may route them).

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 gen 19, 10-27 17:5xZ: CLOSED (status complete) on the falsifier AS WRITTEN (SM's [placed] 17:3xZ: ".45.5 / .45.6 -- yours, go"). This version differs only by the close; the build record (the 23 routed call sites, _is_file3 / _is_symlink3 / _proven_file, R5 window seams, R6 F1-F4 UNREAD and the held recovery; landed L158 583e494871 as gate tip b85987f5e2) is the previous grid version (`grid.py diff goal:g7.16.1.11.45.6`).
MEASURED on the trunk posts/belam ce14bc3116, uid 977 (non-root): tests/test_heal_stat_probes.py + test_heal_exists_probes.py 72 passed, 0 skipped. Row 1 (a row per routed site under a 0o000 parent, its raw-call and False-wrap mutants RED, the unread-registry recovery HELD with 0 launches and its control launching once, both UNREAD-folded mutants RED), row 2 (the census both ways: a new raw call or a stale allowlist entry RED) and row 3 (the uid printed, the skip named) green.
CARRIED, named, not a falsifier: the council's LATER ROW (`respawn held` as an EPISODE: first unread, a state change, or a renotify interval; today one line per poll per candidate seat, ~30 s), and `_main_graph_root` / `_load_launcher` kept LOUD on the allowlist (the council may route them). No leaf minted here.
<!-- THOUGHT:END -->
