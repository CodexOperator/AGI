# CLAUDE.md — agi

Read [GOALS.md](GOALS.md) first. It is the source of truth for what this project
is committed to and **the only place new work is recorded**. This file covers
what the repo contains and how to run the loop.

## What agi is

`agi` is the code that operates on thoughtgraphs, and the thoughtgraph that
built it, in one repo. Before `goal:g11` these were two — `agi-tree` held the
nodes, `agi` held the code — and a whole pipeline existed for no reason but to
carry bytes across that boundary: `payloads/` as a staged checkout, `grid.py
checkout`, `stitch.py --publish`, `publish-engine.sh` with four gates in front
of it. The boundary was never load-bearing; it was inherited. **It is gone.**
One repo holds the source, the graph, and the grid refs that version both.

## Layout

```
agi/                        ONE repo — the engine, which absorbed the graph
  GOALS.md                  rendered here, at the root
  CLAUDE.md  AGENTS.md      at the root (AGENTS.md is a symlink to CLAUDE.md)
  extensions/ skills/ src/  the live source — edited directly
  .agi/
    config.json             was agi-tree.config.json
    nodes/                  the graph
    context/                schemas, kits, plans
  refs/grid/*               same repo, same namespace

fantasia/                   any other project
  GOALS.md   <game source>
  .agi/                     that project's graph        (committed)
  agi/                      engine clone                (gitignored, one line)
    GOALS.md .agi/          the engine's own graph, live in place
```

**`.agi` is a dot directory on purpose** — it files the graph with `.git`,
`.github` and `.claude`, rather than in the middle of the source tree.
**`GOALS.md` is the deliberate exception** and renders to the repo root, not
into `.agi/`, because the one document a human opens first must not be hidden
in a dot directory.

`bin/locations.py` is the single resolver every entry point calls: **nearest
enclosing `.agi/` wins**, no flag, no project name anywhere (`goal:g8.2`). Run
a command from `agi/` and it resolves this repo's own graph at `agi/.agi`; run
the same command from inside a project that has cloned `agi` in, and it
resolves whichever `.agi/` is nearer — the project's own from the project
root, the engine's from inside the clone. That is also why the old
`agi ↔ agi-tree` symlink pair is gone rather than replaced: `agi` doesn't need
a special case to describe itself, only the same layout every project gets,
minus the clone step it doesn't need to take against itself.

## What is allowed to exist here

| Path | Why it is here |
|---|---|
| `extensions/`, `skills/`, `src/` | The live source. Edited directly — there is no staged copy to check out. |
| `.agi/nodes/` | The graph. The persistent thoughts. Committed. |
| `GOALS.md` | **Derived** — `snapshot-goals.py --render` writes it from `.agi/nodes/goal/`, to the repo root. Read it first; author in the goal node. |
| *(retired 2026-09-03, L1.09)* `.agi/context/kits/`, `.agi/context/plans/build-site.md` | Were the generator inputs for the 159 `origin: build-site` nodes. Deleted in one atomic pass with the nodes deprecated (`.agi/nodes/deprecated/`); `snapshot-build-site.py` is now a permanent no-op here. Never recreate them. |
| `.agi/context/schemas/` | Node-type schemas. `schema_registry` reads `[name].md` as active. |
| `.agi/config.json` | Project marker + loop tuning. Its presence is what makes the enclosing repo a project. (The legacy name, `agi-tree.config.json` at the repo root instead of inside `.agi/`, still resolves.) |
| `refs/grid/*` | Per-node version history, in this repo's own ref namespace. See Git grid below. |
| `HANDOFF.md` | The director's **live scratchpad** — one session, replaced wholesale each time. Written *during* the work, not after. See below. |
| `QUICKSTART.md` | Standing bootstrap: clone, deps, install, the safety rail, one iteration. Split out of `HANDOFF.md` on 2026-09-02 so a director replacing the handoff cannot destroy the install guide. |
| `CLAUDE.md`, `AGENTS.md` | This file, read by every agent. `AGENTS.md` is a symlink to it — one document, two names agents look for it under. |

**The table above is the graph's footprint, not the whole repo** — `agi` also
carries whatever the engine itself needs outside `.agi/` (docs, tests,
packaging). What the table guards against is graph content leaking to the
wrong place: a second `nodes/` outside `.agi/`, a hand-maintained `GOALS.md`,
or scratch scripts that belong in neither half. This repo has cleaned house
on the graph side before — ~95 one-off experiment scripts, a vendored copy of
the engine, the cavekit-era runner and 768 session transcripts were removed on
2026-08-23; git history is the archive, not a to-do list to keep re-adding to.

## Running the loop

`bin/locations.py` / `lib/find-root.sh` resolve the project root by walking up
for a `.agi/` holding a config (nearest enclosing wins); a bare
`agi-tree.config.json` still resolves for a project that has not moved to this
layout. Run from anywhere inside this repo:

```bash
bash extensions/agi/driver.sh --smoke --max-iters 1
```

`--smoke` is a dry pass: snapshot + render + metrics, no agent dispatch. Drop it
(and pass `--max-iters N`) for a live run, which dispatches paid model agents —
models are set in `.agi/config.json` under `agent_dispatch` and `cc_dispatch`.

Everything is reachable globally, by symlink, with no second copy anywhere:

| Handle | Symlink |
|---|---|
| `agi` skill (any session, any dir) | `~/.claude/skills/agi` → `/home/ubuntu/work/agi/skills/agi` |
| `agi` command (on `PATH`) | `~/.local/bin/agi` → `/home/ubuntu/work/agi/extensions/agi/driver.sh` |
| SessionStart map injection | `~/.claude/settings.json` → `/home/ubuntu/work/agi/extensions/agi/hooks/cc-session-start.sh` |

One skill, one source. The hook is a silent no-op outside a project, which is
what makes registering it globally safe.

## `HANDOFF.md` is a scratchpad, not a report — and the director replaces it

**Write it as you work, not when you finish.** It is the one file a cold
session can open and resume from, so it has to be current at every moment —
including the moment a session dies without a summary. A handoff written at the
end is a handoff that does not exist for every run that ends badly, which is
exactly when it is needed.

### The director REPLACES the session content. It does not append to it.

**Default, no permission needed, no asking:** on your first substantive action
as director, **delete the previous session section and write your own in its
place.** Do not read it first, do not extend it, do not preserve it "just in
case". One session's handoff at a time.

**The only exception: when the user asks you to check the handoff.** Then read
what is there before touching it — they are asking about the previous session,
not the current one.

**Erasing is safe here, and that is a measured property of this file rather
than a general licence.** `HANDOFF.md` is `build:HANDOFF.md` with
`payload_ref: HANDOFF.md`, so `grid.py commit --all` versions the payload
alongside the node. Every prior handoff is one command away:

```bash
python3 extensions/agi/bin/grid.py versions build:HANDOFF.md
python3 extensions/agi/bin/grid.py payload  build:HANDOFF.md --version N
```

At the time this rule was written there were **55 versions**, and v40
materialised in full. Plus ordinary git history. **Nothing is lost by
replacing, so accumulating costs context and buys nothing.**

**Accumulating was the previous rule and it was wrong.** It said old sections
are archive and stay; the file reached **1,723 lines with six session
sections**, of which five were superseded — and it is read by every session
that resumes cold. Trimmed to the bootstrap plus one live section on
2026-09-02. This is the same principle the repo already applies to its own
history: *git history is the archive, not a to-do list to keep re-adding to.*

**Standing instructions do not belong in this file at all.** The bootstrap —
the `bin/*.py` safety rail, cloning and installing on a new machine, the
one-iteration diagram, the glossary — moved to **`QUICKSTART.md`** on
2026-09-02. Keeping it here was a live hazard once replacement became the
default: the first director to follow the rule correctly would have deleted the
install guide along with the previous session's state. **Anything that is true
across sessions goes in `QUICKSTART.md`, `CLAUDE.md` or a goal node — never
here.**

### What a live section owes a cold reader

In this order: **§0 the state block** (counts, runtime, models, whether
anything is unpushed), **§1 the plan with each item marked done/next/blocked**,
**§2 what landed in one line each**, **§3 🔴 where it stopped and the exact
next command**, **§4 traps hit this session**, **§5 the known-good verification
sequence.** Mark the next action so plainly that a fresh session does not have
to infer it.

```
# SESSION HANDOFF — 2026-09-02: LIVE SCRATCHPAD (session in progress)
```

**Keep it thin. `GOALS.md` is the tracker, not this.** Active goals are how
projects are tracked; `HANDOFF.md` is only the session-to-session bridge — the
things a graph cannot say, like "the run is half done and the next command is
this". Anything that is a commitment belongs in a goal node. Work recorded only
here is work the graph does not know about.

## Delegated authority — when the owner steps away mid-run

The owner hands the director authority for the rest of an iteration budget and
leaves. **Codified here on 2026-09-02 because it had been re-negotiated at the
start of every such run**, which is motion spent on operations rather than
work — the thing this project's whole design is against.

**The standing terms, once authority is handed over:**

1. **Keep working to the end of the declared iteration budget.** Authority is
   over the budget, not over "until something is unclear". A run that stops on
   the first ambiguity has returned the authority it was given.
2. **Bank, do not block.** A decision that genuinely needs the owner goes in
   `HANDOFF.md` **§6 BANKED** with the options and a recommendation, and the
   run continues on everything that does not depend on it. Blocking is for a
   step that would be unsafe or useless under *every* assumption — which is
   rare, and is not the same as "I would rather be told".
3. **Decide and document, in the graph.** A judgement call is made, recorded
   in the node's `THOUGHT` block as a deviation with its reason, and left for
   verdict writers to weigh. An undocumented judgement call is the one thing
   this arrangement cannot absorb.
4. **`HANDOFF.md` stays live throughout.** Written *during* the work. The
   owner returns to it cold and it is the only thing that has to be current.
5. **Push after every iteration** while crons are off, so an interrupted run
   leaves nothing stranded on the box.
6. **Two things authority never covers**, regardless: an irreversible or
   destructive operation outside the loop's own commits (force-pushing a
   shared branch, `git rm` on nodes, rewriting published history), and
   spending on a provider or scale the owner did not name. Bank those.

**Scope creep is the failure mode to watch, not idleness.** The budget is the
limit and the active goals are the field; a run that invents new goals to fill
its remaining iterations has spent the owner's tokens on the director's ideas.

## Editing the engine — one commit

**Before `goal:g11`:** an engine change was `grid.py checkout --all`, edit
under `payloads/`, run the tests against that staged copy, `grid.py commit
--all`, commit the graph, then `publish-engine.sh` and its four gates. That
whole pipeline computed nothing — it existed only because the bytes lived in
one repo and had to arrive in another.

**Now:** you edit the file. You run its tests. You commit.

```bash
<edit the file, in place, wherever it already lives in the tree>
<run its tests>
git commit
python3 extensions/agi/bin/grid.py commit --all
```

One commit carries the thought and the code it produced — what `goal:g6.5`
step 3 wanted and never got.

**Retired, because each existed only to move bytes across a boundary that no
longer exists:**

- **`payloads/`** — the staged checkout. Gone; the payload *is* the source file.
- **`grid.py checkout`** — nothing to check out. **Never run it.** Even before
  `goal:g11` it was a whole-tree command scoped by no statement of file
  ownership, and it silently reverted another agent's uncommitted work twice
  in one session (`goal:g4.1`). Under this layout the hazard is gone by
  construction — there is no second copy for a checkout to overwrite, only the
  one file you and git already know about.
- **`stitch.py --publish`** — nothing to publish *into*; the engine tree and
  the source tree are the same tree.
- **`publish-engine.sh`** — its four gates existed to make a cross-repo write
  recoverable. A commit in one repo is already recoverable with `git revert`;
  the gates have nothing left to guard.

**`grid.py commit --all` stays.** It is not the publish pipeline — it is the
grid, and the grid is not what `goal:g11` removes. It versions `node.md` and
its payload *together* as one atomic version, which plain git does not do:
git versions the whole repo per commit, and the grid versions one node's
history independently of whatever else that commit touched. `refs/grid/*`
remains exactly what it was, `grid.py log|diff|versions|payload` all still
work unchanged, and the 5-minute cron still runs `commit --all`. Worth saying
plainly, because "one repo" invites the wrong inference — the grid was never
the thing with the boundary problem.

**One real use survives beyond the grid itself:** `stitch.py --from-grid
--grid-version N --out DIR` still materializes a chosen historical version of
the whole tree into a fresh directory. That writes *out*, not back into this
repo — a genuinely different operation from `--publish`, and it is not retired.

**A new file is created the same way — write it directly under `extensions/`,
`skills/` or `src/`.** `level3.py` discovers it via `git ls-files` on this same
repo, mints its node and its `payload_ref`, and from then on it is ordinary
graph content, from the first commit — no gitignored staging window where a
file can exist with no node behind it.

**Contract derivation is no longer stale by construction.** `level3.py` and
`stitch.py --verify` read the source tree directly, and the source tree is
now the thing you just edited — no publish step sits between an edit and a
fresh contract, and no residual window where the two can disagree. That
closes `goal:g6.1`'s open loop; it isn't narrowed, it no longer applies.

## The two rules this project has already paid for

- **NEVER create `.agi/bin/snapshot-build-site.py` or
  `.agi/bin/render-context.py`.** `driver.sh` resolves the project root
  (`.agi/` under this layout) and prefers a script at `<project-root>/bin/*.py`
  over the engine's own, so a stray copy under `.agi/bin/` silently shadows the
  safe version. A stale one has already wiped `nodes/` once (H0/H0b — confirmed
  29k-node data loss). Don't recreate a `bin/` directory there (S1).
- **`snapshot-build-site.py` deletes every `origin: build-site` node it does
  not re-derive on that run, and resurrects any deprecated one whose kit
  entry still exists.** That is why the build-site cohort was retired in ONE
  atomic pass on 2026-09-03 (L1.09): all 159 nodes deprecated, then the kits
  and plan deleted in the same commit. With no `build-site.md` the script
  short-circuits permanently. Do not recreate the inputs (H0i).

## Git grid

Per-node version history is baked into this repo as `refs/grid/*` — never
checked out, not in `git branch`. After each iteration commit:

```bash
python3 extensions/agi/bin/grid.py commit --all
```

Inspect with `grid.py log|diff|status`. Cadence and enablement are graph
content, not memory: `.agi/nodes/.geometry/crons.md` declares `crons_live`
plus per-job schedules, and `bin/crons.py apply` is the one command that makes
the real crontab agree with it — editing the node and letting it get committed
*is* the change, since `grid_sync` re-applies the declaration every 5 minutes.
`crons_live: false` is a one-edit kill switch for all managed lines at once
(used to freeze the four crons during the `goal:g11` migration itself); turning
it back on takes one manual `crons.py apply`, since the job that would have
re-applied it is itself one of the lines removed. Of the four jobs the node can
declare, two are now vestigial under one repo — `publish_engine` has nothing
left to run, and `engine_push` duplicates `branch_push` against the same
remote — and are expected to stay disabled rather than deleted from the
schema.

**Verify which branch is checked out before trusting any push** — work once
accumulated on a stale `iter24-extend-300hop` branch while a cron pushed
`master` and published nothing. `crons.py` re-resolves the checked-out branch
at every `apply`, never caching it, for exactly this reason.

## Conventions

- Goal ids are never renumbered. A gap beats a renumber; nodes reference goals
  by id.
- Retire a goal by marking it `retired` and **deprecating — never deleting**
  its seed node. Retired chains stay as prior art.
- **Retire a node with `status: deprecated` and move it to
  `.agi/nodes/deprecated/<type>/`** — same per-type split, one level down.
  Never `git rm` it. The reason is mechanical, not sentimental: a node's grid
  ref outlives its file, so deleting the file does not shrink the durable
  structure, it *decouples* it — leaving a ref and any `supersedes:` edges with
  nothing live behind them for G10's hypergraph to reconcile. Moving changes
  the node's **address** (derived, expected to change) and never its **mint
  id**, so every ref and provenance link keeps resolving. `node_count`
  deliberately does not drop; watch `active_node_count` / `deprecated_node_count`
  instead. **Readers that glob one type directory must read the retired
  sibling too, live-first** — `stitch.py`, `level3.py`, `node_writer.py` and
  `zoom.py` do. A reader that stops seeing a retired node fails quietly and in
  its own way (orphaned engine file, re-minted duplicate, unresolvable edge,
  missing title).
- **`GOALS.md` is derived, not the goal nodes.** `driver.sh` runs
  `snapshot-goals.py --render` and nothing else, which writes `GOALS.md` (repo
  root) from `.agi/nodes/goal/*.md`. **Edit the goal node.** A hand-edit to
  `GOALS.md` survives until the next `--smoke` and then vanishes with no
  warning — confirmed by losing one. Check the two directions are still
  inverses with `snapshot-goals.py --render --check`, which exits 0 only on a
  byte-identical round trip.
- **A version is a grid commit, not a second node file.** A fix or update edits
  the target node **in place**; no `@v2` file, no `supersedes:` pair. Run
  `grid.py commit --all` afterward and the grid carries the history (G6.3).
- **Record why, in the node's `THOUGHT` block (G2.11).** A node body may carry
  one authored region, and it now survives the regenerating scans that used to
  destroy it:

  ```
  <!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
  why this version differs from the last one
  <!-- THOUGHT:END -->
  ```

  **`body` is state; `thought` is delta.** The body says what the node asserts
  now; the thought says why *this version* differs from the previous one, and
  is rewritten from scratch each time rather than appended to. The grid
  snapshots `node.md` once per version, so the thought is versioned for free
  and `grid.py diff` reads as a changelog of reasoning. **Absent means empty** —
  never fabricate one after the fact, because a made-up thought reads as
  evidence. Readers strip it (`snapshot-goals.py --render`), so it never
  reaches `GOALS.md` or injected context: it is provenance to zoom into, not
  weight every session carries.
- **This is the one exception to "edit the payload, never the node body".** For
  a build node the `BUILD-CONTRACT` block and surrounding prose are still
  regenerated on every scan and still must not be hand-edited — that hasn't
  changed just because the payload now lives directly in the tracked source
  tree instead of a staged copy. The `THOUGHT` region is the authored half and
  is durable.
- **A build node has exactly two legal origins (`goal:s29`).** Either
  `parents: [mvp:<id>]` — a new file, specified by an mvp that states what it
  must satisfy — or `parents: [build:<id>, goal:<id>]` — a **new version** of a
  file that already exists, with the goal that motivated it. **A goal alone
  never mints a build node**; an existing build node has already proved its
  worth by existing, so a goal may extend it and only it. Enforced by
  `spawn.parent_shapes` in `.agi/context/schemas/[build].md`, which is an OR
  across whole shapes (`allowed_parents` is a flat set and would also permit
  the lone goal this forbids). **The 216 pre-existing build nodes are
  grandfathered** — the gate is creation-time only and `level3.py` does not
  route through it.
- **Two identifiers, two jobs.** A node's **mint id** is assigned once and never
  changes — it is what grid refs and provenance key on. Its **address** is
  derived from tags and is expected to change on every retag or regroup — it is
  what humans, renderers and lookups use. Never conflate the two (G2.5).
- **Verify the node count never drops.** A snapshot, a retag, or a migration
  should only ever grow or hold `active_node_count` + `deprecated_node_count`
  steady, never quietly shrink it. `goal:g11`'s own migration was rehearsed
  four times to check exactly this before the real cut ran: 807 nodes in, 807
  out, zero bytes changed, every time.
