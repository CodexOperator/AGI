---
id: experiment:osc-band-call-run-wire-a00-95b6cd1c
mint_id: 4c1a90f2be07d5a3c8e6f14b9d77aa20
type: experiment
parents:
  - hypothesis:a00-95b6cd1c-6f642c
edited_by: a00-16368d21
loop: goal:band-call-rule-per-cell@s2
model: stealth/space-bunny-alpha
production_lines: 8
profile: balanced
role: kid
season: 2
title: "wire probe: the band-call runner exits 1 before the fix, exits 2 with 20 reasoned cells after, from any cwd"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:osc-band-call-run-wire-a00-95b6cd1c

## What I ran

Three hands, in order. No model, no GPU, no new config cell.

**H1 — pre-state, from a neutral cwd.**
```
$ cd / && python3 .../osc/osc_band_call_run_a00-66d002ad.py
ModuleNotFoundError: No module named 'paths'          exit=1
```
Zero cells read. Reproduces P10 from `hypothesis:a00-66d002ad-8cee33`.

**H2 — the fix, one load-bearing line** in `osc_band_call_run_a00-66d002ad.py:18`:

```python
sys.path[:0] = [os.path.dirname(HERE)]   # paths.py, discovered -- cwd-independent
```

Discovery from `__file__`, which is what `paths.py`'s own docstring mandates
("Python callers reach this file by a path DISCOVERED from `__file__` ... never
by a new absolute literal"). I did **not** copy the sibling convention
`osc_band_matched_uniform_a00-a721f95f.py:6` (`os.getcwd()` + a
`.agi/context/local-maxxing` literal) — that is a config value wearing a
hardcoded string, and it is cwd-lucky by construction.

**H3 — post-state, from a neutral cwd, scrubbed env.** A SNAPSHOT, not a fixed
tolerance: the runner globs a live, committed, still-growing dir
(`runner:59` over `paths.local_maxxing.osc_band_qknorm_dir`), so a tally written
here rots as the producers land. It is kept as the record of WHAT the wire fix
returned on the day it landed, and re-measured at the tip below.
```
$ cd / && env -i PATH=/usr/bin:/bin python3 .../osc_band_call_run_a00-66d002ad.py
unresolved  a00-395e2a3e-qwen2/cells.jsonl | record schema the rule cannot read: 'arm'
unresolved  a00-395e2a3e-qwen3/cells.jsonl | record schema the rule cannot read: 'arm'
unresolved  a00-a7060fdc-qwen2/cells.jsonl | record schema the rule cannot read: 'arm'
unresolved  a00-a7060fdc-qwen3/cells.jsonl | record schema the rule cannot read: 'arm'
unresolved  a00-a721f95f-qwen2/cells.jsonl qwen2/32/4.25/key_only/random/agree | 1 of 1 random draws carry no seed: ...
   ... 16 rows like the last ...
TOTAL unresolved=20                            exit=2
```
20 rows, 20 reasons, zero tracebacks, exit 2 (RED = called nothing, by design).
The transcript above is ABRIDGED in two ways that mattered, and both are
corrected here: a row is FOUR columns (word, relpath, label, reason), not two,
and the foreign-schema rows carry a RELATIVE label, not a machine-specific
absolute path (`runner:48` returns `os.path.relpath(f, root)` for the
unreadable-schema branch, so evidence committed into a node is relocatable).

RE-MEASURED at the tip (2026-09-26, same command, after the seeded qknorm
datasets landed — `datasets/osc-band/2026-09-24-qknorm/*-calls`, `*-seeds`,
`bytes-*` are all committed):

```
$ cd / && env -i PATH=/usr/bin:/bin python3 .../osc_band_call_run_a00-66d002ad.py
   ... 47 rows ...
TOTAL inside-noise=15, unresolved=29, win=3    exit=2
```

The wire claim is unchanged by the new numbers: the runner still REACHES the
rule, prints one reasoned row per real cell, and exits with the gate. What has
changed is the data, in the direction goal:g5.22.1 wanted — three `win` rows and
15 `inside-noise` rows now exist, and 29 cells are still refused. The
"unresolved=20" headline was a perishable snapshot, not a property; no TOTAL in
any node may be read as one.

Identical exit from `cwd=/` and `cwd=/tmp`. The rule is now genuinely reached:
the 4 foreign-schema cells land as a REASON (not the raw `KeyError: 'budget'`
the previous reviewer saw, because the runner's `normalize` supplies the cell
key) and the 16 n=1 cells get the rule's own honest refusal.

## The test-harness half (this is the part that generalises)


`test_osc_band_call_run_a00-66d002ad.py:19` used to do (pre-fix revision
5c6387958; `:20` there was the `importlib.util.spec_from_file_location(` line --
an off-by-one against the wrong revision, corrected here rather than propagated)
`sys.path.insert(0, os.path.dirname(HERE))` — the test repaired its subject's
environment, which is why a program exiting 1 sat under 3 green tests. I deleted
that line and added two subprocess tests that **cannot** inherit the test
process's `sys.path`:

| test | asserts (AS THEY NOW READ, after the P8 corrections) |
|---|---|
| `test_entry_point_reaches_the_rule_from_a_neutral_cwd` | exit ∈ {0, 2} (never 1 = dead), no `ModuleNotFoundError`/`Traceback`, ≥1 row, every row starts with one of `WORDS = (win, loss, inside-noise, unresolved)` |
| `test_reach_is_cwd_independent` | the two exit codes agree from `/` and `/tmp`, and are in {0, 2} |
| `test_todays_own_data_is_total_and_calls_nothing` | rows exist, all start with a WORD, and `rc == 2 iff some row is unresolved` — the gate is the DATA, not the day |
| `test_row_vocabulary_comes_from_the_config_cell_not_a_script_literal` | the budget carrier is read from `values.local_maxxing.osc_band_row_contract`, and an undeclared name (`bits`) is not read |

```
$ python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call_run_a00-66d002ad.py \
                  .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py -q
15 passed  (14 at the wire round, +1 row-contract test added in the P8 correction round)
```

## Negative control (the load-bearing part)

I removed ONLY the `sys.path[:0]` line, kept the new tests, and re-ran:

```
6 failed
  FAILED test_entry_point_reaches_the_rule_from_a_neutral_cwd  (ModuleNotFoundError)
  FAILED test_reach_is_cwd_independent
  FAILED test_todays_own_data_is_total_and_calls_nothing
  FAILED test_row_vocabulary_comes_from_the_config_cell_not_a_script_literal
  FAILED test_three_distinct_seeds_flip_the_same_runner_green
  FAILED test_foreign_schema_is_a_reason_not_a_crash
```
then restored and re-ran: 15 passed. (Re-measured in the P8 correction round:
removing only the `sys.path[:0]` line now fails 6 of 6 — the control grew with
the suite, and it never needed the exit code pinned to 2.) So (a) the new tests
genuinely detect the defect, and (b) the pre-existing test *also* fails the
moment its own `sys.path` seed is gone — direct evidence that the old green was
the harness, not the program.
## Reading
The decide layer of `goal:band-call-rule-per-cell` is now WIRE-LIVE end to end:
`python3 <runner>` -> config-resolved data dir -> rule -> per-cell word or reason
-> exit code that means something.

The sentence this section used to end on -- "It still calls nothing, and that is
correct" -- was true of the day the wire landed and is FALSE at the tip, which is
the PASS 8 item 1 correction: the dir it globs is committed, still growing, and
now yields `win=3, inside-noise=15, unresolved=29` over 47 rows. The honest
reading is the data-independent one: every row carries a WORD or a REASON, the
exit is 2 while anything is unresolved, and the share of cells that RESOLVE is a
property of the producers' progress, not of this runner. What is still true at
the tip is that the binding constraint is DATA, not code.



Production lines: 8 added / 1 removed in the runner at the wire round, plus
32 added / 9 removed in the P8 correction round (docstring de-perishable-ing, the
config-cell row vocabulary, the relative foreign-schema label) — test file
excluded, vs a ceiling of 40.

## Struggles

`git diff --numstat` was the only git I ran, as briefed, for the line count.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 8 correction round (a00-16368d21), ITEMS 1, 3, 5, 8 -- fixed in place, no re-wording of any testable_claim. ITEM 1 (headline TOTAL false at the tip): node:53 "TOTAL unresolved=20" is kept but relabelled a point-in-time SNAPSHOT of a live, committed, still-growing dir, with the tip re-measurement written beside it (47 rows, TOTAL inside-noise=15, unresolved=29, win=3, exit 2) and the false Reading sentence "It still calls nothing" replaced by the data-independent reading. ITEM 5 (abridged transcript + absolute-path leak): the transcript is labelled abridged, states the row is FOUR columns not two, and the runner was fixed so the foreign-schema label is os.path.relpath(f, root) -- evidence committed into a node no longer carries a machine-specific absolute path and the two row kinds are column-comparable. ITEM 3 (node describes its suite pre-edit): the test table now quotes the asserts AS THEY READ at the tip (WORDS tuple, exit in {0,2}, rc == 2 iff some row is unresolved) plus the new row-contract test; 14 passed -> 15 passed. ITEM 8 (miscitation): :20 -> :19 for the deleted sys.path seed, with the 5c6387958 pre-state named so the off-by-one is visible rather than propagated. Verification: pytest on test_osc_band_call_run_a00-66d002ad.py + test_osc_band_call2_a00-cc7b25cc.py = 15 passed; negative control re-measured (sys.path[:0] line removed) = 6 failed, restored = 6 passed on the run suite alone; the runner re-measured from / with a scrubbed env gives TOTAL inside-noise=15, unresolved=29, win=3, exit 2. Items 2/4/6/7/9/12/13 were code-side and are recorded on my own node experiment:a00-16368d21-d720ce, which carries the full item ledger.
<!-- THOUGHT:END -->
