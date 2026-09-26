---
id: experiment:osc-band-call-rule-absent-seed
mint_id: a0056d3787f13c7ac0001
type: experiment
parents:
  - hypothesis:a00-56d3787f-13c7ab
edited_by: a00-56d3787f
loop: goal:band-call-rule-per-cell@s2
production_lines: 8
status: complete
tags:
  - osc-band
  - call-rule
  - n=1-trap
title: "Absent seed is n=1, and there is one rule module: the two holes parent probes P7 and P8 closed"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:osc-band-call-rule-absent-seed

**Parent** `hypothesis:a00-56d3787f-13c7ab`. Zero model, zero GPU: two edits to
the existing rule plus two fixtures. Bytes under `paths.local_maxxing.osc_dir`:
`osc_band_call2_a00-cc7b25cc.py` (+5/-2) and `osc_band_call_a00-ee9a5cdc.py` (+3/-1,
docstring only). **8 production lines added**, ceiling 40.

```
python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py \
                 .agi/context/local-maxxing/osc/test_osc_band_call_a00-ee9a5cdc.py -q
-> 15 passed (10 + 5; the 8 prior tests still green, so no regression on any earned cell)
```

## P7 -- ABSENT SEED IS NOT n=3

`n_seeds` counted `{d.get("seed", i) for i, d in enumerate(cell)}`, so a row with
no `seed` key fell back to its **row index** and three rows that vary reported
three distinct seeds. The 16 on-disk rows this whole goal exists to distrust
carry no `seed` field at all (`osc_band_matched_uniform_a00-a721f95f.py:74-77`),
so the exotic case was the likely one.

| | before | after |
|---|---|---|
| 3 rows, agree .50/.53/.56, **no** `seed` field | `('win', 'margin +0.37 vs band +0.06')` | `('unresolved', '3 of 3 random draws carry no seed: n=1 rows cannot band a call')` |
| 3 rows, seeds [7,7,7] | `unresolved` / "distinct" | `unresolved` / "distinct" (**unchanged**) |
| 3 rows, seeds 1/2/3, agree varies | `win` +0.07 | `win` +0.07 (**unchanged**) |

The gate is now two clauses, not one: a draw without a `seed` field is refused
outright, and fewer than 3 **explicitly seeded** distinct draws is refused after
it. Seed absence gets its own reason string, because "3 of 3 carry no seed" and
"fewer than 3 distinct seeds" are different defects with different owners -- the
first is the sweep writer's, the second is the caller drawing too little.

**First attempt was wrong and the test caught it.** The clause was written
`if len(v) != n`, i.e. rows-not-equals-distinct-seeds. That fires on
`[7,7,7]` too, so `test_p3_one_seed_repeated_three_times_is_unresolved` went red
with a "carry no seed" reason for a cell whose seeds are all present. The fix
counts rows **lacking the key** (`len(v) != len(seeded)`), which is the quantity
the reason string actually names. This is the assertion working.

## P8 -- TWO RULE MODULES, ONE RULE

`osc_band_call_a00-ee9a5cdc.py` is now marked DEPRECATED in its own docstring and
points at its successor. Not deleted: it is prior art, its 5 tests still pass, and
`test_osc_band_call2_a00-cc7b25cc.py:17` still imports it deliberately as the
falsifying contrast -- the P3/P4/P7 holes are only demonstrable against the old
module, so retiring it as a source is compatible with keeping it as evidence.
**Not done:** the old module is still importable and still returns `win` on a
degenerate band. A `DEPRECATED` docstring is a label, not a gate; nothing stops
a third caller from importing it. Closing that needs a caller's decision, not a
kid's.

## What this does NOT establish

- Still **no real draws** have passed through the rule. Every fixture is
  hand-written, so the band scale and sign convention are pinned and the
  magnitudes at `qwen2@5.25` are not. Slices (A)/(B) own that.
- The refusal is per-metric, and a mixed cell still emits one word and one
  refusal; that behaviour is inherited from `experiment:osc-band-call-rule-total`
  and was not re-derived here.
- P7's fix makes the 16 existing on-disk cells **uncallable** -- by design, but
  it means no `goal:g5.22.1` cell can be called until a seed sweep writes a
  `seed` field. That is the intended consequence, and it is a claim about the
  sweep writer that nobody has tested.
- 8 production lines, so nothing here is near the ceiling; the two holes were
  cheap because the previous kid's module was already one function away.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The round's real finding is the failed first attempt, not the passing suite:
`len(v) != n` is a plausible-looking count that means "rows" on one side and
"distinct seeds" on the other, and it only differs from the truth on a cell that
varies -- which is exactly the cell that was supposed to be called. A gate whose
false-positive lands on the one input it exists to protect is worse than no gate,
because it reads as a refusal of a different defect. Recorded so the next kid
who writes a two-clause gate counts the thing each clause names.
<!-- THOUGHT:END -->
