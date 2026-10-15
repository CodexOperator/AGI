# TypeSafe / jev — pricing, billing, data, security, terms digest

Reader: kid `pricing-legal` (agent a00-2132d69a), brief from
`.agi/context/local-maxxing/troves/2026-09-18-typesafe/hunt_args.json`.
All fetches `curl -sL` + python3 tag-strip, no key, no paid API, no auth.
Read date: **2026-09-18** (UTC ~02:16–02:35Z).

**Headline correction to the owner-stated line.** The docs *do* publish a price,
and it is **$0.042 per million input tokens / $42 per billion**, not the
owner-stated **$0.045**. Output tokens are **FREE**. So the owner figure is
**NOT confirmed** — it is off by ~7% and the measured number is *lower*.
Source: https://docs.typesafe.ai/models.md (doc `lastmod` 2026-09-17), and the
same pair repeated on the launch blog at https://typesafe.ai/blog/introducing-system-one-models-and-jev
(fetched 2026-09-18). Both are **MEASURED**.

## Sources read (22 distinct URLs, all 2026-09-18)

| # | URL | What it gave | Tag |
|---|-----|--------------|-----|
| 1 | https://typesafe.ai/ | Home: "$42 Per Billion input tokens", "238x Lower input price than Claude Fable 5.1", cost demo $0.000081 vs LLM $0.013880, FAQ stub "Are these prices temporary or subsidized?" (answer NOT in HTML — client-rendered, not readable) | MEASURED (numbers) |
| 2 | https://typesafe.ai/pricing | **HTTP 404** — no dedicated pricing page | MEASURED |
| 3 | https://typesafe.ai/sitemap.xml | 12 URLs; legal set = terms, privacy-policy, data-processing, mca; no pricing/security page | MEASURED |
| 4 | https://typesafe.ai/robots.txt | `Allow: /`; no disallow | MEASURED |
| 5 | https://typesafe.ai/legal/terms | "Terms of use", last updated **Sep 14, 2026** — covers the **Site only**, not the API | MEASURED |
| 6 | https://typesafe.ai/legal/privacy-policy | Privacy Policy, last updated **Nov 19, 2025** — Input collection, no-training promise, US hosting | MEASURED |
| 7 | https://typesafe.ai/legal/data-processing | DPA, last updated **Apr 24, 2026** — subprocessors, SCCs, security-incident 72h, audit rights | MEASURED |
| 8 | https://typesafe.ai/legal/mca | Master Customer Agreement, last updated **Aug 27, 2026** — the real API contract: credits, data license, output ownership, liability cap | MEASURED |
| 9 | https://typesafe.ai/manifesto | Marketing prose; no pricing/security claim found in stripped text | MEASURED (ABSENT) |
| 10 | https://typesafe.ai/team | JS-rendered; no readable security/compliance/pricing content in static HTML | MEASURED (ABSENT) |
| 11 | https://typesafe.ai/blog/introducing-system-one-models-and-jev | Pricing table `$0.042/Mtok`, output FREE, "we can't prove it isn't subsidized … expect [price] to go down, not up" | MEASURED |
| 12 | https://typesafe.ai/blog/antibenchmaxxing | No pricing/data terms | MEASURED (ABSENT) |
| 13 | https://docs.typesafe.ai/ (→ /introduction) | Doc entry; no pricing on landing | MEASURED |
| 14 | https://docs.typesafe.ai/legal | Three legal docs + "zero data retention (ZDR) for enterprise customers … privacy@typesafe.ai" | MEASURED |
| 15 | https://docs.typesafe.ai/legal.md | Same, machine-readable | MEASURED |
| 16 | https://docs.typesafe.ai/models.md | **The price**: `$42 / $0.042`; rate limits; context length; "not trained on customer requests or responses" | MEASURED |
| 17 | https://docs.typesafe.ai/api.md | `usage.input_tokens` / `usage.output_tokens`; errors 401/422/429/529; no retention statement | MEASURED |
| 18 | https://docs.typesafe.ai/llms.txt | Full doc index (115 lines); no pricing/billing/security page exists in docs | MEASURED |
| 19 | https://docs.typesafe.ai/sitemap.xml | 111 URLs; no `pricing`, `billing`, `security` page | MEASURED |
| 20 | https://trust.typesafe.ai | **Vanta-hosted SPA**; static HTML has title only, all content JS-loaded | MEASURED (unreadable) |
| 21 | https://trust.typesafe.ai/subprocessors | Same Vanta SPA shell (identical 6914 bytes) — no static list | MEASURED (unreadable) |
| 22 | https://console.typesafe.ai | Auth wall: "Welcome to TypeSafe — Continue with Google / Continue Email me a code"; no public pricing/billing view | **AUTH-REQUIRED, skipped** |

Topics with fewer than 12 pages: none. Docs+marketing gave >12 readable pages;
the only unreadable ones are the two Vanta trust-center URLs and the console
(auth), each logged and skipped rather than authenticated.

## Pricing per decision type

- **One price for all primitives.** No page differentiates `noul` vs `choice`
  vs `score`. The unit is the **input token**, independent of question type.
  https://docs.typesafe.ai/models.md, 2026-09-18 — **MEASURED**.
- **$42 per billion / $0.042 per million input tokens.** Same page, and
  https://typesafe.ai/blog/introducing-system-one-models-and-jev — **MEASURED**.
- **Output tokens FREE** ("too cheap to meter"). Same two sources — **MEASURED**.
  Note the API still *reports* non-zero `usage.output_tokens` (e.g. 48). The
  field is metered but priced at $0; do not read a bill from it.
  https://docs.typesafe.ai/api.md — **MEASURED**.
- **Does it differ by state size?** Yes, *implicitly*: price is per input
  token, and the state is the bulk of input. Costs scale linearly with state
  length. Limits: 64k tokens/request, 32k for `state` + longest question.
  https://docs.typesafe.ai/models.md — **MEASURED**.
- **No per-decision-type table, no tiered or volume price published.** `/pricing`
  404s; docs sitemap has no pricing page — **MEASURED (ABSENT)**.
- **Owner-stated $0.045/1M: NOT CONFIRMED.** Correct measured figure is
  $0.042/1M (2026-09-18). Treat $0.045 as stale — **MEASURED**.
- **Subsidy caveat, in the vendor's own words:** "We can't prove it isn't
  subsidized; we'll need the long-term to prove the sustainability of our
  pricing (which we expect to go down, not up)."
  https://typesafe.ai/blog/introducing-system-one-models-and-jev — **MEASURED**
  (statement), **ESTIMATE** (future direction).

**Cost arithmetic** (own calculation, **ESTIMATE**):

| state size | $/decision @ $0.042/Mtok | $/1000 decisions |
|---|---|---|
| 1k tok | $0.000042 | $0.042 |
| 2k tok | $0.000084 | $0.084 |
| 4k tok | $0.000168 | $0.168 |
| 8k tok | $0.000336 | $0.336 |

Homepage's own demo: TypeSafe "$0.000081" vs LLM "$0.013880" for one workflow
(≈171x cheaper) — https://typesafe.ai/, 2026-09-18 — **MEASURED** (vendor claim).
For the town's `idea:lm-typesafe-replay-200`: 200 × 2k = 0.4M tok ≈ **$0.0168**,
not the $0.02 estimated on the idea node — **ESTIMATE**.

## Billing granularity

Source: MCA https://typesafe.ai/legal/mca §8, 2026-09-18 — **MEASURED**.

- **Unit = a Credit, consumed per Input submitted** to the Services (§8.2).
  Not per-seat, not per-question — per *request/Input*. Each Input can carry
  many questions (`fan-out`), so batching lowers effective per-decision cost.
- **Purchased Credits**: expire at the earlier of end-of-Term or **12 months**
  after purchase (§8.2(a)). Optional **auto-refill** if opted in; otherwise
  TypeSafe *may decline to generate Output* when balance hits zero.
- **Promotional Credits** (free tier equivalent) exist **at TypeSafe's sole
  discretion**, no obligation, consumed before Purchased Credits, with their
  own expiry; creating accounts to farm them is barred (§8.2(b)).
- **Minimum spend: none published** — **MEASURED (ABSENT)**.
- **Invoicing**: fees in USD, **due 30 days** after invoice date; late fee 1.5%/mo
  (§8.1, §8.3). Customer pays taxes (§8.4).
- **"The rate at which Credits are consumed may vary based on account settings,
  including the model used"** (§8.2) — i.e. the published $0.042 is a rate for
  a given model, and credit consumption can change with model/settings, subject
  to whatever the console shows — **MEASURED**.
- **Preloaded $5 balance** on the owner account: owner-stated only; the console
  is auth-walled and no page confirms it — **UNCONFIRMED (owner-stated)**.
- No self-serve public price card at `/pricing`; pricing is in docs + blog, and
  purchase/credit display lives behind `console.typesafe.ai` — **MEASURED**.

## Data handling, retention and privacy

- **No model training on Input.** Privacy Policy: "We will not train or fine
  tune any artificial intelligence or machine learning models on your prompts
  or other Input." MCA §4.1 repeats it: TypeSafe "will not include Customer
  Data in a dataset used to train … without Customer's prior consent."
  https://typesafe.ai/legal/privacy-policy (Nov 19, 2025) and
  https://typesafe.ai/legal/mca (Aug 27, 2026) — **MEASURED**.
- **Input license is broad but purpose-limited.** Customer grants TypeSafe a
  non-exclusive, worldwide right to process Input "solely to perform its
  obligations" and to "derive and generate Telemetry" (MCA §4.1) — **MEASURED**.
- **Telemetry is unrestricted.** MCA §4.3: "Telemetry" (technical logs, hashes,
  summary statistics and classifications, metrics, learnings) may be processed
  "without restriction, including to improve the Services". **No opt-out is
  stated.** This is the clause that actually touches our data: even with no
  training on Input, TypeSafe may keep logs/stats/classifications of our
  requests. **MEASURED** — and the sharpest thing in this digest.
- **No retention period tied to a number.** DPA Schedule I §8: Customer Personal
  Data "retained for as long as necessary taking into account the purpose … and
  in compliance with applicable laws". MCA §10.3: after termination TypeSafe
  "will be under no obligation to store or retain Customer Data and may delete
  Customer Data at any time in its sole discretion."
  https://typesafe.ai/legal/data-processing (Apr 24, 2026) — **MEASURED**.
- **Zero Data Retention (ZDR)** offered **to enterprise customers only**;
  contact privacy@typesafe.ai. https://docs.typesafe.ai/legal.md — **MEASURED**.
  Not a default, not self-serve.
- **Privacy Policy collects account info, IP/location, device, usage, cookies**;
  uses Google Analytics; does not "sell"/"share" personal data. Retention: "as
  long as reasonably necessary". https://typesafe.ai/legal/privacy-policy —
  **MEASURED**.
- **US-hosted, US transfer.** "The Services are hosted in the United States";
  non-US data is transferred to the U.S. for storage and processing.
  Privacy Policy — **MEASURED**. (DPA adds SCCs/UK addendum as the transfer
  mechanism, but hosting stays US — **MEASURED**.)
- **Subprocessor disclosure location:** https://trust.typesafe.ai/subprocessors,
  referenced by DPA §3.1 — **MEASURED (link)**, list itself **NOT readable**
  (Vanta SPA, no static content).
- **Jev is not fine-tuned/LoRA-adapted per account; same weights serve every
  account.** https://docs.typesafe.ai/models.md — **MEASURED**.

## Security

- **No SOC 2 / ISO 27001 / encryption claim is published on any statically
  readable page.** Privacy Policy says only: "We make reasonable efforts to
  protect your data by using security measures designed to safeguard the data
  we maintain. However, because no electronic transmission or storage of data
  can be entirely secure, we can make no guarantees…" — **MEASURED (weak/ABSENT)**.
- **DPA §5.1**: "reasonable and appropriate technical and organization security
  measures"; may be updated if they don't materially decrease security —
  **MEASURED**. Specific measures live at **https://trust.typesafe.ai/**
  (DPA Schedule I §11) — a **Vanta**-hosted trust center (Vanta is a compliance-
  automation vendor), which is consistent with an in-progress compliance
  program but **confirms nothing**: the page's static HTML carries only a title,
  everything else is JS-loaded. **MEASURED (unreadable)** — the one place a
  SOC 2 report or subprocessor list would live is not machine-readable here.
- **Security incidents**: notify Customer **within 72 hours** of becoming aware
  (DPA §5.2) — **MEASURED**.
- **Audit**: Customer may audit TypeSafe controls **once per 12 months**, at
  Customer's cost, under mutual scope (DPA §5.3) — **MEASURED**.
- **Data residency**: US-hosted (above). **Encryption at rest/in transit: no
  explicit statement found** — **MEASURED (ABSENT)**.
- **International transfers**: EU SCCs Module 2/3, governing law Ireland,
  courts of Dublin; UK Addendum; Irish DPC supervisory authority.
  https://typesafe.ai/legal/data-processing §6, Schedule I — **MEASURED**.
- **Security-incident/abuse posture in MCA §6**: TypeSafe may suspend access for
  payment ≥30 days overdue, or actions risking harm to other customers or
  service integrity — **MEASURED**.

## Terms that bind us

Source: MCA https://typesafe.ai/legal/mca (Aug 27, 2026) unless noted —
**MEASURED**. Terms-of-use at /legal/terms (Sep 14, 2026) governs the *Site*
only and is not the API contract.

- **Output is ours.** MCA §4.2: TypeSafe "does not claim ownership of Input and
  TypeSafe disclaims ownership of Output … TypeSafe hereby assigns to Customer
  all of its right, title, and interest, if any, in the Output." Good: the
  town's (state, question, answer, confidence) rows are ours to keep and to use
  as training data for the local kid. **MEASURED**.
- **Liability cap.** MCA §12.2: aggregate liability ≤ **the greater of fees paid
  in the prior 12 months or $50 USD**, with the usual consequential-damages
  waiver. For a $5 account the cap is $50. (The separate Site Terms §11(b) cap
  is **$100**, but that is for the website, not the API.) **MEASURED**.
- **Bans that touch our plan.** MCA §2.3: no (b) using Output to **distill or
  train a model to imitate the Services, or develop a similar/competing
  product**; no (f) **publishing benchmarks or performance information about the
  Services**; no (c) reverse engineering; no (a) reselling the Services
  standalone. **The town's stated purpose — building a local kid on TypeSafe's
  labels — brushes against §2.3(b).** Training a *local* model on TypeSafe
  Output to imitate TypeSafe is exactly what that clause forbids. The 200-decision
  replay (measuring agreement/AUROC) is a *measurement*; §2.3(f) also bars
  publishing benchmark numbers. Both need the owner's eye before results are
  published or a local model is distilled. **MEASURED (clause) / judgement
  (interpretation)**.
- **`idea:lm-kid-persona-lora` corpus from TypeSafe labels** — same §2.3(b)
  exposure: using TypeSafe Output as labels to train a local model is the
  prohibited pattern. Flag, do not proceed on the corpus until cleared.
  **MEASURED (clause)**.
- **Confidentiality.** MCA §14.1: TypeSafe Confidential Information explicitly
  includes **Customer's Fees and all pricing information**; §14.2 restricts
  disclosure to need-to-know parties under no-less-protective obligations.
  So publicly quoting our invoice is a breach; quoting the *published* $0.042
  is not. **MEASURED**.
- **No data-retention obligation post-termination** (MCA §10.3, above) — don't
  treat TypeSafe as durable storage for anything the town needs. **MEASURED**.
- **Access credentials.** MCA §2.4: Customer responsible for all activity under
  its API key; keys must stay confidential. The key is a per-spawn secret —
  consistent with the town's existing "no key unasked" stance. **MEASURED**.
- **Third-party platforms** get Customer Data via TypeSafe on our behalf when
  enabled (MCA §7) — no such integration is enabled today. **MEASURED**.
- **Arbitration / class-action waiver** is in the *Site* Terms (§12, with a
  30-day opt-out to the SF address); the MCA's dispute/indemnity terms are civil
  and Dublin/Ireland-governed via the SCCs. **MEASURED**.
- **Feedback is free to exploit** (MCA §11, Site Terms §3(c)) — any suggestion
  we send about TypeSafe is non-confidential and usable without obligation.

## Fit for the town

- **The published price is cheaper than the owner thought** ($0.042 vs $0.045
  per Mtok in; $0 out). Every cost estimate on `idea:lm-typed-decisions-in-the-loop`
  and `hypothesis:lm-typesafe-replay-200` should be recomputed at $0.042 — the
  200-decision replay is ≈**$0.0168**, not $0.02. **ESTIMATE**.
- **Billing is per-Input, not per-decision.** Fan-out (many questions per
  request) is the town's cost lever: one 2k-token state carrying 10 questions
  costs the same as carrying 1. The `patterns/fan-out` cookbook exists precisely
  for this. **MEASURED (per-Input) / ESTIMATE (lever)**.
- **The real data risk is Telemetry, not training.** TypeSafe promises no
  training on Input, but MCA §4.3 lets it keep and use logs, hashes,
  classifications and metrics "without restriction". If the town sends real
  (even redacted) internal state, assume summary statistics about it may be
  retained indefinitely unless a ZDR (enterprise-only) contract is signed.
  **MEASURED** — this is a one-line addition to the town's data-handling rules.
- **The two legal tripwires for the local-kid plan are MCA §2.3(b) and §2.3(f).**
  Distilling TypeSafe Output into a local model, and publishing benchmark
  numbers about the Services, are both contractually barred. The 200-replay
  must be framed as internal evaluation, not a published benchmark, and the
  persona-LoRA corpus must not be labelled by TypeSafe Output without clearing
  §2.3(b). **MEASURED (clause)**.
- **Liability is trivially capped ($50 for a $5 account)** and there is **no
  published SOC 2, encryption, or retention term**. For a town sending only
  redacted state through a $0.02 experiment this is acceptable; for anything
  resembling production internal state it is not — that trade belongs in the
  banked key decision (`idea:lm-typed-decisions-in-the-loop` "BANKED" note).
  **MEASURED (terms) / judgement (acceptability)**.
- **Output ownership is clean**: the (state, question, answer, confidence) log
  is ours to store and reuse — bounded, again, by §2.3(b) if reused as training
  labels. **MEASURED**.

## What changed vs the 19-line digest (.agi/context/local-maxxing/papers/typesafe-ai.md)

1. **Pricing is no longer ABSENT.** The digest listed pricing as absent; it is
   published at `docs.typesafe.ai/models.md`: **$0.042/Mtok in, output FREE** —
   not the owner's $0.045.
2. **Rate limits are no longer ABSENT:** **250,000 tok/s and 1,200 req/min**;
   429 above either; 529 when overloaded. Docs also warn limits are adjusting
   dynamically and may change without notice.
3. **State limits are no longer ABSENT:** **64k tokens/request; 32k for `state`
   + the longest single question.** Input text only (string/JSON/array).
4. **Data handling now specific:** no training on Input (Privacy Policy + MCA
   §4.1); **Telemetry unrestricted (MCA §4.3)**; ZDR enterprise-only; US-hosted;
   no numeric retention period.
5. **Legal contract identified:** the API is governed by the **Master Customer
   Agreement** (Aug 27, 2026), not the Site Terms of Use. Output assigned to
   customer (§4.2); liability cap **greater of 12-mo fees or $50** (§12.2);
   §2.3 bars distillation, competing products, and **published benchmarks**.
6. **Security posture is thin/unreadable:** "reasonable efforts" only; specific
   measures behind a Vanta trust center (`trust.typesafe.ai`) whose static HTML
   has no content; no SOC 2/encryption claim found.
7. **Model versioning corrected:** `jev-latest` → `jev-1.13.0` (a *pinned*
   versioned ID is accepted; alias is floating) — from `models.md`.
