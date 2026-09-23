# SWR.01 gap table — deepseek-v4.1-flash (reference) vs the five local HumanEval arms

**Date:** 2026-09-21  **Round:** SWR.01 (HumanEval table) + SWR-B.02/SWR-B.03 (arm B IFEval row)  **Node:** experiment:a00-559ee702-d3c7dd (HumanEval); experiment:a00-4eec4fce-e9b330 (IFEval)
**Parent hypothesis:** hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery

## What is measured

| field | value |
|---|---|
| HumanEval eval | openai HumanEval, 164 problems, execution pass@1 via `human_eval.execution.check_correctness`, timeout 10 s |
| HumanEval scorer | `datasets/humaneval-abc/scorer.py`, run **UNCHANGED** with `ABC_OUTDIR=datasets/switch-rule/2026-09-21` |
| HumanEval reference | `deepseek/deepseek-v4.1-flash` via OpenRouter (provider DeepInfra), temperature 0.0, top_p 1.0, top_k 1, seed 1234, max_tokens 512, 1 sample/problem |
| thinking-off | local arms: llama.cpp `chat_template_kwargs {"enable_thinking": false}`; reference: OpenRouter `reasoning {"enabled": false}` (the documented equivalent — see README deviation) |
| HumanEval template | the ONE fixed user template hard-coded in `datasets/humaneval-abc/runner.py` (byte-identical for reference and all five local arms) |
| IFEval eval | official Google `instruction_following_eval`, 541 prompts, **strict prompt-level accuracy** from `evaluation_main.py` |
| IFEval reference | same model, temperature 0.0, top_p 1.0, seed 1234, max_tokens 1280, 1 sample/prompt, one response in official input order |

**Label semantics.** pass@1 = fraction of the 164 problems whose single greedy
sample passes the official execution checker (exact numerator/164).
Relative pct = local score ÷ reference score × 100. **Switch rule:** a row
FIRES iff local ≥ 0.9 × reference on that eval.

## HumanEval — 164 problems, all rows scored by the same scorer

Reference: **154/164 = 93.9 %**.  0.9 × reference threshold = **84.5 %**.

| arm (tag) | model | pass@1 | rel. pct vs ref | λ vs ref: c (#arm-only) | b (#ref-only) | McNemar exact p | switch verdict |
|---|---|---|---|---|---|---|---|
| ref_deepseek-v4.1-flash | deepseek/deepseek-v4.1-flash (OpenRouter) | 154/164 = 93.9 % | 100.0 % | — | — | — | — (reference row) |
| armA_qwen3.5-9b-q4km | Qwen3.5-9B-Q4_K_M | 128/164 = 78.0 % | 83.1 % | 3 | 29 | 0.0000 | **does not fire** |
| armA2_qwen3.5-9b-q4km-fork | Qwen3.5-9B-Q4_K_M through the prism fork | 130/164 = 79.3 % | 84.4 % | 3 | 27 | 0.0000 | **does not fire** |
| armB_bonsai27b-ptq1 | Bonsai 2 27B PTQ1_0 (no LoRA) | 142/164 = 86.6 % | 92.2 % | 3 | 15 | 0.0075 | **FIRES** |
| armC1_bonsai27b-abliterate-s1 | B + OrcaBonsai LoRA scale 1 | 141/164 = 86.0 % | 91.6 % | 3 | 16 | 0.0044 | **FIRES** |
| armC2_bonsai27b-abliterate-s2 | B + OrcaBonsai LoRA scale 2 | 143/164 = 87.2 % | 92.9 % | 4 | 15 | 0.0192 | **FIRES** |

`c` = problems the arm passes and the reference fails; `b` = problems the
reference passes and the arm fails. Columns are in this order to match the
numeric cells, which are unchanged (the header labels were previously swapped:
the first column held arm-only counts under a `b (#ref-only)` header). Counts
are computed from the actual per-problem pass/fail bits in
`scorer.py:per_problem`, not estimated. Arithmetic check: for every arm row
`ref_pass − arm_pass = b − c` (armA 154−128=26=29−3; armB 154−142=12=15−3;
armC2 154−143=11=15−4). The reference beats
every local arm with a significant paired difference on all five (p ≤ 0.019);
the three Bonsai-based arms still clear the 0.9× relative bar.

**Best local candidate:** C2 (87.2 %, 92.9 % of reference) — FIRES. Among the
three the hypothesis names {B, C1, A}, the best is B (86.6 %, 92.2 %) — FIRES.

## IFEval — reference and arm B, all 541 prompts, one unchanged official harness

Official `instruction_following_eval/evaluation_main.py` run **UNCHANGED** with the
same `ifeval_input_data.jsonl`; **strict prompt-level** is the metric in the
`field` table above. Scored ONCE per row, never averaged.

| row | strict prompt-level accuracy | loose prompt-level accuracy | instruction-level (strict) |
|---|---|---|---|
| ref_ifeval_deepseek-v4.1-flash | **0.868762 (470/541)** | 0.894640 | 0.908873 |
| armB_bonsai27b-ptq1 | **0.778189 (421/541)** = 89.57 % of ref | 0.815157 (441/541) | 0.851319 (710/834) |

Arm B threshold on IFEval: 0.9 × 0.868762 = **0.781886**. 421 < 423 prompts, so
arm B **does not fire on IFEval** — short of the bar by 0.37 pp. That margin is
*inside* the ±0.4 pp langdetect floor (see below), so the honest reading is
"no fire, but within scorer noise of the bar" rather than a clean miss.

Generation completed cleanly (541/541, exact official order, unique, nonempty);
exact commands in `experiment:a00-4eec4fce-e9b330`.

Arm B fires on HumanEval (92.2 % rel.) and misses on IFEval (89.57 % rel.), so
arm B alone does **not** satisfy the two-eval hypothesis. No mvp minted here.

*Measurement floor.* The official harness re-scores the **reference** at
469–472/541 across runs of the same file: `instruction_following_eval/
instructions.py` calls `langdetect.detect()` (L158, L1416, L1448) unseeded, so
language-detection instructions are non-deterministic. Any IFEval row here,
and the 0.868762 reference itself, carries ±~0.4 pp scorer noise.

## Hypothesis verdict — the 10 pct rule

The hypothesis asks for local ≥ 0.9 × reference on **both** evals. This round
measured the reference on both and the locals on one:

- **HumanEval: LEANS PROVED.** Three of five local arms (B, C1, C2) are within
  10 pct relative of the reference, the best at 92.9 %. The two 9B arms miss.
- **IFEval: arm B row landed.** 0.778189 strict = 89.57 % of reference, 0.37 pp
  under the 0.9 bar and inside the ±0.4 pp floor. **Does not fire.**
- Net: arm B clears one eval and misses the other by less than the noise floor;
  no local arm has yet been scored on IFEval at all beyond B. Recorded as
  `inconclusive_lean_proved:55` on `experiment:a00-4eec4fce-e9b330`.

**Do not read this as a switch.** Per the owner's rule it is a trigger for an
mvp that ties the contributing chains together — the master mints that, never
this round.