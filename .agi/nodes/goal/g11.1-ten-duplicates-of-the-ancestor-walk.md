---
confidence: 1.0
goal_id: G11.1
goal_kind: long-term
heading_level: 3
id: "goal:g11.1"
mint_id: 34c17df8db994d3ea8c6f2a63fae8c62
order: 66
origin: goals-doc
parents:
  - goal:g11
seeds: []
status: active
tags:
  - goal
title: "G11.1: Ten Python files still declare their own ancestor walk"
type: goal
---

**The residual G11 left behind.** `bin/locations.py` exists as the single
Python resolver and `lib/find-root.sh` is checked against it, but existing
does not collapse anything by itself — ten Python files under `bin/` still
declare their own `CONFIG_NAMES` and walk up from cwd for
`agi-tree.config.json` independently, exactly as before `locations.py` was
written.

## The ten

- `benchmark.py`
- `cli.py`
- `dispatch.py`
- `metrics.py`
- `post_wire.py`
- `render-context.py`
- `snapshot-build-site.py`
- `snapshot-goals.py` — **half-migrated**, not a clean member of this list
- `spawn_gate.py`
- `zoom.py`

**`snapshot-goals.py` needs care, not addition.** It already imports
`locations` and calls `goals_path()` — the import this goal would otherwise
ask for is already there. What remains is deletion: its own leftover
`CONFIG_NAMES` constant and `config_path()` function, still declared
alongside the call to the shared resolver. Finishing it means removing code,
not adding an import.

## The target

Each of the ten imports `locations` and calls its resolver for the project
root instead of declaring `CONFIG_NAMES` and walking ancestors itself. No
behavior changes — `test_bash_and_python_agree` already treats agreement
between the bash and Python halves as the contract, and `locations.py` is the
implementation nine of these ten files should be calling and are not.

## Why this is a goal, not a chore

**G11's own migration is blocked on this closing first.** Steps 3 and 4 of
G11's sequencing move the graph inside the repo it builds — a layout change:
`graph_root`, `repo_root`, and `payload_ref` resolution all shift underneath
it. Today that layout is expressed once, correctly, in `locations.py` — and
separately, still, in ten other places that never call it. A layout change
made against ten independent copies is not one edit verified once; it is one
edit that has to be repeated ten times and can drift on any of them, which is
the exact failure `locations.py` was built to stop. **Until this lands, the
layout rule cannot be changed once — it has to be changed eleven times and
trusted to agree**, and G11's migration is precisely that kind of change.

## Falsifier

```
grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py
```

sums to **1** across `bin/` — only `locations.py` still declares it — and the
full test suite still passes. Both mechanical, neither requires judgment.

## Out of scope

**`engine_root`'s double derivation is adjacent, not included here.**
`level3.py :: DEFAULT_ENGINE_ROOT = BIN_DIR.parents[2]` and
`grid.py :: default_engine_root() = Path(__file__).resolve().parents[3]`
compute the same path with two different index arithmetics, off by one
because one counts from a directory and the other from a file.
`context/schemas/[config].md` already names it. It stays out of this goal
deliberately: it is a different failure shape — arithmetic divergence, not
copy-paste duplication — and folding it in would let this goal's mechanical
falsifier drift into something that needs judgment to check.
