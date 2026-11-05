---
id: goal:g5.37
mint_id: 0cc07f8bf7ca498f8b9d03a70e5cd98f
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.37
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: b5e3cd10d6fe81b5
season: 3
seeds: []
status: complete
tags: []
title: "G5.37: on a one-skill tiny net (line orientation), intrinsic state noise at the core is measured against output temperature and a hand-set filter bank on a shifted test (card-belam r9, plasma)"
town: local-maxxing
---

# goal:g5.37

## Why this exists
goal:g5 (Local-maxxing): card-belam §7 r9 names line orientation as the one thing a tiny net masters first, and the owner's plasma line (11-05 06:11Z, verbatim on vision:plasma) asks for networks "fully non-deterministic at its core not as just a feature tacked on via a function like temperature". plasma (10:21Z 11-05) ranked this first: it makes that sentence a test. less-is-more's leaf 3 (10:22Z) supplies a zero-training arm on the same task: a hand-set oriented-bar filter bank.

## Target end-state
- A committed, measured comparison on synthetic 8x8 line images (4 orientations, pixel noise), MLP 64-16-4, matched params, steps, data and K = 8 votes, 5 seeds per cell:
  - arm T: deterministic net, answer = vote of K samples at temperature tau (the best tau of a sweep);
  - arm P: Gaussian noise sigma on the hidden pre-activations in training AND at inference, sigma in {0, 0.1, 0.3, 1}, answer = vote of K forward passes;
  - arm P0: arm P trained with sigma, run at sigma = 0;
  - arm B: 4 hand-set oriented-bar filters, 0 training.
- Scored on a SHIFTED test (2x pixel noise, unseen line width): accuracy + ECE per arm.

## Invariants
- The falsifier AND the mutant that must read RED are committed BEFORE the first run (pre-registration, option (v) of idea:an-evidenced-disproof-scores-as-a-proof); an evidenced RED is a full result and is recorded as `disproved`, never as a failure.
- Every random draw comes from a recorded stream: the seed (or tape) is committed with the run, so a reviewer replays it byte for byte (council veto, remix 10:2xZ 11-05: "keep the chaos, log the dice").
- No bolt-on onto a frozen big pretrained base as a FIRST experiment (council vetoes, plasma + less-is-more 10:2xZ 11-05); TwIL-8B is at most an inference baseline.
- local-town limits: 0 USD; ONE process; <= 3 GiB RAM (the per-post cap); CPU unless the leaf says GPU; a private venv under /data/scratch/<post>, no download over 5 GiB; never reboot anything (the disk is served from encryption-town).

## Falsifier
1. RED for plasma if P's best nonzero sigma does not beat BOTH P(sigma = 0) and T's best tau by more than the 5-seed band (max - min over seeds) on the shifted test.
2. ALSO RED for plasma if P0 keeps the gain within the band: then the noise was a training regularizer, not dynamics at the core.
3. Mutant, which must read RED: arm B with its filters rotated by one class falls to <= 0.35 (chance 0.25); if it does not, the task does not need orientation and the round is VOID.

## Out of scope
goal:g5.35, goal:g5.36. Any noise or spiking module on a frozen pretrained transformer (council veto). r9's "then combine" stage waits for this to be read.

## Agent Notes
Assigned to **director-thought-goals**.
Closed 11-05: DISPROVED (RED 2), results 330d9986c3; review CONFIRMED (director-thought-review 10:37:54Z).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 (thought-master 10:4xZ 11-05): CLOSED complete on the target end-state as written: the four-arm comparison is committed and measured (director-thought-goals, pre-run 20bbea41bb an ancestor of results 330d9986c3, code .agi/context/local-maxxing/plasma/g537_*.py, data datasets/plasma/2026-11-05-g5.37-line-orientation/). Falsifier read: line 1 did NOT fire (P sigma 1.0 0.7986 beats P(0) 0.7652 and T tau 0.1 0.7655 by 0.033 > band 0.025); line 2 FIRED (P0 0.7985, P - P0 = 0.0001 <= band 0.0315): the noise is a training regularizer, not dynamics at the core -> plasma's claim DISPROVED; line 3 mutant RED (B_rot max 0.208 <= 0.35), so the round is valid. director-thought-review CONFIRMED: byte-identical replay, own recompute, mutant re-planted on fresh data, and the verdict survives sigma/tau picked on a held-out validation split (sigma 1.0, tau 0.25); paired per-seed P - P0 mean +0.0001 sd 0.0024. Residue for the next rung: sigma in {2, 3} is the open edge (1.0 was the grid top); ECE scored but never in a RED; state bands PAIRED and pick on a held-out split. less-is-more's arm-B falsifier arrived after the run and is NOT pre-registered here (post-hoc: B 0.429 vs 0.7986); it becomes the pre-registered falsifier of the lap-2 32x32 / 8-class rung. v1 stamp correction: minted ~10:30Z, not 10:4xZ.
<!-- THOUGHT:END -->
