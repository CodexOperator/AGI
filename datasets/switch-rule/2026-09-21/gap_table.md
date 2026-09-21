# SWR.01 gap table — deepseek-v4.1-flash (reference) vs the five local HumanEval arms

**Date:** 2026-09-21  **Round:** SWR.01  **Node:** experiment:a00-559ee702-d3c7dd
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

| arm (tag) | model | pass@1 | rel. pct vs ref | λ vs ref: b (#ref-only) | c (#arm-only) | McNemar exact p | switch verdict |
|---|---|---|---|---|---|---|---|
| ref_deepseek-v4.1-flash | deepseek/deepseek-v4.1-flash (OpenRouter) | 154/164 = 93.9 % | 100.0 % | — | — | — | — (reference row) |
| armA_qwen3.5-9b-q4km | Qwen3.5-9B-Q4_K_M | 128/164 = 78.0 % | 83.1 % | 3 | 29 | 0.0000 | **does not fire** |
| armA2_qwen3.5-9b-q4km-fork | Qwen3.5-9B-Q4_K_M through the prism fork | 130/164 = 79.3 % | 84.4 % | 3 | 27 | 0.0000 | **does not fire** |
| armB_bonsai27b-ptq1 | Bonsai 2 27B PTQ1_0 (no LoRA) | 142/164 = 86.6 % | 92.2 % | 3 | 15 | 0.0075 | **FIRES** |
| armC1_bonsai27b-abliterate-s1 | B + OrcaBonsai LoRA scale 1 | 141/164 = 86.0 % | 91.6 % | 3 | 16 | 0.0044 | **FIRES** |
| armC2_bonsai27b-abliterate-s2 | B + OrcaBonsai LoRA scale 2 | 143/164 = 87.2 % | 92.9 % | 4 | 15 | 0.0192 | **FIRES** |

`b` = problems the reference passes and the arm fails; `c` = problems the arm
passes and the reference fails. Counts are computed from the actual per-problem
pass/fail bits in `scorer.py:per_problem`, not estimated. The reference beats
every local arm with a significant paired difference on all five (p ≤ 0.019);
the three Bonsai-based arms still clear the 0.9× relative bar.

**Best local candidate:** C2 (87.2 %, 92.9 % of reference) — FIRES. Among the
three the hypothesis names {B, C1, A}, the best is B (86.6 %, 92.2 %) — FIRES.

## IFEval — reference only

Reference `deepseek/deepseek-v4.1-flash`, official harness:

| row | strict prompt-level accuracy | loose prompt-level accuracy | instruction-level (strict) |
|---|---|---|---|
| ref_ifeval_deepseek-v4.1-flash | **0.868762 (470/541)** | 0.894640 | 0.908873 |

**There is no local IFEval row yet.** None of A, A2, B, C1, C2 has been scored
on IFEval, so the IFEval column of the gap table has exactly one row and no
local row can be tested against 0.9 × 86.88 % = 78.19 %. A local IFEval row is
a later chunk under goal:g14.11.1, not this round.

## Hypothesis verdict — the 10 pct rule

The hypothesis asks for local ≥ 0.9 × reference on **both** evals. This round
measured the reference on both and the locals on one:

- **HumanEval: LEANS PROVED.** Three of five local arms (B, C1, C2) are within
  10 pct relative of the reference, the best at 92.9 %. The two 9B arms miss.
- **IFEval: UNDECIDED.** The reference is 86.88 % strict; no local row exists.
- Net: the two-eval promise cannot be decided this round. Recorded as
  `inconclusive_lean_proved:60` on `experiment:a00-559ee702-d3c7dd`.

**Do not read this as a switch.** Per the owner's rule it is a trigger for an
mvp that ties the contributing chains together — the master mints that, never
this round.