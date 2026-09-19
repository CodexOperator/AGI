---
id: experiment:a00-2132d69a-6fefcb
mint_id: 102a9cfd7b834642ad36cecb7b624b73
type: experiment
parents:
  - hypothesis:lm-jev-docs-hunt
next_edges: []
edited_by: a00-2132d69a
line_ceiling: 120
loop: hypothesis:lm-jev-docs-hunt@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: ef4786764e56c2c9
season: 2
title: "pricing-legal kid: TypeSafe price corrected to $0.042/Mtok in + $0 output, billing per-Input credit, MCA §2.3(b)/(f) and §4.3 Telemetry tripwires"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:a00-2132d69a-6fefcb

## Experiment

Kid `pricing-legal` under `hypothesis:lm-jev-docs-hunt`. Verb was: hunt
typesafe.ai + docs.typesafe.ai for pricing, billing granularity, data handling,
security posture, and binding terms; confirm or correct the owner-stated
"$0.045 per million input tokens, $0 output"; visit >= 12 distinct pages; fetch
with `curl -sL` + python3 tag-strip, no key, no auth, no paid API.

Deliverable: `.agi/context/local-maxxing/troves/2026-09-18-typesafe/pricing-legal.md`
(19,195 bytes, seven required sections + a "what changed" list), written
2026-09-18 ~02:35Z.

What happened, in order:

1. Enumerated both sites from their sitemaps:
   `typesafe.ai/sitemap.xml` (12 URLs) and `docs.typesafe.ai/sitemap.xml`
   (111 URLs). `typesafe.ai/pricing` returns **404**; neither sitemap has a
   pricing/billing/security page.
2. Found the price in the docs, not on a pricing page:
   **`docs.typesafe.ai/models.md`** — "Price (per Btok / per Mtok) $42 / $0.042",
   "Charged per input token. Output tokens are free." Repeated on the launch
   blog `typesafe.ai/blog/introducing-system-one-models-and-jev`.
3. **Correction landed:** the owner-stated **$0.045 / 1M is wrong**; the
   published figure is **$0.042 / 1M input, $0 output**. The owner number is
   ~7% high and remains unconfirmed on any page.
4. Billing granularity from the Master Customer Agreement (§8): a **Credit
   consumed per Input submitted** (not per-seat, not per-question), 12-month
   credit expiry, discretionary Promotional Credits, no published minimum.
   Console billing is auth-walled (`console.typesafe.ai`) and was skipped.
5. Data handling: no training on Input (Privacy Policy + MCA §4.1), but
   **Telemetry is unrestricted (MCA §4.3)** — the sharpest clause. ZDR is
   **enterprise-only**; US-hosted; no numeric retention period; post-termination
   TypeSafe may delete Customer Data at its sole discretion (MCA §10.3).
6. Security: only "reasonable efforts" published. Specific measures sit behind
   **trust.typesafe.ai**, a Vanta-hosted SPA whose static HTML carries the title
   and nothing else — not machine-readable. No SOC 2 / encryption claim found.
7. Binding terms: Output assigned to Customer (MCA §4.2); liability capped at
   the greater of 12-month fees or **$50** (§12.2); **§2.3(b) bars distilling
   or training a competing model on Output, and §2.3(f) bars publishing
   benchmarks of the Services** — both directly touch the town's local-kid plan.
8. 22 distinct URLs fetched, 12+ readable; two Vanta trust-center URLs were
   unreadable and one (console) was auth-required and logged, not authenticated.

## Evidence

- Pages visited: 22 distinct URLs, table in the digest with URL + fetch date and
  a MEASURED/ESTIMATE tag per row.
- Price quotes: `$42 / $0.042` (docs.typesafe.ai/models.md, doc lastmod
  2026-09-17; blog fetched 2026-09-18). Both MEASURED.
- `typesafe.ai/pricing` HTTP status **404**.
- `trust.typesafe.ai` and `/subprocessors` both return an identical 6,914-byte
  Vanta SPA shell with no static content.
- Cost arithmetic (ESTIMATE, own): 2k-token decision = $0.000084 → $0.084 per
  1000 decisions; the 200-decision replay ≈ **$0.0168**, not the $0.02 on the
  idea node.
- Raw HTML/text cached in this session's scratch dir
  (`.agi/sessions/iter-TM.28/a00-2132d69a/` is reserved; the fetched copies were
  held under /tmp/ts during the round).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version: the round's digest plus this experiment record. The two findings
that changed the round's shape: (1) pricing is published but at $0.042, not the
owner's $0.045, so the kid brief's "confirm or say unconfirmed" resolves to
"corrected" and every downstream cost estimate on the idea node needs recomputing;
(2) the binding risk is not training (explicitly promised away in two places) but
MCA §4.3 Telemetry (unrestricted) and §2.3(b)/(f) (no distillation, no published
benchmarks) — which the town's persona-LoRA and 200-replay plans walk straight
into. Recorded both, plus the unreadable Vanta trust center as an ABSENT rather
than a guess. No code changed; digest + node only.
<!-- THOUGHT:END -->
