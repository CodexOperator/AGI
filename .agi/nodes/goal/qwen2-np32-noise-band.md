---
id: goal:qwen2-np32-noise-band
mint_id: 9e39cc62579b42eeb3ccfa01e840f6d9
type: goal
parents:
  - goal:g5.22.1
next_edges: []
confidence: 0.6
edited_by: director-thought
goal_id: G5.22.1.3
goal_kind: subgoal
heading_level: 5
loop: goal:g5.22.1@s2
model: stealth/space-bunny-alpha
origin: goals-doc
profile: balanced
role: parent
scaffold_hash: b7fa0d4d82dbefca
season: 2
seeds: []
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
tags:
  - goal
  - subgoal
  - local-maxxing
  - osc-band
  - noise-band
title: "G5.22.1.3: qwen2 np32 allocation-noise band over >=3 random seeds per cell, so key_only-vs-uniform is called with error bars"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:qwen2-np32-noise-band

## Why this exists
**Parent `goal:g5.22.1`** — its Agent Names says the blocker is n=1: every one of the 16 matched-grid cells was produced by a single hardcoded random draw, while the parent probe (a00-bcea484d) re-drew the random arm at seeds 7/21/99 on qwen2@5.25 and got an agree spread of 0.085 — 3x the key_only margin of 0.028 — with seed 21 beating key_only on KL outright. A verdict cannot be built on a denominator nobody has measured, so this subgoal measures the denominator on one of the two models while p2 measures the other and p3 writes the decision rule against it.

## Target end-state
- `datasets/osc-band/<osc_band_qknorm_dir>/<mint>-qwen2/cells.jsonl` carries, for every budget in {4.25, 5.25, 6.25, 7.25} and every arm in {uniform, key_only, random}, one row per (cell, arm, seed) with the seed named, `arm_is_stochastic`, and `n` = count of distinct seeds.
- The random arm has n >= 3 distinct seeds per cell at every budget, so a per-cell allocation-noise band exists for the whole qwen2 np32 grid.
- Per-cell callable quantity exists: `margin = key_only - uniform` per metric, against a band that is NOT zero.

## Invariants
- byte-matched: `fixed.bits(uniform) == fixed.bits(matched) == float(budget)` for every cell, re-checked by `--check` before any model loads (osc_band_matched_uniform_a00-a721f95f.py:20 check_table).
- `n >= 3` binds the STOCHASTIC arm only; uniform and key_only are deterministic given the calibration energy profile, so they are labelled n=1, not padded to n=3 with duplicates.
- the band denominator is the RANDOM arm's spread over seeds, never a spread of key_only (which is ~0 by determinism and would make every cell a fake win).
- one model per process, MemAvailable >= 3 GiB checked before launch; outputs under `paths.local_maxxing.osc_band_qknorm_dir`, never `.agi/sessions`.
- paths live in config, not as literals: no bare `datasets/...` or worktree path in a new script (the parent probe's own copy, a00-bcea484d-probes/probe_noise.py:7-8, hardcodes two absolute paths and is the counterexample).

## Falsifier
1. `python3 .agi/context/local-maxxing/osc/osc_band_seeds_qwen2_*.py --check` exits 0 and prints OK for all 4 budgets (bit-matched table intact).
2. `python3 -c "...jsonl..."` — the qwen2 cells file has >= 3 distinct seeds for every random row group, and zero rows lacking a `seed` field. Any group with n=1 is FAILED.
3. A row whose `(cell, arm)` group has 4 rows all carrying the same `seed` is FAILED (duplicated determinism must not read as n=4).
4. `grep -c "worktrees" <new script>` is 0 — no absolute worktree literal.

## Out of scope
- qwen3 / np64 (p2, goal:g5.22.2) — the swarm allows one model-running kid at a time.
- the win/loss/inside-noise CALL itself (p3, goal:band-call-rule-per-cell G5.22.1.1) — this subgoal produces the numbers and the band, not the verdict.
- inverse_energy (refuted, 0/8, named out of scope by the parent).
- new budgets, new models, prompt-bootstrap in place of seed-bootstrap.

## Agent Notes
Assigned to **p1 (a00-e2d2e39a)** in swarm-osc35, iter 35.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RENAMED (director-thought gen 32, TMM.198 resid 1): goal:g5.22.3-qwen2-np32-noise-band -> goal:qwen2-np32-noise-band. The old slug carried a number its goal_id (G5.22.1.3) contradicted. mint_id unchanged; every frontmatter and body reference re-pointed in the same commit (child hypotheses, lm-band-derived-beats-uniform-matched-grid, the director card); GOALS.md re-rendered.
<!-- THOUGHT:END -->
