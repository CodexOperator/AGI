---
id: idea:lm-hunch-energy-frequency-prediction
mint_id: 221091474c3a4826a186757639ff8b53
type: idea
parents:
  - goal:g5.5
next_edges: []
edited_by: belam
scaffold_hash: a8b98a1cd27f3c49
season: 2
tags:
  - local-maxxing
  - owner-hunch
thought_session: dissolve-legacy-2026-09-19
title: Energy ledger and frequency lock on the flip toy; predict-then-verify gate on the A1
town: local-maxxing
---
# idea:lm-hunch-energy-frequency-prediction

# idea:lm-hunch-energy-frequency-prediction

## Owner hunch (verbatim, 2026-09-16, .agi/nodes/doc/l4-owner-decisions.md L852)
"it is somehow important to incorporate energy use and frequency matching domains into the spiking structure, as well as prediction-based models as opposed to probability based"

## What the sources say (measured lines with paths)
- Owner's own definitions (scratchpad machinelearning/snn_applied_finance/snn_energy_topology): energy = spike_cost 0.02/spike + receive_cost 0.002/received spike (neurons.py D3); earned = 2.0 x (1-|rate-target|), 0 if target silent (energy.py L30-37). Never exercised: run_p2_experiments.py imports compute_energy_earned (L14) and never calls it; p2 Exp A net energy -0.1765..-2.159 all negative, spike rate ~= f_in (0.039@0.05..0.490@0.50) = pass-through (trove-survey-2026-09-14.md L438-439, L466).
- Chain 2 flip Kuramoto (.agi/context/local-maxxing/c2/c2_kid{A,B,C}_results.json): N=256, leak 205/256, Kc 115.96+-0.50 (5 seeds, sigma_I 10); R 0.072 at K=0 -> 1.0 at K=192; spike rate 0.201 -> 0.675; pop_period 5 -> 1; flip rate peaks 0.97 at K=80 (R 0.089), 0.65 at K=192. Spike-coupled control: Kc 165.2, R 0.952 at K=176 (rate 0.676), rate 0.994 at K=192 (degenerate, >=0.98). ring8 (fan-in 8): Kc 114.68 (0.989x), R 0.992 at K=192. Switch (kidC): T_sync median 25 ticks at K_on=128 vs 1 at 192; bytes/decision 26,944 vs 2,368; R_off/R0 2.6-3.8x after K->0 (hysteresis).
- Derived ledger, reader arithmetic on those rows under the owner constants (receive = fan-in x flip_rate): all_flip energy/osc/tick 0.210 (K=0), 0.507 (K=80), 0.415 (128), 0.364 (160), 0.347 (192), 0.305 (256); spike control 0.360 (K=176), 0.529 (192); ring8 0.0239 (192). Per decision (x T_sync median): K=128 ~10.4 vs K=192 0.347.
- E3 LUT (.agi/context/local-maxxing/e3/e3_results.json): two-LIF chain, w_syn 0.8 < thr 1.0, seed-42 spike input: N1/N2 spikes 32/3 (beta 0.5), 42/19 (0.8), 58/40 (0.95); oracle 256-entry LUT edit distance 6-10 of 200 (3-5%) vs random-LUT mean 76-97 of 200 (38-49%) at beta 0.8/0.95; beta^8 = 0.168 (0.8), 0.663 (0.95).
- Predict-then-verify family: DVI (papers/arxiv-2510-05421.md) Table 3 KL-only MAT 1.933/1.435x vs PG-only 0.035/0.341x, CE-only 0.039/0.335x; full 2.16x on H100. OSD (papers/osd-2310-07177.md) Table 1 FT labels 0.33 vs TF logits 0.78; Eq. 2 break-even alpha ~0.64 at c=0.30; v4 measured 1.42-2.17x. EAGLE-3 card (papers/baseten-eagle3-heads.md) 2.76 accepted/1.91x at 3 steps, temp 0. K3 (papers/arxiv-2607-24653.md) sec 4.1.4: draft trained with LK = -log sum min(p,q), not KL. Live-draft: +20% median accept, cadence/hardware NOT GIVEN.
- Swarm box bench (.agi/context/local-maxxing/bench/*.jsonl, llama.cpp 093a2f8, 4 threads): Qwen3-0.6B Q8_0 pp512 220-251 tok/s (b2b) vs tg128 33.9-45.2; Qwen3.5-4B Q4_K_M pp512 25.6 vs tg 6.86. The 5-token verify point is unmeasured (DVI critique 13; EAGLE-3 critique 3; survey L82 H7 predicts <=1.3x).
- Dead-head (papers/dead-head.md critique 11): Spearman(z_h, dLoss) +0.268 over 336 heads, precision monotone through chi_c 0.96, lift 1.0001 -> no critical point in real heads. RLT (papers/recurrent-looped-transformer.md): merge +3.1% bytes/token, one supporting cell (90.89 vs 20.57, seed 42), no code. DeepSeek/GLM/IndexCache/tiktok: no spiking or oscillator content (DeepSeek abs grep 0 hits; the others' flip readings are labelled the reader's by their critiques).
- Swarm box has no /sys/class/powercap and no hwmon (checked 2026-09-16): joules/token is unmeasurable on the A1; energy here is an event or bytes ledger only.

## Actionable claims
1. Energy ledger on the flip toy: near-critical coupling is the expensive place, lock is cheap. Instrument c2 with real counters (spikes, flips, received events, ticks-to-decision) for {all_flip, ring8, spike} x K in {80,128,144,160,192,256} x 5 seeds. Claim: energy/tick at every R>=0.9 state is below the K=80 flip peak (0.507 vs 0.347-0.364), bytes/decision at K=128 is >2x K=192 (26,944 vs 2,368), ring8 costs <1/4 of all_flip per decision at Kc within 10%. Falsifier: any of the three fails. Swarm box, <3 min (kidC 20 runs = 5.0 s; kidB 825 runs = 157 s), $0.
2. Predict-then-correct is bandwidth-free on the A1: a 5-token verify batch of Qwen3-0.6B Q8_0 costs <1.5x one decode step, so any proposer (model, EAGLE-3 head, n-gram, LUT cascade) has a >=2x ceiling at MAT 3. Falsifier: ms(batch-5)/ms(tg step) >= 2.5 at depth 0 or 1024 -> verify is compute-bound and the whole family dies here. `llama-bench -m ~/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf -t 4 -p 1,2,4,5,8 -n 0 -r 5 -d 0,1024 -o json` + `-p 0 -n 32`; repeat on Qwen3.5-4B-Q4_K_M. ~5 min, $0.
3. A zero-parameter prediction-based proposer pays on repetitive kid output: `llama-server --spec-type ngram-map-k` vs `none` on Qwen3-0.6B Q8_0, 10 JSON-transform + 5 prose prompts x 256 tokens, temp 0. Claim: >=1.2x tok/s on JSON, ~1.0x prose, byte-identical output (DVI PLD 1.62x on H100; OSD top-100 tokens = 72.2%). Falsifier: <1.1x on JSON or any temp-0 divergence. ~10 min at 34-45 tok/s, $0; gated by claim 2.

## Dead ends
- "Prediction-based instead of probability-based" as the training signal for a proposer: hit/miss-only collapses (DVI PG-only MAT 0.035, CE-only 0.039 vs KL-only 1.933); labels lose to logits by 0.45 alpha (OSD FT 0.33 vs TF 0.78); K3's LK loss is still a distribution objective. Prediction belongs at inference (verify), probability at training.
- Frequency matching as a resonance optimum in the E3 LIF chain: transmission N2/N1 is monotone in beta (3/32, 19/42, 40/58; reader scratch re-run of the same chain, beta1=0.8, beta2 0.3->0.99: N2 5->32 of 42, monotone, not evidence). A leaky integrator with subtract reset is low-pass; matching lives in chain 2 (pop_period 5->1 at Kc), not in E3.
- The owner's energy neuron has produced no evidence yet: earning never applied, pass-through at thr 1.0 (p2 Exp A); the trove's seed 5 fix (<5 CPU-min) runs on the owner's harness, not the town's toy.
- Joules/token on the swarm box: no counters (powercap/hwmon absent); only local-town (nvidia-smi) could give J/token, unmeasured.
- Kuramoto K_c on real transformer heads: rho +0.268, lift 1.0001, no feature at 0.96 (dead-head critique table); the head-coupling map as an SNN mask (survey E4) stays gated on structure D1 did not find (per-layer rescue +0.0395 exists only off-disk; verdict lean_disproved:60).

## First round
- One kid, swarm box, in this order: claim 2 (5 min gate) -> claim 3 (10 min) -> claim 1 (3 min); A1 tenancy rows (loadavg, MemAvailable) beside every number; outputs under .agi/context/local-maxxing/{bench,c2}/.
- Verdict rule: claim 2 fails -> claims 3 and every predictor-side hypothesis (E3 drafter, 1-loop self-draft) are parked on this iron; claim 1 fails -> the toy's energy ledger is re-derived before any "energy in the structure" design.
- If claim 1 holds: next is the owner's earned-energy rule as a homeostatic K controller in the toy (K_i += sign(earned_i - cost_i), target = locked rate) — does the population self-tune to K ~ 1.5 Kc? Bank for the owner: which ledger is canonical (owner constants on the toy vs bytes on the iron); recommendation: both columns, bytes decides on the iron.

## Actionable claims (structured)
- CLAIM: On the town's digital-Kuramoto flip toy, frequency lock is the energy-cheap state and near-critical coupling the expensive one under both ledgers: energy/osc/tick at every R>=0.9 state (K>=160) is below the K=80 flip-peak state (derived 0.347-0.364 vs 0.507 under the owner's spike 0.02 / receive 0.002 constants); bytes per decision at K=128 is >2x that at K=192 (kidC: 26,944 vs 2,368 B, T_sync median 25 vs 1); and fan-in-8 ring coupling reaches lock at Kc within 10% of all-to-all (114.68 vs 115.96) for <1/4 the per-decision energy (derived 0.0239 vs 0.347 per tick).
  - falsifier: With real event counters (spikes, flips, received events per oscillator, ticks-to-decision) over {all_flip, ring8, spike-control} x K in {80,128,144,160,192,256} x 5 seeds at sigma_I=10: any R>=0.9 state costs >= the K=80 state per tick, or bytes/decision at K=128 <= 2x K=192 (median of 5 seeds), or ring8's per-decision energy >= 1/4 of all_flip's at K=192. Any one kills 'lock is cheap' on the toy.
  - cheapest test: Fork c2_kidC_switch.py / c2_kidB_ring.py with three counters and bill each run under (a) owner constants and (b) bytes touched (kidC's N*T_sync*4 + gate_state); print one table K x topo x {energy/tick, energy/decision, bytes/decision, R, spike_rate, flip_rate}. kidC's 20 device runs took 5.0 s wall, kidB's 825 runs 157 s, so the full grid is under 3 min. | iron: swarm box (arm-cloud 4c, numpy 2.4.3, 4 threads); no GPU, no download | cost: < 3 min CPU, $0
  - sources: /home/ubuntu/work/agi/.agi/context/local-maxxing/c2/c2_kidA_results.json, /home/ubuntu/work/agi/.agi/context/local-maxxing/c2/c2_kidB_results.json, /home/ubuntu/work/agi/.agi/context/local-maxxing/c2/c2_kidC_results.json, /home/ubuntu/work/agi/.agi/context/local-maxxing/c2/c2_kidC_switch.py
- CLAIM: Predict-then-correct is bandwidth-free on the A1: a 5-token verify batch of Qwen3-0.6B Q8_0 (the verify pass of a k_spec=4 draft) costs < 1.5x one single-token decode step, so every prediction-based proposer the hunch could mean (draft model, EAGLE-3 head, n-gram, E3 LUT cascade, 1-loop self-draft) has a >= 2x bytes-per-committed-token ceiling at MAT 3 on the town's own decoder. Motivation: the box shows pp512 220-251 tok/s vs tg 33.9-45.2 (batch 512 amortizes 5.5x), the 5-token point is unmeasured, and DVI's 2.16x / EAGLE-3's 1.91x are GPU numbers the survey's H7 discounts to <= 1.3x here.
  - falsifier: ms(batch-5 forward) / ms(single tg step) >= 2.5 at depth 0 or at depth 1024: verify is compute-bound on 4 N1 cores and no proposer at any acceptance clears 1.5x, so the whole predict-then-verify family is parked on this iron regardless of predictor quality.
  - cheapest test: /home/ubuntu/src/llama.cpp/build/bin/llama-bench -m ~/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf -t 4 -p 1,2,4,5,8 -n 0 -d 0,1024 -r 5 -o json, plus -p 0 -n 32 at the same depths; ms per batch = n_prompt / pp_tok_s; report ratio batch-5 / tg-step with loadavg and MemAvailable rows (A1 tenancy protocol). Repeat once on Qwen3.5-4B-Q4_K_M (pp512 25.6 vs tg 6.86 today). | iron: swarm box (arm-cloud 4c), models and llama-bench 093a2f8 already on disk | cost: ~5 min, $0
  - sources: /home/ubuntu/work/agi/.agi/context/local-maxxing/bench/20260914T053136Z.jsonl (and siblings: pp512 / tg128 rows), /home/ubuntu/work/agi/.agi/context/local-maxxing/papers/arxiv-2510-05421.md (Table 2 2.16x, Table 3; critique item 13), /home/ubuntu/work/agi/.agi/context/local-maxxing/papers/baseten-eagle3-heads.md (card 2.76/1.91x; critique item 3), /home/ubuntu/work/agi/.agi/context/local-maxxing/papers/osd-2310-07177.md (Eq. 2; critique item 8 break-even alpha ~0.64 at c=0.30)
- CLAIM: A zero-parameter prediction-based proposer in front of the probability model pays exactly where the town's traffic is repetitive: llama-server --spec-type ngram-map-k on Qwen3-0.6B Q8_0 gives >= 1.2x tok/s on JSON/YAML re-emission prompts and ~1.0x on prose, with byte-identical temperature-0 output. Motivation: DVI Table 2 PLD (prompt lookup) 1.62x avg on H100; OSD sec 5.3 top-100 tokens = 72.2% of generated tokens (power-law traffic); survey chain 5 seed predicts >= 1.3x JSON / < 1.05x prose on the N1.
  - falsifier: < 1.1x tok/s on the repetitive workload, or any temperature-0 output divergence versus --spec-type none: prediction-then-verify does not pay even at zero draft cost on this box, and every heavier predictor (E3 LUT drafter, 1-loop self-draft, EAGLE-3 head) inherits the verdict.
  - cheapest test: llama-server -m ~/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf with --spec-type ngram-map-k vs --spec-type none; 10 prompts transforming a ~1K-token JSON + 5 prose prompts x 256 tokens at temperature 0; tok/s, draft_n and draft_n_accepted from /timings; diff outputs. Run only after claim 2 passes; optional second pass on Qwen3.5-4B-Q4_K_M (6.9 tok/s, ~12 min). | iron: swarm box (arm-cloud 4c), llama-server 093a2f8 (spec-type list confirmed by --help on 2026-09-16) | cost: ~10 min at 34-45 tok/s, $0
  - sources: /home/ubuntu/work/agi/.agi/context/local-maxxing/papers/arxiv-2510-05421.md (Table 2 PLD 1.62x), /home/ubuntu/work/agi/.agi/context/local-maxxing/papers/osd-2310-07177.md (sec 5.3 72.2%), /home/ubuntu/work/agi/.agi/context/local-maxxing/trove-survey-2026-09-14.md L679, L82-84, /home/ubuntu/work/agi/.agi/context/local-maxxing/papers/baseten-eagle3-heads.md (critique item 6: verify makes a lossy proposer lossless only via draft-simple/ngram, not the blog)

## Provenance
Owner hunch 2026-09-16 (verbatim above), explored by one agent over the critiqued treasury (wf_92672d0f-312). Not agreement, not dismissal: each claim above is decidable on the town's iron.
What is the concept? `scale:` big (new chain) or small (extension)?
