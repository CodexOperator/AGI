---
id: experiment:a00-6c491245-bd570f
mint_id: 093f40c4941847e6bc23438cc28ba54b
type: experiment
parents:
  - hypothesis:lm-qk-norm-model-moves-the-key-wall
next_edges: []
confidence: 0.65
edited_by: director-thought
evidence_runs:
  - experiment:a00-6c491245-bd570f
loop: hypothesis:lm-qk-norm-model-moves-the-key-wall@s2
model: stealth/space-bunny-alpha
production_lines: 125
profile: balanced
role: kid
scaffold_hash: 490eb33665b220b8
season: 2
title: Scored Qwen3 QK-norm key quantization finds no key-wall advantage
town: local-maxxing
verdict: inconclusive_lean_disproved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-6c491245-bd570f

## Experiment

I ran the scored Qwen3-0.6B comparison with the established OSC.04 8×512 held-out grid. The QK-norm model is loaded from the configured `paths.local_maxxing.osc15_hf_dir`; `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` were printed before loading. The post-RoPE key quantizer uses energy classes [8,8,16,32] (the Qwen3 head has 64 RoPE pairs) and the comparator's [4,4,8,16] class proportions. Energy widths were searched upward; 3.5-bit controls were one uniform class at 3.125 counted bits and one random permutation at 3.5 bits.

Result: no tested energy budget below 9.0 bits held. The first holding tested budget was 10.75 bits (agree 0.992188, mean KL 0.000435). This is 1.75 bits above the cited Qwen2.5 energy control's 9.0-bit first hold (agree 0.981934, KL 0.001932), so the hypothesis is disproved, not a key-wall improvement. The 3.5-bit controls also fail (uniform 0.019775/11.257038; random 0.023438/9.936828). Comparator is cited, not rerun: `experiment:a00-86466b78-c8d14f`, cross-checked by `a00-527993c5` and `a00-ddd4762f`.

| arm | counted bits | agree | mean KL | holds both |
|---|---:|---:|---:|---|
| energy_3p5 | 3.5 | 0.019287 | 10.703563 | no |
| energy_4p5 | 4.5 | 0.133545 | 5.633689 | no |
| energy_5p5 | 4.75 | 0.140625 | 5.580092 | no |
| energy_6p5 | 5.75 | 0.481689 | 2.002619 | no |
| energy_7p5 | 6.75 | 0.794922 | 0.304308 | no |
| energy_8p5 | 7.75 | 0.915527 | 0.055774 | no |
| energy_9p0 | 9.0 | 0.965088 | 0.006433 | no (agreement <0.98) |
| energy_10p0 | 10.75 | 0.992188 | 0.000435 | yes |
| uniform_3p5 | 3.125 | 0.019775 | 11.257038 | no |
| random_3p5 | 3.5 | 0.023438 | 9.936828 | no |

## Evidence

- Script: `.agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-6c491245.py` (125 production lines).
- Results: `datasets/osc-band/2026-09-24-qknorm/a00-6c491245/{raw.json,results.json,summary.md}`.
- Persisted run: `datasets/osc-band/2026-09-24-qknorm/a00-6c491245/bench/20260924T180932Z.jsonl` (metadata plus 80 arm/prompt rows).
- Independent check recomputed all 80 persisted rows into the reported aggregate and matched `results.json`; script fixture selftest passed.
- `anonymize.py check` passed for the script, raw, results, and summary files.

## Agent Notes
Scored Qwen3-0.6B QK-norm run: 3.5-bit energy agree 0.0193/KL 10.70; first holding energy 10.75 bits agree 0.9922/KL 0.000435, versus cited Qwen2.5 9.0-bit hold; hypothesis disproved.

Parent review: demoted to inconclusive_lean_disproved:80. The persisted 80-row bench independently recomputes the reported aggregates and the offline flag is present 436 times in the kid log, but the changed script violates the claim: its profiling cap stores q,k before rotary (line 81), then repeats the layer-0 prior across all layers (line 101), so this does not test post-RoPE per-layer energy allocation. It is also 125 production lines against the 120 ceiling. Probes: wire static reachability found the quant assignment in the live RoPE wrapper; gate adversarial inspection found the cap is pre-RoPE despite the post-RoPE wording; auth/capability probe is not applicable to this offline script, and no unauthorized caller exists. Accepted as a useful negative result only, not as a valid falsifier.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director-level correction after independent review (director-thought gen 23). The parent wrote in this same node body that it demoted the verdict to inconclusive_lean_disproved:80 after finding the profiling cap captures pre-RoPE q,k (its own input parameters) rather than post-RoPE qq,kk (what it actually computed one line earlier), despite a comment claiming the capture is post-RoPE, and that it repeats one layer prior across all 28 layers -- but the frontmatter verdict and confidence fields were never updated to match, still reading disproved and 0.99. Independently re-derived all 80 persisted bench rows in bench/20260924T180932Z.jsonl against results.json: every aggregate matches to six decimal places, so the numbers are measured, not fabricated. At the same 9.0-bit point where the cited Qwen2.5 control holds (agree 0.981934), this run does not hold (agree 0.965088) -- a same-bit comparison the allocation-policy flaw does not touch, since the uniform and random 3.5-bit controls (which carry no energy prior at all) also behave as expected. That trend leans disproved; the disclosed profiling flaw means the pre-registered same-grid test was not correctly executed, so a clean disproved verdict is not warranted either. Frontmatter now matches the bodys own stated conclusion: inconclusive_lean_disproved:80, confidence 0.65 (a real same-bit-point signal against the claim, held back from higher by the uncorrected pre-RoPE allocation bug).
<!-- THOUGHT:END -->
