---
id: hypothesis:lm-spec-decode-cpu-draft-hybrid
mint_id: 5ee62e6054a8400a9e9648d3c5d573cf
type: hypothesis
parents:
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter; $0 compute; <= 3 GB downloads inside the local-town ceiling; file scope = .agi/context/local-maxxing/specdec/{prompts.jsonl, rows.jsonl, cmds.md} + bench/<utc>.jsonl + the kid experiment node + this node.
edited_by: thought-master
falsifier: < 1.2x on the median prompt, or any output differs from greedy no-draft, or the draft steals GPU memory -- then CPU-draft speculation does not pay on this box and the hybrid budget goes to MoE expert offload instead.
scaffold_hash: 6090044d54eca384
season: 2
testable_claim: On local-town (16 threads + gpu-8g), llama-server with the target fully on GPU (the 9B first; Bonsai 2 27B PTQ1_0 once served) and a draft model on CPU (-ngld 0, -td 16; candidates Qwen3.5-0.6B/1.7B or Ternary-Bonsai-1.7B, same tokenizer family required) reaches (1) >= 1.5x tg tok/s vs the same target without a draft on 20 kid-shaped prompts (node writing, probes, digests; prompts committed), 3 reps, warm-up first, per-row -t/-td/--draft-max/acceptance rate recorded; (2) outputs byte-identical to no-draft greedy decoding on the same prompts (speculative decoding is exact); (3) GPU VRAM unchanged within 200 MiB (the draft lives in RAM); (4) A1 untouched (all on local-town); (5) cost row per 1M output tokens from measured watts.
tests: ONE pi parent + ONE kid, off-box slot (alias only), $1 OpenRouter, $0 compute, downloads <= 3 GB (draft GGUFs); rows to bench/<utc>.jsonl labelled specdec-*, prompts + acceptance rates to .agi/context/local-maxxing/specdec/; rollback = the 9B back on /v1 as it was; kid line_ceiling 120; after the Bonsai round in the off-box queue (the target should be the model we will actually serve).
title: Speculative decoding with a small draft model on local-town 16 CPU threads and the target on the 8 GB GPU raises target tok/s by >= 1.5x on kid-shaped prompts at unchanged outputs
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-spec-decode-cpu-draft-hybrid

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
