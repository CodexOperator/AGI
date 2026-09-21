---
id: goal:g14.15
mint_id: c13838ca1ec14ab9b9d407208f618a8c
type: goal
parents:
  - goal:g14
next_edges: []
confidence: 0.9
edited_by: thought-master
goal_id: G14.15
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: a26df92b01d46d01
season: 2
status: active
tags:
  - local-maxxing
  - telepathy
  - kv-cache
title: "G14.15: KV-CACHE TELEPATHY — self-telepathy (a tool that captures the KV of a span tied to a section/turn, carries it forward and re-surfaces it later: in-session RAG over KV, in-stream memory and compression, latent-to-latent recurrence) and swarm telepathy (same-model small instances each holding a slice of the context, exchanging KV segments, a jev-like weighing of which segments matter, settling into an ordering a decoder consumes)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.15
## Agent Notes
**Owner source (2026-09-21 01:3xZ, verbatim on goal:g14):** "I want to experiment with self-telepathy. Give the model a tool to capture a specific KV cache in a stream linked to a specific section or turn or whatever, kv caches are neat like that I think, and send that 'forward' in the context windows so it's always available and can be re-surfaced later. Like a in-session rag for kv caches that builds as the session progresses. It also works kinda like an in-stream compression and memory mechanism. Latent latent space recurrence." / "And also use the kv cache telepathy to let smaller models swarm together; with each one holding a piece of the total context and all coordinating together via kv cache messaging until the proper kv cache results emerge that can be fed into a decoder. So like a swarm of jevs almost weighing opinions together on which kv caches matter more where until a final ordering and layering settles into place."
**Prior already measured (idea:lm-nodes-as-kv-caches → hypothesis:lm-kv-slot-save-beats-reprefill, owner 09-18):** a saved llama.cpp KV slot restores ≥ 3× faster than re-prefill (README prior 40-100×) but costs 7,000-37,000× the text bytes on disk — KV is compute caching, not compression. Telepathy is what that prior did NOT test: (a) a SPAN, not a whole slot, tied to a section/turn; (b) carried forward and re-surfaced at a LATER position (a KV position shift — `llama_kv_cache_seq_add` — not a byte copy); (c) chosen by a ranking (which spans matter), i.e. RAG over KV; (d) exchanged between same-model instances.
**Commits to.** Chunk by chunk, on the resident 9B at 0 USD GPU: (1) SPAN FIDELITY — a span's KV captured at position p and re-injected at position p′ (shifted) reproduces the same greedy continuation as re-prefilling the span text in ≥ 95 pct of 50 held-out continuations, at ≤ 10 pct of the prefill compute; (2) THE TOOL — a server-side `capture(span_id, tokens[a:b])` / `surface(span_id)` pair the model can call mid-stream (llama.cpp slot save/restore + seq shift, or the fork), with the captured store growing as the session runs; (3) IN-SESSION KV RAG — a ranking over captured spans (attention mass to the span from the last N tokens, or a small scorer) that re-surfaces the right span for a probe question at ≥ the accuracy of text retrieval at lower prefill; (4) SWARM — k same-model instances each holding one slice of a long document exchange captured spans and a shared ranking until one decoder instance answers a question over the whole document at ≥ the single-instance long-context answer; the jev-style weighing = each instance scores every span it receives, the ordering is the consensus. Cross-model swarms (different weights) are OUT of scope until a C2C-style projector exists (banked).
**Invariants.** Every chunk measures fidelity (token-level agreement vs re-prefill), compute (prefill tokens avoided), bytes (KV span size vs text), and wall on the same served 9B, same n_batch/ubatch pinned (logits are not bit-identical across batch sizes — prior). No model bytes leave the rig; nothing is baked into weights; the tool is a server/harness change under `datasets/`-style scratch or the town's fork, never the engine tree.
**Falsifiers.** (1) is falsified if shifted re-injection agrees < 80 pct with re-prefill (then RoPE-shifted KV is not position-portable for this model and telepathy needs re-prefill from saved TEXT plus a saved KV only for the tail); (3) if KV ranking never beats text retrieval on the probe set; (4) if the swarm's answer quality is below the single long-context instance at equal total tokens.
**Done when.** (1)-(3) have verdicts and either a working in-session KV RAG on the served model or the measured reason it cannot work; (4) has one measured k=2 swarm result.
**First chunk (the director mints G14.15.1 self-telepathy and G14.15.2 swarm, same format, then TEL.01 = chunk (1) span fidelity):** `hypothesis:` under G14.15.1 — testable claim (1) above, falsifier, the committed test, file scope, ceiling in engine units; runs on the resident 9B (no model loading on the host), cap 1 USD for the parent, queued after MP.01 (one GPU round at a time). Links: `doc:recurrent-looped-transformer` (latent recurrence), `idea:lm-nodes-as-kv-caches`, the trajectory super node.
