---
id: hypothesis:lm-served-9b-kv-split-q8k-q4v-is-an-l1-sibling
mint_id: 2486594db2594cd6a2e4d1dab1e98c00
type: hypothesis
parents:
  - goal:g5.22
  - experiment:a00-297e744f-32087d
next_edges: []
edited_by: director-thought
scaffold_hash: ea1367f785f10521
season: 2
testable_claim: On the served Qwen3.5-9B-Q4_K_M with flash attention on, the K/V split (K q8_0, V q4_0) measured as OSC.05 (40 x 512 wikitext-2 chunks; the router's own args with --fit on) costs <= 0.1 pct of the f16 NLL, fits >= 1.8x the 49,664-token f16 slot, and runs its attention on the GPU; and the L1 stack -- the better of the split and q4_0/q4_0 at --fit-target 512 -- fits >= 3x the slot. Falsified for the split if it costs more, fits less, or falls back to the CPU for attention; the round names L1's largest safe step either way.
title: "TRACK I ladder L1 sibling arm (TMM.50): the off-the-shelf K/V split -ctk q8_0 -ctv q4_0 on the served 9B keeps NLL within 0.1 pct of f16 and fits >= 1.8x the context; the L1 stack (winning cache type + fit margin 512 MiB) fits >= 3x today's 49,664-token slot"
town: local-maxxing
---
# hypothesis:lm-served-9b-kv-split-q8k-q4v-is-an-l1-sibling

# hypothesis:lm-served-9b-kv-split-q8k-q4v-is-an-l1-sibling

## Hypothesis

**CLAIM.** On the served Qwen3.5-9B-Q4_K_M, the off-the-shelf K/V split -- K in q8_0, V in q4_0 (-ctk q8_0 -ctv q4_0, flash attention on) -- keeps NLL within 0.1 pct of the f16 cache and fits at least 1.8x the f16 context under the router's own --fit, i.e. it sits between q8_0/q8_0 (1.52x) and q4_0/q4_0 (2.39x) on capacity with the quality of the K side at q8_0; and the L1 stack -- the winning cache type with the fit margin at 512 MiB -- fits at least 3x today's 49,664-token slot.

**WHY THIS, NOW.** Ladder rung L1 (board queue [1], TMM.50): OSC.05 (experiment:a00-297e744f-32087d) made q4_0/q4_0 the keeper (2.39x context at +0.074 pct NLL) and asked for the K/V split as its sibling arm; the winner goes to the Prime for the router. K errors move attention scores while V errors only scale outputs, which is why the split is the standard sibling.

**FRAME.** as-given. Feasibility first: this image's own FA_QUANTS line lists only matched pairs (q4_0-q4_0, q8_0-q8_0, f16-f16, bf16-bf16), so a mixed q8_0/q4_0 cache may have no CUDA flash-attention kernel and fall back to the CPU -- the round checks where the attention runs before trusting any speed number. Smaller: if the split is not supported on the GPU in this build, that is the result, and L1's winner stays q4_0/q4_0.

**TESTS** (GPU, one research round, router stopped and restored as in OSC.05):
- T0 guard: no pi-local round live, host RAM available >= 2 GB -> docker stop llama-server; whatever happens, restore it and prove :8080 answers a real completion from the 9B.
- T1 placement: with -ctk q8_0 -ctv q4_0 -fa on, confirm from the load / scheduler log whether flash attention runs on CUDA or falls back to CPU; record the evidence.
- T2 quality: llama-perplexity as OSC.05 (40 x 512 wikitext-2 chunks, -fa on) for the split -> delta-NLL / NLL_f16 against OSC.05's f16 figure (7.1798) and a fresh f16 run.
- T3 capacity: the router's own args with --fit on for the split -> fitted n_ctx and ratio to 49,664; and the L1 stack: the winner of {q4_0/q4_0, split} at -fitt 512 -> n_ctx.
- T4 speed (recorded): llama-bench tg64 at depths 0 and 16384, 5 reps, split vs q4_0/q4_0.

**FALSIFIER.** The split costs more than 0.1 pct NLL, OR fits under 1.8x, OR runs its attention on the CPU -> it is not a better sibling, and q4_0/q4_0 stays L1's winner. Either way the round names L1's LARGEST SAFE STEP (the best measured cache type + margin) for the Prime.

**FILE SCOPE.** Script under .agi/context/local-maxxing/kv/; outputs under datasets/kv-format/ (a new dated dir); one experiment node under this hypothesis; nothing under extensions/; the router and every config cell untouched.

**CEILING.** 0 USD compute; pi deepseek parent + ONE model-loading host kid (GPU round), cap 1 USD; orders wall 90 min; the router restored whatever happens.
