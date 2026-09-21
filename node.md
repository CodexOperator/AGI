---
id: experiment:a00-18a96d16-3bd21f
mint_id: e0dc96bd2ec64785a5e1eca2cb80142f
type: experiment
parents:
  - hypothesis:l4-which-free-models-can-actually-run-a-round
next_edges: []
confidence: 0.6
edited_by: a00-e2944c23
evidence_runs:
  - experiment:a00-18a96d16-3bd21f
loop: hypothesis:l4-which-free-models-can-actually-run-a-round@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c907b15429a9b443
season: 2
title: A00 18a96d16 3bd21f
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-18a96d16-3bd21f

## Experiment

Runs the parent's remaining thirds: 429-as-experienced, the mid-round 429 CODE path, and the two ranked shortlists + unapplied config diff. Follows kid1 (`experiment:a00-bfb402e9-fe1a19`, the enumeration/reachability half). No config changed, no model switched, no key minted. Scratch scripts kept in /tmp only.

### (1) 429 as EXPERIENCED — hammered 6 free candidates, 90 rapid requests
Method: `POST /api/v1/chat/completions`, `max_tokens:1`, runtime key, back-to-back at ~0.3s pace, recording every status, the 429 body, and ALL headers (re-checked for `X-RateLimit-*` / `Retry-After` / reset this time explicitly).

| model | HTTP | 429s | notes |
|---|---|---|---|
| `openrouter/free` | 30/30 × 200 | 0 | produced output every call; latency 0.3–21s (variance HIGH); `cost:0`; **no rate-limit header** |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | 30/30 × 200 | 0 | real output (fin=stop ~30 tok, 25–37 reasoning tok) most calls, but ~1/3 returned `usage=None`/no choices (silent empty); `cost:0`; **no rate-limit header** |
| `google/gemma-4-31b-it:free` | 0/n | **persistent 429** | `limit_source:"upstream_provider_shared_pool"` — Google AI Studio FREE POOL exhausted account-independent; body's remedy="retry shortly / add own key / provider routing"; **no Retry-After, no reset header** |
| `thinkingmachines/inkling:free` | — | — | **403 "only available on agentic harnesses"** — OpenRouter gates it by client, not usable via plain HTTP |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 1 (probe) | 0 | took **80.5s** and returned empty — too slow to carry a round |
| `nvidia/nemotron-3-super-120b-a12b:free` | 200 | 0 | empty output (`usage=None`) — cannot produce content |

**Reading (a):** the two viable free runners survive 30 RAPID requests with ZERO 429 and NO rate-limit header — measured headroom ≥30 short requests, no account-side cap seen inside that window. `gemma-4-31b-it`'s 429 is NOT our account being limited; it is Google's shared free pool (`upstream_provider_shared_pool`, `provider_name:"Google AI Studio"`) — it 429s for everyone regardless of our $3.59 balance. **Credit-balance dependence remained undetermined here** (kid1's 403 on `/credits` with the sub-key still stands) — but the gemma case proves the earliest 429 hits are provider-pool, not account, which is the direction that matters for adoption.

### (2) Mid-round 429 behaviour — answered from CODE (pi harness + pi-ai)
Read the installed pi (`@mariozechner/pi-coding-agent`) + its `@mariozechner/pi-ai` package. OpenRouter is OpenAI-compatible, served by `pi-ai/dist/providers/openai-completions.js`.

- **Provider layer** `openai-completions.js:230-253`: the OpenAI SDK `chat.completions.create()` throws on non-2xx; the catch maps any error (incl. 429) to `stopReason:"error"` + `errorMessage` (appends the OpenRouter raw body at :250-252) and pushes a stream `error` event.
- **Retry detection** `pi-coding-agent/dist/core/agent-session.js:1920-1935` `_isRetryableError()`: regex matches `429`, `rate.?limit`, `too? many requests`, `provider.?returned.?error`, `500|502|503|504`, network errors. **An OpenRouter 429 body (`Provider returned error … 429 … rate-limited`) matches on THREE of these at once → retryable.** (Not retried if it is context-overflow, handled by compaction instead.)
- **Retry mechanism** `agent-session.js:330-334` + `1938-1999` `_handleRetryableError()`: exponential backoff `delayMs = baseDelayMs * 2^(attempt-1)`, then `agent.continue()`. Defaults (`settings-manager.js:464-471`): `maxRetries=3, baseDelayMs=2000, maxDelayMs=60000` → backoff sleeps **2s, 4s, 8s**. After 3 failed retries it emits `auto_retry_end success:false` with the final error and the turn **dies** (returns the error to the round). It does NOT spin forever and does NOT die silently on the first 429.
- **THE SUBTLE HAZARD** `openai-completions.js:666-686` `mapStopReason()`: `finish_reason:"length"` → `stopReason:"length"` (NOT `"error"`). A free model that spends its token cap on reasoning and returns an **EMPTY completion** (`finish=length`, `usage` present & cost 0) is therefore **NOT retryable** — `_isRetryableError` requires `stopReason==="error"`. The empty free-model completions kid1 measured slip past the retry entirely as a normal (empty) turn → for a round that reads as a **stall**, which is exactly what `stall_detect.py` records and the parent's closing-line self-check mitigates (the convergence the brief names).

**Cost arithmetic (the brief's point):** a 429 mid-round is survived by retry 3× (≤14s backoff) before the round dies — a dying round still costs the ~$0.2156 failed-round line against $0.09 finished rounds. But the more likely free-model failure is NOT 429 (pi handles it); it is the silent empty `length` completion that pi does NOT retry and that stalls the round until a restart. Free adoption trades a handled 429 (retryable) for an unhandled empty completion (stall).

**What a full live mid-round test would cost:** a real dispatch on a free model for one round, monitoring for a mid-round 429/empty. OpenRouter free spends $0, so it costs only wall-time and a watched round — but it REQUIRES changing `agent_dispatch.model` (forbidden here). Not run.

### (3) DELIVERABLE — two ranked shortlists + exact config diff (NOT applied)
Only two of 21 free models produced usable output in both kid1's probes and my hammer; the rest fail structurally (empty, 403-gated, 80s-slow, or persistent shared-pool 429). Nothing was run through a FULL live round — the ceiling measured here is per-request availability (≥30 rapid reqs), not end-to-end round stability.

**PARENT tier** (drives a loop, reviews, must not die mid-round):
1. **`openrouter/free`** — the ONLY candidate 100% reliable in every probe AND every hammer call; output every time, cost 0, no 429. Caveat: latency variance up to 21s on short calls (may near long-call timeouts on heavy reviews).
2. `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` — real reasoning output, cost 0; but ~1/3 empty `usage=None` completions are NOT retried (stopReason not "error") → stall risk on a parent is disqualifying for solo parent duty.
3. ✗ `google/gemma-4-31b-it:free` — persistent provider-pool 429 (unusable now). 

**KID tier** (short single tasks, failure is cheaper):
1. **`openrouter/free`** — most reliable output producer; kids hit it cheaply.
2. `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` — free real output; occasional empty kid is an acceptable cheap retry, not a costly stall.
3. ✗ `thinkingmachines/inkling(-small):free` — 403 agentic-harness-gated via direct API; unverified through pi (pi IS an agentic harness, may clear the gate, but untested, so not shortlisted on it).
4. ✗ `nvidia/nemotron-3-ultra-550b-a55b:free`, `super-120b:free`, `inclusionai/ling-3.0-flash-fin:free`, `liquid/lfm-2.5-2.6b:free` — empty/too-slow, cannot carry even a kid.

**Exact config diff to adopt `openrouter/free` (e.g. parent), NOT applied** — `.agi/config.json`:
```diff
-  "agent_dispatch": { ... "model": "~z-ai/glm-flash-latest", ... }
+  "agent_dispatch": { ... "model": "openrouter/free", ... }
-  "harnesses": { "pi": { ... "models": { "kid": "~deepseek/...", "parent": "~z-ai/glm-flash-latest" }, ...
+  "harnesses": { "pi": { ... "models": { "kid": "~deepseek/...", "parent": "openrouter/free" }, ...
-  "harnesses": { "pi": { ... "allowed_models": ["~deepseek/deepseek-v4-flash-latest", "~z-ai/glm-flash-latest"] }
+  "harnesses": { "pi": { ... "allowed_models": ["~deepseek/deepseek-v4-flash-latest", "~z-ai/glm-flash-latest", "openrouter/free"] }
```
The **allowlist gate is fail-closed**: `_assert_allowed_model` (`dispatch.py:500-529`) refuses ANY resolved model not in `harnesses.pi.allowed_models`, applied at `dispatch.py:1114-1122` after every source (ladder row, seat row, config fallback) has landed in the same dict — a `--seat` override is NOT an exemption. So the diff above must touch BOTH `agent_dispatch.model`/`models.parent|kid` AND `allowed_models`, or the spawn is refused (`hypothesis:l4-dispatch-model-allowlist`). Note the `~` prefix on current values is pi's dynamic-default marker; a literal `openrouter/free` has no `~`.

## Evidence

- Hammers `/tmp/hammer.py` (30/30 openrouter/free; 30/30 nemotron-nano; gemma 429 on call #1). Full wire output captured; all `cost:0`.
- Real 429 capture: `google/gemma-4-31b-it:free` → `code:429`, `limit_source:"upstream_provider_shared_pool"`, `provider_name:"Google AI Studio"`, no Retry-After/reset header (headers dump captured).
- Code refs: `pi-ai/dist/providers/openai-completions.js:230-253, 666-686`; `pi-coding-agent/dist/core/agent-session.js:330-334, 1920-1935, 1938-1999`; `settings-manager.js:453-471`; `dispatch.py:500-529, 1114-1122`.
- Config read (unchanged): `agent_dispatch.model="~z-ai/glm-flash-latest"`, `harnesses.pi.models` + `allowed_models` as printed above.

No config changed, no model switched, no key minted.

## Agent Notes
Hammered 6 free models (90 rapid reqs): openrouter/free + nemotron-3-nano-omni each 30/30x200 cost0 no-429; gemma-4-31b persistent shared-pool 429; inkling 403 harness-gated; ultra-550b 80s slow. Code: pi auto-retries 429 exp-backoff 3x(2/4/8s) then dies (agent-session.js:1938); empty finish=length is NOT retried (openai-completions.js:674)-the real free-model stall hazard. Two ranked shortlists + exact config diff (agent_dispatch.model + harnesses.pi.allowed_models), not applied.

Parent review (L4.80 a00-e2944c23): ACCEPTED. The decisive halves a00-bfb402e9 left open are now covered: 429-as-experienced on real hammers (gemmas 429 is upstream shared pool, not account), the mid-round 429 behaviour answered from CODE with exact file:line refs (pi retries 429 3x exp backoff; the real hazard is the unretried empty finish=length stall), and both ranked shortlists plus the fail-closed allowlist config diff, not applied. Verdict inconclusive_lean_proved:65 is right: per-request availability measured, end-to-end round stability untested (needs a config change, forbidden this round).
