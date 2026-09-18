# prismml — Ternary Bonsai 2 27B
source key: prismml | stage: owner-links slice | started 2026-09-17

## p1 — X post @PrismML, id 2100692248480596348
URL: https://x.com/PrismML/status/2100692248480596348
read via https://api.fxtwitter.com/prismml/status/2100692248480596348 (2026-09-17)
MEASURED (quoted, tweet.text verbatim):
  "Today, we're announcing Ternary Bonsai 2 27B.
   Based on Qwen3.8 27B, Bonsai 2 27B is 9x smaller than its full-precision
   counterpart while retaining 98.2% of its aggregate benchmark performance.
   Two months after the first Bonsai 27B release, the biggest change is quality.
   The footprint remains 5.9 GB, but the gap to full precision has narrowed
   materially, with particularly strong gains in agentic coding, multimodal
   reasoning, and long-horizon tool use.
   Ternary Bonsai 2 27B is available today under Apache 2.0."
MEASURED metadata: created_at Thu Sep 17 21:03:55 +0000 2026 (YESTERDAY);
  views 972,974; likes 5,952; replies 245; retweets 631; quotes 257; is_note_tweet true.
MEASURED: post carries NO outbound link facet. Only media: 1 photo
  https://pbs.twimg.com/media/HScnLImaoAAJjz0.jpg?name=orig (1815x866) — that
  image is the benchmark table (read separately, p2).
MEASURED author: PrismML, verified org, 19,488 followers, joined 2025-03-28,
  bio "Centering AI research on efficiency." website https://prismml.com/
NOTE: no paper/HF/GitHub URL in the post itself -> must be found on prismml.com
  or HF org search. Follow-up: p3..p6.

## p2 — prismml.com (product site)
URL: https://prismml.com/  MEASURED (read 2026-09-17, HTTP 200, 81,233 bytes)
MEASURED (quoted): "Bonsai 2 27B — 9x less memory, 8x faster, 5x less energy"
MEASURED (quoted): "Ternary Bonsai 2 27B is our most capable model yet, delivering
  98.2% performance retention of its full-precision counterpart at a 9x smaller
  footprint. At just 5.9 GB ... Built on Qwen3.8 27B"
MEASURED (quoted): "Intelligence density = Negative log of the model's error rate
  divided by the model size" — their headline metric, cites a whitepaper.
MEASURED (quoted): "Utilizing breakthrough research at Caltech"
MEASURED links harvested:
  whitepaper PDF: https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-27b-whitepaper.pdf
  HF org: https://huggingface.co/prism-ml/  collections: /collections/prism-ml/bonsai-2 , /bonsai-27b
  HF models seen on site: Ternary-Bonsai-1.7B-gguf, Ternary-Bonsai-4B-gguf,
    Ternary-Bonsai-8B-gguf, Bonsai-1.7B/4B/8B-gguf (1-bit), bonsai-image-*-mlx
  demo spaces: https://huggingface.co/spaces/webml-community/ternary-bonsai-2-webgpu-kernels
  docs: https://docs.prismml.com/   iOS app: Bonsai Studio (App Store id6767042620)
  NOTE: no Ternary-Bonsai-27B-gguf link on the homepage model list — the 27B
  artifact is NOT on the front page; hunt on HF + docs (p3, p4).

## p3 — WHITEPAPER "Ternary Bonsai 2 27B", PrismML, September 2026 (the source artifact)
URL: https://github.com/PrismML-Eng/Bonsai-demo/blob/main/bonsai-2-27b-whitepaper.pdf
raw: https://raw.githubusercontent.com/PrismML-Eng/Bonsai-demo/main/bonsai-2-27b-whitepaper.pdf
MEASURED (read 2026-09-17; HTTP 200; 366,237 bytes; PDF v1.5; 14 pages; pdftotext 711 lines)
Headline (MEASURED, quoted): "~9.1x smaller | 98.2% intelligence retained | 46.8 tok/s on laptop"
MEASURED spec table 1: based on Qwen3.8-27B [HF Qwen/Qwen3.8-27B], hybrid attention
  ~75% linear-attention / ~25% full attention, SwiGLU, RoPE, RMSNorm; context 262,144 tok;
  params 24.35B language (64 blocks) + 0.47B vision tower (27 blocks) + 2.54B embed/lm-head
  = 27.36B total; weight format "Ternary g128 (FP16 group-wise scaling)";
  weights in {-1,0,+1} in a FIXED blockwise Hadamard-rotated basis (block 1024, fixed +-1 signs,
  R = H_n S / sqrt(n)); 0.0976% of params (26.2M, 52MB bf16) kept full precision
  (recurrent-state path of linear-attention layers + norms); backends MLX (Python, Swift) and
  CUDA; License: Apache License. Reasoning efforts: xhigh or medium ("Low does not reduce thinking").
MEASURED bits/weight: true ternary 1.72 bpw = 5.80 GB (9.3x smaller than FP16 53.80 GB);
  PTQ1_0 (packed ternary) 1.76 bpw = 5.93 GB (9.1x); PQ2_0 2-bit 2.16 bpw = 7.25 GB (7.4x).
  MLX package = 8.49 GB (2.250 bpw; MLX block stores redundant FP16 bias).
  Vision tower separate: mmproj HQQ 4-bit 0.63 GB (Q8_0 container), mmproj BF16 0.93 GB.
  Advertised 5.9 GB = PTQ1_0 language model only, text-only.
MEASURED quality: averages 83.9 on a 20-benchmark suite vs 85.4 for Qwen3.8-27B FP16
  (= 98.2% retention) and 83.6 for Qwen3.6-27B. Suite spans reasoning/math/coding/IF/tool-calling/vision.
  Math block (Table 8-ish): AIME26 97.06?/AIME25/GSM8K 96.66, MATH-500 ... (see p3b).
MEASURED THROUGHPUT Table 5 (tg128 tok/s | pp512 tok/s | mWh/tok), measured 2026-09-16, batch 1, depth 0, vision excluded:
  PQ2_0: RTX 5090 142.5|4121|0.582 ; RTX PRO 6000 Blackwell 140.6|4520|0.637 ; H200 SXM 118.0|2818|0.708 ;
    B200 117.1|3112|0.830 ; H100 NVL 106.4|2484|0.541 ; H100 SXM 103.2|2467|0.584 ;
    RTX 4090 90.9|3134|0.714 ; RTX 6000 Ada 84.8|2430|0.731 ; L40S 74.6|2827|0.812 ;
    A100 SXM 74.0|1328|0.776 ; L4 (24GB,72W) 29.7|778|0.629 ; Laptop M5 Pro Metal 27.7|397|n/a
  PTQ1_0: 5090 134.4|1901 ; H100 NVL 81.6 ; A100 54.6|703 ; L4 32.1|468 ; M5 Pro 27.1|369
  M5 Max (Table 6) 46.8 tok/s decode | 765 pp512 ; M4 Pro 18.0 | 125
  >>> CRITICAL FOR US: **NO CPU ROW AT ALL.** Every number is Metal or CUDA.
  The 46.8 tok/s headline is an M5 Max laptop GPU. Cheapest measured hardware = L4 24GB @ 29.7 tok/s.
  M5 Pro decode 27.7 tok/s at ~201 GB/s weight traffic -> decode is memory-bandwidth bound:
  tok/s ~= RAM_bandwidth / 5.93 GB. That relation is the ONLY way to estimate our A1 CPU.
MEASURED limitations/roadmap (Sec 5): native low-bit kernels still improving; "KV compression
  (sub-4-bit)" named as future work; decode latency = most direct remaining lever.
MEASURED energy: prefill 0.012-0.060 mWh/tok; idle floors stated, not subtracted.
MEASURED refs of note: SpinQuant (rotations, arXiv:2405.16406), HQQ, llama.cpp, EvalScope.
MEASURED (honesty check): the whitepaper reports PTQ1_0 slower than PQ2_0 on H100/A100
  (unpack cost > traffic saved) — packing choice is hardware-dependent, not a free win.

## p4 — HF model card + file manifest, prism-ml/Ternary-Bonsai-2-27B-gguf
URL: https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf  (README.md read 2026-09-17, 22,785 bytes)
MEASURED: license apache-2.0; library_name llama.cpp; base_model Qwen/Qwen3.8-27B; gated False;
  likes 241, downloads 0 (published 2026-09-17T18:44Z — hours old).
MEASURED files+sizes (HF API blobs=true):
  Ternary-Bonsai-2-27B-F16.gguf 53,808.4 MB ; PTQ1_0 5,946.6 MB ; PQ2_0 7,206.2 MB ;
  mmproj-BF16 931.1 MB ; mmproj-Q8_0 629.2 MB ; LICENSE ; NOTICE.txt
MEASURED (quoted, THE DECISIVE LINE): "Full 27B-class reasoning in ternary transformer
  weights, for llama.cpp (CUDA, Metal, CPU)" — CPU is named in the card, but:
MEASURED (quoted): "The ternary hybrid-attention kernels live in the PrismML-Eng/llama.cpp fork.
  **Stock llama.cpp will not run these files.** It rejects PQ2_0 and PTQ1_0 as unknown types,
  and it loads Q2_0 without any warning and produces garbage, because it has no Hadamard
  activation runtime. Use a binary from the fork."
MEASURED (quoted): "This is a reasoning model and it thinks by default."
MEASURED (quoted, 14-bench thinking avg): FP16 86.32 (100%) | UD-Q4_K_XL 5.2bpw/17.6GB 85.18 (98.7%)
  | IQ2_XXS 2.8bpw/9.4GB 72.59 (84.1%) | Bonsai 2 27B 1.72bpw/5.9GB 84.78 (98.2%)
MEASURED per-benchmark highlights: LiveCodeBench 90.07 (IQ2_XXS 56.40), AIME26 95.83 (57.50),
  AIME25 95.00, MATH-500 98.80, GSM8K 96.66, HumanEval+ 95.12, IFBench 74.00, BFCL v3 74.92,
  MMMU-Pro 75.49, OCRBench v2 56.88 (FP16 60.99 — vision is the weak spot).
MEASURED (quoted): "Intelligence density D = -log2(1 - score/100) / size_GB";
  Bonsai2 0.469 vs IQ2_XXS 0.199 vs FP16 0.053 — their framing metric.
MEASURED (quoted, the anti-hype datum): "PTQ1_0 moves 17% less weight data per step, but
  unpacking dense trits costs arithmetic ... loses on H100, A100, and the Blackwell cards,
  where batch-1 decode is limited by instruction throughput and launch overhead instead."
  => low-bit wins only where memory bandwidth is the binding constraint. An A1 CPU is
  bandwidth-bound, so the bet is plausible there — but see p6: nobody measured it.
MEASURED (quoted): "This laptop swings ~4% with background load" (M5 Pro).
MEASURED sibling manifests (HF API, same read):
  Ternary-Bonsai-1.7B-gguf: PQ2_0 463.3 MB | Q2_0 463.3 MB | Q2_0_g64 490.2 MB | F16 3,446.2 MB
    (46 GB-class = 1.7B; **this is the $0 KID-tier candidate size**)
  Ternary-Bonsai-4B-gguf: PQ2_0 1,075.0 MB ; Ternary-Bonsai-8B-gguf: PQ2_0 2,182.2 MB
  NOTE: 1.7B/4B/8B ternary packs are from the JUNE release (lastModified 2026-06-10) and
  ship Q2_0 *and* PQ2_0; only the new 27B ships PTQ1_0.

## p5 — PrismML-Eng/llama.cpp fork releases (what we could actually run, $0)
URL: https://api.github.com/repos/PrismML-Eng/llama.cpp/releases (read 2026-09-17)
MEASURED tag prism-b10687-5d80cff published 2026-09-17T17:42Z (same day as the model);
  previous prism-b10685-7dffb15 2026-09-15T09:34Z, prism-b10684 2026-09-15T06:04Z
MEASURED assets on prism-b10685 (the full set): includes
  **llama-prism-b10685-7dffb15-bin-ubuntu-arm64.tar.gz — 13.7 MB, dl=14**
  (=> a PREBUILT CPU-ONLY LINUX/ARM64 binary exists; this is our A1's exact platform)
  also ubuntu-x64 17.1 MB, win-cpu-arm64 12.3 MB, macos-arm64 11.7 MB, android-arm64 92.7 MB,
  ubuntu-vulkan-arm64 28.0 MB, ubuntu-rocm, win-cuda, linux-cuda-12.4/12.8/13.3, xcframework.
  NOTE: on the newest tag (b10687) only the three cudart windows zips are attached — the
  linux/arm64 CPU tarball is NOT on the latest tag. Pin b10685 (or wait for re-upload).
MEASURED (fork tree, GitHub trees API, 3,890 paths): ternary kernels live in
  ggml/src/ggml-cuda/template-instances/mmq-instance-{pq2_0,ptq1_0,q2_0}.cu,
  ggml/src/ggml-vulkan/vulkan-shaders/{dequant,ptq1_0,mul_mat_vec_tq2_0}.{comp,glsl},
  tests/test-ptq1_0-{cuda-dot,element-map}.cpp
  => named ternary files are GPU-side only; CPU support is in ggml-cpu/quants.c|traits.cpp
     (no filename-level evidence either way — must be read at source level or measured).

## p6 — Bonsai-demo README (the fork's own "source of truth")
URL: https://github.com/PrismML-Eng/Bonsai-demo/blob/main/README.md (raw read 2026-09-17, 33,856 bytes)
MEASURED (quoted): "you can run Bonsai 2, Bonsai (1-bit) and Ternary-Bonsai language models
  locally on Mac (Metal), Linux/Windows (CUDA, Vulkan, ROCm), **or CPU**."
MEASURED (quoted): "**Q1_0 (1-bit) is fully merged upstream**, and **Q2_0 (ternary) now runs on
  mainline CPU, Metal, Vulkan, and CUDA**."
MEASURED (quoted, the CPU gap for Bonsai 2 27B): upstream-status table has exactly ONE row:
  "FWHT with F16 input (CPU) | ⏳ Open | ggml-org/llama.cpp#27779"
  => the 27B ternary CPU path is *not yet upstream*; the fork binary is required.
MEASURED (quoted): "Ternary support has landed in mainline llama.cpp for CPU, Metal, Vulkan and
  CUDA, so the group-64 Q2_0 files run on a stock build with no fork needed."
  => **1.7B / 4B / 8B ternary g64 run on stock llama.cpp CPU today.** This is the $0 door.
MEASURED format facts: PQ2_0 = group 128, 2.13 bpw, "smallest file and usually fastest where the
  backend is optimized (CUDA, Metal, CPU, ROCm)"; Q2_0 g64 = official upstream format, 2.25 bpw,
  widest coverage. Legacy `*-Q2_0.gguf` (no g64) is deprecated and refused by prism-b10658+.
MEASURED: CPU-only build scripts exist and work on arm64: scripts/build_cpu_linux.sh ->
  "Builds a CPU-only binary with no GPU dependencies. Works on both x64 and arm64. Outputs to bin/cpu/"
MEASURED: `BONSAI_NGL=0` = CPU-only inference; `BONSAI_MMPROJ_CPU=1` keeps vision projector in RAM.
MEASURED: speculative decoding exists (DSpark drafter ~0.6 GB sidecar, BONSAI_SPECULATIVE=1).

## p7 — community-benchmarks/ternary-bonsai/README.md (16 published rows)
URL: https://github.com/PrismML-Eng/Bonsai-demo/blob/main/community-benchmarks/ternary-bonsai/README.md
MEASURED (read 2026-09-17): 15 rows for 27B, 3 for 8B. Hardware = RTX PRO 6000 129.9 tg/s,
  L40S 74.3, RTX 4070 Ti SUPER 69.6, A5000 48.2, M5 Max 45.8, RTX 5060 Ti 44.4, M5 Pro MLX 29.5,
  DGX Spark GB10 29.2, M5 Pro Metal 26.5, M4 Pro MLX 24.8, GTX 1080 Ti 20.5, M4 Pro Metal 19.0,
  M1 Pro MLX 15.0, M4 MLX 12.7, M3 Pro 12.6. 8B: RTX 4070 Ti SUPER 215.7 tg/s, GTX 1080 Ti 68.8,
  M3 Pro Metal 51.3.
  >>> **ZERO CPU ROWS.** The submission template explicitly invites "CPU (ARM) | cpu-m4-pro-macos.md"
  and "CPU (x86) | cpu-i9-14900k-linux.md" but nobody has submitted one.
  => an A1 ARM64 CPU tg128 number would be the FIRST published CPU datapoint for this family.
MEASURED: template file TERNARY-TEMPLATE-llama-cpp.md is 404 at main (renamed since the README
  was written) — README is slightly stale; treat its links as approximate.

## p8 — KID-tier candidates (the small ternary models) + THIS BOX's constraints
MEASURED (HF raw .eval_results/gsm8k.yaml, read 2026-09-17):
  Ternary-Bonsai-1.7B: gsm8k 74.2   (caveat: the file's own `source.url` says Bonsai-8B-gguf —
    a copy-paste artifact in their repo; treat the 1.7B number as MEASURED-but-mislabeled)
  Ternary-Bonsai-8B:   gsm8k 91
MEASURED file sizes for the $0 KID tier: 1.7B PQ2_0 463.3 MB / Q2_0_g64 490.2 MB ;
  4B PQ2_0 1,075.0 MB ; 8B PQ2_0 2,182.2 MB ; 27B PTQ1_0 5,946.6 MB / PQ2_0 7,206.2 MB
MEASURED local box (read-only probes, 2026-09-17):
  cpu: 4x aarch64, Features include fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp
    asimdhp asimdrdm lrcpc dcpop asimddp  -> NEON + dotprod + FP16 arithmetic; **no i8mm, no SVE**
  mem: total 23 GB, available 16 GB ; **disk: / 77G with only 6.2 GB free (92% used)**
  tooling: no llama-cli / llama-server / ollama / ~/llama.cpp on PATH or in $HOME
  => the 27B PTQ1_0 (5.95 GB) does NOT fit our disk without freeing space; 8B (2.2 GB) and
     1.7B (0.46 GB) do. Disk is a harder wall here than RAM.
ESTIMATE (method stated, not measured): M5 Pro measured 28.1 tg/s at ~204 GB/s weight traffic,
  so tok/s ~= BW_effective / model_GB. arm-cloud 4-core: BW_effective ESTIMATE 15-40 GB/s
  (no A1 STREAM number read; flagged as the one number to measure first).
  => 27B: 2.5-6.7 tg/s ESTIMATE | 8B: 7-18 tg/s ESTIMATE | 1.7B: 32-86 tg/s ESTIMATE
  Decode-only reasoning: a reasoning model spends 5-50x more tokens than the visible answer,
  so wall-clock per KID task at 8B = tens of seconds to minutes. ESTIMATE.
