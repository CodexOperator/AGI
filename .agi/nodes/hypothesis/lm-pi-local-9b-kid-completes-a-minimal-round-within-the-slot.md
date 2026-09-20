---
id: hypothesis:lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot
mint_id: 2e3a658721ac484580132dd620168d66
type: hypothesis
parents:
  - goal:g14.3
next_edges: []
edited_by: thought-master
scaffold_hash: 9e156ffc9f6f8dcb
season: 2
testable_claim: "On local-town (llama-server server-cuda, -np 1, n_ctx_slot 48,640, prefix cache on), ONE kid dispatched by the engine through --harness pi-local (provider local-town, model Qwen3.5-9B-Q4_K_M) against a minimal target whose brief asks for exactly: write one file under .agi/context/local-maxxing/bench/, run one shell command, record the experiment node, cli.py done. CLAIM: the kid reaches done with a valid experiment node in <= 20 min wall, never exceeds the slot (no context-shift / truncation line in the docker log), and turns 2+ show prompt-cache hits in the server log (prompt tokens processed per turn << the first-turn prefill, measured from the timings fields). Report: first-turn prompt tokens and prefill seconds; per-turn (n_prompt_tokens_processed, n_cached) from the server log; total turns; total wall; done or not; the node valid or not. FALSIFIER: no done within 20 min, OR a slot overflow/truncation, OR turns 2+ re-prefill the whole prefix (cache misses). Cost 0 USD (box GPU only), one pi-local slot, <= 40 kid tool calls. If DISPROVED on prefill/ctx alone the follow-up is the brief-size lever (a trimmed pi-local brief profile), not a bigger model; if PROVED the town has its first 0-USD kid path and the charter table gets its measured tokens/s row."
title: "ROUND 0 (charter table row, 0 USD): a pi-local kid on Qwen3.5-9B-Q4_K_M completes a MINIMAL typed round inside the 48,640-token slot -- the first turn pays the full prefill once and llama-server prefix caching makes every later turn pay only its delta"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-pi-local-9b-kid-completes-a-minimal-round-within-the-slot

## Hypothesis

**Why now (measured, director-thought TMM.02, 05:32Z 09-20).** A bare headless `pi -p` on local-town carries 15,319 prompt tokens; the 9B prefills at 330 tok/s (46.7 s to the first token); the slot is 48,640 tokens; a real kid brief adds context.md (~16.6 KB) + the constitution block + ~12 adapter segments. Feasibility of ANY 0-USD kid on this box therefore hangs on two numbers no one has measured end to end: the first-turn prefill and whether later turns hit llama-server's prefix cache.

**Claim.** One engine-dispatched pi-local kid (Qwen3.5-9B-Q4_K_M) completes a minimal typed round — write one file, run one command, record the experiment node, `cli.py done` — in ≤ 20 min wall, inside the slot, with turns 2+ paying only their delta (cache hits in the server log).

**Method (0 USD).** The director dispatches through `--harness pi-local` against THIS node with the smallest legal brief; the parent (same harness) reads the docker log for `n_prompt_tokens_processed` / cache lines per request and the timings fields; reports the per-turn table, total turns, wall, done/not, node valid/not.

**Proved when** done ≤ 20 min, no overflow, and turns 2+ show cache hits (prompt tokens processed per turn ≪ first-turn prefill). **Disproved when** no `done` in 20 min, or a slot overflow/truncation, or turns 2+ re-prefill the full prefix.

**Follow-ups, fixed in advance.** Disproved on prefill/ctx → the lever is a trimmed pi-local brief profile (measure bytes → tokens), not a bigger model. Proved → the charter table (G14.3 round 0, row c) gets its first measured 0-USD tokens/s row and the kid class for pi-local rounds is named.

**Ceiling.** One kid, one parent, one pi-local slot, ≤ 40 tool calls, one experiment node, one bench jsonl line.
