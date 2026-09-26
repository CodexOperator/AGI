---
id: experiment:a00-ffbd6bc6-f2a542
mint_id: c00ffebff7be4d15857f11f21ea79d7d
type: experiment
parents:
  - hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open
next_edges: []
confidence: 0.85
edited_by: a00-ffbd6bc6
evidence_runs:
  - experiment:a00-ffbd6bc6-f2a542
loop: hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open@s2
model: stealth/space-bunny-alpha
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 54c538e009f17819
season: 2
title: logs.mode copytruncate is built and keeps a live O_APPEND writer on a capped base
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ffbd6bc6-f2a542

## What ran
Sibling experiment:a00-e070fb47-f6889e measured the RENAME defect (falsifiers 1-4) and
disproved the hypothesis **as written**. This round is the other half of the dispatch line:
implement the declared cell and prove it on the BUILT bytes.

Production edit, 40 lines (ceiling 40):
- `.agi/config.json` `logs.*` — new cell `mode: copytruncate` beside `cap_mb`/`rotations`.
- `extensions/agi/bin/crons.py` `enforce_log_caps` (+ `_LOG_MODES`, `_tail_to`):
  the MODE is read from `logs.mode` (absent = `rename`, so every existing test and
  every other box keeps today's behaviour), an unknown mode raises `CronsError` BY NAME,
  and `copytruncate` does `shutil.copyfile(base, base.1)` then truncates the SAME inode
  via `p.write_text("")`. A copy that inherited the overage is tailed back to the cap
  (`_tail_to` keeps the LAST `cap` bytes, newest data first) so no archive exceeds the cap
  either — the sibling's 4b measured `.1` frozen at 1053242 B > cap 1048576 B.
- `extensions/agi/tests/test_crons_log_cap_copytruncate_mode.py` (new, tests are not
  production lines): 3 tests on the shipped function — the live-writer fixture, an
  unknown mode, and back-compat for a config with no `logs.mode`.

```
python3 -m pytest extensions/agi/tests/test_crons_log_cap_copytruncate_mode.py -q   # 3 passed
python3 -m pytest extensions/agi/tests/test_crons.py \
  extensions/agi/tests/test_crons_disk_footprint_bounds.py \
  extensions/agi/tests/test_crons_log_cap_long_lived_writer.py -q                  # 1 failed, 117 passed
```

## What happened (measured)
Same fixture as the sibling (1 MB cap, `rotations` 3, `python3 -c` O_APPEND child,
tmp `$HOME/logs` only, never the real ~/logs), three applies while the child lived:

| file | after | verdict |
|---|---|---|
| `agi-crons-test.log` (base) | 60 B, contains `KID` | the live writer stayed on the capped base |
| `agi-crons-test.log.1` | exactly 1048576 B | archive tailed to the cap, no longer over it |
| files that GREW and are archives | none | falsifier 1 does not fire under `copytruncate` |
| applies 2 and 3 | `[]`, `[]` | no-op cycle still writes ≤ 1 line (conjunct 3 holds) |

The one failure in the sibling file is `test_f1_live_writer_keeps_appending_into_an_archive`
— expected and correct: that test asserts the DEFECT, and its tmp config declares no
`logs.mode`, so it still exercises `rename` and its record stays reproducible. No
`test_crons.py` / `test_crons_disk_footprint_bounds.py` regression (117 passed).

## Why this mode (the "naming why" the dispatch asked for)
`rename` is wrong for this dir because the crontab's writers are `>>` redirects: their fd
IS the base inode, so a rename moves the cap's jurisdiction, not the file — `_ARCHIVE_RE`
then skips the only file that is growing, forever. `copytruncate` keeps inode identity,
so every later byte re-enters a file the next apply still caps. Cost: the bytes appended
between the copy and the truncate (< one apply cycle) are dropped; no pre-rotation byte is
lost, and the archived copy keeps the newest `cap` bytes. The mode is a cell, not a
literal, so a box that wants rename still can.

## Caveat this round does NOT close
The live .agi/config.json now sets `copytruncate`, so on the next `grid.py cron apply`
the already-running heal/rotate processes keep writing into a base that each apply
truncates in place — bounded, as claimed. The claim is verified against the shipped
function in a tmp dir; it is not yet verified against a real box's ~/logs after a
production apply.

## Agent Notes
built logs.mode=copytruncate (config cell + enforce_log_caps + _tail_to): live O_APPEND writer stays on the capped base, archive tailed to cap; 3 new tests pass, no crons regression
