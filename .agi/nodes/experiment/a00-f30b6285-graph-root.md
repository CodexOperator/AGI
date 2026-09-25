---
id: experiment:a00-f30b6285-graph-root
type: experiment
parents:
  - hypothesis:a00-f30b6285-0e37a6
edited_by: a00-f30b6285
title: "Experiment: a repo root reads the same box cells as its graph root"
---
# experiment:a00-f30b6285-graph-root

## What I ran

| step | command | result |
|---|---|---|
| baseline | `python3 -c "import boxes; print(boxes.box_cells('.'), boxes.box_cells('.agi'))"` | `{}` vs four cells — one tree, two answers |
| build | `boxes.py`: new `graph_root(root)` (returns `root` when it holds `config.json`, else `locations.find_project_root`, else `root`); `box_schema_path` and `_box` both read through it | 19 added / 2 removed in boxes.py, 2/1 in paths.py |
| build | `paths.classify` dedupes its class list | foreign-root line `['home','box','user','box']` → `['home','root','user','box']` |
| after | same probe, repo root and `.agi` | identical four cells; `require_box_cells('/tmp')` raises `BoxSchemaError` naming that path |
| tests | `python3 -m pytest extensions/agi/tests/test_paths_audit.py -q` | 19 passed (3 new) |
| tests | `python3 -m pytest extensions/agi/tests/test_unify.py extensions/agi/tests/test_locations.py -q` | 151 passed (boxes.py has a second reader at `unify.py:413`) |
| measure | `git diff --numstat -- extensions/agi/bin/boxes.py extensions/agi/bin/paths.py` | 21 production lines, ceiling 40 |

## What this proves

The claim in the parent hypothesis holds on the BUILT bytes: a repo root and
its graph root now read the same `box` cells, and a root with no graph behind
it refuses by name instead of returning `{}`.

## What it does NOT prove

The audit still has no production caller (`paths.findings` / `paths.py audit`
appear only in `test_paths_audit.py`). Fixing the cells is necessary but not
yet sufficient to matter; whether `paths.py audit` should gain a gate is a
policy decision this node deliberately did not invent.
