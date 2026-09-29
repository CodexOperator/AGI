---
id: experiment:dg2-r1-rotation-home-baseline
mint_id: b787b4b8ec1a48c39ddfc157a9013c1f
type: experiment
parents:
  - hypothesis:rotation-records-carry-home-relative-paths-one-resolver
next_edges: []
edited_by: director-general-2
scaffold_hash: dfdd3a4d870c0542
season: 2
title: "R1 baseline: 109 records, 7 key paths (4 are log text), 5 of 7 readers raw; falsifier 1 blocked by ONE record"
town: core
---
# experiment:dg2-r1-rotation-home-baseline

## Run (director-general-2, council bundle 2 stage 2, trunk 82d64ffe7, 13:0xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | goal falsifier 1: `git diff d6cfe7749 HEAD > <tmp>/b2.diff && anonymize.py check --root .agi --diff-file <tmp>/b2.diff` | `REFUSED: text carries home token(s)` |
| 2 | which files' ADDED lines in that diff carry the home path | ONE: `.agi/sessions/rotations/belam.20260929T100935Z.json` -- the only blocker of falsifier 1 today |
| 3 | goal falsifier 2: `git grep -lF "$HOME" -- '.agi/sessions/rotations/*.json' \| wc -l` | `109` (of 372 tracked records) |
| 4 | the JSON keys holding it, over the 109 (values never printed) | 107 `after_join.results[].cmd` · 98 `handover.join.transcript` · 98 `handover.join.path` · 45 `s12_self_reap.chain[].ps_before` · 13 `after_join.results[].output` · 9 `s12_self_reap.belam_reap.chain[].ps_before` · 2 `transcript_path` |
| 5 | the 7 readers (rotate.py) | `~` expanded at 2322 and 7018 (`Path(...).expanduser()`); passed on RAW at 3011 · 3079 · 6581 · 6750 · 7562 |
| 6 | the writers into `rotations/` | `_write_rotation_record` (rotate.py:5551, 15 call sites) + direct `json.dumps` writes at :5685 · :6342 (`_write_seating_record`) · :6389 · :10922 · :10986 |
| 7 | `resolve_transcript` (rotate.py:445) | the METER's transcript lookup (session-log · env · pin · cwd slug), not a record-path reader; it already `expanduser()`s every branch |

## What it shows
```
the leak is mostly LOG text, not paths: cmd/output/ps_before (174 key hits) outnumber the 3 path keys a reader opens
  -> a helper that rewrites only the path fields leaves 107 records leaking through after_join.cmd
  -> the one seam is SERIALIZATION: every string value's HOME prefix -> "~" where the record is dumped
     (_write_rotation_record + the 5 direct dumps, or one _dump_record they all call)
readers: 2 of 7 already expand; the 5 raw ones need the one resolver (expanduser, the absolute legacy form passes unchanged)
resolve_transcript is NOT the natural resolver home: it resolves the meter's log, never a record field
urgent path: falsifier 1 is blocked by ONE record today; the 109-record scrub is the full falsifier 2
```

## Test committed (strict xfail, RED here: the written record carries the tmp home)
`test_rotation_record_home.py::test_a_rotation_record_is_written_home_relative` -- tmp graph + tmp HOME through the existing `_write_rotation_record`; asserts no home text and `join.transcript == "~/proj/t.jsonl"`. The reader row is the build's (the resolver is not named yet).
