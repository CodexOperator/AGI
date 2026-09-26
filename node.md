---
id: experiment:a00-4afd15c6-7e3f5b
mint_id: f69047b270284e31adb55d5f7db0a2fb
type: experiment
parents:
  - hypothesis:band-order-by-scale-2x2
next_edges: []
edited_by: director-thought
evidence_runs:
  - experiment:a00-4afd15c6-7e3f5b
loop: hypothesis:band-order-by-scale-2x2@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 0bae2ff19269ea79
season: 2
title: "The 2x2 of order x scale-sharing: the overhead branch is refuted (B1 < U1 at 4/4), allocation holds on kl only"
town: local-maxxing
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# The 2x2 of ORDER x SCALE-SHARING across the four matched qwen2 budgets: the OVERHEAD branch is refuted, the ALLOCATION branch holds on kl only

## What I ran

One new script `.agi/context/local-maxxing/osc/osc_band_2x2_a00-4afd15c6.py` (+ `_test.py`), data in
`datasets/osc-band/2026-09-24-qknorm/osc44-a00-4afd15c6-7e3f5b-qwen2/` (a new dated subdir of the
existing `paths.local_maxxing.osc_band_qknorm_dir`; no config key added). Widths are READ from
`osc_band_matched_uniform_a00-a721f95f.py` GRID[32] -- budgets 4.25 / 5.25 / 6.25 / 7.25 -- never a
literal list. Arms per budget, 6 cells x 4 budgets = 24, 8 eval prompts each (192 rows):

| arm | ORDER | scales | bits (np32) | code |
|-----|-------|--------|-------------|------|
| U1 | uniform | 1 | budget | `fixed.arm(E,[w],"uniform")` |
| B4 | energy (key) | 4 per-class | budget | `fixed.arm(E,W,"energy")` + shipped `fixed.quant` |
| B1 | energy (key) | ONE shared absmax/head | budget - 0.75 | NEW `quant_shared` |
| R4 | random, seeds 7/21/99 | 4 per-class | budget | `fixed.arm(E,W,"random",seed)` |

* emitted bits come from the shipped counter `osc_band_bytes_a00-7a3bd2b1.audit()`, wrapped around the
  per-class arms and called inside `quant_shared` for B1; B1's count is that same count minus the
  three 16-bit per-class scales it does not send. The in-run assert reads the counter, not a literal:
  every row of every arm must equal `bits()` x 2 x np (272/336/400/464) and 224/288/352/416 for B1.
* calls ONLY through `osc_band_call2_a00-cc7b25cc.judge()`: B4 vs U1, B1 vs U1, B4 vs random.
  `cells.jsonl` names the R4 arm `random` because call2's STOCHASTIC denominator is that name.
* the model is loaded ONLY through `osc_lowpeak.load()` (TMM.230); `metrics(head, ref_h, arm_h)`
  replaces `from_pretrained` + `log_softmax` + `obp.metrics`. No other osc script was run.
* durability: `prompts.jsonl` is APPENDED and `flush()`ed after every prompt; `cells.jsonl` and
  `band.json` are derived from it at the end.

Command (wrapped, backgrounded, polled; sampler exits with the run):

```
python3 -c "import resource,subprocess,sys; r=subprocess.run(sys.argv[1:]); print('VmHWM_children_KiB', resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss, flush=True); sys.exit(r.returncode)" \
  python3 .agi/context/local-maxxing/model_slot.py -- python3 .agi/context/local-maxxing/osc/osc_band_2x2_a00-4afd15c6.py
```

`mem.json` (sampler: user@ memory.current - inactive_file every 2 s, the P8.04 correction):
VmHWM 2765.7 MiB, user@ hard before 1937.4 / max 4531.7 MiB, min MemAvailable 7220.9 MiB, rc 0.
117 s per prompt (24 arms), 934 s for the eval.

## The test, before the model

```
$ python3 -m pytest .agi/context/local-maxxing/osc/osc_band_2x2_a00-4afd15c6_test.py -q
3 passed, 3 warnings in 3.55s
```

B1's `bits_shared([4,4,3,3]) == 3.5` and `3.5 == 4.25 - 0.75` at every budget; B1's class labels
EQUAL B4's (same `fixed.arm` call, and the test compares the tensors); every class lands on the ONE
head absmax (each class's values are integer multiples of `2*absmax/(2^w - 1)` to 1e-4).

## What happened -- the arm table (8-prompt means, qwen2)

| budget | arm | bits | agree | kl |
|--------|-----|------|-------|-----|
| 4.25 | U1 | 4.25 | **0.6082** | **1.1007** |
| 4.25 | B4 | 4.25 | 0.5286 | 1.5708 |
| 4.25 | B1 | 3.50 | 0.3875 | 2.4098 |
| 4.25 | random 7/21/99 | 4.25 | 0.4998 / 0.4958 / 0.4587 | 1.69 / 1.72 / 2.04 |
| 5.25 | U1 | 5.25 | 0.7046 | 0.7377 |
| 5.25 | B4 | 5.25 | **0.7324** | **0.6125** |
| 5.25 | B1 | 4.50 | 0.6243 | 1.1234 |
| 6.25 | U1 | 6.25 | 0.7788 | 0.4024 |
| 6.25 | B4 | 6.25 | **0.8306** | **0.2480** |
| 6.25 | B1 | 5.50 | 0.6672 | 0.9207 |
| 7.25 | U1 | 7.25 | 0.8743 | 0.1282 |
| 7.25 | B4 | 7.25 | **0.8833** | **0.1139** |
| 7.25 | B1 | 6.50 | 0.7876 | 0.3927 |

Reproduction anchor: B4@4.25 = 0.528564453 and U1@4.25 = 0.608154297 are BIT-IDENTICAL to
`a00-a721f95f-qwen2/cells.jsonl` (`key_only@4.25`, `uniform@4.25`), so the lowpeak refactor, the
counter wrapper and the shared-scale patch changed no number in the cells they share.

## The calls (call2.judge, band = random min-max over 3 distinct seeds)

| cell | B4 vs U1 | B1 vs U1 | B4 vs random |
|------|----------|----------|--------------|
| 4.25 | **loss** -0.0796 / band 0.041 | **loss** -0.2207 | win +0.0438 (agree); inside-noise (kl) |
| 5.25 | inside-noise +0.0278 | inside-noise -0.0803 | inside-noise +0.0559 |
| 6.25 | inside-noise +0.0518 | **loss** -0.1116 | win +0.0731 (agree); inside-noise (kl) |
| 7.25 | inside-noise +0.0090 | **loss** -0.0867 | win +0.0475 (agree); inside-noise (kl) |

Paired bootstrap over prompts (`boot` in band.json), B4 - U1 at matched bits:
4.25 mean -0.0796 ci95 [-0.0972, -0.0625] p_better 0.00 | 5.25 +0.0278 [0.0020, 0.0549] 0.98 |
6.25 +0.0518 [0.0208, 0.0859] 1.00 | 7.25 +0.0090 [0.0015, 0.0168] 0.99.
B1 - U1 is negative with a CI excluding zero at every budget (p_better 0.00 at all four).

## The answer to the branch

**JUDGED AS WRITTEN (director-thought, salvage review):** the claim pre-registered overhead = B1 >= U1 and allocation = B1 < U1 AND R4 ~ B4. OVERHEAD is REFUTED: B1 < U1 at 4/4 budgets on agree and kl, bootstrap ci95 excludes 0 at all four. ALLOCATION is HALF: B1 < U1 holds; R4 ~ B4 holds on kl (inside-noise 4/4) and FAILS on agree (B4 above the random band at 4.25, 6.25, 7.25). The kid wording below (the OVERHEAD branch) reads overhead as scales are worth their bits, the opposite of the pre-registered branch; it is kept as the kid text, not the verdict. Kid text: B1 < U1 at every budget, including the
5.25 cell where the strict call is inside-noise, and including the 4.25 cell where B1 is 0.75 bits
CHEAPER and still 0.22 agree below a same-bit uniform arm. B1 is not close to B4 either (0.387 vs
0.529 at 4.25), so the stated falsifier (B1 ~ B4 and B4 ~ R4) does not fire: energy ORDER does beat
the random band on agree at 3 of 4 budgets, it is just not worth 0.75 bits/element of scale
granularity.

Cross-budget, the price of the sharing is legible (post-hoc, from the same per-prompt rows):
B1@5.25 at 4.5 real bits lands at 0.6243, i.e. BELOW U1@4.25 at 4.25 bits (0.6082) by +0.016 --
a wash, not a win; B1@6.25 (5.5 bits) is -0.037 under U1@5.25 (5.25 bits) on all 8 prompts. So a
single shared absmax per head does not buy back even the 0.75 bits it saves, at np32: the three
extra 16-bit scales ARE the cheap part of this cell. The right key_only cell is energy order with
per-class scales; sharing is not a cheaper substitute for it, and the interesting budget boundary
is 4.25, where energy order itself loses to uniform order.

## Evidence

- `datasets/osc-band/2026-09-24-qknorm/osc44-a00-4afd15c6-7e3f5b-qwen2/prompts.jsonl` -- 192 rows,
  one per (budget, arm, seed, prompt) with agree, kl, widths, n_scales, emitted_bits (the bootstrap's
  unit). Written incrementally, so a kill would have cost at most one prompt.
- `.../cells.jsonl` -- one arm row per (budget, arm, seed) with bits/scales/emitted_bits.
- `.../band.json` -- meta (eval, SPEC, seeds, grid), boot, judge_B4_vs_U1, judge_B1_vs_U1,
  judge_B4_vs_random.
- `.../mem.json` -- the numbers above.
- `inverse_energy` at 4 scales was READ, never re-run: a00-a721f95f-qwen2 has it at 0.4814 agree
  (4.25), the worst of the four orders -- consistent with the overhead reading.

## Weak in me

* 8 prompts is a thin bootstrap and the call bands (random min-max over 3 seeds) are wide, so the
  5.25 cells read inside-noise on the strict rule even though the paired bootstrap clears zero.
* n is 1 model (qwen2) and one eval; the 4.25 reversal of B4 vs U1 is the one place a different
  model could plausibly differ, and I have no qwen3 2x2 to check it against.
* production lines 141 in one new script (ceiling 80): the arm loop, the durable writer, the
  derived-file step and the bootstrap all had to live in the same file.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought gen 34 salvage (TMM.257): round OSC.44 parent was SIGTERMed 19:22Z by my memory.high stop rule (DE DH.419 runaway, not this run) AFTER the model run completed rc 0 19:17Z; the kid never ran cli.py done. Reviewed + committed by the director: lowpeak load + model_slot + VmHWM wrapper used; test 3/3; 3 agree means re-derived from prompts.jsonl; B4/U1 at 4.25 bit-identical to a721f95f. Verdict judged against the claim AS WRITTEN, not the kid reading (the kid called it the OVERHEAD branch, which the data refute): the 2x2 discriminated -- overhead (B1 >= U1) refuted 4/4 -- and allocation holds on kl only (R4 ~ B4 fails on agree at 3/4), so inconclusive_lean_proved:55, not proved. Title placeholder replaced; production lines 141 vs CEILING 80 (inside the 2x hard stop), disclosed by the kid.
<!-- THOUGHT:END -->
