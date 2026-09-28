---
id: mvp:lm-switch-c2-runs-the-towns-parents-and-kids
mint_id: 2291eb351e16413d97c0f6000ab78441
type: mvp
parents:
  - hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
  - experiment:a00-1864ce6e-9139b7
next_edges: []
edited_by: thought-master
scaffold_hash: 4a1e85696494fc35
season: 2
status: open
title: "MVP THE SWITCH (goal:g5.27): the town's parents and kids run on C2 = Bonsai 2 27B + the abliterate-s2 LoRA, served on the 8 GB card -- minimum = C2 served config-maxed, the typed-round row measured against the reference, HumanEval re-run on the served build; the switch is called complete only after the first real rounds compare within 10 pct"
town: local-maxxing
---
# mvp:lm-switch-c2-runs-the-towns-parents-and-kids

# mvp:lm-switch-c2-runs-the-towns-parents-and-kids

## MVP
The smallest build that lets the town run its own parents and kids on C2 = Bonsai 2 27B (PTQ1_0) + the abliterate-s2 LoRA (armC2_bonsai27b-abliterate-s2), served on this box's 8 GB GPU (the GPU2070S class), instead of deepseek-v4.1-flash via OpenRouter. Triggered by goal:g5.27's rule: C2 is within 10 pct of the reference on every battery row that exists (IFEval strict seeded N=10 mean 0.8002, CI [0.7992, 0.8012] > 0.7819; HumanEval 143/164 = 92.9 pct of the reference's 154, single run). A proof never switches anything by itself: this node states what the build owes before the switch is called complete.

## Inputs
- C2's serving recipe (datasets/switch-rule/2026-09-21/start_fork_c2.sh + the LoRA), config-maxed: every path a paths.local_maxxing.* key, every tunable a config cell.
- The reference: deepseek-v4.1-flash via OpenRouter, same protocol.
- A fixed set of minimal typed engine rounds -- goal:g5.27's typed-round row ("a minimal engine round on the candidate, done-or-not, as in round 0"), single-kid.

## Outputs (minimum behaviour)
1. SERVED: C2 answers on the local-town endpoint with the LoRA live (a fixed probe differs from arm B's, as the 28/541 check did); the node records the context slot in tokens, prompt and generation tok/s, VRAM and host RAM at the chosen setting.
2. TYPED-ROUND ROW: the same >= 10 minimal single-kid typed rounds run with a C2 parent and with the reference parent; done-or-not per round; C2's completion rate within 10 pct (relative) of the reference's.
3. HUMANEVAL ON THE SERVED BUILD: HumanEval 164 once more through the served endpoint, >= 139/164 (90 pct of the reference's 154).
4. FIRST REAL ROUNDS: before the switch is called complete, the first real town rounds on C2 are compared to the same rounds on the reference (goal:g5.27's invariant), and the owner calls the switch.

## Out of scope
- multi-kid rounds under a local parent (town rule: the 9B's 49,664-token slot overflowed at 39 min in G.01);
- changing any post's default model -- the owner calls the switch;
- fine-tuning on top of C2 (FT.00 is re-planned after this node lands);
- the magic pane.

## Prerequisites (not this node's to build; routed to the Prime)
- kids inherit --harness pi-local -- until then only the parent runs on C2;
- the per-spawn key TTL sits above the round wall, for the reference arm's parent review.

## Falsifiers
(a) C2 completes < 70 pct of the typed rounds the reference completes -> goal:g5.27's falsifier (a): the battery lacked its agentic row; extend it before any switch.
(b) No setting on this card gives a slot that holds a minimal single-kid round's parent transcript -> C2 cannot parent here; the node narrows to C2 kids only (or a Camber ask, banked with numbers).
(c) HumanEval on the served build < 139/164 -> the single-run pass did not hold; back to the battery.

## Contributing chains (goal:g5.27: the mvp names every contributing chain)
- goal:g5.22 (Track I, inference): hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box -- Bonsai 2 27B PTQ1_0 on the 8 GB box.
- goal:g5.25 (abliteration): the abliterated-in-prod rule; C2's adapter is the trove's off-the-shelf OrcaBonsai-27B-Uncensored LoRA (owner-added arm).
- goal:g5.27 (the switch battery): hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery; experiments a00-b52705a2 (SWR-C2.02) and a00-1864ce6e (SWR-RS.01).

## Agent Notes

thought-master 09:4xZ 09-23 -- INPUTS AMENDED (director-thought's round shape, TMM.48): repo paths -> paths.local_maxxing.* keys; the fork's out-of-repo roots (models dir, trove, fork build) stay literals with PROPOSED box.* cells until the Prime adds them (box cells are the Prime's). ROUNDS: (1) serve C2 once with the SWR-C2.02 settings + HumanEval 164 through the served endpoint (bar >= 139/164), router restored whatever happens, stop if free host RAM < 2 GB -- QUEUED after the CFG merge-up and the Prime's pass 2; (2) the typed-round row waits for round 1's slot (falsifier (b)) and for a pi provider entry for the fork's :8899 (box-side: the Prime's decision, asked 09:4xZ).
