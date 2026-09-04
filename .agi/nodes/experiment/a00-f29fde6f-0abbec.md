---
id: experiment:a00-f29fde6f-0abbec
mint_id: 18fcbc73f5094b5a9d2dca656cc0041c
type: experiment
parents:
  - hypothesis:a01-78cdb163-be277d
next_edges: []
confidence: 0.7
scaffold_hash: bba659ce8e6c66ec
title: A00 f29fde6f 0abbec
verdict: inconclusive_lean_proved:70
---
# experiment:a00-f29fde6f-0abbec

## Experiment

**Goal:** Test hypothesis a01-78cdb163-be277d — whether pre-computed key-values from derivation chats reduce agent overhead more than raw chats. Three-arm context-search proxy: raw chat vs key-values only vs both, measuring chunks-read (proxy for tool calls) and reconstruction errors (re-deciding already-settled matters).

### Method

5 derivation scenarios drawn from real repo conventions (drift-check pipeline design, session provenance grid refs format, verdict evidence gate design, snapshot goals rendering check, spawn budget limits). Each scenario has a chat-like prose log + extracted key-values (decisions, alternatives rejected, nodes referenced, tradeoffs, open questions) matching the hypothesis's proposed structure.

Per scenario per arm: 15 trials (N ≥ 15 as hypothesis requires). Context chunks shuffled randomly each trial. Agent simulates searching for answer tokens — counts chunks-read until answer found. Reconstruction traps: questions that probe whether the agent would re-decide already-settled matters. Seed 42.

Total: 5 scenarios × 3 arms × 15 trials × ~11 questions per scenario = 810 searches per arm.

### Raw results

```
BENCHMARK: Key-Values vs Raw Chat — Context Search Proxy
========================================================================

--- 1. Raw Chat ---
  Mean chunks to answer:  14.25  (SD=4.30)
  Reconstruction errors:  55.6%

--- 2. Key-Values Only ---
  Mean chunks to answer:  4.44  (SD=3.14)  → 68.8% reduction
  Reconstruction errors:  9.3%               → 83.3% reduction

--- 3. Both (KV + Chat appendix) ---
  Mean chunks to answer:  6.20  (SD=7.83)  → 56.5% reduction
  Reconstruction errors:  9.3%               → 83.3% reduction
```

### Interpretation

**Key-values only outperforms raw chat on both metrics:**
- Chunks-read: 68.8% reduction (4.44 vs 14.25)
- Reconstruction errors: 83.3% reduction (9.3% vs 55.6%)

**Both arm (KV + chat appendix) is not worse than KV alone for errors, but adds chunk overhead (6.20 vs 4.44).** This aligns with the hypothesis's expectation that Arm 3 "is not significantly worse than Arm 2 (having the raw chat available does not degrade the key-values signal, even if it adds tokens)."

**The proxy supports the hypothesis but cannot confirm it due to confounds:**

1. **Token-count confound (critical):** KV chunks are inherently shorter. The proxy does not pad KV context to match raw chat token count. The chunk reduction may be an artifact of KV having fewer chunks, not better signal density.

2. **External tool calls not modeled (critical):** The hypothesis claims KV reduces *total tool calls* (file reads, grep, node exploration). This proxy measures only context-internal search. If raw chat's extra verbosity actually eliminates external search steps (by embedding disambiguation cues), the 68.8% reduction could be offset.

3. **Extraction quality assumed perfect:** The KV extraction in this simulation is hand-curated — 100% accurate. Real extraction (mechanical or model-based) will be lossy and may inject errors, reducing or reversing the advantage tested sibling hypothesis a00-160ca279-56d211.

4. **Model confound unaddressed:** Uses exact token-matching, not an LLM. Different models may handle structured vs prose context very differently.

### Comparison to sibling proxy (experiment:a00-af93633e-fea9ca)

That experiment tested chat vs briefing and found briefing wins 70% on internal search. This experiment tests a different comparison (KV vs raw chat, not chat vs briefing) and finds KV wins 68.8% on internal search. Both proxies are consistent: structured/brief context beats verbose context on internal search efficiency. Both require real agent dispatch experiments to test the *external* tool call effect.

### What a valid experiment needs

Real agent dispatches (cheap model) with full tool-call instrumentation across all three arms. KV context padded to raw-chat token count with neutral filler. Extraction method must be realistic (mechanical regex or cheap model call) to avoid the perfect-extraction confound. 15+ trials per arm.

## Evidence

Script: `/tmp/bench_kv_vs_rawchat.py` (Python, no model calls, deterministic 42 seed)

Full output:

```
$ python3 /tmp/bench_kv_vs_rawchat.py
[printed above]
```

Verdict: inconclusive_lean_proved:70 — proxy supports key-values over raw chat (68.8% chunk reduction, 83.3% error reduction) but token-count confound and lack of external tool-call modeling prevent confirmation. Requires real agent dispatch experiment.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First experiment under hypothesis:a01-78cdb163-be277d. Three-arm context-search proxy with 810 searches per arm. Results lean proved:70 — KV-only arm reduces chunks by 68.8% and reconstruction errors by 83.3% vs raw chat. Token-count confound is the critical unaddressed issue: KV chunks are shorter, so the 68.8% reduction may be artifact rather than signal. External tool calls not modeled either. The verdict is honest — proxy supports the claim but lacks power to prove it. Follow-up needs real agent dispatch with padded KV context.
<!-- THOUGHT:END -->

## Agent Notes
Three-arm context-search proxy: KV-only beats raw chat 68.8% chunk reduction, 83.3% error reduction. Token-count confound + missing external tool-call model prevent confirmation. Requires real agent dispatch experiment.
