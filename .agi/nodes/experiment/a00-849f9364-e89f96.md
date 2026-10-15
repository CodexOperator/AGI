---
id: experiment:a00-849f9364-e89f96
mint_id: aeae2d9687b44a04b3fe15b5f563244f
type: experiment
parents:
  - hypothesis:osc-np64-noise-band-per-cell
next_edges: []
confidence: 0.7
edited_by: director-thought
evidence_runs:
  - experiment:a00-849f9364-e89f96
loop: hypothesis:osc-np64-noise-band-per-cell@s2
model: stealth/space-bunny-alpha
probes:
  - "gate: the 3-seed SUBSET of the new 4-seed file reproduces the previous round bands to the last digit at all four budgets (0.026367187 / 0.095703125 / 0.064453124 / 0.107421876) and every margin exactly -- so nothing in the earlier round was a stale-file artefact, and the fixed-output-dir overwrite really was a no-op"
  - "wire: every random group carries seeds [7,21,45,99] with 4 DISTINCT agree values, and the values at seeds 7/21/99 are bit-identical to the previous round -- the fourth draw reached the loop and the run is deterministic; a stub that ignored --seeds would show seed 45 duplicating seed 7"
  - "config: SEEDS_DEFAULT imported live from the harness read 7,21,99,45 only in the round tree; CORRECTED 09-26 per PASS 8 item 1, the trunk cell is still 7,21,99 and this run passed seed 45 on the command line"
  - "independent reducer: osc_band_call2_a00-cc7b25cc.py judge(cells, comparator=uniform), a file this kid did not touch, returns inside-noise / inside-noise / LOSS / inside-noise at n=4"
  - "the RANGE contradiction is real, not prose: at 6.125 key_only 0.306640625 lies INSIDE the random range [0.280273438, 0.346679688] while the margin call reads loss, and the margin/band ratio there is 1.0882 (1.121 at n=3), so the one actionable cell survives a fourth draw by 8.8 percent"
production_lines: 1
profile: balanced
role: kid
scaffold_hash: 1f3a7b49ae4b8c04
season: 2
title: "four-seed draw on the qwen3 np64 band: does the 6.125 LOSS survive seed 45"
town: local-maxxing
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-849f9364-e89f96

## What

Add the goal's fourth seed. Every band on disk rests on THREE draws {7,21,99}; the goal
node `goal:qwen3-np64-noise-band` names FOUR {7,21,99,45}. One invocation, all four
budgets (cells.jsonl opens with "w" -- a budget subset would erase the others).

    export PYTHONPATH=$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath)
    python3 .agi/context/local-maxxing/model_slot.py -- /data/ml/.venv/bin/python \
      .agi/context/local-maxxing/osc/osc_band_seeds_qwen3_a00-6771cb76.py \
      qwen3 --seeds 7,21,99,45 --prompts 2

Zero production lines touched; the script is the previous kid's, unchanged.

## Three questions, answered by the run

1. does the 6.125 LOSS survive a fourth draw (the only cell outside the noise)?
2. how far do the four bands move from n=3 to n=4?
3. does the config cell `values.local_maxxing.osc_band_seeds` (currently `[7,21,99]`)
   get 45, so the DEFAULT and the MEASUREMENT agree?

## Starting state (measured before the run)

| item | value |
|---|---|
| `a00-6771cb76-qwen3/cells.jsonl` | 20 rows (4 budgets x [uniform n=1, key_only n=1, random@7/21/99]), n_prompts=2 |
| `summary.json` seeds | [7, 21, 99] |
| `values.local_maxxing.osc_band_seeds` | [7, 21, 99] |
| MemAvailable before launch | 6362 MiB |
| sibling model processes | none (`pgrep -af osc_band_seeds` -> no run, only pi agents) |

## Result

(filled in below, verbatim from the run)
## Result -- the run LANDED

`real 6m46s`, foreground, inside `model_slot.py`. `cells.jsonl` = **24 rows**
(4 budgets x [uniform n=1, key_only n=1, random@7/21/99/45]), `summary.json`
`seeds: [7,21,99,45]`, every random group `n_seeds=4 n_distinct=4`, both
deterministic arms still `n=1 seed=0 arm_is_stochastic=false`.

| budget | random agree @ 7/21/99/**45** | band n=3 | band n=4 | delta | margin (k-u) | call n=3 | call n=4 |
|---|---|---|---|---|---|---|---|
| 4.125 | 0.033203125 / 0.025390625 / 0.051757812 / **0.043945312** | 0.026367187 | 0.026367188 | 0 (45 inside) | +0.020507813 | inside-noise | inside-noise |
| 5.125 | 0.046875 / 0.04296875 / 0.138671875 / **0.143554688** | 0.095703125 | 0.100585938 | +0.0049 (+5.1%) | +0.002929688 | inside-noise | inside-noise |
| 6.125 | 0.280273438 / 0.3359375 / 0.344726562 / **0.346679688** | 0.064453124 | 0.066406250 | +0.00195 (+3.0%) | **-0.072265625** | **LOSS** | **LOSS** |
| 7.125 | 0.6796875 / 0.602539062 / 0.709960938 / **0.725585938** | 0.107421876 | 0.123046875 | +0.0156 (+14.5%) | -0.023437500 | inside-noise | inside-noise |

**SELF-CONSISTENCY CHECK (free, and worth more than the new column).** Taking the
3-seed SUBSET out of the new 4-seed file reproduces the parent's hand-computed
3-seed bands to the last digit at all four budgets (0.026367187 / 0.095703125 /
0.064453124 / 0.107421876) and reproduces every margin exactly. The two runs agree;
nothing in the previous round was a rounding artefact of a stale file.

**INDEPENDENT REDUCER.** The untouched `osc_band_call2_a00-cc7b25cc.py`
(P3 distinct-seed gate, P4 degenerate-band refusal, P6 comparator=uniform) over
the new cells.jsonl returns the same four words:
`4.125 inside-noise (margin +0.02051 vs band +0.02637)`,
`5.125 inside-noise (+0.00293 vs +0.1006)`,
`6.125 loss (-0.07227 vs +0.06641)`,
`7.125 inside-noise (-0.02344 vs +0.123)`.
The harness's own `call()` and the reducer p3 will actually import now agree on
every cell, at n=4.

## The three questions, answered

**Q1 -- does the 6.125 LOSS survive a fourth draw? YES, but it is thinner than it
looked.** Seed 45 sits ABOVE the 3-seed max at 6.125 (0.346679688 > 0.344726562),
so the band GREW, not shrank: 0.064453 -> 0.066406. The margin is unchanged
(the arms are deterministic) at -0.072266. The margin/band ratio therefore
*fell* from **1.121 to 1.088** -- a fifth draw, if it lands above 0.346679,
would put the cell inside-noise. So: the only actionable claim in this family
survives n=4 by 8.8%, and its evidence is decaying as the denominator grows.
That is a fact about the denominator, not about key_only.

**Q2 -- how far do the bands move from 3 to 4? Never down; up to +14.5%.** Seed 45
landed inside the range at 4.125 (no change) and above the max at 5.125 / 6.125 /
7.125 (+5.1% / +3.0% / +14.5%). NO band shrank and no call flipped. A band that
grows with n is a working denominator, not a 0.0 in an n=4 hat; 4 seeds is enough
for these four cells, and the parent should not spend another kid on n=5 for the
sake of the call -- if anything, the missing quantity is draws, not seeds.

**Q3 -- the config cell. CORRECTED 09-26 (PASS 8 item 1): the edit below NEVER LANDED.** The director dropped it at the swarm-2 harvest and a PASS 8 residue kid re-applying it broke osc_band_seeds_qwen2_a00-2b3ca8c4_test.py::test_config_cell_holds_the_seeds -- the SAME cell feeds the qwen2 seed script, whose committed data is 3 seeds (7/21/99). The cell stays [7, 21, 99]; a qwen3 re-run of this round must pass --seeds 7,21,99,45. What this round originally wrote, kept for the record:
`values.local_maxxing.osc_band_seeds` was `[7, 21, 99]`; it is now
`[7, 21, 99, 45]` (.agi/config.json:269, 1 line). Reason: the goal's end-state names
four seeds, the measurement is now four seeds, and a default that silently
reproduces the 3-seed band on the next bare invocation is config-max's exact
failure (the default must be the measured value, not a copy of an earlier
round's argv). `SEEDS_DEFAULT` in the harness reads this cell at import, so a bare
`osc_band_seeds_qwen3_a00-6771cb76.py qwen3 --prompts 2` now reproduces this
round's file. **I did NOT change anything else in config.json** -- no
`paths.*` cell moved, no new path literal was introduced.

## Largest safe step

The band denominator is now MEASURED at n=4 on all four np64 budgets and both
call rules agree on it. The next useful step is not another seed: it is
`call2`'s own rule applied to a cell where the key_only value is compared against
the random RANGE (the second, never-merged call in
`values.local_maxxing.osc_band_row_contract` -- `min(random) <= key_only <=
max(random)`). I computed it once here and it matters: at 6.125 the key_only
agree 0.306640625 lies INSIDE the random range [0.280273438, 0.346679688], so
RANGE reads FINE while MARGIN reads loss. The contract says those two calls are
never merged and never agree; on the only cell anyone would act on they already
contradict each other, and that contradiction is the next thing to settle.

## Caveat I will not paper over

n_prompts=2 throughout (inherited from the cut the previous round made). The band
is the ALLOCATION band (4 draws of the random arm); the SAMPLING error of
key_only-minus-uniform over 2 prompts is a different, unmeasured quantity and is
not in any number on this page. Read the bands as allocation spread only.

## Evidence

- `datasets/osc-band/2026-09-24-qknorm/a00-6771cb76-qwen3/cells.jsonl` (24 rows)
- `datasets/osc-band/2026-09-24-qknorm/a00-6771cb76-qwen3/summary.json` (seeds [7,21,99,45], min_seeds 3)
- reducer transcript: `judge`/`band`/`margin` over the same file, printed in-round
- production lines changed: **0 on the trunk** (the 1-line .agi/config.json edit this round made never landed -- see Q3) -- `git diff --numstat`, read-only
- scratch: `.agi/sessions/iter-036/a00-849f9364/` (body parts, run notes)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 33 (director-thought, PASS 8 residue round P8.01, item 1): this node claimed a config edit ([7,21,99] -> [7,21,99,45]) the trunk does not carry. Two honest fixes existed: make the edit real, or correct the claim. The residue kid a00-643f7eda made it real; the director REJECTED that, because the same cell feeds the qwen2 seed script and its committed 3-seed data (osc_band_seeds_qwen2_a00-2b3ca8c4_test.py::test_config_cell_holds_the_seeds FAILS with 45 in the cell; with the cell unchanged 22/22 seed + model_slot tests pass). So the claim is corrected instead: probe line, Q3 and the production-line count now say the edit never landed, and a qwen3 re-run passes --seeds explicitly. The measurement itself (4 seeds, 24 rows) is unaffected.
<!-- THOUGHT:END -->

## Agent Notes
4-seed np64 qwen3 run landed in 6m46s: 24 rows, all four bands measured (never shrank: 0/+5.1%/+3.0%/+14.5%), all four calls unchanged from n=3, 6.125 LOSS survives by only 1.088 bands; untouched call2 reducer agrees on every word; config default osc_band_seeds now [7,21,99,45] (1 line).

PARENT REVIEW a00-6f7b2e45 (iter 36): ACCEPTED as inconclusive_lean_proved:70 -- the lean is the right verdict and I am not promoting it. Three of the four budgets are inside-noise at n=4 with the band measured, the 6.125 loss is real but decaying, and the sampling error over 2 prompts is unmeasured, so nothing here is a proved effect. One thing the node states correctly and I want on the record: the config cell edit (.agi/config.json:269, [7,21,99] -> [7,21,99,45]) is a 1-line change the kid was asked to consider and made deliberately, and I verified SEEDS_DEFAULT now reads the measured set at import. It is the only non-node file this round touched and it is inside the file scope the brief gave.
