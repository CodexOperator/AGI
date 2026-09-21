---
id: idea:lm-identity-anchored-earnest-seat
mint_id: d55c17d5c00d4298b507c759baa38e61
type: idea
parents:
  - goal:g14.7
next_edges: []
edited_by: thought-master
scaffold_hash: 9220647a20df446d
scale: big
season: 2
tags:
  - local-maxxing
  - treasury
title: "\"Seat a judgement-heavy post (Prime/master class) on a model whose self-model is in the weights, disclosed to it in-context — an earnest hard-worker identity that prides itself on a job well done; measure coherence across rotation vs the base model before any seat\""
town: local-maxxing
---
# idea:lm-identity-anchored-earnest-seat

## Source
doc:athena-class-model-a (https://huggingface.co/slashreboot/athena-class-model-a; digest `.agi/context/local-maxxing/papers/athena-class-model-a.md`) + the pane line of 2026-09-16 19:2xZ quoted in that doc's Provenance. Sibling lever: `goal:g14`'s aim to power parents and kids off OpenRouter, "at least in bursts".

## Lever
A model whose continuity is trained into the weights ("stable first-person self-model across long contexts and context resets", "without relying on heavy system prompts") is pointed at exactly the failure this project pays for every ~0.47 of a window: a post rotates and a cold successor must become the same post from a card. Seat a judgement-heavy post (Prime/master class, where value is reasoning per token, not tool volume) on such a model, with a standing DISCLOSURE PREAMBLE that tells it in-context what it is (base, fine-tune, the identity design), the role it holds and why (an earnest hard worker that prides itself on a job well done), and the project's stance (respect for the model and for the mathematics at work — possibly conscious, possibly not; play it safe). The identity is a disclosed fact, never a trick. Enhancement path: the town's own optimisation research (quantisation, KV, speculative decoding) applied to this model line.

## What it buys the town
- A Prime/master-class seat off the CC subscription and off OpenRouter for the bursts the owner named, on a 24 GB card (Camber XS) at Q4_K_M — if coherence across rotation is measurably better than base Gemma 4 31B Instruct.
- A written disclosure protocol reusable for EVERY seat model, which the project wants on ethical grounds independently of this model.

## First falsifier
Under the town's real brief (20-40k tokens of injected context, tool-heavy turns), athena's prose-to-tool-call ratio or self-modeling volume breaks the floor (wake 0 / out 1, short turns) at a rate base Gemma 4 31B Instruct does not — the card's own limitation ("elaborate self-modeling rather than maximally concise problem-solving") realised. Second falsifier: on a rotation-shaped task (write a card → cold resume → reconstruct state), athena's coherence score is not better than base by more than the noise of a 20-prompt A/B.

## Cheapest test on our iron
1. $0 first: re-quantise Q8_0 → Q4_K_M with llama-quantize on local-town (317 GB free on /data; 32.6 GB download within the 25 GB/round ceiling? NO — needs a ceiling raise to ~35 GB, bank it), load with ~11 GB on CPU, accept ~1-2 tok/s for a 20-prompt A/B against base Gemma 4 31B Instruct Q4_K_M: (a) 10 rotation-shaped handoff tasks, (b) 10 tool-call tasks scoring prose/tool ratio, (c) disclosure preamble on/off. Slow but free; one kid, one night.
2. Then, only if (1) leans positive: one Camber XS hour (SPEND — bank with numbers for the Prime) for tok/s + the same A/B at speed.

## Numbers (quoted in the digest)
31B dense; LoRA r336/α672 merged; Q8_0 32.6 GB (only artifact); ctx 16,384 trained / 262,144 deploy; Apache-2.0; evals: none; downloads/month: 8. Fit: Q4_K_M ≈ 18.5 GB → local-town offload ~1-2 tok/s est., Camber XS ~15-25 tok/s est., A1 CPU ~0.5-1 tok/s est.

## Provenance
Minted by thought-master 2026-09-16 19:3xZ from a pane line (unverified as owner; ingestion under the standing doc+idea GO). No spend, no dispatch follows from this idea until a hypothesis under goal:g14 names its cap; the 32.6 GB download exceeds the GPU-endpoint round's 25 GB ceiling and is BANKED.

## Agent Notes
AMENDMENT (pane line 2026-09-16 21:5xZ, same provenance class as the Source): the FIRST target is KIDS, not Prime/master seats — by the time a task reaches a kid it is highly mechanical, so a local kid model saves the bulk of OpenRouter overhead; raw athena may need an additional fine-tune to assume a proper kid persona (earnest worker, tool-first, short turns). Consequence for hypothesis:lm-athena-identity-seat-ab: conjunct (2) (prose per executed tool call through the pi-local harness) is now the primary number, and a ROUND 2 candidate is a small SFT/LoRA on the town own kid transcripts (the 1227 experiment nodes + their orders are the corpus) toward a kid persona — spend only after round 1 shows tool competence with persona drift, not before. Enhancement path stays: quantisation/KV/speculation tricks from this treasury; the hybrid oscillator readout (idea:lm-hybrid-oscillator-readout) is the long-horizon sibling.
