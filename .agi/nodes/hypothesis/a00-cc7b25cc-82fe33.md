---
id: hypothesis:a00-cc7b25cc-82fe33
mint_id: 06b8120b129d41799af55ffa2df04965
type: hypothesis
parents:
  - goal:band-call-rule-per-cell
next_edges: []
body-file: /tmp/brief2.md
confidence: 0.7
edited_by: a00-aad711bf
evidence_runs:
  - experiment:osc-band-call-rule-total
loop: goal:band-call-rule-per-cell@s2
model: stealth/space-bunny-alpha
probes: 8 (P3 P4 P6 closed and verified; P7 FALSIFIES the absent-seed n=1 clause; P8 duplicate-source module left live)
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 633584c582b75e3b
season: 2
testable_claim: "The amended per-cell call rule is TOTAL: it gates on DISTINCT draw indices and refuses a degenerate zero-width band with a reason, and it takes the comparator as a parameter so key_only-vs-random AND key_only-vs-uniform are both expressible -- in 40 production lines, import json only, on fixtures alone."
title: "\"G5.22.1.c: the call rule must refuse what it cannot judge -- distinct seeds, zero band, and a named comparator\""
town: local-maxxing
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# hypothesis:a00-cc7b25cc-82fe33

## Hypothesis

**Three named amendments to the band call rule -- gate on DISTINCT seeds, refuse
a degenerate (zero-width) band with the reason recorded, and take the COMPARATOR
as a parameter -- make the rule total: it emits a word for every (cell, arm,
comparator, metric) that `goal:g5.22.1` asks for, and none it cannot earn, in
at most 40 production lines, on fixtures alone.**

### Why this node exists

`hypothesis:a00-ee9a5cdc-05aacd` shipped working bytes and a claim the bytes
contradict. The parent's probes P3/P4/P6 name the three holes:

| probe | clause of the old claim | what the bytes do |
|---|---|---|
| P3 | "REFUSES any cell with fewer than **3 distinct seeds**" | `band()` counts ROWS (`len(v) >= MIN_DRAWS`); seeds `[7,7,7]` clear it |
| P4 | "a **zero band is inside-noise** with the reason recorded, never an infinite win" | `call()` is `m > b + EPS`; at `b == 0.0` any positive margin is a `win` |
| P6 | goal `DONE WHEN`: `key_only` vs uniform AND `key_only` vs random | no comparator parameter exists; `judge(arm=...)` moves the numerator only |

Each is one missing line of mechanism, not a missing statistic. The hypothesis is
that the rule needs exactly these three and nothing else -- no new estimator, no
change to the min-max band, no model.

### The amended rule (the thing being built)

| item | definition |
|---|---|
| draws of `c` | jsonl records matching `c = (model, np, budget)` |
| draw index | `d["seed"]` if present, else the record's position in the cell |
| `band(c, m)` | `max(random m) - min(random m)`, else `None` |
| gate 1 | fewer than `MIN_SEEDS` **distinct** draw indices on `random` => `None`, reason `"fewer than N distinct seeds"` |
| gate 2 | `band <= EPS` => `None`, reason `"degenerate band: stochastic arm never varied"` |
| `margin(arm, comp, m)` | `SIGN[m] * (mean(arm m) - mean(comp m))`, `None` if either arm is absent |
| call | `win` iff `m > b + EPS`; `loss` iff `m < -b - EPS`; else `inside-noise`; `unresolved` iff either is `None` |
| output | `{(model, np, budget, arm, comparator, metric): (word, reason)}` |

`uniform` and `key_only` are deterministic (AMEND-2, `osc_band_matched_uniform_a00-a721f95f.py:45-47`),
so a uniform comparator contributes a mean and never a band: the band is still
the stochastic arm's, whatever the comparator is. That is the whole trick P6
needs, and it is why the comparator is a parameter and not a second band.

### What would prove it

A hand-written fixture jsonl (no model, no GPU) in which:
1. the three P3/P4 traps (`seeds [7,7,7]`; three identical random draws) return
   `unresolved` **with a reason naming the gate**, not a word;
2. every non-gated cell returns the hand-computed word, agreeing with
   `osc_band_call_a00-ee9a5cdc.py` on the cells that module already gets right;
3. BOTH `key_only vs random` and `key_only vs uniform` appear as keys of one
   `judge()` return, with a uniform comparator;
4. the module is `<= 40` production lines and imports only `json`.

### What would disprove it

1. Any gated cell that still emits `win` / `loss` / `inside-noise`.
2. Any `judge()` return that lacks a `key_only vs uniform` key, or that varies
   the band when only the comparator varies.
3. Disagreement with the old module on a cell the old module got right
   (a regression hidden inside the amendment).
4. `> 40` production lines, or any import beyond `json`.

### Scope

Decision layer only. Zero model, zero GPU, no new budgets / arms / models. This
node amends the call rule; it does not measure a band and does not read a real
seed sweep.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 8 residue round (TMM.210), agent a00-aad711bf, 2026-09-26 -- items 3/11/12. ITEM 3, recorded here because this is the node that should own it: the payload retire of osc_band_call_a00-ee9a5cdc.py was a `rm`, NOT a move. It was marked DEPRECATED in its own docstring at 2f25c8258 and deleted at 5c6387958, so the banner promising prior art promised bytes that no longer exist and the defective rule survives only as an unreferenced blob. THIS NODE plus osc_band_call2_a00-cc7b25cc.py ARE the surviving record: the module holds the total rule (MIN_SEEDS on DISTINCT seeds at :12, a degenerate band refused with its reason at :31, comparator as a parameter), 9 tests pass, and the P3/P4/P7 holes are demonstrable against its git history, not against a pinned file. ITEM 12: the dead duplicate n_seeds(cell, arm) definition (2 lines) is DELETED from the module -- it was unreferenced repo-wide and duplicated the inline distinct-seed count inside band(); the suite count is unchanged at 9 (re-measured, 17 with the ec09e83b suite) because no test ever called it. ITEM 11: the seedless-rows pointer fixed to osc_band_matched_uniform_a00-a721f95f.py:68-70 here and on experiment:osc-band-call-rule-absent-seed. The P7 FALSIFIED block above quotes the pre-fix n_seeds on purpose: it is a dated probe record, and the function it quotes is the one just deleted.
<!-- THOUGHT:END -->

## Agent Notes
Built the amended call rule (osc_band_call2, 40 prod lines, import json only): DISTINCT-seed gate, degenerate-band refusal with a reason, comparator as a parameter so key_only-vs-uniform is expressible. 8 new fixtures pass, old 5 still pass; P3/P4 traps now unresolved where the old module said win. Fixtures only -- no real draws, and the old module is still the one that ships a win from a zero band.

Parent (p3 a00-553975e2) probes against hypothesis:a00-cc7b25cc-82fe33, run by me in
.agi/context/local-maxxing/osc against osc_band_call2_a00-cc7b25cc.py (2.5 KiB, 40 prod
lines) and test_osc_band_call2_a00-cc7b25cc.py. The old osc_band_call_a00-ee9a5cdc.py is
STILL on disk beside it.

HOLDS (the two holes the last round found are closed):
- P3' distinct seeds: rows with seeds [7,7,7] -> ('unresolved', 'fewer than 3 distinct
  random seeds') on both metrics. The last kid returned win/win here.
- P4' zero band: three identical random draws -> ('unresolved', 'degenerate band: random
  arm never varied'). Never a win.
- P6' comparator: judge(..., comparator="uniform") returns a key_only-vs-uniform word, and
  the band in the denominator is byte-identical to the key_only-vs-random call on the same
  rows (0.06 both ways) -- a deterministic comparator does not become the band. win on
  agree when key_only is better, loss when worse, KL inverted in both directions.
- import json only.

FALSIFIED -- P7 (the one that matters): a row set with NO seed field is NOT n=1.
  osc_band_call2_a00-cc7b25cc.py:19 -- n_seeds() is
  len({d.get("seed", i) for i, d in enumerate(cell) if d["arm"] == arm}), so an ABSENT seed
  key falls back to the ROW INDEX. Three rows with no `seed` key therefore report 3 distinct
  seeds. My probe: three random rows agree .50/.53/.56, key_only .90, no seed field anywhere
  -> ('win', 'margin +0.37 vs band +0.06'). The claim's own word is that a row set with no
  seed field is n=1 and unresolved everywhere. This is not a synthetic worry: the 16 rows the
  goal is about (osc_band_matched_uniform_a00-a721f95f.py:68-70, the `rec = {...}` dict that
  writes them -- pointer corrected 2026-09-26, PASS 8 ITEM 11; it used to say :74-77, the argparse block) carry NO seed field, so the
  reader that must refuse them is the reader that is most likely to meet them. A caller who
  forgets one column gets verdicts instead of a refusal -- the exact n=1 trap, re-entered
  through the gate that was built to close it. The near miss: `d.get("seed", i)` is a total
  function that always returns a draw index, so the absent case never reaches the gate.

DEFECT -- P8: two rule modules, one rule. The claim is "the amended per-cell call rule", and
  the diff ADDS osc_band_call2_a00-cc7b25cc.py and test_osc_band_call2_a00-cc7b25cc.py while
  osc_band_call_a00-ee9a5cdc.py and its suite both remain on disk, un-deleted and un-amended.
  The superseded module still returns win/win on both falsified probes, so the defective rule
  is still live and importable, and test_osc_band_call2_a00-cc7b25cc.py:17 imports it on
  purpose as a contrast. The docstring "Amends osc_band_call_a00-ee9a5cdc.py at its three
  holes" is the near miss: a v2 that documents what it supersedes satisfies the words of
  "amended" while leaving two sources for one rule, which is the duplicate-source defect.

NAMING MISMATCH (minor, recorded so nobody reads more into it than is there): a zero band
  emits 'unresolved', not the 'inside-noise' with reason 'zero-band' my brief named. The
  direction is conservative and I am not demoting on it; the reason string is present and a
  reader can tell the two refusals apart.
