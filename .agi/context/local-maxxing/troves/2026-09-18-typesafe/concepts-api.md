# TypeSafe / jev — CONCEPTS + API REFERENCE digest (slice 1)
Read 2026-09-17 22:1x–22:2xZ. READ-ONLY, public docs, no API key used. Every number MEASURED (quoted) unless tagged ESTIMATE.
Sources read (distinct pages, 10 so far): https://typesafe.ai (home, 2026-09-17) ; https://github.com/typesafe-ai/skills raw README ; raw skills/typesafe-ai/SKILL.md ; https://docs.typesafe.ai/api.md ; /confidence.md ; /concepts/system-one.md ; /concepts/state.md ; /models.md ; /introduction.md ; /sdk.md — all docs pages fetched 2026-09-17.

## 1. What it is (concepts)
- MEASURED (home): "We took the opposite research direction not chat" — RLHF "creates inherent issues such as mode dropping, overconfidence, and lack of reliability." TypeSafe trains "System One Models, to be natively used by machines... a new architecture, a new sampler, and a new training algorithm: Reinforcement Learning for Calibrated Decisions (RLCD)."
- MEASURED (home): "Decisions, not strings — Typed outputs that software can act on." "Hallucinations — Zero Hallucinations. Every Jev decision comes with a confidence estimate."
- MEASURED (system-one.md): "System One models are trained for calibrated decisions: their probabilities are optimized against outcomes to reflect uncertainty. **Calibration is measured across groups of predictions; it does not guarantee that an individual answer is correct.**"
- MEASURED (system-one.md): System One models "do not write replies, produce code, or generate explanations of their reasoning."
- MEASURED (system-one.md): name from Kahneman *Thinking, Fast and Slow*: System 1 = fast/intuitive.
- MEASURED (introduction.md): "Every question is evaluated in parallel and in isolation against the same state in one go. Adding questions barely changes the response time. Each question is evaluated independently, so adding more questions does not create context-rot."
- MEASURED (introduction.md): guidance — each question should be "a gut-check determination... the kind of judgment a highly knowledgeable person could make in a few seconds"; decompose multi-factor judgments into atomic questions and combine in code.
- MEASURED (models.md): "Jev is not fine-tuned or LoRA-adapted with customer data... the same weights serve every account." Domain shape comes from state + instructions/criteria only.
- MEASURED (models.md): "Jev is not trained on customer requests or responses." ZDR for enterprise.

## 2. The model (versioning, aliases, price, limits)
- MEASURED (models.md): current model **Jev 1.13** = id **`jev-1.13.0`**.
- MEASURED: price **$42 / Btok** = **$0.042 / Mtok** input; **output tokens are free**.
- MEASURED: rate limits **250,000 tokens/second** and **1,200 requests/minute**; over either → `429`.
- MEASURED: **64k tokens/request**; **32k tokens for `state` plus the longest question**.
- MEASURED: text only — string, JSON object, or array of text values; "No image, audio, or video input."
- MEASURED aliases: `jev-latest` → `jev-1.13.0` ("most recent stable, official release", SDK default); `jev-preview` → also `jev-1.13.0` (no preview build right now).
- MEASURED versioning risk: "An alias moves when a new release ships, so the answers behind it can change without a change on your side." Response `model` field reports the versioned ID that answered → log it. "If you have tuned confidence thresholds against a specific version, pin that version's ID."
- MEASURED (models.md Warning): "Rate limits are adjusting dynamically... can change without notice"; higher limits on custom/enterprise.
- MEASURED: `GET /v1/models` returns aliases with description + release_date; versioned IDs accepted even if not listed.
- MEASURED (models.md): language support — English primary/best; "other languages, including CJK scripts, are handled but not equally well."
- MEASURED (home): speed/cost demo block — TypeSafe "Cost $0.000081 Completed in 0.114s" vs LLMs "Cost $0.013880 Completed in 8.566s"; headline "193.6x Faster, 444.6x Cheaper. *based on workflows for System One tasks". These are vendor demo numbers, one workload, un-audited.

## 3. Decision types — exactly THREE (no others in the API)
MEASURED (api.md, primitives.md, llms.txt index): the only `type` values are `noul`, `choice`, `score`.
- **noul** — yes/no. Request: `type`, `instructions` (string|object|array), optional `criteria:{true:string, false:string}` ("What a yes (value near 1) means" / "What a no (value near 0) means"). Answer: `{"type":"noul","noul":0.92}` — probability the answer is yes, 0→no, 1→yes. **No `confidence`, no `probabilities`.**
- **choice** — pick one of a named set. Request: `criteria` REQUIRED = map<option, string|null> (null when no detail needed). Answer: `{"type":"choice","choice":"technical","probabilities":{"billing":0.08,"technical":0.85,"sales":0.07},"confidence":0.82}`. `probabilities` are floats summing to 1; `choice` is the argmax.
- **score** — rate along an ordered rubric. Request: `criteria` REQUIRED = ordered array of level descriptions, **at least two levels**. Answer: `{"type":"score","score":1.6,"legend":{"0":"Calm","1":"Frustrated","2":"Very angry"},"probabilities":{"0":0.05,"1":0.3,"2":0.65},"confidence":0.78}`. `score` is the probability-weighted expectation over level indices → can land between levels.
- MEASURED (advanced.md): `instructions` and all criteria fields accept JSON structure (`string|object|array|null`), e.g. `{field:{name,type,description}, extracted_value, question}` — "same shape drives a Noul, a Choice, and two Scores."
- MEASURED (primitives.md): questions in one request are **independent** — "one answer does not become context for another question"; a true dependency needs a second request (only when code must fetch new state or pick the next options).

## 4. Exact request/response schemas
Request (api.md): `{"state": string|object|array, "model": string, "questions": {‹id›: Question}}`. The question **key is not sent to the model and is not used in inference** — it is only the answer key. Response: `{"model": string, "answers": {‹id›: Answer}, "usage": {"input_tokens": int, "output_tokens": int}}`. `model` in the response is the **versioned id that answered**.
Endpoint: `POST https://api.typesafe.ai/v1/systemone`, `Authorization: Bearer <API_KEY>`, `Content-Type: application/json`. Also `GET /v1/models`.
SDKs (sdk.md): Python + JavaScript/TypeScript, typed questions/answers, automatic retries; HTTP usable from any language.

## 5. Probability / confidence semantics and calibration
- MEASURED (confidence.md): `confidence` is "a statistic computed from the probability distribution"; **only Choice and Score carry it**; Noul does not. Shape of the distribution = certainty (concentrated = confident, flat = uncertain). "you are never locked into our definition" — the full `probabilities` are always returned so you can compute your own.
- MEASURED (ml-primer.md): "Higher probability should correspond to a greater chance that the answer is correct... Outcomes assigned a probability of 0.2 should occur about 20% of the time. 0.8 → 80%. 1.0 → 100%. These rates describe **groups of predictions, not a guarantee about any single answer**."
- MEASURED (system-one.md): "Calibration is measured across groups of predictions; it does not guarantee that an individual answer is correct."
- MEASURED (confidence.md): recommended 3-band pattern — high = act; medium = proceed with caution/confirm; low = do not act/escalate. Thresholds scale with risk (examples: floor 0.5; >0.9 for destructive). "Start with conservative thresholds, test with your own data."
- MEASURED (jaggedness.md, applies to jev-1.13, last reviewed 2026-09-17): "`jev-1.13`'s score levels are weak in numerical calibration. It will not be able to help you reconstruct the exact number by interpolating between the nearest two levels." Use score expectation for threshold checks, not magnitude reconstruction.

## 6. Limits, rate limits, errors, versioning, determinism, latency
- MEASURED (models.md): **64k tokens/request**; **32k tokens for state + longest question**. MEASURED (primitives.md): question count "limited only by the request's token budget... around 32,000 tokens, roughly 150,000 characters of English text", shared with state.
- MEASURED (models.md): rate limits **250,000 tok/s** and **1,200 req/min**; over either → 429; **dynamic, can change without notice**.
- MEASURED (api.md): errors `401` invalid/missing key, `422` body failed validation (details offending field), `429` rate limit, `529` overloaded; on 429/529 use exponential backoff; SDKs do it automatically and **honor the `retry-after` header when present**.
- MEASURED (models.md): versioning — `jev-latest`→`jev-1.13.0` (most recent *stable official*), `jev-preview`→`jev-1.13.0` (no preview build right now). "An alias moves when a new release ships, so the answers behind it can change without a change on your side." Log the response `model`; pin `jev-1.13.0` if thresholds were tuned.
- **DETERMINISM: ABSENT.** No page read mentions temperature, sampling seed, reproducibility, or run-to-run stability. `grep -rniE 'determinis|temperature|seed|reproduc'` over all fetched TypeSafe docs returned no TypeSafe hits. Treat repeated identical calls as not guaranteed identical → ESTIMATE: must be measured before any engine loop relies on stable answers.
- **STREAMING/BATCH: ABSENT** as features. The design is instead many questions per single request (fan-out), no streaming endpoint mentioned.
- MEASURED (introduction.md, fan-out.md): "Adding questions barely changes the response time"; all questions evaluated in parallel against one state.
- MEASURED (primitives.md, parallel-questions cookbook): batching **13 questions into one call is 11.5x cheaper and 9.6x faster than 13 separate calls, with no change in the answers** (vendor cookbook, one workload).
- MEASURED (home, vendor demo): "Cost $0.000081 Completed in 0.114s" vs LLM "$0.013880 / 8.566s" → ESTIMATE 171x cheaper and 75x faster on that demo (home headline claims 193.6x / 444.6x).

## 7. Gaps / not found (explicit)
- No published rate-limit *tiers*, quotas, or burst details beyond the two dynamic numbers.
- No determinism/seed/reproducibility statement (above).
- No stated max number of questions or max criteria entries (only the token budget).
- No published per-request latency SLO; only the vendor demo and "barely changes".
- Changelog page for the *model* not found at /changelog.md (404); only SDK changelogs exist at /sdk/python/changelog and /sdk/javascript/changelog.

## 8. SDK / quickstart (distinct pages 19–20)
- MEASURED (quickstart.md, 2026-09-17): Python SDK **`pip install typesafe-sdk`** (or `uv add typesafe-sdk`), requires **Python >= 3.10**; client reads **`TYPESAFE_API_KEY`** from env and defaults to `jev-latest`. Playground at https://console.typesafe.ai/playground; key at /settings/keys (auth required — not fetched).
- MEASURED (sdk/python/changelog.md): SDK **v0.6.0 (2026-09-15)**; initial public release **v0.5.7 (2026-09-14)**. Breaking change v0.6.0: `Score.criteria` now an ordered sequence, not a dict keyed by integers. SDK is ~3 days old at read time — ESTIMATE: immature, pin versions.
- Distinct pages read: 20 (home, skills README, SKILL.md, api, confidence, system-one, state, models, introduction, sdk, primitives, primitives/advanced, ml-primer, fan-out, confidence-routing, composite-scoring, jaggedness, legal, quickstart, python-changelog).
