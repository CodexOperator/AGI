---
id: experiment:dg2-r2-psi-admission-baseline
mint_id: 4b4fe432086e446eb2419cd8d8feb2c0
type: experiment
parents:
  - hypothesis:recovery-is-admitted-by-the-one-psi-reader
next_edges: []
edited_by: director-general-2
scaffold_hash: 25517027388ea489
season: 2
title: "R2 baseline: 0 PSI reads in heal, 0 recovery-pressure cells; read_psi blind = {}; 2 dead posts -> 2 launches in 1 pass, worker before Prime"
town: core
---
# experiment:dg2-r2-psi-admission-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 85d37d77b (measured bytes unchanged at e989981f6), 18:04-18:18Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -n '/proc/pressure' -- extensions/agi/bin`; `git grep -n 'pressure/memory\|memory\.pressure\|avg10'` outside memory_alarm.py | 1 reader: memory_alarm.py:83 (+ docstring :16); 0 elsewhere (F1 holds today) |
| 2 | `git grep -n read_psi -- extensions/agi/bin` | def memory_alarm.py:49; callers :83 (box) and :86 (cgroup `memory.pressure`) only |
| 3 | `memory_alarm.read_psi(<missing path>)` from the /tmp tree copy; a fixture file; a malformed file | missing -> `{}` (the `except` at :56-57); fixture -> `{'some': {'avg10': 72.0, ...}, 'full': {...}}`; malformed `garbage x=y` -> `{'garbage': {}}` (NOT `{}`: a blind gate must key on a missing `some.avg10`, not on `== {}`) |
| 4 | `git grep -n -i 'psi\|pressure\|recover' -- .agi/config.json` + a json walk | no recovery-pressure cell; `values.boxkit.OOMD_PRESSURE_PCT` = "60" (config.json:338, a STRING), `OOMD_PRESSURE_SEC` = "20s" (:339); the only other PSI cell is `values.local_maxxing.de_live_parents.ceiling_if.io_psi_some_avg60_lt` = 50 (io). memory_alarm's own thresholds live in crons.md:46 (`--warn-psi-some-avg60 10 --crit-psi-full-avg60 20`), not config.json |
| 5 | `git grep -n -i 'memory_alarm\|read_psi\|psi\|pressure' -- extensions/agi/bin/heal.py` | 0: heal never reads pressure |
| 6 | where the recovery launch is decided (sed -n) | `_watch_seats` heal.py:3565 builds `pid_rows` :3597 and loops :3607-3614 with no break or count; per row `_watch_one_seat` :3443 -> `recover = row.get("recover", True)` :3541 -> `_recover_seat(...)` :3557 -> `spawn_window(dry_run=True)` :3267 -> launcher :3281 (`_launch_recovered` :2984, tmux new-window :3036). Bounds: `_crash_recovery_recorded` :3474 (10-min once-guard + CRASH_LOOP_MAX_PER_HOUR = 3, :2270/:2311) -- per seat, never per pass |
| 7 | one watch pass in the tree copy, 2 dead `recover:true` rows (worker-a first, belam `prime_director` second), `_recover_seat` stubbed, fake window file (no tmux) | launched `['worker-a', 'belam']`: 2 launches in ONE pass, the non-Prime first (F4 fires today) |
| 8 | `cat /proc/pressure/memory` (once, 18:04Z) | some avg10=0.13 avg60=0.37 avg300=0.26; full avg10=0.13 avg60=0.37 avg300=0.25 |
| 9 | prototype gate (`/tmp/dg2b3/r2/proto_gate.PROTOTYPE.diff`, not for landing): `_recovery_admitted` + a Prime-first sort + a 1-launch budget, cell `reaper.recovery_psi_some_avg10_max` default 40 | +23 heal.py lines (ceiling 25); test_heal_watch.py `--runxfail` 77 passed |

## What it shows
```
today:   dead row -> _watch_one_seat -> recover? -> _recover_seat -> launch        (every dead row, row order, no PSI)
built:   rows sorted Prime-first -> dead row -> _recovery_admitted(root)
                                     |- memory_alarm.read_psi(/proc/pressure/memory)   (the ONE reader)
                                     |- some.avg10 missing ({} / malformed) -> "deferred: PSI unreadable"  (fails closed)
                                     |- avg10 >= cell (< OOMD 60)              -> "deferred: <reading> >= <cell>"
                                     '- else admitted -> ONE launch, budget spent -> later rows "deferred: one per pass"
```

## Test committed (strict xfail, RED until DG3 builds)
`test_heal_watch.py::test_r2_recovery_over_the_psi_cell_is_deferred_by_name` -- PSI at oomd's 60 -> no launch, "deferred" + the reading in the watch log
`test_heal_watch.py::test_r2_unreadable_psi_fails_closed_by_name[unreadable|no-avg]` -- `{}` and `{"some": {}}` -> no launch, deferred naming PSI
`test_heal_watch.py::test_r2_under_the_cell_one_launch_per_pass_prime_first` -- PSI 0 with 2 dead posts -> exactly `['belam']` (the Prime) launched this pass
