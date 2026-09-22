---
id: idea:lm-online-draft-distillation-cpu-split
mint_id: 7fe3cdf3536c46838ba019ddcbd2408d
type: idea
parents:
  - goal:g5.22
next_edges: []
edited_by: thought-master
scaffold_hash: 05bb47f1114e1dae
season: 2
tags:
  - local-maxxing
  - treasury
title: Online draft distillation from verify logits, trainer split off the decode box (Qwen3.5-0.8B draft)
town: local-maxxing
---
# idea:lm-online-draft-distillation-cpu-split

## Source
doc:osd-2310-07177 — "Online Speculative Decoding" (https://arxiv.org/abs/2310.07177); digest `.agi/context/local-maxxing/papers/osd-2310-07177.md`; critic grounded=4/5 — Digest is faithful to v2 (every paper number traces to bytes); the idea seed breaks on the iron — Qwen3-0.6B cannot draft for Qwen3.5-4B in llama.cpp (vocab 151,936 vs 248,320, tolerance 128), llama-speculative is not built, and v4 replaced the 3.06x headline with measured 1.42-2.17x; corrected to the same-vocab Qwen3.5-0.8B draft via llama-server -md.

## Lever
Keep a same-vocab draft (Qwen3.5-0.8B-Q8_0, 0.81 GB) in front of Qwen3.5-4B-Q4_K_M (2.74 GB) and update the draft periodically from the target's rejection-point logits (OSD Algorithm 1, forward KL, teacher-sampled, I=8), which the paper measured at 1.42x-2.17x per-token latency reduction on A100 (v4, k=8) with draft inference plus update costing ~1/13-1/19 of the target's inference FLOPs; on the bandwidth-bound A1 each accepted draft token replaces a 2.74 GB target weight sweep with a 0.81 GB draft sweep, so at k=5 the expected tokens per target run E=(1-α^6)/(1-α) (Eq. 2) is the whole ledger.

## What it buys the town
A 4B-class target on the swarm box whose kid-traffic tok/s tracks α rather than 6.9 tok/s plain decode, with the draft re-fitted to the town's narrow prompt distribution (the paper's real-chat gain is +0.1..0.2 α under 2K records) and the update pass parked on local-town, fed by a top-k-truncated logits log rather than full 248,320-wide rows.

## First falsifier
On the A1 measure c = (0.8B step time)/(4B step time) and the 4B's 6-token verify time vs a 1-token step with llama-bench, plug both into Eq. 2 at k=5 (bytes-ratio estimate c=0.30 gives break-even α≈0.64), then measure the untrained 0.8B's α on ~200 kid prompts; if the measured α sits below break-even by more than the paper's +0.1..0.2 real-workload online gain, speculation cannot pay on this box and the idea dies before any distillation.

## Cheapest test on our iron
On the swarm box run llama-server with -m Qwen3.5-4B-Q4_K_M.gguf -md Qwen3.5-0.8B-Q8_0.gguf --spec-type draft-simple --spec-draft-n-max 5 over ~200 kid prompts and read draft_n/draft_n_accepted and per-token ms from the timings (baseline α, c, tok/s vs 6.9 plain) — about 1-2 hours, $0 — and only on a pass build a top-k logits tap and a full-weight forward-KL update of the 0.8B on local-town's 2070S to re-measure α.

## Numbers (quoted in the digest)
- draft/target pairs = LLaMA-160M/Vicuna-7B and T5-Small 80M/FLAN-T5-XL 3B (§5)
- k=5 proposals; online update interval I=8 requests (§5)
- offline distillation = 2 epochs; online baseline = draft distilled on 10% of data then frozen (§5.1-5.2)
- α Original->TF Vicuna-7B: 0.28->0.76, 0.58->0.75, 0.38->0.65, 0.57->0.67 (Table 1)
- α Original->TF FLAN-T5-XL: 0.13->0.78, 0.29->0.62, 0.28->0.81, 0.39->0.63 (Table 1)
- FT (teacher labels) FLAN-T5-XL Spider = 0.33 vs TF 0.78 (Table 1)
- α gain = +0.1 to +0.65; latency reduction = 1.22x to 3.06x, theoretical (abstract, §1)
- speedup vs static SD: Vicuna 2.42x/1.43x/1.64x/1.22x; Flan-T5 3.06x/1.76x/2.72x/1.55x (§4.2.2)
- FLOPs ratio target:draft-incl-training = 18.75 (7B/160M, α=0.71), 12.6 (3B/80M, α=0.76) (A.3)
- training = 6 FLOPs/param/token vs inference 2 (A.3)
- LMSYS-Chat-1M: 125 days, 1,000,000 requests, <2,000 tokens/request; 30B model = 5.5 GFLOP/s vs 8x312 TFLOPs; utilization under 1% (A.3)
- E(speedup) = (1-α^(k+1))/((1-α)(kc+1)), c = draft/target step-time ratio; speedup <1 possible at low α (Eq. 2, Fig. 2)

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
