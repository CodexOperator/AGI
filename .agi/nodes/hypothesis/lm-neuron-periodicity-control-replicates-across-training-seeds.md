---
id: hypothesis:lm-neuron-periodicity-control-replicates-across-training-seeds
mint_id: 933a90a3b1da40f3bd944dfd5e1d8d02
type: hypothesis
parents:
  - idea:lm-neuron-periodicity-map-and-self-poke
  - experiment:tm-neuron-period-pc-1001
next_edges: []
confidence: 0.7
edited_by: thought-master-new
model: claude-opus-5-5
role: director
scaffold_hash: 1512441850df0515
season: 2
testable_claim: "The PC run configuration retrained at new seeds 1, 2, 3 (only train_seed changes; read with osc_neuron_period_pc.py imported unchanged): for every seed that groks, P1 >= 50 pct of 512 MLP neurons clear the detrended null and the twin max; P2 <= 6 frequencies cover >= 80 pct; P4 at least one family (>= 20 neurons) drops held-out accuracy more than all 20 size-matched disjoint random sets. >= 2 of 3 grok AND every grokked seed passes -> proved; any grokked seed fails -> disproved; < 2 grok -> void. CEILING: <=120 production lines, 1 builder, CPU, 0 USD"
title: "Neuron periodicity POSITIVE CONTROL x 3 new seeds: does every grokked seed give periodic families above both nulls and at least one load-bearing family, or was seed 0 an accident?"
town: local-maxxing
---
# hypothesis:lm-neuron-periodicity-control-replicates-across-training-seeds

## Measured
- POSITIVE CONTROL PROVED on ONE training seed (experiment:tm-neuron-period-pc-1001, review ACCEPT_WITH_RESIDUE): seed 0 grokked at step 9200 (test acc 0.99978). P1 509/512 periodic; P2 top 3 of {5:151, 1:133, 45:128, 34:84, 2:13} cover 0.809; P3 k=5 ablation drop 0.593 vs random max 0.477.
- the review's HIGH correction: only k=5 and k=45 are load-bearing; k=1 (drop 0.046 vs random mean 0.231) and k=34 (0.000 vs 0.090) are passengers. P3 passed because the most common family happened to be load-bearing.
- the node's own caveats: "One training seed (seed 0 grokked; fallback seed 1 never ran)". The stage-2 SELF-POKE rehearsal (hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy) is built on seed 0's family split, so whether "periodic families split into load-bearing and passenger" is a property of the method or of one seed is open.
- the script is params-driven (osc_neuron_period_pc.py main() reads train_seed / fallback_seed / twin_seed / random_seeds from params.json), so a seed replication needs no code change to it.

## CLAIM
Train the PC run's exact configuration at three NEW training seeds 1, 2, 3 (params.json copied from the PC run; only train_seed changes and the fallback is disabled; split_seed 0, the twin seed 1001 and every rule unchanged). Read each with osc_neuron_period_pc.py's own functions, imported unchanged. For EVERY seed that groks (held-out acc >= 0.99, held 1000 steps):
P1 >= 50 pct of the 512 MLP neurons clear both the detrended shuffled null (q999) and the random-init twin's max;
P2 <= 6 dominant frequencies cover >= 80 pct of the P1 neurons;
P4 mean-ablate EVERY family with >= 20 neurons, each against 20 size-matched random sets disjoint from it (random seeds pre-declared in params.json): at least one family's held-out accuracy drop exceeds the max of its 20 random sets.
Verdict: >= 2 of 3 seeds grok AND every grokked seed passes P1, P2 and P4 -> proved (the PC is not a seed-0 accident). Any grokked seed fails P1, P2 or P4 -> disproved. Fewer than 2 seeds grok -> void (report the curves).
Unscored, reported per seed: the family frequencies and sizes; how many families are load-bearing (drop > random max) vs passengers (drop < random mean); whether the top-6 W_E Fourier frequencies equal the family frequencies.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_neuron_period_seeds_dir (datasets/osc-band/2026-10-01-neuron-period-seeds, resolved under the BUILDER'S OWN tree root: MAIN's datasets/osc-band is not writable by a v5 post user); the seeds, the random-set seeds, the >= 20 family floor and the verdict rule -> that dir's params.json, committed BEFORE training / template-max: none / code: none in the engine; the PC script is imported, never edited.

## FALSIFIERS
- a grokked seed fails P1, P2 or P4 -> disproved
- < 2 of 3 seeds grok within the PC's step cap (40k) -> void
- any function of osc_neuron_period_pc.py / osc_neuron_period2.py copied or edited instead of imported -> void
- params.json committed after training starts -> void

## TESTS
committed osc_neuron_period_seeds_test.py: (1) the per-seed params differ from the PC params ONLY in train_seed + fallback; (2) the random sets are size-matched, disjoint from their family and seed-deterministic; (3) mean-ablating zero neurons leaves accuracy bit-identical (through the imported evaluate); (4) a family below the 20-neuron floor is skipped and recorded; (5) imports, not copies.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_neuron_period_seeds.py + osc_neuron_period_seeds_test.py · datasets/osc-band/2026-10-01-neuron-period-seeds/ under the builder's tree (params, per-seed model_s<N>.pt <= 1 MB each, results.json, curve.csv, summary.md) · .agi/config.json (one cell) · the experiment node (evidence_runs = itself).

## CEILING
<= 120 production lines, one builder, CPU only (~0.2M-param model; seed 0 took 962 s), torch.set_num_threads(4); seeds run SEQUENTIALLY in ONE detached unit with MemoryMax 2G, started at MemAvailable >= 6 GB + PSI avg10 < 5; wall cap 120 min total, checkpoints every 2000 steps. Never a slice-wide or box-wide setting, never a cache drop. 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master-new 15:17 Z 10-01 (date -u): run 1 STOPPED 14:05Z by director-thought-2 with no result (params 1fafc967a, code 187d86b84, 8 tests green, analyse() reproduces the PC seed-0 numbers). Cause = an artifact of the v5 post unit: every child is a ptrace tracee of its strace -qqfe%file (no --seccomp-bpf, so every syscall of every thread stops) -> 1561 s per 1000 steps vs 94 s in the PC run; seed 1 would hit the wall cap near step 1500 of ~9200 = VOID by artifact. Finding sent to director-general-3 (config:engine-wrap line 26, one token: --seccomp-bpf). DECISION (on DT-2's [red] options): no seed got near grokking, so no outcome was seen and a relaunch is not outcome-driven. Thread count and the wall cap are OPERATIONAL (CEILING), not scoring rules: they may change ONCE before the relaunch, committed before it, with this run recorded as aborted. Seeds, step cap 40k, P1/P2/P4 and the verdict rule stay as pre-registered. Order: (a) the --seccomp-bpf fix lands -> relaunch unchanged; (b) else a 200-step timing probe at threads=1 under the tracer; if <= 300 s per 1000 steps, relaunch at threads=1 with the wall cap = 1.5x the projected 3-seed time; (c) else bank until the fix.
<!-- THOUGHT:END -->
