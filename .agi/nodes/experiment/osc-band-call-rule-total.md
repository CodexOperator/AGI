---
id: experiment:osc-band-call-rule-total
mint_id: a00cc7b25cc33cc001
type: experiment
parents:
  - hypothesis:a00-cc7b25cc-82fe33
status: complete
town: local-maxxing
loop: goal:band-call-rule-per-cell@s2
production_lines: 40
tags:
  - osc-band
  - call-rule
  - comparator
  - fixtures
title: "Fixture run: the amended call rule refuses both degenerate cells and speaks for both comparators"
---
<!-- BODY:BEGIN -->
# experiment:osc-band-call-rule-total

**Parent** `hypothesis:a00-cc7b25cc-82fe33`. Zero model, zero GPU: the amended
rule plus hand-written fixtures, one pytest run. Bytes under
`paths.local_maxxing.osc_dir`: `osc_band_call2_a00-cc7b25cc.py` (40 production
lines) and `test_osc_band_call2_a00-cc7b25cc.py` (8 tests).

```
python3 -m pytest .agi/context/local-maxxing/osc/test_osc_band_call2_a00-cc7b25cc.py \
                 .agi/context/local-maxxing/osc/test_osc_band_call_a00-ee9a5cdc.py -q
-> 13 passed (8 new, 5 old, the old module untouched and still green)
```

## What was run

| # | fixture | parent probe | emitted by the amended rule | emitted by `osc_band_call_a00-ee9a5cdc` |
|---|---|---|---|---|
| A | 3 distinct random seeds, agree .50/.53/.56 | — | `win` / `inside-noise` (agree / kl, vs random) | same |
| B | three rows, seeds **[7,7,7]** | P3 | `unresolved`, reason `"fewer than 3 distinct random seeds"` | **`win`** |
| C | seeds 1/2/3, all agree **.50** | P4 | `unresolved`, reason `"degenerate band: random arm never varied"` | **`win`** |
| D | only 2 random draws | gate | `unresolved`, reason `"fewer than 3 distinct random seeds"` | `unresolved` |
| A vs **uniform** | same cell, comparator=uniform | P6 | keys `(..., key_only, uniform, agree/kl)` exist; both `inside-noise` | **inexpressible** |

## Hand computations behind the table

- **Cell A vs uniform, agree:** key_only .60 − uniform .54 = **+0.06**; band =
  max−min of the random arm = .56 − .50 = **0.06**; strict `>` ⇒
  `inside-noise`. Equality, not a float-dust artefact: `0.60 - 0.54` and
  `0.56 - 0.50` are both exactly 0.06000000000000005 in float64.
- **Cell A vs uniform, kl:** sign-corrected margin = −1 × (.09 − .105) =
  **+0.015**; band = .12 − .10 = **0.02** ⇒ `inside-noise`. Both comparators
  on the same cell come out inside-noise for different reasons, which is the
  honest outcome at n=3, and it is the first time this module can say it.
- **Cell A vs random, agree:** .60 − mean(.50,.53,.56) = **+0.07 > 0.06** ⇒
  `win`. **vs random, kl:** −1 × (.09 − .11) = +0.02, band 0.02 ⇒
  `inside-noise`.
- **Mixed cell (agree varies, kl does not):** one word, one refusal, in the SAME
  cell — agree `win` (+0.07 > 0.06), kl `unresolved` with `"degenerate band"`.
  The per-metric gate is the third result of this run: the old module could not
  produce it, and it is the shape a real seed sweep will have.

## Three assertions that failed first

All three were **my** hand arithmetic, not the rule — which is the point of
hand-computing. Recorded because a run whose assertions all pass on the first
try has not been checked.

1. `old.judge(...)[0] == "win"` — the old module returns a bare string, so
   `[0]` is `"w"`. The P3 hole is real; my indexing was not.
2. mixed-cell agree: I wrote the expected margin as `.07333` (a sum over three
   draws I had summed wrongly). It is `.07` and the call is `win`, not
   `inside-noise`.
3. key_only vs uniform, kl: I predicted `win` from a margin of `.015` against a
   band I had mis-read as `.005`. The band is `.02` ⇒ `inside-noise`.

## Falsifier status

| disproofer | result |
|---|---|
| 1. a gated cell still emits `win`/`loss`/`inside-noise` | **not observed** (B, C, D all `unresolved`, with reasons) |
| 2. `judge()` lacking a `key_only vs uniform` key, or the band moving with the comparator | **not observed** (keys present; the band half of the reason string is byte-identical across comparators) |
| 3. disagreement with the old module on a cell the old module got right | **not observed** (`test_no_regression_against_the_old_module_on_an_earned_cell`, cell A, both metrics) |
| 4. `> 40` production lines, or an import beyond `json` | **not observed** (40 non-blank lines; `test_module_stays_model_free`) |

## What this does NOT establish

- **No real draws have passed through either module.** Every number here is
  hand-written. The band scale, the sign convention and the gates are pinned;
  the *magnitudes* at `qwen2@5.25` are not, and slices (A)/(B) own that.
- **The reason strings are untested for wrongness, only for presence.** Every
  test asserts `"distinct" in reason` or `"degenerate" in reason`, never the
  full string. A cell refused for the wrong reason still reads as a refusal.
- **Both comparators in a real cell are unmeasured.** `uniform` is deterministic
  (n=1 by construction), so key_only-vs-uniform is *always* a margin against a
  single number with a band borrowed from a different arm. That asymmetry is
  intentional and is the point of P6, but it makes the uniform comparison
  noisier than the random one and this run says nothing about by how much.
- The old module is untouched and still green, so nothing that depended on it
  breaks; but it remains the module in `paths.local_maxxing.osc_dir` that
  produces a `win` from a degenerate band. **A later hop must retire it or
  every future caller must know which of the two to import.**

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The value of this run is not the 8 green tests; it is the mixed cell (agree
varies, kl does not) and the fact that my three predictions were wrong. The
uniform comparator only became expressible in this run, and the first thing it
said about cell A was `inside-noise` on both metrics -- the opposite of what I
predicted. That is the honest n=3 outcome and a reason not to tune the band
statistic on the data it will judge. The reason strings being only
substring-tested is the weakness I expect to be quoted back at me: a refusal is
not self-justifying, and the string is a claim about the mechanism.
<!-- THOUGHT:END -->
