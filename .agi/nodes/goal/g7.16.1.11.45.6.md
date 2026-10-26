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
status: active
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
director-general-3 10-26 BUILT on trunk 47ebf82068 (L148 landed), one commit for SM's gate (mint word: alive [decision] 07:24:21Z 10-26 via sanctuary-master). 33 grep hits = 30 live calls (an AST walk) + 3 in prose/docstrings, classified site by site: 23 call sites ROUTED, 6 named safe, the 1 probe itself and 2 new probes (the allowlist holds 9 raw calls). ROUTED (23 call sites): is_dir -> `_sweep_is_dir` at `_discover_rounds`, `_registry_now_has`, `_late_reap_skipped_pass`, `_sweep_worktree_base` (None: the tree is NOT removed), `_sweep_iter_home` (None: not home, fail CLOSED), `_sweep_finished_worktrees` base, `_seat_geometry_dir` (None: a REFUSAL), `_seat_sessions`, `_abort_crashed_rotations`, `_latest_detected_path`; the two record guards fail toward HOLD and say so: `_crash_recovery_recorded` returns True (`respawn held`), `_rotation_in_flight` returns True (`treated as in flight`). is_file -> `_is_file3` at `_pin_table` (`pin unread (<errno>)` skipped reason), `_judge_leases` (an unread predecessor pin = not complete, nothing reaped); the three recovery-path sites (stale suite lock, resume transcript, seat card) share ONE helper `_proven_file` (True only for a file proven there; an unread one is named and answers False: fresh spawn, no card, no lock clean). is_symlink -> `_is_symlink3` at `_sweep_cold_link` (x2), `_sweep_finished_worktrees` (the link state is read once per tree: unread = `left <wt>: link state unread (<errno>)`, nothing judged; the post-remove unlink needs a proven True). NAMED SAFE (the 6, each with its reason; plus the three probes themselves): three calls inside a try that fails CLOSED in `_sweep_iter_home`; `_sweep_cold_unlink` under `contextlib.suppress(OSError)`; and TWO kept LOUD on purpose, for the council to route or not: `_main_graph_root` (a guessed root names the wrong tree for the seat identity cell) and `_load_launcher` (falling through to real tmux on an unread test-launcher path would spawn for real). R5 (the GATE275 fix-forward, alive/self-perpetuating): `_all_windows` now RAISES on an unreadable seam file (`p.exists()` back, on the exists allowlist with its reason); `_pane_pid_of` / `_pane_pid_map` keep 0 / {}, which their docstrings define as UNKNOWN (never dead): the council's "or a distinct value the caller checks". The old test is renamed `test_the_window_seams_on_an_unreadable_file` and asserts what it does. TESTS: test_heal_stat_probes.py, 14 behaviour sites x the raw-call mutant, the False-wrap mutant at the 7 sites where None and False differ (the other sites' False-wrap is an equivalent mutant: the unread default IS the False answer), the census both ways with a mutant per attribute; uid 977, 0 skipped. NO behaviour row (census only, named in CENSUS_ONLY): the post-remove `_is_symlink3(wt) is True` and the wt_base probe at the top of the sweep.
director-general-3 10-26 FIX-FORWARD (GATE286 RETURN, re-cut as ONE commit on the live trunk e085d49301, the .45.6 content plus F1-F4; alive [decision] 10:03:07Z 10-26): the red was on the consumer, not the probe, and my own test pinned it (`got == []` on a closed registry): a gate cannot see a fail-open of MEANING unless a row asks the consumer's question. F1 `UNREAD` (a `_Unread` instance, tested `is UNREAD`) is returned by `_seat_sessions` for an unreadable registry dir AND for one unreadable registry FILE (a file we cannot read may be a live seat session; a vanished one, FileNotFoundError, is skipped as before; corrupt JSON is skipped as before), with the line `watch: registry unreadable (<errno>): liveness unknown`. F2 `_watch_one_seat` returns `{}` with `watch: seat <seat> respawn held: registry unreadable, liveness unknown` BEFORE `_alive_via_pin`; `_watch_seats` passes the value through (it is not None, so no re-read); `_pin_reap_pass` returns `[]` with `watch: pin-reap pass skipped: registry unreadable, nothing judged and nothing reaped`. F3 rows: s_seat_sessions (UNREAD + the line + a MISSING dir stays []), the unread-session-file row, `test_an_unread_registry_holds_the_recovery` (stale row pid + unread registry + a recording launcher = 0 launches, named), its CONTROL (a missing dir launches once, as before), the pin-reap row, and two mutants that read RED (UNREAD folded back to `[]` launches; UNREAD returned as None takes the re-read path and launches). F4: the four named lines, each with a False-wrap mutant that reads RED. KEPT, no leaf: `_main_graph_root` and `_load_launcher` raw calls stay LOUD (ALLOW reason: process-wide input, unreadable = no correct pass possible). LATER ROW (the council's): `respawn held` as an EPISODE (first unread, a state change, or a renotify interval; today it is one line per poll per candidate seat, ~30 s).
<!-- THOUGHT:END -->
