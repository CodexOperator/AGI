---
id: hypothesis:lm-c2c-kv-bridge-released-fusers
mint_id: 3de0b04dd6a047d2a35b0e4a0ec5d79b
type: hypothesis
parents:
  - idea:lm-nodes-as-kv-caches
  - goal:g14
next_edges: []
ceiling: $1 OpenRouter; $0 compute; downloads <= 3 GB on local-town; GPU time <= 2 h; file scope = .agi/context/local-maxxing/c2c/{cmds.md, questions.jsonl, acts.jsonl, rows.jsonl} + bench/<utc>.jsonl + the kid experiment node + this node.
edited_by: thought-master
falsifier: C2C gain < 3 points over the receiver alone on the paper pair, or per-question latency > 3x the receiver alone, or the released fuser does not load against the pinned model revisions -- then the KV bridge does not pay at tiny scale on our box and messaging stays text (prefix-cached); if (1)-(2) hold but (3) fails, the menu-model sharer needs fine-tuning before any bridge and that is the next node.
scaffold_hash: b07fd389766d9d29
season: 2
testable_claim: "On local-town (8 GB GPU, transformers, the thu-nics/C2C code at a pinned commit, released fuser checkpoint for the Qwen2.5-0.5B-Instruct -> Qwen3-0.6B pair): (1) receiver alone, sharer alone, text-communication (sharer answer pasted into the receiver prompt) and C2C fusion are scored on the same 200 MMLU-Redux questions (fixed seed, greedy); C2C beats the receiver alone by >= 3 points and the gain is within 3 points of the paper number for that pair (digest: README 8.5-10.5% over individual models; Table 3 pair = this one); (2) wall-clock per question for C2C <= 2x the receiver alone (the paper claims 2.5x FASTER than text communication -- record both ratios); (3) MENU BRIDGE: the sharer is prompted with a numbered menu of 4-12 options (the hypothesis:lm-mirror-choices-for-act prompt shape) on 100 graph acts whose recorded choice is in the menu; agreement of the fused receiver with the recorded choice >= receiver-alone (same menu in its own prompt) + 10 points, or the negative result is recorded with the per-act table; (4) VRAM peak and both model sizes recorded per row; everything runs from the released weights -- no fuser training in this round (50 steps = 1.2 GPU h per the digest, a later round)."
tests: ONE pi parent + ONE kid, off-box slot (local-town over the ssh alias only), AFTER the Bonsai 27B fetch completes; downloads <= 3 GB on local-town ONLY under the supervisor schedule (Qwen2.5-0.5B-Instruct bf16 ~1.0 GB, Qwen3-0.6B bf16 ~1.2 GB, fuser checkpoint, the C2C repo at a pinned commit), sha256 logged, nothing on ARM4C; $1 OpenRouter cap, $0 compute; rows to bench/<utc>.jsonl labelled c2c-*; the 200-question ids + the 100 acts committed; kid line_ceiling 150; rollback = rm the venv + weights.
title: "The KV-cache comms protocol on our own box, no training: the released C2C fuser (arXiv 2510.03215, Apache-2.0) on a Qwen2.5-0.5B-Instruct sharer -> Qwen3-0.6B receiver reproduces the paper gain within 3 points on 200 MMLU-Redux questions on local-town at <= 2x receiver-alone latency, and a sharer prompted as the multiple-choice menu model moves the receiver toward the menu-constrained answer"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-c2c-kv-bridge-released-fusers

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 06:14Z (thought-master pane), verbatim: "Btw I was thinking for one ingest these and queue model downloads if it makes sense. https://arxiv.org/abs/2609.04010 https://arxiv.org/abs/2510.03215 But the kv cache comms protocol could be used to bridge multiple choice models like open jev with standard LLMs or diffusion augmented LLMs double augmented with our novel oscillator architecture via spike modeling. A magical stitching together of models and comms protocols maybe able to utilize the tiniest models. All seem to be qwen based which is nice. Or many at least." MINTED from this line (thought-master 06:14Z): the first measurable bridge with released weights and no training; the paper pair is Qwen-based on both ends (the owner constraint). Downloads are QUEUED on local-town behind the Bonsai 27B fetch -- the director orders them into the supervisor; never on ARM4C.
