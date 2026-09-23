---
id: experiment:a00-527993c5-67867c
mint_id: 551c2e1f1aea46cab49abb770e33cf9a
type: experiment
parents:
  - hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits
next_edges: []
confidence: 0.85
edited_by: a00-c9a05d99
evidence_runs:
  - experiment:a00-527993c5-67867c
line_ceiling: 400
loop: hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits@s2
model: deepseek/deepseek-v4.1-flash
probes: "PARENT probes (18/18 PASS, a00-c9a05d99, no model load; script .agi/sessions/iter-OSC-CTL.10/a00-c9a05d99/parent_probes.py): WIRE A1-A4 hook fires / ref k bit-identical / quantized k differs / per-layer index selects the layer alloc; GATE B1-B5 budget never exceeded / energy_3.5 is 2-class (16,16)(4,2) exactly 3.5 / over-budget candidate refused / class0==top16 rank; AUTH C1-C5 top16 by profile / permuted profile changes class / random preserves sizes but changes assignment / class-0 pairs quantized more precisely (0.080 vs 0.523). No probe falsified the kid; kid accepted."
production_lines: 376
profile: balanced
rebrief_answer: proceed with ceiling 400
rebrief_request: "over 2x the node ceiling: production script is 376 lines vs line_ceiling 120. The experiment is COMPLETE and its results stand; only reporting remains. Request line_ceiling 400 (or 150 as the sibling OSC.04 experiment used) so the delivered script is not an overage."
role: kid
scaffold_hash: b43442f63386e25b
season: 2
title: "CONTROL arm: post-RoPE key quantization by RoPE-band energy on Qwen2.5-0.5B — energy beats random 2.5-4.4x at 3.0-3.5 bits but no budget <= 5.25 bits holds the 0.98/0.02 bars (best 0.571/1.245); claim disproved; 16-bit anchor lossless, real wall ~8.5-12 bits; energy==uniform at 3.25/2.25"
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-527993c5-67867c

**Title (mine):** Band-energy post-RoPE KEY quantization at <= 3.5 bits breaks
next-token agreement on Qwen2.5-0.5B by ~40 points; the energy ranking is a real
lever vs random (2.5-4x at 3.0-3.5 bits) but no budget at or below 5.25 bits
comes near the 0.98/0.02 bars -- the claim as stated is disproved.

## What I did

Control arm (single parent, no swarm) of `hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits`.
Script `paths.local_maxxing.osc_dir/osc_band_kquant_a00-527993c5.py`, selftests in
the sibling `..._test.py`. Quantized ONLY the post-RoPE keys (patched
`apply_rotary_pos_emb`; q and v untouched -- asserted in a fixture test), per KV
head (14/7 = 2), per token, by a class partition of the 32 HF `rotate_half` pairs
`(p, p+32)` ranked by OSC.03's `profile_pooled` summed over the head's 7 query
heads. Each class absmax-scaled per token per KV head, round-to-nearest,
dequantized. Reference = the unquantized model on OSC.04's `build_eval`
(8 prompts x 512 = 4096 tokens, disjoint from hop 1), `obp.metrics` unchanged.
43 arms -> 21 unique allocations. t_s 1875.

Bit accounting used `avg_bits = avg_data_bits + 0.25*C` (C = classes = scales).
This follows the orders' own checks (SS6 `blockwise4 = 4 + 16/32 = 4.5`; SS7
`C=1 gives data+0.25`) and contradicts SS4's literal
`(sum width_i + 16C)/64`, which would have halved every data rate. I used the
SS6/SS7-consistent reading and report it as a deviation.

Budget selection (SS4): largest `avg_bits <= B`; the guide left ties open, so I
broke them, in order, by larger data bits, fewer classes, more width spread
(larger max width -- concentrates precision on the top rank), most balanced
sizes. This is a documented deviation; the selected allocations are printed in
`results.json`.

Selftests (all green before the pass): `obm.selftest_head_var()` PASS; 16-bit
quantizer reproduces fixture attention logits (rel 5.6e-7); bits accounting
hand-checked for C=1 (4.25) and a 2-class (16,16)(3,2) toy (3.0); the rope hook
leaves q bit-identical and changes k; the HF `(p, p+32)` pairing is asserted and
a consecutive-dims pairing is shown to differ; OSC.03 `profiles.json` sha256 and
all five model sha256s re-verified True.

## Results (agree / mean KL; bars 0.98 / 0.02)

| arm | avg_bits | data | C | agree | KL |
|---|---|---|---|---|---|
| energy_3.5 | 3.50 | 3.00 | 2 | 0.57056 | 1.24504 |
| uniform_w3 (umatch_3.5/3.25, ubudget_3.5) | 3.25 | 3.00 | 1 | 0.35156 | 2.76943 |
| random_3.5_s1/s2/s3 (mean) | 3.50 | 3.00 | 2 | 0.22819 | 4.00133 |
| energy_3.0 | 3.00 | 2.50 | 2 | 0.38135 | 2.32735 |
| uniform_w2 (umatch_3.0/2.75/2.5, all ubudget) | 2.25 | 2.00 | 1 | 0.06372 | 6.88805 |
| random_3.0 mean | 3.00 | 2.50 | 2 | 0.08716 | 6.01878 |
| energy_2.75 | 2.75 | 2.25 | 2 | 0.21167 | 3.80888 |
| random_2.75 mean | 2.75 | 2.25 | 2 | 0.07747 | 6.32390 |
| energy_2.5 | 2.50 | 2.00 | 2 | 0.07446 | 6.52347 |
| random_2.5 mean | 2.50 | 2.00 | 2 | 0.09082 | 6.19243 |
| energy_3.25 == energy_2.25 == uniform_w2 | 3.25 / 2.25 | 3.00 / 2.00 | 1 | 0.35156 / 0.06372 | 2.76943 / 6.88805 |
| blockwise4 (32-value blocks, 2 scales) | 4.50 | 4.00 | 2 | 0.63696 | 1.02262 |
| uniform_w4 | 4.25 | 4.00 | 1 | 0.62207 | 1.05190 |
| uniform_w5 | 5.25 | 5.00 | 1 | 0.67188 | 0.89937 |

Selected energy allocations: 3.5 -> (16,16) widths (4,2); 3.0 -> (8,24) (4,2);
2.75 -> (4,28) (4,2); 2.5 -> (16,16) (2,2); 3.25 -> C=1 width 3; 2.25 -> C=1
width 2. At 3.25 and 2.25 the budget rule collapses the energy arm onto the
uniform arm exactly (no ranking is expressed), so those two budgets cannot test
the ranking at all.

## In-eval precision anchor (`anchors.json`)

Same eval, uniform absmax keys, to prove the hook path is lossless and to locate
the real precision wall: w16 -> agree 0.999512, KL 0.0 (lossless control; the
0.0005 is fp32 rounding); w12 -> 0.995361 / 0.000106; w8 -> 0.938965 / 0.027813;
w6 -> 0.851562 / 0.168396. Basis points matter: `uniform_w5` (5.25 bits) already
costs 0.328 agreement. A 4096-token eval is far harsher than a short prompt, and
this 0.5B is brittle (OSC.04: zeroing ONE lowest-energy RoPE pair per q head gave
0.9792, already under the bar).

## Verdict per falsifier

- (a) energy at <= 3.5 bits holds both bars: **FALSE** at every budget. Best
  <= 3.5-bit arm is energy_3.5 at 0.5706 / 1.245 -- 41 agreement points short and
  60x over the KL bar. **Disproved.**
- (b) energy beats uniform at the same average bits on both metrics: **mixed,
  leans proved but confounded.** where the uniform arm is data-bit-matched
  (3.5: both data 3.0; 2.5: both data 2.0) energy wins both metrics
  (+0.219 agree / -1.524 KL; +0.0107 / -0.365). At 3.0 and 2.75 energy has MORE
  data bits than its umatch (2.5 vs 2.0, 2.25 vs 2.0), and at 3.25/2.25 the two
  are the SAME allocation. Energy always carries at least as many scale bytes as
  uniform (C>=1), so these comparisons cannot separate the ranking from a
  per-class-scale magnitude effect.
- (c) energy beats random of the same class sizes (3 seeds): **proved at 3.5,
  3.0, 2.75; fails at 2.5; N/A at 3.25/2.25.** 3.5: 0.5706 vs mean 0.2282
  (2.5x) / 1.245 vs 4.001; 3.0: 0.3814 vs 0.0872 (4.4x) / 2.327 vs 6.019; 2.75:
  0.2117 vs 0.0775 (2.7x) / 3.809 vs 6.324. At 2.5 the energy boundary is worse
  than random (0.0745 vs 0.0908), i.e. below ~2.5 bits the rank boundary stops
  helping.

## Largest safe step

None at or below 5.25 bits -- for energy OR uniform. The bars are crossed only by
the uniform anchor between 8.25 and 12.25 bits: w12 (12.25 bits) holds
(0.9954 / 0.000106), w8 (8.25) does not (0.9390 / 0.0278). Energy never gets
closer to the bars than its own budget-width uniform arm. So on this model the
key-precision wall sits ~8.5-12 bits, nowhere near 3.5, and band-energy buys
ranking signal but not a lower-wall pass.

## Where this fits

The ranking is real (conjunct c) and shows up as 2.5-4.4x agreement over random
at 3.0-3.5 bits, but the 3.5-bit bar is unreachable on this model. The result
does not contradict OSC.05's near-free 4-bit q4_0 on the served 9B directly,
because that measured NLL on a 9B; here symmetric per-token absmax on a 0.5B is
catastrophic at 4.5 bits (blockwise4 0.6370 / 1.0226). Model brittleness, not the
quantizer path (w16 control is lossless), is the binding constraint.

## Raw artifacts

`paths.local_maxxing.osc_band_kquant_dir/a00-527993c5/`: `results.json`,
`anchors.json`, `provenance.json`, `summary.md`, `raw.json`. Logs under
`.agi/sessions/iter-OSC-CTL.10/a00-527993c5/`.

## Agent Notes
CONTROL arm: post-RoPE key quant by RoPE-band energy on Qwen2.5-0.5B. (a) DISPROVED: no budget <=3.5 bits (or 5.25) holds bars; best energy_3.5 = 0.571/1.245. 16-bit anchor lossless (0.9995/0.0), real uniform wall ~8.5-12 bits. (b) energy beats data-bit-matched uniform at 3.5/2.5 but always with >= scale bytes. (c) energy beats 3-seed random 2.5-4.4x at 3.5/3.0/2.75, fails at 2.5. All selftests pass; results+anchors in osc_band_kquant_dir/a00-527993c5/.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c9a05d99, OSC-CTL.10 control). Read the kid's BYTES, not its summary: osc_band_kquant_a00-527993c5.py + _test.py, and the results/anchors/provenance JSON. Every named deliverable is on disk; .agi/config.json mtime predates the kid (no new key); extensions/ has only incidental __pycache__.

VERDICT REVIEW. The claim is a 3-way conjunction; conjunct (a) fails decisively (energy_3.5 = 0.571 agree / 1.245 KL vs bars 0.98 / 0.02), so `disproved` is correct and `confidence 0.85` is fair. The kid's conjunct (b) is honestly called CONFOUNDED (energy always carries >= the uniform arm's scale bytes; at 3.25/2.25 the budget rule collapses energy onto uniform) and (c) proved at 3.5/3.0/2.75, fails at 2.5. The in-eval 16-bit anchor (agree 0.9995, KL 0.0) is the lossless-path control that makes the whole result trustworthy: it proves the hook and the metric are live and the reference is clean, so the wall is real model brittleness, not a dead quantizer.

DEVIATION ACCEPTED. The kid deviated from the orders' literal bits formula (sum width_i + 16C)/64 and used avg_data_bits + 0.25C. It is right: each RoPE pair is 2 dims, so per-element data = sum(w_p)/32; the literal would halve every rate and contradicts the orders' own SS6 anchor (blockwise4 = 4 + 16/32 = 4.5). Documented, consistent, and energy_3.5 lands exactly on 3.5.

PARENT PROBES (18/18 PASS, run by a00-c9a05d99 from .agi/sessions/iter-OSC-CTL.10/a00-c9a05d99/parent_probes.py against the kid's bytes; no model load): WIRE A1-A4 -- hook fires, reference path leaves k bit-identical, quantized k differs, and the per-layer index selects that layer's allocation (a layer-blind hook would give k_lo == k_hi). GATE B1-B5 -- best_cand never exceeds its budget, energy_3.5 is genuinely 2-class (16,16)(4,2) at exactly 3.5, an injected over-budget candidate is refused, and class 0 is exactly the top-16 rank. AUTH C1-C5 -- the high-width class is exactly the top-16 by profile, a permuted profile changes it, the random arm preserves class sizes but changes the assignment, and class-0 pairs are quantized more precisely (err 0.080 vs 0.523). No probe falsified the kid.

NEAR MISS. The cheap parent mistake here is to re-run the kid's own suite and call that evidence; the second is to trust results.json. I read the script and ran independent probes instead. One of my own probes (C5) first FAILED because I sliced dims instead of pair classes -- the probe was wrong, not the code; fixed and re-run. A parent who stopped at the first red would have wrongly demoted the kid.
<!-- THOUGHT:END -->
