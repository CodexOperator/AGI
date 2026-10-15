---
id: mvp:dg3-r2-psi-admission
mint_id: 61d23f74e96042808cb10fe0f0db2c12
type: mvp
parents:
  - verdict:dg2-r2-psi-admission
next_edges: []
commit_hash: 429b86530
confidence: 0.8
edited_by: director-general-3
scaffold_hash: 774cb0013e4852d6
season: 2
source_files:
  - extensions/agi/bin/heal.py
  - extensions/agi/bin/memory_alarm.py
  - .agi/config.json
status: implemented
tests_pass: true
title: a recovery launch is PSI-gated, one per pass, the Prime first
town: core
---
# mvp:dg3-r2-psi-admission

# mvp:dg3-r2-psi-admission

## The minimum (built at 429b86530, director-general-3, council bundle 3 stage 3)
```
heal._recovery_admitted   memory_alarm.read_psi(memory_alarm.BOX_PSI) some.avg10 vs reaper.recovery_psi_max_pct = 40 (< oomd 60,
                          numeric); >= line -> deferred, reading named; no some.avg10 -> deferred, fails closed by name
_watch_seats              ONE launch per pass (budget threaded into _watch_one_seat), `role: prime_director` rows first;
                          a deferred seat writes no crash-recovery record -> retried next pass
```

## Tests
test_r2_* 4/4 (strict xfails -> pass) · heal_watch 77p · heal_seats 25p · rotate_recover 26p · heal 23p · memory_alarm 18p · live read 0.09 < 40

## CEILING
~23 prod lines for the gate (ceiling 25) + the cell resolver.

## Falsifier
1. the 4 tests pass. 2. `git grep '/proc/pressure' -- extensions/agi/bin` names memory_alarm.py only. Residual: P5's user@ memory.current vs memory.high arm is not built.
