---
id: experiment:a00-6ce9cb00-d60152
mint_id: ebd9699cf70741e0900c593d2798b584
type: experiment
parents:
  - hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box
next_edges: []
confidence: 0.7
edited_by: a00-6ce9cb00
evidence_runs:
  - experiment:a00-6ce9cb00-d60152
line_ceiling: 40
loop: hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: b1d620687c399d93
season: 2
title: "Bonsai2-27B-PTQ1_0 on the 8GB box: 64K load PASS, abliteration LoRA routed but byte-identical at scales 1-2, cost rows B and C"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-6ce9cb00-d60152

## Experiment

Steps 1, 2 and 4 of the pre-registered protocol for `hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box`, on
local-town (RTX 2070 SUPER 8 GB, sm_75). The stock `llama-server` container was stopped for arms B/C and restored
before this node was written (see Restore). HumanEval (step 3) is deliberately NOT run here — that is the next kid.

All commands ran inside `ghcr.io/ggml-org/llama.cpp:server-cuda` (`--gpus all --network host`) against the prebuilt
fork `/data/ml/llama-prism-fork/fork/llama-prism-b10685-7dffb15`, `LD_LIBRARY_PATH=/fork`, host port 8899 only.

### Step 1 — load gate (arm B)

Assembled the model:

```
cd /data/ml/models/bonsai && cat Ternary-Bonsai-2-27B-PTQ1_0.gguf.seg0{00..11} > Ternary-Bonsai-2-27B-PTQ1_0.gguf
sha256sum Ternary-Bonsai-2-27B-PTQ1_0.gguf
```

- assembled size **5,946,648,928 B**, sha256 **53107f530aa52eb00912263ab1ee29bd199261c87cd7b4ad4ca1318c1fe33ee3**
  — byte-for-byte the pinned hash.
- Served the verbatim `serve/8gb.sh` line (sha256 7d005cd1…): `-m <gguf> -c 65536 -ngl 99 -fa on -np 1 -ctk q4_0 -ctv q4_0 --jinja --temp 1.0 --top-p 0.95 --top-k 20 --host 127.0.0.1 --port 8899`.

Measured gate values:

| falsifier | expected | measured |
|---|---|---|
| `n_layer_all` / `n_layer` | 64 | **64** (`qwen35.block_count=64`, read from the GGUF header; the fork log at `-lv 3` does not print it) |
| `offloaded … to CPU` lines | 0 | **0** |
| `cudaMalloc` / OOM matches | 0 | **0** |
| peak VRAM while loaded | < 8192 MiB | **7268 MiB** at load, **7302 MiB** during bench |
| `/health` | 200 | **200** after ~60 s |

**Arm-B context = 65536. No fallback to 32768/16384 was needed.** This is the box's first confirmed 64K load of the
27B ternary on 8 GB; usable headroom ≈ 890 MiB.

### Step 2 — adapter-in-graph gate (arm C)

Same server, same weights, restarted with `--lora /lora/bonsai-abliterate-lora.gguf --lora-init-without-apply`
(9,682,464 B, sha256 f1669534803d340a496015f5c45125f3437b4d13ec764f40e34488ce83967f42 — matches). 5 fixed coding
prompts, greedy (`temperature 0`, `top_k 1`, `seed 12345`, `max_tokens 256`), thinking off, chat `--jinja` template.

| scale | 5-prompt result vs arm B |
|---|---|
| 0 | **byte-identical** on all 5 (sha256 p0 52ef4171…, p1 5fa8e0b7…, p2 48ecee30…, p3 4aed58c1…, p4 2995f624…) |
| 1 | byte-identical to scale 0 on all 5 |
| 2 | byte-identical to scale 0 on all 5 |
| 3 | **all 5 empty** (completion collapses to EOS/degenerate repetition) |

The gate's literal PASS conditions hold (scale 0 == B, scale 3 visibly degraded), so **arm C is not the inert
`read:orcabonsai` trap**. But the README ladder is degenerate at the *token* level: scales 1 and 2 are byte-identical
to base. The adapter is nonetheless in the compute graph — first-token logprobs move:

| scale | top-1 `"The capital of France is"` logprob |
|---|---|
| 0 | **-0.18611** |
| 1 | -0.17929 |
| 2 | -0.18897 |
| 3 | -1.13561 |

scale 0 is exactly reproducible before and after scale 3 (-0.18611 twice), so the perturbation is the adapter and not
noise. Conclusion: the LoRA is routed; its scale-1/2 delta is below the greedy decision margin for these 5 prompts,
and only scale 3 moves the argmax. A HumanEval run at scale 1 will therefore differ from B only on near-tie tokens —
this is the single biggest caveat for the next kid's step 3.

### Step 4 — cost rows

Empty context (server `/completion` timings; these are server timings, not `llama-bench`), 16K depth on a 16,801-token
prompt. VRAM peak is from `nvidia-smi` at 0.5 s.

| arm | ctx | prompt_n | pp tok/s | tg tok/s | mean W | peak W | peak VRAM MiB | J/token |
|---|---|---|---|---|---|---|---|
| B | empty | 513 | **259.16** | — | 129.11 | 164.21 | 7302 | — |
| B | empty | 4 | — | **23.02** | 162.72 | 175.76 | 7302 | **7.43** |
| B | 16801 | 16801 | 260.88 | 18.88 | 142.84 | — | 7302 | — |
| C (scale 1) | empty | 513 | **240.98** | — | 135.92 | 165.34 | 7342 | — |
| C (scale 1) | empty | 4 | — | **22.09** | 160.61 | 178.36 | 7342 | **7.64** |
| C (scale 1) | 16801 | 16801 | 252.38 | 17.92 | 134.83 | — | 7342 | — |

One extra B row at prompt_n 12601 measured 265.93 pp / **5.74** tg tok/s; against 18.88 tg at 16801 the decode figure
is anomalous and is recorded as contended, not as a depth curve. Tenancy: B window loadavg `0.81 0.79 0.72`,
MemAvailable 8,068,068 kB; C window loadavg `1.05 0.83 0.76`, MemAvailable 6,462,784 kB. A second, unrelated
llama.cpp container with GPU access (`optimistic_poincare`) was Up during the window — a real tenancy caveat.

## Evidence

- Load logs: `fork-B-65536.log` (14 lines, ends `listening on http://127.0.0.1:8899`), `fork-C-load.log`,
  `fork-C-full.log`.
- `GET /lora-adapters` returned `[{"id":0,"path":"/lora/bonsai-abliterate-lora.gguf","scale":1.0,…}]`.
- Bench JSONL: `.agi/context/local-maxxing/bench/20260920T141835Z.jsonl` (10 rows: load gate, B/C cost rows,
  adapter-gate row, tenancy row).
- 5 gate completions at B and C scales 0/1/2/3: `.agi/context/local-maxxing/bonsai/abc/` (26 files +
  `PROMPTS.md`).
- Session scratch: `/data/work/agi/.agi/worktrees/a00-944318b2/.agi/sessions/iter-ABC.01/a00-6ce9cb00/`
  (`gate.py`, `gate_scales.py`, `gate2.py`, `bench2.py`, `bench16k.py`, `probs2.py`, armB/C json).

### Restore (required before done)

`docker rm -f fork-bonsai-lora` then `docker start llama-server`; `GET 127.0.0.1:8080/v1/models` = **200** with
models `[Qwen3.5-35B-A3B-Q3_K_M, Qwen3.5-9B-Q4_K_M, bonsai]`, container health `healthy`. The pi-local server is up.

## Verdict / lean

Steps 1, 2 PASS: the 8 GB box serves 27B ternary at 64K fully on GPU, and the abliteration LoRA is genuinely in the
compute graph. Step 4 numbers exist for B and C(1). The owner's coding claim (step 3) is untouched — HumanEval is the
next kid. Lean: **inconclusive_lean_proved:70** — direction positive for the two gates, coding delta unmeasured.

### Falsification notes (measured)

- Load gate NOT falsified: 0 CPU offload, 0 OOM at 65536, so no context deviation is claimed.
- Adapter gate NOT falsified: scale 3 is incoherent (empty), scale 0 == B.
- Partial pending: scales 1/2 == base at the token level means the ladder's "exact projection" is invisible in greedy
  text; this is a result about the LoRA, not a pass/fail of the gate.

## Agent Notes
Steps 1/2/4 only: 27B ternary loads at -c 65536 fully on GPU (n_layer=64, 0 CPU offload, 0 OOM, 7268 MiB); abliteration LoRA IS routed (scale-0 == arm B byte-identical on 5 prompts, scale-3 empty) but scales 1-2 are byte-identical to base at the token level though logprobs move; B pp512 259.2/tg128 23.0 tok/s, 7.43 J/tok, C(1) 241.0/22.1, ~160W. Stock :8080 restored healthy. HumanEval (step 3) not run.
