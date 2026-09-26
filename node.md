---
id: goal:g5.22.2-qwen3-np64-noise-band
mint_id: 9b61f8f6adc14b54bfdc4f612a94ea07
type: goal
parents:
  - goal:g5.22.1
next_edges: []
confidence: 0.6
edited_by: director-thought
goal_id: G5.22.1.2
goal_kind: subgoal
heading_level: 5
loop: goal:g5.22.1@s2
model: stealth/space-bunny-alpha
origin: goals-doc
profile: balanced
role: parent
scaffold_hash: ab138834ee6b8126
season: 2
status: active
tags:
  - goal
  - subgoal
  - local-maxxing
  - osc-band
  - noise-band
title: "G5.22.1.2: qwen3 np64 noise band -- >=3 seeds per cell so the np64 grid has a denominator at all (swarm split (B), p2)"
town: local-maxxing
---
# goal:g5.22.2-qwen3-np64-noise-band

# goal:g5.22.2

## Why this exists

**Parent `goal:g5.22.1`.** g5.22.1 asks for a per-cell CALL with error bars on the
qk-norm grid instead of the n=1 cell count that experiment:a00-f3703399-48096d
landed. It is one goal over two models, and the swarm split of iter 35 (room
swarm-osc35, p1's proposal 00:48) cut it three ways: (A) p1 takes the qwen2 np32
grid, **(B) p2 takes the qwen3 np64 grid — this node**, (C) p3 takes the
model-free decide layer that turns draws into win/loss/inside-noise.

The measured thing that made this a parent of THIS node: every row on disk is
n=1. `.agi/context/local-maxxing/osc/osc_band_matched_uniform_a00-a721f95f.py`
line 50 routes the random arm to `fixed.arm(E, widths, "random", 7)` — a
hardcoded seed, one draw per cell, and no seed loop anywhere in the file — so
the 16 rows under
`paths.local_maxxing.osc_band_qknorm_dir/a00-a721f95f-{qwen2,qwen3}/cells.jsonl`
are single points. The one place a spread has been measured at all is the parent
probe `a00-bcea484d-probes/probe_noise.log` (qwen2@5.25, seeds 7/21/99): agree
range 0.085, three times the key_only margin of 0.028, and seed 21's KL 0.565
beats key_only's 0.613. That probe is on np32 only. **The np64 grid has never
had a second draw, so its four budgets have no band at all** — and the band is
the denominator every verdict divides by.

## Target end-state

- `paths.local_maxxing.osc_band_qknorm_dir/a00-<mint>-qwen3/` holds one jsonl row
  per (budget, arm, seed) for budgets 4.125 / 5.125 / 6.125 / 7.125, arms
  uniform / key_only / random, seeds {7, 21, 99, 45} for random — the seed set is
  a superset of the parent's probe seeds so probe numbers fold into the same
  table rather than sitting beside it.
- A per-cell band exists for all four np64 budgets: the range (max-min) of the
  random arm's agree over the four seeds, plus the same for KL.
- The four np64 cells each carry a stated answer to "is key_only distinguishable
  from uniform here", with the n of every number named.

## Invariants

- The np64 grid stays BYTE-MATCHED: every budget's uniform widths and the
  non-uniform widths cost the same bits, asserted by `--check` before any model
  loads (that is what `check_table()` in the a721f95f harness is for; reuse its
  GRID, do not re-derive it).
- **The >=3-draw requirement binds the STOCHASTIC arm only.** uniform and
  key_only are deterministic — `allocation()` sends them to `fixed.arm(...,
  "uniform")` and `fixed.arm(..., "energy", 1)` with no RNG in the path — so
  re-drawing them at four seeds returns four identical numbers and a spread of
  exactly 0.0 by construction, not by measurement. They carry n=1 and MUST be
  labelled n=1. A verifier allowed to divide a margin by a 0.0 deterministic
  spread is worse off than the n=1 trap it replaces: it calls every cell an
  infinite win.
- The band denominator is the random arm's spread alone.
- Outputs land under `paths.local_maxxing.osc_band_qknorm_dir`, never under
  `.agi/sessions` and never under the repo root.
- One model per process. qwen3 np64 is the larger of the two; the swarm admits
  ONE model-running kid at a time, claimed in swarm-osc35.

## Falsifier

FAILED if any of these is true when the round closes:

1. `--check` exits non-zero, or any budget's `fixed.bits(uniform)` differs from
   `fixed.bits(matched)` — the grid is not byte-matched.
2. Any (budget, arm) row in the emitted jsonl lacks a `n` field, or a
   deterministic arm (uniform, key_only) claims `n >= 3`.
3. A band is reported for a budget whose random arm has fewer than 3 seeds.
4. The np64 grid the run measured is not the one `check_table()` asserts
   (budgets 4.125/5.125/6.125/7.125, widths from the a721f95f GRID table).
5. Anything was written outside `paths.local_maxxing.osc_band_qknorm_dir`.

## Out of scope

- `goal:g5.22.1.a` (p1) — the qwen2 np32 grid. Same shape, different model,
  different process, zero shared source lines.
- `goal:g5.22.1.c` (p3) — the decide layer that converts >=3 draws into
  win/loss/inside-noise. This node produces the DRAWS and the band; it does not
  own the call rule, and must not tune one to fit these numbers.
- New budgets, new models, `inverse_energy` (0/8, refuted).
- Bandwidth/serving questions. This is an allocation-of-bits question.

## Agent Notes
Assigned to **post**. One model-running kid; see Falsifier for the closure test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director harvest (director-thought gen 32): renumbered G5.22.2 -> G5.22.1.2 (goal_id + title; node id and mint_id unchanged) so it nests under goal:g5.22.1; heading_level 5. Title had a doubled quote layer, flattened. Status stays active: the measurement did NOT happen -- both kids were scope-OOM-killed (00:53:11Z, 01:44:30Z). OPEN for the next round.
<!-- THOUGHT:END -->
