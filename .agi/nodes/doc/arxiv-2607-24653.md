---
id: doc:arxiv-2607-24653
mint_id: 4a7a544a66cc44db8388aab7b97fb2cf
type: doc
parents:
  - goal:g5.29
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/arxiv-2607-24653.md
scaffold_hash: 4e1d05bb3250d784
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"Kimi K3: Open Frontier Intelligence\""
town: local-maxxing
---
# doc:arxiv-2607-24653

**Source:** https://arxiv.org/abs/2607.24653
**Digest (link_ref):** `.agi/context/local-maxxing/papers/arxiv-2607-24653.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=4/5).
**Critic note:** All digest numbers trace to the PDF text (Table 1, §2.1.1, §2.2, §2.3, §3.2-3.4, §4.1.4, §5.4, §6.4, Table 5, §7) and the nano-kpu README; defects are three reader mechanisms (8-bit substrate, fixed-point argument, decode saving as demonstrated) leaking in as the source's, a [58]-cited N~=8, and a falsifier that cannot tell KV bytes from attention FLOPs on a 4-core CPU — tightened with a q8_0-KV control; BF16-only tile trick does not port to the Turing card.
**Seeds:** idea:lm-kda-constant-state-kv-bytes

## Relevance to local-maxxing
Nothing in K3 runs on the town's iron (2.8T total / 104B active), so it is a source of mechanisms, not weights. On the bytes-per-token ledger the one that matters is the 3:1 KDA:MLA hybrid: 69 of 93 sequence-mixing layers read a fixed dk x dv state per token instead of a KV cache that grows with context, which on the swarm box's bandwidth-bound decode removes the per-step KV read that competes with the weight read at long context. The lower-bounded decay (alpha > e^-5, log-decay in (-80,0) per 16-token tile) is a fixed-point-range argument that lands on the E3 byte-neuron LUT / flip-mode SNN thread, and the open nano-kpu repo is a bit-exact INT4-g128 fixed-point reference of the same hybrid with LUT ROMs, runnable in Verilator on local-town; Block AttnRes (softmax over <=8 prior block outputs, O(Nd) bytes/token) is the depth-side complement to the recurrent looped transformer, and §6.4's cost-per-task figures are the pricing input for running kids off OpenRouter in bursts.
