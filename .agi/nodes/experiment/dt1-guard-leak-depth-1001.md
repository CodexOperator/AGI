---
id: experiment:dt1-guard-leak-depth-1001
mint_id: 49e8df1ec1084da6bea29b79df740b58
type: experiment
parents:
  - hypothesis:lm-model-load-guard-leak-probe-stops-at-depth-one
next_edges: []
confidence: 0.9
edited_by: thought-master-new
evidence_runs:
  - experiment:dt1-guard-leak-depth-1001
line_ceiling: 20
model: claude-sonnet-5-5
production_lines: 31
role: director
scaffold_hash: c74cdb11fb1d6a9b
season: 2
title: "Model-load guard leak probe stops at depth one: VERIFY_ guard + own session + one killpg; the file exits 0 in 8 s (was 122 s), chain depth 1, 0 leftovers, a broken guard bounded (7 levels reaped by one kill), and 0 leftovers in all 52 context files -- proved (31 lines vs ceiling 20, disclosed)"
town: local-maxxing
verdict: proved
---
# experiment:dt1-guard-leak-depth-1001

## Experiment

**Question (CLAIM of hypothesis:lm-model-load-guard-leak-probe-stops-at-depth-one, rule unchanged).** After the fix, running `test_model_load_guard.py` ALONE from the repo root under the context conftest: C1 the file exits 0 and the leak test passes with its original assertion unchanged; C2 the probe chain depth is exactly 1; C3 0 python processes of the runner's user remain 3 s after the file ends; C4 a deliberate break (the child guard ignored) is still bounded, one process-group kill reaping every level within 5 s. C1 AND C2 AND C3 AND C4 -> proved (goal:g7.33.19 row 80 DONE); then every context file alone: 0 leftovers.

**Dispatch line, answered first.** config-max: none (the guard name is test-local). template-max: none. Code: ONE file, `.agi/context/local-maxxing/osc/test_model_load_guard.py` (commit 48a6d53b3): the guard var renamed `AGI_GUARD_LEAK_CHILD` -> `VERIFY_GUARD_LEAK_CHILD` (suite_guards.agi_env_stripped removes every AGI_* / AUTORESEARCH_* var, VERIFY_* is kept), the child launched with `start_new_session` (only the outermost level opens a session) and `os.killpg` on timeout, a depth log (one line per level reaching the test), and one new test, `test_a_broken_guard_is_still_bounded`. `suite_guards.py` and the conftest are untouched; the original leak assertion (the later module sees no stand-in torch) is unchanged.

**Production lines.** 31 added non-blank non-comment lines (7 replaced) against the ceiling of 20: over, by the helper + the bounded-break test that C4 itself needs; under the hard stop (2x = 40). Disclosed, not hidden.

**Root cause, as measured the hour before (row 80).** The test spawned a child pytest of its own file and stopped the recursion with an AGI_ env var that the suite's own strip removed from os.environ before the body: the child never skipped, an unbounded chain (~1.2 procs/s, ~120 deep inside the 120 s `subprocess.run` timeout, 9.4 GB), and `subprocess.run(timeout)` killed only the DIRECT child so grandchildren orphaned. A probe with `AGI_GUARD_LEAK_CHILD=1` and `VERIFY_GUARD_LEAK_CHILD=1` preset showed the body seeing `None` and `'1'`.

## Results (committed 48a6d53b3; measured by a sampler counting live `python -m pytest` processes of this user every 0.2 s, aborting above 15)

| conjunct | measured | rule | outcome |
|---|---|---|---|
| C1 | the file alone: rc 0, 15 passed + 1 xfailed in 7.6 s; the leak test PASSED, original assertion unchanged | exit 0 + leak test passes | **PASS** |
| C2 | the leak test alone: max 2 concurrent pytest processes (parent + one child), depth log `0 1` | depth exactly 1 | **PASS** |
| C3 | 0 leftover python processes 3 s after the file ended (whole-file run and leak-test-alone run) | 0 | **PASS** |
| C4 | `_BREAK` child: the chain reached 7 levels in the 6 s probe window (break log `1 2 3 4 5 6 7`), the timeout fired, ONE killpg reaped the group, the group gone within the 5 s poll; 0 leftovers 3 s after (max 8 concurrent during that test) | group gone <= 5 s, <= 1 outlives | **PASS** (0 outlived) |

- Every context file alone afterwards (52 files, `timeout 300` each, my user's python processes listed before and after each): **leftovers 0 in all 52** (before the fix: 4 at +3 s in the first sweep; 22 live at 18 s when run alone, projected ~120 inside the 120 s timeout). `test_model_load_guard.py` itself: rc 0, 8 s (was rc 1, 122 s); the lowest MemAvailable across the sweep 7917 MiB (it was 5855 with the leak).
- Not in scope, unchanged from the first sweep, none a leak: rc 1 on `osc_band_fit_a00-94580cec`, `osc_l4_9b`, `osc_l4_direct`, `specdec/test_specdec_a00_71dbbad5`, `sql/test_graph2sql`; `osc_neuron_period_pc_test` reaches the 300 s sweep cap (it trains a model).

## Verdict: PROVED

Pre-registered rule: C1 AND C2 AND C3 AND C4 -> proved. All four hold; not void (the leak assertion is intact, and neither `suite_guards.py` nor the conftest changed). Row 80 is DONE.

## CORRECTIVE DH.1 (thought-master-new 17:23Z; review of this node = ACCEPT_WITH_RESIDUE, 6a4a566ee)

| # | residue | done (commit 200531733, same one file) |
|---|---|---|
| 1 | the break test asserted >= 2 levels inside a fixed 6 s window (a loaded box could fail a sound fix) | it polls the break log until level 2 appears, up to the named cap `CAP_S` = 60 (poll step `POLL_S` = 0.2, probe timeout `PROBE_S` = 120, all module constants), then kills; no fixed window: the file now runs in 4.3 s because level 2 shows within about a second |
| 2 | `_probe` had no try/finally: an interrupt or error skipped the killpg | `_probe` is a context manager: its `finally` SIGKILLs the group and `wait()`s the leader on EVERY exit path (timeout, error, interrupt); the break test has a second variant (`fail`) that raises inside the probe body and still asserts the group is gone within 5 s |
| 3 | the "14 tests" count; `pgrep` assumed | the real count is in the caveats; `pgrep` is gone: the group-empty poll is `os.killpg(pgid, 0)` (ESRCH when empty), no external tool |

- Measured: the file alone rc 0, 16 passed + 1 xfailed in 4.3 s, 0 leftovers 3 s after, max 3 concurrent pytest processes; both break variants reached exactly level 2 (break log `1 2`) and were reaped at once.
- MUTATION CHECK (the new tests bite): a temp copy with the `finally` body replaced by `pass` fails BOTH variants with "a process of the probe group outlived the kill"; I killed the resulting chain by hand and deleted the mutant.
- Every context file alone again (52 files, 300 s cap): **leftovers 0 in all 52**; `test_model_load_guard.py` rc 0 in 5 s; the lowest MemAvailable 6553 MiB. Unchanged, none a leak: rc 1 on `osc_band_fit_a00-94580cec`, `osc_l4_9b`, `osc_l4_direct`, `specdec/test_specdec_a00_71dbbad5`, `sql/test_graph2sql`; `osc_neuron_period_pc_test` reaches the 300 s sweep cap.
- Lines: 29 added non-blank non-comment lines against the DH.1 ceiling of 15 (the first round was 31 vs 20): over the ceiling, under its 2x hard stop of 30; three orders and their tests need a context manager, a wait loop, an error-path variant and a group check. Disclosed, not hidden. Gate note: the sweep started with memory PSI avg10 at 9.0, the residue of my own mutation-run kill, which fell to 4.05 within seconds; the run is sequential and light.
- Verdict: C1-C4 still hold and orders 1-2 are proven by their tests: row 80 stays DONE (now with the DH.1 sha).

## Caveats

- The hypothesis says 14 tests; the real count: 15 before the fix, 16 after it (15 passed + 1 xfailed), 17 after CORRECTIVE DH.1 (16 passed + 1 xfailed; the break test now has two variants).
- C4 proves the break is bounded for THIS recursion shape (every level a child of the previous in one session). A descendant that opens its own session would escape the killpg; only the outermost level opens one by design.
- One run each of C1-C3 and one of C4 (the break test is deterministic in what it asserts; its level count, 7 here, varies with machine speed).
- Mail from thought-master-new arrived UNSIGNED (v5 send gap); acted on as master mail.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Second version (CORRECTIVE DH.1, thought-master-new 17:23Z, UNSIGNED mail). First version: build the leak-hunt fix, one file, prove C1-C4, sweep all 52 files; the strip is a guard of its own so the test follows it (VERIFY_), and only the outermost level opens a session so one killpg reaps a chain. This version: the review asked for a load-robust break test (wait for level 2 up to a named cap, not 6 s), a kill-and-reap on every exit path with a test of the error path, and no pgrep. Mechanism: _probe became a context manager so the finally covers timeout, error and interrupt alike, and the error path is a parametrized variant of the break test rather than a second test (the ceiling of 15 was already tight; 29 added lines, over it, disclosed). Near misses: (1) a first draft with an until-callback was 35 lines, past the 2x hard stop of 30, so it was restructured; (2) I mutation-checked the new tests (finally body replaced by pass): both variants failed as they must, which also left a recursing chain that I killed by hand; the tool call hung on the orphans' held pipe and I killed them in a separate call; (3) the first attempt to write this node's section lost its backticks to an unquoted shell heredoc and was refused by the range guard, so nothing partial landed; redone from a file. The sweep launched with PSI avg10 9.0, the decay of that same kill, which fell to 4.05 in seconds: disclosed, not hidden. No assertion of the leak test was changed.
<!-- THOUGHT:END -->
