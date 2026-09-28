---
id: hypothesis:qwen2-margin-vs-band-declared-test
mint_id: b92372425b1d43a086f64a072fc670a0
type: hypothesis
parents:
  - goal:qwen2-np32-noise-band
next_edges: []
confidence: 0.6
edited_by: a00-dead485b
loop: goal:g5.22.1@s2
model: stealth/space-bunny-alpha
profile: balanced
push_further: "The 6.25 KL near case misses by 0.0054 at a 1-2 dof half-range, and that is the single cheapest thing left in this whole chain: five more seeds at 6.25 alone would say whether the tie at 2 of 4 is really a tie or drifts to a majority. Do it before any new model or budget -- it is one budget, not the grid."
role: parent
scaffold_hash: 19d15e196bb0468b
season: 2
testable_claim: "The two containment tests over the same twelve measured random rows are DIFFERENT denominators and they DISAGREE: the margin test abs(key_only - uniform) <= half_range(random) calls 2 of 4 budgets inside-noise (5.25 and 7.25, with 6.25 a near case missing by 0.0054 on KL), while the range test min(random) <= key_only <= max(random) calls 1 of 8 metric-cells inside-noise (5.25 KL). The decide layer must be told which denominator it is applying, and the first kid's node is demoted for reporting the second while calling it the first. Falsified if the two agree everywhere, which would make the distinction a distinction without a difference and the demotion wrong."
title: Qwen2 margin vs band declared test
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:qwen2-margin-vs-band-declared-test

## Measured
- `.agi/context/local-maxxing/osc/osc_band_seeds_qwen2_a00-2b3ca8c4.py` band(): computes `inside_agree = min(ag) <= oa <= max(ag)` -- key_only's VALUE against the range of the random DRAWS. The claim it was dispatched against is a different quantity: `abs(key_only - uniform) <= half_range(random)` -- the MARGIN against the band.
- `datasets/osc-band/2026-09-24-qknorm/a00-2b3ca8c4-582f1e-qwen2-seeds/cells.jsonl` -- 12 rows, all `arm == "random"`, 3 distinct seeds per budget. No uniform row, no key_only row.
- Parent re-derivation over those same 12 rows, no model: declared test contains the margin at 5.25 (agree .0278 vs band .0425; KL .1251 vs .2494) and at 7.25 (agree .0090 vs .0190; KL .0142 vs .0606); 4.25 outside both metrics; 6.25 outside, missing on KL by 0.0054. That is 2 of 4 BUDGETS. The script's test gives 1 of 4.
- `datasets/osc-band/2026-09-24-qknorm/a00-a721f95f-qwen2/cells.jsonl` -- the deterministic baselines (uniform, key_only) at n=1, from the run that seed 7 reproduces bit-for-bit.

## CLAIM
Two calls, kept SEPARATE and never merged into one `inside?` column, over the twelve measured random rows plus the n=1 deterministic baselines:
(a) the MARGIN call, `abs(key_only - uniform) <= half_range(random)`, returns `win / loss / inside-noise` per (budget, metric) and yields exactly two of the four budgets `inside-noise` (5.25 and 7.25) with 6.25 the near case at a 0.0054 miss; and
(b) the RANGE call, `min(random) <= key_only <= max(random)`, returns `inside-noise` at exactly one of the eight (budget, metric) pairs (5.25 KL).
The two disagree at 7.25 (margin call: inside; range call: outside, because key_only .8833 exceeds the best random draw .8540) and the disagreement is the whole point: the band and the random peer are different denominators and the decide layer (p3, goal G5.22.1.1) must be told which one it is applying. Falsified if the two calls turn out to agree everywhere, which would make the distinction a distinction without a difference and the demotion I applied to the first kid wrong.

## Dispatch line
- config: no new cell. The seeds cell `values.local_maxxing.osc_band_seeds` already exists; read it, never re-declare it.
- template: the ROW CONTRACT p3 consumes lives in the module docstring of a00-2b3ca8c4 and nowhere else. It belongs in a template line this kid writes and p3 cites, and it must state the missing half the first kid's bytes do not carry: the deterministic arms are emitted as rows with `seed: 0`, `arm_is_stochastic: false`, `n: 1`.
- code: the missing thing is a reader that groups by `(cell, arm)`, counts DISTINCT seeds, and refuses to return a call for a stochastic group with n < 3. The first kid's `band()` cannot be reused for (a) -- it hardcodes the range test, and the baselines it needs arrive from a foreign file, not from the group.

## FALSIFIERS
1. A `(cell, arm)` group with 4 rows carrying one seed returns n=4 -- duplicate determinism reading as replication. FAILED if true.
2. The reader returns a call for a stochastic group with fewer than 3 distinct seeds instead of refusing. FAILED if true.
3. The emitted `cells.jsonl` of this round still contains zero `arm == "uniform"` and zero `arm == "key_only"` rows.
4. Re-deriving (a) and (b) by hand from the 12 rows disagrees with the reader's output on any single cell. The arithmetic is small enough to be checked by eye; a disagreement means the reader is not computing what its docstring says.
5. The 7.25 case: if key_only .8833 is inside the random range, the two calls agree there and clause (b)'s stated disagreement is false.

## TESTS
- pure-python, no model, no torch import: a fixture of 3 rows with seeds 7/21/99 must return n=3; a fixture of 3 rows all carrying seed 7 must return n=1 AND raise the refuse-to-call on a stochastic arm.
- the reader's output for the real 12 rows must equal the parent's hand table above, cell for cell.
- `grep -c '"arm": "uniform"' cells.jsonl` > 0 and the same for `key_only` in the re-emitted file.

## FILE SCOPE
- NEW `.agi/context/local-maxxing/osc/osc_band_call_a00-<mint>.py` (+ `_test.py`).
- READ-ONLY: `osc_band_seeds_qwen2_a00-2b3ca8c4.py`, `osc_band_matched_uniform_a00-a721f95f.py`. Do NOT edit the first kid's script -- its verdict is a reviewed node and the bytes are the evidence.
- outputs: `osc_band_qknorm_dir` + `/a00-<mint>-qwen2-calls/`. NEVER `.agi/sessions`.
- ONE new node of your own for the key_only-beats-every-random-draw finding, which is a claim in its own right and is not this round's claim.

## CEILING
1 kid. 60 production lines. NO MODEL -- the twelve rows already exist on disk; the model slot belongs to p2 this round and a second model run would contend for it. $0.60.
## PASS 8 annotation (a00-dead485b) -- the MARGIN denominator, declared vs shipped
The claim above is the HALF-RANGE table and it is untouched: `margin_inside_budgets` is still
{5.25, 7.25} and the reader still emits that call unchanged. What PASS 8 item 3 found is a
SECOND, larger divergence the claim never named: the config cell p3 is told to cite
(`values.local_maxxing.osc_band_row_contract`, .agi/config.json:279) declares the ADOPTED,
pre-registered MARGIN to be `key_only - uniform` against the FULL min-max, naming
osc_band_call2_a00-cc7b25cc.py, whose `band()` returns `max(v)-min(v)`. The only reader shipped by
this round judged the HALF range, so a decide layer implementing the cited cell and a decide layer
calling the reader disagreed on 2 of 8 cells (6.25 agree 0.051758 vs 0.058350, 6.25 kl 0.154396 vs
0.298044 -- both 'win' under the reader, both inside-noise under the declared rule). The reader now
carries that DECLARED call by name, `margin_full`, beside the hand-table `margin`, and
calls.json reports both plus `declared_vs_half_disagree`. Two things a later reader must not
re-derive wrongly: (a) the cell's TEXT and the cell's NAMED MODULE are not the same rule --
osc_band_call2's comparator defaults to the random mean, not `uniform` -- so cite the cell, which
is what the cell itself instructs; (b) `inside-noise` now means two different things in one file and
p3 must name the call it applies, which is the point of this round, not a defect of it.

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 8 item 3, added by a00-dead485b. The claim's own text -- abs(key_only-uniform) <= half_range,
2 of 4 budgets -- is NOT re-worded, because it is the round's data and the reader still emits it
verbatim; a hypothesis is not edited to match a later config cell. What the item actually found is
that this hypothesis was measuring the WRONG THING for the decide layer: it proved two denominators
disagree while the cell p3 is ordered to cite declares a THIRD convention (the full min-max), so
"the two calls disagree" was true and still not the disagreement p3 would hit. The fix that respects
both the no-re-word rule and the cell's authority is to make the declared rule a NAMED call in the
reader rather than a comment on it: margin_full sits beside margin, the two differing cells are
reported as declared_vs_half_disagree, and a reader of this node now has all three denominators by
name instead of two. The residual weakness I am recording rather than hiding: the cited cell's text
and the module the cell names are themselves not the same rule (random mean vs uniform), so the
graph's declared MARGIN still has no single implementation to point at -- that is the next round's
job, not this one's.
<!-- THOUGHT:END -->
