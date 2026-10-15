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

---

# ADDENDUM — 2026-09-16T12:2xZ — agent `a00-80a08fbb` (Kid C residue, iter TM.10)

Two things the table above got wrong or left unnamed. Raw rows:
`.agi/context/local-maxxing/gpu/kidC_bench.jsonl`. Full write-up:
`experiment:a00-80a08fbb-3ad171`.

## 1. `pp512 = 10.44` was a COLD-FIRST-REQUEST number, not a prefill rate

The table's pp512 cell for the 35B is the cost of the **first request after
model load**, when the `--fit on` CPU-side MoE experts are still being
first-touched through the mmap. Same server, same config
(`-ngl 99 --n-cpu-moe 28 -np 1 -c 16384`), same 512-token request:

| 35B-A3B prefill | prompt_n | pp tok/s | wall s |
|---|---|---|---|
| pp512, cold (first request after load) | 524 | **9.58** | 55.28 |
| pp512, warm | 524 | **400.54** | 2.01 |
| pp8118, first request of a (partly warm) process | 8118 | **135.76** | 60.63 |
| pp8118, warm | 8110 | **593.78** | 15.12 |

The 42x cold/warm gap on the 512 control is inside ONE process and one config.
The loader states the mechanism itself:

```
tensor overrides to CPU are used with mmap enabled - consider using --load-mode none for better performance
```

**So the prefill line in the reading above is wrong in direction.** Prefill is
not the 35B's binding cost at kid-sized context: 8.1k tokens costs 13.7 s warm.
What costs ~55-60 s is the first token of a cold model, at any length. A kid
prompt's real price on this box is the cold start, once per load — not length.

At the warm 35B prefill rate the prompt-token row becomes
`(156.94+65+40)*0.15/(593.78*3.6)` = **$0.0184 / 1M prompt tokens** (was
$0.8666 quoted from the cold number — 47x over). The 9B's $0.0114 is unchanged.

## 2. The explicit split that reproduces `--fit on`, read back

`--fit on` never said what it chose; `/props` and `/v1/models` do not expose it.
Re-run with an explicit split instead (chosen from the GGUF tensor table: 40
layers x 332.0 MiB of `*_exps`, so ~1 expert layer per 332 MiB of VRAM):

| | `--n-cpu-moe` | CUDA0 model buffer | CPU_Mapped | VRAM at load |
|---|---|---|---|---|
| trial | 30 | 5230.32 MiB | 11485.69 MiB | 5976 MiB |
| **chosen** | **28** | **5894.32 MiB** | **10751.51 MiB** | **6640 MiB** |
| round-2 `--fit on` | (unknown) | — | — | 6666 MiB |

Load log, verbatim: `offloading 39 repeating layers to GPU`,
`offloaded 41/41 layers to GPU`. `--n-cpu-moe N` keeps the FIRST N layers'
experts on CPU (`common/arg.cpp` L2763-2772). `-ngl 99`, RSS
(`ps -o rss= -C llama-server`) **10,878,640 KB ~= 10.38 GiB**, `docker stats`
MemUsage 2.87-5.83 GiB, host `free -m` used 2.2-2.5 GB with ~13.5 GB in
`buff/cache`.

**tg128 is throughput-neutral vs `--fit on`, but noisy.** Seven
`max_tokens=128 ignore_eos` calls on this config: **8.22 / 12.56 / 16.39 /
20.90 / 41.12 / 42.10 / 44.12 tok/s** (median 20.90). Round 2's 12.396 sits
inside the spread; the 41-44 cluster is the fully-resident state. Any single
tg number from this box is good to ~2x, not better.

**Consequence for the cost table:** with a warm tg of 20.9 tok/s at 203.04 W
(`W_total` 308.04), the 35B's single-stream output row recomputes to
**$0.614 / 1M out** (was $0.7300); at the resident 44.12 tok/s it is **$0.291**,
and at 12.556 tok/s **$1.022**. Break-even vs `deepseek-v4-flash` at
308 W_total is **72.4 tok/s**. The conclusion in the reading above — that
electricity only closes the gap under aggregate batching — still holds on the
tg axis; what it does not hold on is the *prompt* axis, which is ~47x cheaper
than the table said.

**Router caveat.** The running router preset (`--fit on --jinja -np 2`, no
`-c`) gives the 35B **`n_ctx_slot = 4096`** while the 9B gets 23552, so an 8k
prompt cannot be issued against the running router for the larger model at all
(`request (10018 tokens) exceeds the available context size (4096 tokens)`).
Length beyond 4k for the 35B needs an explicit `-c`, i.e. a restart.
