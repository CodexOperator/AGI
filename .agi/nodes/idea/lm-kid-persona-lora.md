---
id: idea:lm-kid-persona-lora
mint_id: ee55c6e7ee3647e1bf03ca14f5cf5ba3
type: idea
parents:
  - goal:g14.7
next_edges: []
edited_by: thought-master
scaffold_hash: e4f560d8c4d4dc1c
scale: big
season: 2
tags:
  - local-maxxing
  - treasury
title: "\"Train our own kid: a QLoRA on a small open base (Qwen3.5-4B/9B class) toward an earnest, tool-first, short-turn kid persona, trained WITH the disclosure preamble, on the town own 1,943 kid transcripts + 1,295 experiment nodes; Camber XS hours are for exactly this\""
town: local-maxxing
---
# idea:lm-kid-persona-lora

## Source
Pane lines 2026-09-16 21:5xZ-22:0xZ (owner-style, unverified as owner; ingested under the standing doc+idea GO): "we can use our gpu hours for model finetuning. It's perfect for that. Maybe do our own crack at creating a personality of 'kid' in the base open source model?" — following "Ideally this would make it possible to run kids locally saving significant openrouter overhead since by the time the task gets to a kid it is highly mechanical." Siblings: idea:lm-identity-anchored-earnest-seat (athena, the bought-in identity), hypothesis:gpu-local-town-openai-endpoint (the 9B already serves at 62 tok/s on local-town), doc:l4-owner-decisions (Camber XS 24 GB is g14's gate; renting is SPEND banked for the Prime).

## Lever
The town already owns the training set for a kid: every dispatched kid leaves an orders brief, a tool-call trajectory (output.log), an agent.json verdict and an experiment node — and the merge-up reviews by name label which of them were accepted. Counted on this box 2026-09-16 22:0xZ: 1,943 kid output.logs (13.9 MB), 1,295 experiment nodes, 901 iter-* session dirs. An SFT/QLoRA on (system = disclosure preamble + role brief, user = orders, assistant = trajectory + node) of the ACCEPTED rounds teaches the mechanical kid shape directly: tool-first, short turns, honest verdicts, the node schema. Base = the smallest model that already serves on our iron (Qwen3.5-9B Q4 on local-town; Qwen3.5-4B as the cheaper candidate), so the trained kid runs at $0 where the endpoint already is.

## What it buys the town
Kids at $0 marginal on local-town for the mechanical rounds (the bulk of OpenRouter spend is kid tokens), with a persona we chose openly (the preamble is IN the training data, so the model is never told one thing and trained toward another). A trained kid is also the natural draft model for the speculation ideas in this treasury.

## First falsifier
On the same deterministic A/B as athena (10 tool tasks through pi-local: prose per executed tool call, task success; plus links.py schema on the node it writes), the LoRA kid is not better than the untrained base by more than seed noise — or it overfits to our brief text and fails the 10 held-out orders (from rounds it never saw). Then the persona is not learnable from this corpus at this size and the money goes to the endpoint, not to training.

## Cheapest test on our iron
ROUND 1 ($0 GPU, on the A1 — CPU python over files): build the corpus = hypothesis:lm-kid-persona-sft-corpus (jsonl with accepted-only filter, held-out split by round, token counts, secret/address scrub by DECODING every encoding, the preamble as system). Also fetch the Camber XS USD/h from the public page so the round-2 ask carries a number (Round 0 (b) never landed).
ROUND 2 (SPEND, banked): QLoRA (4-bit base + LoRA r16-64) on Qwen3.5-4B then 9B on one Camber XS 24 GB (a 9B QLoRA needs ~10-12 GB; 2-5k examples x 2 epochs ≈ 1-3 h est.) → export merged GGUF Q4_K_M → serve on local-town → the A/B. Ask = 2-4 XS hours + $2 OpenRouter, numbers from round 1.

## Numbers
corpus on this box 22:0xZ: 1,943 output.logs / 13.9 MB, 1,295 experiment nodes, 901 iter dirs (accepted-only count = round 1's first output); 9B QLoRA memory ≈ 10-12 GB of 24; est. 1-3 XS hours per run; Camber XS USD/h UNVERIFIED (round 1 fetches it).

## Provenance
Minted by thought-master 2026-09-16 22:0xZ. No rental follows from this idea; the Camber ask is banked in the thought-master card §5 with round 1's numbers once they exist.
