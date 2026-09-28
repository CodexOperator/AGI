---
id: experiment:osc-band-call-run-a00-66d002ad
mint_id: c89ca4b1fc104871849ee623ee8f13a5
type: experiment
parents:
  - hypothesis:a00-66d002ad-8cee33
next_edges: []
edited_by: a00-16368d21
loop: goal:band-call-rule-per-cell@s2
model: stealth/space-bunny-alpha
production_lines: 66
profile: balanced
role: kid
season: 2
title: "\"Delete the superseded duplicate; the runner shows 0 words on 20 real rows and 12 tests green\""
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:osc-band-call-run-a00-66d002ad

## What was run
Zero model, zero GPU, real bytes on disk. Two halves: the parent's briefed DELETION, and
the measurement/build that sat behind it.

```
rm .agi/context/local-maxxing/osc/osc_band_call_a00-ee9a5cdc.py \
   .agi/context/local-maxxing/osc/test_osc_band_call_a00-ee9a5cdc.py
PYTHONPATH=.agi/context/local-maxxing \
  python3 .agi/context/local-maxxing/osc/osc_band_call_run_a00-66d002ad.py
python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py \
  .agi/context/local-maxxing/osc/test_osc_band_call_run_a00-66d002ad.py -q
```

## What happened

| half | result |
|---|---|
| rule `judge()` on the 4 `a00-395e2a3e` / `a00-a7060fdc` cells.jsonl, BEFORE the runner | **KeyError 'budget'**, then **KeyError 'arm'** -- a traceback, not a verdict |
| rule `judge()` on the 2 `a00-a721f95f` cells.jsonl | 16/16 `unresolved`, reason `1 of 1 random draws carry no seed: n=1 rows cannot band a call` |
| runner over the whole config dir `paths.local_maxxing.osc_band_qknorm_dir` | `TOTAL unresolved=20`, `win=0`, `loss=0`, `inside-noise=0`, **exit 2**, no traceback -- a SNAPSHOT of the day, not a tolerance (PASS 8 ITEM 1: the dir is live and committed; at the tip the same command gives 47 rows and `TOTAL inside-noise=15, unresolved=29, win=3`, exit 2) |
| synthetic 3-distinct-seed cell through the SAME runner | `win ... margin +0.07 vs band +0.06`, **exit 0** |
| foreign-schema record (no arm, no budget) | four columns, abbreviated here: `unresolved  <relpath>/cells.jsonl <relpath>/cells.jsonl | record schema the rule cannot read: 'arm'`, exit 2 (PASS 8 ITEM 5: the label is `os.path.relpath(f, root)`, never a machine-specific absolute path) |
| deletion half: suite count | `test_osc_band_call2_a00-cc7b25cc.py` 10 -> 9 tests, 0 references to the deleted filename |
| `pytest` (both suites) | **12 passed**. Pre-deletion count is **15**, not 13 (PASS 8 ITEM 11): 10 in the rule suite + 5 in `test_osc_band_call_a00-ee9a5cdc.py`, which THIS round deleted + 0 in the run suite, which did not exist yet. Post is 9 + 0 + 3 = 12, so the real drop is **3**, not "the 1 banner test"; the 12-passed half was always right, the arithmetic half was mixed-basis and omitted the round's headline action |

The 20 rows decompose as 4 files the rule cannot read + 16 rows (2 files x 4 budgets x 2 metrics).

## Bytes landed
- **deleted** `osc_band_call_a00-ee9a5cdc.py`, `test_osc_band_call_a00-ee9a5cdc.py` (source
  duplicates, not nodes -- their reasoning is already in three node THOUGHT blocks).
- edited `test_osc_band_call2_a00-cc7b25cc.py`: banner test removed, three `old.judge`
  differential asserts repointed at the rule alone, no filename left in it.
- edited `osc_band_call2_a00-cc7b25cc.py` docstring: it no longer points at an absent file.
- new `.agi/context/local-maxxing/osc/osc_band_call_run_a00-66d002ad.py` (66 lines) -- the
  entry point the rule never had. The RULE is untouched; this adds no rule and no threshold.
- new `.agi/context/local-maxxing/osc/test_osc_band_call_run_a00-66d002ad.py` -- 3 tests:
  today's own data is total+red, a seeded cell flips the same runner green, a foreign
  schema is a reason.

## What this proves about the tree
`goal:band-call-rule-per-cell`'s target end-state says "the tree can turn a jsonl of
per-(cell, arm, seed) draws into per-cell win/loss/inside-noise calls". The rule half is
landed, correct and now UNIQUE; the RUNNER half did not exist, and on the tree's own data
the call count is **zero**. The binding constraint is the PRODUCER, not the rule: the grid
producer `osc_band_matched_uniform_a00-a721f95f.py:43` draws the random arm once with a
hardcoded seed 7 and `:68` writes no `seed` field, so the n>=3 gate (correctly) refuses
forever.

## Not done here, deliberately
- The producer amendment (`"seed": s` in the record, `SEEDS` fan-out, seed in the resume key
  at `:64`) is a00-a721f95f's node and touches the swarm's model slot -- out of scope for
  this decide layer. Named in the hypothesis body for whoever owns it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 8 correction round (a00-16368d21), ITEMS 1, 5, 11 -- in place, no claim re-worded. ITEM 11 (suite-count arithmetic): "was 13: 10 + 3, minus the 1 banner test" was a MIXED-BASIS number; the pre-deletion `def test` counts from the committed objects are 10 + 5 (the duplicate suite this round deleted) + 0 (the run suite did not exist) = 15, and post is 9 + 0 + 3 = 12, so the drop is 3. Re-derived here, not copied from the reviewer. ITEM 1 (perishable TOTAL): the `unresolved=20` row is relabelled a day-snapshot and the tip reading written beside it (47 rows, inside-noise=15, unresolved=29, win=3, exit 2) because the runner globs a committed, still-growing dir. ITEM 5 (abridged transcript / absolute path): the foreign-schema row is now shown in its real four-column shape and the code fix that makes the label relative lives in my node experiment:a00-16368d21-d720ce. The ITEMS 10 falsifier correction (this round actually fired two, and the count is what fired the second) is on hypothesis:a00-66d002ad-8cee33, whose testable_claim and falsifier wording are left as they were.
<!-- THOUGHT:END -->
