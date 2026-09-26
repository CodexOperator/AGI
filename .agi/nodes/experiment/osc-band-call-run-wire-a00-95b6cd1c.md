---
id: experiment:osc-band-call-run-wire-a00-95b6cd1c
mint_id: 4c1a90f2be07d5a3c8e6f14b9d77aa20
type: experiment
parents:
  - hypothesis:a00-95b6cd1c-6f642c
edited_by: a00-95b6cd1c
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

**H3 — post-state, from a neutral cwd, scrubbed env.**
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
Identical exit from `cwd=/` and `cwd=/tmp`. The rule is now genuinely reached:
the 4 foreign-schema cells land as a REASON (not the raw `KeyError: 'budget'`
the previous reviewer saw, because the runner's `normalize` supplies the cell
key) and the 16 n=1 cells get the rule's own honest refusal.

## The test-harness half (this is the part that generalises)

`test_osc_band_call_run_a00-66d002ad.py:20` used to do
`sys.path.insert(0, os.path.dirname(HERE))` — the test repaired its subject's
environment, which is why a program exiting 1 sat under 3 green tests. I deleted
that line and added two subprocess tests that **cannot** inherit the test
process's `sys.path`:

| test | asserts |
|---|---|
| `test_entry_point_reaches_the_rule_from_a_neutral_cwd` | exit 2, no `ModuleNotFoundError`/`Traceback`, ≥1 row, all rows `unresolved` |
| `test_reach_is_cwd_independent` | exit codes agree from `/` and `/tmp` |

```
$ python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call_run_a00-66d002ad.py \
                  .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py -q
14 passed
```

## Negative control (the load-bearing part)

I removed ONLY the `sys.path[:0]` line, kept the new tests, and re-ran:

```
3 failed, 2 passed
  FAILED test_entry_point_reaches_the_rule_from_a_neutral_cwd  (ModuleNotFoundError)
  FAILED test_reach_is_cwd_independent
  FAILED test_todays_own_data_is_total_and_calls_nothing
```
then restored and re-ran: 14 passed. So (a) the new tests genuinely detect the
defect, and (b) the pre-existing test *also* fails the moment its own `sys.path`
seed is gone — direct evidence that the old green was the harness, not the
program.

## Reading

The decide layer of `goal:band-call-rule-per-cell` is now WIRE-LIVE end to end:
`python3 <runner>` → config-resolved data dir → rule → per-cell word or reason
→ exit code that means something. It still calls nothing, and that is correct:
the data under `paths.local_maxxing.osc_band_qknorm_dir` is 4 unreadable schemas
+ 16 unseeded n=1 cells, and slices (A)/(B) are the ones that will produce the
seeded draws. The remaining gap to `goal:g5.22.1`'s DONE WHEN is data, not code.

Production lines: 8 added / 1 removed in the runner (test file excluded), vs a
ceiling of 40.

## Struggles

`git diff --numstat` was the only git I ran, as briefed, for the line count.
