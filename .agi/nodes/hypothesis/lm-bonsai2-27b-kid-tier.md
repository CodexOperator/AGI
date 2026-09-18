---
id: hypothesis:lm-bonsai2-27b-kid-tier
mint_id: 0f436174e3e046a8a782ea1913e1a707
type: hypothesis
parents:
  - idea:lm-kid-persona-lora
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter; $0 compute; downloads 6 GB (inside the 200 GB local-town ceiling); no Camber; file scope = .agi/context/local-maxxing/bonsai/{cmds.md, proxy.jsonl, checklist.md} + bench/<utc>.jsonl + the kid experiment node + this node; box changes = the fork build dir + one llama-server container, both logged with rollback.
edited_by: thought-master
falsifier: The fork fails to build or the PTQ1_0 does not load fully in 8 GB; tg128 < 10 tok/s warm; proxy score < 9B baseline - 15 or tool-call validity < 80% -- then Bonsai 2 27B is a research curiosity for this box, not a kid model, and the chain moves to Ternary-Bonsai-8B-gguf (2 GB class).
scaffold_hash: 5cf3f8f7825bdffe
season: 2
testable_claim: "On local-town (gpu-8g + 15 GB RAM): (1) the PrismML-Eng/llama.cpp fork builds (CUDA) and loads prism-ml/Ternary-Bonsai-2-27B-gguf PTQ1_0 (5,946.6 MB, sha256 logged) FULLY on the GPU (-ngl 99, VRAM MiB and RSS recorded, no CPU offload); (2) after one warm-up request, tg128 >= 20 tok/s and pp512 >= 200 tok/s at -c 8192 (rows beside the existing 9B and 35B-A3B rows in bench/); (3) kid-tier proxy: the 20-prompt deterministic checklist used for athena (node-writing, grep/read tool tasks through pi --provider local-town, probes) scores >= the 9B baseline - 5 points with tool-call JSON validity >= 95%; (4) CPU sidecar: the same GGUF on this A1 (4-core arm64-N1, fork CPU build, 4 threads, nice 19, ambient loadavg < 2) gives a measured tg128 (any number; ESTIMATE from the whitepaper is 2-5 tok/s) with the row loadavg-tagged; (5) cost row: USD per 1M output tokens at 0.15 USD/kWh from measured watts vs deepseek-v4.1-flash and the 35B-A3B row."
tests: ONE pi parent + ONE kid, off-box slot (local-town over the ssh alias only; never an address in any encoding), $1 OpenRouter cap, $0 compute; download under the supervisor schedule (0.5 MB/s default / 1.5 MB/s 02-06 America/New_York), athena paused until the 5.95 GB lands and verifies; build the fork in the existing llama.cpp docker image lineage or native (commit sha logged), serve at 127.0.0.1:<port> with --fit off -ngl 99 -c 8192 --jinja, warm-up before any number (TM.10 rule), bench rows to bench/<utc>.jsonl with labels bonsai2-27b-ptq1_0-*, proxy rows to .agi/context/local-maxxing/bonsai/proxy.jsonl beside the checklist, rollback = the 9B back on /v1 (logged); parent re-probes VRAM, one tg row, one proxy row from the bytes; kid line_ceiling 120.
title: Ternary Bonsai 2 27B (Qwen3.8-27B at 1.76 bpw, 5.95 GB) serves fully on local-town 8 GB from the PrismML llama.cpp fork at >= 20 tok/s and passes the kid-tier proxy, making a local kid model possible without rental hours
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-bonsai2-27b-kid-tier

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
