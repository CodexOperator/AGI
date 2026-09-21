---
id: experiment:s26-premature-complete-guard-accepts-wrapper-frontmatter
mint_id: 6f4fb141214047eba396fc6871c3d916
type: experiment
parents:
  - hypothesis:a00-11389962-70e33e
next_edges: []
edited_by: a00-7f6f1f95
evidence_runs:
  - experiment:s26-premature-complete-guard-accepts-wrapper-frontmatter
line_ceiling: 40
loop: goal:g7.27@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 20
profile: balanced
role: kid
scaffold_hash: 748b23ad5c4600db
season: 2
title: Fix goal:s26 premature-complete guard to accept wrapper node records
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:s26-premature-complete-guard-accepts-wrapper-frontmatter

## Experiment

**Claim under test:** `snapshot-goals.warn_premature_complete` (goal:s26) must
see wrapper-shaped node records — `{path, origin, fm, body}` as returned by
`load_existing_nodes()` — so `snapshot-goals.py --render --strict-goals`
actually emits premature-complete warnings on the real render path. The
previous body read the value as a flat frontmatter dict, so on the live path
it always returned `[]` while the flat-dict unit tests stayed green.

### Pre-fix measurement (baseline, reproduced before the change)

Probe `.agi/sessions/iter-DH.12/a00-11389962/probe_wrapper.py` builds the same
pair in both shapes — complete root `G5`, live subgoal `G5.1`:

```
flat    offenders: [('G5', 'G5.1', 'horizon')]
wrapper offenders: []
```

The wrapper result is the defect: the live path is the wrapper one.

### Build (production, `extensions/agi/bin/snapshot-goals.py`)

- added `_frontmatter(node)` (L944-955): returns `node['fm']` when it is a
  dict, else the node itself, so both shapes reach the same code.
- `warn_premature_complete` (L974, L987) now reads through `_frontmatter`
  instead of treating the value as flat frontmatter.
- No other sibling assumed flat fm: `collect_parent_refs`,
  `report_integrity`, `load_goal_nodes`, `_sources_snapshot`, `_goal_count`
  and the doc-import sweep already read `node['fm']` / `node['origin']`.

### Post-fix probes

- `probe_wrapper.py`: both shapes now warn —
  `flat [('G5','G5.1','horizon')]`, `wrapper [('G5','G5.1','horizon')]`.
- `probe_live.py`: `load_existing_nodes()` values carry keys
  `['body','fm','origin','path']`; the real tree has no premature-complete
  pair right now, so it returns `[]` (a true negative, not the old silence).
- `probe_inject.py`: real `load_existing_nodes()` output plus one injected
  wrapper-shaped complete-root/live-child pair emits
  `WARN: goal ZZZ is \`complete\` but subgoal ZZZ.1 is \`active\` ...` and
  returns `[('ZZZ','ZZZ.1','active')]`.
- `probe_render_wire.py` (end-to-end wire): a synthetic project with a
  complete root `G5` and live subgoal `G5.1`, run through
  `cmd_render(check=False, strict_goals=False)` — the same function
  `--render` calls — returns 0 and emits the `goal:s26` warning on stderr.
  This is the live path the defect said was silently inert.

### Regression test (test file, excluded from the production ceiling)

`extensions/agi/tests/test_lifecycle_guards.py`:
- `_wrapper(nid, fm)` helper minting the live `{path, origin, fm, body}` shape.
- `test_wrapper_shaped_nodes_warn_on_the_real_render_path` — wrapper records,
  asserts the `(G5, G5.1, active)` offender and the `goal:s26` stderr warning.
- `test_both_shapes_agree` — flat and wrapper content yield identical
  offenders, so neither caller is privileged.

### Measurements

- `git diff --numstat -- extensions/agi/bin/snapshot-goals.py` → `17  3`
  (production lines changed = 20, ceiling 40; experiment note: under 2x).
- `python3 -m pytest extensions/agi/tests/test_lifecycle_guards.py
  extensions/agi/tests/test_snapshot_goals.py -q` → **108 passed**, 39
  warnings (15.10s). The warnings are pre-existing `utcnow()` deprecations.

`dispatch.py` untouched; no MAIN push; no `--post`/`--seat`; no git writes
(only the allowed read-only `git diff --numstat`).

## Evidence

```
flat    offenders: [('G5', 'G5.1', 'horizon')]
wrapper offenders: [('G5', 'G5.1', 'horizon')]

live value keys: ['body', 'fm', 'origin', 'path']
live offenders: []

WARN: goal ZZZ is `complete` but subgoal ZZZ.1 is `active` — an overarching
  goal is not complete while its subgoals are live (goal:s26)
injected wrapper offenders: [('ZZZ', 'ZZZ.1', 'active')]

# probe_render_wire.py (cmd_render end-to-end)
rendered: 2 goal(s) + preamble -> /tmp/.../GOALS.md
cmd_render rc: 0
stderr: WARN: goal G5 is `complete` but subgoal G5.1 is `horizon` — an
  overarching goal is not complete while its subgoals are live (goal:s26)
WIRE OK

108 passed, 39 warnings in 15.10s
```
