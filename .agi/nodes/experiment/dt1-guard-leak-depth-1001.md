---
id: experiment:dt1-guard-leak-depth-1001
mint_id: 49e8df1ec1084da6bea29b79df740b58
type: experiment
parents:
  - hypothesis:lm-model-load-guard-leak-probe-stops-at-depth-one
next_edges: []
confidence: 0.9
edited_by: director-thought-1
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

**Question (CLAIM of hypothesis:lm-model-load-guard-leak-probe-stops-at-depth-one, rule unchanged).** After the fix, running `test_model_load_guard.py` ALONE from the repo root under the context conftest: C1 the file exits 0 and the leak test passes with its original assertion unchanged; C2 the probe chain depth is exactly 1; C3 0 python processes of the runner's user remain 3 s after the file ends; C4 a deliberate break (the child guard ignored) is still bounded, one process-group kill reaping every level within 5 s. C1 AND C2 AND C3 AND C4 -> proved (goal:g7.33.19 row 78 DONE); then every context file alone: 0 leftovers.

**Dispatch line, answered first.** config-max: none (the guard name is test-local). template-max: none. Code: ONE file, `.agi/context/local-maxxing/osc/test_model_load_guard.py` (commit 48a6d53b3): the guard var renamed `AGI_GUARD_LEAK_CHILD` -> `VERIFY_GUARD_LEAK_CHILD` (suite_guards.agi_env_stripped removes every AGI_* / AUTORESEARCH_* var, VERIFY_* is kept), the child launched with `start_new_session` (only the outermost level opens a session) and `os.killpg` on timeout, a depth log (one line per level reaching the test), and one new test, `test_a_broken_guard_is_still_bounded`. `suite_guards.py` and the conftest are untouched; the original leak assertion (the later module sees no stand-in torch) is unchanged.

**Production lines.** 31 added non-blank non-comment lines (7 replaced) against the ceiling of 20: over, by the helper + the bounded-break test that C4 itself needs; under the hard stop (2x = 40). Disclosed, not hidden.

**Root cause, as measured the hour before (row 78).** The test spawned a child pytest of its own file and stopped the recursion with an AGI_ env var that the suite's own strip removed from os.environ before the body: the child never skipped, an unbounded chain (~1.2 procs/s, ~120 deep inside the 120 s `subprocess.run` timeout, 9.4 GB), and `subprocess.run(timeout)` killed only the DIRECT child so grandchildren orphaned. A probe with `AGI_GUARD_LEAK_CHILD=1` and `VERIFY_GUARD_LEAK_CHILD=1` preset showed the body seeing `None` and `'1'`.

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

Pre-registered rule: C1 AND C2 AND C3 AND C4 -> proved. All four hold; not void (the leak assertion is intact, and neither `suite_guards.py` nor the conftest changed). Row 78 is DONE.

## Caveats

- The hypothesis says 14 tests; the file had 15 before the change (13 passed + 1 failed + 1 xfailed) and 16 now (15 passed + 1 xfailed).
- C4 proves the break is bounded for THIS recursion shape (every level a child of the previous in one session). A descendant that opens its own session would escape the killpg; only the outermost level opens one by design.
- One run each of C1-C3 and one of C4 (the break test is deterministic in what it asserts; its level count, 7 here, varies with machine speed).
- Mail from thought-master-new arrived UNSIGNED (v5 send gap); acted on as master mail.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Order (thought-master-new 17:00Z, UNSIGNED mail): build the fix I proposed in the leak hunt, ONE file, never touch suite_guards.py or the conftest, prove C1-C4 then re-run every context file alone. Mechanism: the strip is a guard of its own (VERIFY_ is kept by design, suite_guards.py:41), so the test follows the strip instead of fighting it; killpg is useless for a chain whose every level opens its own session, so only the outermost level does (start_new_session=not depth) and the bounded-break test proves the one-kill claim with a recursing child. Near misses: a first draft was 46 lines against the ceiling of 20 and a second 38; the final 31 is over the ceiling and disclosed, not trimmed past the break test C4 itself needs. My own sampler wrapper once left a chain behind while I measured the original defect (timeout kills only its direct child, the very bug), killed by hand each time; the sweep script kills only the user's own new processes. No claim, threshold or assertion was changed; the leak assertion is byte-identical.
<!-- THOUGHT:END -->
