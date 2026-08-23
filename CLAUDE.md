# CLAUDE.md — agi-tree

Read [GOALS.md](GOALS.md) first. It is the source of truth for what this project
is committed to and **the only place new work is recorded**. This file covers
what the repo contains and how to run the loop.

## What agi-tree is

`agi-tree` is the thoughtgraph that builds `agi`; `agi` is the code that operates
on thoughtgraphs. This repo holds **the nodes and the inputs the graph is
derived from — nothing else.** Code lives in the engine repo.

## What is allowed to exist here

| Path | Why it is here |
|---|---|
| `nodes/` | The graph. The persistent thoughts. Committed. |
| `GOALS.md` | Human-authored goal contract. `snapshot-goals.py` derives `nodes/goal/` from it. |
| `context/kits/`, `context/plans/build-site.md` | Generator inputs for the 159 `origin: build-site` nodes. See the warning below. |
| `context/schemas/` | Node-type schemas. `schema_registry` reads `[name].md` as active. |
| `agi-tree.config.json` | Project marker + loop tuning. Its presence is what makes this dir a project. |
| `agi/` | Drop-in clone of the engine. Gitignored — never commit it here. |

**Anything not in that table does not belong in this repo.** ~95 one-off
experiment scripts, a vendored copy of the engine (`src/`, `tests/`), the
cavekit-era runner and 768 session transcripts were removed on 2026-08-23; git
history is the archive. If you find yourself adding a `.py` file here, it
belongs in the engine.

## Running the loop

The engine auto-detects the project root by walking up for `agi-tree.config.json`,
so run from anywhere inside this repo:

```bash
bash agi/extensions/agi/driver.sh --smoke --max-iters 1
```

`--smoke` is a dry pass: snapshot + render + metrics, no agent dispatch. Drop it
(and pass `--max-iters N`) for a live run, which dispatches paid model agents —
models are set in `agi-tree.config.json` under `agent_dispatch` and `cc_dispatch`.

The `agi` skill is already installed globally: `~/.claude/skills/agi` symlinks to
`/home/ubuntu/work/agi/skills/agi`. There is deliberately no second copy here —
one skill, one source.

## Engine edits

`agi/` here is a read-only clone for running the loop. Engine changes are made
in `/home/ubuntu/work/agi` and pulled down (`git -C agi pull`). Do not edit
`agi-tree/agi/` — a fix made there is invisible to the engine repo and will be
overwritten. G6.3/G6.5 replace this arrangement with stitch-from-graph; until
then the engine repo is the write path.

## The two rules this project has already paid for

- **NEVER create `bin/snapshot-build-site.py` or `bin/render-context.py` here.**
  A project-local copy shadows the engine's safe version, and a stale copy
  silently wipes `nodes/` (H0/H0b — confirmed 29k-node data loss). `bin/` was
  deleted for this reason; do not recreate it (S1).
- **`snapshot-build-site.py` deletes every `origin: build-site` node it does not
  re-derive on that run.** So deleting or emptying `context/kits/` or
  `context/plans/build-site.md` silently prunes 159 nodes on the next loop run.
  Retire them by deprecating the nodes first, never by deleting the input (H0i).

## Git grid

Per-node version history is baked into this repo as `refs/grid/*` — never checked
out, not in `git branch`. After each iteration commit:

```bash
python3 agi/extensions/agi/bin/grid.py commit --all
```

Inspect with `grid.py log|diff|status`. Two crons (S2): a 5-minute auto-snapshot
plus grid push, and an hourly push of `master`. **Verify which branch is checked
out before trusting any push** — work once accumulated on a stale
`iter24-extend-300hop` branch while a cron pushed `master` and published nothing.

## Conventions

- Goal ids are never renumbered. A gap beats a renumber; nodes reference goals
  by id.
- Retire a goal by marking it `phasing-out` and **deprecating — never deleting**
  its seed node. Retired chains stay as prior art.
- `nodes/goal/` is derived. Never hand-edit it; edit `GOALS.md`.
