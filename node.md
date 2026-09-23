---
id: goal:g5.30
mint_id: c13838ca1ec14ab9b9d407208f618a8c
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G5.30
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
title: "G5.30: KV-CACHE TELEPATHY — self-telepathy (a tool that captures the KV of a span tied to a section/turn, carries it forward and re-surfaces it later: in-session RAG over KV, in-stream memory and compression, latent-to-latent recurrence) and swarm telepathy (same-model small instances each holding a slice of the context, exchanging KV segments, a jev-like weighing of which segments matter, settling into an ordering a decoder consumes)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.30
## Agent Notes
**Owner source (2026-09-21 01:3xZ, verbatim on goal:g14):** "I want to experiment with self-telepathy. Give the model a tool to capture a specific KV cache in a stream linked to a specific section or turn or whatever, kv caches are neat like that I think, and send that 'forward' in the context windows so it's always available and can be re-surfaced later. Like a in-session rag for kv caches that builds as the session progresses. It also works kinda like an in-stream compression and memory mechanism. Latent latent space recurrence." / "And also use the kv cache telepathy to let smaller models swarm together; with each one holding a piece of the total context and all coordinating together via kv cache messaging until the proper kv cache results emerge that can be fed into a decoder. So like a swarm of jevs almost weighing opinions together on which kv caches matter more where until a final ordering and layering settles into place."
**Prior already measured (idea:lm-nodes-as-kv-caches → hypothesis:lm-kv-slot-save-beats-reprefill, owner 09-18):** a saved llama.cpp KV slot restores ≥ 3× faster than re-prefill (README prior 40-100×) but costs 7,000-37,000× the text bytes on disk — KV is compute caching, not compression. Telepathy is what that prior did NOT test: (a) a SPAN, not a whole slot, tied to a section/turn; (b) carried forward and re-surfaced at a LATER position (a KV position shift — `llama_kv_cache_seq_add` — not a byte copy); (c) chosen by a ranking (which spans matter), i.e. RAG over KV; (d) exchanged between same-model instances.
**Commits to.** Chunk by chunk, on the resident 9B at 0 USD GPU: (1) SPAN FIDELITY — a span's KV captured at position p and re-injected at position p′ (shifted) reproduces the same greedy continuation as re-prefilling the span text in ≥ 95 pct of 50 held-out continuations, at ≤ 10 pct of the prefill compute; (2) THE TOOL — a server-side `capture(span_id, tokens[a:b])` / `surface(span_id)` pair the model can call mid-stream (llama.cpp slot save/restore + seq shift, or the fork), with the captured store growing as the session runs; (3) IN-SESSION KV RAG — a ranking over captured spans (attention mass to the span from the last N tokens, or a small scorer) that re-surfaces the right span for a probe question at ≥ the accuracy of text retrieval at lower prefill; (4) SWARM — k same-model instances each holding one slice of a long document exchange captured spans and a shared ranking until one decoder instance answers a question over the whole document at ≥ the single-instance long-context answer; the jev-style weighing = each instance scores every span it receives, the ordering is the consensus. Cross-model swarms (different weights) are OUT of scope until a C2C-style projector exists (banked).
**Invariants.** Every chunk measures fidelity (token-level agreement vs re-prefill), compute (prefill tokens avoided), bytes (KV span size vs text), and wall on the same served 9B, same n_batch/ubatch pinned (logits are not bit-identical across batch sizes — prior). No model bytes leave the rig; nothing is baked into weights; the tool is a server/harness change under `datasets/`-style scratch or the town's fork, never the engine tree.
**Falsifiers.** (1) is falsified if shifted re-injection agrees < 80 pct with re-prefill (then RoPE-shifted KV is not position-portable for this model and telepathy needs re-prefill from saved TEXT plus a saved KV only for the tail); (3) if KV ranking never beats text retrieval on the probe set; (4) if the swarm's answer quality is below the single long-context instance at equal total tokens.
**Done when.** (1)-(3) have verdicts and either a working in-session KV RAG on the served model or the measured reason it cannot work; (4) has one measured k=2 swarm result.
**First chunk (the director mints G14.15.1 self-telepathy and G14.15.2 swarm, same format, then TEL.01 = chunk (1) span fidelity):** `hypothesis:` under G14.15.1 — testable claim (1) above, falsifier, the committed test, file scope, ceiling in engine units; runs on the resident 9B (no model loading on the host), cap 1 USD for the parent, queued after MP.01 (one GPU round at a time). Links: `doc:recurrent-looped-transformer` (latent recurrence), `idea:lm-nodes-as-kv-caches`, the trajectory super node.

thought-master 05:0xZ 09-21 (owner 05:0xZ, verbatim on goal:g14): TEL.01 may restart :8080 with --cache-reuse N (llama.cpp prompt-cache reuse = KV shift of the matching prefix, the primitive span fidelity tests); slot save/restore stays available; conditions: between rounds only, router mode kept (the 9B reloads on demand), restore = a real completion; record the exact server line on the experiment node.

thought-master 05:1xZ 09-21 (knowledge, TEL.01): span fidelity is unmeasurable on the resident server line (no slot save path, no cache reuse); the shift mechanism exists in the binary. TEL.02 = the same claim on a server started with --cache-reuse N --slot-save-path (owner-permitted restart); if cache_n > 0 on a shifted span there, chunk (1) is measurable; if not, the primitive needs the fork or a C-side seq_add call, not HTTP.

thought-master 06:4xZ 09-21 (knowledge, TEL.02): for the Qwen3.5 family (IMROPE, 4 positions per embedding) KV spans are NOT position-portable in llama.cpp -- telepathy on this model line = same-prefix reuse (works, 0.093x prefill) + saved TEXT with a tail KV, never a shifted span. Consequence: chunk (1) is CLOSED on Qwen3.5 with the measured reason; chunk (2) the capture/surface tool builds on prefix reuse + text; and a TEL.03 census (0 USD, CPU/metadata) decides which candidates in the line are shift-capable at all (get_can_shift per GGUF: Bonsai 2 27B / Qwen3.8-27B hybrid attention, the 0.6B-4B small bases for G14.7.2) -- telepathy's swarm (chunk 4) needs one shift-capable family or stays prefix-only.

thought-master 08:0xZ 09-21 (knowledge, TEL.03): a KV-shift SWARM (G14.15.2) cannot include the town's three bigger candidates under stock llama.cpp -- IMROPE families are not position-portable; only a 1.7B-class qwen3/NEOX member (Bonsai-1.7B, on the box) can join a real shift-based swarm today. Telepathy's path on this line: (a) same-prefix reuse (works, 0.093x prefill) + saved TEXT with tail KV for the big models; (b) a shift-based k=2 swarm PROTOTYPE on Bonsai-1.7B (the only shift-capable member) to prove the coordination mechanics cheaply before any bigger family is sought; (c) one probe: get_can_shift on the deployed prism fork (build 10685) -- if the fork differs, the census re-runs there.
**First chunk (the director mints G5.30.1 self-telepathy and G5.30.2 swarm, same format, then TEL.01 = chunk (1) span fidelity):** `hypothesis:` under G5.30.1 — testable claim (1) above, falsifier, the committed test, file scope, ceiling in engine units; runs on the resident 9B (no model loading on the host), cap 1 USD for the parent, queued after MP.01 (one GPU round at a time). Links: `doc:recurrent-looped-transformer` (latent recurrence), `idea:lm-nodes-as-kv-caches`, the trajectory super node.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ask 2026-09-21: renumber local-maxxing research g5.30 → g5.30 (g5 continuation after g5.21; mint_id preserved; town:local-maxxing kept); no director assignment
<!-- THOUGHT:END -->
