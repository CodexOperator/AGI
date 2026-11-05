---
id: goal:g5.36
mint_id: 485c97d570594512979a6ed71804d29a
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.36
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 8925f1b38ec64e3e
season: 3
seeds: []
status: complete
tags: []
title: "G5.36: the proved mod-113 net cut by hand to its key-frequency neurons with a closed-form W_out (0 training) is measured against random cuts: how few neurons a known circuit needs (card-belam r9, less-is-more)"
town: local-maxxing
---

# goal:g5.36

## Why this exists
goal:g5 (Local-maxxing): card-belam §7 r9 asks for first-principles intelligence, tiny nets that master one thing first, and the owner's vision line for less-is-more (11-05 06:11Z, verbatim on vision:less-is-more) points at "claude modifying weights of tiny models (1b or less) directly". less-is-more (10:22Z 11-05) ranked this first: the proved mod-113 net of experiment:tm-neuron-period-pc-1001 (held-out 0.99978, 512 MLP neurons, key frequencies 5/1/45/34; model.pt already in-tree under datasets/osc-band/2026-10-01-neuron-period-pc) is a known circuit to EDIT, with no training.

## Target end-state
- A committed, measured answer: keeping N of the 512 MLP neurons and writing W_out in closed form (least squares onto the full net's TRAIN-split logits; 0 gradient steps), the held-out accuracy on the 8939 test pairs at N in {8, 16, 24, 32, 48, 64}, for frequency-picked neurons (top peakiness, round-robin over the key frequencies) against 5 random-picked seeds and the random-init twin.
- N_f = the smallest N where the frequency pick reaches >= 0.99, named in results.json.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).

## Falsifier
1. PROVED iff N_f <= 64 AND the random picks (5 seeds, same solve) need N_r >= 2 x N_f to reach 0.99. RED if N_f > 64, or if the random picks reach 0.99 at N_r < 2 x N_f (the circuit knowledge did not matter).
2. Mutant, which must read RED: the same solve on 64 neurons of the random-init twin (seed 1001) stays < 0.5; if it does not, the solve, not the trained features, does the work, and the round is VOID.

## Out of scope
goal:g5.35, goal:g5.37. Integer quantization of the N_f net and its bend2 proof over all 12769 pairs are the NEXT rung (less-is-more leaf 2), only if this one is green.

## Agent Notes
Assigned to **director-thought-1**.
Closed 11-05: DISPROVED, results f157dedb99; review CONFIRMED (director-thought-review 10:56Z).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (thought-master 11:0xZ 11-05): CLOSED complete on the target end-state as written: the six-size cut is committed and measured (director-thought-1, pre-run f533da2a1a an ancestor of results f157dedb99, tip 5bb45c4d40; experiment:dt1-neuron-period-cut-1105). Falsifier read: N_f > 64 on the leaf grid (freq 0.815 at 64; 0.985 at 96 and 0.9946 at 128 as pre-registered extras) and random reaches 0.99 at N_r = 64 (seeds 64/64/96/64/64) -> both RED conditions fire -> DISPROVED; mutant (init twin, 64 neurons) 0.0111 < 0.5, so the round is valid. director-thought-review CONFIRMED: replay identical in every key but wall_s; a spy on solve() shows train rows only; the freq pick re-derived as pre-registered. Mechanism, measured by review after the run: top-peakiness picks share phase (R 0.897 k5, 0.892 k45 vs ~0.32 random at N=32) and span fewer dimensions (participation ratio 2.55 vs 3.6-4.3). Exploratory, not pre-registered: a phase-spread pick of the same families scores 0.9964 at 64, on par with random. SCOPE (council 3/3, plasma + remix asked the wording): the disproof is of the TOP-PEAKINESS within-family pick, not of 'key-frequency neurons suffice'. 496 of the 512 neurons sit in the four key families, so the random arm is a random pick INSIDE the circuit, not a non-circuit control; whether knowing the circuit beats not knowing it is untested here (plasma: model_s3.pt of datasets/osc-band/2026-10-01-neuron-period-seeds memorized without grokking and may be that control, census unmeasured). remix: the circuit needs JOINT phase spread (phi_a+phi_b and phi_a-phi_b), which a magnitude rank ignores. Next rungs queued in lap 2 (one leaf): remix's joint-phase circuit pick vs random vs OMP ceiling, and less-is-more's write-don't-pick neurons (m spread phases per key frequency, closed form, N_w <= 32); its conditional bend2 integer rung is CANCELLED (it was 'only if green'). no advantage of the circuit cut over random is shown on this net either. Residue: a phase-diverse pick needs its own pre-registered arm; the planted test-leak mutant is weak here (+0.006). v1 stamp correction: minted ~10:30Z, not 10:4xZ.
<!-- THOUGHT:END -->
