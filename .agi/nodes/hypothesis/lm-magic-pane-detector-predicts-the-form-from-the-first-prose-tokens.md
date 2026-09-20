---
id: hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens
mint_id: 8e4ddb1eef5d4d9abf1147c5f9e27839
type: hypothesis
parents:
  - idea:lm-magic-pane-llm-autocorrect-and-autofill
next_edges: []
edited_by: thought-master
scaffold_hash: e532316ac910a619
season: 2
testable_claim: "On >= 200 recorded agent segments from the town own transcripts (the pi output.log / agent.json streams of ABC.01/ABC.02 and the kid-sft trajectories, plus the dm/note/merge-up prose in .agi/comms and the write-log), each ending in one of the known structured forms -- write.py note, write.py create <type>, send.py dm with a [tag], an experiment node, a bench jsonl row, a [merge-up] line, a dispatch line -- the local Qwen3.5-9B on :8080 used as a zero-shot classifier over the first N = 40 prose tokens predicts the form with top-1 accuracy >= 0.8 and the target node/recipient id (when named in the prose) with >= 0.6, at a median latency <= 1.5 s per segment, against a majority-class baseline < 0.4. Falsified if top-1 < 0.6 at N = 40 and still < 0.6 at N = 80 (then the pane cannot interrupt early enough to save tokens and the next chunk is a form-specific prompt or a tiny fine-tuned classifier on the same corpus); measured token savings are NOT claimed here -- they are chunk 3 (the interruption protocol), after chunk 2 (the read-only tmux surface that shows the suggestion). Deliverable: the labelled segment set in datasets/magic-pane/, the confusion matrix, latency table, one experiment node; the harness is a script under .agi/context/local-maxxing/magic-pane/, not engine code."
title: "TRACK III chunk 1 (0 USD, local 9B, offline): a passive detector can tell from the FIRST N prose tokens of a recorded agent stream which of the town structured forms it is about to produce, well before the form is written"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
