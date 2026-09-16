# kidC_cost — electricity cost per million OUTPUT tokens, local-town vs OpenRouter

Agent `a00-4869b99b` (Kid C, iter TM.07), 2026-09-16T10:36Z. All tok/s in this file are
**tunnel-side**: measured from core-town through `127.0.0.1:18080` (the `local-town-tunnel`
systemd --user unit forwarding to the loopback llama-server). Raw rows:
`.agi/context/local-maxxing/bench/20260916T103631Z.jsonl` (labels `gpu-*`).

## Formula (as ordered, $/kWh an explicit PARAMETER)

```
USD per 1M output tokens = (GPU power.draw W + 65 W CPU + 40 W system) / 1000
                             * ($/kWh) / (tok/s * 0.0036)
```

**PARAMETER: $/kWh = $0.15** (owner-declared; not measured). Equivalently
`W_total * $/kWh / (tok/s * 3.6)`. W_total = GPU + 65 + 40.

GPU W is the `gpu_power_draw_max_w` of the matching sampler window in
`/data/ml/logs/sample_*.log` (nvidia-smi sampled every 2 s; `/proc/loadavg` beside it).

## Measured rows (all tunnel-side; 2026-09-16)

| model | quant | GPU W max | tg128 single tok/s | -np agg tok/s | VRAM MiB | loadavg1 max |
|---|---|---|---|---|---|---|
| Qwen3.5-9B (dense, fully on GPU, -np 2) | Q4_K_M | 238.13 | **62.535** | 67.84 (@np2) | 6686 | 1.37 |
| Qwen3.5-35B-A3B (MoE, `--fit on` CPU offload, -np 4) | Q3_K_M | 112.18 | **12.396** | 51.09 (@np4, 40.11 @np2) | 6666 | 3.27 |

pp512 (tunnel-side, same runs): 9B **1257.22** tok/s; 35B-A3B **10.44** tok/s (CPU-offloaded
experts make prompt processing ~120x slower than the 9B — this is the real 35B cost driver).

## Cost row

| model | speed | W_total | USD / 1M out @$0.15/kWh | vs OpenRouter deepseek-v4-flash ($0.1772) | vs deepseek-v4.1-flash ($1.20) |
|---|---|---|---|---|---|
| Qwen3.5-9B Q4_K_M | tg128 single | 343.13 | **$0.2286** | 1.29x more | 5.2x cheaper |
| Qwen3.5-9B Q4_K_M | @np2 aggregate 67.84 | 343.13 | **$0.2107** | 1.19x more | 5.7x cheaper |
| Qwen3.5-35B-A3B Q3_K_M | tg128 single | 217.18 | **$0.7300** | 4.12x more | 1.64x cheaper |
| Qwen3.5-35B-A3B Q3_K_M | @np4 aggregate 51.09 | 217.18 | **$0.1771** | **1.00x — exact break-even** | 6.8x cheaper |

Prompt-token cost at the 35B-A3B's measured pp rate, same formula on pp512:
**$0.8666 / 1M prompt tokens** (9B: `343.13*0.15/(1257.22*3.6)` = $0.0114 /1M prompt).

### Break-even (formula inverted, W_total = 300 W as the tests block names)
- vs kid-class cloud (`deepseek-v4-flash` $0.1772/1M out): need **>= 70.54 tok/s**.
- vs parent-class cloud (`deepseek-v4.1-flash` $1.20/1M out): need **>= 10.42 tok/s**.

## Reading

- **Single-stream, neither GPU model beats the kid-class cloud model on electricity.** The 9B is
  1.2-1.3x over; the 35B single-stream is 4.1x over.
- **Aggregate batching is what closes the gap.** At -np4 the 35B-A3B reaches 51.09 tok/s aggregate,
  which lands on **exact break-even** with `deepseek-v4-flash` ($0.1771 vs $0.1772). At -np2 it is
  1.27x over. The 9B's -np2 only lifts 62.5 -> 67.8 (its two slots contend for the same SM), so
  batching helps the CPU-offloaded MoE far more than the fully-resident dense 9B.
- **The 35B-A3B already beats the parent-class cloud model 1.6x-6.8x** at every measured rate,
  including single-stream. For parent-tier reasoning (deepseek-v4.1-flash class) the box pays for
  itself on electricity alone; the 35B's 12.4 tok/s is still above every parent-model break-even.
- **The binding constraint for the 35B is prompt processing, not generation.** pp512 = 10.44 tok/s
  means a 512-token prompt costs 49 s of wall and ~$0.001 of electricity before one output token.
  Kid-sized 30-60k contexts would be minutes of prefill. If the 35B is used, it should be with
  prefix caching / short prompts, or accept the prefill latency as the price of $0 marginal cost
  and local privacy.

## Caveats / what is weak

- $/kWh = 0.15 is a PARAMETER, not a measured tariff; the whole table scales linearly with it.
- CPU (65 W) and system (40 W) are the tests block's fixed allowances, not measured on this box
  (x86-8c, 15 GB RAM). Only GPU W is measured.
- Aggregate tok/s counts generated tokens over wall time including a short prefill; at 512-prompt
  kid contexts the aggregate would fall (prefill amortised differently).
- The 35B-A3B single-stream tg was 12.396 tok/s with a ~36-token prompt; longer prompts lower it.
- Electricity is the owner's own cost; this row exists to answer "off OpenRouter how far", not to
  bill anyone.
