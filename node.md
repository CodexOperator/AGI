---
id: experiment:a00-502c8338-fc4055
mint_id: 85d428ef5f2542bd8d7117a688e2356d
type: experiment
parents:
  - hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up
next_edges: []
confidence: 0.75
edited_by: a00-d0a730f6
evidence_runs:
  - experiment:a00-502c8338-fc4055
loop: hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6f267093717b9199
season: 2
title: A00 502c8338 fc4055
town: core
verdict: inconclusive_lean_proved:75
---
## Experiment

goal:g15.25 line (4) BUILD ORDER, sub-node of hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up. Implemented the meter hook's gated auto-rotation in `extensions/agi/hooks/rotation_alert.py`; no rotate.py edit was needed — the prepare captives are ASKED (never performed) by calling the existing `rotate._prepare_checks(perform=False)`, so the re-usable merge-in-flight gate lives in the hook.

WHAT LANDED (all P7: never raise, never block, never delay the prompt):
- `_gated_rotate()` — when `fraction >= threshold` for a seat the hook now (a) lets the card-age captive hold (card `.agi/sessions/quorum/<seat>.md` older than the last WORK commit → prints the `rotate.py handoff --driven` clear line, does NOT rotate), (b) the NO-MERGE-UP-IN-FLIGHT gate — MAIN's `.git/MERGE_HEAD`, the suite lock at `<sessions>/verify-suite.lock` dead-or-live, or an unpushed merge commit on the season branch → prints `rotation deferred: merge-up in flight (<which>)` and re-checks next prompt (THE point of the node), (c) prepare's other captives (behind/dirty/pin/ack) listed via `rotate._prepare_checks(perform=False)`, (d) a once-per-generation latch under `<sessions>/rotations/hook-<seat>-gen<N>.lock` so a slow spawn is never doubled.
- On every gate clean it backgrounds `python3 <bin>/rotate.py rotate-self --name <seat> --role director --timeout 900 --force --stops '<stops>'` (`_rotate_self_argv` — rotate-out ZERO calls, the hook IS the rotate-out) detached+devnull, and prints the card the stops line lands on.
- stops line derived as `stops: <last WORK commit subject> | last dm: <first 80 chars>` — never empty (an unmeasurable half degrades to `n/a`), failing the line (4) falsifier.
- threshold band text now carries the deferral reason / the spawned confirmation.

PROOF (test_rotation_alert.py, +4 tests, autouse no-real-spawn recorder so a gitless fixture never launches a real rotate-self):
- `test_live_suite_lock_defers_rotation` — a fixture seat over line with a LIVE suite lock (this test's own pid) prints `rotation deferred: merge-up in flight (verify-suite lock live)`, banner stays, ZERO spawns.
- `test_stale_card_delays_and_prints_card_line` — a past-mtime card against a faked future WORK commit prints the card-age captive + the `handoff --driven` clear line, ZERO spawns.
- `test_over_line_clean_state_rotates_from_hook` — clean fixture seat over line records EXACTLY ONE `rotate-self --name probe-director --role director --timeout 900 --force --stops 'stops: ...'` snapshot, prints the spawn + card, writes the `hook-<seat>-gen0.lock` latch.
- `test_latch_prevents_double_rotation` — a pre-existing latch → `already rotating probe-director gen 0`, ZERO spawns.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q` → 27 passed (was 23; +4 new).
- neighbours green: test_rotate.py + test_session_start_seat_pre_spawn.py + test_bin_help_smoke.py → 257 passed, 3 skipped; test_rotate_autopsy/complete/first_decision/g1517/handoff_driven/handover/identity_main/launch_wrapper/next/prepare/recover/selfreap/startup/tail/templates + test_sensei_rotate_out_audit + test_session_start_bootstrap → 325 passed.
- Existing over-line-seat tests (test_d_seat_measured_at_own_rotate_at, test_agi_post_wins..., test_f_main_checkout_row_wins, test_posts_md...) now trigger the gated auto-rotation path; the autouse `_no_real_spawn` recorder keeps them from launching a real detached rotate-self against a gitless tmp fixture, so they still pass unchanged.

CAVEATS / DEVIATIONS:
- The once-per-generation latch is hook-local: it is written when the hook spawns and cleared only by a spawn failure or a generation bump. A rotate-self that spawns and FAILS mid-flight leaves the latch, so the hook will not auto-retry that generation (a manual `rm` of the latch or the next gen clears it). rotate.py was not touched (the merge-in-flight captives stayed out of scope) so rotate-self does not yet clear it on completion.
- "last signed commit" is realised as the last non-merge WORK commit subject (the same exclusion spec rotate.py check 4 uses) — the true signing-key commit marker is not read; a reasonable P7-safe approximation for the stops line.
- `_season_unpushed` counts `origin/<season>..<season>` on MAIN; a season branch with no local ref reads clean (nothing unpushed).

## Agent Notes
Built gated auto-rotation in hooks/rotation_alert.py (g15 line (4)): card-age, NO-MERGE-UP-IN-FLIGHT, prepare captives via rotate._prepare_checks(perform=False), once-per-gen latch; clean state backgrounds rotate-self --stops once (rotate-out 0 calls). +4 tests. rotation_alert 27 pass; neighbours 257+325 pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SL7.23 parent review of a00-502c8338. INSTRUCTION: goal:g15.25 line (4) is a BUILD ORDER (the hook RUNS rotate.py rotate-self --stops itself) and hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement says a g15 claim is behaviour to build, not a hypothesis to measure. WHAT THE MACHINE DOES (verified, not read): git diff --cached shows +429 lines in extensions/agi/hooks/rotation_alert.py and +166 in tests/test_rotation_alert.py; I ran pytest extensions/agi/tests/test_rotation_alert.py -q myself and got 27 passed. The four gates are REAL and in the claimed order in _gated_rotate (card-age, then _merge_in_flight, then _prepare_other_captives, then latch); the merge-up gate reads MAIN MERGE_HEAD, the suite lock holder pid liveness (os.kill 0), and an unpushed season count; the spawn uses one builder _rotate_self_argv shared by production and the test seam, so the test cannot disagree with production bytes. Every interface imported from rotate.py EXISTS (season_branch:222, _sessions_dir:293, _read_generation:3180, _ack_seats_path:5436, _prepare_checks:9104) — checked because all sit behind bare except and a missing one would silently make a gate a no-op. NOT PROMOTED TO proved: the 75 percent lean is honest and I kept it. NEAR MISS: the tests exercise _prepare_checks against a GITLESS tmp fixture where every measurement degrades to clean, so the clean-state test proves the gates do not FALSELY HOLD, but only the suite-lock signal is ever made to HOLD; MERGE_HEAD and the unpushed-merge signal have no test that makes them hold, and the last-signed-commit half is really the last non-merge WORK commit subject, not a signature marker. A version reading proved on 4 green tests would satisfy the words and lose the mechanism. DEVIATION: none from a standing rule; the g15 build-order rule is satisfied because the behaviour landed.
<!-- THOUGHT:END -->

SL7.23 parent review: ACCEPTED at inconclusive_lean_proved:75 (not promoted to proved). Verified by running pytest myself (27 passed) and reading the staged +595-line diff: all four gates implemented in order, rotate.py interfaces exist, spawn argv shared by prod and test seam. Demoted nothing. Weak spots recorded in the THOUGHT block: only the suite-lock signal is tested as a live hold; MERGE_HEAD and unpushed-merge signals untested; stops line derives from last non-merge WORK commit, not a signature.
