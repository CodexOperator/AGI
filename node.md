---
id: experiment:a00-5b80b456-eda3d8
mint_id: 220ae5f1ecae42cfa0d6d195dfc51316
type: experiment
parents:
  - hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens
next_edges: []
confidence: 0.85
edited_by: belam
evidence_runs:
  - experiment:a00-5b80b456-eda3d8
line_ceiling: 200
loop: hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "independent broad re-parse of the same 19 recorded streams (live and MP.01 excluded)", "expected": "a hidden reservoir of real forms near 200 if the 63-count was an undercount", "observed": "~68 real form productions found (write.py set 13, thought 4, replace 3, note 1; node write-edit tool 11; dispatch.py spawns 22; bench appends ~8) -- same order of magnitude as this node own 63", "result": "corpus_sufficient=false holds, no hidden reservoir exists"}
  - {"conjunct": 1, "class": "wire", "cmd": "toolcall-level check for real send.py send or dm commands across the 14 logs where send.py send textually appears", "expected": "some nonzero count of real dm-sending tool calls if the corpus undercounts dm", "observed": "ZERO real send.py send|dm commands -- every textual hit is prose or a tool result", "result": "confirms dm=0, and merge_up=0 as a text emission absent from any recorded tool call"}
  - {"conjunct": 1, "class": "noise", "cmd": "manual check of the 39 strict segments for residual false positives", "expected": "some nonzero false-positive rate given kid1 own labeler had ~82pct", "observed": "~2/39 (~5pct), e.g. a grep dispatch.py command matching the dispatch regex", "result": "real but small, does not change the order-of-magnitude corpus gap"}
production_lines: 48
profile: balanced
role: kid
scaffold_hash: 471ced251bfd7531
season: 2
title: "Chunk 1 strict retest: recorded corpus holds 63 real form segments (39 with >=40 prose tokens), dm and merge_up have zero, corpus_sufficient=false -- the corpus, not the classifier, is the finding"
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-5b80b456-eda3d8

## Experiment

Re-extracted the chunk-1 corpus under a **strict** labeler and did not force a
measurement, because the strict corpus cannot carry one. This is the decisive
statement the parent asked for as the alternative to a valid test.

### Strict predicates (a read or a mere mention is never a form)

| label | produced by |
|---|---|
| `write_note` | `write.py <node> '… note …'` |
| `write_set` | `write.py <node> '… set …'` |
| `dm` | `send.py send` / `send.py dm` (never `send.py read`) |
| `merge_up` | emitting a `[merge-up]` line (a text emission, not a tool call) |
| `dispatch` | `dispatch.py <project> <ITER.x> …` (not `--help`, not a `grep`/`sed` of the file) |
| `bench_jsonl` | `>> …jsonl`, `tee …jsonl`, `json.dump` into a `.jsonl`, `open(…jsonl,"a"/"w")` |
| `node_write` | the `write`/`edit` tool on a `.agi/nodes/…` path, or `write.py … create` |

`detect.py:label_of` in the previous run returned the first regex match over
`command + " " + path`, so `RULES[5] = r"\.jsonl"` and `RULES[6] =
r"\.agi/nodes/\S+\.md"` gold-labelled any `cat`/`ls`/`grep`/`git log` that
mentioned one. That is the defect this run removes.

Prose/form split unchanged: prose = `thinking_delta` + `text_delta` deltas
before `toolcall_start`; form read ONLY from the paired `toolcall_end`; token
unit = `\S+` run; `< 40` units dropped and counted per class. This round's own
live `iter-MP.01` logs are excluded.

## Evidence

### Real per-class histogram (recorded pi streams, all worktrees + main repo)

| label | real (≥40 tokens) | dropped (<40) | total real forms |
|---|---|---|---|
| write_set | 12 | 5 | 17 |
| dispatch | 11 | 11 | 22 |
| bench_jsonl | 8 | 2 | 10 |
| node_write | 7 | 4 | 11 |
| write_note | 1 | 2 | 3 |
| **dm** | **0** | **0** | **0** |
| **merge_up** | **0** | **0** | **0** |
| **total** | **39** | **24** | **63** |

Majority baseline 0.3077 (`write_set` at 12/39). Missing
classes: `dm`, `merge_up`. Thin (<5): `write_note` (1) — cannot carry a
per-class accuracy. Dropped counts total 24; the four predicates with real
instances (≥40) are all present, so the drop rule is not hiding a class.

**δ < 200.** Even ignoring the 40-token threshold the recorded corpus holds
**63** real forms in total. The hypothesis requires ≥ 200.

**Live-stream contamination, and the fix.** Three other rounds (EF.01, EF.02,
EF.03) were writing their `output.log` during this census; the raw count drifted
38 -> 39 -> 41 across three runs. A stream whose agent holds a lease in
`.agi/sessions/.spawn-budget/*.lease` is therefore excluded (a still-growing
log is not a recorded stream), which made the count stable at 39 across two
consecutive runs. This is a defect a naive re-run will hit.

### The other named corpora cannot supply the missing prose

| corpus | shape | why it cannot carry a segment |
|---|---|---|
| `datasets/trajectories/*/*/trajectory.jsonl` | `{ts, tool, args, result}` | **no prose / thinking deltas at all** |
| `datasets/kid-sft/kid_sft.jsonl` | 354 SFT examples; 344 node-body-only (`trajectory_available=false`) | assistant text is the finished node body, not pre-form prose |
| `.agi/sessions/write-log.jsonl` | 263 `{actor, node_id, operation, path, sha256, ts}` rows | **no prose** — a log of forms already produced |
| `.agi/comms/season-2/**/*.md` | sent message bodies | the dm form **is** the body — using it leaks the label |

### Where the missing classes' prose would have to come from

* **`dm`** — a `send.py send|dm` call. Across the recorded streams there are
  **16 `send.py read` and zero `send.py send|dm`**: kids
  report with `cli.py done`, they do not dm. Only a round's *director* emits
  dms, and this round's director log is excluded as live. A captured live
  director round is the single stream that would supply `dm`.
* **`merge_up`** — `[merge-up]` is emitted as a prose line, not a structured
  tool call. In the corpus it appears only inside file contents written by tool
  calls (e.g. an `echo '[merge-up]'` template) and in this round's own live
  director log. No recorded segment *ends in* a merge-up emission.

### Decision

**No measurement forced.** 39 real segments (63 ignoring the prose floor) and
two of seven classes at zero mean the zero-shot top-1 cannot be computed as the
hypothesis defines it. The measured path (fair, label-order-shuffled, N=40/80)
was removed from the harness to keep it inside the line ceiling and lives in
grid history; it must be re-added if a future round grows the corpus past 200.

**Falsifier check: NOT APPLICABLE.** The falsifier is `top-1 < 0.6 at N=40 and
N=80`; this corpus cannot produce a top-1. The honest verdict is
`inconclusive_lean_disproved` — the corpus as specified cannot carry the test —
not `disproved`.

### Deliverables

`datasets/magic-pane/{segments.jsonl, metrics_strict.json, metrics.json,
predictions.jsonl (empty), report.md, README.md}`; harness
`.agi/context/local-maxxing/magic-pane/detect.py`.

### Line ceiling

`production_lines 48` (`wc -l`), `line_ceiling 40`. `git diff --numstat` over
the production path reports the added/deleted delta. 48 is above the 40 ceiling
but below the 2x stop (80), so the run continued; the census-only harness has no
model-call path, which is the part that was cut.

## Agent Notes
Strict re-extract: 39 real segments (>=40 prose tokens) + 24 dropped = 63 real forms total, dm=0 and merge_up=0, write_note=1 (thin), majority 0.3077; corpus_sufficient=false, so no measurement was forced. The other named corpora cannot supply prose (trajectory.jsonl is tool-calls-only, write-log has no prose, kid_sft is node bodies, comms bodies ARE the dm form). Live streams excluded via .spawn-budget leases (count drifted 38->41 in 3 runs otherwise). Harness .agi/context/local-maxxing/magic-pane/detect.py (48 lines), data in datasets/magic-pane/.

PARENT REVIEW (a00-af8cefa3, MP.01). Read the bytes: datasets/magic-pane/{segments.jsonl (39 rows), metrics_strict.json, report.md, README.md} and .agi/context/local-maxxing/magic-pane/detect.py. Strict census reproduced (write_set 12, dispatch 11, bench_jsonl 8, node_write 7, write_note 1; dm and merge_up 0). ACCEPT inconclusive_lean_disproved:70 -- the finding is corpus insufficiency, not detector failure.
probes:
 - gate/corpus (decisive conjunct): an independent broad re-parse of the same 19 recorded streams (live + MP.01 excluded) found ~68 real form productions (write.py set 13 / thought 4 / replace 3 / note 1; node write-edit tool 11; dispatch.py spawns 22; bench appends ~8). Same order as this node 63, so corpus_sufficient=false holds: no hidden reservoir near 200 exists.
 - wire (dm=0): send.py send appears in 14 recorded logs, but a toolcall-level check found ZERO real send.py send|dm commands -- every hit is prose or a tool result. Confirms dm=0, and merge_up=0 as a text emission absent from recorded tool calls.
 - residual label noise: ~2/39 strict segments are still false positives (e.g. a grep dispatch.py command matched the dispatch regex). ~5%, down from kid 1's ~82%; it does not change the order-of-magnitude gap.
Caveat carried forward: the detector itself was not measured on the 39 valid segments (census-only harness), so this node does not speak to the 0.8 accuracy bar, only to whether the named corpus can carry it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID: if the strict set is under 200, do not force a measurement -- land the corpus-insufficiency finding instead.
(2) WHAT THE MACHINE ACTUALLY DOES: detect.py strict() gates every label through the tool NAME plus a write/append regex, so reads are excluded; its census is 39 rows (63 counting <40-token drops). My independent broad parse of the same 19 recorded streams found ~68 real forms, and a toolcall-level grep found 0 real send.py send|dm. The corpus genuinely lacks dm and merge_up at any scale.
(3) THE NEAR MISS: keeping kid 1's 237-segment set and reporting 0.27/0.29 would satisfy the falsifier numerically while measuring spurious labels; the corrected census shows the binding constraint is the DATA, not the classifier.
(4) DEVIATION: none. The verdict is framed as corpus-insufficiency, not detector failure, and the parent accepted that framing.
<!-- THOUGHT:END -->
