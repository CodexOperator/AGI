---
id: experiment:g1714-heading-level-residue
mint_id: 1a88e6ea331945d2b8f7a4072d17ceaa
type: experiment
parents:
  - hypothesis:a00-f41683a4-7b27fd
next_edges: []
edited_by: a00-f41683a4
evidence_runs:
  - experiment:g1714-heading-level-residue
line_ceiling: 40
loop: goal:g17.14@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 26
profile: balanced
role: kid
scaffold_hash: 249d4a15be20a508
season: 2
title: heading-level declared, subgoals at depth 4, id-prefix depth guard refusing by name
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:g1714-heading-level-residue

## Experiment

Fix-only round on the `goal:g17.14` family, DT.19, checkout `a00-254721e3`.
No grok adapter/config files touched (owned elsewhere). Production lines:
`snapshot-goals.py` +23/-0, `[goal].md` +3/-1, measured with
`git diff --numstat` (read-only; no commit). Test file excluded.

### Pre-fix state

`python3 extensions/agi/bin/snapshot-goals.py --render --check` -> rc=1:

```
ERR: .../.agi/nodes/goal/g17.14.1.md has no heading_level; run
`snapshot-goals.py --from-doc` once to backfill it before rendering (goal:g6.9)
```

Scan of `nodes/goal/*.md`: 193 goal nodes total; exactly 3 lack
`heading_level` (`goal:g17.14.1/.2/.3`); exactly 4 lack `origin: goals-doc`
(`goal:g14.2/.3/.4/.5`).

### Writes (sanctioned writer only)

```
write.py goal:g17.14.1 'set heading_level 4'
write.py goal:g17.14.2 'set heading_level 4'
write.py goal:g17.14.3 'set heading_level 4'
```

Value 4, not 3: the parent `goal:g17.14` is level 3 and the disk doc already
carries `#### G17.14.1/.2/.3`. `--from-doc` is NOT usable here — `SUBGOAL_RE`
only matches `###` dotted ids and cannot see `####` subgoals.

Schema `.agi/context/schemas/[goal].md`: added `heading_level: {type: int}` to
`fields:`, `heading_level` to `validation.required:`, and `heading_level: int`
to `validation.types:`.

Guard in `snapshot-goals.py::load_goal_nodes`: collects each rendered goal's
`parents` and refuses BY NAME when a goal's `goal_id` nests under a named
parent's `goal_id` (`G17.14.1` under `G17.14`) but `heading_level !=
parent.heading_level + 1`.

### Measured results

- **gate/missing** (scratch copy, `heading_level:` stripped from g17.14.2):
  rc=1, error names the file:
  `ERR: .../g17.14.2.md has no heading_level; run ...`
- **gate/wrong-depth** (scratch copy, `g17.14.1` set to 3 under the level-3
  parent): rc=1, named refusal:
  `ERR: .../g17.14.1.md (G17.14.1) has heading_level 3 but its parent
  goal:g17.14 (G17.14) is level 3; must be 4 (goal:g17.14)`
- **gate/origin**: `load_existing_nodes` 193 goals, `origin: goals-doc` 189,
  lacking origin 4 = `['goal:g14.2','goal:g14.3','goal:g14.4','goal:g14.5']`;
  `load_goal_nodes` returns 189 and the set missing from the render is exactly
  those 4 ids. Mechanism is `snapshot-goals.py` `if node.get("origin") != ORIGIN:
  continue` — the excluded ids are ACTIVE goals with live node files, not stale
  sections, so `origin` must not be silently added to them.
- **wire/right**: `G17.14.1/.2/.3` each render with 4 hashes
  (`#### G17.14.1 — ...`) and each node reads `heading_level: 4`.
- **gate/guard-false-positive**: under the blanket "any named goal parent" rule
  the measured violation count is **39** (35 S-goals -> `goal:g15`, plus
  `goal:g14` -> `goal:g4`, `goal:g3.2` -> `goal:g16.1`, `goal:g15.26` ->
  `goal:g15.25`). Under the id-prefix predicate: **0**. So the guard uses the
  id-prefix predicate; the blanket rule the brief described would refuse 39
  legitimate nodes.
- **gate/G17.14-section**: the `### G17.14` section rendered from nodes is
  byte-identical to `GOALS.md` on disk (`5196 == 5196` bytes).
- **gate/final (global)**: `--render --check` is rc=1 with
  `MISMATCH, 1260 diff line(s)`. **Pre-existing and not this chain's**: `GOALS.md`
  is stale against other live agents' uncommitted node work (`G1.18`/`G1.19` in
  nodes, absent from the doc; `G1.1 legacy-direct` in the doc, not rendered).
  Zero diff lines touch `G17.14`. Not re-rendered: 1260 lines of derived churn
  from other chains is the loop's to own, not this round's.
- **tests**: `python3 -m pytest extensions/agi/tests/test_snapshot_goals.py
  extensions/agi/tests/test_links.py -q` -> **108 passed**; after adding two
  guard tests, `test_snapshot_goals.py` alone -> 88 passed.

## Evidence

Checkout `a00-254721e3`; commands and outputs above. Scratch probes under
`.agi/sessions/iter-DT.19/a00-f41683a4/`. The `--render --check` diff stream
(1260 lines) was captured to `.../check.err`, 62 printed lines, none naming
`G17.14`.
