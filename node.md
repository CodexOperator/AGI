---
id: goal:g14.7.3
mint_id: 1b169527986a41f8abe2455f5e908f04
type: goal
parents:
  - goal:g14.7
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G14.7.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 61c0d92dc174210d
season: 2
status: active
tags:
  - local-maxxing
  - track-ii
  - fine-tuning
  - diagram-max
title: "G14.7.3: DIAGRAM-MAXED THOUGHT TRACES AS TRAINING DATA -- does the same training method and base, trained on diagram-maxed traces (goal:g14.16 shape) vs prose traces, change battery performance and tokens-per-solution? (owner 02:1xZ 09-21)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.7.3
## Agent Notes
**Owner source (2026-09-21 02:1xZ, verbatim on goal:g14, relayed via goal:g14.7's thought-master program block):** "Queue up experiments on how diagram maxxed thought patterns and finetuning vs lora vs rl or even pretraining affect model performance especially smaller ones..." -- the diagram-maxed-shape half of the same line.

**Commits to.** One controlled A/B: the SAME base size and SAME training method (whichever arm `goal:g14.7.2` finds strongest on its ladder), trained on two versions of the SAME underlying trace content -- prose traces vs diagram-maxed traces (the compression shape defined on `goal:g14.16`) -- varying only the corpus's SHAPE, nothing else. Question: does the diagram-maxed shape change battery performance and tokens-per-solution?

**Invariants.** The diagram-maxed corpus comes from the SAME scrub + labelling pipeline as `goal:g14.10.2` (not a one-off hand transform); a training corpus is frozen by sha256 in the trial's node (G14.10 rule). Measured on the battery AND on tokens-per-solution -- token efficiency, not just accuracy, is the entire point of diagram-maxing (G14.16's own target: fewer tokens, more meaning). No trial judged on training loss (G14.7 rule).

**Falsifiers.** Falsified as a lever if the diagram-maxed-trained arm does not beat the prose-trained arm on tokens-per-solution at an equal-or-better battery score -- then diagram-maxed shape helps human/agent readers (its proven use on cards and dms) but is not itself a useful training-data shape, and the two uses are kept separate going forward.

**Done when.** One measured pair (prose-trained vs diagram-maxed-trained, same base, same method) exists with a verdict.

**First chunk.** None minted yet -- blocked on two things landing first: `goal:g14.7.2` needs a verdict (which base/method to hold fixed) and `goal:g14.10.2` needs its classifier pass done (the "reasoning shape prose/diagram-maxed" label is exactly what that pass adds -- without it there is no diagram-maxed corpus to train on). Layers with `goal:g14.15` (KV telepathy) the same way G14.7.2 does, after both have verdicts.
