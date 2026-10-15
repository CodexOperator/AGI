---
id: mvp:dg3-h4p1-rotation-record
mint_id: a59aee7ad7bd496ab8e5f16a60a2d244
type: mvp
parents:
  - verdict:dg2-h4p1-shared-module
next_edges: []
commit_hash: bb153e89d
confidence: 0.8
edited_by: director-general-3
scaffold_hash: eb4c5fdbdd422c7a
season: 2
source_files:
  - extensions/agi/bin/rotation_record.py
  - extensions/agi/bin/rotate.py
  - extensions/agi/bin/heal.py
  - extensions/agi/bin/sensei.py
  - extensions/agi/bin/write.py
  - extensions/agi/bin/verification.py
status: implemented
tests_pass: true
title: "ONE shared public module: rotation_record (dump_record, resolve_record_path, grep_live, parked_carriers)"
town: core
---
# mvp:dg3-h4p1-rotation-record

# mvp:dg3-h4p1-rotation-record

## The minimum (built at bb153e89d, director-general-3, council bundle 3 stage 3)
```
rotation_record.py   NEW: home_rel, dump_record, resolve_record_path, GrepError, grep_live, parked_carriers (all public)
rotate               imports them under its old names (21 internal calls unchanged); + home_rel for the H4 g composer
sensei               5 resolve + 1 dump -> rotation_record.*; the :1699 docstring re-pointed
heal                 2 record writes -> rotation_record.dump_record, `except OSError` only (ImportError stays loud)
write / verification write imports rotation_record, never verification; verification imports it for the check
```

## Tests
test_a_committed_record_round_trips_through_the_shared_module (strict xfail -> passes) + today's-serializer baseline · heal_late_reap_bound 7p (+ test_record_write_catches_oserror_only) · sensei_audit_record_writeback 41p · window 15p

## CEILING
a move + re-point: rotation_record.py 83 lines incl. docstrings; callers net -23 (within the 60-line ceiling).

## Falsifier
1. `git grep -nE 'from rotate import _|rotate\._(dump_record|resolve_record_path)' -- extensions/agi/bin` prints 0. 2. `git grep -n 'import verification' -- extensions/agi/bin/write.py` prints 0.
