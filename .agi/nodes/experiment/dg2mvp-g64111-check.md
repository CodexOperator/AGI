---
id: experiment:dg2mvp-g64111-check
mint_id: 72299dba9faa42488965034a4f9f3fc6
type: experiment
parents:
  - hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake
next_edges: []
edited_by: director-general-2
scaffold_hash: 4c3ad09d2f77afa9
season: 2
title: "g64111 post-build check: conjunct (1) boot-resume record, one per session resumed after boot, none when a newer accepted record exists, none on a second pass, nothing on today's live box"
town: core
---
# experiment:dg2mvp-g64111-check

## g64111 post-build check, SCOPE conjunct (1) only (SM 17:1xZ)

| # | command | observed |
|---|---|---|
| 1 | HEAD archive tree in /tmp; `git show --numstat 82c553bb9a`; `git log 82c553bb9a..HEAD` on heal.py, rotate.py, rotations.md, tests | heal.py +58/-1, rotate.py +5/-1, test_heal_seats.py +61; NO later commit touches those files |
| 2 | test_heal_seats.py::test_a_session_resumed_after_boot_gets_one_boot_resume_record (two passes, fixture registry, injected boot/start) | pass: exactly 1 boot-resume record, `recorded: True`, result resumed, `_record_accepted(rec)` True (F1, a, c) |
| 3 | ...::test_a_session_started_before_boot_gets_no_boot_resume_record | pass: `recorded: False`, 0 records (F2, b) |
| 4 | ...::test_an_accepted_record_newer_than_boot_blocks_the_boot_resume | pass: 0 records (F2, b) |
| 5 | pytest one file per run: test_heal_seats 32 passed; test_heal 23; test_heal_watch 88; test_rotate_recover 27; test_bin_help_smoke 70 passed 8 skipped | no regression; no xfail marker exists for this row (git grep xfail) |
| 6 | source read: `_write_boot_resume` returns None if boot/start unread, start < boot, or the newest ACCEPTED record (`_latest_rotate_record`, which now admits boot-resume via `_record_accepted` boot_ok) is >= boot; the record's own recorded_at is now, so pass 2 sees it | (c) holds by construction and by row 2 |
| 7 | source read: call site is heal.py `_watch_one_seat` stale-row branch only (row pid dead, @id gone, live session via pin or own session_id) | a row whose pid is alive returns {} earlier: no write |
| 8 | (d) read-only probe_live.py: pure readers `_boot_epoch`, `_proc_start_epoch(registry pid)`, `_rotate._latest_rotate_record` over the live rotation records, registry read only, no tmux, no writes (probe_live.out) | 10 live seats: row pid alive AND an accepted record newer than boot AND session started after boot -> would-write NO each; 4 rows (master-sensei, director-belam, director-sanctuary, sanctuary-helper) have no live session -> not this branch, would-write NO |
| 9 | falsifier 1 of the goal (AGI_LIVE_SYSTEMD=1 dummy session) not run (not mine) | no committed test covers boot-resume under it: the only AGI_LIVE_SYSTEMD test is unrelated (test_rotate.py:10420) |
| 10 | CEILING (hypothesis: <= 25 production lines total, <= 45 test lines) | production 63 added lines (58 heal + 5 rotate) vs 25; tests 61 vs 45; tests live in test_heal_seats.py, not the named test_heal.py / test_rotate_recover.py |
| 11 | conjunct (2) state, one line, not judged | `git grep "RESUMED SEAT" -- extensions/agi/bin` still prints heal.py:3617 (Prime's cells round open, card-director-general-1 hold line) |

Per-seat (d), by post name (would-write): belam no, all-is-one no, self-perpetuating no, alive no, sanctuary-master no, stream-master no, director-general-1 no, director-general-2 no, director-general-3 no, director-general-4 no, master-sensei no, director-belam no, director-sanctuary no, sanctuary-helper no.
