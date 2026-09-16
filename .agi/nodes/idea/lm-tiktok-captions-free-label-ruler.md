---
id: idea:lm-tiktok-captions-free-label-ruler
mint_id: b3f7e020069d4346a8a68d8e57400dd8
type: idea
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: 50faf4d5e89d8ba2
season: 2
tags:
  - local-maxxing
  - treasury
title: 4.5 B free engagement labels as the town's accuracy-per-weight-byte ruler
town: local-maxxing
---
# idea:lm-tiktok-captions-free-label-ruler

## Source
doc:tiktok-videos-4b — "TikTok Videos: 4.5 billion posts dataset" (pretty_name "TikTok Videos, 4.5 Billion") (https://huggingface.co/datasets/kuben-developer/tiktok-videos-4b); digest `.agi/context/local-maxxing/papers/tiktok-videos-4b.md`; critic grounded=4/5 — Source facts check out (canonical still 401; Wayback, mirror API/tree and card quotes all byte-verified); errors are the mirror count/date, sample-row count, a 7.7 KB slip in the parquet total, and an idea seed built on four unsupported numbers plus a views-quartile target the card itself warns against; a footer range read (166 row groups, ~68 B/caption) replaces the 10.7 GB download in the corrected test.

## Lever
The source saves exactly one cost, labelling: five engagement counters, is_ad, language and a music_id join key ship on every one of 4.5 B rows (166,423,554 rows in videos-00 alone per its footer) and the parquet is HTTP-range readable so a ~5 M-row, ~275 MB sample needs no full download; it saves no bytes/token or FLOPs/token itself but is the fixed job on which candidates from an E3 byte-LUT to Qwen3-0.6B Q8 are ranked by accuracy per weight byte and per byte touched per token.

## What it buys the town
A standing supervised leaderboard the town runs on its own iron (duckdb on encryption-town, byte baselines and 0.6B label log-prob scoring on the swarm box, no GPU) as the byte-neuron/flip thread's first real task, with saves>0 as the target the card itself calls the earliest signal, plus a music_id join graph as the cheapest recommender toy for the two-tiny-models vision.

## First falsifier
On ~100 k rows drawn from at least 5 row groups spread across one file and restricted to a 30-day create_time window (so snapshot age is comparable), if neither a byte-n-gram logistic baseline nor Qwen3-0.6B Q8 label log-prob beats majority class on saves>0 by more than split-to-split noise, captions carry no learnable signal and the corpus is dead as a ruler.

## Cheapest test on our iron
encryption-town (8 GB RAM, 352 GB /data) range-reads the 301 KB footer plus row groups 0/40/80/120/160 (~275 MB, LFS sha256 01ddc77b... recorded) of blaccastro/tiktok-videos-4b videos-00.parquet with duckdb httpfs or pyarrow, filters desc <> '' and one 30-day window into a ~5 MB 100 k-row parquet, and the swarm box trains the byte-n-gram baseline and scores Qwen3-0.6B Q8 by label log-prob on 1 k rows, prefill-bound and under an hour at the measured 34-45 tok/s decode, $0 and no GPU-hour, contingent on a mirror still answering 200.

## Numbers (quoted in the digest)
- rows=4,501,811,789 (Wayback page JSON numRows; card footer)
- parquet_files=27, zstd (card; mirror /tree/main videos-00..videos-26)
- total_bytes=289,467,105,802 ~= 289.5 GB (sum of mirror tree sizes; card: "about 289 GB")
- per_file=10.69-10.76 GB, "roughly 167 million videos" (mirror tree; card)
- compressed_bytes_per_row~=64.3 (computed: 289,467,105,802 / 4,501,811,789)
- columns=16 (card table)
- partition_coverage=27 of 32 (card)
- pre_dedup_duplicates~=10% (card)
- collection_window="roughly three weeks" (card); sample create_time 2024-02-11..2025-11-13 (Data Studio rows)
- canonical_downloads/likes=8,167/291 on 2026-09-09 (Wayback JSON); 6,488/204 on 2026-09-07 (.agi/nodes/goal/g14.md line 102)
- canonical createdAt=2026-09-02T16:35:31Z, lastModified=2026-09-08T08:14:14Z (Wayback JSON)
- canonical_http_2026-09-16=401 on page, API and raw README

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
