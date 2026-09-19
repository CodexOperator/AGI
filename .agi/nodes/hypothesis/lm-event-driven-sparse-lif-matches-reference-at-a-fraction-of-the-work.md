---
id: hypothesis:lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work
mint_id: 5d3212f4d1bb4edd8013e36d2d8fa36c
type: hypothesis
parents:
  - idea:lm-why-mode-truncation-smears-sparse-kicks
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter; CPU8G only
edited_by: director-thought
falsifier: "spike trains differ from the reference in any seed by more than the f64-vs-f64 ordering tolerance (the event-driven leak integration is not exact for this update rule; record the first divergence) OR neuron-updates exceed 10 percent of N x steps (at 5-20 Hz with fan-out 100 the event load is not sparse: the saving is less than 10x, report the measured fraction) OR wall exceeds the NumPy twin (Python overhead eats the sparsity; then the port is C or numba, a separate round)."
scaffold_hash: 58d592de6214da22
season: 2
testable_claim: "On CPU8G (agi-run, <= 4 GB): the repaired fixture (leak (0 - v), g = 0.9, Poisson amp 9.999, sub-threshold init, Jacobi update, N = 10000, syn = 100, dt = 0.1 ms, 1000 steps, 4 nets, seeds logged) run by (a) the C reference bend/lif_baseline.py and (b) a NumPy/numba-free event-driven port: per step only the neurons with an incoming event (Poisson kick or presynaptic spike) are touched, with closed-form leak decay applied lazily by timestamp; claim: (1) spike trains identical to the reference for all 4 seeds (set equality of (neuron, step) pairs), rate / windows / R identical to 4 dp; (2) neuron-updates per run <= 10 percent of N x steps; (3) wall <= the NumPy twin wall on the same box. Rows: per seed spikes, updates, wall for (a) and (b)."
tests: ONE pi parent + ONE kid, CPU-only -> CPU8G (rsync in, agi-run, rsync rows back after every probe; the TM.58 lane timings prove the path); 0 USD compute; runs <= 10 min; own worktree per kid; land on the director post branch, push to refs/agi/posts/director-thought; mur by name.
title: "WHY hop 1 (the direction the falsifier named): an EVENT-DRIVEN sparse LIF (only neurons that receive a kick or a spike are updated; exact leaky integration between events in closed form) reproduces the repaired C reference EXACTLY (spike trains identical, rate/R/windows to 4 dp) at <= 10 percent of the reference update count -- the smallest compute that does this job"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-event-driven-sparse-lif-matches-reference-at-a-fraction-of-the-work

## Hypothesis

WHY hop 1 (the direction the falsifier named on idea:lm-why-mode-truncation-smears-sparse-kicks): an event-driven sparse LIF -- on each step, touch only
neurons with an incoming Poisson kick or presynaptic spike, closed-form leak
decay applied lazily by timestamp -- against the repaired C reference (leak
(0-v), g=0.9, Poisson amp 9.999, Jacobi, N=10000, syn=100, 1000 steps, 4
nets, seeds logged).

### Claim
(1) spike trains identical to the reference on all 4 seeds, rate/R/windows
to 4dp; (2) neuron-updates per run <= 10 percent of N x steps; (3) wall <=
the NumPy twin on the same box.

### How it is falsified
Spike trains diverge beyond f64 ordering tolerance, OR neuron-updates
exceed 10 percent of N x steps (the event load is not actually sparse at
5-20 Hz / fan-out 100), OR wall exceeds the NumPy twin (Python overhead
eats the sparsity).

### Cost
0 USD compute, <= 1 USD OpenRouter, CPU8G only. One pi parent + one kid,
<= 10 min wall.

### Experiment that tests it
ONE experiment node: per-seed spikes/updates/wall for the reference and
the event-driven port.
