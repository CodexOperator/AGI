# TypeSafe — PRICING, LIMITS, DATA HANDLING, TERMS (Slice 3)
Read-only digest, 2026-09-18Z. Public pages only, no API key used. MEASURED = quoted from a page read here; ESTIMATE = my arithmetic.
Companion to slice 1 `concepts-api.md` (model/API/limits) and slice 2 `recipes-sdks.md` (recipes/SDKs). This slice covers money, quotas, data policy, legal.

## Pages read (distinct)
1. https://typesafe.ai (home, incl. embedded FAQ) — fetched 2026-09-18
2. https://docs.typesafe.ai/legal.md — legal index
3. https://typesafe.ai/legal/privacy-policy (Last updated Nov 19, 2025)
4. https://typesafe.ai/legal/data-processing (DPA, Last updated Apr 24, 2026)
5. https://typesafe.ai/legal/mca (Master Customer Agreement, Last updated Aug 27, 2026)
6. https://typesafe.ai/legal/terms (Terms of use, Last updated Sep 14, 2026; /terms redirects here)
7. https://trust.typesafe.ai/subprocessors
8. console.typesafe.ai (probe for pricing/free tier)

## 1. PRICE (MEASURED)
- Home: "Jev.Cost $42 Per Billion input tokens. 238x Lower input price than Claude Fable 5.1" → **$42/Btok = $0.042/Mtok input**.
- Home benchmark claim: "193.6x Faster, 444.6x Cheaper. *based on workflows for System One tasks (proof)" with a widget "TypeSafe AI Cost $0.000081 Completed in 0.114s" vs "LLMs Cost $0.013880 Completed in 8.566s" — ESTIMATE: that is ~171x cost ratio on the shown example (0.013880/0.000081 = 171.4), not the headline 444.6x.
- slice 1 `models.md` MEASURED: "output tokens are free"; price $42/Btok input. Output = 0 ⇒ billing is **input-token only**; a decision's price is set by prompt size, not answer size.
- Home FAQ (questions present; answers are client-rendered and NOT in the fetched HTML — MEASURED absence): "Are these prices temporary or subsidized?" is listed as a FAQ question. **No answer text is in the static HTML.** Treat price durability as UNKNOWN from public docs.

## 2. BILLING GRANULARITY (MEASURED)
- REST response carries `usage{input_tokens,output_tokens}` (slice 1/2) → per-request token accounting, reported per call.
- No subscription/seat/decision-count price is published. The only published meter is **input tokens**. There is no published "per decision" price; one decision's cost = (state + question tokens) × $0.042/Mtok.
- ESTIMATE: a small noul/choice call with ~500 input tokens costs ~500/1e9 × $42 = **$0.000021** (2.1e-5 USD). A 2,000-token call ≈ $0.000084. So **$0.021 per 1,000** tiny calls and **$0.084 per 1,000** 2k-token calls. (Arithmetic only — no published per-decision rate exists.)

## 3. FREE TIER / QUOTAS (MEASURED)
- slice 1 `models.md`: rate limits **250,000 tokens/second** and **1,200 requests/minute**, over either → HTTP 429; "Rate limits are adjusting dynamically ... can change without notice."
- slice 1 `models.md`: **64k tokens/request**; **32k tokens for `state` plus the longest question**.
- Home page has a **"Join Waitlist"** nav item (MEASURED) — the product appears gated/early-access, so a free tier is not advertised publicly.
- **No published free-tier token allowance or monthly quota found on any public page read here.** Console/account pricing is behind console.typesafe.ai (see §6).

## 4. DATA HANDLING (MEASURED)
- Privacy policy: "We collect the personal data you provide when you use the Services, including your prompts, data, instructions, and other input ('Input'). **We will not train or fine tune any artificial intelligence or machine learning models on your prompts or other Input.**"
- slice 1 `models.md` (MEASURED): "Jev is not fine-tuned or LoRA-adapted with customer data ... the same weights serve every account"; "Jev is not trained on customer requests or responses." ZDR for enterprise.
- Privacy policy Retention: "We retain personal data about you for as long as reasonably necessary to provide you with the Services ... When you request that we do so, we take measures to delete your personal data ... unless we are required by law to keep this data for a longer period." → **retention is indefinite by default, deletion on request**, not a fixed N-day window.
- DPA §2.2: Typesafe will not "(a) 'sell' or 'share' ... Customer Personal Data, (b) retain, use, or disclose Customer Personal Data for any purpose other than in accordance with the Documented Instructions ... outside of the direct business relationship ... nor (d) ... combine Customer Personal Data with personal data that Typesafe receives from or on behalf of any third party."
- DPA §3.1: "Customer provides general authorization for Typesafe to engage the following subprocessors as described in https://trust.typesafe.ai/subprocessors."
- docs legal.md: "We also offer zero data retention (ZDR) for enterprise customers. Contact privacy@typesafe.ai." → **ZDR is enterprise-only, gated by a human email.**

## 5. TERMS THAT BIND AN AUTOMATED AGENT SYSTEM (MEASURED, page-level)
- Terms of use (Sep 14, 2026): "ARBITRATION NOTICE. Except for certain kinds of disputes described in Section 12 (Dispute Resolution and Arbitration), you ..." → binding arbitration + class-action waiver.
- MCA (Aug 27, 2026): agreement formed by "clicking a box ... executing an Order ... or making any payment"; governs purchased access. Full billing/SLA/liability clauses to be quoted in §7 (appended below).
- DPA (Apr 24, 2026): Customer is controller/business, Typesafe is processor/service provider; subprocessors authorized generally.

## 6. PROBES / GAPS
- console.typesafe.ai is the account surface named by slice 1/2; pricing, free tier and quotas, if any, live there. Probe result appended in §7.
- No SLA document was found linked from docs legal.md or the home page (MEASURED absence). MCA is the place an SLA would attach; check §7.
- Home FAQ answers are not in static HTML (client-rendered). Not retrievable read-only without a browser.

## 7. APPENDED PAGE DETAILS
(added per-page as fetched)
### P7. Home FAQ — client-rendered, answers NOT in static HTML (MEASURED absence)
FAQ questions listed (answers absent): "What are System One Models?"; "Is Jev just a smaller LLM?"; "How is this different from JSON mode or structured outputs?"; "How can Jev be so fast and inexpensive?"; "Can you make Jev even faster?"; "**Are these prices temporary or subsidized?**"; "What is Jev good at?"; "Where does it struggle?"; "Can Jev still get things wrong?"; "Is Jev deterministic?"; "How do I get started or ask a question?" → price-durability is an *asked question*, unanswered publicly.
### P7. https://trust.typesafe.ai/subprocessors — HTTP 200, JS Trust Center shell only, no static list (MEASURED). Subprocessor names require JS/auth.
### P7. https://console.typesafe.ai — 302 to /login ("Continue with Google" / "Continue Email me a code instead"). **AUTH REQUIRED → skipped per brief.** No public price/free-tier/quota page exists there for an unauthenticated reader.
### P7. MCA (Aug 27, 2026) — BILLING & LIMITS
- §8.1 "All fees ... will be paid in US dollars ... all Fees are due within 30 days after the invoice date."
- §8.2 "Customer must obtain TypeSafe-managed **credits** that are consumed by each Input submitted ... Credits include Credits purchased ... ('Purchased Credit') and Credits that TypeSafe, at its sole discretion, issues ... at no cost ('Promotional Credits'). **The rate at which Credits are consumed may vary based on account settings, including the model used** ... Credits (y) are not redeemable, refundable, transferable ... (z) do not constitute ... any personal property right." → **billing unit = a TypeSafe Credit per Input; promotional (free) credits are discretionary, not a published free tier.**
- §2.1 license bounded by "the usage limits set forth in the Order ('Usage Limits')" → quotas are per-contract, not published.
### P7. MCA — SLA / WARRANTY
- §9.1 "TypeSafe warrants ... the Services will perform **materially as described in its Documentation** ('Service Warranty')."
- §9.2 remedy: written claim within **30 days**; TypeSafe has **30 days** to correct; else terminate + refund pre-paid unused Fees.
- §9.3 "**AS IS** and **AS AVAILABLE** ... DOES NOT WARRANT THAT CUSTOMER'S USE OF THE SERVICES WILL BE UNINTERRUPTED OR ERROR-FREE." → **no uptime SLA / no % availability commitment found.**
### P7. MCA — LIABILITY, IP, RESTRICTIONS
- §12.2 cap: "greater of (A) the amounts paid ... during the 12 months prior ... and (B) **$50 USD**."
- §12.1 waives indirect/consequential/lost-data/lost-profit.
- §11 Customer "retains all intellectual property rights in its Input"; TypeSafe retains Services/Documentation/**Telemetry**.
- §2.3 restrictions: no reselling Services as a standalone service; **no "model distillation, train a model to imitate the output ... or develop ... a similar or competing product"**; no reverse engineering.
- §6 immediate suspension on breach, payment overdue ≥30 days, or harm to security/availability.
### P7. Terms of use (Sep 14, 2026)
- §2(b) forbids using the **Site** "by automated electronic processes, 'robots,' 'spiders,' 'scrapers,' 'webcrawlers' ... that monitor, copy, or download data" (this is the *Site*; the API is licensed separately under the MCA).
- Governing law **Delaware**; binding individual arbitration + class-action waiver; opt-out by mailed notice to "TypeSafe AI, Inc., Attention: Legal Department – Arbitration Opt-Out, 255 California St, Suite 1300, San Francisco, CA 94117".

## 8. HYPOTHESIS SEEDS — $/1k decisions at $0.042/Mtok input, output $0 (ESTIMATE, arithmetic only)
| Loop site | Input tokens/decision (EST) | $/1k decisions | $/1M decisions |
|---|---|---|---|
| tiny noul flag (guardrail class) | 150 | $0.0063 | $6.30 |
| small choice (intent route) | 500 | $0.021 | $21.00 |
| medium choice+state (skill pick) | 2,000 | $0.084 | $84.00 |
| rerank pair (query+passage) | 2,000 | $0.084 | $84.00 |
| long-state decision (≤32k) | 32,000 | $1.34 | $1,344.00 |
- **Cheap enough for every act of every kid: the tiny/small sites only** (≤$0.021/1k). Medium and long-state sites must be gated (fan-out only where a cheap screen says "relevant").
- **deepseek-v4.1-flash comparison NOT MADE — its price was not measured on any page read in this slice.** Owner line in `papers/typesafe-ai.md` says jev ≈ "$0.045/Mtok in, output free" (OWNER-STATED); treat the deepseek ratio as a follow-up, not a number. Do NOT quote an invented figure.
- Caveat: no published per-decision price; all rows are ESTIMATE from token counts I did not measure per site (except cookbook request counts in slice 2).
## 9. ONE-LINE ANSWER
Jev's only published meter is **$42/Btok input, output free**; billing is **credit-per-Input** (free credits discretionary), quotas are **contract-only**, data is **not trained on, retained indefinitely, deleted on request, ZDR enterprise-only**, there is **no uptime SLA** (AS-IS), liability capped at **12-month fees or $50**, and **distillation/imitating outputs is contractually forbidden**.
