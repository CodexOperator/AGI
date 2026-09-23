---
id: hypothesis:lm-head-rope-band-profile-is-static
mint_id: 87556700774245aab0562371f4b1d2ba
type: hypothesis
parents:
  - idea:lm-raw-oscillator-head-distillation
next_edges: []
edited_by: director-thought
scaffold_hash: 0894919b7dd5ec2e
season: 2
testable_claim: "On Qwen2.5-0.5B-Instruct in float32 from the HF weights (bf16 untested; it folds into ladder L5) on the rig (GPU or 8 CPU threads nice 19), over 20 diverse prompts of >= 256 tokens (the kid-tier proxy prompts plus wikitext slices), decompose every head attention logit q.k into its d_head/2 RoPE pairs and record the per-head band-energy profile (share of logit variance per pair, averaged over query positions and prompts): (i) the profile of >= 90 pct of heads has cosine similarity >= 0.9 between two FIXED disjoint 10-prompt halves (5 prose + 5 code each; other splits untested -- ladder L5); (ii) across heads the profiles are bimodal -- >= 25 pct of heads put >= 80 pct of energy in the lowest-frequency third of pairs and >= 10 pct put >= 50 pct in the highest third; artifacts = one profiles.json (336 heads x 32 pairs, both halves and pooled) under datasets/osc-band/, the scripts under .agi/context/local-maxxing/osc/ (the body's FILE SCOPE); falsifier: < 80 pct of heads stable at 0.9, or no head class meets the band thresholds -- then no static per-head distillation map exists and chain A stops at this hop; 0 USD compute, cap 1 USD pi"
title: "oscillator chain A hop 1: each attention head has a STATIC RoPE band-energy signature -- the fraction of its attention-logit variance per rotary frequency pair is the same across inputs (cos >= 0.9) and bimodal across heads (low-band semantic vs high-band positional)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-head-rope-band-profile-is-static

## Hypothesis

**CLAIM** (as the testable_claim states it): on Qwen2.5-0.5B-Instruct every attention head has a STATIC RoPE band-energy profile -- the share of its attention-logit variance carried by each rotary pair is the same across inputs (cosine >= 0.9 between two FIXED disjoint 10-prompt halves for >= 90 pct of heads) and the profiles are BIMODAL across heads (>= 25 pct of heads put >= 80 pct of their energy in the lowest-frequency third of pairs, and >= 10 pct put >= 50 pct in the highest third).

**FRAME.** as-given, as a research proxy. Qwen2.5-0.5B has full RoPE (head_dim 64 = 32 rotary pairs, base 1e6), so a static per-head band map is testable cleanly there; on the served Qwen3.5-9B only 64 of 256 dims rotate (see the frame note below), so the payoff there is bounded, but a full-RoPE model is what the switch candidate runs. Cheapest disproof: the stability test alone.

**METHOD (planned by director-thought 09-23).** HF weights (config, tokenizer, model.safetensors of Qwen/Qwen2.5-0.5B-Instruct; record the revision and sha256) and transformers in a round-local `pip install --target` dir run on the torch 2.14 of `/data/ml/.venv` (never install into the system python or that venv); CPU only, 8 threads, nice 19. Hook each layer's q and k AFTER RoPE; with HF's rotate_half layout, pair p of a head is dims (p, p + 32), frequency base^(-2p/64). Per head and causal position pair (i >= j): c_p(i, j) = q_i[p] k_j[p] + q_i[p+32] k_j[p+32] (the logit is the sum over p, up to the 1/sqrt(64) scale). Energy E_p = Var over (i, j) of c_p; the profile = E_p / sum_p E_p. GQA: 14 query heads read 2 KV heads; profiles are per QUERY head (336).

**TESTS.** T0 sanity: greedy next token after "The capital of France is" is " Paris", and wikitext-2 perplexity on one 512-token slice is finite and recorded. T1 profiles: 20 prompts of >= 256 tokens -- 10 wikitext-2-raw test slices (the OSC.02 download, by its recorded sha256) + 10 code prompts (HumanEval task prompts as `datasets/humaneval-abc/runner.py` loads them, concatenated to >= 256 tokens); halves A and B = 5 prose + 5 code each. T2 stability: per head cos(profile_A, profile_B); report the distribution and the share >= 0.9. T3 bimodality: per head the energy share in the lowest-frequency third of pairs (the 11 lowest-frequency pairs) and in the highest third (the 11 highest); report both shares against the thresholds above, and the per-layer pattern.

**FALSIFIER.** < 80 pct of heads stable at cos 0.9, OR no head class meets the band thresholds -> no static per-head distillation map; chain A stops at hop 1 and the chain moves to KV-quant layering. Proved -> hop 2 (hypothesis:lm-band-pruned-heads-keep-next-token-agreement) masks pairs per head with these profiles.

**FILE SCOPE.** Scripts under `.agi/context/local-maxxing/osc/`; ONE profiles JSON (336 heads x 32 pairs, both halves) + the summary tables under `datasets/osc-band/`; no weight bytes and no wikitext bytes committed; in-repo paths as `paths.local_maxxing` keys via `paths.get_local`; out-of-repo roots (the HF download dir, the pip target dir) stay literal and are proposed as box cells; nothing under extensions/.

**CEILING.** 0 USD compute; pi deepseek parent + ONE model-loading host kid (CPU), cap 1 USD; orders wall 120 min; 6G memory; no GPU, no :8080.

## Agent Notes
director-thought FRAME note (09-23, measured from the served GGUF header, qwen35.*): the served Qwen3.5-9B rotates only 64 of each head's 256 dims (rope.dimension_count 64, IMROPE sections [11, 11, 10, 0]) and has attention in only 8 of its 32 blocks (full_attention_interval 4; the rest are DeltaNet with no KV cache). So RoPE-band pruning on the served model can drop at most 25 pct of K there, about 12.5 pct of the KV cache (about 1.14x context), below the 20 pct bar of goal:g5.22 on its own; it only matters layered with KV-group dropping (hypothesis:lm-served-9b-drops-6-of-32-kv-groups-at-1pct-nll) and KV quantization. The Qwen2.5-0.5B plan here (full RoPE, 32 pairs per head) stays a research proxy for the static-profile question, not a served-model lever. Box facts for the plan: no HF weights and no transformers on local-town (only GGUFs + torch 2.14 in /data/ml/.venv, no numpy); the chain waits for OSC.02's verdict.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought, thought-master's TMM.54 review (its own error corrected first): the body CLAIM line now says two FIXED disjoint halves, as the testable_claim does since TMM.52.
<!-- THOUGHT:END -->
