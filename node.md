---
id: experiment:osc-band-call-run-a00-66d002ad
mint_id: 3852ef0659874500a1c6a26c641df2fb
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
RE-MINTED belam gen 28, 01:2xZ 10-08: mint_id c89ca4b1fc104871849ee623ee8f13a5 -> 3852ef0659874500a1c6a26c641df2fb. Owner 01:2xZ 10-08, verbatim: "How about them grid commits can we resolves the duplicate mint id and the missing mint id issue". Since its birth (a264761af4, 09-26) this experiment carried the SAME mint as its parent hypothesis:a00-66d002ad-8cee33, so `grid.py commit --all` wrote both files into ONE grid ref twice per tick (2,284+ interleaved versions, ~30% of all grid versions; PASS B4 grid finding, DG2 dg2b4-w2d1-baseline row 6). The hypothesis keeps c89ca4b1 (and that ref, which also holds this node's pre-10-08 versions); this node starts a fresh ref under the new mint. This resolves the owner decision DG2 banked in dg2b4-w2d1-baseline:33 (CLAUDE.md "the mint id never changes" yields here: two nodes cannot share one identity).
<!-- THOUGHT:END -->
