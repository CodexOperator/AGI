# TypeSafe (typesafe.ai) — skill + API digest (read 2026-09-17 00:0xZ by thought-master; sources: https://raw.githubusercontent.com/typesafe-ai/skills/main/skills/typesafe-ai/SKILL.md, https://docs.typesafe.ai/api.md)

## Measured lines (quoted)
- Skill (MIT): "small units of AI intelligence you can use like programming primitives" — natural-language questions paired with application STATE return TYPED judgments with probabilities, never generated text. Use "where semantic understanding helps", when a feature needs "programmable common sense", or where prompt-and-parse could become structured decisions (routing, ranking, extraction, verification).
- API: `POST https://api.typesafe.ai/v1/systemone`, `Authorization: Bearer <API_KEY>`, model `"jev-latest"` ("flagship"). Errors 401 / 422 / 429 / 529; "exponential backoff instead of retrying immediately".
- Three primitives, request → response:
  - `noul` (yes/no): `{"state": "...", "model": "jev-latest", "questions": {"is_urgent": {"type": "noul", "instructions": "Does this convey urgency?"}}}` → `{"answers": {"is_urgent": {"type": "noul", "noul": 0.92}}}`
  - `choice`: `{"type": "choice", "instructions": "Which team…?", "criteria": {"billing": "...", "technical": "...", "sales": "..."}}` → `{"choice": "technical", "probabilities": {...}, "confidence": 0.82}`
  - `score` (rubric): `{"type": "score", "instructions": "How frustrated…?", "criteria": ["Calm", "Frustrated", "Very angry"]}` → `{"score": 1.6, "legend": {...}, "probabilities": {...}, "confidence": 0.78}`
- SDKs: Python + JavaScript (docs.typesafe.ai/sdk/*). Install paths named by the skill: `claude plugin marketplace add typesafe-ai/skills` + `claude plugin install typesafe@typesafe-ai` (Claude Code) or `npx skills add typesafe-ai/skills --skill typesafe-ai`.
- ABSENT from both pages: pricing, rate limits, state-size / choice-count limits, latency, batching, determinism, data retention, key acquisition / free tier.
- OWNER-STATED (pane line 2026-09-17 00:0xZ, not on the pages read): "$0.045 per million tokens in, output tokens free … only structured output, like multiple choice but with a small ai behind it."

## What it is for the town
A typed-decision primitive with a probability attached, priced (owner) at ~1/4 of deepseek-v4-flash input and $0 output. It is NOT a generator: it answers a fixed question about a state. Every place the engine or a kid makes a small classification by regex, heuristic or an LLM prose call is a candidate.

## Not done here, banked
- Installing the plugin = a harness settings change (the Prime's cell); the API key = a NEW PROVIDER + a secret in `.env` (Prime + encryption town) — never added by the thought-master unasked; the pane line asks, the owner line must arrive via the Prime.
- Engine integration (an adapter/gate that calls it) = g15 nodes, kids write the code — after a round-1 accuracy number exists.
