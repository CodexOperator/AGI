# datasets/magic-pane — labelled segments for the magic-pane detector (chunk 1)

Built by `.agi/context/local-maxxing/magic-pane/detect.py`. Chunk 1 only: a
passive, offline detector that predicts which structured form a recorded agent
segment is about to emit, from only the first N prose tokens it streamed.

## The prose/form split (the leak trap, stated exactly)

A **segment** is one tool call in a recorded pi `--mode json` stream.

* **prose** = the concatenation of the assistant's `thinking_delta` and
  `text_delta` *deltas* (the `delta` field only, never `partial`) emitted
  between the previous `toolcall_start` (or the message start) and this
  `toolcall_start`.
* **form / label** = read ONLY from the paired `toolcall_end`'s
  `toolCall.name` + `toolCall.arguments`. Tool-call args are never shown to
  the classifier and never enter the prose buffer — a `toolcall_start` flushes
  the prose buffer.
* A segment with fewer than **40 whitespace token units** (`\S+` runs) of
  pre-form prose is **dropped** and counted (`dropped_short_prose` in
  `metrics.json`; 40 is also the smallest N tested).
* `N=40` / `N=80` mean the first 40 / 80 `\S+` units of `prose`. The model's
  own BPE tokenizer is not used offline; a `\S+` unit is 1–2 BPE tokens, so
  N units of prose is *at least* N model tokens — the input is therefore no
  smaller than the claim's N, which makes the accuracy bar if anything easier.

## Sources

| source | what | labels |
|---|---|---|
| `pi` | every `output.log` under the main repo and all worktrees (the round's own live log excluded); 19 streams, ABC.01/ABC.02 among them | `write_note`, `write_set`, `dm`, `merge_up`, `dispatch`, `bench_jsonl`, `node_write` |
| `comms` | message blocks (split on `---` frontmatter fences) in `.agi/comms/season-2/**/*.md` | `dm`, `merge_up` (leading `[tag]`) |

`comms` is a second stratum: its prose is the *body* of a message that was
sent, not the pre-form stream of a tool call. It is included only because the
pi streams contain almost no `dm`/`merge_up` segments (0 and 0 with >=40
tokens); per-source accuracy is reported separately in `metrics.json` and
`report.md` so the two strata never have to be pooled blindly.

## Files

* `segments.jsonl` — one record per labelled segment:
  `{id, source, session, label, prose, form}`. `form` is the tool-call
  command/path (pi) or the message header (comms) — provenance only, never
  classifier input.
* `predictions.jsonl` — `{id, condition, N, gold, pred, latency_s, source}`
  for every condition x N x segment.
* `metrics.json` — per condition x N: top-1 accuracy, majority baseline,
  median + p95 latency, label histogram, per-source accuracy, confusion.
* `report.md` — the same as markdown tables.

## Conditions

Two prompt conditions (same model, same segments, same labels):

* `fixed` — labels listed in `LAB` order. The 9B collapses onto the first
  listed label; this condition is reported to *show* that position bias.
* `shuffled` — the label order is deterministically reshuffled per segment
  (`random.Random(20260921)`), which removes the position bias in expectation.
  **`shuffled` is the fair condition**; the verdict rests on it.

Model: `Qwen3.5-9B-Q4_K_M` on `http://127.0.0.1:8080/v1`, `temperature 0`,
`max_tokens 8`, `chat_template_kwargs {"enable_thinking": false}` (required —
without it the endpoint returns empty `content`), requests serial.
