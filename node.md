---
id: goal:g5.23.2
mint_id: 8aee8669ff74493987b44447de138b23
type: goal
parents:
  - goal:g5.23
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G5.23.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 8ac62b892f71fa92
season: 2
status: active
tags:
  - local-maxxing
  - track-ii
  - fine-tuning
  - training-ladder
title: "G14.7.2: TRAINING-METHOD LADDER -- SFT full | LoRA/QLoRA | RL on verdict labels | pretrain from scratch, small bases first (0.6B/1.7B/4B), measured on the battery + kid-tier checklist vs base and reference, USD/GPU-h per arm, Camber for FT/RL via the Prime (owner 02:1xZ 09-21)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.7.2
## Agent Notes
**Owner source (2026-09-21 02:1xZ, verbatim on goal:g14, relayed via goal:g14.7's thought-master program block):** "Queue up experiments on how diagram maxxed thought patterns and finetuning vs lora vs rl or even pretraining affect model performance especially smaller ones cause we can batch rounds and even train from ground up for even somewhat big ish models using all this synthetic data. Then layer that with the kv cache telepathy chain."

**Commits to.** A training-METHOD ladder, base held small first: 0.6B / 1.7B / 4B (the resident 9B last, only after the small ladder proves a recipe). Corpus = `datasets/` (kid-sft after DS.01's re-scrub, jev-typed-acts, the ABC/SWR/ABL trajectories, the switch-rule battery, abl-01). Four arms per base: (1) SFT full, (2) LoRA (+QLoRA), (3) RL on verdict labels (DPO/GRPO-style, label = the round's own verdict or its mur residue class), (4) PRETRAIN from scratch on the synthetic corpus -- attempted only once the small-base ladder has proved the recipe is worth scaling.

**Invariants.** Every arm measured on the G14.11 battery (HumanEval + IFEval strict) plus the kid-tier checklist, against BOTH the untuned base and the reference bar; USD + GPU-h recorded per arm. Camber hours are authorised for FT/RL (owner 21:4xZ 09-20, per-job keys via the Prime, numbers stated first, failing is fine). Rounds are batch-maxed: one order = the whole ladder for one base size, ONE merge-up per batch (goal:g14.16 rule). Corpus is measured/scrubbed/split before any GPU hour (G14.10 rule); no trial judged on training loss (G14.7 rule).

**Falsifiers.** An arm that does not beat the untuned base on the battery by a real margin without a bigger loss elsewhere is a failed arm -- recorded as a row, not hidden (G14.7 falsifier (a) applied per-arm). If NO arm across the entire small-base ladder closes any measurable fraction of the local-vs-reference gap, the ladder itself is falsified for that base size and the next base does not get the full four-arm treatment -- only the arm(s) that showed any signal.

**Done when.** Each of the four arms has one measured chunk on the smallest base (0.6B), in one comparison table: recipe, USD, GPU-h, battery delta vs base and vs reference.

**First chunk.** None minted yet -- queued behind FT.00 (morals + sanctuary SFT, the first Track II round, stays first and is not replaced by this ladder) and DS.01 + G14.10.2 (the labelled corpus this ladder reads). Layers with `goal:g14.15` (KV telepathy) only once G14.7.2 AND G14.15 each have their own verdict (owner: "Then layer that with the kv cache telepathy chain") -- that layered chunk is not this node's own first chunk, it comes after.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
renumber g14.7.2 -> g5.23.2 to align the town with core's 09-21 goal re-arrangement (owner GO on core; owner 09-23 asked the two teams be aligned): the parent g14.7 became g5.23 on core; mint_id preserved; Prime core-sync 09-23
<!-- THOUGHT:END -->
