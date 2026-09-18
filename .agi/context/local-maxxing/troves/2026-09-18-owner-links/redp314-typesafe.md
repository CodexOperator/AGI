# X-THREAD: @redp314 — TypeSafe/Jev as a PR reviewer
Slice X-THREADS / local-maxxing town. READ-ONLY (no key, no install). Read 2026-09-18Z.
Tag legend: MEASURED = quoted from a page/file read here; ESTIMATE = my arithmetic/inference.

## 0. The post (pointer)
- Post: https://x.com/redp314/status/2100585126652481915 — @redp314 (Paolo Rosson), created **Thu Sep 17 13:58:15 +0000 2026** (MEASURED, fxtwitter `created_at`), 197,479 views, 2,210 likes (MEASURED). JSON read via `https://api.fxtwitter.com/redp314/status/2100585126652481915`.
- Media: 32.4 s mp4 (video/1), no external card URL, no quoted tweet, no `urls` facets (MEASURED — post carries NO outbound link).

## 1. What is claimed (all MEASURED, verbatim from post text)
- "~200x cheaper than Claude and it answers in half a second"
- "6 real PRs in the video. **$0.00007 each**. 1,000 PRs = **7 cents** vs **~$14.50 on Opus 5**"
- "paste a diff → ONE call to @typesafeai → **14 typed checks** come back as probabilities: hardcoded secret, sql injection, touches auth, deletes tests, breaks api, migration, debug leftovers, does the description actually match the diff, blast radius, reviewer effort…"
- "code turns that into a verdict: BLOCK / security review / nits / merge. anything a critical check isn't sure about (**0.35–0.65**) gets escalated to a human or a big model instead of guessed"

## 2. The artifact it points to
- @typesafeai → **TypeSafe AI**, model **Jev** (System One Models). Site https://typesafe.ai; API `POST https://api.typesafe.ai/v1/systemone`; docs https://docs.typesafe.ai.
- Already-troved by this town: `troves/2026-09-18-typesafe/{concepts-api.md,pricing-terms.md,recipes-sdks.md}` (read 2026-09-17/18).
- Model id **`jev-1.13.0`** (alias `jev-latest`); **$42/Btok = $0.042/Mtok input; output tokens free** (MEASURED, models.md via town trove).
- Only three decision types exist: `noul` (yes/no), `choice` (probabilities+confidence), `score` (ordered rubric). All questions in one request are independent and evaluated in parallel (MEASURED, docs).
- Vendor blog: https://typesafe.ai/blog/introducing-system-one-models-and-jev — "two orders of magnitude faster and more [cheaper]" (MEASURED quote via search; date not captured).

## 3. The headline number (and cross-checks)
- Post headline: **$0.00007 per PR review**, **7¢ / 1,000 PRs**, "~200x cheaper", "half a second" (MEASURED, post).
- Vendor home demo: TypeSafe "$0.000081 / 0.114 s" vs LLMs "$0.013880 / 8.566 s"; badge "193.6x Faster, 444.6x Cheaper" (MEASURED, typesafe.ai via town trove).
- ESTIMATE cross-check: $0.00007 ÷ $0.042/Mtok ⇒ **~1,667 input tokens per PR** at list price. Consistent with a diff + 14 criteria prompts; output is free so answer length does not add cost.
- ESTIMATE: post's implied ratio vs "$14.50 on Opus 5" = 14.50/0.07 ≈ **207x**, matching the post's "~200x". Internal arithmetic is self-consistent; neither figure is independently audited here.
- CAUTION: the 14 checks / escalation band are a **user-built wrapper** ("code turns that into a verdict"), not a published TypeSafe feature — TypeSafe supplies `noul/choice/score`, the caller supplies the 14 questions and the 0.35–0.65 rule. The post does not publish that code (MEASURED absence).

## 4. Town chain it touches
- **Typed decisions** chain (primary): calibrated probabilities + explicit escalate-if-unsure is exactly "typed decisions" and the "decide vs guess" boundary.
- **Local inference** (secondary): "answers in half a second", one call, no chat loop — a System One model is a tiny-model-shaped decision box, not a generator.
- **Kid persona / two tiny models cooperating** (tertiary): the escalation band 0.35–0.65 is a concrete, testable **router policy** for when a tiny model hands off to a big one — a "cooperating models" mechanism with a numeric threshold.

## 5. Hypothesis seeds (smallest experiment)
- **S1 (THIS box, 4-core arm-cloud, no GPU) — replicate the escalation router offline.** Take 14 atomic `noul`-style checks over a diff; substitute a local tiny model for Jev (no paid API), emit probabilities, apply the 0.35–0.65 → escalate rule, and measure (a) coverage, (b) how often it escalates, (c) agreement with a hand label. Est cost **$0.00**, **~30–45 min**. Falsifier: tiny-model probabilities are uncalibrated so the band escalates ~everything or ~nothing.
- **S2 (THIS box) — list-price arithmetic audit.** 1,000 synthetic PR-review calls at list price ⇒ **$0.07 ESTIMATE** (1,667 tok × $0.042/Mtok × 1,000). Do NOT spend: TypeSafe has no public free tier (town trove §3), so this stays an ESTIMATE unless the owner authorises paid keys.
- **S3 (local-town, ssh alias, gpu-8g) — Jev vs local tiny model on the same 14 checks.** Same prompts, two deciders, compare verdicts. Est cost **$0.00** (local only) + optional ~$0.07 API. **~45 min**.

## 6. Open questions
- Is `@typesafeai` a public repo/SDK? Town trove found Python/JS SDKs (sdk.md) but no PR-review wrapper repo (MEASURED absence).
- No published free tier; console gated behind waitlist. Any live test of S1/S2 requires owner-authorised spend.
- Post's 6 PRs are in the video only; per-PR token counts not disclosed.
