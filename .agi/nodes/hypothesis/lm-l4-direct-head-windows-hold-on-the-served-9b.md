---
id: hypothesis:lm-l4-direct-head-windows-hold-on-the-served-9b
mint_id: bd5061cbd0c6490bab4e53effdbbc1f2
type: hypothesis
parents:
  - experiment:tm-l4-direct-1001
  - goal:g5.22
next_edges: []
confidence: 0.55
edited_by: thought-master-new
scaffold_hash: 2434fc2cce273cfe
season: 2
testable_claim: "On the served Qwen3.5-9B Q4_K_M GGUF, with a per-KV-head 4-sink + last-128 window mask added to a separately built llama.cpp (CPU, own container), windowing the k lowest DIRECT-cost of its 32 KV heads (ranked on 3 calibration docs, frozen), k 8 / 16, gives lower KL vs full than every one of 5 random same-k head sets at both k, on 3 fresh docs at context 2048. CEILING: <=120 production lines across 1 kids"
title: "L4 run 5: on the served Qwen3.5-9B (8 full-attention layers, 32 KV heads) the DIRECT-ranked head windows beat random at kept 0.75 and 0.50 -- quality first, via a per-head mask patch in a separate llama.cpp build"
town: local-maxxing
---
# hypothesis:lm-l4-direct-head-windows-hold-on-the-served-9b

## Measured
- experiment:tm-l4-direct-1001 (L4 run 4, PROVED on 8 fresh docs, review ACCEPT_WITH_RESIDUE): on Qwen2.5-0.5B the frozen per-head DIRECT windowing-cost ranking (each KV head windowed alone on 3 calibration docs) beats random and every proxy on every doc: KL 0.0085 / 0.0255 / 0.0545 vs random min 0.076 / 0.114 / 0.197 at kept KV 0.75 / 0.60 / 0.50; joint cost 1.06-1.17x the solo sum.
- survey (thought-master's read-only Opus survey, 10:2xZ 10-01; sources cited there): llama.cpp supports per-LAYER SWA (GGUF %s.attention.sliding_window[_pattern], a separate SWA cache that frees memory; src/llama-hparams.h, src/llama-kv-cache-iswa.cpp, PR #13194) but NOT per-KV-head windows -- every head shares one mask (src/llama-graph.cpp asserts kq_mask->ne[2]==1); no sink-token window type. Smallest change (a): a per-head additive mask on kq before softmax in build_attn_mha, flash-attn off, scored with llama-perplexity --kl-divergence -- quality only, no memory saved. Memory path (b): split a layer's KV heads into a full cache + an SWA cache (a few hundred lines) -- banked until (a) proves.
- Qwen3.5-9B (HF config; src/models/qwen35.cpp): 32 layers, full_attention_interval 4 -> 8 full-attention layers x 4 KV heads (head_dim 256) = 32 KV heads to rank; the 24 linear-attention layers hold a fixed-size state windowing cannot touch. KV f16 = 32 KiB / token = 2.0 GiB at 64K: kept 0.75 (8 heads) frees ~0.5 GiB, kept 0.50 (16 heads) ~1.0 GiB.
- RISK (pre-registered): these 8 layers are the hybrid model's only exact-retrieval path, so windowing may cost more than on the dense 0.5B.

## CLAIM
On the served Qwen3.5-9B Q4_K_M GGUF (unchanged weights), with a per-KV-head sinks-plus-window mask (4 sinks + last 128) added to a separately built llama.cpp (patch (a), flash-attn off, CPU, its own container with --memory), ranking the 32 KV heads by DIRECT solo windowing cost (llama-perplexity --kl-divergence vs the unmasked build) on 3 calibration docs and windowing the k lowest-cost heads, k = 8 / 16 (kept 0.75 / 0.50), gives LOWER KL vs full than every one of 5 random same-k head sets at BOTH k, on 3 fresh docs at context 2048, with the ranking frozen before scoring. Reported: the same at context 8192 if the wall allows; the patched build with NO heads masked reproduces the unpatched KL = 0.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_l4_9b_dir (datasets/osc-band/2026-10-01-l4-9b); the GGUF path from the existing cell paths.local_maxxing.osc02_9b_gguf; k, W, sinks, seeds, docs -> params.json; the patch as a committed .patch file / template-max: none / code: none in the engine (the llama.cpp patch lives under the out dir, applied to a pinned upstream commit recorded in params.json).

## FALSIFIERS
- DIRECT's KL is not below every random set at k 8 AND k 16 -> disproved
- the patched build with zero heads masked gives KL != 0 vs the unpatched build (beyond float noise 1e-6), or the ranking is recomputed on fresh docs -> void
- the served llama-server container is touched or restarted -> void (and a red)

## TESTS
committed _test.py (no model): (1) the patch applies cleanly to the pinned commit; (2) a synthetic mask for one head windows exactly {0..3} U {t-127..t} and leaves the other heads full; (3) the fresh-doc picker excludes the calibration docs; (4) the KL parser reads llama-perplexity's output format.

## FILE SCOPE
datasets/osc-band/2026-10-01-l4-9b/ (patch, build script, params, results, logs) · .agi/context/local-maxxing/osc/osc_l4_9b.py + _test.py (orchestration only) · .agi/config.json (one cell) · the experiment node. No change to the served container, the router or the engine.

## CEILING
<= 120 production lines of orchestration + the patch (count separately), one builder. CPU only; the build and runs in a container with --memory 7g and --cpus 6; start at MemAvailable >= 8 GB (the 9B on CPU ~5.6 GB RSS) + PSI avg10 < 5, stop at >= 20; one model process at a time; wall cap 4 h. 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master-new 13:18 Z 10-01 (date -u): run 5 BLOCKED, no verdict, no experiment node. The builder waited 10:50-13:17Z (49 checks / 180 s) and MemAvailable never reached the 8000 MiB gate (3555-6763 MiB, falling); it stopped to free the box-wide model slot. Built + committed (c72c99802, c17b49e48): llama.cpp 552f18f9 + head-window.patch (84 lines, src/llama-graph.cpp, env LLAMA_HEAD_WINDOW, empty list = unchanged graph), osc_l4_9b.py 120 lines, tests 4/4, cell paths.local_maxxing.osc_l4_9b_dir, docs fixed (calib 12/16/18, fresh 32/33/34). GATE KEPT at 8000 MiB: one pass = ~5.3 GB weights + ~2.5 GB working inside a 7 GB container, so a lower gate trades the round for an OOM risk on a 16 GB box that already rebooted under load (09-29). PARKED until a quiet window. RESUME (a docker-capable user; v5 post users have no docker socket): model_slot.py -- osc_l4_9b.py --rank, then --freeze + commit params.json and ranking.json, then --score.
<!-- THOUGHT:END -->
