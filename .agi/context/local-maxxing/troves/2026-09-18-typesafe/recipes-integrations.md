# TypeSafe / jev — recipes, integrations, SDKs, latency
reader: recipes-integrations kid (a00-bb925977), read 2026-09-17 by `curl -sL` + tag strip.
Every claim below carries a URL; `MEASURED` = quoted from the page, `ESTIMATE` = my arithmetic/derivation. Pages have no own date stamp except SDK changelog.

## Sources read
44 distinct pages fetched (all 200), docs.typesafe.ai unless noted:
- index `https://docs.typesafe.ai/llms.txt`; `https://docs.typesafe.ai/`; `https://docs.typesafe.ai/sdk/`
- `api.md`, `models.md`, `legal.md`, `agent-skill.md`, `migrating-to-v1.md`, `confidence.md`, `primitives.md`, `primitives/advanced.md`
- skill README `https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md`
- concepts: `system-one.md`, `state.md`, `how-to-build-with-system-one.md`, `use-case-map.md`
- patterns: `patterns.md`, `fan-out.md`, `confidence-routing.md`, `composite-scoring.md`, `intent-routing.md`
- demos: `demos.md`, `demos/smart-home.md`; intro: `introduction/quickstart.md`, `introduction/machine-learning-primer.md`; `model-jaggedness/jev-1.13.md`
- SDK: `sdk.md`, `sdk/python.md`, `sdk/python/usage.md`, `sdk/python/api.md`, `sdk/python/changelog.md`, `sdk/javascript.md`, `sdk/javascript/api.md`,
  `sdk/python/api/clients/sync/client.md`, `sdk/python/api/clients/async/client.md`, `sdk/python/api/types/questions.md`, `sdk/python/api/types/responses.md`,
  `sdk/python/api/retries.md`, `sdk/python/api/exceptions.md`, `sdk/python/api/constants.md`, `sdk/python/api/clients/sync/models.md`,
  `sdk/javascript/api/classes/TypeSafeClient.md`, `sdk/javascript/api/functions/choice.md`
- cookbooks (18): `consistency_noul`, `consistency_choice`, `parallel_questions`, `rerank_typesafe`, `semantic_find`, `autoformat`, `function_calling`,
  `skill_suggestion`, `entity_alignment`, `classifying_rag_passages`, `citation_check`, `llm_guardrails`, `sde_cascade`, `date_extraction`,
  `pre_parsed_value_extraction`, `hierarchical_classification`, `autoresearch_feature_discovery`, `classification_using_confidence` (all under `/cookbooks/<name>.md`).
- No page found that had *fewer* than 12 sources; MCP/streaming/latency-p50 have no page at all (below).

## Recipes and worked examples
Four published architectural patterns, each with runnable code shape (`/patterns.md`):
- **Speculative fan-out** (`/patterns/fan-out.md`): ask all questions in one call, ignore irrelevant answers. MEASURED: "adding more questions to a call typically doesn't add any latency."
- **Confidence-gated routing** (`/patterns/confidence-routing.md`): MEASURED code `if action.confidence < 0.6: route_to_support_agent(...)`, then `elif action.choice == "approve_transfer": if action.confidence > 0.85: approve_transfer(...)`. Thresholds 0.6 / 0.85 are example constants.
- **Composite scoring** (`/patterns/composite-scoring.md`): independent `score` questions per dimension, weights in code. Resume example: `python_depth`, `team_leadership`, `system_design`, `generalist`, each a 5-level score.
- **Intent routing** (`/patterns/intent-routing.md`): one `choice` (`intent` ∈ order_status/product_question/return_exchange/complaint) + one `score` (`complexity`); route on `intent.choice`, escalate on `complexity.confidence < 0.5`.

18 cookbooks, each a full notebook with code + cached outputs. The ones worth quoting for the town:
- `parallel_questions` — 13 questions on the GDPR article, one call vs 13. MEASURED table: one call `$0.000497 / 0.27s`; 13 calls `$0.006090 / 2.71s`; "12.2x cheaper, 10.0x faster". Answers unchanged (std 0.0 for choices/scores/6-of-8 nouls). (Note: `/primitives.md` quotes the same experiment as "11.5x cheaper and 9.6x faster" — doc inconsistency.)
- `rerank_typesafe` — 40 CLERC legal queries, 30-passage BM25 shortlists, one question per query-candidate pair; MEASURED top-1 5%→18%, top-10 38%→62%. Code reads `stream = load_dataset(...)` — that "stream" is HF dataset streaming, not an API mode.
- `semantic_find` — score 218 line ids against a query with a Choice, one Noul "does the doc contain an answer".
- `autoformat` — rebuild Markdown in 2 requests; pass1 16 questions `0.32s`, pass2 62 questions `0.51s`; MEASURED printed total `0.8s` (page then says "$0.0015" in prose after printing `$0.0003` — internal inconsistency).
- `hierarchical_classification` — GM of Choice probabilities + width-K beam search in code (patent/retail/biomedical/code taxonomies); "extra exploration adds little [latency]" because each frontier is parallel questions. Uses `beam_width` (seen in `extra_body={"beam_width": 4}` in `/sdk/python/usage.md`).
- `function_calling`, `skill_suggestion` (182 Hermes skills), `entity_alignment` (450 pairs, one Score of merge/leave/curate), `classifying_rag_passages`, `citation_check`, `llm_guardrails`, `sde_cascade`, `date_extraction`, `pre_parsed_value_extraction`, `autoresearch_feature_discovery`, `classification_using_confidence`, `consistency_noul`, `consistency_choice`.
- `smart-home` demo (`/demos/smart-home.md`): fan-out long question list; a Noul splits a compound request, then an LLM splits into atomic commands; TypeSafe "adds negligible latency" vs the LLM fallback.

Question JSON shape is identical in every recipe: `{"questions": {"<id>": {"type": "choice|score|noul", "instructions": <str|obj|arr>, "criteria": <map|array|{true,false}>}}}`, answers keyed by the same id (`/api.md`).

## SDKs
- **Python** (`typesafe-sdk`, `uv add typesafe-sdk` / `pip install typesafe-sdk`): `TypeSafeClient.system_one(state, questions, *, model=None, retry=None, timeout=None, extra_headers=None, extra_body=None) -> SystemOneResponse`; `client.models.list()`; `client.close()`; sync context manager. `AsyncTypeSafeClient` mirrors it with `await client.system_one(...)`, `await client.models.list()`, `await client.aclose()`, `async with`. MEASURED from `/sdk/python/api/clients/{sync,async}/client.md`.
  - Question classes `Noul`, `Choice`, `Score` (plus `NoulModel`/`ChoiceModel`/`ScoreModel` dict forms); answers read as `result.nouls[...]`, `result.choices[...]`, `result.scores[...]`, `result.usage.input_tokens/output_tokens`, `result.raw_http_response` (`/sdk/python/api/types/{questions,responses}.md`).
  - Env vars `TYPESAFE_API_KEY`, `TYPESAFE_BASE_URL` (default `https://api.typesafe.ai`), `TYPESAFE_DEFAULT_MODEL` (`jev-latest`), `TYPESAFE_LOG_LEVEL`; `DEFAULT_TIMEOUT = 10.0` (`/sdk/python/api/constants.md`).
  - Forward-compat escape hatches: `extra_body` (e.g. `{"beam_width": 4}`), raw question dicts for unmodeled fields, unknown answer kinds skipped + warning, `raw_http_response` (`/sdk/python/usage.md`).
  - Changelog MEASURED: v0.5.7 initial public release **2026-09-14**, v0.6.0 **2026-09-15** (Score.criteria now an ordered sequence) — the SDK is ~3 days old (`/sdk/python/changelog.md`).
- **JavaScript/TS** (`@typesafe-ai/sdk`, `npm install`, Node ≥20, ESM+CJS+`.d.ts`): `new TypeSafeClient(config?)`, `client.systemOne<Q>(request, options?) -> APIPromise<SystemOneResult<Q>>`, `client.models.list()`; properties `baseURL`, `defaultHeaders`, `defaultModel`, `fetch`, `logger`, `logLevel`, `models`, `retry`, `timeout`; helpers `noul()`, `choice()`, `score()`; error classes incl. `APIUserAbortError`, `RateLimitError`, `UnprocessableEntityError` (`/sdk/javascript.md`, `/sdk/javascript/api/classes/TypeSafeClient.md`, `/sdk/javascript/api/functions/choice.md`).
- **Batching helpers:** none beyond "put every question in one `questions` map" — no `batch()`/`parallel()` SDK method exists in either SDK's reference (`/sdk/python/api.md`, `/sdk/javascript/api.md`).
- **Retries:** default `RetryPolicy(max_retries=3, timeout=10.0, http_statuses={429,500,502,503,504})`, exponential backoff with `backoff_initial`/`backoff_max`/`backoff_jitter`; honors `retry-after`; `TypeSafeRateLimitError.retry_after_ms` (`/sdk/python/api/retries.md`, `/sdk/python/api/exceptions.md`, `/models.md`).

## Agent and MCP integrations
- **Agent skill: YES** — a drop-in SKILL.md for Claude Code / Codex / other agents (`/agent-skill.md`). Install: `claude plugin marketplace add typesafe-ai/skills` + `claude plugin install typesafe@typesafe-ai`, or `npx skills add typesafe-ai/skills --skill typesafe-ai` (project-local, `-g` global). Update: `claude plugin marketplace update typesafe-ai` + `claude plugin update typesafe@typesafe-ai`, or `npx skills update`.
- **MCP server: ABSENT.** No `mcp` token in `/llms.txt`, `/agent-skill.md`, `/sdk.md`, or any page read; no "Model Context Protocol" string anywhere.
- **LangChain / LlamaIndex / CrewAI / Vercel-AI-style adapter: ABSENT.** No such token on any page read; the only integration surface is the HTTP API + two SDKs + the agent skill.
- MEASURED caveat from `/agent-skill.md`: "Agents aren't great at writing questions, so expect to edit collaboratively"; put questions/thresholds in one reviewable file.

## Streaming
**ABSENT.** No streaming/SSE/chunked response mode exists in `/api.md` (response is one complete JSON `{model, answers, usage}`), and neither SDK reference lists a stream method (`/sdk/python/api.md`, `/sdk/javascript/api.md`). The word "stream" appears only as HF dataset streaming and "downstream". If the town wants incremental probabilities it must poll or accept whole-response latency.

## Latency numbers
Published, quoted (all docs pages are undated except changelog; read 2026-09-17):
- `/cookbooks/consistency_noul_cookbook.md` MEASURED: TypeSafe mean round-trip **111 ms**; LLM conditions **1.1–13.9 s**.
- `/cookbooks/consistency_choice_cookbook.md` MEASURED: TypeSafe mean round-trip **114 ms**; LLM conditions **826 ms–13.0 s**.
- `/cookbooks/parallel_questions.md` MEASURED: 13 questions in one call **0.27 s** vs 13 separate calls **2.71 s** (summed, sequential); **12.2x cheaper / 10.0x faster**.
- `/cookbooks/autoformat.md` MEASURED: 16 q in **0.32 s**, 62 q in **0.51 s**, total **0.8 s**, 10,211 tokens.
- `/concepts/use-case-map.md` marketing claim: "Frontier intelligence at real-time speeds (**150ms**)"; "100x cheaper… process giant datasets" (ESTIMATE/marketing, not a measured table).
- `/patterns/fan-out.md` MEASURED: adding questions "typically doesn't add any latency."
- SDK default timeout 10.0 s (`/sdk/python/api/constants.md`).
- **p50/p95 by primitive or state size: ABSENT** on every page read. No state-size latency curve; `models.md` rate limits are the closest capacity number.

## Fit for the town
Maps onto the 6 sites on `idea:lm-typed-decisions-in-the-loop` (`/home/ubuntu/work/agi/.agi/nodes/idea/lm-typed-decisions-in-the-loop.md`, 2026-09-17). Ranked by usefulness of what the docs *add*:
1. **Verdict class / evidence-present pre-check** — cookbook `consistency_noul` + `classification_using_confidence` give the exact pattern: Choice + read `answer.confidence` to decide auto vs route-to-human. The docs' own caveat (thresholds must be tuned) is the falsifier already on the idea node. Engine seam: a pre-check in the kid scaffold before `cli.py done` (a `write.py`/gate).
2. **Merge-up review triage (defect severity)** — `entity_alignment` shows the move: a 3-level Score whose levels ARE the actions (demote / residue / note). This is the strongest recipe match; no threshold to fit. Seam: the mur (`workflow.py run merge-up-review`).
3. **Confidence routing generally** — `/patterns/confidence-routing.md` 0.6/0.85 gate is a ready template for the gate that decides demote vs review.
4. **Corpus labels for the kid-persona LoRA** — `classification_using_confidence` + `consistency_choice` (label agreement vs auto-action share) give a labellable, auditable shape over the 354 examples.
5. **Dispatch guard (touches-real-resource / secret)** — Noul with `criteria.true/false`; `/api.md` shows the exact optional `criteria` shape.
6. **Comms tag / rotation stops-slot** — plain Choice over a fixed label set; cheapest, least evidence needed.
- **Cost:** docs MEASURED price `/models.md`: **$42 per Btok = $0.042 / Mtok input, output tokens free**. The idea node's owner-stated `$0.045/1M` is close but not what the docs say — ESTIMATE a 2k-token node ≈ **$0.000084** at docs price. (pricing-legal kid owns confirmation.)
- **Batch every question for one state into one call** (fan-out): the town's sites are independent questions over the same node/diff, so one `systemone` call per decision-point, not per site.
- **Rate limits** (docs MEASURED, `/models.md`): 250,000 tok/s and **1,200 req/min**, dynamically adjusting; `429` over either.
- **Context** (docs MEASURED): 64k tokens/request (32k for `state` + longest question); text-only — so a full node body fits without chunking.
- **No streaming and no MCP** means the town integrates via an HTTP/SDK adapter, not a tool server; the three-day-old SDKs mean pin or vendor rather than assume stability.
