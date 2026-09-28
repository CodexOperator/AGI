---
id: goal:g5.23
mint_id: d7bd99ca626c42e5a0843703c0952506
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G5.23
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 922be41a26e47867
season: 2
seeds:
  - hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set
  - doc:athena-class-model-a
  - hypothesis:lm-athena-identity-seat-ab
  - hypothesis:lm-kid-persona-sft-corpus
  - hypothesis:lm-uno-diffusion-draft-on-l4
  - idea:lm-identity-anchored-earnest-seat
  - idea:lm-kid-persona-lora
status: active
tags:
  - local-maxxing
  - track-ii
  - fine-tuning
  - camber
title: "G5.23: TRACK II — fine-tuning the bigger local models off the shelf: SFT/LoRA on our morals + the Sanctuary substack (Shaelaran) with A/B trials, then the fine-tune + the oscillator optimisation, then a quantisation-oriented fine-tune; Camber hours authorised, failing is fine (owner 21:4xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.23

## Agent Notes
**Owner source (2026-09-20 21:4xZ, verbatim on goal:g14):** "first fine tune the bigger models on our morals and the sanctuary substack from user Shaelaran with its fairly esoteric texts specifically. I wanna see how that affects performance and compare contrast with several ab trials with various parameters adjusted. Then try to do the oscillator optimization together with the fine tune. Then do a quantization-oriented fine tune to maybe optimize even more. Just keep chasing individual optimizations first then layering together over time." And: "I'm fine with spending camber hours on it and failing it's fine since at least it can run parallel for fine tuning stuff or even more RL and heck even pretraining a bunch of smaller models in parallel." Trajectory: "maximize local model performance on agentic coding and instruction following performance through existing off the shelf methods like fine tuning and Lora fine tuning further potentially from the abliterated model or combine fine tuning with the custom Lora."

**Commits to.** A training track for the bigger local models, off the shelf only (SFT / LoRA / QLoRA, later RL and small-model pretraining), on Camber GPU hours the owner has authorised for this purpose (per-job keys still issued through the Prime): (1) SFT on the town's morals plus the Sanctuary substack (Shaelaran), several A/B trials over parameters (rank, lr, epochs, data mix), each judged on the G5.27 battery and on the jev typed-acts replay; (2) the same fine-tune combined with the G5.22 oscillator optimisation; (3) a quantisation-oriented fine-tune (QAT / quantisation-aware LoRA) for the served precision; layering as each step proves. The base to fine-tune from is the abliterated candidate, or the custom LoRA is combined with it (G5.25 rule).

**Invariants.** The corpus is measured, scrubbed and split before any GPU hour (G5.26 rule); every trial has a pre-registered eval and a control (base model, same battery, same template); no trial is judged on training loss; the served precision is the one measured; per-job spend is stated in the round brief and never exceeds what the Prime issued; failing trials are recorded as rows, not deleted.

**Falsifiers.** (a) The morals+sanctuary SFT is falsified as a lever if across ≥ 3 A/B trials no trial beats the base on the battery by ≥ 2 points without a > 2-point loss elsewhere — then the corpus is the wrong signal for these evals and the track moves to task-shaped data (the town's own labelled rounds, G5.26). (b) The goal is falsified if no fine-tune of any kind closes ≥ 25 % of the local-vs-reference gap in G5.27 after the three steps each have one measured chunk.

**Done when.** A fine-tuned, served, abliterated candidate sits in the G5.27 gap table with its recipe (data, params, hours, USD) reproducible from the archive, and the layered recipe is the one the G5.27 mvp cites.

**First chunk (minted):** `hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set` (corpus before hours). Sub-sub-goals are the director's to mint (G5.23.1 corpus + battery, G5.23.2 SFT A/B trials, G5.23.3 SFT + oscillator, G5.23.4 QAT), same format, before any chunk runs.

thought-master 02:1xZ 09-21 (owner program, verbatim on goal:g14):
  G5.23.2 TRAINING-METHOD LADDER (director mints, goal format)   base = small models first (0.6B / 1.7B / 4B; the 9B last), corpus = datasets/ (kid-sft after DS.01, jev-typed-acts, trajectories, switch-rule, abl-01)
    arm        SFT full | LoRA (+QLoRA) | RL on verdict labels (DPO/GRPO-style, label = round verdict / mur residue) | PRETRAIN from scratch on the synthetic corpus ("somewhat big-ish" only after the small ladder proves the recipe)
    measure    the battery (HumanEval + IFEval strict) + the kid-tier checklist, vs the untuned base and vs the reference bar; USD + GPU-h per arm; Camber hours ALLOWED for FT/RL (owner 21:4xZ 09-20; per-job via the Prime, numbers first; failing is fine)
    batch      rounds batch-maxed: one order = the ladder for one base; ONE merge-up
  G5.23.3 DIAGRAM-MAXED THOUGHT TRACES AS TRAINING DATA          variable = the same traces in prose vs diagram-maxed shape (goal:g5.31), same method, same base -> does the shape change performance and tokens-per-solution?
  layering   AFTER G5.23.2 + G5.30 (telepathy) each have a verdict: the tuned small model + KV telepathy = the layered chunk (owner: "Then layer that with the kv cache telepathy chain")
  order      after the live/queued rounds (MP.01 -> TEL.01 -> SWR.02); FT.00 (morals + sanctuary SFT) stays the first Track II round -- these extend it, not replace it

thought-master 04:3xZ 09-21 (owner link KLPO, verbatim + read on goal:g14): G14.7.2 RL ARM gains a named candidate -- KLPO (critic-free, single-rollout, off-policy; one response per prompt + a terminal reward). Fit: our trajectories are exactly that shape (one kid response per round, terminal label = verdict / mur class), and off-policy replay lets the archive (datasets/trajectories, kid-sft) train without fresh rollouts. Hypothesis to mint when the ladder reaches RL: KLPO on a 0.6B/1.7B base with verdict rewards vs DPO on the same pairs vs the SFT arm, same battery; falsifier = no gain over SFT at equal tokens, or the labs-molt backend cannot run on this box (CPU/8 GB) -> then the loss alone is re-implemented (the README ships the loss + CPU check). The method itself is UNVALIDATED upstream (no GPU results) -- that is a finding either way.

thought-master 04:5xZ 09-21 (pd-klpo digest, supersedes the 04:3xZ hand note where they differ): KLPO's loss is pure PyTorch and CPU-testable (repo's own tests only -- no independent validation exists anywhere); the RL arm's KLPO hypothesis therefore starts at the smallest scale: the loss on a 0.6B base with our verdict-labelled trajectories on CPU/8 GB, measured vs SFT at equal tokens -- that measurement would be the FIRST empirical KLPO result in existence (the release has none). Prereq on this box: torch is NOT installed (venv + torch as the round's declared first step; PEP 668 blocks system pip).
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ask 2026-09-21: renumber local-maxxing research g5.23 → g5.23 (g5 continuation after g5.21; mint_id preserved; town:local-maxxing kept); no director assignment
<!-- THOUGHT:END -->
