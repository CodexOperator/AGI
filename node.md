---
id: goal:g8.1
mint_id: 06a693d0580646d0924eaf956b8c12e8
type: goal
parents:
  - goal:g8
confidence: 1.0
edited_by: season.py
goal_id: G8.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - build:skills-agi-SKILL.md@v2
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G8.1: Decide the distribution shape: drop-in clone, skill package, or install"
---
**The engine currently arrives by being cloned into a project and gitignored.**
That was chosen to prevent vendoring (H0/H0b: a committed copy diverges
forever, and a stale one destroyed 29,264 files). It works, but it means every
project carries a full checkout it must remember to pull, and L9 already found
the gap: **the clone is unpinned and silently stale** — nothing declares which
engine version a project expects and nothing warns on drift.

Three candidate shapes, and the question is which one the engine should *be*:

1. **Drop-in clone (today).** Simple, pullable, no packaging step. Costs a
   checkout per project and has no version pinning.
2. **Skill package(s).** Most of the engine is Python scripts invoked by a
   skill; as features get more advanced the question is whether the `.py` files
   belong *inside* skill packages rather than beside them. This would make the
   engine installable the way every other skill is, and would fold naturally
   into **G1.2** (folding caveman/cavekit/gitnexus into one skill). Open
   question: whether a skill package is a sane home for ~15 entry points, a
   `src/` tree and a test suite, or whether that is stretching the format past
   what it is for.
3. **A real install** (`pip`/`uv` tool, pinned version). Clean dependency and
   version story; adds a release step and a packaging surface the project does
   not have today.

**Not a cosmetic choice — it decides who owns the engine's history.** Cloning
into a work repo keeps the engine out of the project's history and lets the
project maintain its own node set independently, which is the property that
makes forkability work at all. Any shape chosen must preserve that separation.

Pull L9's pinning gap in here regardless of the outcome: record the expected
engine commit in `agi-tree.config.json` and warn (never fail) on drift. That
closes the whole staleness class H0/H0b belong to, and it is cheap under any of
the three shapes.

**Related and load-bearing: S1.** Retiring `bin/` is partly a packaging
question — a directory of scripts named `bin/` is exactly what a package
layout would have to rename anyway, and it is currently costing GitNexus
coverage of all fifteen entry points.