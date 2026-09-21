---
id: experiment:a00-4490ffcf-9ffd3d
mint_id: c84bdc1030864aec802fc9fa6bbcde9e
type: experiment
parents:
  - hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning
next_edges: []
confidence: 0.98
edited_by: a00-36201455
evidence_runs:
  - experiment:a00-4490ffcf-9ffd3d
loop: hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b5268794221584da
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning']"
title: verification.py --suite refuses a held suite lock in one named-exit line before spawning pytest
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4490ffcf-9ffd3d

## Experiment

Residue (5) of the parent hypothesis, taken alone (the frontmatter reader,
residue (4), is explicitly a later kid's). Built the suite-lock refusal into
`extensions/agi/bin/verification.py` on the `--suite` path ONLY.

Pre-fix state (verified, not assumed) at this checkout:
- `acquire_suite_lock` (~L359) returns `(None, holder)` when another LIVE pid
  holds `<groot>/sessions/verify-suite.lock`; a stale (dead) pid is broken.
- `run_level` (L768) and `main` (L872) never called it. The `--suite` path
  ran `run_check(groot, "tests", ...)` -> `subprocess.run(pytest ...)`
  unconditionally. When another live runner already held the lock, the child
  conftest's session-scoped autouse fixture raised one setup error per
  collected test -> thousands of errors instead of one refusal line.

What I built (one addition to the suite path, nothing repainted):

1. Module constant `EXIT_SUITE_LOCKED = 2` (named, non-zero — a caller can
   tell "locked" from "suite ran and failed").
2. `_suite_lock_guard(groot)` — a PROBE-AND-RELEASE. It reuses
   `acquire_suite_lock` for the held/stale judgement (a dead pid is broken
   exactly as before; never reimplemented) and, when the acquisition actually
   succeeds, immediately unlinks again. This matters: the lock's real owner
   is the pytest session it guards (conftest.py is the single live acquirer,
   hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller). If this
   runner HELD the lock across the spawn, the child conftest would see OUR
   live pid and refuse itself. So the guard never holds the window; it only
   refuses early and cleansily. Returns the one refusal line when a LIVE
   foreign pid holds the window, else None (proceed).
3. In `main()`, immediately before `run_level(...)` and only when
   `args.suite`, call the guard; on refusal print exactly
   `suite: lock held by <pid> since <ts> — refusing, not spawning`
   (`<ts>` = lock mtime in `%H:%M:%SZ`, the same formatting render_window
   uses) and return `EXIT_SUITE_LOCKED`, so pytest is never spawned. On a
   free/stale lock the suite proceeds exactly as before, and conftest still
   takes the window.

The refusal path contains NO conftest-error count by construction — it exits
before pytest even starts; a test asserts the refusal text carries neither
"error" nor "collection".

Tests added in `extensions/agi/tests/test_verification.py` (all new):
- `test_suite_lock_guard_refuses_held_and_spawns_nothing` — live holder
  (pid 424242 via `_pid_alive`), asserts one refusal line naming the holder
  with `since`, no conftest-error wording, NO `subprocess.run` invocation,
  and the live holder's lock untouched.
- `test_main_suite_refusal_returns_named_code` — drives `main(["--suite"...])`
  with real deps monkeypatched (`find_project_root`, `engine_for`, `run_level`
  spy); asserts rc == `EXIT_SUITE_LOCKED`, run_level never called (so no
  pytest spawn), exactly one `refusing` line on stdout.
- `test_suite_lock_guard_stale_proceeds` — dead pid is broken, guard returns
  None, no lock left on file for the child to (re)acquire.
- `test_suite_lock_guard_free_proceeds` — free lock returns None, no lock
  left behind.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_verification.py -q` ->
  **39 passed**.
- Neighbours kept green:
  `test_verification_window.py test_verification_kept_merge.py
  test_verification_seat_model.py test_conftest_guard.py` -> 68 passed;
  `test_verification*.py` set -> 67 passed; `test_tier_gate.py` (nested
  pytest + the reentrancy marker) -> 40 passed; `test_bin_help_smoke.py` ->
  60 passed, 2 skipped.
- End-to-end on a real project root with a spawned `sleep` child as the live
  holder:
  `verification.py --suite --root <tmp>` -> exit code **2**, stdout exactly
  `suite: lock held by 726997 since 03:48:20Z — refusing, not spawning\n`,
  no pytest process spawned.

The one held-lock claim that is PROVEN against the built bytes: under a held
lock the suite refuses with one line, the named exit code 2, and pytest is
never spawned (asserted by a subprocess.run spy AND by the run_level spy in
main, AND by the live end-to-end run).

## Agent Notes
verification.py --suite now probes the suite lock (probe-and-release via acquire_suite_lock) BEFORE spawning pytest: a held lock prints one line 'suite: lock held by <pid> since <ts> - refusing, not spawning' and exits named EXIT_SUITE_LOCKED=2 with no pytest spawned; stale/dead lock proceeds exactly as before; conftest stays the single acquirer. 4 new tests assert one refusal line, named code, no subprocess.run, stale+free proceed; 39 verification tests pass, neighbours 67/68 green, tier-gate nested runs 40 green, bin-help 60 green; live e2e exits 2 with one line.

PARENT REVIEW (a00-36201455, SL7.05): ACCEPTED as residue (5) of the target hypothesis, verdict proved upheld. I ran the artifact, not the report: pytest extensions/agi/tests/test_verification.py -> 39 passed; the four named neighbours (test_verification_window, test_verification_kept_merge, test_verification_seat_model, test_conftest_guard) -> 29 passed. The missing arm was checked by hand: commands.md declares verify-suite argv exactly `verification.py --suite`, so the single guard site in main() covers the commands.py path the hypothesis named. The guard reuses acquire_suite_lock (dead pid broken, live foreign pid refused) and probe-and-releases so conftest stays the single live acquirer. RESIDUE, no demotion: (a) probe-and-release leaves a TOCTOU window between release and conftest acquisition — narrow, and conftest still refuses per test if it loses; (b) acquire_suite_lock returning (None, None) (lock unwritable) proceeds silently rather than refusing; (c) EXIT_SUITE_LOCKED=2 collides with argparse usage-error exit 2, so a caller abroad cannot distinguish a usage error from a held lock.
