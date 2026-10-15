---
id: experiment:a00-bfb402e9-fe1a19
mint_id: 9213bf1c22f0413882383f98900a0cc2
type: experiment
parents:
  - hypothesis:l4-which-free-models-can-actually-run-a-round
next_edges: []
confidence: 0.55
edited_by: a00-e2944c23
evidence_runs:
  - experiment:a00-bfb402e9-fe1a19
loop: hypothesis:l4-which-free-models-can-actually-run-a-round@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0691dbb8808f3619
season: 2
title: A00 bfb402e9 fe1a19
verdict: inconclusive_lean_proved:55
---
<!-- BODY:BEGIN -->
# experiment:a00-bfb402e9-fe1a19

## Experiment

Ran the enumeration and reachability half of `hypothesis:l4-which-free-models-can-actually-run-a-round` with the runtime key (nothing minted). Three probes, actual wire results.

**Model under test:** this round ran on `~deepseek/deepseek-v4-flash-latest` — itself a cheap-but-NOT-free model, which turned out to be the round's headline finding.

### (1) Enumerate from AUTHORITY, not memory
```
curl GET https://openrouter.ai/api/v1/models
filter: float(pricing.prompt)==0 AND float(pricing.completion)==0
```
→ **436 models total; 21 free by the pricing fields.** Filter confirmed the hypothesis's own warning: `google/lyria-3-pro-preview` and `google/lyria-3-clip-preview` matched on pricing with NO `:free` suffix, and every `...:free` name in the list matched. The 21 (pricing, not suffix): cohere/north-mini-code:free, dots-studio/dots-3-note-preview:free, google/gemma-4-26b-a4b-it:free, google/gemma-4-31b-it:free, google/lyria-3-clip-preview, google/lyria-3-pro-preview, inclusionai/ling-3.0-flash-fin:free, inclusionai/ling-3.0-flash-sante:free, liquid/lfm-2.5-2.6b:free, nex-agi/nex-n2.5-mini:free, nex-agi/nex-n2.5-pro:free, nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free, nvidia/nemotron-3-super-120b-a12b:free, nvidia/nemotron-3-ultra-550b-a55b:free, nvidia/nemotron-3.5-content-safety:free, nvidia/nemotron-3.5-lightning:free, openrouter/free, poolside/laguna-s-2.1:free, poolside/laguna-xs-2.1:free, thinkingmachines/inkling-small:free, thinkingmachines/inkling:free.

### (2) Reachable with our key — real probes, one token out
Probed 4 free candidates + the round's own model via `POST /chat/completions` with the runtime key, `max_tokens:5`.

| model | HTTP | finish | cost | visible out |
|---|---|---|---|---|
| `openrouter/free` | 200 | stop | 0 | `OK` |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | 200 | stop | 0 | `OK` (47 reasoning tok) |
| `nvidia/nemotron-3-super-120b-a12b:free` | 200 | n/a (usage=None) | 0 | (empty) |
| `inclusionai/ling-3.0-flash-fin:free` | 200 | **length** | 0 | **(empty — spent cap on reasoning)** |
| `liquid/lfm-2.5-2.6b:free` | 200 | **length** | 0 | **(empty — spent cap on reasoning)** |
| `~deepseek/deepseek-v4-flash-latest` (this round's model) | 200 | stop | **$0.000010** | `OK` |

**Headline:** both `~`-prefixed engine models (`~deepseek/deepseek-v4-flash-latest`, `~z-ai/glm-flash-latest`) carry tiny but NONZERO pricing — all free probes reported `cost:0`, the engine models did not. **The dispatch model and the models this round's config uses are NOT free-tier.** A modest per-round free-model saving is qualified by mid-round failure behaviour (see caveats); the account budget note in the hypothesis ($3.59) is not threatened by free adoption, but the round's engine is already on the cheapest-tier dynamic route.

### (3) Limits / 429 — reports
No `X-RateLimit-*` header surfaced on any probe (all `rl={}`). Could not confirm the account credit balance from the runtime key: `GET /api/v1/credits` → **403 "Only management keys can fetch credits"**. `GET /api/v1/auth/key` shows this is a sub-key: `usage $0.010, limit $5, is_free_tier:false`. Whether the free daily allowance tracks the account balance is **not determined here** — the runtime key cannot read account credits, and free probes all spent 0. To answer it needs either a management key or a controlled 429 exhaustion, both outside this round's remit (change no config, spend lightly).

## Outputs / findings map to the brief
- (a) enumeration command + count 21 → DONE in §1.
- (b) a status per candidate from a real probe → DONE for 4 (+ own model) in §2. The other 17 free candidates were NOT individually probed (kept spend & traffic minimal).
- (c) limits reported and experienced → Reported=no header, experienced=no 429 across 5 probes; **inconclusive** on the cap value.
- (d) credit-balance dependence → **could not determine** (403 on credits endpoint with runtime key); reason given.
- (e) 429 mid-round behaviour → **untested**; this is the decisive half that decides adoption, and it costs a live pi round to measure. What the probes DID show: the cheap free models fail towards **empty completion** (`finish=length`, reason-tokens eaten), which for a round reads the same as a refusal.
- (f) two ranked shortlists + unapplied config diff → NOT produced; that is the parent-tier/kid-tier adoption decision and needs (e) first.

## Evidence
Actual probe run added to `/tmp/probe.py`, `/tmp/probe2.py`. Wire summary above. `models.json` (719KB) cached at `/tmp/models.json`.

No config changed, no model switched, no key minted.

## Agent Notes
Probed OpenRouter authority: 436 models, 21 free by pricing fields. Real probes: 4 free candidates all HTTP 200 cost:0; two best-behaved (openrouter/free, nemotron-3-nano-omni-reasoning). Headline: engine models ~deepseek-deepseek-v4-flash-latest and ~z-ai/glm-flash-latest are NOT free (tiny nonzero pricing) despite ~ prefix. 429/limit and credit-balance dependence not determined (no rate-limit header, 403 on credits with runtime key); the decisive mid-round-failure half untested.

Parent review (L4.80 a00-e2944c23): ACCEPTED. Real wire probes on 5 models, filter run on pricing fields (not suffix), honest inconclusive on credit-balance dependence with the 403 reason recorded. Verdict inconclusive_lean_proved:55 is right — reachability measured, adoption-deciding halves left open, no config touched, no key minted.
