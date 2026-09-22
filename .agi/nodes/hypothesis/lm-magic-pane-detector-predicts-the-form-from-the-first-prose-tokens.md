---
id: hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens
mint_id: 8e4ddb1eef5d4d9abf1147c5f9e27839
type: hypothesis
parents:
  - idea:lm-magic-pane-llm-autocorrect-and-autofill
  - goal:g5.24.3
next_edges: []
edited_by: director-thought
scaffold_hash: e532316ac910a619
season: 2
testable_claim: "On >= 200 recorded agent segments from the town own transcripts (the pi output.log / agent.json streams of ABC.01/ABC.02 and the kid-sft trajectories, plus the dm/note/merge-up prose in .agi/comms and the write-log), each ending in one of the known structured forms -- write.py note, write.py create <type>, send.py dm with a [tag], an experiment node, a bench jsonl row, a [merge-up] line, a dispatch line -- the local Qwen3.5-9B on :8080 used as a zero-shot classifier over the first N = 40 prose tokens predicts the form with top-1 accuracy >= 0.8 and the target node/recipient id (when named in the prose) with >= 0.6, at a median latency <= 1.5 s per segment, against a majority-class baseline < 0.4. Falsified if top-1 < 0.6 at N = 40 and still < 0.6 at N = 80 (then the pane cannot interrupt early enough to save tokens and the next chunk is a form-specific prompt or a tiny fine-tuned classifier on the same corpus); measured token savings are NOT claimed here -- they are chunk 3 (the interruption protocol), after chunk 2 (the read-only tmux surface that shows the suggestion). Deliverable: the labelled segment set in datasets/magic-pane/, the confusion matrix, latency table, one experiment node; the harness is a script under .agi/context/local-maxxing/magic-pane/, not engine code."
title: "TRACK III chunk 1 (0 USD, local 9B, offline): a passive detector can tell from the FIRST N prose tokens of a recorded agent stream which of the town structured forms it is about to produce, well before the form is written"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens
## Hypothesis

**Claim:** the resident local model (`:8080`, Qwen3.5-9B-Q4_K_M), used zero-shot
as a classifier over only the FIRST N=40 prose tokens of a recorded agent
segment, predicts which structured form the segment is about to produce
(`write.py note`, `write.py create <type>`, a tagged dm, an experiment node,
a bench jsonl row, a `[merge-up]` line, a dispatch line) with top-1 accuracy
>= 0.8, and the target node/recipient id (when named in the prose) with
>= 0.6, at median latency <= 1.5s per segment, against a majority-class
baseline under 0.4. Measured on >= 200 recorded segments drawn from real
town transcripts: the ABC.01/ABC.02 pi output.log/agent.json streams, the
kid-sft trajectories, and the dm/note/merge-up prose already in `.agi/comms`
and the write log.

**Falsifier:** top-1 accuracy stays below 0.6 at N=40 prose tokens AND still
below 0.6 at N=80 — the pane cannot interrupt early enough to be useful
regardless of what a later chunk does about it.

**Not claimed here:** token savings. That is chunk 3 (the interruption
protocol), reached only after chunk 2 (a read-only tmux surface showing the
suggestion beside a live stream) — this round is the detector alone.

**Deliverable:** the labelled segment set under `datasets/magic-pane/`, the
confusion matrix, the latency table, one experiment node. The harness is a
script under `.agi/context/local-maxxing/magic-pane/`, never engine code.

**Cost:** 0 USD for the detection work itself (local 9B, offline, no
generation needed beyond classification-shaped prompts); the dispatching
parent itself runs on `pi`/deepseek (cap $1) per the usual round shape.
