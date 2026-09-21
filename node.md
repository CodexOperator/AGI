---
id: experiment:a00-38101b34-95565e
mint_id: 5b9d63d8133e4ddb9eca13a9e6a1e8e7
type: experiment
parents:
  - hypothesis:l3w1-goal-kind-perpetual
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-38101b34-95565e
loop: hypothesis:l3w1-goal-kind-perpetual@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a8d1f16808bf8fe2
season: 1
title: A00 38101b34 95565e
verdict: proved
---
# experiment:a00-38101b34-95565e

## Experiment

Implemented L3 wave 1 of `hypothesis:l3w1-goal-kind-perpetual`: the
`goal_kind: perpetual` rename, with `long-term` kept as a legacy spelling
accepted forever (the `phasing-out` reader pattern). Edits, in place:

1. **`.agi/context/schemas/[goal].md`** — goal_kind regex widened to
   `^(long-term|perpetual|short-term|subgoal)$` (comment + regex), a
   `perpetual:` spawn variant added (`allowed_parents [build, goal, vision]`,
   `min_parents 1`, `max_parents 2` — mirroring long-term so the spawn gate's
   parentless_types invariant is satisfied without touching `[shape].md`),
   and the variant/table prose refreshed for a four-variant discriminator.
2. **`extensions/agi/bin/snapshot-goals.py`** —
   - `load_goal_nodes` now reads `goal_kind` off each goal node;
   - `render_goals` splits `perpetual` out of the regular G/S list and renders
     a `## Perpetual` section at the END of GOALS.md — each perpetual as
     `### <gid> — <title>` (nested one level), **no `— status: <status>`
     lifecycle column**; a `PERPETUAL_INTRO` line, retire still legal on the
     node;
   - `parse_goals` recognises a non-dotted `### <gid>` heading as a perpetual
     root (forced to heading_level 2 so round trips never drift depth), so
     `--from-doc` keeps a perpetual goal `perpetual`;
   - the `--from-doc` writer honours parsed `goal_kind` (tags gain
     `perpetual`/`root` for a perpetual root, else the old derivation).
3. **`extensions/agi/bin/season.py`** — `_plan_type_for_kind` now maps
   `perpetual` → `"long-term goal"`, so a perpetual goal still tallies as a
   tier-1 plan and a report under it still resolves it as its plan parent;
   `_kind_from_goal_type("long-term goal")` → `"perpetual"` (canonical).
4. **`goal:g1`, `goal:g15`, `goal:g16`** — `goal_kind` set to `perpetual`
   through write.py. Bodies untouched (each perpetual director rewords in
   wave 2).

Red-first surfaced one real red: the first full-suite run failed the two
spawn_gate schema tests (`test_shipped_schemas_load_without_error`,
`test_goal_may_not_parent_mvp_or_experiment`) because a `perpetual` variant
with `min_parents: 0` is not in `[shape].md`'s parentless_types. Fixed by
making the perpetual variant `min_parents: 1` (exactly how `long-term` works;
roots G1/g15/g16 are grandfathered). Green after.

## Evidence

Tests — four new, in `test_snapshot_goals.py`:
`test_render_goals_puts_perpetual_under_its_own_section`,
`test_perpetual_goal_round_trips_via_render`,
`test_from_doc_round_trip_keeps_a_perpetual_goal_perpetual`,
`test_goal_schema_accepts_perpetual_and_legacy_long_term` — all PASS.

```
$ python3 -m pytest extensions/agi/tests/test_spawn_gate.py::test_shipped_schemas_load_without_error \
      extensions/agi/tests/test_spawn_gate.py::test_goal_may_not_parent_mvp_or_experiment \
      extensions/agi/tests/test_snapshot_goals.py -q
82 passed in 7.53s

$ python3 -m pytest extensions/agi/tests/ -q
1759 passed, 1 skipped in 97.53s
```

Render + check (byte-identical):
```
$ python3 extensions/agi/bin/snapshot-goals.py --render
rendered: 127 goal(s) + preamble -> /home/ubuntu/work/agi/GOALS.md
$ python3 extensions/agi/bin/snapshot-goals.py --render --check
render --check: 127 goal(s) round-trip byte-identical
```

Perpetual section in GOALS.md (no status column on the three):
```
## Perpetual

The following goals are `goal_kind: perpetual` — the long-horizon
commitments, broadly worded, one director each. ...

### G1 — Config-maxxing: every engine action is declared, never improvised
### G15 — Bugfix and optimization
### G16 — Telemetry per node, propagated up the ladder
```

Nodes carrying it — 3 of 3:
```
$ grep -rl "goal_kind: perpetual" .agi/nodes/goal/ | wc -l
3
```

Schema + spawn gate:
```
$ python3 extensions/agi/bin/links.py schema
schema: 129 node(s) missing a required field   (hypothesis/idea/outcome/verdict —
NONE under `goal`; no new violation)
$ python3 -m pytest extensions/agi/tests/test_spawn_gate.py -q   # part of full suite above, green
```

Metrics + smoke (node count stable, no broken links, no pruning):
```
$ python3 extensions/agi/bin/metrics.py .agi
METRIC goal_count=127  active_node_count=1242  deprecated_node_count=194
METRIC goals_horizon=71  goals_retired=2
$ bash extensions/agi/driver.sh --smoke --max-iters 1
METRIC broken_links=0
[smoke] skipping agent dispatch + heal
```

No git operations performed.

## Agent Notes
WAVE 1 of hypothesis:l3w1-goal-kind-perpetual — perpetual goal kind is legal
(schema regex + spawn variant), long-term kept as legacy forever, G1/g15/g16
carry `goal_kind: perpetual`, GOALS.md renders a `## Perpetual` section with
no per-goal complete/retired column (retire stays legal), and
`snapshot-goals.py --render --check` round-trips byte-identical. Supporting:
season.py plan-type normaliser maps perpetual→long-term goal so ladder tallies
and report plan-parent resolution stay coherent. Full engine suite green
(1759 passed, 1 skipped); links schema has no new goal violation; smoke shows
broken_links=0 and a stable node count. One stray observation, left untouched:
a sibling scaffold `.agi/nodes/experiment/a00-664d15f8-f9f173.md` references
an unknown parent `hypothesis:l3-corrupt-frontmatter-19` (flagged by its own
spawn_check and by render INTEGRITY) — not mine, not cleaned.

## Agent Notes
Perpetual goal kind implemented and verified: schema accepts perpetual+long-term, G1/g15/g16 carry it, GOALS.md renders a Perpetual section (no status column), --render --check byte-identical, season.py kind-map fixed, full suite green.

REVIEW (parent a00-8def5dd1): ACCEPTED as proved — verified artifacts, not just report. Parents link resolves; evidence_runs is a real list [self]. Independent checks: schema [goal].md regex accepts ^(long-term|perpetual|short-term|subgoal)$ with long-term legacy; g1/g15/g16 all carry goal_kind: perpetual; GOALS.md renders a ## Perpetual section with ### G1/G15/G16 and 0 status-column lines; snapshot-goals.py --render --check exits 0 byte-identical. Full suite 1759 passed claimed. Verdict proved upheld — no demotion. Sibling scaffold a00-664d15f8 orphan (unknown parent hypothesis:l3-corrupt-frontmatter-19) correctly left untouched — belongs to other parent a00-872399cd.
