# Kid B — bytes-per-token ledger derivation, reversed-order control (TM.18)

Rows: `.agi/context/local-maxxing/r1/kidB_rows.jsonl` (28), also `bench/20260916T165510Z.jsonl`, labels `r1-B-*`.
Order REVERSED vs Kid A: 4B-Q4_K_M first, then 0.6B-Q8_0. One `llama-bench -t 4 -p 1,2,4,5,6,8 -n 32 -d <0|1024> -r 3 -o json` per (model,depth); tenancy snapshot around each invocation, fields identical to `extensions/agi/bin/lm_bench.py` (unmodified). llama.cpp build 093a2f8.

## Ledger (from GGUF kv metadata, read directly)

| model | n_layer | n_kv_head | head_dim | KV bytes/token = L·H·D·2(K+V)·2B(f16) | GGUF bytes W |
|---|---|---|---|---|---|
| Qwen3-0.6B-Q8_0 | 28 | 8 | 128 | 28·8·128·2·2 = 114,688 (112 KiB) | 639,447,744 |
| Qwen3.5-4B-Q4_K_M | 32 | 4 | 256 | 32·4·256·2·2 = 131,072 (128 KiB) | 2,740,937,888 |

Decode step is bandwidth-bound: every weight must be read once per step. Step bytes at depth `d` = `W + d·KV`. Batch-k prefill = one weight pass + k tokens' attention/FFN; the KV term it adds is `k·KV`.
Predicted ratio `t(batch-k)/t(step) = 1 + k·KV/(W + d·KV) + (compute term)`.
- 0.6B d=0, k=5: KV term 0.0897% → **pred 1.0009**; d=1024: W+1024·KV=756,888,256 → **pred 1.0008**
- 4B d=0, k=6: KV term 0.029% → **pred 1.0003**; d=1024: W+1024·KV=2,875,155,616 → **pred 1.0003**

The ledger says the KV read is a rounding error at k≤6; a batch-k that costs more than ~1.0x a step is spending it on compute, not bytes. So the derivation **predicts ratio ≈ 1.0** (upper bound k, if prefill were purely compute-bound).

## Predicted vs measured (this control, 3 reps averaged)

| model | d | k | pred | meas | Δ | pp1_ms | step_ms |
|---|---|---|---|---|---|---|---|
| 0.6B-Q8_0 | 0 | 5 | 1.00 | 1.17 | +17% | 245.0 | 189.9 |
| 0.6B-Q8_0 | 1024 | 5 | 1.00 | 1.74 | +74% | 273.2 | 175.9 |
| 4B-Q4_K_M | 0 | 6 | 1.00 | 4.35 | +335% | 998.5 | 214.6 |
| 4B-Q4_K_M | 1024 | 6 | 1.00 | 1.51 | +51% | 578.0 | 544.3 |

Within 25%: 1 of 4 (0.6B d=0 only).

## Control result — FAILS, and it is the finding

`pp1` must reproduce one decode step (ratio ≈ 1.0). Measured pp1/step: **1.29, 1.56, 4.65, 1.06**. At three of four points a 1-token prefill costs *more* than a full 32-token decode step — impossible as compute. llama-bench's prompt test carries a fixed per-test overhead (context init/reset per test) that does not amortise at k≤8, so `t(batch-k)=1000·k/pp_ts(k)` is not measuring the intended quantity. Same failure Kid A saw (a 512 ms pp1 against a 224 ms step on 4B d=0).

Ratios also do **not** reproduce Kid A's: Kid A 7.66 / 6.06 / 3.73 / 3.13 vs B 1.17 / 1.74 / 4.35 / 1.51 (6.5x apart at 0.6B d=0). Loadavg 3.39→5.42 during the rows (Kid A 2.34→5.53); the node's own tenancy gate is <2 (round rule: >4 ⇒ pending at best). Verdict on the claim `derivation predicts measured ratio within 25%`: **the metric cannot validate it, so it cannot be proved; at the point it is least broken (0.6B d=0) the derivation is within 25%**, which is why the lean is not a clean disproof.

Next round must use a same-shape baseline: a batched-decode control (k decode positions in one forward vs 1) or a server-side `n_prompt` that amortises the per-test overhead, on a quiet box (loadavg < 2).
