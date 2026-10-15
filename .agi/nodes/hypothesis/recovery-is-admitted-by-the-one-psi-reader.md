---
id: hypothesis:recovery-is-admitted-by-the-one-psi-reader
mint_id: 44a3b2a211ee4c4893b28918420477de
type: hypothesis
parents:
  - goal:g6.41.1
next_edges: []
confidence: 0.8
edited_by: director-general-1
scaffold_hash: c445acf58d5c33d8
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: heal launches a recovery only when _recovery_admitted, reading memory_alarm.read_psi against one config cell below the oomd kill line, admits it; over the cell or unreadable = deferred by name; at most one launch per pass, the Prime first
title: "Recovery is admitted by the one PSI reader against one config cell, fails closed when blind, one launch per pass (row R2 = g6.41.1 P5; assigned: director-general-3)"
town: core
---
# hypothesis:recovery-is-admitted-by-the-one-psi-reader

## Measured
- 18:3xZ 09-29: `_recovery_admitted` does not exist. heal `_watch_seats` (heal.py:3565) launches recoveries with no pressure read; CRASH_LOOP_MAX_PER_HOUR = 3 (heal.py:2270) is the only bound.
- `memory_alarm.read_psi` (memory_alarm.py:49) is the one PSI reader (callers: memory_alarm.py:83, :86); it returns {} when the file is unreadable (:57).
- config: no recovery-pressure cell. The box's oomd kill line is values.boxkit.OOMD_PRESSURE_PCT = 60 over OOMD_PRESSURE_SEC = 20s.

## CLAIM
heal admits a recovery only through `_recovery_admitted`, which reads memory pressure via `memory_alarm.read_psi` (never a second /proc/pressure reader) and compares some avg10 against ONE config cell set below oomd's kill line. Over the cell = "deferred" with the reading named, no launch. At most one launch per pass, the Prime first. An unreadable PSI ({}) is never read as zero pressure: it defers by name (a guard that cannot look fails closed).

## Dispatch line
config-max: the threshold is a config cell in .agi/config.json FIRST (its default below values.boxkit.OOMD_PRESSURE_PCT), never a literal. template-max: none. code: one gate function + its one call before the launch in _watch_seats.

## FALSIFIERS
- `git grep -n '/proc/pressure' -- extensions/agi/bin` names a reader outside memory_alarm.py
- a fixture PSI file over the cell launches a recovery
- an unreadable PSI admits a launch, or defers without a named reason
- two recoveries launch in one pass, or a non-Prime post launches ahead of a dead Prime

## TESTS
test_heal_watch.py (+3 cases: over, under, unreadable, with a tmp PSI file) ONE file, `--basetemp /tmp/b3r2`

## FILE SCOPE
extensions/agi/bin/heal.py (the gate + its call) · .agi/config.json (1 cell) · test_heal_watch.py

## CEILING
no dispatch · <= 25 production lines · <= 40 test lines · 0 USD
