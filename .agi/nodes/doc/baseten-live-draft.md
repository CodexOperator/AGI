---
id: doc:baseten-live-draft
mint_id: 084c8cdf3cc947b8bc332166be4aab1e
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/baseten-live-draft.md
scaffold_hash: 37dd1dd6ce97b1a9
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"Live draft model training for speculative decoding\""
town: local-maxxing
---
# doc:baseten-live-draft

**Source:** https://www.baseten.co/blog/live-draft-model-training-for-speculative-decoding/
**Digest (link_ref):** `.agi/context/local-maxxing/papers/baseten-live-draft.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=4/5).
**Critic note:** Source half fully grounded (all quotes/numbers byte-match; NOT-GIVEN list confirmed by grep, engine is proprietary, no open engine named); every error is reader-side arithmetic or mechanism gloss in the idea seed; corrected seed drops live/EAGLE-3/SGLang/CPU-refit packaging for an offline SFT refit gated on H7.
**Seeds:** idea:lm-draft-refit-own-traffic

## Relevance to local-maxxing
Speculative decoding leaves the target's bytes untouched and divides them by accepted tokens per verify step, so accept rate is the divisor on the bytes-per-token ledger; this blog measures that the divisor drifts with traffic and that refitting the draft on served hidden states moves it +20% median, +100% on narrow traffic, which is the regime the town's repetitive kid/parent prose lives in. The loop's shape (target serves, hidden states streamed off-box, draft trained elsewhere) maps onto local-town serving while the Ryzen or swarm-box CPUs refit a 16-100 MB head over the gigabit LAN, though the blog trains on GPU nodes and says nothing about CPU. For the looped transformer the per-loop hidden state is the same tap feeding early-exit calibration and draft training; for the flip/SNN thread the draft is a cheap oscillator predicting flips verified by the full cascade; the harness cost is a serving engine that exposes per-iteration hidden states (SGLang yes, llama.cpp not out of the box).
