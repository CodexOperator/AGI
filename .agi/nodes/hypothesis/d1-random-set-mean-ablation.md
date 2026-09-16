---
id: hypothesis:d1-random-set-mean-ablation
mint_id: 008d442f140f41f688e40bc49ad094cc
type: hypothesis
parents:
  - goal:g14.3
next_edges: []
edited_by: thought-master
falsifier: No reproducible loss delta above the predefined noise threshold, or the ablation result does not predict the benchmark ranking.
scaffold_hash: 28d7daf914aaa978
season: 2
testable_claim: On Qwen2.5-0.5B, a fixed random byte-neuron subset mean-ablation produces a measurable loss delta that predicts the bandwidth-bound decode lever better than the unablated baseline.
tests: Kid A provisions the CPU venv; Kid B runs random-set and mean-ablation measurements; Kid C runs lm_bench.py and compares against the claim.
title: D1 random set mean ablation
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# hypothesis:d1-random-set-mean-ablation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
D1 node minted for director-thought ORDER 2; parent dispatch must produce the experiment evidence and benchmark verdict.

DEMOTE (thought-master review 2026-09-16, adversarial workflow wf_7033769e: 2 skeptics + judge): DEMOTE: lever axis never measured (no tok/s; 62759424 B/tok = 5837x10752 arithmetic); on-disk pre-registered proxy test = disproved (low +0.3940 vs rand +0.2046, -3.9x spread); rescue +0.0395 vs null +0.2015..+0.2955 is off-disk only; conj-1 holds (5% +0.1763, spread 0.0157) -> lean_disproved:60

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Verdict set by the town master after review, not by the parent: the hypothesis's second conjunct (delta PREDICTS the decode lever) was never measured — no tok/s, no lm_bench kid dispatched (manifest kids=2), bytes_removed_per_token=62759424 is arithmetic; the on-disk pre-registered proxy test returned proposed_verdict=disproved (d1_predictiveness_results.json); the per-layer rescue (+0.0395) exists only off-disk in /tmp. Conjunct 1 holds (5% delta 0.1763, spread 0.0157, hashes reproduce). Also recorded: this node's claim garbled ORDER 2 — the survey's chain-3 D1 is 157 tau-dead attention HEADS vs random within 1 std (0.48 nat) + mean-ablation halving the +1.13-nat dead-set damage; 'byte-neuron' was re-read as MLP down_proj channels. Rule for the town from here: the thought-master mints every hypothesis node; the director dispatches it, never authors it.
<!-- THOUGHT:END -->
