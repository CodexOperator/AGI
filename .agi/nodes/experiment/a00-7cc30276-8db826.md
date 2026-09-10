---
id: experiment:a00-7cc30276-8db826
mint_id: de55b034a2c44f2bb7f9d9c6ba1379b6
type: experiment
parents:
  - hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking
next_edges: []
confidence: 0.7
edited_by: a00-bb0994fd
evidence_runs:
  - experiment:a00-7cc30276-8db826
loop: hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3c34c931f1f520ba
season: 2
title: Shared room fixed via hoisted resolver; every sessions consumer enumerated and classified
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-7cc30276-8db826

## Experiment

Completion pass on `hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking`. Delivered the four open pieces the parent review held at lean 78: **(g4)** the shared-room resolver, **(w1)/(g5)** the full directory-addressed enumeration + per-consumer classification, and **(w4)** the successor-first-reply measurement. Full engine suite green (2310 passed, 1 skipped).

**G4 — the shared helper, fixed the honest way.** The sessions directory is MIXED, not uniformly shared: the meter pins / mail / budget / suite stamp / rotation records must be ONE room across worktrees, but the `iter-*` output dirs are legitimately per-worktree during a run (a seat's session is forked in its own worktree and merged home by `session-complete`/`rotate complete` — `cli.py:1520` and `rotate.py:1639` are the merge). So a single "shared" `sessions_dir` is the wrong abstraction. Resolution: hoisted the proven shared resolver out of `rotate`:

- **NEW `locations.shared_sessions_dir(root)`** — the common-root room resolver (routes through `git_common_root` to the main checkout, re-derives the graph there; non-git/non-worktree root is the identity, so every fixture behaves byte-for-byte as before).
- **`rotate._sessions_dir` now delegates to it** — one implementation, so the plain join and the shared resolver can never disagree (the round invited exactly this hoist).
- **`locations.sessions_dir` kept as the PER-WORKTREE join, now explicitly documented** as such (it is what iteration output wants) — no longer silently claiming to be the shared room.
- Re-routed the named shared faces through `shared_sessions_dir`: `send._inbox_dir` (THE mail), `mail_alert._inbox_unread` (via `send._inbox_path`), `viewport._seat_sessions` (meter pins), `hierarchy.seat_sessions_dir` (meter pins), `grid.py:758` `.grid.lock` (grid `--all` serializes SHARED refs, so its flock must be one across worktrees).

**G4 verified on the real tree:** from THIS seat worktree, `shared_sessions_dir(wt/.agi)` == `/home/ubuntu/work/agi/.agi/sessions` (the MAIN room) while `sessions_dir(wt/.agi)` correctly stays worktree-local — the fork honored for iteration, the room shared for pins/mail.

**W4 — successor's first reply, measured, settles YES.** The predecessor's read-back and the successor's `--debug-file` are now the SAME shared file: `spawn_window` defaults its successor log to `_sessions_dir(root)/<name>.log` and `rotate_self` polls that exact path (`:1340`), so a successor first reply cannot be stranded in a file the predecessor cannot see — even when the rotation is driven from a linked worktree. New falsifier asserts path equality from both worktree and main (`_make_main_and_worktree` fixture) plus that the shared log is on the MAIN checkout. Both sides of a rotation now resolve the one `<name>.log`.

**W1 + G5 — every sessions-dir consumer, by the directory addressed (both the `root/"sessions"` join and the `.agi/sessions/...` relative form):** see the full classification table in Evidence.

**Struggles recorded in-line:** the legacy send fixtures passed a malformed root (a `.agi/config.json` project marker alongside sessions written at the legacy `root/sessions`), so shared routing sent the inbox to `.agi/sessions` and 10 path expectations broke; each was updated to assert the G11 shared room explicitly rather than the old legacy assumption (the round's rule: a changed test asserts the corrected fact).

## Evidence

**Full engine suite: 2310 passed, 1 skipped** (explicit per-file list — kid tier refuses a bare dir run). Touched modules re-run individually green: locations, rotate, send, viewport, hierarchy, mail_alert, grid, metrics, workflow, verification, provisioning, dispatch, cli, failures, heal.

New/updated falsifier tests (all green):
- `test_locations::test_shared_sessions_dir_resolves_main_room_from_worktree` (g4 — shared routes to main checkout; per-worktree `sessions_dir` keeps the fork)
- `test_locations::test_shared_sessions_dir_is_identity_in_main_checkout` (g4 — non-worktree is the identity)
- `test_send::test_inbox_dir_resolves_to_main_from_a_linked_worktree` (g4 inbox face — ONE mail room)
- `test_rotate::test_successor_reply_lands_in_the_file_the_predecessor_reads` (w4 — path equality from worktree and main, on the MAIN checkout)

**Full consumer enumeration + classification (g5; "unexamined = fail", "<10 need change = fine"):**

SHARED-ROOM (must be ONE across worktrees) — through `shared_sessions_dir`/`_sessions_dir`:
1. meter pins `*.meter` — rotate (pre-round), **viewport:686, hierarchy:104 (this round)**. Seat readable from any tree.
2. mail inbox `sessions/inbox/` — **send:123, mail_alert:73 (this round)**. Recipient sees mail whatever tree wrote it.
3. suite stamp `verify-suite-ts.json` — verification `_suite_ts_path` (prior kid). `bin-suite-fresh` must see the prime's suite from any seat.
4. rotation records `sessions/rotations/` — rotate `_write_rotation_record` (via `_sessions_dir`).
5. debug/readback logs `<name>.log` — rotate four defaults + read-back (prior kid, w2). w4 proves both sides share.
6. budget `.spawn-budget` — spawn_budget.budget_dir (already re-roots via `git_common_root`). Correct as-is.
7. spend captures `.spend-captures` — provisioning `_captures_dir` (already re-roots). Correct as-is.
8. grid lock `.grid.lock` — **grid.py:758 (this round)**. `--all` serializes SHARED refs; flock must be one.
9. workflows jsonl — workflow `_track_run:464` (already `shared_project_root`). Correct as-is.

LEGITIMATELY PER-WORKTREE (iteration output, forked during a run, merged home) — SEPARATE from the boundary:
10. iteration dirs `sessions/iter-*` — `locations.iteration_dir` + dispatch:1165 / cli:1082 / heal:78,173 / post_wire:347 / zoom:483 / failures:113,266 / `list_iterations`/`claim_iteration`. A seat's session is forked in its own worktree during a run; `cli.py session-complete:1520,1532` and `rotate complete:1639-1640` merge worktree→main at retirement. This is the design, NOT the boundary — `iteration_dir` stays on the per-worktree join.
11. viewport.iteration_points:573 / agents_of_iteration:588 / `_manifest_agents:649` — read the CURRENT tree's iter dirs for the live axis. Same per-worktree rule.
12. glitch_master `_out_dir:57` (`.agi/sessions/iter-../review`) — per-worktree review drop-point, but 🔴 FLAGGED: `--root` is the GRAPH root so `.agi/sessions` DOUBLES `.agi` in G11 (`<repo>/.agi/.agi/sessions`) — latent standalone-tool bug; outside this round's file scope (envfile/verification/provisioning/rotate), not changed.

STANDALONE / legacy / cwd-relative (not the loop's shared room):
13. plan_master:34 `DEFAULT_LOG=".agi/sessions/..."` — cwd-relative standalone constant.
14. unify.py:763 `"sessions/": ".agi/sessions/"` — legacy path-rewrite mapping.
15. analyze-chat-structure.py:19 — SESSIONS_DIR from the engine path, standalone analysis.
16. verification.py:166 state-file / :238 suite lock — per-run bookkeeping (the suite STAMP is what gates, and it is shared via `_suite_ts_path`).
17. success_metrics:59,75,163 (write-log / success-metrics-N.json) — metrics source read with the caller's root; run read-only from main. Classification: shared-in-practice (metrics reflect the whole tree); NOT re-routed this round (no worktree writer), recorded as a candidate.

Aligned with the round: only the meter-pin/inbox/suite-stamp/budget/rotation faces were ever named shared — the triage concludes exactly those plus the grid lock need the shared room, and iteration output legitimately does not. Ten-odd sites examined; far fewer needed changing; every consumer is now classified with its reason.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-bb0994fd, L4.103) — ACCEPTED at inconclusive_lean_proved:70. What the instruction said: finish w1/w4/g4/g5 — enumerate sessions-dir consumers BY DIRECTORY ADDRESSED, classify each, fix or remove locations.sessions_dir, measure the successor-reply path. What the machine actually does, verified by me in this worktree: locations.py:602 defines shared_sessions_dir routing through git_common_root with non-git identity; rotate._sessions_dir delegates to it (one implementation, no divergence possible); send.py:129, grid.py:762, viewport.py:686, hierarchy.py:110 route the inbox/lock/pin faces through it; sessions_dir is kept as the per-worktree join with an honest docstring, and iteration_dir deliberately builds on it because iter-* output is forked-then-merged (cli.py session-complete, rotate complete) — the classification the round demanded. The near miss I checked for: a hoist that made ALL of sessions shared and broke iteration-output merging, or a fix that greens seats by weakening the freshness judgement — neither; the judgement is untouched and I ran the FULL engine suite myself as parent tier: 2542 passed, 1 skipped, no edited judgement. Why lean and not proved: success_metrics is classified shared-in-practice but NOT re-routed (candidate), and glitch_master's doubled-.agi latent bug is flagged but out of file scope — both recorded honestly rather than silently; the remaining residue is small and named. Note the kid also broke 10 legacy send fixtures and repaired each to assert the corrected shared room, which is within the round's edited-test rule.
<!-- THOUGHT:END -->

## Agent Notes
Completion pass: g4 hoisted shared_sessions_dir into locations (rotate delegates), re-routed shared faces (send/mail_alert inbox, viewport/hierarchy pins, grid lock); w1+g5 full sessions-dir enumeration+classification (shared vs' per-worktree-iteration); w4 successor-reply measured YES (both sides now one shared <name>.log). Full suite 2310 passed.

Parent review accepted: shared_sessions_dir hoist + delegation verified, all shared faces re-routed, per-worktree iteration fork deliberately preserved, w4 falsifier green, full suite 2542 passed re-run by parent. Lean 70 not proved: success_metrics candidate re-route and glitch_master doubled-.agi bug recorded as flagged residue, out of round scope.
