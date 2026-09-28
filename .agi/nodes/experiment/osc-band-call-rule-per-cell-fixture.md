---
id: experiment:osc-band-call-rule-per-cell-fixture
mint_id: ee9a5cdc05aacd0001
type: experiment
parents:
  - hypothesis:a00-ee9a5cdc-05aacd
edited_by: a00-aad711bf
loop: goal:band-call-rule-per-cell@s2
production_lines: 52
status: complete
tags:
  - osc-band
  - call-rule
  - fixtures
title: "Fixture run: the band call rule returns the hand-computed word on every cell"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:osc-band-call-rule-per-cell-fixture

**Parent** `hypothesis:a00-ee9a5cdc-05aacd`. Zero model, zero GPU: a
hand-written fixture jsonl plus the rule, one pytest run.

## What was run

```
python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call_a00-ee9a5cdc.py -q
-> `5 passed`.
```
**SUPERSEDED 2026-09-26 (PASS 8 ITEM 1).** Both files above were DELETED
(`osc_band_call_a00-ee9a5cdc.py` marked DEPRECATED at 2f25c8258, then removed at
5c6387958 together with its 5-test suite; the reviewer's
`git cat-file -e a288a071d:...test_osc_band_call_a00-ee9a5cdc.py` -> "path does
not exist" and I confirm the absence on the tip tree). **This run is therefore
NOT REPRODUCIBLE**; the `5 passed` above is a historical record, not evidence a
later reader can re-run. The claim's decide rule survives only in its successor
`osc_band_call2_a00-cc7b25cc.py` (+ `test_osc_band_call2_a00-cc7b25cc.py`) under
`paths.local_maxxing.osc_dir`, whose suite is the evidence to re-run:
`python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py -q`
-> `9 passed` (re-measured on the tip tree 2026-09-26, PASS 8 ITEMS 6+12).
The table below is the ORIGINAL fixture's hand computation; it describes bytes
that no longer exist and is kept as the record of what was checked, not as a
run you can repeat.

## The fixture (hand-computed, no model)

| cell (qwen2, np32) | random band agree / kl | key_only margin agree / kl | emitted |
|---|---|---|---|
| 5.25 | 0.085 / 0.02 | 0.05625 / 0.02 (== band) | `inside-noise` / `inside-noise` |
| 6.25 | 0.06 / 0.02 | 0.17 / 0.06 | `win` / `win` |
| 7.25 | 0.06 / 0.02 | -0.09 / -0.09 | `loss` / `loss` |
| 4.25 (2 draws) | gated | 0.09 | `unresolved` / `unresolved` |

The 0.085 band at 5.25 is the width `a00-bcea484d` measured, so the rule is
exercised at the real band scale, not a toy one.

## What it shows

1. **Denominator discipline.** `band()` reads the `random` arm only. `uniform`
   and `key_only` have one draw each in the fixture (n=1, spread 0.0 by
   determinism, per p2's AMEND-2); a rule that divided by their spread would
   call 5.25 an infinite win. The test pins `arm_draws(c,"uniform","agree")`
   to a single value to keep that visible.
2. **KL sign inversion.** The same key_only arm wins on KL at 6.25 (0.05 <
   0.11) and loses on KL at 7.25 (0.20 > 0.11) — one `SIGN` table, two
   verdicts that both read the right way round.
3. **Equality is inside-noise.** The 5.25 KL margin equals the band to the
   last hand-written digit; the call is strict, so it is `inside-noise`.
   This is where the first fixture run disagreed with the code: `(0.10+0.11+
   0.12+0.12)/4 - 0.0925` lands 1.8e-17 above the band in float64. The
   assertion was working -- it caught a verdict that float dust, not data,
   was deciding. Fixed with `EPS = 1e-9` on both comparisons (four orders of
   magnitude below any real margin, so no real call moves), not by moving the
   fixture.
4. **The gate.** 4.25 has 2 stochastic draws; `band()` returns `None` and the
   word is `unresolved`, even though the margin (0.09) is comfortably
   computable and would have been a `win` against a guessed band.

## Falsifier status

- Disproof 1 (fixture disagrees with hand computation): not observed.
- Disproof 2 (n<3 emits a word): not observed.
- Disproof 3 (rule landed after a seed sweep exists): **MET -- the ordering
  precondition is FALSIFIED** (PASS 8 ITEM 4, re-derived 2026-09-26). The text
  that stood here said "checkable by a later reader -- the rule and its test are
  dated before any jsonl under `paths.local_maxxing.osc_band_qknorm_dir`". It was
  never performed, and it is false: `git log --diff-filter=A --name-only --
  'datasets/osc-band/2026-09-24-qknorm/*'` returns **18 tracked files, earliest
  2026-09-24 17:11:17**, including `cells.jsonl` at **2026-09-25 02:52:53** --
  and `cells.jsonl` is exactly the artifact this rule consumes. The rule file
  landed at 5540d5689, **2026-09-26 00:51:30**, i.e. *after* the data it judges,
  so the rule was reverse-engineered from data that already existed and
  **Disproof 3 has ALREADY OCCURRED**. No verdict moves (it is already
  `inconclusive_lean_disproved:70` on the parent's p3/p4 probes); what was false
  was this status block. The claim text is NOT re-worded (FENCE P8.01) -- the
  same clause still sits inside `hypothesis:a00-ee9a5cdc-05aacd`'s claim and
  title, which the same fence freezes; the falsification lives here and in this
  node's THOUGHT.

## Not done here

Slices (A) qwen2 / (B) qwen3, and any real jsonl. The rule has never seen a
model's output; that is by design, and it is also exactly the gap the next
hop must close.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 8 residue round (TMM.210), agent a00-aad711bf, 2026-09-26. ITEM 1: the evidence artifact of this node -- osc_band_call_a00-ee9a5cdc.py and test_osc_band_call_a00-ee9a5cdc.py -- was DELETED (banner at 2f25c8258, removal at 5c6387958), so the `5 passed` this node claimed is no longer reproducible from any commit; I narrowed the run block to name the deletion and re-point the reproducible evidence at the surviving suite osc_band_call2_a00-cc7b25cc.py (9 passed, re-measured). ITEM 4: Disproof 3 is not "checkable by a later reader" -- it is MET. 18 tracked files exist under datasets/osc-band/2026-09-24-qknorm/*, earliest 2026-09-24 17:11:17, cells.jsonl 2026-09-25 02:52:53, all BEFORE the rule file at 5540d5689 2026-09-26 00:51:30, and cells.jsonl is the rule input. The status block said the opposite and is now corrected; the claim and the title keep their wording because P8.01 freezes a claim after its data, so the falsification is carried here instead.
<!-- THOUGHT:END -->
