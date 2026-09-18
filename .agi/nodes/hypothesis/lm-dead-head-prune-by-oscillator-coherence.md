---
id: hypothesis:lm-dead-head-prune-by-oscillator-coherence
mint_id: 9c0d3a846d2d4a7687e464c26766cf22
type: hypothesis
parents:
  - idea:lm-dead-head-coupling-scan
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter; $0 compute; <= 10 GB downloads; file scope = .agi/context/local-maxxing/deadhead/{scan.py, scan.jsonl, prune.md, proxy.jsonl, sync.jsonl} + the kid experiment node + this node; no engine file; no served model touched.
edited_by: thought-master
falsifier: (1) fails to reproduce (dead count off by > 15 heads or precision off by > 5 points) -> the method is not portable; or (2) marks < 8% of heads on a served model; or (3) pruning costs > 3 proxy points or > 1.5 perplexity; or (4) Jaccard < 0.4 -> the oscillator reading is dropped and the paper is kept as a plain threshold heuristic; any of these = disproved for the pruning-in-production claim.
scaffold_hash: d919b4621121244f
season: 2
testable_claim: "On local-town (16 CPU threads + gpu-8g), with the paper scripts (project-89/coherence-guided-dead-head-identification, per-head c_h(i) = cos(s_h(i), x_i) averaged over a calibration set, zero-parameter geometric threshold): (1) the paper Qwen2.5-0.5B result reproduces from its own frozen JSON + scripts (dead 157/336 within +-5 heads, precision within 3 points of 95.5%) on our box; (2) the same scan on a model the town serves -- Qwen3.5-4B or the 9B in HF bf16/fp16 form, batch 1, 16 threads, GPU for the forward passes -- marks >= 15% of heads dead at the paper threshold AND the paper own base-rate control is reported beside it (random-k precision, the paper admits ~99% for GPT-2 Medium); (3) pruning the marked heads (zeroing their write-back, or dropping them from the GGUF via a conversion the kid documents) shrinks weights + KV bytes by a measured amount and costs <= 1 point on the 20-prompt kid-tier proxy and <= 0.5 perplexity on a 50k-token held-out text vs the unpruned model, on the same box, same seeds; (4) the oscillator link is TESTED not assumed: per-head c_h time series over positions are fed to the town Kuramoto order-parameter readout (C2 toys) and the dead set from synchrony (heads that never lock, order parameter < threshold) overlaps the paper dead set with Jaccard >= 0.7 -- else the paper criticality story is decoration and only the threshold survives."
tests: "ONE pi parent + ONE kid, off-box slot (local-town, alias only; GPU forward passes, 16 threads, -j16 builds), $1 OpenRouter, $0 compute, downloads <= 10 GB (paper repo, Qwen2.5-0.5B, the 4B in HF form); no Camber. Steps: clone the paper repo (commit sha logged), run its scripts on its frozen JSON (conjunct 1); write scan.py for the served model (per-head cosine over a 2k-token calibration slice, rows to .agi/context/local-maxxing/deadhead/scan.jsonl with model, layer, head, c_bar, threshold, dead flag); prune + measure (conjunct 3) with proxy rows beside the athena/bonsai checklist; synchrony readout (conjunct 4) reusing the C2 numpy toy code, Jaccard row; every number with the exact command; kid line_ceiling 120; rollback = nothing served is changed (all measurement in a scratch container). Order: AFTER hypothesis:lm-bonsai2-27b-kid-tier lands (same off-box slot); the paper digest already in the trove is the research (papers/dead-head.md, 2026-09-14 survey), this round is the application. If it holds, round 2 prunes Bonsai 2 27B itself (owner: several GB off each model we run)."
title: The dead-head paper coherence threshold (coupled-oscillator criticality, c_h = cos(head write-back, residual)) reproduces on a model we actually serve and lets us prune >= 15% of attention heads (GB off the KV + weights) with <= 1 point of kid-tier proxy loss -- measured on local-town 16 threads + 8 GB, $0
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-dead-head-prune-by-oscillator-coherence

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 03:4xZ (thought-master pane), verbatim: "Also most things might be way more useful if we can prove the pruning paper method using oscillators. We could prune several gn from each model we run even further" -- read: prove the dead-head paper method (coupled-oscillator criticality threshold) on models we serve, then prune several GB from each. Chain: papers/dead-head.md (survey 09-14: Qwen2.5-0.5B 157/336 dead, precision 95.5%, base-rate caveat ~99% random on GPT-2 Medium) -> idea:lm-dead-head-coupling-scan -> this hypothesis (reproduce, scan a served model, prune + measure, test the oscillator link with the C2 Kuramoto readout) -> round 2 = prune Bonsai 2 27B. Queued at director-thought after the Bonsai round (same off-box slot).

OWNER 2026-09-18 03:5xZ, verbatim: "Same with openjev" -- ROUND 3 TARGET (after Bonsai 2 27B): openjev stack = frozen Qwen/Qwen3.5-4B bf16 + Qwen3-Reranker-4B (8.9-11.6 GB peak on a 3090, CUDA-only, does not fit local-town 8 GB today): dead-head scan + prune of both models, then 8-bit/4-bit of the survivors, target = the openjev-score CLI running fully on local-town 8 GB with its own docs/RESULTS.md numbers reproduced within 2 points -> a $0 local typed-decision scorer to test against the jev bars on hypothesis:lm-jev-typed-acts-replay (top-1 >= 0.75, ECE <= 0.10; note openjev probabilities are uncalibrated per its README, so ECE is the honest gate).
