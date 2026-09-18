---
id: idea:lm-nodes-as-kv-caches
mint_id: 6d6627067bb94e019ead24b41c21c1ff
type: idea
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: 37d5a66da5dee54a
season: 2
title: "Nodes and messages stored as compressed KV caches: prefill once, load the KV instead of re-reading -- a new messaging layer + node storage paradigm on top of arXiv 2510.03215 + KV-cache compression"
town: core
---
<!-- BODY:BEGIN -->
# idea:lm-nodes-as-kv-caches

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
OWNER 2026-09-18 04:0xZ (thought-master pane), verbatim: "Here is another paper. https://arxiv.org/abs/2510.03215 Combine that with kv cache compression like kv turbo or whatever and it can enable massive parallelization and new paradigm of messaging layer and node storage. Nodes stored as kv caches as well for direct ingestion in compressed form for massive info compression savings." RESEARCH ACT: trove-survey ts-nodes-as-kv-messaging-as-kv-massive-parallel launched 04:0xZ on pi (2 readers: the paper; the KV-compression landscape incl. TurboQuant / KIVI / KVQuant / whatever "kv turbo" resolves to + llama.cpp -ctk/-ctv, --slot-save-path, prefix caching; 3 angles: nodes-as-kv, messaging-as-kv, massive-parallel); args at .agi/context/local-maxxing/troves/2026-09-18-kv-nodes/hunt_args.json. KNOWN CONSTRAINT to test first: a KV cache is valid only for the exact model + context layout, so node-as-KV binds the graph to a pinned model per KV set (the markdown stays the truth; the KV is a derived cache keyed by model sha) -- the first $0 measurement on local-town: prefill seconds saved and bytes per node at q4/q8 KV for 20 real nodes, vs re-prefill. SUCCESSOR: read the digests when they land, judge (panel/judge by hand until SM.105), mint the first hypothesis (node-as-KV on the served kid model, bars = bytes/node <= 2x markdown at 4-bit KV, prefill saved >= 80%, byte-identical continuation) and queue it after spec-decode (same endpoint, same slot).

JUDGE (thought-master 04:2xZ): survey ts-nodes-as-kv landed 1 of 2 slices (paper digest 2 pages; kv-compression slice never wrote -- process gone at 04:12Z; the 600 s wall / rotation), digest landed at troves/2026-09-18-kv-nodes/paper-2510-03215.md. First hypothesis minted: hypothesis:lm-kv-slot-save-beats-reprefill (node-as-KV = compute caching not compression; arithmetic on the node: a 1,000-token node = 27-144 MiB of KV vs 4 KB of text; the win is prefill time, measured with the llama.cpp slot save/restore that already ships). Next in this chain after its verdict: prefix caching across -np slots for the shared kid brief (massive parallel), then a C2C fuser between two small served models as the messaging layer. The kv-compression slice (TurboQuant/KIVI/KVQuant + the 4k/32k byte table) re-runs once trove-survey holds its 3600 s wall (after SM.105).

JUDGED BY HAND (thought-master 05:11Z): the kv-compression slice re-ran under setsid (workflow rc=2 at the structured return, every digest complete): 5 digests, 7 pages in troves/2026-09-18-kv-nodes/ (turboquant-2504-19874, kivi-2402-02750, kvquant-2401-18079, llama-cpp-kv, kv-slice-synthesis). WHAT THE OWNER MEANS (MEASURED): TurboQuant = arXiv 2504.19874 (Google, 28 Apr 2025; 3.5 bits neutral / 2.5 marginal; blog says 6x at 3 bits); kv turbo / turbokv = third-party GPU implementations of it, none from Google, no CPU path. LANDSCAPE: KIVI 2-bit (MIT, CUDA), KVQuant nuq2-4 (no licence file, CUDA), TurboQuant (no upstream code) -- NONE runs on ARM4C or in ggml-cpu today; what runs is llama.cpp -ctk/-ctv: q8_0 = 1.0625 B/elem = 1.88x, q4_0 = 0.5625 B/elem = 3.56x (MEASURED block sizes), quantised V requires flash attention (CPU FA exists, untested here). BYTE TABLE (ESTIMATE, formula on the digest): 9B-class 4k = 576 MiB f16 / 306 q8_0 / 162 q4_0, 32k = 4.5 GiB / 2.39 / 1.27; 27B-class 4k = 1.0 GiB / 544 MiB / 288 MiB, 32k = 8.0 GiB / 4.25 / 2.25. FIT: ARM4C runs 9B/32k at q4_0 (1.27 GiB KV + 5-6 GiB weights); 27B never fits ARM4C and 9B/32k barely fits the 8 GB GPU. VERDICT ON THE FRAMING: (a) compression savings = 1.9-3.6x today, 6x only with new ggml code (banked as a research opportunity: per-channel-K 2-bit in ggml-cpu, not minted -- chain no longer than the evidence); (b) node-as-KV is 10,000-37,000x the text bytes and pays only in prefill time: the upstream README example restores 1,745 tokens in 43 ms from an 8.2 KB/token file (MEASURED, unknown hardware) -> hypothesis:lm-kv-slot-save-beats-reprefill measures it on local-town; (c) massive parallel = the prefix cache that already ships (--cache-prompt default on, --cache-reuse N, -np 4 + --kv-unified), caveat MEASURED: logits are not bit-identical across batch sizes; (d) messaging-as-KV needs the same model + cache type on both ends; cross-model = the C2C fuser (paper digest). CHAIN ORDER: kv-slot round -> prefix-cache -np round (mint after the first verdict) -> C2C fuser between two small served models.
