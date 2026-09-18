---
id: hypothesis:lm-kv-slot-save-beats-reprefill
mint_id: 80a14e3a899a4f159e02f6fafdbda843
type: hypothesis
parents:
  - idea:lm-nodes-as-kv-caches
  - goal:g14
next_edges: []
ceiling: $0.50 OpenRouter; $0 compute; 0 downloads; <= 2 GB of slot files, deleted after; file scope = .agi/context/local-maxxing/kvslot/{cmds.md, rows.jsonl} + bench/<utc>.jsonl + the kid experiment node + this node.
edited_by: thought-master
falsifier: Restore not faster than re-prefill by 3x on the median node (read-bound), or q8_0 restore diverges from the f16 greedy continuation on any node, or file bytes miss the arithmetic by > 10% -- then node-as-KV storage is not a paradigm for this box and the chain narrows to prefix caching across -np slots (shared brief prefix, no files) and to C2C fuser training as the messaging layer.
scaffold_hash: d8e71e6402831d9d
season: 2
testable_claim: "On local-town (llama-server, the served 9B, -ngl 99, -t 16, --slot-save-path <dir>, -np 2): for 10 committed nodes of 500-2,000 tokens each, (1) POST /slots/<id>?action=save after a prefill writes a file whose bytes/token match the arithmetic within 10% (f16 KV per token = 2 x n_layer x n_kv_head x head_dim x 2 B, the served model config.json values written into the row; q8_0 -ctk/-ctv = x 8.5/16; q4_0 = x 4.5/16); (2) ?action=restore plus one generated token completes in <= 1/3 of the wall-clock of re-prefilling the same node (cold, 3 reps, warm-up first); (3) greedy continuation (temp 0, 64 tokens) after restore is byte-identical to the re-prefilled continuation at f16 and at q8_0, and the divergence at q4_0 is reported per node; (4) the ratio KV bytes / UTF-8 text bytes is reported per node per cache type. ARITHMETIC (ESTIMATE, public GQA configs -- verify from config.json): Qwen3-8B-class (36 layers, 8 KV heads, head_dim 128) = 147,456 B/token f16 -> a 1,000-token node = 144 MiB f16 / 76.5 MiB q8_0 / 40.5 MiB q4_0 / ~27 MiB at a TurboQuant-class 3 bpe, against ~4 KB of UTF-8 text = 37,000x / 20,000x / 10,000x / 7,000x; a 4k context = 576 MiB f16, 32k = 4.5 GiB; Gemma-3-27B-class (62 layers, 16 KV heads, 128) = 496 KiB/token -> 4k = 1.94 GiB, 32k = 15.5 GiB f16; Qwen3-32B-class (64 layers, 8 KV heads) = 256 KiB/token -> 4k = 1 GiB, 32k = 8 GiB. What a saved KV buys is PREFILL time (1,000 tokens at pp 300-1,000 tok/s = 1-3 s) against a 40-80 MiB read (NVMe 0.05-0.2 s; 1 Gbit LAN 0.4-0.7 s) -- it pays only when the same node is ingested repeatedly by the SAME model and cache type (a KV is never portable across models or quants; cross-model is the C2C fuser, a separate hypothesis)."
tests: ONE pi parent + ONE kid, off-box slot (local-town over the ssh alias only, never an address in any encoding), after the Bonsai round frees the slot; $0.50 OpenRouter cap, $0 compute, 0 downloads; rows to bench/<utc>.jsonl labelled kvslot-* (node id, tokens, text bytes, KV bytes per cache type, save/restore/prefill ms, identical yes/no); slot files deleted after the run; rollback = rm the slot dir, the server back on /v1 as it was; kid line_ceiling 120.
title: "A graph node stored as a saved llama.cpp KV slot restores >= 3x faster than re-prefilling it but costs 7,000-37,000x the node text bytes on disk: node-as-KV is compute caching, not compression -- measured on local-town with the served 9B, $0"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-kv-slot-save-beats-reprefill

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 04:0xZ (thought-master pane), verbatim: "Here is another paper. https://arxiv.org/abs/2510.03215 Combine that with kv cache compression like kv turbo or whatever and it can enable massive parallelization and new paradigm of messaging layer and node storage. Nodes stored as kv caches as well for direct ingestion in compressed form for massive info compression savings." JUDGE (thought-master 04:2xZ, by hand -- the pi survey ts-nodes-as-kv landed 1 of 2 slices: paper-2510-03215.md 2 pages MEASURED, the kv-compression slice never wrote, process gone at 04:12Z): arXiv 2510.03215 = Cache-to-Cache (C2C), ICLR 2026, code thu-nics/C2C -- a trained 3-layer MLP fuser + per-layer gate projects the sharer KV into the receiver KV, both LLMs frozen: +11.0% avg accuracy over individual models, ~2.5x latency vs text communication (MEASURED in the digest). It needs a trained fuser PER (sharer, receiver) pair, so the messaging layer is a training job per model pair (small pairs train on 8 GB; a 27B pair does not) and it does NOT make a KV portable across models. The owner framing (nodes stored as KV for compression savings) inverts at the byte level -- a KV is 4 orders of magnitude larger than its text -- and holds at the compute level (prefill saved); this node measures exactly that with the slot save/restore llama.cpp already ships, and the C2C fuser gets its own hypothesis after this verdict.
