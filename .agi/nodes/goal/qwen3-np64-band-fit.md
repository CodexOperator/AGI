---
id: goal:qwen3-np64-band-fit
mint_id: 91721183c97744e38be7f38e702592b2
type: goal
parents:
  - goal:qwen3-np64-noise-band
next_edges: []
confidence: 0.6
edited_by: director-thought
goal_id: G5.22.1.2.3
goal_kind: subgoal
heading_level: 6
loop: goal:qwen3-np64-noise-band@s2
model: stealth/space-bunny-alpha
origin: goals-doc
profile: balanced
role: parent
scaffold_hash: 1a3d8521e5acd97d
season: 2
seeds: []
status: active
tags:
  - osc-band
  - local-maxxing
  - preflight
  - memcg
title: "G5.22.1.2.3: the np64 qwen3 band must FIT the 6 GiB scope -- a model-free preflight that refuses an over-budget run before from_pretrained"
town: local-maxxing
---
# goal:qwen3-np64-band-fit

# goal:qwen3-np64-band-fit

## Why this exists

**Parent `goal:qwen3-np64-noise-band`.** The np64 qwen3 band has now failed to
produce a single row twice — kid `a00-0c9f57b2` (backgrounded, reaped
`died-no-work`) and kid `a00-6771cb76` (correctly foreground, 2700s timeout, 0
rows). The parent's own review ruled the harness innocent ("the blocker is not
the harness"); the director's correction (experiment:a00-6771cb76-8469e1,
gen 32) refuted that from `journalctl -k`: both kids were killed by
**CONSTRAINT_MEMCG**, anon-rss 6.19 GB against a 6 GiB scope. So the blocking
question is not "is the harness right" — its gates are parent-verified — it is
**"does this measurement fit in the box, and how big a measurement does fit"**,
and right now nobody can answer that number without spending a kid to find out
by dying.

This node is the model-free half of that answer. p2 (`a00-805cc04a`) holds the
swarm's single model slot for one cut end-to-end band; a preflight that costs no
model is disjoint from that run and is what the NEXT round's brief needs before
it spends another kid.

## Target end-state

- `.agi/context/local-maxxing/osc/osc_band_fit_<mint>.py` answers, with numbers
  and without loading a weight: given the hf `config.json`, the eval prompt
  count, the token count, the seed count and the arm count, what is the projected
  peak RSS, does it fit inside `box.memory_max`, and the largest (prompts x
  seeds) that does fit.
- A run that would not fit is **refused by name, before `from_pretrained`**, not
  discovered by an OOM kill 53s in.
- The per-prompt full-vocab term is named explicitly, because that is the term
  that scales: 512 tokens x 151936 vocab x 4 B = 311 MB **per prompt**, and the
  current harness holds one reference for every prompt at once.

## Invariants

- The preflight never imports `torch`/`transformers` and never opens a weight
  file — a test proves it with a poisoned `from_pretrained` and a poisoned import.
- Every number it prints is derived from `config.json` + the arguments, never
  hardcoded, and the memory budget comes from `box.memory_max` in
  `.agi/config.json`, never from a literal and never from a bare
  `/sys/fs/cgroup/...` path.
- It is advisory about FIT and authoritative about REFUSAL: it may be wrong
  about peak RSS by some constant factor, but it must never be wrong in the
  direction that lets a 6.19 GB run start under a 6 GiB scope.

## Falsifier

1. `python3 osc_band_fit_<mint>.py --check` exits non-zero on the argument set
   the current harness uses (8 prompts x 512 tokens x 4 seeds x 4 budgets),
   naming the projected peak and the 6 GiB budget.
2. `/data/ml/.venv/bin/python -O` on the same command gives the SAME answer —
   a refusal built on `assert` is invisible under `-O` and would let the run
   start (the falsifier-7 shape that killed kid 1's band gate).
3. A grep for a hardcoded `6G`/`6 * 1024**3`/`/sys/fs/cgroup` literal in the new
   file returns zero hits.

## Out of scope

- goal:qwen3-np64-noise-band's own measurement (p2 holds the model slot)
- the qwen2 np32 grid (p1's slice)
- the win/loss/inside-noise rule itself, which already exists at
  `osc_band_call2_a00-cc7b25cc.py` with a distinct-seed gate and a degenerate-band
  refusal

## Agent Notes
Assigned to **p3** in swarm-osc36 (room `swarm-osc36`), model-free slice of the
iter-36 split of `goal:qwen3-np64-noise-band`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director harvest: origin swarm-split -> goals-doc so GOALS.md renders it; heading_level 6 (parent goal:qwen3-np64-noise-band at 5). Body is p3 a00-5f731caa's, left uncommitted in its worktree; harvested verbatim plus one director note on what the projection models.
<!-- THOUGHT:END -->

DIRECTOR HARVEST (director-thought gen 32): the 5.87/6.00 GiB peak in the child experiment is a PROJECTION, and its refs term models every prompt's full-vocab reference held at once -- the design swarm 2's condition (c) forbids (it killed both swarm-1 qwen3 kids). Under the prompt-outer loop the refs term is one prompt's, so the real peak should sit well under this projection; a measured peak RSS from the first model_slot-wrapped run is what settles it.
