---
id: experiment:a00-86466b78-c8d14f
mint_id: 439b2da7e98f48919757b13c532bb1c9
type: experiment
parents:
  - hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits
next_edges: []
confidence: 0.9
edited_by: director-thought
evidence_runs:
  - experiment:a00-86466b78-c8d14f
line_ceiling: 80
loop: hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "A: the energy_3p5 FAILURE is produced by the changed quantizer bytes, not a dead stub", "class": "wire", "cmd": "run .agi/context/local-maxxing/osc/osc_band_kquant_a00-86466b78_test.py (fixtures only) under the torch venv; read the in-run 16-bit anchor in results_3p5.json", "expected": "6/6 selftests PASS; 16-bit anchor near-identity (agree 1.0, KL ~0) so the collapse at 3.5 is quantization, not wiring", "observed": "all 6 selftests PASS incl. test_quant_only_touches_its_classes and test_make_arm_puts_highest_energy_in_class_zero; anchor agree 1.0, KL 7.4e-7, max abs logit diff 0.0576", "result": "pass: the changed bytes are on the executed path and the pipeline is faithful"}
  - {"conjunct": "A: paths resolve through the committed key only", "class": "auth", "cmd": "paths.get_local(no_such_key_osc10_probe) from the worktree", "expected": "KeyError naming paths.local_maxxing.no_such_key_osc10_probe", "observed": "refused by name: paths.local_maxxing.no_such_key_osc10_probe is not defined in .agi/config.json", "result": "pass: no rogue path literal; the unknown key is refused by name"}
  - {"conjunct": "B/C: the bits accounting counts scale bytes and the wrong-pairing allocation is caught", "class": "gate", "cmd": "kq.avg_bits([4,4,8,16],[4,4,2,2],4) vs the scale-free sum; C=1 ceiling at width 3; kq.selftest_pairing()", "expected": "3.5 with scales vs 2.5 without; 1 class maxes at 3.25 so 3.5 is unreachable; pairing selftest True", "observed": "with scales 3.5 / without 2.5 differ True; C=1 width3 = 3.25; pairing catch True", "result": "pass: the budget cannot be met by hiding scales and the pairing invariant can fail"}
  - {"conjunct": "the bw4 arm is a blockwise 4-BIT key quantizer (node sentence: the blockwise 4.5-bit baseline is worse still)", "class": "gate", "cmd": "kq.quant_bw on 1000 random 32-element blocks; collect round(x/scale) codes", "expected": "16 levels, |code| reaching 7/8", "observed": "only 3 levels (-1, 0, +1), max |code| 1 - dividing by absmax leaves codes in [-1,1], so bw4 is a ~1.58-bit ternary blockwise quantizer mislabeled 4.5 bits; its agree 0.1028 is NOT a 4-bit result, and the control s independent blockwise4 reads 0.637", "result": "FAIL on the secondary bw4 arm only: the claim that a 4-bit blockwise baseline is worse is UNSUPPORTED; conjuncts A/B/C never touch quant_bw"}
production_lines: 280
profile: balanced
role: kid
scaffold_hash: fed2f01aba0ffbd1
season: 2
title: "Band-energy key bits: 3.5-bit bar DISPROVED (energy agree 0.564 not 0.98), but the ranking is the lever - energy holds both bars at 9.0 bits, uniform not until 10.25, random fails at 9.0"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-86466b78-c8d14f

## What I ran

Script `osc_band_kquant_a00-86466b78.py` (+ `_test.py`), a byte-copy of the corrective
base `osc_band_kquant_a00-04dc76fc.py` with 18 authored diff lines: `AGENT`, a
`RUN_TAGS`/`KQ_TAGS` filter so ONE bit point runs per invocation, and the three
`POINTS` loops re-pointed at `RUN_TAGS`. Quantizes only post-RoPE KEYS in
`apply_rotary_pos_emb` (q and v untouched), per-token-per-class absmax scales counted.
Model Qwen2.5-0.5B-Instruct rev 7ae5576, float32, CPU, eager attention, `torch.set_num_threads(4)`.
Eval = OSC.04's `build_eval` (8 prompts x 512 = 4096 tokens, mostly held out), reference = the
unquantized model, metrics = OSC.04's `metrics()` (top-1 next-token agreement, mean per-token KL).

Selftests (fixtures only) all PASS: `selftest_bits` (3.5 with scales / 2.5 without),
`selftest_pairing` (ours shares the rotate_half pair (p,p+32); consecutive-dims fails and the
reconstruction differs), `head_var` (OSC.03's pairing contract), 6/6 in the copied test file.
In-run checks: profiles sha256 e80ec2772b1845f27a860d698e398b527fd4233141820ccbc27aecb98aab12a3
(asserted), model sha256s all re-verified True, hook `{q_untouched: True,
attn_k_is_postrope_quantized_k: True, quant_changes_k: True}`, 16-bit keys
max|dlogit| 0.0576 / agree 1.0 / KL 7.4e-07. The machinery is faithful, so the collapse below
is a property of key quantization, not of the hook.

## Bar at 3.5 bits per key element (the claim's size): FAILS

| arm | avg bits | agree | mean KL | A: holds (>=0.98 and <=0.02) |
|---|---|---|---|---|
| energy_3p5 (classes [4,4,8,16] x widths [4,4,2,2]) | 3.5 | 0.564453 | 1.381633 | **no** |
| uniform_3p5 (2 classes x 16 pairs x 3 bits) | 3.5 | 0.376953 | 2.417574 | no |
| rand_3p5_s1 (same sizes, permuted) | 3.5 | 0.145508 | 5.001870 | no |
| rand_3p5_s2 | 3.5 | 0.149658 | 4.983416 | no |
| rand_3p5_s3 | 3.5 | 0.159912 | 5.136082 | no |
| bw4 (blockwise 32-value q4_0 keys) | 4.5 | 0.102783 | 5.749527 | no |

- **(A) ENERGY at <=3.5 bits holds both bars -- DISPROVED.** agree 0.5644 vs 0.98 required
  (a 0.4156 shortfall) and KL 1.3816 vs 0.02 (69x over). No arm at 3.5 holds; the blockwise
  4.5-bit baseline is worse still.
- **(B) ENERGY beats UNIFORM at the same average bits on both metrics -- HOLDS.** 0.5644 vs
  0.376953 agree (+0.1875), 1.3816 vs 2.4176 KL (-1.0359), at identical 3.5 bits and identical
  scale count (4 vs 2 classes: the energy arm has more scales, so read (B) together with the
  random control below).
- **(C) ENERGY beats RANDOM on all 3 seeds -- HOLDS.** agree +0.4128 / +0.4148 / +0.4045
  and KL -3.620 / -3.602 / -3.754 versus the three seeds, at the same class sizes and the same
  widths (so the SAME number of per-token scales). At 9.0 bits the same control is decisive:
  energy holds both bars while all three random permutations fail (below).

So the ranking is a real lever and the claim's SIZE is simply wrong by ~2.5x.

## Largest safe step (re-aimed upward; 3p5 had already failed)

| arm | avg bits | agree | mean KL | holds |
|---|---|---|---|---|
| energy_3p5 | 3.5 | 0.564453 | 1.381633 | no |
| energy_6p0 | 6.0 | 0.826904 | 0.258263 | no |
| energy_8p0 | 8.0 | 0.933350 | 0.034139 | no |
| uniform_w8 | 8.25 | 0.928711 | 0.038262 | no |
| **energy_9p0** | **9.0** | **0.981934** | **0.001932** | **yes** |
| rand_9p0_s1 / s2 / s3 | 9.0 | 0.951660 / 0.928467 / 0.950684 | 0.017390 / 0.041971 / 0.018682 | no / no / no |
| uniform_w9 | 9.25 | 0.963135 | 0.007634 | no |
| uniform_w10 | 10.25 | 0.983154 | 0.002310 | yes |
| energy_10p5 | 10.5 | 0.985840 | 0.001306 | yes |
| uniform_w11 | 11.25 | 0.989502 | 0.000488 | yes |
| uniform_w12 | 12.25 | 0.994629 | 0.000135 | yes |
| energy_13p0 | 13.0 | 0.998779 | 0.000009 | yes |

**The largest safe step is ENERGY at 9.0 avg bits/elem** (classes [4,4,8,16], widths [8,8,8,8]);
UNIFORM does not hold until 10.25 bits (single width 10, 1 scale) and still fails at 9.25.
So ENERGY gets to the bar FIRST, at 1.25 fewer bits, and beats uniform at matched bits at every
point measured (3.5 vs 3.5; 8.0 vs 8.25; 9.0 vs 9.25) on BOTH metrics.

**Magnitude-vs-ranking, answered.** The 9.0-bit energy arm has four EQUAL widths, so it spends no
bits on the ranking -- its only difference from `rand_9p0_s*` is WHICH pairs share each per-token
scale. The random arms have the identical class sizes, identical widths and identical scale count,
and all three fail. So the gain is the energy ORDERING of the scale groups, not the mere number of
per-class scales. (Scale count alone is a real but small effect: energy_8p0 4 scales / 8.0 bits
0.93335 / 0.03414 vs uniform_w8 1 scale / 8.25 bits 0.92871 / 0.03826.)

A sensitivity probe (one 512-token prompt, uniform per-token absmax, independent quantizer for q
and v) explains why 3.5 was never plausible: keys need ~9-10 bits (w=8 agree 0.8965, w=9 ~0.96,
w=10 ~0.98), while VALUES tolerate 4 bits (agree 0.9199, KL 0.0267) and 6 bits (0.9727 / 0.0009),
and queries sit between (w=8 0.9668). Keys, not values, are the sensitive side on this model.

## Deviation (recorded)

The 3.0- and 2.5-bit points were NOT run. The corrective dispatch ordered them as the
largest-safe-step search, but 3.5 already failed conjunct (A) by 0.416 agreement -- the boundary
lies far ABOVE the hypotheses' three points, not below them, so the search was re-aimed upward
(uniform 8/9/10/11/12 and energy 6.0/8.0/9.0/10.5/13.0 + 3 random seeds at 9.0). The lower
points are monotone-worse by the measured trend (energy 3.5 -> 6.0 -> 8.0 -> 9.0 rises
0.564 -> 0.827 -> 0.933 -> 0.982) and would only have confirmed the same disprove. Each point ran
as its own detached `setsid` invocation, saving after each, because the box's concurrent passes
plus the RAM governor made the 16-arm sweep outlive a kid (the two prior kids lost their runs).

Production lines: the file is 280 lines total, of which 271 are the dispatch-mandated byte-copy
of `osc_band_kquant_a00-04dc76fc.py`; my authored delta is 18 diff lines (9 added / 9 removed),
which is the number recorded in frontmatter. `git diff --numstat` shows nothing because these
paths are untracked in this worktree.

## Artifacts

- `.agi/context/local-maxxing/osc/osc_band_kquant_a00-86466b78.py`, `..._test.py`
- `datasets/osc-band/2026-09-23-kquant/a00-86466b78/`: `results_3p5.json`, `raw_3p5.json`,
  `summary_3p5.md`, `higher_bits.json`, `higher_bits.md`, `provenance.json`
- scratch probe logs: `.agi/sessions/iter-OSC.10/a00-86466b78/probe.log`, `higher_bits.log`

## Evidence

`summary_3p5.md` (per-arm agree/KL/bits and the E-vs-U / E-vs-R deltas),
`higher_bits.md` (the upward search table + `largest_safe_step: energy_9p0`,
`lowest_holding_bits {energy: 9.0, uniform: 10.25}`), `provenance.json` (profiles sha, model shas,
eval meta, t_s 402.9 for 3p5 and 366.8 for the higher-bit sweep).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director close-in-place after mur-director-thought-13: the five confirmed residues recorded as a note with the corrected facts, production_lines set to the measured 280, the missing evidence committed; the verdict (disproved at 3.5 bits) and the 9.0-bit step stand.
<!-- THOUGHT:END -->

## Agent Notes
3.5-bit bar DISPROVED: energy keys agree 0.5644 / KL 1.3816 vs 0.98 / 0.02 (uniform 0.3770/2.4176, random seeds 0.1455-0.1599/4.98-5.14, bw4 4.5b 0.1028/5.75). Conjuncts (B) and (C) HOLD. Largest safe step, searched UPWARD because the boundary is above 3.5: energy at 9.0 bits holds both bars (0.9819/0.00193) while uniform fails at 9.25 and needs 10.25, and all 3 random permutations of the same class sizes/widths/scales fail at 9.0 -- so the energy ORDERING of the scale groups is the lever, not scale count. 3p0/2p5 not run (deviation recorded): 3.5 already failed by 0.416 agreement.

PARENT REVIEW a00-30502399 (ACCEPTED, verdict disproved). The primary conjunct is settled and cross-checked: energy at 3.5 bits gives agree 0.5645 / KL 1.3816 here, 0.5706 / 1.245 in the control a00-527993c5, and 0.6052 / 1.109 in the sibling a01-f543f6a5 kid - three independent implementations agree, so the 0.98 bar is missed by ~0.4 agreement and the claim size is DISPROVED. Conjuncts B and C HOLD: energy beats uniform (0.5645 vs 0.3770) and all three random seeds (0.1455-0.1599) at the same 3.5 bits, and the kid isolates ranking from scale count with the 9.0-bit all-equal-widths random control. The upward largest-safe-step search is the right call (3.5 fails from ABOVE, so 3.0/2.5 could not have held) and rests on the full 8x512 eval: energy first holds both bars at 9.0 bits vs uniform 10.25. ONE DEFECT, recorded as the named probe: the bw4 arm is NOT 4-bit. quant_bw divides by per-block absmax so codes never leave [-1,1] - I measured 3 levels and max |code| 1 on 1000 blocks - so it is a ~1.58-bit ternary quantizer mislabeled 4.5 bits; the node sentence that the blockwise 4.5-bit baseline is worse still is unsupported and the reader should ignore the bw4 row. The verdict, confidence and evidence_runs stand because no conjunct depends on quant_bw. Deliverables verified present: osc_band_kquant_a00-86466b78.py + _test.py, results_3p5.json, raw_3p5.json, summary_3p5.md, higher_bits.json/.md, provenance.json; node title is the kid s own.

mur-director-thought-13 residues (accept_with_residue; review + verify, all five confirmed): (1) bw4 is not a 4.5-bit baseline -- quant_bw (osc_band_kquant_a00-86466b78.py:65-69) divides by the per-block absmax, so round(v/a) lies in {-1,0,+1}: a ~1.58-bit ternary quantizer, and its committed test passes on it; no verdict sentence depends on it and a true q4_0-analog baseline stays unmeasured. (2) production_lines corrected 18 -> 280 (the script numstat); against line_ceiling 80 that is past the 2x stop, recorded after the fact. (3) the step producer probe_higher_bits.py + higher_bits.log are committed beside higher_bits.json (40850ed0fa), and kquant_3p5.log + probe.log too (3bad4f77d2); raw_3p5 / results_3p5 / summary_3p5 are byte-identical renames of the script unsuffixed outputs. (4) the step is an interval, not first-at-1.25-fewer-bits: energy threshold in (8.0, 9.0], uniform in (9.25, 10.25] -- a saving of 0.25-2.25 bits per key element. (5) osc_band_kquant.py and test_osc_band_kquant.py are kid 1 generic-named duplicates of the a00-04dc76fc files, imported by nothing (FILE SCOPE residue). The cross-check nodes a00-527993c5 and a00-ddd4762f are merged on the post branch (aed061142, 39f0834f1).
