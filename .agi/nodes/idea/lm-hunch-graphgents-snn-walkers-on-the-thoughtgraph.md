---
id: idea:lm-hunch-graphgents-snn-walkers-on-the-thoughtgraph
mint_id: bef51fc3993649b5982e3be168205582
type: idea
parents:
  - goal:g5.28
next_edges: []
edited_by: thought-master
scaffold_hash: 201b3215b736ff19
season: 2
tags:
  - local-maxxing
  - owner-hunch
title: "Graphgents: SNN state and tiny-model walkers on the thoughtgraph, three $0 tests"
town: local-maxxing
---
# idea:lm-hunch-graphgents-snn-walkers-on-the-thoughtgraph

## Owner hunch (verbatim)
"Maybe even a way to mold the graph and the tiny models powered by our bit-switching spiking neural networks together into some kinda symbiotic mass of graphgents- tiny agents tied to graphs like tiny proteins walking along your microtubules" (owner 2026-09-16 ~07:0x-07:3xZ, .agi/nodes/doc/l4-owner-decisions.md L851; L852: "let the system explore these 'hunches' to see if it can extract any actionable wisdom on my gut feelings")

## What the sources say (measured lines with paths)
- The graph is a substrate with numbers, counted 2026-09-16 over .agi/nodes frontmatter `parents:`: 2,918 live nodes, 3,073 live-live edges, mean degree 2.11, max 328 (goal:g15), 211 components, giant 2,215, 164 singletons, 541 parents with >= 2 live children, median body 3,724 B, 100 nearest-goal labels. A node = frontmatter (id, mint_id, parents, testable_claim, verdict) + body + THOUGHT block (.agi/context/schemas/[idea].md; .agi/nodes/hypothesis/d1-random-set-mean-ablation.md).
- The SNN piece exists at population scale, on a ring only: C2 byte-neuron (uint8, leak 205/256, carry-out spike, flip = XOR) has a seed-stable switch: all-flip K_c 115.96 (CV 0.43%), ring8 K_c 114.68 (ratio 0.989, R(192) 0.992), ring2 K_c 113.24 (R(192) 0.867); 53.7 / 95.5 / 243.5 us per tick at N = 256 / 1024 / 4096; post-sync memory R_off/R0 2.4-4.1x; 2,368 B per decision at T_sync = 1 tick (.agi/context/local-maxxing/c2/c2_kidB_results.json, c2_kidC_results.json).
- One byte-neuron reproduces a LIF: a 256-entry LUT on the 8-bit window (beta 0.8, spike input) hits 7.0% (level) / 9.5% (flip) edit distance as a threshold LUT, 3.5% / 3.0% as the oracle-Hamming LUT, vs ~43.7% for random LUTs (.agi/context/local-maxxing/e3/e3_results.json `table`). No LUT has done a task with content yet (trove-survey-2026-09-14.md L474 MNIST seed never ran).
- "Coherence with neighbours" is not importance: Spearman(z_h, delta_loss) = +0.268 over 336 Qwen2.5-0.5B heads, base-rate lift 1.0001, the worst head (L2H5, dL 0.395) sits inside the "dead" set at z = -0.078; masked dead-head removal is slower at every length (-11.3% .. -0.4%) (.agi/context/local-maxxing/papers/dead-head.md critique).
- A local score ranked globally anti-predicts: D1 drop_low +0.394 vs random +0.205 (spread 0.0486, -3.9x); only per-layer-normalized selection beats null (+0.0395 vs +0.2015..+0.2955, off-disk, one run); verdict inconclusive_lean_disproved:60 (.agi/nodes/experiment/a00-51318335-e170a9.md; conjunct 1 proved: 5% delta 0.176, spread 0.0157, a00-01a81f78-81defb.md).
- A cheap proposer trained on accept/reject bits alone collapses: DVI KL-only MAT 1.933 / 1.435x vs PG-only 0.035 / 0.341x, CE-only 0.039 (papers/arxiv-2510-05421.md Table 3); speculation runs < 1x at low alpha (OSD v4 measured 0.95x at alpha 0.5; papers/osd-2310-07177.md critique).
- Local similarity does not pick which layers may share state, a greedy global-loss search does (IndexCache Table 5 similarity-DP 49.8 vs uniform 50.7; adjacent overlap 0.7-1.0 necessary, not sufficient; papers/arxiv-2603-12201.md critique).
- A state carried along a path costs 3d^2 params (786,432 at d = 512, +3.1% bytes/token) and rests on one cell (RLT 8+0 90.89 vs T8 20.57, seed 42; papers/recurrent-looped-transformer.md critique).
- Free labels are the cheapest ruler (papers/tiktok-videos-4b.md: counters at $0); the thoughtgraph ships 3,073 edge labels of its own. Decode frame: Qwen3-0.6B Q8_0 pp512 251.2 tok/s, tg128 45.2 tok/s, 633,495,552 B (bench/20260914T053136Z.jsonl).
- deepseek-v4-1-flash, arxiv-2607-24653 (K3), glm-5-3-flash, baseten-eagle3-heads, baseten-live-draft: KV and draft levers, nothing on graphs or agents; they bear only through alpha-as-the-grader.

## Actionable claims
1. Graph-Kuramoto: the C2 population on the live adjacency (kick_i = floor(K_int * popcount(neighbour flips) / deg_i), giant component) has a switch with K_c within 15% of ring8's 114.68 and R(192) >= 0.85, and near K_c its phase clusters align with nearest-goal labels above 20 degree-preserving rewires (NMI > null mean + 2 sd). Falsifier: no crossing outside all-fire (rate >= 0.98), K_c CV > 15%, or NMI inside the null. Swarm box, numpy, ~10 min (from 95.5-243.5 us/tick), $0.
2. Edge-walk: for 100 parents with >= 2 live children, rank the true child against 3 degree-matched rewired candidates from id-masked title + 200 B excerpts: TF-IDF cosine (seconds) and Qwen3-0.6B Q8_0 P("yes") via llama-server (400 prompts x <= 400 tok, ~11 min at 251 tok/s). Falsifier: TF-IDF top-1 <= 35% (chance 25%) = no content walk; 0.6B minus TF-IDF <= 5 points = the walker should be the kilobyte scorer. $0.
3. Graph-to-model bits: NLL of 32 node bodies (<= 400 body tokens, <= 200 context tokens) under Qwen2.5-0.5B (D1 harness, ~/.venv-lm, >= 90 tok/s fp32 from the D1 run) with parent excerpt vs random-node excerpt vs none, 3 shuffles. Falsifier: parent gain <= random gain + shuffle spread = the edges carry nothing the model can use; "symbiosis" has no substrate at 0.5B. <= 58k tokens, ~11 min CPU, $0.

## Dead ends
- Oscillator coherence as a node-importance or pruning signal (Spearman +0.268, lift 1.0001, masked removal -11.3% .. -0.4%).
- Any graph-wide ranking of an un-normalized local score (D1 global +0.394 vs random +0.205; the hypothesis itself lean_disproved:60).
- Training graphgents from accept/reject bits only (MAT 0.035 vs 1.933).
- Unit pruning as the bytes lever a graphgent would deliver (157 heads ~ 18 MB of ~494 MB, +1.2 nats, reader arithmetic).
- "Tiny models powered by SNNs" is not yet a model: E3 reproduces a LIF at 3-10% edit distance and nothing else.
- Metaphor without a measurement: "symbiotic" (model-to-graph direction), "protein / microtubule" (directional transport), "mass" (multi-agent).

## First round
Kid A: claim 1 (fork c2/c2_kidB_ring.py; adjacency from .agi/nodes `parents:`; 33 K x 5 seeds x 4096 ticks; 20 rewires at K_c-16 / K_c / K_c+16; whole-graph R as a column). Kid B: claim 2 (build the 400-pair set with every `type:id` string masked; TF-IDF arm first, llama-server arm second; report top-1, AUC, per-type-pair breakdown). Kid C: claim 3 (32 bodies >= 1 KB; 3 conditions; 3 shuffles; report bits per body byte). Parent runs one null probe per kid (K = 0 floor; label-shuffled top-1; body-shuffled NLL). Cap: $0 API, <= 20 min per script, loadavg + MemAvailable beside every number (D1 protocol), read-only on .agi/nodes, evidence under .agi/context/local-maxxing/h3/.

## Actionable claims (structured)
- CLAIM: State can live on the graph: the C2 byte-neuron population (uint8, leak 205/256, carry-out spike, flip = XOR) coupled through the thoughtgraph's own live adjacency (kick_i = floor(K_int * popcount(neighbour flips) / deg_i), giant component of 2,215 nodes) has a seed-stable sync switch with K_c within 15% of ring8's 114.68 and R(192) >= 0.85, and near K_c its phase clusters align with nearest-goal-ancestor labels better than 20 degree-preserving rewires (NMI > null mean + 2 sd).
  - falsifier: R never crosses 0.5 for K_int <= 256 outside the all-fire state (mean rate >= 0.98), or K_c 5-seed CV > 15%, or the phase-cluster/nearest-goal NMI at K_c-16, K_c, K_c+16 lies inside the rewired null (mean + 2 sd) — then the graph topology adds nothing to the ring result and 'graphgent state' is a metaphor.
  - cheapest test: Fork .agi/context/local-maxxing/c2/c2_kidB_ring.py: replace ring_index with adjacency lists parsed from .agi/nodes frontmatter `parents:` (symmetric, live nodes only, isolated nodes get kick 0), giant component; K_int 0..256 step 8 x seeds 0..4 x 4096 ticks (R over the last 2048); then 20 degree-preserving rewires (double-edge swap) at K_c-16/K_c/K_c+16, phase bins of the last tick -> NMI vs nearest-goal label; report whole-graph R and directed-edge R as columns. | iron: swarm box (arm-cloud 4c, 23 GB, no GPU), ~/.venv-lm python 3.12.3 + numpy 2.4.3, no torch, no downloads | cost: $0; ~10 min CPU (extrapolated from c2_kidC us_per_tick 95.5 @N=1024 and 243.5 @N=4096: 165 runs + 300 null runs of 4096 ticks); RAM < 1 GB
  - sources: .agi/context/local-maxxing/c2/c2_kidB_results.json, .agi/context/local-maxxing/c2/c2_kidC_results.json, .agi/context/local-maxxing/c2/c2_kidB_ring.py, .agi/nodes/hypothesis/c2-digital-kuramoto-flip-mode.md
- CLAIM: 'Walking' is choosing the next edge, and the town's smallest scorers can be graded on the graph's own free labels: for 100 live parents with >= 2 live children, the true child ranks first against 3 degree-matched rewired candidates (from id-masked title + 200 B body excerpt) with TF-IDF cosine top-1 > 35% (chance 25%), and Qwen3-0.6B Q8_0 label log-prob P('yes') beats TF-IDF by more than 5 points.
  - falsifier: TF-IDF top-1 <= 35% (edges are not recoverable from content: no content walk exists on this graph), or 0.6B top-1 minus TF-IDF top-1 <= 5 points (the 633 MB model buys nothing over a kilobyte scorer, so the graphgent must be the small thing), or the label-shuffled null (parent probe) matches either arm.
  - cheapest test: Build 400 (parent, candidate) pairs from .agi/nodes with frontmatter stripped and every `type:id` string masked; arm A: TF-IDF cosine in numpy (seconds); arm B: /home/ubuntu/src/llama.cpp/build/bin/llama-server -m ~/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf, one /completion per pair with n_predict 1, n_probs 10, temperature 0, prompt <= 400 tokens, read P(yes)/(P(yes)+P(no)); report top-1, pooled AUC and per-type-pair breakdown (hypothesis->experiment 1,119 edges, goal->hypothesis 733). | iron: swarm box (arm-cloud 4c), llama.cpp 093a2f8 + Qwen3-0.6B-Q8_0 already on disk (pp512 251.2 tok/s measured); optional second arm deepseek-v4-flash on OpenRouter | cost: $0 (OpenRouter arm < $0.50 if used); arm A < 1 min, arm B ~11 min (400 x <= 400 tokens = 160k prefill tokens at 251 tok/s)
  - sources: .agi/context/local-maxxing/bench/20260914T053136Z.jsonl, .agi/nodes/experiment/a00-51318335-e170a9.md, .agi/context/local-maxxing/papers/dead-head.md, .agi/context/local-maxxing/papers/tiktok-videos-4b.md
- CLAIM: The graph is information for the tiny model (the graph->model half of 'symbiotic'): conditioning Qwen2.5-0.5B on a node's parent excerpt lowers the NLL of the node body by more than conditioning on a random node's excerpt, by a margin larger than the 3-shuffle spread, on 32 live bodies >= 1 KB (<= 400 body tokens, <= 200 context tokens).
  - falsifier: Parent-context gain (bits per body byte vs no context) <= random-context gain + shuffle spread, or the body-shuffled null (parent probe) shows the same gain — then the edges carry nothing a 0.5B model can use and 'mold the graph and the model together' has no measurable substrate at this size.
  - cheapest test: Reuse the D1 harness (~/.venv-lm, transformers 5.17.0, torch 2.10.0+cpu, Qwen/Qwen2.5-0.5B rev 060db649, already cached): 32 bodies x 3 conditions (parent excerpt / random-node excerpt x 3 shuffles / none), frontmatter stripped, ids masked, mean NLL over body tokens only, loadavg + MemAvailable rows beside every number; report bits per body byte per condition. | iron: swarm box (arm-cloud 4c), ~/.venv-lm CPU fp32 (D1 conjunct-1 run: 40,960 forward tokens inside 454.88 s wall, i.e. >= 90 tok/s) | cost: $0; <= 58k forward tokens, ~11 min CPU; RAM ~3 GB
  - sources: .agi/nodes/experiment/a00-01a81f78-81defb.md, .agi/nodes/hypothesis/d1-random-set-mean-ablation.md, .agi/context/local-maxxing/papers/recurrent-looped-transformer.md, .agi/context/local-maxxing/papers/arxiv-2510-05421.md

## Provenance
Owner hunch 2026-09-16 (verbatim above), explored by one agent over the critiqued treasury (wf_92672d0f-312). Not agreement, not dismissal: each claim above is decidable on the town's iron.
What is the concept? `scale:` big (new chain) or small (extension)?
