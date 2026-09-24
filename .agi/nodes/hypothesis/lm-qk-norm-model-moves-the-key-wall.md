---
id: hypothesis:lm-qk-norm-model-moves-the-key-wall
mint_id: 637aa93419a34e70905f39c4fdea6952
type: hypothesis
parents:
  - idea:lm-why-l3-precision-allocation-wall-is-8-12-bits
  - goal:g5.22
next_edges: []
FILE SCOPE: .agi/context/local-maxxing/osc/ and datasets/osc-band/2026-09-24-qknorm/ (repo-tracked) plus paths.local_maxxing.osc15_hf_dir (new scratch dir outside the repo, for the ONE named download below) only -- no router changes, no engine edits
ceiling: <= 1 USD OpenRouter; 0 cloud GPU compute; ONE named download permitted on this rig -- Qwen/Qwen3-0.6B, post-trained, under the owner's standing yes for this rig (doc:l5-owner-decisions:130, TMM.126) -- no other downloads without a fresh owner yes; runs <= 10 min per scored probe (the one-time download itself is separate and detached, not counted against this)
edited_by: director-thought
falsifier: If the QK-norm model misses both bars at 3.5 bits and its lowest tested holding budget is not at least 1.0 bit below the Qwen2.5 control lowest tested holding budget, the claim is disproved. Because the single model pair confounds model identity with normalization, a pass licenses matched ablations but cannot by itself attribute the shift to QK normalization. The first experiment can produce the killing result with the preregistered same-grid sweep.
scaffold_hash: 9684db81c0b1bc2a
season: 2
testable_claim: "On one resident QK-norm model with attn_k_norm, post-RoPE key energy allocation has a lowest tested budget meeting agreement >=0.98 and mean KL <=0.02 at least 1.0 bit below the lowest tested holding budget of a same-grid Qwen2.5 control, while the same 3.5-bit arm is compared against uniform and random controls. A pass is evidence that model class moves the wall, not proof that key normalization caused the move. CEILING: <=120 production lines."
tests: "ONE pi parent + ONE kid, slot: off-box (needs the rig), steps (1) read the Qwen3.5 GGUF metadata and assert attn_k_norm before touching weights, (2) run the existing OSC.04-style key quantization probe against the resident QK-norm model and a same-eval Qwen2.5 control, (3) sweep matched 3.5/6/8/9/10/12-bit energy, uniform, and random arms with scale overhead, (4) persist agreement, KL, bits, model alias, and input shas after every probe, rows to bench/<utc>.jsonl, kid line_ceiling 120."
title: A QK-norm model moves the key-precision wall, separating architecture from Qwen2.5 outliers
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-qk-norm-model-moves-the-key-wall

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
ADVERSARIAL REVIEW MODIFIED: narrowed the inference from causal QK-norm attribution to a model-class probe and aligned the falsifier with the claim. The rig requirement is explicitly off-box while that rig is offline; no host, hardware model, location, or secret is named.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Amended FILE SCOPE + ceiling (director-thought gen 22, TMM.126): the owner has a STANDING yes for model downloads on this rig (doc:l5-owner-decisions:130) -- the ceiling's old 'no downloads on ARM4C without an owner yes' clause was never actually about THIS rig (a different, ARM4C box), so it over-read as broader caution than the owner's own policy required. TMM.126 approved ONE named download, Qwen/Qwen3-0.6B (post-trained, matching the existing Qwen2.5-0.5B-Instruct control), as batch 9 after batch 8's mechanical proof (OSC.15, experiment:a00-688fdd59-f9e124) landed. FILE SCOPE now names the new scratch config path (paths.local_maxxing.osc15_hf_dir, added separately, config-max) the download will live under -- no literal path in any orders text. This does not reopen the door to ANY future download: it is scoped to this one named checkpoint, cited here so a future reader sees the authorization was real, not assumed.
<!-- THOUGHT:END -->
