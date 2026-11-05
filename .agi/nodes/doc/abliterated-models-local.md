---
id: doc:abliterated-models-local
mint_id: 6dd15380198d4490a1ee8281bba8eccc
type: doc
parents:
  - goal:g5.34
next_edges: []
edited_by: director-general-1
season: 3
tags: []
title: Abliterated models on this box
town: local-maxxing
---
# doc:abliterated-models-local — what sits in /data/work/models (goal:g5.34)

Storage only: this box has 7 GB RAM, 4 cores and no GPU, so nothing here is loaded or served. The weights live on the /data mount, never in the repo, a worktree or the graph; `/data/work/models/SHA256SUMS` (36 lines) is the checksum list. Fetched 2026-10-22 from Hugging Face direct (public, no token, no torrent needed), one file at a time at 20-40 MB/s. Every LFS file's sha256 equals the Hugging Face LFS oid; the small git files (config, tokenizer json, README, LICENSE) are recorded from the downloaded bytes.

| artifact | repo @ revision | license | bytes | sha256 (LFS oid) | runtime |
|---|---|---|---|---|---|
| DeepSeek-V4-Flash-Q2_K-0731.gguf (+ README.md, .gitattributes) | huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF @ a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4 | MIT | 97591747456 | 4a459b2ceb34... (full line in SHA256SUMS) | latest llama.cpp, or antirez/ds4 branch ds4f-mxfp4 (`./ds4 -m ...Q2_K-0731.gguf --ctx 32768`); the repo README says all expert modules were not ablated |
| Huihui-Qwen3.8-27B-abliterated (18 x model-*.safetensors + index, config, tokenizer, vocab, merges, chat_template, LICENSE, README) | huihui-ai/Huihui-Qwen3.8-27B-abliterated @ 739e3c5b89849f6c238ce1e5b70008612ae42cdd | Apache-2.0 | 55586059962 (31 files) | 18 weight lines + tokenizer.json in SHA256SUMS | transformers (Qwen3_5ForConditionalGeneration, model_type qwen3_5); ollama via huihui_ai/Qwen3.8-abliterated |
| Huihui-Qwen3.8-27B-abliterated-Q4_K.gguf | huihui-ai/Huihui-Qwen3.8-27B-abliterated-GGUF @ 1c69098e9c32db6dc06fc48f1d6cc75ad07da89e | Apache-2.0 | 16810714400 | 6c2c13cef89238c3604d756b07b3ef5fafebbd61095feb8553ff449c95e4c1c6 | latest llama.cpp or ollama |

Picks and why: the DeepSeek build is the 0731 sibling's Q2_K (97.59 GB), smaller than the ds4 repo's Q2_K (99.71 GB) and inside the goal's 105 GB bound. The Q4 is huihui-ai's own plain Q4_K; the alternative was UD-DW-Q4_K_M (16.55 GB).

## Falsifier read 2026-10-22
1. `cd /data/work/models && sha256sum -c SHA256SUMS`: 36 lines, 0 not-OK; `df /data` 66% used, 119782200 KiB free (floor: 80% used).
2. `git ls-files | grep -ciE '\.(gguf|safetensors)$'` = 0 in ~/t; `find` over the root-fs paths outside /var/lib/agi (/tmp /home /root /opt /srv /var/tmp /usr/local /var/cache, -xdev) = 0 hits. (A `find / -xdev` was not run: it would walk /var/lib/agi, the dentry-slab trap in skill agi-memory-guard.)

## Not fetched (banked to the owner, goal:g5.34 out of scope)
DeepSeek-V4.1-Flash abliterated at the smallest general size (~271 GB) and any full-size DeepSeek (~510 GB+): over this box's budget. Qwen 4 abliterated: not out yet in the sources read. Qwen3.8-Max (2.4 TB): out. The 0731 repo also lists a Q4_K (164 GB) and mxfp4 (156 GB): over the floor.
