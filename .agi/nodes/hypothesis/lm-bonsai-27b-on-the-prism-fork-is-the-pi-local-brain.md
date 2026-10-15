---
id: hypothesis:lm-bonsai-27b-on-the-prism-fork-is-the-pi-local-brain
mint_id: bc07a6ec11684fdf9ecc48ebbdedee6a
type: hypothesis
parents:
  - experiment:a00-bb10233d-5a7f1f
  - goal:g5.27
next_edges: []
edited_by: director-thought
scaffold_hash: 72dccaca200b05c1
season: 2
testable_claim: Served on the PrismML fork b10685 inside the stock server-cuda image with arm B's line (-c 65536 -ngl 99 -fa on -np 1 -ctk q4_0 -ctv q4_0 --jinja) on the router's loopback port under its own alias, the plain Ternary-Bonsai-2-27B-PTQ1_0 fits the 8 GB card (peak VRAM <= 8,192 MiB), keeps one 65,536-token slot, decodes >= 17 tok/s after a warm-up, and completes ONE pi-local tool-call smoke turn through the local-town provider -- so the 0-credit lane runs on a brain that scored HumanEval 86.6 pct against the 9B's 78.0.
title: "TMM.76 step 1 (0-credit lane): the plain Bonsai 27B on the PrismML fork, KV at q4_0, is the pi-local BRAIN on the 8 GB box -- fits VRAM at a 65,536-token slot, >= 17 tok/s, and completes a pi-local tool-call turn"
town: local-maxxing
---
# hypothesis:lm-bonsai-27b-on-the-prism-fork-is-the-pi-local-brain

# hypothesis:lm-bonsai-27b-on-the-prism-fork-is-the-pi-local-brain

## Measured
```
source     experiment:a00-bb10233d-5a7f1f -- arm B = the plain Ternary-Bonsai-2-27B-PTQ1_0 on the PrismML fork b10685 (a CUDA 12.4 build run inside the
           stock server-cuda image), line -c 65536 -ngl 99 -fa on -np 1 -ctk q4_0 -ctv q4_0 --jinja: HumanEval 142/164 = 86.6 pct vs the served 9B's
           128/164 = 78.0 pct · peak VRAM 7,302 MiB · 10.06 s per problem · the OrcaBonsai LoRA is inert on coding (C1 -0.6 pp, 141/164 byte-identical)
board      B decodes 20.5-23 tok/s (7.27 GB) · the 9B 62.7 tok/s · the router's preset named bonsai is the 1.7B, not the 27B
before     01:0xZ 09-24 (director-thought): the router llama-server = router mode on 127.0.0.1:8080, restart unless-stopped, the 9B loaded and idle
           (one slot of 49,664 tokens) · GPU 6,730 / 8,192 MiB · host RAM available 10,748 MiB · 0 live agents · the pi local-town provider = the
           same loopback port, 3 model entries (the 9B, the 35B-A3B, the 1.7B)
```
- OWNER 00:xZ-01:0xZ 09-24 (verbatim on goal:g5), relayed as TMM.76: the 0-credit lane opens now -- "Use the bonsai or the orca one which is more
  optimized I think but combine it with kv cache compression"; step 1 = the brain swap, director-thought's, in its own window.

## CLAIM
Served on the PrismML fork b10685 inside the stock server-cuda image with arm B's line (-c 65536 -ngl 99 -fa on -np 1 -ctk q4_0 -ctv q4_0 --jinja)
on the router's loopback port under its own alias, the plain Ternary-Bonsai-2-27B-PTQ1_0 fits the 8 GB card (peak VRAM <= 8,192 MiB), keeps one
65,536-token slot, decodes >= 17 tok/s after a warm-up, and completes ONE pi-local tool-call smoke turn through the local-town provider -- so the
0-credit lane runs on a brain that scored HumanEval 86.6 pct against the 9B's 78.0.

## Dispatch line
config-max: paths.local_maxxing.brain_swap_out_dir (added in this mint commit) for the evidence; the new alias joins the pi provider's local-town
model list (off-repo harness config, before-value backed up) / template-max: none / code: none -- arm B's committed line, the port and an alias
are server flags; the director runs it in its own window (TMM.76), no kid.

## FALSIFIERS
- the fork fails to load or runs out of VRAM at -c 65536 -> the router is restored at once; fallback B (TMM.76): the 9B on the router with L1's
  -fa on -ctk q4_0 -ctv q4_0 (156,416 tokens = -np 3 at about 52K a slot).
- the smoke turn fails -- no tool call, a template or parse error, or no answer within 10 min -> the same restore and fallback B.
- decode < 17 tok/s after the warm-up -> the brain serves but the lane is slower than the board's 20.5-23 band: recorded, the leaves sized for it.

## TESTS
- VRAM through the nvidia-smi shim at load and at peak · the slot from the server's /slots · decode and prefill tok/s from the server's own timings
  on a warm-up request, then a measured one · ONE headless pi turn on the local-town provider with the new alias that must call a tool and answer.

## FILE SCOPE
- evidence (before / after values, the serve line, the timings, the smoke transcript's summary -- never its raw text) under
  paths.local_maxxing.brain_swap_out_dir · ONE experiment node under this hypothesis · nothing under extensions/ · the router's own
  configuration is never edited (stopped and started only).

## CEILING
```
who       the director in its own window (TMM.76) -- no kid, no parent, 0 USD
box       the GPU only; PASS 3 (01:37Z) uses no GPU · every before-value recorded; the router restored if anything fails
wall      30 min for the swap and the measures
STEP      LARGEST SAFE STEP if the smoke fails: fallback B -- the 9B at 3 slots of ~52K on L1's KV format, the lane still opens at 0 USD
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 3 residue correction (hypothesis:pass3-0924-residue-batch, demote reason: Post-warmup decode sample violates the literal bar) -- CORRECTED IN PLACE per thought-master TMM.118 owed 1. experiment:director-thought-brain-swap-2026-09-24 reports, in prose but outside its Measured table, plain Bonsai B's first real decode request after the warm-up at 16.99 tok/s -- a genuine post-warmup sample that sits below this hypothesis's own >= 17 tok/s bar. The Measured table instead reports only three later distinct-prompt rows for arm B (21.25 / 21.06 / 22.10, median 21.25); the sample actually excluded for cause was B's repeat request (a byte-identical prompt from a slicing slip, a prompt-cache hit at 4 prompt tokens), a different, later request than the 16.99 one. This residue does not flip a clean proved into a disprove -- the experiment's own verdict (inconclusive_lean_proved:90) already treats the literal plain-B claim as untested end-to-end, since B's one smoke attempt hung on a harness stdin defect before a clean re-run, and the owner switched the brain to the Orca variant before one happened. But it does mean the >= 17 tok/s decode bar for plain B was never cleanly met either: one legitimate post-warmup sample sits under it, undercounted in the table. The lane that actually went live and is named in TMM.76 step 2 is Orca C2 (20.17 / 20.51 tok/s, both clearing the bar, its own smoke PASS in 17 s) -- this residue is scoped to the literal plain-B claim only and does not touch the operative brain.
<!-- THOUGHT:END -->
