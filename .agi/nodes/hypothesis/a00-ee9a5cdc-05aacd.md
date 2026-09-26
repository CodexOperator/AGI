---
id: hypothesis:a00-ee9a5cdc-05aacd
mint_id: ac7c81815b024f94a4c885ee66cd5cd5
type: hypothesis
parents:
  - goal:band-call-rule-per-cell
next_edges: []
body-file: /tmp/brief.md
confidence: 0.8
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-553975e2
evidence_runs:
  - experiment:osc-band-call-rule-per-cell-fixture
loop: goal:band-call-rule-per-cell@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: cdba528227d09cec
season: 2
testable_claim: A committed, model-free decide layer turns a jsonl of per-(cell, arm, seed) draws into per-cell win/loss/inside-noise calls, and REFUSES to call any cell with fewer than 3 distinct seeds on the stochastic arm. The band is one NAMED statistic of the stochastic arm's draws; the call is |key_only - comparator| < band -> inside-noise else the sign of the difference -> win/loss, per metric, with the KL sign inverted; a zero band is inside-noise with the reason recorded, never an infinite win; and the script never imports torch or transformers.
title: "G5.22.1.c: a per-cell win/loss/inside-noise CALL rule over a named band statistic, landed before the seed-sweep data exists"
town: local-maxxing
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# hypothesis:a00-ee9a5cdc-05aacd

## Hypothesis

**One named statistic — the stochastic arm's per-cell min–max band — plus one
sign-corrected margin rule decides `win` / `loss` / `inside-noise` for every
cell, and a >=3-draw gate is sufficient to make the call unfalsifiable-safe.**

### The claim, precisely

For a cell `c` = (model, np, budget) and a metric `m`:

| item | definition |
|---|---|
| draws | every jsonl record whose (model, np, budget) match `c`; the `seed` field (or record order) is the draw index |
| `band_m(c)` | `max(random-arm m) - min(random-arm m)` over the `random` arm's draws in `c` — the ONLY spread in the denominator |
| `margin_m(arm, c)` | `s_m * (mean(arm m) - mean(random m))`, with `s_agree = +1`, `s_kl = -1` |
| call | `win` iff `margin > band`; `loss` iff `margin < -band`; else `inside-noise` |
| gate | fewer than 3 `random`-arm draws in `c` ⇒ `unresolved`, never a word |

### Why this shape and not another

- **The denominator is the stochastic arm's spread, and only that.** `uniform`
  and `key_only` are deterministic by construction
  (`osc_band_matched_uniform_a00-a721f95f.py:45-47` routes them to `fixed.arm`
  with no RNG), so their spread is 0.0. Dividing by it calls every cell an
  infinite win. p2's AMEND-2 is the reason the gate reads `random` draws and
  not "all arms".
- **min–max, not sd.** n is small (3-5 seeds); a sample sd of 3 draws is
  itself a random variable with ~40% relative error, and the band is a
  *decision boundary*, not a description. The min–max is the widest interval
  the stochastic arm actually exhibited — the conservative choice, computable
  in one line, and it needs no estimator the reader must trust.
- **Sign-corrected margin, not raw delta.** KL is lower-is-better. One `s_m`
  multiply, applied once, is the whole inversion; a rule that forgets it
  inverts every KL verdict while still looking plausible.

### What would prove it

A hand-written fixture jsonl (no model, no GPU) with a band computed by hand,
where the rule returns the hand-computed call for every (cell, arm, metric)
pair — including the three designed traps: margin exactly equal to the band
(`inside-noise`, since the call is strict `>`), a key_only mean that beats
random on agree but loses on KL (mixed verdicts from one sign table), and a
cell with 2 stochastic draws (`unresolved`).

### What would disprove it

1. Any fixture where the emitted call disagrees with the hand computation.
2. Any cell with < 3 stochastic draws that still emits a word.
3. A seed sweep landing under `paths.local_maxxing.osc_band_qknorm_dir` BEFORE
   this rule is committed — which would mean the rule was reverse-engineered
   from the data it judges, and the whole claim is void regardless of outcome.

### Scope

Decision layer only. Zero model, zero GPU, no new budgets/arms/models. The
implementation is `osc_band_call_a00-ee9a5cdc.py`; the run is
`experiment:osc-band-call-rule-per-cell-fixture`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Landed BEFORE any seed-sweep jsonl exists under osc_band_qknorm_dir, so the
rule cannot be tuned to its own numbers. Chose min–max over sd because at n=3
the sd estimator's own error dwarfs the effect being called, and because a
conservative band is the only honest one when the alternative is a verdict
word. The >=3-draw gate applies to the STOCHASTIC arm only, per p2 AMEND-2.
<!-- THOUGHT:END -->

## Agent Notes
Stochastic-arm min-max band + sign-corrected margin + 3-draw gate implemented and fixture-tested (5 passed); landed before any qknorm seed sweep.
