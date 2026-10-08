---
id: idea:lm-raw-oscillator-head-distillation
mint_id: ab68cc91032c464ba6cb592a042f3d0c
type: idea
parents:
  - hypothesis:lm-dead-head-prune-by-oscillator-coherence
next_edges: []
edited_by: thought-master
scaffold_hash: 5381952dcba59574
scale: big
season: 2
title: "OWNER 06:1xZ 09-19: raw (non-spiking) oscillators to distill attention heads further -- RoPE is already a bank of oscillators per head, the dead-head c_h is already a coherence statistic; chain it with the KV-compression line (q4 KV, kv-slot, C2C)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-raw-oscillator-head-distillation

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
thought-master 06:16Z 09-19 OWNER ORDER in the thought-master pane 06:1xZ, verbatim: Can we also try out a few hypothesis regarding using raw oscillators to help distill down the attention heads even further? No need to try and tackle applying it to spiking things yet, let's just see what we can do using more or less directly the knowledge we have, including then chaining it with or combining it with a separate chain on kv compression. READING: two oscillator handles we already hold without spiking -- (1) RoPE: every head is a bank of d_head/2 rotary oscillators at frequencies base^(-2j/d), so a head can be distilled to the bands it actually uses; (2) the dead-head coherence c_h = cos(head write-back, residual), the paper's coupled-oscillator criticality statistic. CHAIN A (heads): hypothesis:lm-head-rope-band-profile-is-static -> hypothesis:lm-band-pruned-heads-keep-next-token-agreement; CHAIN B (KV, existing): hypothesis:lm-q4-kv-cache-tg-at-4k (measured), lm-kv-slot-save-beats-reprefill, lm-c2c-kv-bridge-released-fusers; JOIN: hypothesis:lm-band-pruned-k-cache-compounds-with-q4-kv (dropped bands are never stored, on top of q4); PARALLEL: hypothesis:lm-head-merge-by-phase-locking-matches-dead-head-coherence. BYTES: the first measured hop needs Qwen2.5-0.5B-Instruct + Qwen3-0.6B in HF bf16 on the rig = the owner download queue item (1), the C2C pair -- not yet fetched (verified 06:1xZ: no HF dirs under /data). Not spiking; the LIF/spectral line stays where it is.
