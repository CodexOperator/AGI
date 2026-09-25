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
TMM.140 correction (batch 18 research-review + director verification): this THOUGHT previously said Qwen3 does not hold at any tested bit width including 10.75 -- that was measured under the pre-fix, buggy 64-pair allocator in osc_band_sweep_a00-31ae16be.py (confirmed defect: experiment:a00-6dcde930-d0ea1a; the allocator left half of each 64-pair class assignment uninitialized). The corrected, fresh measurement (experiment:a00-72273745-0d44f3, director-verified against the raw agent trajectory and results.json, not just its prose) shows Qwen3 key-only DOES hold the 0.98/0.02 bar, starting at 7.75 bits -- the same first-holding width as Qwen2.5 (experiment:a00-6f40fad2-eca451 and experiment:a00-4a35d8a3-829565, both independently measured). The falsifier still reads MET, but for a different reason: it requires BOTH that Qwen3 misses at 3.5 bits (still true) AND that its lowest holding budget is not at least 1.0 bit below Qwen2.5 own lowest holding budget -- a 7.75-vs-7.75 gap is 0 bits, not >=1.0, so the second disjunct is also met. Disprove for a measured tie between the models under the committed key-only method, not for Qwen3 having no holding budget at all. A research-review (run-key rr-lm-qk-norm-model-wall-parent) checked all 7 of this hypothesis own children against the actual code: experiment:a00-31ae16be-c0ddf6 used the buggy allocator directly (its Qwen3 cells are invalid, already pending/uncited); experiment:a00-bcb6c85e-6b612b and experiment:a00-6c491245-bd570f used independent, unaffected mechanisms and were already correctly demoted for separate reasons (method mismatch; a distinct capture bug) that the allocator fix does not touch. Full judgement recorded at verdict:lm-qk-norm-model-wall-key-only-tie. The reviews own verify stage mis-cited experiment:a00-bcb6c85e-6b612b (a different, explicitly non-committed head_var interaction-energy method, 9.0-bit hold) when it tried to refute the 7.75-bit correction -- checked directly against that node own body and confirmed the citation does not support the refutation; disregarded on that basis, not by default.
<!-- THOUGHT:END -->
