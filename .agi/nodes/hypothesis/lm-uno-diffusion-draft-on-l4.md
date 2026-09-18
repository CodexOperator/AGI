---
id: hypothesis:lm-uno-diffusion-draft-on-l4
mint_id: e4b135df5ee244e2b38dd859d6edab6e
type: hypothesis
parents:
  - hypothesis:lm-spec-decode-cpu-draft-hybrid
  - goal:g14
next_edges: []
ceiling: 1 Camber XS hour (1.50 USD) + 0.03 USD CPU probe, only after the GO; $1 OpenRouter; $0 on our boxes; downloads 0 on our boxes; file scope = .agi/context/local-maxxing/uno/{cmds.md, prompts.jsonl, rows.jsonl} + bench/<utc>.jsonl + the kid experiment node + this node.
edited_by: thought-master
falsifier: < 1.3x at batch 1, or any non-identical greedy output, or the stack does not install on the L4 image within 20 min of the hour -- then diffusion drafting is not the GPU-resident arm at this scale and the spec-decode node keeps its CPU-draft + MTP/EAGLE-3 arms; if the job is billed at more than 2x its wall-clock, no further Camber jobs until the granularity is understood.
scaffold_hash: 10e342ab749fbb46
season: 2
testable_claim: "On one Camber GPU XSMALL (1x L4 24 GB, 8 cores, 32 GB) as a one-shot job (SDK/CLI, never an interactive box): (1) the ifm-ai/uno stack installs (torch cu128, FlashAttention-2 linear sampler; FA3 tree sampler is Hopper-only and is skipped) and s-sahoo/uno-qwen3-8B loads beside its base (16.38 + 0.70 GB bf16 fit 24 GB with an 8k KV); (2) on 20 kid-shaped prompts (the town checklist, greedy, 256 new tokens) the Psi-Spec Linear sampler reaches >= 1.5x tok/s over the base Qwen3-8B at batch 1 and >= 1.3x at batch 8, outputs byte-identical to the base greedy decode (the lossless guarantee, checked per prompt); (3) tokens-per-forward (TPF) and acceptance rate recorded per prompt; (4) total cost = job wall-clock x 1.50 USD/h + the observed billing granularity (the 5-min CPU-XSMALL probe from doc:lm-round0-table runs first, 0.03 USD), the 17 GB download timed on the rental network; every number in bench/<utc>.jsonl labelled uno-*."
tests: "NO DISPATCH WITHOUT THE PRIME GO (spend: 1 XS GPU-hour = 1.50 USD + 0.03 USD CPU probe, from the 3 GPU-h/month allowance; the 100 signup credits may cover it). Then ONE pi parent + ONE kid, API slot (the kid drives the Camber CLI from ARM4C; model bytes land on the rental only, never on our boxes); $1 OpenRouter cap; job torn down at the end, verified; kid line_ceiling 150; rows to bench/<utc>.jsonl; the 20 prompts committed."
title: "BANKED SPEND (one Camber XS hour, needs the Prime GO): uno-qwen3-8B (Qwen3-8B bf16 + 0.7 GB diffusion LoRA, Apache-2.0) on one L4 24 GB reaches >= 1.5x tok/s over base Qwen3-8B at batch 1 and >= 1.3x at batch 8 with byte-identical greedy outputs, for <= 1.50 USD + the download on the rental -- decides whether diffusion drafting is the GPU-resident draft arm of the town"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-uno-diffusion-draft-on-l4

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
GO (Prime 06:28Z): step (1) ordered to director-thought 06:28Z as the API-slot round; step (2) waits for the probe line + the owner window.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DEVIATION RECORDED (thought-master 06:28Z): this node spends rental time, which a director never starts on its own authority -- Prime-granted 06:28Z (VERIFIED belam) under the owner Camber XS allowance (09-16 21:2xZ, 3 GPU-h/month), two steps gated: (1) a 5-min CPU-XSMALL probe (0.03 USD) that must show billing granularity <= per-minute (a core-hour bill = STOP and report the number); (2) ONE XS GPU-hour (1.50 USD, hard cap one hour, signup credits first) only after (1) reports and the owner has not vetoed in the Prime pane (silence after the probe line = proceed). Claim unchanged: >= 1.5x tok/s at batch 1 with byte-identical greedy outputs.
<!-- THOUGHT:END -->
