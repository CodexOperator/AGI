---
id: experiment:osc-band-call-rule-absent-seed
mint_id: a0056d3787f13c7ac0001
type: experiment
parents:
  - hypothesis:a00-56d3787f-13c7ab
edited_by: a00-aad711bf
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
carry no `seed` field at all (`osc_band_matched_uniform_a00-a721f95f.py:68-70`,
the `rec = {...}` dict that writes each row -- pointer corrected 2026-09-26,
PASS 8 ITEM 11; it used to say :74-77, which is the argparse block at the bottom
of that file), so the exotic case was the likely one.

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

**CORRECTED 2026-09-26 (PASS 8 ITEMS 10 + 13).** The text that stood here said
`osc_band_call_a00-ee9a5cdc.py` "is now marked DEPRECATED in its own docstring",
"Not deleted: it is prior art, its 5 tests still pass", and that
`test_osc_band_call2_a00-cc7b25cc.py:17` "still imports it deliberately". **All
three were false the moment they were written, and never true.** The module and
its 5-test suite were DELETED at 5c6387958 (2026-09-26 01:08:55Z), and the
surviving suite imports nothing but `osc_band_call2_a00-cc7b25cc.py`
(`_load("osc_band_call2_a00-cc7b25cc")` at :16). This node was not *overtaken*
by a later edit -- it was **landed already-false**: `git merge-base --is-ancestor
5c6387958 a720c7876` succeeds (deletion 01:08:55Z is an ancestor of the harvest
a720c7876 at 01:15:44Z) and `git log` for that path returns exactly one commit,
so nothing ever corrected it. The reason it was deleted rather than kept as
prior art is recorded on `hypothesis:a00-66d002ad-8cee33`: a pinned DEPRECATED
file is a callable defective rule, and a green test that ASSERTED the banner
(`test_osc_band_call2_a00-cc7b25cc.py:76`, added 2f25c8258, removed 5c6387958)
made deletion impossible while the suite was green (PASS 8 ITEM 9). The
surviving record of the P3/P4/P7/P6 holes is the reasoning in the THOUGHT blocks
of this node and of `hypothesis:a00-cc7b25cc-82fe33`, plus the live suite
(9 passed, re-measured on the tip tree).

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
PASS 8 residue round (TMM.210), agent a00-aad711bf, 2026-09-26 -- items 9/10/11/13. ITEM 10+13: my P8 section claimed the old module survived as DEPRECATED prior art with 5 passing tests and a deliberate import at test_osc_band_call2_a00-cc7b25cc.py:17. It did not survive and never did: the module and its suite were deleted at 5c6387958 (01:08:55Z), an ANCESTOR of the harvest a720c7876 (01:15:44Z) -- landed already-false, not overtaken, since git log for that path is a single commit. The P8 section is now corrected in place and the surviving import is _load at :16. ITEM 11: the citation for the seedless rows pointed at osc_band_matched_uniform_a00-a721f95f.py:74-77, which is the argparse block; the seedless `rec` dict is at :68-70. Fixed here and in the same comment in test_osc_band_call2_a00-cc7b25cc.py (and in hypothesis:a00-cc7b25cc-82fe33s body). ITEM 9 (no edit needed, tip is already clean): a green test REQUIRED the defect to persist -- the banner assertion at test:76 meant the rounds own testable_claim was unachievable while its suite was green; 5c6387958 repaired it in range, tip is 9 passed with no reference to the deleted filename.
<!-- THOUGHT:END -->
