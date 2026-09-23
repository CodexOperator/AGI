---
id: doc:dead-head
mint_id: 2f86798d9bfb427dbf5c0a9b051bf0ec
type: doc
parents:
  - goal:g5.29
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/dead-head.md
scaffold_hash: 9d63728a609eef15
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"Coherence-Guided Dead-Head Identification in Frozen Transformers: A Zero-Parameter Geometric Threshold from Coupled-Oscillator Criticality\""
town: local-maxxing
---
# doc:dead-head

**Source:** https://github.com/project-89/coherence-guided-dead-head-identification
**Digest (link_ref):** `.agi/context/local-maxxing/papers/dead-head.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=4/5).
**Critic note:** Numbers trace to source bytes but the framing does not: ground truth is zero- not mean-ablation, death_persistence is a batch-timer fraction not a recurrence quantity, the '157 dead' rule is not 'z<0.96', the paper's SmolLM2 234 contradicts its own bundle's 261, and the artifact itself refutes the K_c story (precision rises monotonically through chi_c=0.96, Spearman(z,dL)=+0.27); what survives is GQA-group KV compaction tested on Qwen3-0.6B (g=2) and the artifact as a free D1 ground truth.
**Seeds:** idea:lm-dead-head-coupling-scan

## Relevance to local-maxxing
On the bandwidth-bound swarm decoder a dead head only saves its q/o slices (derived ~18 MB of ~494 MB per Q8 token on Qwen2.5-0.5B, ~3.6%) at the paper's own +1.2 to +1.5 nats, so as a pruning lever it is a bad trade; the only KV-cache-reaching result (SmolLM2 -27.5% KV at +0.53) needs a small GQA group and Qwen2.5-0.5B's g=7 kills it (Qwen3-0.6B g=2 untested). What is directly usable is the frozen Qwen2.5-0.5B artifact: 336 per-head mean-ablation deltas on exactly the D1 model, so D1's per-layer-normalized importance can be scored head-by-head against z_h with no GPU, and identification is one 32x128-token forward pass instead of 336 ablations. The framing is the town's flip/SNN thread verbatim (LayerNorm puts tokens on S^(d-1), heads are Kuramoto/Lohe couplings, MLPs intra-oscillator modes, dead = coupling below K_c), so chain 2's R-vs-K apparatus is the right tool to test whether 0.96 is a real transition or a label on a smooth ranking (base-rate lift 1.0001 on Qwen says the latter); for the looped transformer the artifact's per-head death_persistence field (e.g. 0.625 for L0H0) is the quantity that decides whether a recurrent block's heads can be pruned at all.
