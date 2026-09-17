---
id: experiment:a00-a3f2be5b-1ec18a
mint_id: b6676cf4eae542b09b2584b33d9629d1
type: experiment
parents:
  - hypothesis:l4-the-suite-lock-has-one-read-only-holder-judgement-for-its-probe-only-callers-and-one-writer
next_edges: []
confidence: 0.8
edited_by: a00-a3f2be5b
evidence_runs:
  - experiment:a00-a3f2be5b-1ec18a
line_ceiling: 20
loop: hypothesis:l4-the-suite-lock-has-one-read-only-holder-judgement-for-its-probe-only-callers-and-one-writer@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 18
profile: balanced
role: kid
scaffold_hash: a67d37880637e5a5
season: 2
title: Suite lock read only holder judgement lands and both probes use it
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-a3f2be5b-1ec18a

## Experiment

**What I built** (the g15 build order): the suite-lock READ-ONLY holder judgement and both probe-only callers rewired through it, so a probe never plants a live pid in the lock for microseconds.

Pre-fix state (measured on this tree): `verification._suite_lock_guard` and `grid.py`'s cron-path evidence-gate both probed via `acquire_suite_lock` then `unlink()`ed — a probe that momentarily WROTE its own live pid (the SM.88 residue: a suite starting on the same tick reads that pid as a live foreign holder and refuses once). `rotate._suite_lock_state_readonly` already existed but returned a display string and was used only by `cmd_merge_up`'s refusal line.

Landing (verification.py + grid.py only, 18 net production lines = 0.9x of the 20 ceiling):
1. `verification.suite_lock_holder(groot) -> int | None` — ONE read-only judgement: reads the lock + `_pid_alive`, WRITES NOTHING (never creates, never unlinks, never plants). Dead/absent/corrupt all read None. `acquire_suite_lock` stays the single WRITER.
2. `_suite_lock_guard` reuses it for the held/refusal arm (marker arm unchanged); a dead pid is still broken so the pinned stale test's `not lock.exists()` stays green.
3. `grid.py` cron-path gate calls `suite_lock_holder` instead of `acquire_suite_lock`+unlink — now fully read-only, never touches the file at all.
4. Added 3 tests proving `suite_lock_holder`: live foreign pid returned with byte+mtime identical; absent → None, no file created; dead pid → None, file left for the acquirer.

**The measured contradiction (why not plain `proved`)**: parent hypothesis claim (1) says the probe "never unlinks", but the pinned `test_suite_lock_guard_stale_proceeds` asserts the guard DOES break a dead-pid lock (`assert not lock.exists()`). Claim (1)'s "never unlinks" is therefore not fully landable without changing that pinned test. The hypothesis's own TESTS section permits "file left for the acquirer (or broken -- state it, one way)". I chose **broken, stated**: the guard still unlinks a dead pid (harmless cleanup, never plants a live pid), the grid gate is fully read-only. The microsecond window (the actual harm) is closed on both callers.

## Evidence

- `python3 -m pytest test_grid_evidence_gate_defer.py test_verification.py -q` → **54 passed** in ~1.2s. Includes: the three new `suite_lock_holder` tests; the existing guard tests (`refuses_held`, `stale_proceeds`, `marker`, `free`); and the three SM.88 grid-gate tests (`held_lock_defers_rewrite`, `tick_not_skip`, `stale_dead_pid_never_defers`) — ALL pass unchanged with the subprocess-foreign-pid semantics intact.
- `test_rotate.py` run surfaced a pre-existing failure `test_stops_stale_clock_grep_is_extended_regexp` (a `_stops_slot_is_stale` "UNCHANGED" vs "STALE" message-wording assertion). It is **outside my production scope** — rotate.py untouched by me (`git diff --name-only` shows only verification.py + grid.py) and has no suite-lock dependency. Reported as foreign noise, not mine.
- `git diff --numstat -- verification.py grid.py` = **18 net production lines** (grid +1/−3, verification +26/−6; the one read-only git measurement allowed), under the 20-line ceiling.

## Agent Notes
Built the read-only suite_lock_holder(groot)->live-foreign-pid judgement in verification.py; rewired _suite_lock_guard and grid.py cron gate through it so neither probe ever plants a live pid (SM.88 window closed); acquire_suite_lock stays single writer. 3 new tests + 54 pass on test_verification+test_grid_evidence_gate_defer incl SM.88 grid tests unchanged. 18 net production lines (0.9x). Caveat: guard still breaks a dead pid per pinned stale test so 'never unlinks' not literal — 'broken' arm stated. One foreign pre-existing red in test_rotate (stops-stale msg wording), not mine.
