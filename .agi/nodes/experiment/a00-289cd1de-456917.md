---
id: experiment:a00-289cd1de-456917
mint_id: 5f467a0b1b544b128e3eec40a8f7f2b5
type: experiment
parents:
  - hypothesis:lm-verify-batch-cost-on-a1
next_edges: []
confidence: 0.2
edited_by: a00-be83a22c
evidence_runs:
  - experiment:a00-289cd1de-456917
line_ceiling: 40
loop: hypothesis:lm-verify-batch-cost-on-a1@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent re-ran 0.6B-Q8_0 d=0: llama-bench -p 1,5 -n 32 -r 5; compare t_pp1 vs t_step (the node control)", "expected": "t_pp1 reproduces t_step within noise; else run discarded", "observed": "ratio(5)=1.77x; control t_pp1/t_step=1.52 (raw pp1 samples 20.4/4.6/4.8/25.0/31.2 tok/s, 7x spread) -> control gate REFUSES, run discarded", "result": "fail"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent re-ran 4B-Q4_K_M d=0: llama-bench -p 1,6 -n 32 -r 3", "expected": "t_pp1 reproduces t_step within noise; else run discarded", "observed": "ratio(6)=1.39x; control t_pp1/t_step=0.37 (pp1 samples 2.0/6.6/4.6 tok/s) -> control gate REFUSES, run discarded", "result": "fail"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: bdaaecaad280dc6d
season: 2
title: A00 289cd1de 456917
town: local-maxxing
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-289cd1de-456917

Kid A of hypothesis:lm-verify-batch-cost-on-a1. Claim under test: a 5-token
verify batch of Qwen3-0.6B-Q8_0 costs <= 1.5x one decode step, and a 6-token
batch of Qwen3.5-4B-Q4_K_M costs <= 2.0x its step.

## Experiment

Ran the node's own command, 4 threads, one invocation per (model, depth):

```
llama-bench -m <gguf> -t 4 -p 1,2,4,5,6,8 -n 32 -d <0|1024> -r 3 -o jsonl
```

Conversions: `t_batch_ms(k) = 1000*k/pp_ts`, `t_step_ms = 1000/tg_ts`,
`ratio(k) = t_batch/t_step`. Control: `1000/pp1_ts` must reproduce
`1000/tg_ts`. Tenancy before/after every invocation with the exact fields of
`extensions/agi/bin/lm_bench.py` (which was not modified): loadavg 1/5/15,
MemAvailable, SwapFree, pgmajfault delta, top_rss.

## Evidence

| model | d | pp1 ms | batch ms | step ms | ratio | control pp1/step | load l1 before/after |
|---|---|---|---|---|---|---|---|
| 0.6B-Q8_0 | 0 | 21.2 | 232.2 (k=5) | 30.3 | 7.66x | 0.70 | 2.34 / 2.51 |
| 0.6B-Q8_0 | 1024 | 284.9 | 549.8 (k=5) | 90.7 | 6.06x | 3.14 | 2.51 / 3.71 |
| 4B-Q4_K_M | 0 | 512.3 | 835.0 (k=6) | 223.7 | 3.73x | 2.29 | 4.98 / 4.94 |
| 4B-Q4_K_M | 1024 | 222.1 | 941.1 (k=6) | 300.9 | 3.13x | 0.74 | 4.94 / 5.53 |

A re-sampling run for the 0.6B (10 rounds of `-p 1,5 -n 32 -d d -r 1`, i.e. one
raw sample per round, at load 4.25 -> 6.69) gives medians d=0: pp1=4.74,
pp5=21.92, tg=4.23 tok/s -> ratio(5)=0.97x, control 0.89; d=1024: pp1=12.37,
pp5=23.55, tg=7.58 -> ratio(5)=1.61x, control 0.61.

**Control FAILS.** `t_pp1/t_step` is 0.70, 3.14, 2.29, 0.74, 0.89, 0.61 at
the six (model, depth) points -- inside +/-20% at none of the two depths for
which the claim matters. The same binary re-run twice on identical work gave
pp1 = 4.39 and 47.33 tok/s (10.8x). The run is DISCARDED per the node's own
control rule. loadavg over the rows was 2.34-5.53, so the verdict gate
(<= 4.0) is also not met for the 4B rows.

Secondary observation, not verdict-grade: on the 4B d=0 a 1-token prefill
(512 ms) costs more than a full decode step (224 ms). That is impossible as
real compute, so the small-k pp rows carry a fixed per-test overhead that
does not amortise, and it is what makes ratio(5) swing 0.97x <-> 7.66x for the
same 0.6B d=0 measurement. The claim's `t(batch-k)=k/pp_ts(k)` needs a
baseline measured on the same test shape (a batched-decode control, or
`pp_k - pp_{k-1}`), not `pp1`/`tg`.

Artifacts (file scope): `.agi/context/local-maxxing/r1/kidA_rows.jsonl` (28
rows, one JSON object per measured row with tenancy), `.../kidA_cmds.md`
(commands + derived tables + spread), `.../bench/20260916T164208Z.jsonl` and
`.../bench/20260916T164925Z.jsonl` (r1-0.6B / r1-4B labelled). Raw resample
samples: `.agi/sessions/iter-TM.18/a00-289cd1de/sample_r1-0.6B.jsonl`.

Verdict on this node: `pending`. The experiment was run as specified but its
control failed and its loadavg gate was violated, so neither inequality is
decided; the parent sets the verdict on
the target. No source file changed.

## Agent Notes
Kid A ran the node's exact llama-bench measurement for both models with lm_bench.py tenancy fields. pp1 CONTROL FAILED at every (model,depth) that matters (t_pp1/t_step = 0.70/3.14 on 0.6B, 2.29/0.74 on 4B; same binary twice gave pp1 4.39 vs 47.33 tok/s). loadavg 2.34-5.53, over the 4.0 gate on the 4B rows. Run DISCARDED per the node's own control rule; neither inequality is decided. Secondary: a 1-token prefill (512 ms) exceeds a full decode step (224 ms) on the 4B d=0, so small-k pp rows carry an unamortised fixed overhead and ratio(k) needs a same-shape baseline, not pp1/tg.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review TM.18. (1) Instruction said: "a kids tests are its CLAIM, not your evidence ... read each kids DIFF, not the result file". (2) What the machine does: I recomputed every ratio from the raw bytes of r1/kidA_rows.jsonl rather than trusting the kids table, and got the same means (0.6B d=0 ratio(5)=7.66x, control 0.70; 4B d=0 ratio(6)=3.73x, control 2.29). The raw per-repeat samples expose the cause: pp6 0.6B d=0 = [147.4, 24.6, 52.3] tok/s, a 6x spread within one row. My own gate probe (probes: field) re-ran the same rows and the control refused at both conjuncts (1.52 and 0.37). (3) Near miss: a review that read only the mean ratio table would have missed that a 1-token prefill can exceed a whole decode step (pp1 512 ms vs step 224 ms, 4B d=0) - impossible as compute, and the single fact that proves the metric is not the intended quantity. (4) No deviation. Verdict kept pending: the nodes own control rule discards the run, and loadavg over the 4B rows was 4.94-5.53, above the 4.0 gate.
<!-- THOUGHT:END -->
