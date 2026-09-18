# TypeSafe — RECIPES / EXAMPLES / SDKs / INTEGRATIONS (Slice 2)
Read-only digest, 2026-09-18Z. Docs: docs.typesafe.ai (index llms.txt) + github.com/typesafe-ai/skills. No API key used.
MEASURED = quoted from a page read here (all fetched this session, 2026-09-18). ESTIMATE = my arithmetic.
Pages read (distinct, 25): llms.txt; README.md; skills/typesafe-ai/SKILL.md; introduction/quickstart; patterns; patterns/fan-out; patterns/confidence-routing; patterns/composite-scoring; patterns/intent-routing; concepts/how-to-build-with-system-one; concepts/use-case-map; agent-skill; sdk; sdk/python; sdk/javascript; api; models; confidence; cookbooks/{skill_suggestion,function_calling,parallel_questions,sde_cascade,llm_guardrails,autoresearch_feature_discovery,rerank_typesafe}; demos/smart-home; migrating-to-v1. 3 probes 404 (below).

## 1. RECIPES / WORKED EXAMPLES (all pages list code + a cached `json_cache.json` so numbers replay without API spend — MEASURED)
- **Parallel questions** (batch): 13-question GDPR briefing on ~54k-char doc. "batching every question into one TypeSafe call is 12.2x cheaper and 10.0x faster with no change in answers" (MEASURED). Most answers identical across 5 repeats, std dev 0.0.
- **Re-ranking**: 30-passage BM25 shortlists, 40 CLERC queries. "raise top-1 accuracy from 5% to 18% and top-10 accuracy from 38% to 62%" (MEASURED). 1 question per query-candidate pair.
- **Skill suggestion** (agent integration): pick ≤1 skill from Hermes' 182. 488 requests vs claude-haiku-4-5. Wrong-skill loads 16.8%→7.3%; loads-one-when-none-fits 9.8%→4.0%; floor (handed right answer) 2.5%/1.2% (MEASURED). Two calls: call1 ranks all 182 + nouls "need a skill at all?"; call2 re-reads top-3 full text, may reject all.
- **Function calling**: NL trading request → typed fn + enum args + confidence. Closed sets read from Python `Literal` types: choice / set (`list[Literal]`) / flag (bool). "whatever reaches the function is a value the function accepts" (MEASURED). Own `Dispatcher`, not provider tool-calling.
- **SDE cascade**: rung0 mini (gpt-5.4-mini $0.75/$4.50) → **verify each field with jev Noul P(wrong)** → escalate to gpt-5.5 ($5/$30) if any field P(wrong)>0.7. jev-1.12 $0.042/$0.00 (MEASURED).
- **Guardrails**: ONE request screens LLM input AND output; Noul battery (jailbreak/harm/diagnosis/self-harm) + Score severity → route() thresholds: pass/review/block/support (MEASURED).
- **Autoresearch feature discovery** (eval loop): LLM proposes TypeSafe questions → answers become numeric CatBoost features → model errors feed next proposal. RMSE on 800 held-out wine reviews: mean 3.09 → word-counts 2.47 → ask-TypeSafe-for-score 2.15 → 18 questions 1.87 → 38 questions after 5 rounds **1.77** (MEASURED).
- Others (index only, not fetched in full): line-by-line semantic search (218 line-ids/request), structure recovery (2 requests), entity alignment (450 pairs, Score levels = merge/unlink/curator), RAG passage classification, citation double-check, date extraction, pre-parsed value extraction, hierarchical classification (beam search over Choice probs), classification-using-confidence (75 SEC industry groups), consistency cookbooks (route uncertain to human).
- **Patterns**: speculative fan-out; confidence-gated routing; composite scoring (atomic scores + code-owned weights); intent routing (deterministic / specialist LLM / human).

## 2. SDKs & LANGUAGES
- **Python** `typesafe-sdk` (`pip install` / `uv add`), AsyncTypeSafeClient + TypeSafeClient, typed `Noul/Choice/Score` objects; helpers pkg `cooksafe`; some cookbooks need `--extra-index-url https://pypi.typesafe.ai/` and pin `typesafe-sdk>=0.5.7` (MEASURED).
- **JavaScript/TypeScript** `@typesafe-ai/sdk`, Node 20+, `npm install`; `choice()`/`noul()`/`score()` functions, answers inferred from questions; ships ESM+CJS+`.d.ts` (MEASURED).
- **REST**: `POST https://api.typesafe.ai/v1/systemone`, Bearer key, `model:"jev-latest"`; request `{state, model, questions{id:{type,instructions,criteria}}}` → `{model, answers{id:…}, usage{input_tokens,output_tokens}}` (MEASURED). Errors 401/422/429/529; SDKs auto-retry with backoff honoring `retry-after`.
- Key minted at console.typesafe.ai; env var `TYPESAFE_API_KEY`; optional `TYPESAFE_ENDPOINT` (MEASURED).

## 3. AGENT / MCP / TOOL-CALLING INTEGRATIONS
- **No MCP server exists in the public docs.** `docs.typesafe.ai/mcp.md`, `/integrations.md`, `/mcp-server.md` all **404** (MEASURED 2026-09-18). So any "jev MCP" is OUR wrapper, not theirs.
- Agent integration = **Agent Skill**: `claude plugin marketplace add typesafe-ai/skills` + `claude plugin install typesafe@typesafe-ai`, or `npx skills add typesafe-ai/skills --skill typesafe-ai` (project-local default, `-g` global). Repo tree = LICENSE + README + `.claude-plugin/{plugin,marketplace}.json` + `skills/typesafe-ai/SKILL.md` only (MEASURED).
- SKILL.md instructs the agent to **read live docs at task time** (llms.txt index, append `.md` to any page) rather than trust the skill text; routing table by task; "keep control flow, deterministic rules, and side effects in code" (MEASURED).
- Tool calling is a **cookbook pattern**, not a native feature: closed-set args → Choice questions, name selection → Choice, then code invokes the real function (MEASURED, function_calling).

## 4. STREAMING vs BATCH
- **No streaming** (no SSE/websocket/chunked mode anywhere in index or api.md; api.md documents a single JSON response — MEASURED absence).
- **Batch = fan-out in one request.** One `state`, N questions evaluated independently in parallel; batching adds no noise (12.2x/10.0x above). 64k-token budget = state + ALL questions; 32k = state + longest single question (MEASURED, models.md). Rate limits 250,000 tok/s and 1,200 req/min (MEASURED). "Most queries complete in about 100 ms" (MEASURED, how-to-build); use-case map says "150ms" (MEASURED). Input text-only.
- Models: jev-1.13.0, $42/Btok in ($0.042/Mtok), **output tokens free**; `jev-latest` alias (MEASURED). Context 64k.

## 5. EVALUATION GUIDANCE
- Confidence 0–1 derived from the Choice/Score probability distribution (Noul has none); 3 ranges = act / caution / route-to-human (MEASURED, confidence.md).
- Self-consistency cookbooks measure label agreement; jaggedness page lists known jev-1.13 failure edges (MEASURED).
- Autoresearch loop is the built-in "improve over time" eval recipe (RMSE table above).
- Replay discipline: every cookbook caches calls in `json_cache.json` and "re-running replays the published numbers instead of calling the API; delete that file to run live" (MEASURED) — a ready-made deterministic test harness.

## 6. CHAINING DECISIONS (pre/post pipelines)
- Pre: guardrail screen input → route; BM25 fast search → rerank; code extracts candidates → jev selects span; LLM proposes questions → jev scores them.
- Post: verify extracted fields → escalate; guardrail screen output; composite-score combine weights in code; citation check after generation.
- Decision always returns to **code** (`if` on probability/confidence); model never picks its own next action (MEASURED, how-to-build: "It does not generate code or choose its own next action").

## 7. PRICING/COST DATAPOINTS (for the town)
- jev input $0.042/Mtok, output $0.00 (MEASURED). ESTIMATE: one 2k-token state + 5 questions ≈ 2.5k in ≈ $0.000105; 10k such calls ≈ $1.05.

## HYPOTHESIS SEEDS (owner threads; each with falsifier + replay test)
- **H1 three-layer jev-MCP sandwich.** jev BEFORE an MCP tool call suggests the action (function_calling closed sets → Choice/noul); jev AFTER the MCP result reads {pre-inputs + tool result} and dispatches the next suggestion; mature to auto-dispatch with 10–60 s undo. *Falsifier:* on a replayable tool-call log, post-layer next-action suggestion accuracy ≤ the harness's own default policy, or auto-dispatch within 60 s undo produces ≥1 unrecoverable side effect. *Replay test:* cache the MCP calls in `json_cache.json`; re-run the sandwich offline and compare suggested action vs logged human action (precision/recall), zero API spend.
- **H2 live transcript view with call suggestions.** Stream the agent transcript into one fan-out jev call per turn (noul "is a tool needed?" + Choice over the tool roster), render the suggestion beside the live turn. *Falsifier:* suggestion wrong-load rate not better than the 7.3% skill-suggestion baseline on our own roster, or added latency >150 ms/turn breaks the view. *Replay test:* record N real transcripts, replay through the two-call rank→verify pipeline, measure wrong-load and no-op load rates vs agent-alone baseline.
- **H3 fan-out economics for the engine.** Replace K separate kid classification calls with ONE batched jev call. *Falsifier:* answers differ from K-single calls beyond cached std-dev (expect 0.0) or 64k budget forces state truncation that changes answers. *Replay test:* same questions both ways on a pinned state, compare distributions.
- **H4 cascade with jev as verifier.** Small local model extracts; jev Noul P(wrong) per field; escalate only on fire. *Falsifier:* jev verifier adds no accuracy over small-model-alone at equal cost, or fires on >X% of correct fields. *Replay test:* cached extractor outputs, vary FIRE_T, plot quality/cost.
- **H5 confidence-gated auto-dispatch.** Only auto-run engine actions when jev confidence ≥ T. *Falsifier:* at chosen T, error rate not below manual-review baseline. *Replay test:* labelled past decisions, sweep T, report precision at each.

## GAPS / NOT DONE
- No MCP integration page exists (3× 404) — if the owner wants jev-as-MCP, it is our build.
- Did not fetch in full: use-case-map details, consistency/entity/date/autoformat/citation cookbooks, jaggedness, ML primer, JS API reference, playground. Pricing page (blog) not read; $0.042/Mtok taken from models.md + cookbook constant.
