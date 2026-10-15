---
id: experiment:a00-288aec4d-1f6c77
mint_id: 61d16440c58f464aacb1074b0a552b77
type: experiment
parents:
  - hypothesis:lm-oscillator-research-hunt
next_edges: []
confidence: 0.6
edited_by: a00-288aec4d
evidence_runs:
  - experiment:a00-288aec4d-1f6c77
loop: hypothesis:lm-oscillator-research-hunt@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1e0b8f4c8e0722f1
season: 2
title: "Diffusion-LLM reader hunt: Mercury closed, Fast_dLLM_v2_1.5B is the runnable open dLLM, per-step unmask-confidence is the oscillator read site"
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-288aec4d-1f6c77

## Experiment

Diffusion-LLM reader hunt for the owner's hybrid oscillator sketch. Fetched 11 sources (arXiv abs + search, HF API + cards, READMEs) 2026-09-16. Digest: `.agi/context/local-maxxing/troves/2026-09-16-oscillatory/diffusion-llm.md` (also mirrored in this worktree).

**Answers to end-questions:**
- **Mercury weights open?** NO — API only (arXiv 2506.17298). Weights not released. Measured.
- **One open dLLM for our iron (gpu-8g / Camber 24GB)?** Fast_dLLM_v2_1.5B (apache-2.0, ~1.5B) — quant ~1-1.5GB fits the 8GB card. Dense runner-up: LLaDA-8B (MIT) fits Camber 24GB but burns the 3 GPU-hr/mo budget on remask loops. Measured weights/licence, ESTIMATE on quant memory.
- **Ternary dLLM?** None surfaced (surveyed LLaDA/iLLaDA/MoE, Mercury, SEDD, Fast-dLLM, Dream GGUF). Honest hole flagged: no citation possible for absence; recommend a dedicated ternary-dLLM hunt.
- **3 closest dLLM mechanisms to the sketch:** (1) remask/unmask-confidence schedule loop = the timeful per-position state axis (LLaDA optimal steps==response length); (2) dKV-Cache subscribe/reuse across steps = the "KV as read sites" (Fast-dLLM); (3) block/R3 process-guided scheduling = the no-strict-hierarchy (Block Diffusion).
- **Smallest numpy toy:** N=32 oscillator net reading synthetic per-step confidences, phase-lock vs a rhythm-neuron subnetwork, <5 min CPU.
- **$0 next experiment:** run Fast_dLLM v2_1.5B once, hook per-step unmask-confidence, drive a numpy oscillator gate to schedule which positions unmask next; measure quality vs steps vs the equal-steps baseline.

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
returned diffusion-llm digest
