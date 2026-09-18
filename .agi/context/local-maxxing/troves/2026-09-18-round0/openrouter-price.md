# TROVE: OpenRouter price today — openrouter-price
date: 2026-09-18 (UTC ~05:21Z)
mode: READ-ONLY, curl -sL public, no key, no install, no clone
tag: MEASURED = quoted from a page/file I read; ESTIMATE = arithmetic shown.
## Page 1 — OpenRouter model catalog API (public, no key)
URL: https://openrouter.ai/api/v1/models  (fetched 2026-09-18T05:21Z, HTTP 200)
MEASURED: total_count=445 models, links.next=null.
Pricing fields are USD **per token**; multiply by 1e6 for per-1M-token.
MEASURED rows (id | name | context | $/1M prompt | $/1M completion | $/1M cache-read):
- deepseek/deepseek-v4-flash | DeepSeek V4 Flash 0423 | ctx 1,048,576 (top_provider 1,024,000, max_completion 384,000) | in 0.088606 | out 0.177212 | cache 0.0177212
- deepseek/deepseek-v4.1-flash | DeepSeek V4.1 Flash | ctx 1,048,576 (max_completion 384,000) | in 0.15 | out 0.60 | cache 0.003
    - MEASURED time-of-day overrides (utc_days/utc_start/utc_end): weekday 100-400 and 600-1000 UTC -> in 0.30 / out 1.20 / cache 0.006 (DOUBLE); all other windows (incl. weekends) -> 0.15 / 0.60 / 0.003.
- deepseek/deepseek-v4-flash-0731 | DeepSeek V4 Flash 0731 | ctx 1,310,720 (max_completion 943,718) | in 0.06 | out 0.12 | cache 0.012
- deepseek/deepseek-v4-pro | DeepSeek V4 Pro 0423 | ctx 1,048,576 | in 0.94336 | out 1.88672 | cache 0.079596
- qwen/qwen3.8-27b | Qwen3.8 27B | ctx 1,000,000 (top_provider 262,144, max_completion 131,072) | in 0.214 | out 2.55 | cache 0.15
- qwen/qwen3.8-flash | Qwen3.8 Flash | ctx 1,000,000 (max_completion 131,072) | in 0.15 | out 0.47 | cache 0.016 (+ cache-write 0.20)
- qwen/qwen3.8-max-0902 | Qwen3.8 Max (0902) | ctx 1,000,000 | in 2.00 | out 6.00 | cache 0.25
- qwen/qwen3.8-2.4t-a95b | Qwen3.8 2.4T A95B | ctx 1,048,576 | in 2.00 | out 6.00 | cache 0.25
- qwen/qwen3.5-35b-a3b | Qwen3.5-35B-A3B | ctx 262,144 (max_completion 65,536) | in 0.1625 | out 1.30 | cache n/a
- qwen/qwen3.5-27b | Qwen3.5-27B | ctx 262,144 | in 0.195 | out 1.56 | cache n/a
- qwen/qwen3.5-9b | Qwen3.5-9B | ctx 262,144 (max_completion 235,929) | in 0.10 | out 0.15 | cache n/a
- qwen/qwen3-8b | Qwen3 8B | ctx 131,072 (max_completion 8,192) | in 0.117 | out 0.455 | cache n/a
- qwen/qwen3.5-122b-a10b | Qwen3.5-122B-A10B | ctx 262,144 | in 0.26 | out 2.08 | cache n/a
- qwen/qwen3.5-397b-a17b | Qwen3.5 397B A17B | ctx 262,144 | in 0.55 | out 3.50 | cache 0.225
MEASURED: NO model id contains "qwen3.8-50b" or a 50B-class qwen3.8. Nearest qwen3.8 sizes in catalog:
27B (0.214/2.55), Flash (0.15/0.47), Max (2.00/6.00), 2.4T-A95B (2.00/6.00).
=> "qwen3.8 50b" is NOT an OpenRouter-hosted id today; likely either Qwen3.5-35B-A3B (MoE, 3B active) or Qwen3.8-27B.
## Page 2 — Private Models ("bring your own model") 
URL: https://openrouter.ai/docs/guides/routing/private-models.md (fetched 2026-09-18T05:2xZ)
MEASURED quotes:
- "Private Models are available for Enterprise Plan customers." (Note block)
- "Private Models let you route to your own custom, fine-tuned, or dedicated model endpoints through OpenRouter"
- "Your private models and endpoints are only visible to the users and organizations you approve, and they will never show up in public model lists, rankings, search, charts, and benchmarks."
- "A private endpoint must meet two requirements: It is hosted by a provider that OpenRouter supports for BYOK ... It serves a model that already exists in the OpenRouter catalog, with the same request and response shape ... The private endpoint inherits the model's slug and capabilities."
- "Organization admins on the Enterprise Plan can add private endpoints themselves from Settings > Private Endpoints"
- "Each organization can have up to 10 private endpoints by default."
- Endpoint wizard 4 steps: Blueprint -> Connect (HTTPS base URL + upstream model/deployment ID, set pricing, declare retention) -> Test (BYOK key) -> Activate.
=> ANSWER: a private endpoint / BYO model CAN be listed and routed on OpenRouter, but ONLY on the Enterprise Plan, must be OpenAI-compatible, must shadow a catalog model (inherits its slug), max 10 endpoints, and auth uses your own BYOK provider key per workspace. Not a route for a tiny self-hosted model on the free/PAYG tier.
## Page 3 — BYOK ("bring your own provider API keys")
URL: https://openrouter.ai/docs/guides/overview/auth/byok.md (fetched 2026-09-18T05:2xZ)
MEASURED quotes:
- "The cost of using custom provider keys on OpenRouter is 5% of what the same model/provider would cost normally on OpenRouter and will be deducted from your OpenRouter credits."
- Free allowance (list-price inference cost, not request count): PAYG = $25,000/month, Enterprise = $200,000/month (constants BYOK_FEE_PERCENTAGE='5', BYOK_PAYG_MONTHLY_LIST_PRICE_THRESHOLD_USD='$25,000').
- "OpenRouter always prioritizes BYOK endpoints first, regardless of where that provider appears in your specified order." (order still controls fallback after BYOK exhausted.)
=> ESTIMATE: BYOK gives a 5% surcharge on top of your own provider bill for a provider OpenRouter already supports; irrelevant for models OpenRouter does not host at all (that needs Private Models, Page 2).
## Page 4 — Provider Routing
URL: https://openrouter.ai/docs/features/provider-routing (fetched 2026-09-18T05:2xZ)
MEASURED: default strategy is "Price-Based Load Balancing ... By default, requests are load balanced across the top providers to maximize uptime."
provider object fields (MEASURED, quoted types/defaults):
- order: string[] (provider slugs, tried in order)
- allow_fallbacks: boolean, default true
- only: string[] (allowlist; account-wide allowlist acts as ceiling; mismatch -> 404)
- ignore: string[] (denylist; merged with account-wide ignored)
- sort: "price" | "throughput" | "latency" (or object) — setting sort/order disables load balancing
- quantizations: string[] (e.g. ["int4","int8"]), require_parameters, data_collection, zdr, enforce_distillable_text, max_price
- "Targeting Specific Provider Endpoints / Base Slug Matching" exists, incl. variants like "/turbo".
=> Tiny-model relevance: you CAN pin one cheap provider with provider.only + allow_fallbacks=false, and filter by quantizations (int4/int8) — useful to keep a round on CPU-cheap endpoints and off expensive ones.
## Arithmetic — kid session cost (ESTIMATE, formula shown)
Shape (owner): 20,000 input + 5,000 output tokens per call, 40 calls.
= 40*20,000 = 800,000 input tokens = 0.800M ; 40*5,000 = 200,000 output = 0.200M.
session_usd = 0.800*price_in_per_1M + 0.200*price_out_per_1M.
$/1M OUTPUT column = price_out_per_1M (MEASURED*1e6).
| model | $/1M in | $/1M out | session USD |
|---|---|---|---|
| deepseek-v4-flash | 0.0886 | 0.1772 | 0.1063 |
| deepseek-v4.1-flash (off-peak) | 0.15 | 0.60 | 0.2400 |
| deepseek-v4.1-flash (peak wkday 100-400/600-1000Z) | 0.30 | 1.20 | 0.4800 |
| deepseek-v4-flash-0731 | 0.06 | 0.12 | 0.0720 |
| qwen3.8-27b | 0.214 | 2.55 | 0.6812 |
| qwen3.8-flash | 0.15 | 0.47 | 0.2140 |
| qwen3.8-max-0902 | 2.00 | 6.00 | 2.8000 |
| qwen3.8-2.4t-a95b | 2.00 | 6.00 | 2.8000 |
| qwen3.5-35b-a3b | 0.1625 | 1.30 | 0.3900 |
| qwen3.5-27b | 0.195 | 1.56 | 0.4680 |
| qwen3.5-9b (7-9B class) | 0.10 | 0.15 | 0.1100 |
| qwen3-8b (7-9B class) | 0.117 | 0.455 | 0.1846 |
| qwen3.5-122b-a10b | 0.26 | 2.08 | 0.6240 |
| qwen3.5-397b-a17b | 0.55 | 3.50 | 1.1400 |
READ: cheapest 7-9B-class session = qwen3.5-9b at $0.110; cheapest overall = deepseek-v4-flash-0731 at $0.072.
deepseek-v4.1-flash is 2-4x its own sibling v4-flash on output (0.60 vs 0.177) — and doubles again in two weekday UTC windows.
## Page 5 — OpenRouter Pricing (plans)
URL: https://openrouter.ai/pricing (fetched 2026-09-18T05:2xZ)
MEASURED: Platform fees — Free: N/A; Standard (PAYG): 5.5%; Business (PAYG): 8%; Enterprise: fee discounts available.
MEASURED BYOK limits — Free: No BYOK; Standard: "$25,000 of list price inference / month with no fees, 5% fee after"; Business: same $25,000; Enterprise: "$200,000/month with no fee, 5% after".
MEASURED rate limits — Free: 50 requests/day; Standard/Business: passthrough from the provider(s); Enterprise: higher allowances.
MEASURED: Free tier = 25+ free models, 4 free providers, no prompt caching, no management API key.
=> ESTIMATE: 5.5% platform fee applies on top of catalog per-token prices for PAYG (the numbers in Page 1 appear to be the list prices; fee is separate). For our 40-call kid session this is +5.5% on the tiny totals below, i.e. still < $0.12 for the cheapest model.
## Page 6 — Web: does a "Qwen3.8 50B" exist? 
Sources (fetched 2026-09-18T05:2xZ via web search, MEASURED quotes):
- HF model card "Qwen/Qwen3.8-27B": "Number of Parameters: 27B - Hidden Dimension: 5120" (https://huggingface.co/Qwen/Qwen3.8-27B)
- Qwen blog "Qwen3.8-Max": "Qwen 3.8-Max scales to 2.4 trillion parameters" (https://qwen.ai/blog?id=qwen3.8)
- HF "Qwen/Qwen3.8-Flash-Next": MoE, "125B total parameters and only 6B activated per token" (https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
=> RESOLUTION: there is NO Qwen3.8 50B. The Qwen3.8 family is 27B (dense), Flash (125B total / 6B active MoE), Max (2.4T). "50B-class" likely refers to Qwen3.5-35B-A3B (MoE, 3B active) or the owner means Qwen3.8-27B. Candidate id to use: qwen/qwen3.8-27b or qwen/qwen3.5-35b-a3b.
## WALL / method notes
- Pages read (>=5): (1) /api/v1/models JSON, (2) private-models.md, (3) byok.md, (4) provider-routing (HTML+.md), (5) /pricing, (6) web search on Qwen3.8 sizes. All curl -sL public, no key, no install, no clone. READ-ONLY.
- Every catalog price above is MEASURED (raw per-token strings from the JSON, multiplied by 1e6); every session total is ESTIMATE (arithmetic shown).
- Anonymized: no host names/IPs/hardware of our boxes, no location, no key ids.
