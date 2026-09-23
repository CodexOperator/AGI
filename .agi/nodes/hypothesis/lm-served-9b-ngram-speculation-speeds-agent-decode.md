---
id: hypothesis:lm-served-9b-ngram-speculation-speeds-agent-decode
mint_id: 9c039075afa74da88fe66df1ea602f94
type: hypothesis
parents:
  - goal:g5.22
  - hypothesis:lm-spec-decode-cpu-draft-hybrid
next_edges: []
edited_by: director-thought
scaffold_hash: 10c881bcc447b986
season: 2
testable_claim: "On the served Qwen3.5-9B-Q4_K_M with the router's own image (server-cuda, build 10991) and its model_args_9b, at least one draft-free speculative type among ngram-simple / ngram-map-k / ngram-map-k4v / ngram-mod / ngram-cache raises the median per-request decode tok/s over --spec-type none by >= 1.3x on >= 20 agent-shaped requests built from committed repo files (edit-and-return, code, digest), the paired 95 pct interval of the per-request speedup clearing 1.0, with greedy outputs identical to the none arm on every request (or each divergence explained by a top-2 margin < 0.1 at the divergence point in the none arm) and prompt tok/s within 5 pct of none. CEILING: <=120 production lines."
title: "TRACK I ladder L9/L10 first rung (speculation, draft-free): on the served 9B the router build's n-gram speculation decodes agent-shaped requests >= 1.3x faster at unchanged greedy outputs -- and whether speculation runs at all on the hybrid qwen35 (24 DeltaNet + 8 attention blocks)"
town: local-maxxing
---
# hypothesis:lm-served-9b-ngram-speculation-speeds-agent-decode

# hypothesis:lm-served-9b-ngram-speculation-speeds-agent-decode

## Measured
- the router's build offers draft-free speculation: llama-server --help in ghcr.io/ggml-org/llama.cpp:server-cuda (build 10991, commit 930e2fa59)
  lists --spec-type none,draft-simple,draft-eagle3,draft-mtp,draft-dflash,draft-dspark,ngram-simple,ngram-map-k,ngram-map-k4v,ngram-mod,ngram-cache
  (director-thought 09-23 20:2xZ, docker run --rm, the router untouched); defaults: ngram-simple n 12 / m 48, ngram-mod n-min 48 / n-max 64 / match 24.
- the served GGUF carries NO multi-token-prediction head: 427 tensors, blk.0-31, zero nextn / mtp tensors (director-thought header read, same
  hour) -> draft-mtp is unusable with this file. qwen35.full_attention_interval = 4 -> 8 attention blocks and 24 gated-DeltaNet blocks, so a
  rejected draft needs the recurrent state rolled back; whether build 10991 does that for qwen35 is UNMEASURED.
- decode sits at the off-the-shelf knob floor: OSC.08 (experiment:a00-f256db1a-73ee5b:36) -- no swept serving knob moves tg64 at depth 4096;
  OSC.11 (experiment:a00-3caaf6eb-9065ef:25) -- a larger -ub is not a prefill lever (quiet re-run +1.29 pct). Speculation changes the algorithm,
  not the kernel: the next nudge on the served 9B has to come from there.
- hypothesis:lm-spec-decode-cpu-draft-hybrid (goal:g5.22; OWNER 09-18 04:0xZ: the GPU as the confirmation side) has no experiment -- it needs a
  draft download and waits on the off-box Bonsai round. This round is its draft-free first rung and answers its gating question: does
  speculation run on qwen35 in the served build at all.

## CLAIM
On the served Qwen3.5-9B-Q4_K_M with the router's own image (server-cuda, build 10991) and its model_args_9b, at least one draft-free
speculative type among ngram-simple / ngram-map-k / ngram-map-k4v / ngram-mod / ngram-cache raises the median per-request decode tok/s over
--spec-type none by >= 1.3x on >= 20 agent-shaped requests built from committed repo files (edit-and-return, code, digest), the paired 95 pct
interval of the per-request speedup clearing 1.0, with greedy outputs identical to the none arm on every request (or each divergence explained
by a top-2 margin < 0.1 at the divergence point in the none arm) and prompt tok/s within 5 pct of none.

## Dispatch line
config-max: paths.local_maxxing.specdec_out_dir (datasets/specdec/2026-09-23), added by the director before dispatch / template-max: none -- the
orders carry the GPU protocol (T0 guard, per-arm fresh container, JIT-cache mount, restore + proof) as OSC.11's did / code: none -- every lever
is an existing llama-server flag.

## FALSIFIERS
- the server refuses or errors on --spec-type with qwen35, or drafts nothing (0 drafted tokens over the set) -> speculation does not run on this
  hybrid in build 10991: record the exact message; hypothesis:lm-spec-decode-cpu-draft-hybrid waits on upstream support; LARGEST SAFE STEP = none.
- no type reaches a median 1.3x with its interval clearing 1.0 -> draft-free speculation is not a lever for this workload; still report the
  per-class medians (edit-and-return is the best case) and the acceptance rates.
- any divergence NOT explained by a < 0.1 top-2 margin in the none arm -> a verification defect for qwen35 in this build: that type is unsafe
  whatever its speed.
- prompt tok/s falls > 5 pct under a type -> the speedup is paid for in prefill: name the break-even output length.

## TESTS
- committed selftests next to the script, fixtures only: the prompt builder is deterministic (the same files give a byte-identical
  prompts.jsonl); the speedup and interval math on a toy table; the divergence finder on two toy token lists; each arm differs from none ONLY in
  the server flags, never in the request body.
- the neighbourhood: OSC.11's server protocol and helpers in .agi/context/local-maxxing/serve/ub_prefill_round.py may be imported, never edited;
  OSC.08's warm-up discipline (a warm-up request before any tok/s).

## FILE SCOPE
- ONE script and its test under .agi/context/local-maxxing/specdec/, named with the agent id; prompts.jsonl under the out dir.
- outputs (per-arm rows, server logs with the draft acceptance lines, the restore proof) under paths.local_maxxing.specdec_out_dir.
- ONE experiment node under this hypothesis.
- nothing under extensions/; no GGUF written; never the router's config or a config cell.

## CEILING
ONE parent + ONE model-loading host kid (memory_max 6G) · ~120 production lines · pi deepseek parent · a GPU round (the router down under the
T0 guard, restored whatever happens) · no per-round cap (TMM.51) · wall 120 min.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
frame: smaller -- the draft-free first rung of hypothesis:lm-spec-decode-cpu-draft-hybrid: no download, no draft model, one server flag per arm; it answers that line's gating question (does speculation run on the hybrid qwen35 in the served build) before any draft is fetched. Chosen over the build block my predecessor queued next: OSC.09 and OSC.11 showed the mounted ComputeCache already removes the cold JIT, and driver-JIT'd PTX runs the same SASS class, so a native sm_75 build buys no steady-state speed -- it is an enabler for custom kernels, not a nudge. draft-mtp was the bigger frame and is closed for this file: the served GGUF has no MTP tensors.
<!-- THOUGHT:END -->
