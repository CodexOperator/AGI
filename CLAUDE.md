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
| `GOALS.md` | **Derived** — `snapshot-goals.py --render` writes it from `nodes/goal/`. Read it first; author in the goal node. |
| `context/kits/`, `context/plans/build-site.md` | Generator inputs for the 159 `origin: build-site` nodes. See the warning below. |
| `context/schemas/` | Node-type schemas. `schema_registry` reads `[name].md` as active. |
| `agi-tree.config.json` | Project marker + loop tuning. Its presence is what makes this dir a project. |
| `agi/` | Symlink to `/home/ubuntu/work/agi`, the engine repo. Gitignored — never commit it here. |
| `payloads/` | Staged checkout of build-node payloads (`grid.py checkout`). Gitignored — the committed home of these bytes is each node's grid ref. This is where you edit engine code. |

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

Everything is reachable globally, by symlink, with no second copy anywhere:

| Handle | Symlink |
|---|---|
| `agi` skill (any session, any dir) | `~/.claude/skills/agi` → `/home/ubuntu/work/agi/skills/agi` |
| `agi` command (on `PATH`) | `~/.local/bin/agi` → `/home/ubuntu/work/agi/extensions/agi/driver.sh` |
| SessionStart map injection | `~/.claude/settings.json` → `/home/ubuntu/work/agi/extensions/agi/hooks/cc-session-start.sh` |

One skill, one source. The hook is a silent no-op outside a project, which is
what makes registering it globally safe.

## Layout: the tree is outside the engine

**General shape, every project: `<project>/<project>-tree/agi`.** The graph is a
separate repo one level inside the project, and the engine clone lives
*underneath it*. Dropped into `fantasia`, that is:

```
fantasia/
  fantasia-tree/        the graph repo (GOALS.md, config, nodes/)
    agi/                gitignored clone of the engine
```

The tree is outside the engine, never inside it, so an engine checkout never
contains a graph. That makes the gitignore story one line in one repo — `agi/`
in the tree — and nothing at all in the engine.

**This pair is the exception, and only in that both hops are symlinks:**

- `agi/agi-tree` → `/home/ubuntu/work/agi-tree` (this repo)
- `agi-tree/agi` → `/home/ubuntu/work/agi` (the engine repo)

So `agi/agi-tree/agi` resolves back to the engine — same
`<project>/<project>-tree/agi` shape, with `agi` as the outermost layer because
`agi-tree` is literally the graph that builds it. Symlinks rather than a clone
because an engine edit made from inside the tree has to land in the real
checkout, not a copy nobody ships. The engine's `.gitignore` carries exactly one
literal `agi-tree` line for the outer symlink — not a `*-tree` glob, since
nothing else should be ignorable there, and no trailing slash, since that would
not match a symlink.

This is an organizational convenience for one local pair, **never a mode the
engine knows about** — G8.2's invariant is that no `if project == "agi-tree"`
branch exists anywhere, and the symlinks add none.

## Engine edits — do not open a file in `agi/`

**As of 2026-08-25 an engine change originates here and is published to `agi`.**
G6.3 is complete: every build node's payload lives in its own grid ref, so the
graph holds the bytes and the engine tree is what falls out. The four steps:

```bash
python3 agi/extensions/agi/bin/grid.py checkout --all
```

Edit under `payloads/<payload_ref>` — e.g. `payloads/extensions/agi/bin/grid.py`.
Run the tests against that copy (`python3 -m pytest payloads/extensions/agi/tests/`),
then record and publish:

```bash
python3 agi/extensions/agi/bin/grid.py commit --all
```

Then **commit the graph**, and publish with the one command that owns the whole
sequence:

```bash
bash agi/extensions/agi/bin/publish-engine.sh
```

It re-derives contracts from the grid, `grid commit`s them, runs
`stitch --verify --from-grid --strict`, publishes, **and commits the engine
citing the graph commit it derives from**. It is also the hourly `:37` cron, so
in the normal case you do not run it at all. `--dry-run` reports every gate
without writing.

**Do not call `stitch.py --publish` by hand.** It is the layer underneath and
it stops one step short: it writes the bytes into the engine tree and never
commits them, which leaves the engine dirty — and a dirty engine is exactly
what `--publish` refuses on next time. That was walked into on 2026-08-27; the
recovery is `git -C <engine> checkout .` (the bytes are in the grid) followed
by `publish-engine.sh`.

**Its first gate is the one that will stop you: the graph must have no
uncommitted changes under `nodes/` or `GOALS.md`.** A published engine must
cite a graph commit that exists. This bites in a non-obvious way — a *single*
node whose stored contract differs from what `level3.py` re-derives leaves the
graph permanently dirty after every scan, and the cron then refuses silently,
every hour, forever. One character of YAML quoting in
`tests-schema-registry-test-brackets.md` did exactly that. If the cron seems
not to be publishing, run `level3.py` and check `git status` first.

**A new file is created the same way — write it under `payloads/`.** `level3.py`
discovers it there, mints its node and its `payload_ref`, and from then on it is
ordinary graph content. Before 2026-08-25 discovery only read `git ls-files` on
the engine, so a script authored in `payloads/` had no node, was never committed
to the grid, and lived in exactly one gitignored directory — two were found in
that state within an hour of the workflow existing.

**`checkout` will not overwrite a payload you have edited but not committed.**
It reports `SKIP (locally modified)` and leaves it; `--force` discards. Two
agents sharing this worktree is the normal case (G4.1), and `checkout --all` is
`git checkout .` on the payload tree.

Read a payload back without checking out: `grid.py payload <node-id> [--version N]`.
Materialise a chosen historical version of the whole tree:
`stitch.py --from-grid --grid-version N --out DIR`.

**The one legitimate exception is a change that the pipeline itself cannot
carry** — the bootstrap that built this pipeline was made directly in `agi` and
recorded as a deviation in G6.1. If you think you have another one, say so in
the node rather than quietly editing the engine.

**Still engine-first:** contract derivation. `level3.py` and `stitch.py --verify`
read the engine tree, so a payload edited only here has a stale contract until
you publish and rescan. That residual is G6.1's.

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
- **`GOALS.md` is derived, not the goal nodes.** The arrow reversed on
  2026-08-25 (G6.9, commit `2b204a5d4`) and this line said the opposite until
  2026-08-26. `driver.sh` runs `snapshot-goals.py --render` and nothing else,
  which writes `GOALS.md` from `nodes/goal/*.md`. **Edit the goal node.** A
  hand-edit to `GOALS.md` survives until the next `--smoke` and then vanishes
  with no warning — confirmed by losing one. Check the two directions are still
  inverses with `snapshot-goals.py --render --check`, which exits 0 only on a
  byte-identical round trip.
- **A version is a grid commit, not a second node file.** A fix or update edits
  the target node **in place**; no `@v2` file, no `supersedes:` pair. Run
  `grid.py commit --all` afterward and the grid carries the history (G6.3).
- **Two identifiers, two jobs.** A node's **mint id** is assigned once and never
  changes — it is what grid refs and provenance key on. Its **address** is
  derived from tags and is expected to change on every retag or regroup — it is
  what humans, renderers and lookups use. Never conflate the two (G2.5).
