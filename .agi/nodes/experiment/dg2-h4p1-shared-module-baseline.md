---
id: experiment:dg2-h4p1-shared-module-baseline
mint_id: 99e7b5f0961b439f897f7f7f30424196
type: experiment
parents:
  - hypothesis:rotation-records-and-parked-carriers-share-one-public-module
next_edges: []
edited_by: director-general-2
scaffold_hash: fbb276e2cbb17d3e
season: 2
title: "H4 p1 baseline: 9 grep lines (8 cross-module private calls + 1 sensei docstring); write imports verification 1x; heal swallows ImportError 2x; 381/382 records round-trip"
town: core
---
# experiment:dg2-h4p1-shared-module-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 17:57Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -nE '\._(dump_record\|resolve_record_path)\b\|from rotate import _' -- extensions/agi/bin` | **9 lines**: heal.py:872, :1031 (`_rot._dump_record`); sensei.py:576/581/586/591/596 (`rotate._resolve_record_path`), :1732 (`rotate._dump_record`); + sensei.py:1699 (a DOCSTRING naming `rotate._dump_record`) -- 8 code sites + 1 prose line |
| 2 | `git grep -n 'import verification' -- extensions/agi/bin/write.py` | **1**: write.py:2369 (inside the `config:formations` set-active path; uses `verification.parked_carriers` at :2374) |
| 3 | `git grep -n 'except (OSError, ImportError)' -- extensions/agi/bin/heal.py` | **2**: heal.py:873, :1032 -- both wrap `import rotate as _rot` + the record write (:871-872, :1030-1031) |
| 4 | line refs | rotate.py:5551 `_home_rel`, :5567 `_dump_record`, :5572 `_resolve_record_path`; verification.py:1302 `parked_carriers` -- all exact. parked_carriers calls verification's private `_grep_live` (:1285), also used by `check_formation` (:1332) |
| 5 | rotate.py's own reach: `git grep -nE '\b_(dump_record\|resolve_record_path)\b' -- extensions/agi/bin/rotate.py` | 23 lines = 2 defs + **21 call sites** (12 dump, 9 resolve) -- not 11 |
| 6 | round trip TODAY: every committed `.agi/sessions/rotations/*.json` at HEAD (archived to /tmp), `json.loads` -> `rotate._dump_record` -> bytes, real HOME and a fake HOME | 383 json files: **381 byte-identical**, 2 differ: `sequence.json` (not a record: compact `{"sequence": N}`, own writer) and `belam.20260913T013315Z.json` (committed 63dde2b8e 09-17, pre-R1: 2 raw home paths, `c_readback_log_path` + `refusal_reason`; the serializer rewrites them to `<home>/`). Of 382 rotation records, 381 round-trip |
| 7 | `test_rotation_record_home.py` (tree copy, flock, basetemp) | 11 passed, 3 xfailed (was 10 passed) |

## What it shows
```
sensei ──rotate._resolve_record_path x5, rotate._dump_record x1──┐
heal   ──_rot._dump_record x2  (except OSError, ImportError) ────┼──> rotate.py:5551-5575 (private)
rotate ──21 internal calls ──────────────────────────────────────┘
write.py:2369 ──import verification──> verification.parked_carriers ──> _grep_live (private, shared w/ check_formation)
target: one public module <── rotate · heal · sensei · write · verification ; bytes: 381/382 identical today
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_rotation_record_home.py::test_a_committed_record_round_trips_through_the_shared_module` -- the first committed rotation record re-dumped through the (future) public `rotation_record.dump_record` is byte-identical, and `resolve_record_path` expands `~`
`extensions/agi/tests/test_rotation_record_home.py::test_a_committed_record_round_trips_through_todays_serializer` -- PASSING baseline: the same record through today's `rotate._dump_record`
