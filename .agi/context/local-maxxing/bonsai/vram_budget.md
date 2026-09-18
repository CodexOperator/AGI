# VRAM budget — Ternary-Bonsai-2-27B PTQ1_0 on GPU2070S (7786 MiB usable)

Derived from the model's own GGUF header (first 16 MiB range-fetched, not the whole
5.95 GB), 2026-09-18. Header parse: `gguf_meta.py` output in the node's evidence.
**This is arithmetic on measured header fields, not a load test** — no 27B bytes
have been on the card yet. It bounds the falsifier "the PTQ1_0 does not load fully
in 8 GB".

## The architecture is why it fits

`general.architecture = qwen35`, `block_count = 64`, `full_attention_interval = 4`.
Only **16 of 64 layers carry a growing KV cache**; the other 48 are SSM/linear
layers with constant-size state (`ssm.state_size 128`, `group_count 16`,
`conv_kernel 4`, `inner_size 6144` -> ~5 MiB total, not per token).

| field | value |
|---|---|
| head_count / head_count_kv | 24 / 4 (GQA) |
| key_length / value_length | 256 / 256 |
| KV bytes/token (f16) | 16 layers x 4 kvheads x (256+256) x 2 B = **65,536 B** |

## Budget (f16 KV)

| ctx | KV MiB | weights MiB | sum MiB | headroom MiB |
|---:|---:|---:|---:|---:|
| 4096 | 256.0 | 5671.2 | 5927.2 | 1858.8 |
| **8192** | **512.0** | **5671.2** | **6183.2** | **1602.8** |
| 16384 | 1024.0 | 5671.2 | 6695.2 | 1090.8 |
| 32768 | 2048.0 | 5671.2 | 7719.2 | 66.8 |

At the hypothesis's `-c 8192` the weights+KV sum is 6183 MiB, leaving ~1.6 GiB for
the CUDA context and compute buffer — the margin the 9B (5672 MiB weights, 5568 MiB
observed peak) never needed. At `-c 32768` it is 67 MiB of headroom, i.e. expect an
OOM: **8192 is the right context for this card, not a conservative one.**

Raw: `probe.jsonl` rows `gguf_header_27b_ptq1_0` / `belam_hf_egress_*`.
