# datasets/magic-pane — STRICT labelled segments for the magic-pane detector (chunk 1)

Built by `.agi/context/local-maxxing/magic-pane/detect.py`. Chunk 1 only: a
passive, offline detector that predicts which structured form a recorded agent
segment is about to emit, from only the first N prose tokens it streamed.

**STRICT, after retest.** This directory supersedes the first run
(`experiment:a00-aecd4776-2f10c5`), whose gold labels counted *mentions* of
`.jsonl` / `.agi/nodes/*.md` as writes. A segment now counts only if its tool
call **PRODUCES** the form; a read (`cat`, `ls`, `grep`, `git log`) is never a
form. Strict predicates are in `report.md`.

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
  pre-form prose is **dropped** and counted per class
  (`dropped_short_prose` in `metrics_strict.json`; 40 is also the smallest N
  tested).
* `N=40` / `N=80` mean the first 40 / 80 `\S+` units of `prose`.

## What this corpus is, and is not

* Source: every recorded `output.log` under `/data/work/agi/.agi/sessions/` and
  `/data/work/agi/.agi/worktrees/*/.agi/sessions/`. **Recorded** excludes this
  round's `iter-MP.01` logs and any stream whose agent currently holds a lease
  in `.agi/sessions/.spawn-budget/*.lease` (a live stream is still growing).
  39 real segments (≥40 prose units) + 24 dropped = 63 real forms in total.
* **Missing classes:** `dm`, `merge_up` — zero instances. `write_note` has 1
  instance and cannot carry a per-class accuracy.
* `datasets/trajectories/*/trajectory.jsonl` carries tool calls only, **no
  prose**; `datasets/kid-sft/kid_sft.jsonl` is mostly finished node bodies, not
  pre-form prose; `.agi/sessions/write-log.jsonl` has no prose. None of them
  can supply segments. `.agi/comms/` message bodies ARE the dm form, so using
  them leaks the label.
* **No model measurement was run** — 63 < 200. `metrics_strict.json` records
  `corpus_sufficient: false`. The measured (fair, shuffled-label) path is
  retained in grid history for a future round that grows the corpus.

## Files

* `segments.jsonl` — one record per labelled segment:
  `{id, label, prose, form}`. `form` is the producing command — provenance
  only, never classifier input.
* `metrics_strict.json` — the strict census: real histogram, per-class drops,
  missing classes, thin classes, majority baseline, `corpus_sufficient`.
* `predictions.jsonl` — empty: no measurement was run.
* `metrics.json` — a copy of the strict census, so readers of the old path are
  not shown the superseded numbers.
* `report.md` — the full strict predicates, histogram and the corpus decision.

Model intended for a future measured run: `Qwen3.5-9B-Q4_K_M` on
`http://127.0.0.1:8080/v1`, `temperature 0`, `max_tokens 8`,
`chat_template_kwargs {"enable_thinking": false}`, requests serial.