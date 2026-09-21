---
id: goal:s6
mint_id: 7b5e4b82d1844a56bf67898c520bf0eb
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S6
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S6: Strip agi-tree to the graph and its inputs"
---
Done 2026-08-23. `agi-tree` had accumulated a second copy of most of `agi`:
~95 one-off `exp-*.py` / `extend-*.py` scripts at the root, a vendored engine
tree (`src/`, `tests/`, `engines/` — the copy **G7.7** wanted retired), the
cavekit-era runner, both `.STALE-DO-NOT-USE` snapshot scripts, a duplicate
`skill/autoresearch-tree/` under the pre-rename name, and 768 tracked session
transcripts. 1,026 files, −281k lines; git history is the archive.

**The rule that replaces it, now in `CLAUDE.md` as a table:** this repo holds
`nodes/`, the inputs the nodes are derived from (`GOALS.md`, `context/kits/`,
`context/plans/build-site.md`, `context/schemas/`), and `agi-tree.config.json`.
A `.py` file added here belongs in the engine.

> `GOALS.md` moved out of that list on 2026-08-25 (goal:g6.9): it is now
> **derived from** `nodes/goal/`, not an input to it. The table in `CLAUDE.md`
> is the live version, as this sentence already says — the list above is what
> it read when this goal closed.

The engine arrives as a gitignored clone at `agi/`, the way `fantasia` takes it,
so `driver.sh --smoke` runs from this repo with no install step. That is an
interim shape and **G8.1** still owns the real answer — it is a second working
copy of a repo that also lives at `~/work/agi`, and G6.5 wants exactly one
stitch target. Recorded here so the interim is not mistaken for the decision.

The duplicate skill was deleted rather than re-pointed: `~/.claude/skills/agi`
already symlinks to `agi/skills/agi`. One skill, one source — **G1.2**'s first
concrete step, taken by subtraction.

Two things this surfaced that were not housekeeping:

- **`agi` was 11 commits ahead of `origin`** — exactly **S5**'s defect, caught
  because a fresh clone would have pulled an engine 11 commits stale. Pushed
  before cloning. S5's standing arrangement is still open.
- **`context/kits/` and `context/plans/build-site.md` are generators, not
  stale output.** They mint 159 of 661 nodes, and `snapshot-build-site.py`
  unlinks every `origin: build-site` node it does not re-derive on a run — so
  deleting them prunes a quarter of the graph silently, at loop time rather than
  at delete time. Kept, and the hazard is written into `CLAUDE.md`. This is the
  **H0i** class a third time, and the third time it was found by reading the
  script rather than by losing the data.

Verified: `driver.sh --smoke --max-iters 1` completes and `nodes/` is
byte-identical afterwards.

**Left standing on purpose:** `nodes.db` (7.8 MB, gitignored — **G7.6** owns the
persistence question, and deleting it while two loaders disagree is not
cleanup), and the `.claude/worktrees/` worktree still registered against a
`~/.hermes/agi-tree/` path (**S4** C5, which is gated and explicitly last).