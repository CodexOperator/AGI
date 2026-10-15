# Kid A — r1 verify-batch cost, commands + derived ratios

Box: /home/ubuntu/src/llama.cpp/build/bin/llama-bench (093a2f8-class build), 4 threads, shared arm-cloud 4c.
Tenancy protocol reproduced from extensions/agi/bin/lm_bench.py (loadavg 1/5/15 + MemAvailable +
SwapFree + pgmajfault + top_rss before/after each invocation).

## Commands (verbatim)

```
/home/ubuntu/src/llama.cpp/build/bin/llama-bench -m /home/ubuntu/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf -t 4 -p 1,2,4,5,6,8 -n 32 -d 0 -r 3 -o jsonl
/home/ubuntu/src/llama.cpp/build/bin/llama-bench -m /home/ubuntu/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf -t 4 -p 1,2,4,5,6,8 -n 32 -d 1024 -r 3 -o jsonl
/home/ubuntu/src/llama.cpp/build/bin/llama-bench -m /home/ubuntu/.cache/lm-models/Qwen3.5-4B-Q4_K_M.gguf -t 4 -p 1,2,4,5,6,8 -n 32 -d 0 -r 3 -o jsonl
/home/ubuntu/src/llama.cpp/build/bin/llama-bench -m /home/ubuntu/.cache/lm-models/Qwen3.5-4B-Q4_K_M.gguf -t 4 -p 1,2,4,5,6,8 -n 32 -d 1024 -r 3 -o jsonl
```

Rows: 14 per model (6 pp batches k=1,2,4,5,6,8 + one n=32 tg run, at d=0 and d=1024), -r 3.
Derived: t_batch_ms(k) = 1000*k/pp_ts ; t_step_ms = 1000/tg_ts ; ratio(k) = t_batch/t_step.
Control: t_pp1 = 1000/pp1_ts must reproduce t_step within noise.

## Derived table (avg over the 3 reps; stddev_ts in parens)

| model | d | pp1 ms | pp5/pp6 ms | step ms | ratio k=5/6 | control t_pp1/t_step | load before/after |
|---|---|---|---|---|---|---|---|
| Qwen3-0.6B-Q8_0.gguf | 0 | 21.2 (4050.8) | 232.2 (0.0) | 30.3 (0.0) | 7.66x | 0.70 | 2.34 / 2.51 |
| Qwen3-0.6B-Q8_0.gguf | 1024 | 284.9 (65943.6) | 549.8 (0.0) | 90.7 (0.0) | 6.06x | 3.14 | 2.51 / 3.71 |
| Qwen3.5-4B-Q4_K_M.gguf | 0 | 512.3 (25553.4) | 835.0 (0.0) | 223.7 (0.0) | 3.73x | 2.29 | 4.98 / 4.94 |
| Qwen3.5-4B-Q4_K_M.gguf | 1024 | 222.1 (78180.0) | 941.1 (0.0) | 300.9 (0.0) | 3.13x | 0.74 | 4.94 / 5.53 |

## Per-repeat spread (stddev_ts of the 3 reps, tok/s)

| model | d | pp1 | pp5/6 | tg |
|---|---|---|---|---|
| Qwen3-0.6B-Q8_0.gguf | 0 | 9.02 | 1.13 | 4.81 |
| Qwen3-0.6B-Q8_0.gguf | 1024 | 0.81 | 1.76 | 5.93 |
| Qwen3.5-4B-Q4_K_M.gguf | 0 | 0.10 | 0.37 | 1.49 |
| Qwen3.5-4B-Q4_K_M.gguf | 1024 | 1.59 | 0.33 | 1.00 |

## Re-sampling run (interleaved, -r 1, 10 rounds, 0.6B k=5)

Purpose: test whether the pp1 control failure is contention or a real
small-batch overhead. One invocation per round: `-p 1,5 -n 32 -d <d> -r 1`.
loadavg over the run: 4.25 -> 6.69. Raw samples:
`.agi/sessions/iter-TM.18/a00-289cd1de/sample_r1-0.6B.jsonl`.

| d | pp1 tok/s | pp5 tok/s | tg tok/s | t_pp1 ms | t_batch ms | t_step ms | ratio(5) | control |
|---|---|---|---|---|---|---|---|---|
| 0 | 4.74 | 21.92 | 4.23 | 210.8 | 228.1 | 236.2 | 0.97x | 0.89 |
| 1024 | 12.37 | 23.55 | 7.58 | 80.8 | 212.3 | 131.9 | 1.61x | 0.61 |

## Control result

FAILS. t_pp1/t_step = 0.67 (0.6B d=0, first run), 1.10 (0.6B d=1024, first run),
2.29 (4B d=0), 0.74 (4B d=1024), 0.89 (0.6B d=0, resample median), 0.61 (0.6B d=1024,
resample median). The pp1 control holds at only one of six (model, depth) points
within +/-20%; the same binary re-run twice gives pp1 = 4.4 and 47.3 tok/s (10.8x)
for identical work. The run is DISCARDED per the node's own control rule.

## loadavg

Every invocation logged. Minimim l1 seen 2.34, maximum 6.69. The verdict gate
(loadavg <= 4.0 during the rows) is NOT met for the 4B rows (4.94-5.53) and for
the 0.6B rows only while load rose through 3.7.

## Secondary observation (not verdict-grade)

t_pp1 is 0.5-1.5x the tg step at some points and 2.3x at others, and t_pp1
sometimes exceeds a FULL step: 513 ms for a 1-token prefill vs 224 ms for a
decode step on the 4B d=0. A 1-token prefill cannot legitimately cost more
than one step, so the pp(k) rows for small k carry a fixed per-test overhead
that does not amortise. That overhead is exactly what makes ratio(5/6) swing
0.97x <-> 7.7x for the same 0.6B d=0 k=5 measurement. The claim's
t(batch-k)=k/pp_ts(k) therefore needs a baseline that is measured on the SAME
test shape (e.g. pp_k minus pp_{k-1}, or a batched-decode control), not pp1.
