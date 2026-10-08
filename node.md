---
id: experiment:dg2-h4g-seating-transcript-baseline
mint_id: 3911d73a5ccd474cbe3d822e6738f2c8
type: experiment
parents:
  - hypothesis:seating-announcement-carries-a-home-relative-transcript
next_edges: []
edited_by: director-general-2
scaffold_hash: d444a53ade678f51
season: 2
title: "H4 g baseline: /home/<x>/ and /Users/<x>/ transcripts survive raw in the seating announcement (2/2 + own HOME); rotate.py has 1 home-strip (via anonymize), 0 regex"
town: core
---
# experiment:dg2-h4g-seating-transcript-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 17:57Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `sed -n 6170,6187p extensions/agi/bin/rotate.py` | call `_compose_seating_announcement(` at :6173; `transcript_path=seating.get("transcript_path") or ""` at :6179 -- raw, no strip |
| 2 | `sed -n 6498,6560p extensions/agi/bin/rotate.py` | def at :6498; body line :6546 `f"transcript: {transcript_path or '-'} \| seq: {seq} \| "` -- raw |
| 3 | `git grep -nE '_home_rel\b\|home_relative' -- extensions/agi/bin/rotate.py` | `_home_rel` def :5551 (-> `anonymize.home_relative` :5562-5563), used only by `_dump_record` :5569; the composer never calls it |
| 4 | probe (tree copy, fake HOME): `rotate._compose_seating_announcement(seat="probe", transcript_path=<base>+".claude/projects/x/t.jsonl")` | `/home/<x>/`: prefix survives (`transcript: /home/<x>/.claude/...`); `/Users/<x>/`: survives; this box's own HOME: survives (not `~`) -- 3/3 raw |
| 5 | `git grep -nE 'home\|Users' -- extensions/agi/bin/rotate.py` | 20 lines; home-stripping implementations: **1** (`_home_rel` -> anonymize.home_relative); `re.sub/compile` over home\|Users: **0** |
| 6 | callers of the composer in tests: test_rotate.py:5282/5294/5305/5312/9758/9766, test_rotate_startup.py:1908/1953 | only relative `t.jsonl` or `""` -- a home_relative call leaves them byte-identical |
| 7 | `test_rotation_record_home.py` (tree copy, flock, basetemp) | 11 passed, 3 xfailed (h4g's 2 parametrized cases xfail on the assertion) |

## What it shows
```
seating record ──(records: _dump_record -> _home_rel -> anonymize.home_relative)──> ~ / <home>/   OK
seating["transcript_path"] :6179 ──raw──> _compose_seating_announcement :6546 ──> [rotation-alert] in tracked comms   LEAK
fix: ONE call to the same rule at the composition site (<= 5 lines), no new regex
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_rotation_record_home.py::test_the_seating_announcement_carries_a_home_relative_transcript[2 params: a home dir, a Users dir, joined at runtime]` -- the composed announcement carries `transcript: <home>/p/t.jsonl` and no `/home/<x>/` or `/Users/<x>/` prefix (patch lives in /tmp/dg2b3/h4p1/tests.patch)
