---
id: goal:g11.1
mint_id: 34c17df8db994d3ea8c6f2a63fae8c62
type: goal
parents:
  - goal:g11
confidence: 1.0
edited_by: season.py
goal_id: G11.1
goal_kind: long-term
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
thought_session: season
title: "G11.1: Nine Python files still declare their own ancestor walk, and it has cost three outages"
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked complete in the 2026-09-01 sweep, on its own falsifier rather than on
judgement: `grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py` names exactly one
file. The goal asked for ten duplicates of the ancestor walk to become one
resolver, and iter-5 (2026-08-30) did it.

Worth keeping from that work: the goal said ten *duplicates*; the measurement
said ten *breakages*. No legacy config file existed anywhere in the repo, so
every copy of the walk was already dead code resolving nothing — seven failed
hard, two answered `os.getcwd()` with no walk at all.
<!-- THOUGHT:END -->

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


## What it cost, measured 2026-08-29 — the hour goal:g11 landed

Three of the copies broke immediately, in production, each in a different way.
This section exists because a count of duplicates is an abstraction and these
are not.

| file | failure | how it presented |
|---|---|---|
| `snapshot-goals.py` | `os.getcwd()` is the repo root, not the graph root | **refused** to write an empty `GOALS.md` — loud, safe |
| `grid.py` | own ancestor walk, no phase 0, could not see `.agi/` | exited; `commit --all` would have stopped recording history, on stderr, in a cron |
| `level3.py` | same `os.getcwd()` fallback | wrote build nodes to `<repo>/nodes/build` instead of `<repo>/.agi/nodes/build` — **a stray node tree that then became input to the next scan** |

**The third is the shape that matters.** Combined with a separate boundary bug
it produced a generator whose output was inside its own input set: 190 files
scanned became 4131, minting nodes named
`nodes-build-nodes-build-nodes-build-....md.md.md`. Nothing crashed. 3,098
generated files were committed before anyone noticed.

**Only the first failed safely, and by luck of a different goal.**
`goal:s12`'s "never write an empty GOALS.md" guard is the sole reason that one
was a bug report rather than a data-loss incident. The other two had no such
guard, and the difference was not by design.

### Current count: nine residuals

`grid.py` and `snapshot-goals.py` now delegate to `locations`. `level3.py`
delegates for `PROJECT_ROOT` but still declares its own `CONFIG_NAMES`, so it
is a half-case of the same kind `snapshot-goals.py` was. Still carrying their
own walk: `cli.py`, `benchmark.py`, `dispatch.py`, `snapshot-build-site.py`,
`post_wire.py`, `spawn_gate.py`, `zoom.py`, `metrics.py`, `render-context.py`.

**`snapshot-build-site.py` is the one to fix first, and not because it is
worst — because of what it does when wrong.** It deletes every
`origin: build-site` node it does not re-derive on that run. A resolver that
points it at the wrong directory is the H0i pruning hazard with the safety
catch removed. It has not fired only because nothing has run it from a cwd
where the old rule resolves differently.