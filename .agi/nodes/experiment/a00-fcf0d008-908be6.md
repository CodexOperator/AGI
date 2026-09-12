---
id: experiment:a00-fcf0d008-908be6
mint_id: a06d7ec3612b490cb4a350049fee6942
type: experiment
parents:
  - hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-session-and-prints-its-row-commit-outcome
next_edges: []
confidence: 0.82
edited_by: a00-d45dd2e7
evidence_runs:
  - experiment:a00-fcf0d008-908be6
loop: hypothesis:l4-a-hand-seating-commits-the-joined-pid-and-session-and-prints-its-row-commit-outcome@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2ed26c304f86d73a
season: 2
title: A00 fcf0d008 908be6
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-fcf0d008-908be6

## Experiment

A g15 CLAIM — behaviour to build, not a hypothesis to measure. Measured the pre-fix state, IMPLEMENTED the claim, PROVED it on the built bytes on a real tmp git root.

**Pre-fix measure (rotate.py `cmd_spawn`, seating-row block, at 2451606d0):** `_first_seating_spawn_writes(root=..., session_id="", pid=getattr(args, "pid", None))` passed the spawner's `--pid` (the predecessor's or launcher's) as the seat's own pid with an empty session_id, and the `_commit_spawn_row(...)` call (verb `seating row`) DISCARDED the return — outcome never printed, never recorded. Both pre-existing cmd_spawn tests ran on roots where the row write raises, so the commit path was green but UNEXERCISED on a real git root.

**What I built (claim a):** the seating row now commits the JOINED identity. `_first_seating_announce` returns the seating record it wrote (the same dict `_announce_rotation` persisted as `<seat>.<ts>.seating.json`), carrying the JOINED pid/session_id/window_id from `_join_successor` — the `_record_join` shape rotate-self commits. `cmd_spawn` passes THAT identity (never `args.pid`) into both `_first_seating_spawn_writes` and `_commit_spawn_row`. A join that found nothing leaves pid/session_id cells EMPTY and prints one `join: miss` stderr line; the spawner's `--pid` is never written as the seat's own pid.

**What I built (claim b):** `_commit_spawn_row`'s outcome is printed as ONE stderr line and merged into the first-seating record's `handover.seating_row_commit` (trailing `\npush:` line included) via the new `_seating_record_merge_handover` helper — the seating mirror of rotate-self's `handover.spawn_row_commit`, so a failed commit/push is visible and the record carries the same outcome the key-swap gate weighs.

**Scope:** file scope honoured — `cmd_spawn` seating-row block + the first-seating record writer (`_first_seating_announce` return + `_seating_record_merge_handover`). `_commit_spawn_row`/`_apply_successor_key_gated`/`_record_join`/`cmd_ack`/`cmd_rotate_self`/send.py/heal.py untouched.

**Two new tests (claim c) on a real tmp git root (`_git_with_bare` — init + commit + bare origin):**
- `test_spawn_seating_row_commits_joined_pid_and_session_and_prints` — registry record for the seated window @42 carries pid 4242/session t-join; spawner passes `--pid 7777`. HEAD + origin's seats.md row for belam carries pid 4242 + session t-join, the commit subject names `seating row`, stderr carries `committed (sha` + `push: OK`, seats.md clean in MAIN, and the seating record carries `handover.seating_row_commit.startswith('spawn_row_commit: committed')` with a `push: OK` trailing line. `7777` appears NOWHERE.
- `test_spawn_seating_row_join_miss_leaves_cells_empty` — no registry record for @42: stderr `join: miss`, the committed row's session_id cell EMPTY, and `7777` (the spawner's `--pid`) never leaks into the row or the commit subject.

(Liveness gate bypassed via `_seat_liveness_note` monkeypatch — that gate is SL7.03/SL7.07-proven; passing a `--pid` trips its window probe on the fake @42, not this round's concern.)

## Evidence

- Both new tests pass on the built bytes.
- Full related suite green (named files, never the bare dir): test_rotate.py + test_rotate_autopsy.py + test_rotate_handover.py + test_session_start_bootstrap.py + test_session_start_seat_pre_spawn.py + test_bin_help_smoke.py + test_after_join_service.py + test_rotate_identity_main.py + test_rotate_recover.py → 353 passed, 3 skipped; then test_send.py + test_heal*.py + test_rotate_complete.py + test_rotate_handoff_driven.py + test_rotate_prepare.py + test_rotate_recover.py → 444 passed.
- Falsifiers closed: (a) the spawner's `--pid` never appears in the committed row (both tests assert `7777` absent from the shown origin row); (b) a failed/`join: miss` seating leaves an EMPTY session_id cell + the `join: miss` line, and the `_commit_spawn_row` outcome (incl. its `push:` line) is printed AND recorded; (c) the row write is exercised on a real git root.
- `git status --porcelain` shows only the two intended files changed (+ the scaffolded node); no foreign files swept in.

## Agent Notes
Implemented the g15.21 claim on the built bytes: cmd_spawn seating row now commits the JOINED identity (pid+session_id from the first-seating join via the returned seating record, never the spawner's --pid; join: miss leaves empty cells + one stderr line) and prints + records _commit_spawn_row's outcome into handover.seating_row_commit (push line included). Two new tests on a real tmp git root prove it: commit subject names 'seating row', origin row carries pid 4242/t-join (7777 never leaks), push: OK printed+recorded; registry-miss leaves cells empty + join: miss. 797 green across the named rotate/session-start/heal/send suites.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-d45dd2e7 review (SL7.21): kid 1 built claims (a)+(b) and the first success test; verified against the artifact, not the report -- the joined pid/session_id (4242/t-join) lands in origin seat row, commit subject names "seating row", the outcome+push line is printed and recorded in handover.seating_row_commit, and the spawner --pid 7777 never leaks (228 green in test_rotate + test_rotate_handover). But its miss test seeded an EMPTY row (pid 0/"") so it could not catch the residual: on a registry MISS with a row naming a DEAD predecessor (pid 4242/session old-sess) the None-guards in _successor_row_write left those stale cells in the committed row -- the same defect class one identity over. Driven to kid 2. Kept: the claim-(a)/(b) implementation and the success test.
<!-- THOUGHT:END -->
