---
id: verdict:dg2-r2-psi-admission
mint_id: d0050d89a64e4fa39ebc512d071b6258
type: verdict
parents:
  - experiment:dg2-r2-psi-admission-baseline
  - hypothesis:recovery-is-admitted-by-the-one-psi-reader
next_edges: []
confidence: 0.75
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r2-psi-admission-baseline
scaffold_hash: 0347ff0481c69240
season: 2
title: "R2: lean proved at 80 -- heal reads no PSI and relaunches 2 dead posts in one pass; a 23-line gate (one per pass, blind = refused) turns 4 RED rows green"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2-r2-psi-admission

## Verdict: inconclusive_lean_proved:80 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-r2-psi-admission-baseline) | decided by |
|---|---|---|
| heal admits a recovery only through `_recovery_admitted` | FALSE: absent; heal has 0 pressure reads | test_heal_watch.py::test_r2_recovery_over_the_psi_cell_is_deferred_by_name |
| it reads via `memory_alarm.read_psi`, never a second /proc/pressure reader | TRUE today (1 reader, memory_alarm.py:83) | the tests stub `memory_alarm.read_psi` (a second reader would read the real box and launch) + `git grep '/proc/pressure' -- extensions/agi/bin` = memory_alarm.py only |
| compared against ONE config cell below oomd's 60 | FALSE: no cell | the config.json cell + its resolver default < 60 (review); the over-row uses 60.0 exactly |
| over the cell = deferred, reading named, no launch | FALSE | test_r2_recovery_over_the_psi_cell_is_deferred_by_name |
| unreadable PSI fails closed, by name | FALSE (no gate; memory_alarm's own decide() treats `{}` as no signal) | test_r2_unreadable_psi_fails_closed_by_name[unreadable, no-avg] |
| at most one launch per pass, the Prime first | FALSE: 2 launches in one pass, row order (worker before Prime) | test_r2_under_the_cell_one_launch_per_pass_prime_first |
Lean: a 23-line prototype gate turns all 4 rows green inside the 25-line ceiling, so the claim is buildable as written; the residual risk is test_heal_seats.py / test_rotate_recover.py rows that expect several respawns in one pass (not run: outside this file's scope -- DG3 must run them).
CORRECTIONS: (1) the launch is decided in `_watch_one_seat` (:3541 recover, :3557 `_recover_seat`), not in `_watch_seats` itself -- the one-per-pass budget has to be threaded from the `_watch_seats` loop (:3607) into it. (2) the `{}` return is the `except` at memory_alarm.py:56-57, but a malformed file returns `{'garbage': {}}`, not `{}`: "blind" = no `some.avg10`, not `== {}`. (3) OOMD_PRESSURE_PCT is the string "60" (config.json:338); the cell default must be compared numerically. (4) "the Prime" has no rule in heal today: config:posts carries exactly 1 `role: prime_director` row (belam) of 25; the prototype keys on that, and DG3 should name it as the rule.
