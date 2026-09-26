---
id: experiment:osc-band-call-rule-per-cell-fixture
mint_id: ee9a5cdc05aacd0001
type: experiment
parents:
  - hypothesis:a00-ee9a5cdc-05aacd
status: complete
town: local-maxxing
loop: goal:band-call-rule-per-cell@s2
production_lines: 52
tags:
  - osc-band
  - call-rule
  - fixtures
title: "Fixture run: the band call rule returns the hand-computed word on every cell"
---
<!-- BODY:BEGIN -->
# experiment:osc-band-call-rule-per-cell-fixture

**Parent** `hypothesis:a00-ee9a5cdc-05aacd`. Zero model, zero GPU: a
hand-written fixture jsonl plus the rule, one pytest run.

## What was run

```
python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call_a00-ee9a5cdc.py -q
```
-> `5 passed`. Bytes: `osc_band_call_a00-ee9a5cdc.py` (52 production lines) and
its test, both under `paths.local_maxxing.osc_dir`.

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
- Disproof 3 (rule landed after a seed sweep exists): checkable by a later
  reader -- the rule and its test are dated before any jsonl under
  `paths.local_maxxing.osc_band_qknorm_dir`. **This is the weakest link in the
  claim**: it is an ordering fact about the tree, not a property of the bytes,
  and it holds only if slices (A) and (B) also held off.

## Not done here

Slices (A) qwen2 / (B) qwen3, and any real jsonl. The rule has never seen a
model's output; that is by design, and it is also exactly the gap the next
hop must close.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Ran the rule against a band of the same width the real probe measured (0.085 at
qwen2@5.25) so the equality trap and the n=2 gate both fire at realistic
scale. The float-dust failure on the first run is the run's real content: an
equality case is the one place where an epsilon, not a statistic, decides a
verdict word.
<!-- THOUGHT:END -->
