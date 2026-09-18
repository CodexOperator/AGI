# TypeSafe jev — concepts & API digest (concepts-api kid)

All pages fetched with `curl -sL` on **2026-09-17** (Mintlify serves Markdown by
appending `.md`). Every claim below is tagged **MEASURED** (quoted from a page
fetched this run) or **ESTIMATE**. This digest EXTENDS
`.agi/context/local-maxxing/papers/typesafe-ai.md` (19 lines); do not re-derive
what is already there unless a correction is flagged.

## Sources read (23 distinct pages, all HTTP 200 unless noted)

| # | URL | What it gave |
|---|-----|--------------|
| 1 | https://docs.typesafe.ai/api.md | full request/response schema, error table |
| 2 | https://docs.typesafe.ai/llms.txt | documentation index |
| 3 | https://docs.typesafe.ai/primitives.md | the three types, multi-question batching, token budget |
| 4 | https://docs.typesafe.ai/primitives/choice.md | Choice schema + **255-option limit** |
| 5 | https://docs.typesafe.ai/primitives/score.md | Score schema + 2–10 level limit |
| 6 | https://docs.typesafe.ai/primitives/noul.md | Noul schema, optional criteria, no confidence |
| 7 | https://docs.typesafe.ai/primitives/advanced.md | EntryType: instructions/criteria accept JSON |
| 8 | https://docs.typesafe.ai/confidence.md | confidence-vs-probability semantics |
| 9 | https://docs.typesafe.ai/concepts/state.md | state shapes |
| 10 | https://docs.typesafe.ai/concepts/system-one.md | primitive overview |
| 11 | https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md | workflow guidance, thresholds |
| 12 | https://docs.typesafe.ai/models.md | **pricing, rate limits, context, aliases** |
| 13 | https://docs.typesafe.ai/patterns/fan-out.md | batching many questions one call |
| 14 | https://docs.typesafe.ai/patterns/confidence-routing.md | three confidence bands |
| 15 | https://docs.typesafe.ai/introduction/machine-learning-primer.md | **RLCD calibration claims** |
| 16 | https://docs.typesafe.ai/model-jaggedness/jev-1.13.md | known failure modes (dated 2026-09-17) |
| 17 | https://docs.typesafe.ai/migrating-to-v1.md | v1 versioning history |
| 18 | https://docs.typesafe.ai/sdk/python/api/types/responses.md | typed answer/usage fields |
| 19 | https://docs.typesafe.ai/sdk/python/api/retries.md | RetryPolicy defaults |
| 20 | https://docs.typesafe.ai/sdk/python/api/exceptions.md | full SDK error taxonomy |
| 21 | https://docs.typesafe.ai/sdk/python/api/constants.md | env vars, timeouts |
| 22 | https://docs.typesafe.ai/sdk/python/api/types/questions.md | SDK question types |
| 23 | https://docs.typesafe.ai/sdk/python/api/clients/sync/client.md | sync client surface |

23 pages visited; >12 required. One 404 (`/mobile.md`) was not a real doc page.

## Decision types — exactly three (confirmed)

**MEASURED** https://docs.typesafe.ai/primitives.md: "There are three question
types" — `choice`, `score`, `noul`, set by the `type` field. No fourth type
exists anywhere in the index or API. Each question has an id (map key, *not*
sent to the model), `type`, `instructions` (string | object | array | null) and
its own `criteria`.

| Type | Answers | Response fields |
|------|---------|-----------------|
| `choice` | Which of these options? | `choice`, `probabilities`, `confidence` |
| `score` | Which level? | `score`, `legend`, `probabilities`, `confidence` |
| `noul` | Is this true? | `noul` (0–1), **no confidence** |

**MEASURED** `Noul` criteria are **optional** (`{true, false}` descriptions);
`Choice` criteria are a required map `option → description|null`; `Score`
criteria are a required ordered array, **at least 2 levels**. (Noul page says
"criteria | No", i.e. optional.)

## Request / response schemas

**Request** (**MEASURED** https://docs.typesafe.ai/api.md):
```json
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer <API_KEY>
Content-Type: application/json
{
  "state": "<string | object | array of text>",
  "model": "jev-latest",
  "questions": {
    "is_urgent": {"type": "noul", "instructions": "Does this convey urgency?",
                  "criteria": {"true": "...", "false": "..."}},
    "department": {"type": "choice", "instructions": "...",
                   "criteria": {"billing": "...", "technical": null}},
    "frustration": {"type": "score", "instructions": "...",
                    "criteria": ["Calm", "Frustrated", "Very angry"]}
  }
}
```
All three fields required. `state` = string | object | array (text only).
`instructions` and every `criteria` entry accept `string | object | array |
null` (**MEASURED** `primitives/advanced.md` — `EntryType`).

**Response** fields: `model`, `answers` (map keyed by question id), `usage`
(`{input_tokens, output_tokens}`, both integers). Answer bodies:
- noul: `{type, noul}`
- choice: `{type, choice, probabilities (map option→float, sums to 1), confidence}`
- score: `{type, score (can be fractional), legend (map level#→description),
  probabilities (map level#→float), confidence}`

**MEASURED** `sdk/python/api/types/responses.md`: SDK `SystemOneResponse` also
carries `request_id`; `Usage.input_tokens/output_tokens` are `None` "when the
API did not report it". `ScoreAnswer.probabilities` and `.legend` are keyed by
**integer** level in the SDK but by **string** key in raw JSON.

Optional fields NOT in the old digest: `criteria` on Noul; structured
instructions/criteria; `usage`; `request_id`.

## Probability and confidence semantics

- **Calibration claim — MEASURED** https://docs.typesafe.ai/introduction/machine-learning-primer.md:
  trained with **RLCD** (reinforcement learning for calibrated decisions).
  "Outcomes assigned a probability of `0.2` should occur about 20% of the
  time… `0.8` about 80%… `1.0` should occur 100%". These rates describe groups
  of predictions, "not a guarantee about any single answer".
- **`confidence` is derived from `probabilities` — MEASURED**
  https://docs.typesafe.ai/confidence.md: "a statistic computed from the
  probability distribution the answer already gives you", 0–1, present on every
  Choice and Score answer. **Noul has no confidence** — its `noul` value *is*
  the probability.
- Contrast: `probabilities` = full distribution over the options/levels you
  supplied; `confidence` = one-number collapse of that shape (peaked = high,
  flat = low). You may compute your own statistic from `probabilities` instead.
- **ESTIMATE**: since `confidence` is a statistic of the distribution and the
  distribution is calibrated, confidence is *indirectly* calibrated; TypeSafe
  publishes no confidence-vs-accuracy curve in these docs (ABSENT).
- **MEASURED** https://docs.typesafe.ai/primitives/score.md: "confidence 1.0
  means the returned distribution puts all its probability on one level. This
  describes the model's answer, not a guarantee that the answer is correct."

## Limits

| Limit | Value | Source |
|-------|-------|--------|
| Context length | **64k tokens/request** total; **32k tokens for `state` + longest question** | models.md (MEASURED) |
| Shared token budget (state+questions) | **~32,000 tokens ≈ 150,000 chars English** | primitives.md (MEASURED) |
| Choice options | **up to 255** | primitives/choice.md (MEASURED) |
| Score levels | **min 2, max 10** | primitives/score.md (MEASURED) |
| Rate limit (jev-1.13) | **250,000 tokens/sec** and **1,200 requests/min**; over either → `429` | models.md (MEASURED) |
| Rate limit stability | "adjusting dynamically… can change without notice" | models.md (MEASURED) |
| Input modality | **text only** (string/JSON/text array); no image/audio/video | models.md, state.md (MEASURED) |
| Batching | none separate — *one request is the batch*; adding questions ≈ free in latency | primitives.md (MEASURED) |
| Questions per request | limited only by the shared token budget | primitives.md (MEASURED) |
| Streaming | **ABSENT** in all pages read (recipes kid owns the definitive answer) | — |
| Published latency p50/p95 | **ABSENT** in all concept/api pages | — |

**MEASURED** cookbook claim (index): batching 13 questions into one call is
**12.2x cheaper and 10.0x faster** than 13 separate calls with no change in
answers (primitives.md says 11.5x/9.6x; the index says 12.2x/10.0x — minor
doc inconsistency worth noting).

## Errors and versioning

**HTTP status table — MEASURED** https://docs.typesafe.ai/api.md:
`401` (missing/invalid key), `422` (body failed validation; body names the
offending field), `429` (rate limit), `529` (Overloaded — TypeSafe temporarily
overloaded). The old digest lists only these four.

**Fuller error set — MEASURED** https://docs.typesafe.ai/sdk/python/api/exceptions.md
(the SDK maps more codes than the HTTP table documents):
`400` BadRequest, `401` Authentication, `403` PermissionDenied, `404` NotFound,
`422` UnprocessableEntity, `429` RateLimit (**carries `retry_after_ms`** parses
`Retry-After`), `5xx` InternalServer, plus `TypeSafeAPIConnectionError`,
`TypeSafeAPITimeoutError` and `TypeSafeAPIResponseValidationError`
(`field_path` like `answers.tone.confidence`). Base `TypeSafeError`; API errors
expose `status`, `body`, `headers`, `endpoint`, `request_id`
(`x-typesafe-request-id` header).

**Retry policy defaults — MEASURED** https://docs.typesafe.ai/sdk/python/api/retries.md:
`max_retries=2`, `backoff_initial=0.5s`, `backoff_max=5.0s`,
`backoff_jitter=0.25`, retryable statuses `{408, 429, 500–599}`,
`respect_retry_after=True` (honors `Retry-After` and `retry-after-ms`), retries
connection + timeout errors, total retry `timeout=30.0s`.

**SDK constants — MEASURED** https://docs.typesafe.ai/sdk/python/api/constants.md:
env vars `TYPESAFE_API_KEY`, `TYPESAFE_BASE_URL`, `TYPESAFE_DEFAULT_MODEL`,
`TYPESAFE_LOG_LEVEL`; `DEFAULT_BASE_URL=https://api.typesafe.ai`,
`DEFAULT_MODEL='jev-latest'`, `DEFAULT_TIMEOUT=10.0s`.

**Versioning — MEASURED** https://docs.typesafe.ai/models.md:
- `jev-latest` is an **alias → `jev-1.13.0`** ("most recent stable, official
  release"; SDK default). It **floats** — "An alias moves when a new release
  ships, so the answers behind it can change without a change on your side."
- `jev-preview` is an alias that also currently points to `jev-1.13.0`
  (no preview build available).
- **A dated/versioned model name exists: `jev-1.13.0`** and is accepted by the
  `model` field even though `GET /v1/models` currently lists only the aliases.
  The response's `model` field reports the versioned ID that answered, so a
  caller can log/pin. **Recommendation for the town: pin `jev-1.13.0`, not
  `jev-latest`,** because tuned confidence thresholds are version-sensitive.
- Endpoint itself is `v1`; the prior `/preview/evaluation` shape was a breaking
  change documented at https://docs.typesafe.ai/migrating-to-v1.md (old fields
  `prompts`/`responses`/`probability`/`chosen`/`expectation` renamed).

## Fit for the town

- **The three-primitive contract is the whole surface.** Everything the engine
  can ask a TypeSafe call is a Choice, Score or Noul. A "typed decision" in the
  town is one of these three, each with a probability (Choice/Score: a full
  distribution; Noul: a single p).
- **Batching is the economic lever.** One request with N questions costs the
  state once plus a few tokens per question; N separate requests pay the state
  N times. Every town site that would call jev per-item should instead consider
  one call with many questions (fan-out pattern) — ~10x cheaper/faster per the
  cookbook claim.
- **Confidence is the escalation gate.** Choice/Score answers carry a derived
  confidence; a three-band policy (high = act, medium = confirm/flag, low =
  human) is the documented pattern. Noul has no confidence, so a Noul-only site
  must threshold the `noul` value itself, or pair with a Choice for escalation.
- **Known failure modes (dated 2026-09-17)** that bound which seams are legal:
  no counting, no numeric/date arithmetic, no multi-hop indirection, degraded
  accuracy as irrelevant state grows, literal reading of instructions. Keep the
  arithmetic in code; ask the semantic question only.
- **Cost** (**MEASURED**): $42/Btok = **$0.042 per Mtok input, output tokens
  free**. For a ~1k-token state, ~$0.000042/decision. This CORRECTS the owner's
  owner-stated "$0.045/Mtok" — the page says $0.042.
- **No key needed for this digest**; nothing here touches `.env` or Doppler.

## Delta vs `.agi/context/local-maxxing/papers/typesafe-ai.md`

1. **CORRECTION — price**: page says **$0.042/Mtok input, $0/Btok output**
   (models.md), not the owner-stated $0.045.
2. **NEW — rate limits**: 250k tok/s, 1,200 req/min, dynamically adjusting.
3. **NEW — context limits**: 64k/request, 32k for state+longest question,
   ~32k shared token budget (~150k chars).
4. **NEW — cardinality limits**: Choice ≤255 options; Score 2–10 levels; Noul
   criteria optional.
5. **NEW — confidence semantics**: derived statistic from `probabilities`;
   Noul has none; RLCD calibration claim (0.2↔20%).
6. **NEW — full error list**: 400/401/403/404/422/429/5xx + connection/timeout/
   response-validation SDK errors; `529` Overloaded documented.
7. **NEW — versioning**: `jev-latest` floats and currently = `jev-1.13.0`;
   `jev-preview` same; versioned ID accepted; `GET /v1/models`.
8. **NEW — request/response extras**: `usage{input_tokens,output_tokens}`,
   `request_id`, structured `instructions`/`criteria` (EntryType), `legend`.
9. **NEW — SDK constants/retry**: env vars, `DEFAULT_TIMEOUT=10s`, RetryPolicy
   defaults, `retry-after` honoring.
10. **CONFIRMED**: `POST /v1/systemone`, Bearer auth, three primitives,
    401/422/429/529 + exponential backoff — all still correct.
11. **STILL ABSENT everywhere**: published latency p50/p95, streaming mode,
    a documented MCP server, per-primitive price differences (recipes and
    pricing kids own those).
