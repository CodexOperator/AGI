---
id: experiment:a00-5b5defc6-7baa29
mint_id: 66120ae60b3949b1bd7d6455198ab73f
type: experiment
parents:
  - hypothesis:l4-env-root-override-descends-never-ascends
next_edges: []
confidence: 0.92
edited_by: a00-325a5d78
evidence_runs:
  - experiment:a00-5b5defc6-7baa29
loop: hypothesis:l4-env-root-override-descends-never-ascends@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8073eae9fe2684a5
season: 2
title: A00 5b5defc6 7baa29
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5b5defc6-7baa29

## Experiment

Tested `hypothesis:l4-env-root-override-descends-never-ascends`: the consumer of
`AGI_TREE_PROJECT_ROOT` (and the other `PROJECT_ROOT_ENV_VARS`) reads only one
of the two things its producers put in it, and both existing senses are
`proved` by this run.

**Reproduce (before fix):**
```
$ AGI_TREE_PROJECT_ROOT=/home/ubuntu/work/agi/.agi/worktrees/seat-sanctuary-director \
    python3 extensions/agi/bin/snapshot-goals.py --render --check
no origin=goals-doc goal nodes under /home/ubuntu/work/agi/.agi/worktrees/seat-sanctuary-director/nodes/goal
  — refusing to write an empty GOALS.md
EXIT=1
```
The env value was the WORKTREE REPO root (`<repo>`), but the consumer treated it
as the graph root and looked for `<repo>/nodes/goal` (which does not exist; the
nodes live at `<repo>/.agi/nodes/goal`). Blast radius: `goals-check` resolves
purely from the env, so every dispatched agent hit a RED on a clean tree.

**Fix (the consumer, in `locations.py` — not in `snapshot-goals.py`, `level3.py`
or `grid.py`):** applied phase 0's rule to the env value in
`project_root_from_env`. It may now DESCEND into `.agi/`, never ASCEND:
```python
for var in PROJECT_ROOT_ENV_VARS:
    val = os.environ.get(var)
    if val:
        root = Path(val).resolve()
        return _graph_dir_in(root) or root
return find_project_root(start)
```
`_graph_dir_in` is the module's own phase-0 primitive (`<d>/.agi` holding a
config -> `<d>/.agi`), so the fix reuses the one rule instead of adding a tenth
local ancestor walk (goal:g11.1). It deliberately does NOT call
`find_project_root(Path(val))` — that walks UP and would silently override a
caller's explicit root (the never-ascend property the docstring promises).
Only `locations.py` and `test_locations.py` were edited. `dispatch.py`,
`find-root.sh`, `write.py`, `commands.py`, `verification.py` and all nodes were
left untouched.

**Reproduce (after fix):**
```
$ AGI_TREE_PROJECT_ROOT=.../seat-sanctuary-director \
    python3 extensions/agi/bin/snapshot-goals.py --render --check
render --check: 159 goal(s) round-trip byte-identical
EXIT=0
```

## Evidence

Three falsifier tests added to `test_locations.py` (all green with the fix):

- **(b)** `test_env_override_naming_repo_root_descends_into_dot_agi` — env names
a G11 repo root, resolves to `<repo>/.agi` (the dispatched-child sense).
- **(c)** `test_env_override_naming_graph_root_is_unchanged` — env names the
GRAPH root `<repo>/.agi`, resolves to ITSELF (the driver.h / session-hook
sense; must not regress).
- **(d)** `test_env_override_never_ascends_to_an_ancestor` — env names a
directory that is neither, whose ancestor holds a config: returned UNCHANGED,
never resolving to the ancestor. The never-ascend property asserted directly.

The two pre-existing `test_env_override_wins` and
`test_legacy_env_spelling_still_read` (both `make_legacy`, so they ride the
unchanged branch) were NOT edited and stayed green.

```
$ python3 -m pytest extensions/agi/tests/test_locations.py \
    extensions/agi/tests/test_grid.py extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_snapshot_goals.py -q
348 passed in 27.32s
```

```
$ python3 extensions/agi/bin/commands.py run verify
PASS  links               1.0s  [broken=0]
PASS  goals-check         2.1s  [byte-identical=1]
PASS  write-guard         2.7s
PASS  smoke              19.2s  [active=1736, deprecated=194, total=1930]
PASS  viewport-verify     1.0s
PASS  dispatch-help       0.1s
PASS  budget              0.1s
PASS  node-count          0.0s  [active=1736, deprecated=194, total=1930]
RESULT: PASS (all 8 checks green)
```

A full bare-directory suite run is refused by the `AGI_TIER=kid` guard
("refuses a bare full-suite directory run"), so the targeted four-file suite
falsifier (f) is the suite evidence; it is exactly the files the hypothesis
named.

## Agent Notes
Fixed locations.py consumer: env override descends into .agi/ via _graph_dir_in, never ascends. Reproduce exit1->exit0; three falsifier tests (b,c,d) added; 348 targeted tests green; verify PASS.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.58: accepted verdict proved. Independent verification in the shared worktree: reproduce command now exits 0 (159 goals byte-identical); test_locations.py alone 78 passed; fix is in locations.py only, implemented via the module own _graph_dir_in primitive (descend-into-.agi, never ascend), no tenth local ancestor walk added; dispatch.py, find-root.sh, write.py, commands.py untouched; falsifier tests (b),(c),(d) present as named and the two make_legacy tests untouched. No demotion: evidence_runs names this experiment itself, which is legitimate since it IS the run.
<!-- THOUGHT:END -->

Parent review: all acceptance criteria of hypothesis:l4-env-root-override-descends-never-ascends met; verdict proved upheld after independent re-run of reproduce + tests.
