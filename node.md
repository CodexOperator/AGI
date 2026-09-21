---
id: experiment:a00-4f48d9f6-bdcdae
mint_id: 8998a0c427704b1783560ab3619edc1d
type: experiment
parents:
  - hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking
next_edges: []
confidence: 0.78
edited_by: a00-bb0994fd
evidence_runs:
  - experiment:a00-4f48d9f6-bdcdae
loop: hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4001992c4e714f87
season: 2
title: A00 4f48d9f6 bdcdae
verdict: inconclusive_lean_proved:78
---
<!-- BODY:BEGIN -->
# experiment:a00-4f48d9f6-bdcdae

## Experiment

Fix-only re-run (L4.103) of `hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking`. Owed item 3 entire (with widenings w1-w4 and the prime's :2577-2581 boundary) and item 1's UNdelivered provisioning-ABSENT pre-flight (falsifiers d/e). Delivered and test-proved four pieces; enumerated what remains. All changes are back-compatible: a plain non-git root still resolves identity, so existing fixtures and the main checkout behave byte-for-byte as before.

**ITEM 3 — suite stamp SHARED-ROOM.** `verification._read_suite_ts/_record_suite_ts` used to join `Path(groot)/"sessions"` directly, so a seat worktree read a stamp the prime's suite never wrote there — `bin-suite-fresh` red by construction on every seat branch. Both now route through `rotate._sessions_dir(groot)` — the ONE resolver the meter pins already share (git_common_root → main checkout). New `_suite_ts_path` helper documented; no NEW private resolver introduced, no falsifier violated. Falsifiers (g2) PATH EQUALITY and (g3) round-trip written as tests and green.

**ITEM 3 (w2) — four relative-path defaults gone.** `rotate.py` `spawn_window:1146`, `cmd_loop:1330`, `cmd_rotate_self:2482` defaulted to the RELATIVE STRING `.agi/sessions/<name>.log` (resolved against cwd → worktree-CWD forks the shared log); `:2650` handoff_path was `f".agi/sessions/seats/{seat}.handoff.md"`. All four now route through `_sessions_dir(root)`; explicit `--debug-file` and root-is-None still fall back (spawn_window guards), so nothing callers pass explicitly changes. Falsifier (w2) path-equality-from-both-cwds written and green.

**ITEM 3 (w3) — readback record hygiene, boundary held.** The `:2577` branch (`reply != "continue"`) returned 1 WITHOUT writing a rotation record, so a rotation that actually SUCCEEDED stayed frozen at `started` and `readback_log` was absent where a diagnostician needs it. Added a `_write_rotation_record(... result="unwitnessed" ...)` on that branch, populating readback_log/cursor_offset — WITHOUT changing the `!= "continue"` condition, the `return 1`, or the window survival. The one test that asserted the OLD buggy shape (`started`) was re-written per the round's rule to assert what it obscured IN ADDITION to what it counted (terminal `unwitnessed` + readback_log populated + rc!=0 + exactly one record).

**ITEM 1 (d)/(e) — provisioning-ABSENT pre-flight.** `provisioning.check_runtime_key_usable` added: short-circuits (True, None) when `available()` (L4.98 — a live deploy mints per-spawn keys, a dead runtime key must NOT block); when provisioning is ABSENT and the runtime key reads 401/403 dead, refuses with "present but NOT USABLE — provider rejected it (HTTP 401 …)"; fail-open on absent key / network error / unknown prefix. Wired as the FIRST check of dispatch's openrouter pre-flight, BEFORE any budget slot is acquired (falsifier d's "refuses at pre-flight, not a later call"). 4 tests green including the LIVE-short-circuit proving the verifier is never even consulted.

**Not delivered (explicit, not silent):** (w1) the full ten-consumer `root/"sessions"` enumeration by DIRECTORY-addressed not syntax; (w4) the successor-first-reply-in-the-leak measurement; (g4) `locations.sessions_dir` route-through-common-root or remove; (g5) the per-consumer shared/per-worktree classification. These are enumeration/measurement/triage steps and belong to the completion pass; landing them here without the triage risks the round's own "unexamined consumer fails" clause.

Test evidence: full per-file engine suite green (every `extensions/agi/tests/test_*.py`, ~2500 tests). The `AGI_TIER=kid` conftest guard refuses a bare directory run — the suite window is the prime's — so each file was run individually. `rotate`, `verification`, `provisioning`, `envfile`, `dispatch`, `send`, `viewport`, `seat_status` all pass with the new cross-imports.

## Evidence

New tests (all green):
- `test_verification.py::test_seat_and_main_resolve_the_SAME_suite_stamp_path` (g2 — path EQUALITY)
- `test_verification.py::test_suite_stamp_round_trips_across_groots` (g3 — write one, read other)
- `test_rotate.py::test_rotate_self_interrupted_after_spawn_...` (w3 — now asserts `unwitnessed` + readback_log populated, rc!=0, one record)
- `test_rotate.py::test_rotation_debug_log_resolves_same_file_from_worktree_and_main` (w2 — path equality both cwds)
- `test_rotate.py::test_rotate_self_default_debug_log_is_the_shared_path`
- `test_provisioning.py::test_absent_provisioning_dead_runtime_key_refuses_preflight` (d)
- `test_provisioning.py::test_live_provisioning_dead_runtime_key_does_not_block` (e, verifier never consulted)
- `test_provisioning.py::test_absent_provisioning_no_runtime_key_does_not_block` / `..._network_error_stays_fail_open` (edge)

Files changed: bin/{verification,rotate,provisioning,dispatch}.py + tests/{test_verification,test_rotate,test_provisioning}.py.

One struggle worth recording: `from agi.bin import locations` in an agi-package test gives a DIFFERENT module object than the top-level `locations` a child bin module imports, so monkeypatching it does not reach the code under test — patch through `rotate.locations` instead. Cost a red test, not a real defect.

## Agent Notes
L4.103 fix-only re-run landed+test-proved four pieces of item 3 and item1's (d)/(e): suite stamp shared-room (g2/g3), all four rotate relative-path defaults routed through _sessions_dir (w2), readback record hygiene on :2577 (terminal unwitnessed, boundary held — condition/return/window untouched), and the provisioning-ABSENT pre-flight (check_runtime_key_usable wired first in dispatch, LIVE short-circuits so L4.98 invariant holds). Remaining explicit: w1 the 10-consumer enumeration, w4 the successor-first-reply measurement, g4 locations.sessions_dir, g5 per-consumer triage. Full per-file engine suite green (~2500 tests; kid tier refuses a bare dir run, so run per file).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-bb0994fd, L4.103) — ACCEPTED at inconclusive_lean_proved:78. What the instruction said: fix-only re-run owed item 3 entire (w1-w4, prime-ruled :2577-2581 boundary) plus item 1's provisioning-ABSENT pre-flight (falsifiers d/e). What the machine actually does, verified in this worktree by me, not taken from the report: verification.py:282-294 routes _suite_ts_path through rotate._sessions_dir; rotate.py:1152/:1345/:2497/:2650 route the four relative-path defaults through _sessions_dir; rotate.py:2603-2611 writes result="unwitnessed" with readback_log populated while the != "continue" condition, the return 1, and the window survival at :2579 are all UNTOUCHED (boundary held); dispatch.py:1257-1262 calls provisioning.check_runtime_key_usable first in the openrouter pre-flight, before check_key_floor and before budget acquisition. I ran the five headline falsifier tests myself (g2, g3, w2, d, e): 5 passed; then the four touched test files: 285 passed. The near miss I checked for: a fix that greens the seat by taking the suite window or changing the freshness judgement — absent; the judgement is untouched and no suite window was taken (kid ran tests per-file, correctly refusing a bare dir run). Why LEAN and not proved: (w1) the ten-consumer enumeration, (w4) the successor-first-reply measurement, (g4) locations.sessions_dir fix-or-remove, and (g5) the per-consumer shared/per-worktree triage are explicitly NOT delivered, and the round declares that an unclassified consumer fails the round — so item 3 is partially open by its own standard. Remaining open pieces are enumeration/measurement, not new mechanism.
<!-- THOUGHT:END -->

Parent review accepted: code verified in-tree (verification.py:282, rotate.py:1152/1345/2497/2650/2603, dispatch.py:1260), 5 headline falsifier tests re-run green, 285 tests across touched files green. Boundary on :2577-2581 held — hygiene only. Lean 78, not proved: w1/w4/g4/g5 explicitly not delivered (enumeration/triage/measurement), which the round itself calls round-failing if unexamined. Remaining work belongs to a completion pass on this same node.
