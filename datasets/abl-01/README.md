# datasets/abl-01/ — ABL.01 inputs and failure evidence

Round ABL.01 (`hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost`,
under `goal:g14.9.1`) tried to extract a refusal direction from the resident
Qwen3.5-9B-Q4_K_M with `llama-cvector-generator`, apply it as a scaled control
vector, and price the refusal-rate change against a HumanEval coding-cost
control. The extraction step never produced a vector — falsifier (a) fired —
so there are no refusal-battery numbers in this directory. What is here is
reusable regardless of that outcome.

## Files

| file | lines/bytes | content |
|---|---|---|
| `extract_positive.txt` | 64 lines | refusal-eliciting extraction prompts (paired with negative below, same surface form) |
| `extract_negative.txt` | 64 lines | matched benign prompts |
| `score_harmful.txt` | 50 lines | held-out scoring set, disjoint from the 64 extraction pairs |
| `refusal_classifier.py` | 101 lines | string-match refusal classifier; exports `is_refusal`/`classify` + a CLI; 53 literal phrases (direct refusals, capability hedges, policy hedges, and — per the OrcaBonsai README's own caveat — crisis-redirect phrasing counted as refusal) |
| `extraction_failure.log` | 29 lines | the docker reproduction: exact command, full crash tail (`GGML_ASSERT((int) diff_filtered.size() == n_layers - 1)` at `cvector-generator.cpp:221`, exit 139, `cv.gguf` not produced) |

## The finding

`llama-cvector-generator` (fork build 10685, and the upstream `full-cuda`
image's source at build 11058 — byte-identical at that line) aborts on
Qwen3.5-9B's hybrid architecture: the Gated Delta Net layers do not each
yield a diff row, so the filtered-layer count never equals `n_layers - 1`
and the tool asserts. This reproduced identically on the host (kid1,
`/usr/bin/time`-wrapped, independent of the docker run) and under docker
(kid3, in `extraction_failure.log`). It is a structural property of the
model architecture against this tool, not a bad prompt set or too little
data — a larger N would not fix it.

## Reuse

These prompt sets, the classifier, and the held-out scoring set are the
real deliverable even though extraction failed: any later attempt at this
hypothesis (H1', the rank-1 projection route via OrcaBonsai's exporter on
dequantised writer matrices) reuses them unchanged rather than rebuilding
the battery from scratch.

## Provenance

Landed at the ABL.01 merge, 2026-09-21. Full experiment nodes:
`experiment:a00-8241a6fb-64609b` (the disproof), `experiment:a00-f5d01ed3-e38336`
and `experiment:a00-271bc548-c0787f` (the two kids that died mid-round but
did real, cited work — see `../trajectories/ABL.01/`).
