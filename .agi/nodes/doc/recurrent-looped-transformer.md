---
id: doc:recurrent-looped-transformer
mint_id: a659f4c9e2bb46388d739f5445dd8e33
type: doc
parents:
  - goal:g5.29
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/recurrent-looped-transformer.md
scaffold_hash: f993e963daf1c937
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"Recurrent Looped Transformer\""
town: local-maxxing
---
# doc:recurrent-looped-transformer

**Source:** https://www.alphaxiv.org/abs/2609.recurrent-looped-transformer
**Digest (link_ref):** `.agi/context/local-maxxing/papers/recurrent-looped-transformer.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=4/5).
**Critic note:** Every quoted number traces to the README/PDF bytes; the errors are the reader's inferences — the merge costs +3.1% bytes/token not ~0, merge-only 8+0 wins exactly one README cell (mod-5 flat seed 42) and loses two, the proposed no-feedback 8+0 control is just T8, and no code/generator/wall-clock exists in the source.
**Seeds:** idea:lm-token-state-feedback-merge

## Relevance to local-maxxing
The owner hint mislabels the mechanism: RLT is temporal recurrence (one hidden vector carried across tokens, fixed blocks per token), not depth recurrence, and it cites Geiping-style recurrent depth as distinct prior art; its only parameter-reduction axis is encoder/decoder weight tying, which the paper says "does not by itself reduce block evaluations or guarantee lower latency" — so on the bandwidth-bound decode ledger the bytes-touched-per-token delta from tying is ~0 while stored footprint halves. What it does offer the ledger is near-free state: 3d^2 params (0.79M at d=512) plus a 512-float state, with the README's merge-only RLT 8+0 hitting 90.89% on mod-5 flat vs 20.57% for a same-depth transformer — though the isolating no-feedback ablation is not yet run. For the flip/SNN and Kuramoto threads, s_t updated by a gated leaky-integrator merge is structurally an oscillator/byte-neuron state coupled token-to-token, and the paper's Appendix B Jacobian-product warning is chain 2's R-vs-K stability question; the 25-29M-param synthetic runs fit local-town's local-town GPU.

## Agent Notes
CHAIN (d) HOP 1 (thought-master 20:1xZ, from the 2026-09-18-looped survey read stage, judged by hand -- critique/panel/judge stages not run): the RLT paper is an analytical report with NO empirical numbers and no released weights (MEASURED) -- it cannot carry evidence; its recurrence is temporal, not depth. The only released looped LM with a CPU path is Ouro (ByteDance, 2510.25741: 1.4B = 24 layers x 4 loops, 2.6B = 48 x 4, Apache-2.0, GGUF via a patched llama.cpp); Huginn-0125 (3.5B latent depth, F32 15.6 GB, no GGUF) is the archival control; MoR / Loop-Think-Generalize weights sit on external drives. So the chain starts where evidence can be measured on our CPU: hypothesis:lm-ouro-loops-beat-dense-on-kid-checklist (loops=4 vs loops=1 vs a same-unique-param dense model on the 20-prompt kid checklist). Ledger rule learned: looping multiplies CPU memory traffic by the loop count -- bytes-touched-per-token = weight_bytes x loops (ESTIMATE 3.3 tok/s for Ouro-1.4B Q4 at 4 loops on this box at 12 GB/s).
