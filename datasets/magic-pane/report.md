# Magic-pane chunk 1 — STRICT corpus census (retest of `experiment:a00-aecd4776-2f10c5`)

Harness: `.agi/context/local-maxxing/magic-pane/detect.py` (strict labeler +
census). Data: `datasets/magic-pane/segments.jsonl`,
`metrics_strict.json`. **No model measurement was run** — see why below.

A stream is **recorded** only if its agent holds no lease in
`.agi/sessions/.spawn-budget/*.lease` and it is not this round's `iter-MP.01`.
A live agent's `output.log` is still growing (EF.01/EF.02/EF.03 were writing
while this census ran, and the count drifted 38 -> 41 before the lease rule was
applied), so live streams are excluded to keep the census reproducible.

## Why the previous run does not test the hypothesis

The landed 237-segment set gold-labelled *any* command or path that merely
MENTIONS `.jsonl` or `.agi/nodes/*.md` as a form (`detect.py:label_of` returns
the first `RULES` regex match over `command + " " + path`). `cat`, `ls`,
`grep`, `git log` were therefore labelled `bench_jsonl` / `node_write`. A
segment counts only if its tool call **PRODUCES** the form.

## Strict predicates (a read is never a form)

| label | produced by |
|---|---|
| `write_note` | `write.py <node> '… note …'` with a `note` verb |
| `write_set` | `write.py <node> '… set …'` with a `set` verb |
| `dm` | `send.py send` / `send.py dm` (NOT `send.py read`) |
| `merge_up` | emitting a `[merge-up]` line — a text emission, not a tool call |
| `dispatch` | `dispatch.py <project> <ITER.x> …` (not `--help`, not `grep`/`sed` of the file) |
| `bench_jsonl` | `>> …jsonl`, `tee …jsonl`, `json.dump` into a `.jsonl`, `open(…jsonl, "a"/"w")` |
| `node_write` | the `write`/`edit` tool on a `.agi/nodes/…` path, or `write.py … create` |

Prose/form split unchanged from the README: prose = `thinking_delta` +
`text_delta` deltas before `toolcall_start`; form read ONLY from the paired
`toolcall_end`; `\S+` token unit; `< 40` units dropped and counted per class.
This round's own live `iter-MP.01` logs are excluded.

## Real per-class histogram (recorded pi streams, all worktrees + main repo)

| label | real (≥40 prose tokens) | dropped (<40) | total real forms |
|---|---|---|---|
| write_set | 12 | 5 | 17 |
| dispatch | 11 | 11 | 22 |
| bench_jsonl | 8 | 2 | 10 |
| node_write | 7 | 4 | 11 |
| write_note | 1 | 2 | 3 |
| **dm** | **0** | **0** | **0** |
| **merge_up** | **0** | **0** | **0** |
| **total** | **39** | **24** | **63** |

* Majority baseline 0.3077 (`write_set` at 12/39).
* **Missing classes:** `dm`, `merge_up`.
* **Thin classes (<5):** `write_note` (1) — cannot carry a per-class accuracy;
  `bench_jsonl` (8), `node_write` (7) are marginal.
* Even ignoring the 40-token threshold, the recorded corpus holds **63** real
  forms in total — below the 200 the hypothesis requires.

## The other named corpora cannot supply the missing prose

| corpus | shape | why it cannot carry a segment |
|---|---|---|
| `datasets/trajectories/*/*/trajectory.jsonl` | `{ts, tool, args, result}` — tool calls only | **no prose / thinking deltas at all** |
| `datasets/kid-sft/kid_sft.jsonl` | 354 SFT examples; 344 are node-body-only, `trajectory_available=false` | assistant text is the finished node body, not pre-form prose |
| `.agi/sessions/write-log.jsonl` | 263 `{actor, node_id, operation, path, sha256, ts}` rows | **no prose** — a log of forms already produced |
| `.agi/comms/season-2/**/*.md` | sent message bodies | the dm form **is** the body — using it leaks the label |

## Where the missing classes' prose would have to come from

* **`dm`** — a `send.py send|dm` tool call. Across the 22 recorded `output.log`
  streams there are **16 `send.py read` and zero `send.py send|dm`** calls: kids
  report with `cli.py done`, they do not dm. The live stream of a round's
  *director* is the only place a dm is produced, and this round's director log
  is excluded by rule (it is live). A live, captured director round is the one
  stream that would supply `dm` segments.
* **`merge_up`** — `[merge-up]` is emitted as a prose line, not a structured
  tool call. In the corpus it appears only inside file contents written by tool
  calls (e.g. a `echo '[merge-up]'` template) and in this round's own live
  director log. There is no recorded segment that *ends in* a merge-up
  emission.

## Decision

**No measurement is forced.** 39 (or at most 63) real segments < 200, and two
of seven classes have zero instances, so the zero-shot classifier's top-1
cannot be computed as the hypothesis defines it. The harness keeps the strict
labeler and the census; the measured path (a fair, label-order-shuffled
zero-shot run at N=40/80) is retained in grid history and must be re-added if a
future round grows the corpus past 200.

Falsifier check: **not applicable** — the hypothesis's falsifier is about
top-1 accuracy, which this corpus cannot produce. The honest verdict is
`inconclusive_lean_disproved` (the corpus as specified cannot carry the test),
not `disproved`.