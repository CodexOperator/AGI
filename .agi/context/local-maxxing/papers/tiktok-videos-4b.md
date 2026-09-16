# "TikTok Videos: 4.5 billion posts dataset" (kuben-developer/tiktok-videos-4b)

Source key: `tiktok-videos-4b`. Kind: dataset (HF Hub). Owner hint, verbatim
(2026-09-07 19:47 UTC): "Record following link and info under the localmaxxing goal".
Digested 2026-09-16 by a read-stage subagent; nothing below is from memory —
every number carries the URL it was read from.

## Provenance

| What | URL | HTTP | Bytes | Note |
|---|---|---|---|---|
| Canonical repo, HF API | https://huggingface.co/api/datasets/kuben-developer/tiktok-videos-4b | **401** | 41 | `{"error":"Invalid username or password."}` — the same body HF returns for a nonexistent or private repo; a control call to `api/datasets/HuggingFaceFW/fineweb` returned 200, and `api/datasets?author=kuben-developer` returned `[]` (200). The canonical repo is **not publicly reachable on 2026-09-16**. |
| Canonical repo, HTML page | https://huggingface.co/datasets/kuben-developer/tiktok-videos-4b | 401 | 52,325 | renders `<title>404 – Hugging Face` |
| Canonical README raw | https://huggingface.co/datasets/kuben-developer/tiktok-videos-4b/raw/main/README.md | 401 | 29 | |
| Author page | https://huggingface.co/kuben-developer | 200 | 73,059 | `<title>kuben-developer (Kuben)` — the account exists |
| **Wayback snapshot of the canonical page** | https://web.archive.org/web/20260909161509/https://huggingface.co/datasets/kuben-developer/tiktok-videos-4b | 200 | 918,097 | captured 2026-09-09 16:15:09 UTC; the card body, column schema, sample rows and the page's embedded JSON metadata below are all read from this |
| Wayback CDX index | https://web.archive.org/cdx/search/cdx?url=huggingface.co/datasets/kuben-developer/tiktok-videos-4b*&output=json&limit=20 | 200 | — | 11 captures of the page between 2026-09-03 06:19 and 2026-09-09 16:15; none later |
| **Live mirror, HF API** | https://huggingface.co/api/datasets/blaccastro/tiktok-videos-4b | 200 | 2,844 | `createdAt 2026-09-09T03:44:20Z`, `private: false, gated: false, disabled: false`, downloads 259, likes 2; same card text and cardData as the canonical |
| Live mirror, file tree | https://huggingface.co/api/datasets/blaccastro/tiktok-videos-4b/tree/main | 200 | 8,460 | 29 entries: `.gitattributes`, `README.md`, `videos-00.parquet` … `videos-26.parquet`; per-file sizes summed below |
| HF search | https://huggingface.co/api/datasets?search=tiktok-videos-4b | 200 | — | two mirrors exist: `blaccastro/tiktok-videos-4b` and `dams2005/tiktok-videos-4b` (459 downloads) |
| Repo record (secondary) | `/home/ubuntu/work/agi/.agi/nodes/goal/g14.md` line 102 | local | — | Belam VI's 2026-09-07 note from the then-live HF API/README: "6488 downloads, 204 likes, last modified 2026-09-02" — consistent with the Wayback numbers below |

Not fetched: any parquet bytes (10.7 GB each); the scraper write-up at
tiktok-api.seeksocial.io (linked from the card, not opened).

## Summary (measured lines)

- The card's own description (Wayback 2026-09-09): "4.5 billion TikTok video records with captions, engagement counts, sound identifiers and timing. Collected from TikTok's mobile API over roughly three weeks. Every content_id appears exactly once." Row count from the page's dataset-server JSON: `"numRows":4501811789`.
- Storage (card): "27 Parquet files, zstd compressed, about 289 GB in total. One row per video." … "One file is about 10 GB and holds roughly 167 million videos, so start with a single file before pulling all 27." The mirror's tree confirms 27 files of 10,692,560,875–10,761,008,262 bytes, total 289,467,105,802 bytes = 289.5 GB, i.e. **~64.3 compressed bytes per row**.
- Schema (16 columns, from the card table and the Data Studio header): `content_id uint64, create_time timestamp[ms,UTC], desc string, mentions list[uint64], duration uint16, is_video uint8, music_id uint64, music_title string, views/likes/comments/shares/saves uint64, country string, language string, is_ad uint8`. "Creator identity is not included. There is no author ID, username or profile data." "Media URLs are not included."
- Sampling and ordering caveats stated by the author: "This is 27 of 32 storage partitions, split on a hash of the creator ID"; "Rows are grouped by creator, not shuffled … If you are training on this, shuffle"; "The counts are a snapshot, not a time series"; "The source table had about 10% repeat rows … collapsed"; "`country` and `language` are TikTok's labels, inferred by them, not verified. They are wrong often enough that you should not treat them as ground truth." The 60-odd sample rows visible in the Data Studio all carry `language = "un"` (undetermined) and captions that are empty or a single hashtag (`#onthisday`, `#CapCut`).
- Licence/legal (card): "Released for research and educational use." "this dataset is personal data under GDPR, the UK GDPR and CCPA regardless of the fact that it was publicly posted." "Collection was contrary to TikTok's terms of service." Card metadata: `license: other, license_name: research-use`, languages `en, es, pt, id, ar`, tasks `text-classification, text-generation, feature-extraction`.
- Availability on 2026-09-16: the canonical `kuben-developer` repo answers 401 to every unauthenticated call (page, API, raw README) while the account page is live and lists zero public datasets; the last Wayback capture is 2026-09-09 (8,167 downloads, 291 likes, `lastModified 2026-09-08T08:14:14Z`). Two forks created 2026-09-09 are live and ungated. Read this as: the original is private or taken down; the bytes survive in mirrors for now.

## Numbers

- rows = 4,501,811,789 (Wayback page JSON `numRows`; card footer "Number of rows: 4,501,811,789")
- files = 27 parquet, zstd (card; mirror tree lists videos-00 … videos-26)
- total size = 289,467,105,802 bytes ≈ 289.5 GB (sum of mirror tree `size` fields; card says "about 289 GB")
- per file = 10.69–10.76 GB, "roughly 167 million videos" each (mirror tree; card)
- compressed bytes/row ≈ 64.3 (289,467,105,802 / 4,501,811,789, computed here)
- columns = 16 (card table)
- coverage = "27 of 32 storage partitions" (card)
- duplicate rate before dedup ≈ "about 10%" (card)
- collection window = "roughly three weeks" (card); sample `create_time` values span 2024-02-11 to 2025-11-13 (Data Studio rows in the Wayback capture)
- canonical downloads/likes = 8,167 / 291 on 2026-09-09 (Wayback JSON); 6,488 / 204 on 2026-09-07 (g14.md line 102)
- canonical `createdAt` = 2026-09-02T16:35:31Z, `lastModified` = 2026-09-08T08:14:14Z (Wayback JSON)
- mirror blaccastro: created 2026-09-09T03:44:20Z, 259 downloads (HF API 2026-09-16); mirror dams2005: 459 downloads (HF search 2026-09-16)
- canonical HTTP on 2026-09-16 = 401 (three URLs, see Provenance)

## Relevance to local-maxxing

**What it is not.** This corpus touches none of the town's compute levers. It
says nothing about bytes-per-token, depth recurrence, KV cache, quantisation,
head pruning or oscillators; it is a labelled table, not a technique. It is also
not a pretraining corpus in any useful sense: the text column is a short caption
(the visible sample rows are empty strings or one hashtag), at ~64 bytes per
whole row compressed, so 4.5 B rows is on the order of the *rows* of a web
corpus, not its tokens. Its one link to the "old oscillator friend" is nil.

**What it buys a smallest-model town.** Free supervision at scale. Every row
carries five engagement counters, a language tag, an ad flag and a sound-id join
key, with no labelling cost. That is exactly the shape of task g14's ruler needs:
a job with a ground truth, cheap to score, where the town can ask *how small a
model still does it* — and where the E3 byte-neuron LUT cascade (weights in the
kilobytes) can sit on the same leaderboard as Qwen3-0.6B Q8 (~0.6 GB, 34–45 tok/s
on the swarm box), scored as accuracy per weight byte touched. Concretely: (a) a
caption→engagement-bucket or caption→`saves>0` classifier as a byte-level
distillation/eval target; (b) `is_ad` and `language` as noisy-label tasks (the
author warns `language` is often wrong — a test of robustness, not truth);
(c) the `music_id` join as a recommender toy for vision 3 ("two or more tiny
models together"). It fits the iron: one 10.7 GB file on encryption-town's 352 GB
`/data` (the owner named the archive box for datasets), duckdb-queried in place,
sampled to a few tens of MB before anything crosses the WireGuard overlay to the
swarm box.

**Costs the town must weigh.** The author states the data is GDPR/CCPA personal
data and was collected against TikTok's ToS; the canonical repo went dark
between 2026-09-09 and 2026-09-16 and only forks remain. Any experiment should
keep a stratified sample, never the full 289 GB, never re-publish rows, and
record the mirror URL and sha it was drawn from, since the source may vanish
again. The sample rows also warn that most captions are near-empty: the first
measurement is whether captions carry any signal at all, before any model is
argued over.

## Idea seed

- **slug:** `lm-tiktok-captions-free-label-ruler`
- **title:** 4.5 B free engagement labels as the town's accuracy-per-weight-byte ruler
- **lever:** One 10.7 GB parquet file yields ~167 M caption→engagement rows at zero labelling cost, giving the town a fixed supervised job on which every candidate — from an E3 byte-LUT with kilobytes of weights to Qwen3-0.6B Q8 at ~0.6 GB — is scored on the same rows as accuracy per weight byte touched, which is the g14 quantity "smallest model that does the job" made measurable.
- **buys:** A standing leaderboard the town runs on its own iron (duckdb on encryption-town, byte baselines and 0.6B zero-shot on the swarm box, no GPU) for the byte-neuron/flip thread's first real supervised task, plus a `music_id` join graph as the cheapest recommender toy for the "two tiny models beat one" vision.
- **first falsifier:** On a 100 k-row stratified sample (`desc` non-empty, one bucket per views quartile), if neither a byte-n-gram logistic baseline nor Qwen3-0.6B Q8 zero-shot beats majority class on views-quartile or `saves>0` by more than the split's noise, captions carry no learnable signal and the corpus is dead as a ruler.
- **cheapest test on our iron:** encryption-town pulls `videos-00.parquet` (10.7 GB) from a live mirror onto `/data`, duckdb samples 100 k rows to ~20 MB, the swarm box trains a byte-n-gram logistic baseline in minutes and scores Qwen3-0.6B Q8 zero-shot on 1 k rows (~1 k prompts × ~50 tok at 34–45 tok/s ≈ 25 min), total $0 and no GPU-hour — provided the mirror still answers 200 (the canonical was 401 on 2026-09-16).

## Critique (adversarial, 2026-09-16)

Re-fetched every URL in the Provenance table on 2026-09-16 with the same
methods (curl, `-A 'Mozilla/5.0'`), plus one thing the reader did not do: an
HTTP range read of the parquet footer of `videos-00.parquet` on the
`blaccastro` mirror (301,128 bytes of footer, no row data). Canonical repo
still 401 on all three URLs (API 41 B `{"error":"Invalid username or
password."}`, page 52,325 B titled `404 – Hugging Face`, raw README 29 B);
`api/datasets?author=kuben-developer` → 200 `[]`; author page → 200 (72,937 B,
`<title>kuben-developer (Kuben)`). Wayback capture → 200, 918,100 B (3 bytes
off the reader's 918,097 — the archive banner varies; not an error). CDX → 200,
11 page captures 20260903061941…20260909161509. Mirror API → 200, 2,844 B;
tree → 200, 8,460 B, 29 entries. HF search → 200, 23,032 B.

**Verified as quoted** (bytes match): numRows 4,501,811,789; 27 parquet files,
per-file 10,692,560,875–10,761,008,262 B; "about 289 GB"; "roughly 167
million"; "27 of 32"; "about 10%"; "roughly three weeks"; "grouped by
creator, not shuffled"; "snapshot, not a time series"; "wrong often enough";
"Creator identity is not included"; "Media URLs are not included"; "Released
for research and educational use"; GDPR/UK GDPR/CCPA and "contrary to
TikTok's terms of service"; canonical downloads 8,167 / likes 291 /
createdAt 2026-09-02T16:35:31Z / lastModified 2026-09-08T08:14:14Z; mirror
blaccastro createdAt 2026-09-09T03:44:20Z, downloads 259, likes 2,
private/gated/disabled false, sha `948afdf8220e9845a95366c45009c0e664657e28`;
dams2005 downloads 459; cardData license other / research-use, languages
en,es,pt,id,ar, tasks text-classification, text-generation,
feature-extraction; sample create_time span 2024-02-11T20:13:41 …
2025-11-13T13:32:51; language = "un" on every sample row.

### Errors (digest claim → what the source says → where)

1. **"total size = 289,467,105,802 bytes (sum of mirror tree size fields)"
   over videos-00..26** → that figure includes `.gitattributes` (2,504 B) and
   `README.md` (5,197 B). The 27 parquet files alone sum to
   **289,467,098,101 B**; bytes/row is still 64.30. (mirror `/tree/main`)
2. **"~60 Data Studio sample rows" / "The 60-odd sample rows"** → the
   embedded `sampleData.rows` array holds **100 rows**. Of those: `desc` is
   "" on 34, "#CapCut " on 48, "#onthisday " on 12, "#Mureka " on 4, and two
   rows carry 2–3 hashtags; country US 65 / MM 35; views 8–855; `is_ad` 0 on
   all 100; `saves>0` on 16. (Wayback capture JSON)
3. **"two mirrors exist" and "Two forks created 2026-09-09 are live"** →
   `api/datasets?search=tiktok-videos-4b` returns **16** repos named
   `tiktok-videos-4b` (blaccastro, dams2005, 0xd4t4, alex12223322, kkndlee,
   hojj, grimboy, kunalmiind, ansulev, mrfakename, seanphan,
   abdellatifinformation, merway, kwakuobeng, KOM-00, utopiar), created
   2026-09-02 … 2026-09-15. **dams2005 was created 2026-09-02T17:55:00Z**
   (80 min after the canonical), not 2026-09-09; only blaccastro dates from
   2026-09-09. (HF search JSON; `api/datasets/dams2005/tiktok-videos-4b`)
4. **"most captions are near-empty" / "the text column is a short caption
   (the visible sample rows are empty strings or one hashtag)"** as a
   property of the corpus → the 100 sample rows are the head of a
   creator-grouped file (the card: "Rows are grouped by creator, not
   shuffled") and are not a sample of anything. The footer of
   `videos-00.parquet` (mirror, HTTP range 206) says: **166 row groups,
   166,423,554 rows, 16 columns**; row group 0 has 1,005,985 rows with
   `desc` at **68,595,253 B uncompressed / 22,324,106 B zstd**, i.e. ~68 B
   per caption on average (plain-encoded, includes 4 B length prefix) —
   short, but not "near-empty". The reader's "first measurement is whether
   captions carry any signal at all" survives; the premise that they are
   mostly empty does not.
5. **Idea: "Qwen3-0.6B Q8 at ~0.6 GB"** → appears in neither the source nor
   the town's frame (which gives 34–45 tok/s, no size). Unsupported number.
6. **Idea: "~1 k prompts × ~50 tok at 34–45 tok/s ≈ 25 min"** → reader
   arithmetic, not source; 50,000 tok / 34 = 24.5 min, / 45 = 18.5 min, and
   it omits prefill of the prompt (caption + instruction) on a CPU box. A
   label needs 1–5 output tokens, or zero if scored by label log-prob, so
   the generation budget is over-stated by ~10×.
7. **Idea: "duckdb samples 100 k rows to ~20 MB"** → unsupported. From the
   footer: row groups are 786,156–1,007,842 rows and 48.4–60.7 MB zstd each,
   so 100 k rows ≈ 5.5 MB zstd parquet (≈ 13 MB uncompressed).
8. **Idea: "trains a byte-n-gram logistic baseline in minutes"** → no
   measurement anywhere; plausible for 100 k × ~68 B rows, but a guess.
9. **Falsifier "views quartile"** contradicts the source's own warning:
   "Every engagement number is whatever it was at the moment that row was
   collected, somewhere in a three week window … Do not compare raw counts
   across distant create_time values without normalising for age." A views
   quartile over rows posted 2024-02 … 2025-11 mixes age with popularity.
   The card names the better target itself: `saves` — "Bookmarks. Often the
   earliest signal that something is moving."
10. **Cheapest test "encryption-town pulls videos-00.parquet (10.7 GB)"** → not
    necessary and, on a creator-grouped file, not even the right cut. The
    mirror's `resolve/main/videos-00.parquet` answers **HTTP 206** to range
    requests (`accept-ranges: bytes`, `content-range: bytes 0-0/10697285411`),
    so duckdb `httpfs` / pyarrow can read the 301 KB footer plus a handful
    of ~55 MB row groups spread across the file (row groups 0, 40, 80, 120,
    160 ≈ 275 MB) and get ~5 M rows from five different creator clusters,
    without a 10.7 GB download over the WireGuard overlay.
11. **Lever: "a fixed supervised job … scored as accuracy per weight byte"**
    is a ruler, not a cost-saving mechanism, and the task standard asks for a
    mechanism the source demonstrates. The source demonstrates exactly two
    cost properties: labels at $0 (engagement counters, `is_ad`, `language`,
    `music_id` ship with every row) and "Query it without loading it. No
    unpacking, no full download needed" (duckdb over parquet). The reader's
    own Relevance section already concedes the corpus touches no compute
    lever; the lever should say so and claim only the labelling/eval-build
    cost it saves.
12. Minor: the card's column table says `create_time datetime`; the
    `timestamp[ms, tz=UTC]` type is the Data Studio header only. The digest
    merges the two without saying which said what. Also the mirror tree
    exposes an LFS sha256 per file (`videos-00.parquet` lfs.oid
    `01ddc77b19a47b1f0f606b3a1feac17928ee007dcbd5e39ec8b76c44b144c16f`), which
    is the thing to record for reproducibility, not the repo sha alone.

### Not errors, but not source-traceable

- "6,488 downloads / 204 likes on 2026-09-07" comes from
  `.agi/nodes/goal/g14.md` line 102 (Belam VI's note), correctly labelled as
  secondary; it cannot be re-verified now that the canonical is 401.
- "one 10.7 GB file on encryption-town's 352 GB /data" — encryption-town has 8 GB
  RAM; duckdb reads parquet out-of-core, so it fits, but nothing measured.

### Corrected idea seed

- **slug:** `lm-tiktok-captions-free-label-ruler`
- **title:** 4.5 B free engagement labels as the town's accuracy-per-weight-byte ruler
- **lever:** The source saves exactly one cost — labelling — by shipping
  five engagement counters, `is_ad`, `language` and a `music_id` join key on
  every one of 4.5 B rows (mirror footer: 166,423,554 rows in `videos-00`
  alone), plus HTTP-range parquet so a 5 M-row, ~275 MB sample costs no
  full download; it saves no bytes/token or FLOPs/token itself, it is the
  fixed job on which candidates from an E3 byte-LUT to Qwen3-0.6B Q8 are
  ranked by accuracy per weight byte and per byte touched per token.
- **buys:** A standing supervised leaderboard the town runs on its own iron
  (duckdb on encryption-town, byte baselines and 0.6B log-prob scoring on the
  swarm box, no GPU) as the byte-neuron/flip thread's first real task, with
  `saves>0` as the target the card itself calls the earliest signal, and a
  `music_id` join graph as the cheapest recommender toy.
- **first falsifier:** On ~100 k rows drawn from ≥5 row groups spread across
  one file, restricted to a 30-day `create_time` window so snapshot age is
  comparable, if neither a byte-n-gram logistic baseline nor Qwen3-0.6B Q8
  label log-prob beats majority class on `saves>0` by more than
  split-to-split noise, captions carry no learnable signal and the corpus is
  dead as a ruler.
- **cheapest test on our iron:** encryption-town (8 GB RAM) uses duckdb `httpfs`
  or pyarrow to range-read the footer plus row groups 0/40/80/120/160 of
  `blaccastro/…/videos-00.parquet` (~275 MB, LFS sha256 recorded), filters to
  `desc <> ''` and one 30-day window, writes a ~5 MB 100 k-row parquet; the
  swarm box trains the byte-n-gram baseline and scores Qwen3-0.6B Q8 by
  label log-prob on 1 k rows (prefill-bound, well under an hour at the
  measured 34–45 tok/s decode); $0, no GPU-hour, contingent on a mirror still
  answering 200.
