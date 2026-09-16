---
id: doc:tiktok-videos-4b
mint_id: 6b47004b48144fc1ae50946421f3e7af
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/tiktok-videos-4b.md
scaffold_hash: 460abf6ec9e26c77
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"TikTok Videos: 4.5 billion posts dataset\" (pretty_name \"TikTok Videos, 4.5 Billion\")"
town: local-maxxing
---
# doc:tiktok-videos-4b

**Source:** https://huggingface.co/datasets/kuben-developer/tiktok-videos-4b
**Digest (link_ref):** `.agi/context/local-maxxing/papers/tiktok-videos-4b.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=4/5).
**Critic note:** Source facts check out (canonical still 401; Wayback, mirror API/tree and card quotes all byte-verified); errors are the mirror count/date, sample-row count, a 7.7 KB slip in the parquet total, and an idea seed built on four unsupported numbers plus a views-quartile target the card itself warns against; a footer range read (166 row groups, ~68 B/caption) replaces the 10.7 GB download in the corrected test.
**Seeds:** idea:lm-tiktok-captions-free-label-ruler

## Relevance to local-maxxing
It touches none of the compute levers directly — no bytes/token, looped-transformer, KV or oscillator content; the text column is a short caption (sample rows are empty or one hashtag) so it is not a pretraining corpus. What it buys g14 is free supervision at scale: five engagement counters, is_ad, language and a music_id join key per row give a fixed, cheaply scored job on which the E3 byte-neuron LUT (kilobytes of weights) and Qwen3-0.6B Q8 (~0.6 GB, 34-45 tok/s) can be ranked on the same rows as accuracy per weight byte — the "smallest model that does the job" made measurable — plus a music_id join graph as a recommender toy for the two-tiny-models vision. It fits the cluster (one 10.7 GB file on encryption-town's 352 GB /data, duckdb in place, tens-of-MB samples over the overlay) but carries stated GDPR/ToS baggage and the canonical repo went dark between 2026-09-09 and 2026-09-16, so any run must record the mirror sha it drew from and keep only a stratified sample.
