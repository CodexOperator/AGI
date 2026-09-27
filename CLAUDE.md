# CLAUDE.md — agi

**Goals are the source of truth and the only place new work is recorded** — the goal nodes under
`.agi/nodes/goal/`, rendered to `GOALS.md` (derived, ~1.5 MB). Read YOUR goal by id
(`python3 extensions/agi/bin/write.py goal:<id> 'read body 1:60'`), never the whole render.
**Flows have skills** — `skills/agi-<flow>/SKILL.md` (goal · node-write · send · rotate · dispatch ·
workflow · merge-pass · verify; Claude posts: the Skill tool). Read the matching one BEFORE the flow.
Long form of this file, before the 2026-09-27 trim (goal:g4.18.2): `grid.py payload build:CLAUDE.md --version N` or git history.

## What agi is
The code that operates on thoughtgraphs, and the thoughtgraph that built it, in ONE repo: source, graph, and the
grid refs that version both. (Before the one-repo move, `agi-tree` held the nodes; `payloads/`, `grid.py checkout`,
`stitch.py --publish` and `publish-engine.sh` only carried bytes across that boundary. All retired — never run them.)

## Layout
```
agi/                        ONE repo — the engine, which absorbed the graph
  GOALS.md                  rendered at the root (the one doc a human opens first is never hidden in a dot dir)
  CLAUDE.md  AGENTS.md      at the root (AGENTS.md is a symlink to CLAUDE.md)
  extensions/ skills/ src/  the live source — edited directly
  .claude/skills/ .claude/workflows/   committed symlinks into skills/ and extensions/agi/workflows/
  .agi/
    config.json             project marker + loop tuning (legacy agi-tree.config.json at the root still resolves)
    nodes/                  the graph (deprecated/<type>/ = retired, moved, never deleted)
    context/schemas/        node-type schemas, [<type>].md
  refs/grid/*               per-node version history, same repo
fantasia/                   any other project: its own .agi/ + GOALS.md; agi/ cloned in (gitignored)
```
`bin/locations.py` is the single resolver: **nearest enclosing `.agi/` wins** — no flag, no project name.

## What is allowed to exist here (the graph's footprint)
| Path | Why |
|---|---|
| `extensions/`, `skills/`, `src/` | the live source, edited directly |
| `.agi/nodes/` | the graph, committed |
| `GOALS.md` | DERIVED by `snapshot-goals.py --render` — author in the goal node |
| `.agi/context/schemas/` | node-type schemas; `schema_registry` reads `[name].md` |
| `.agi/config.json` | project marker + loop tuning |
| `refs/grid/*` | per-node version history |
| `COMPLETE.md` | post-loop report (`goal:g1.13`), **replaced whole at each loop close** (owner 2026-09-05, reaffirmed 09-11: "Complete should be a whole replacement as it's already versioned anyway"); appended only when the owner asks. Shape in `skills/agi/SKILL.md` |
| `HANDOFF.md` | symlink to the Prime's card (`doc:card-belam`); every post's card = `.agi/sessions/quorum/<post>.md` → its doc node |
| `QUICKSTART.md` | standing bootstrap: clone, deps, install, safety rail, one iteration |
| `CLAUDE.md`, `AGENTS.md` | this file, one document under two names |

Retired 2026-09-03 (L1.09): `.agi/context/kits/`, `.agi/context/plans/build-site.md` — never recreate them.
Git history is the archive, not a to-do list: no second `nodes/`, no hand-kept `GOALS.md`, no scratch scripts.

## Running the loop
```bash
bash extensions/agi/driver.sh --smoke --max-iters 1     # snapshot + render + metrics, no dispatch
bash extensions/agi/driver.sh --max-iters N              # live: dispatches PAID agents (models: .agi/config.json)
```
Global handles (symlinks, no second copy): the `agi` skill, the `agi` command → `extensions/agi/driver.sh`, the
SessionStart hook → `extensions/agi/hooks/cc-session-start.sh` (a silent no-op outside a project).

## Cards and the handoff
A post's card is its ONE scratch: written DURING the work (a session that dies without a summary must still be
resumable), **replaced whole**, never appended — every prior version is in git and the grid. Order: §0 state · §1 plan
(done/next/blocked) · §2 landed, one line each · 🔴 where it stops + the exact next command · §4 traps · §5 verification ·
§6 BANKED. ≤ 100 lines. **A card lists its post's skills; it never copies their rules**, and never tracks goals
(goals are trackers). Standing truths go in `QUICKSTART.md`, this file, a role template or a node — never a card.
Standing, owner 2026-09-09: trim + diagram-max, for every role, all the time; owner verbatim lives in NODES.

## Delegated authority — when the owner steps away mid-run
1. Keep working to the end of the declared budget; authority is over the budget, not "until something is unclear".
2. **Bank, do not block**: a decision that needs the owner goes in the card's §6 BANKED with options + a
   recommendation; the run continues on everything else. Block only what is unsafe or useless under EVERY assumption.
3. **Decide and document, in the graph**: the deviation and its reason in the node's `THOUGHT` block.
4. The card stays live throughout.   5. Push after every iteration while crons are off.
6. Never, regardless: an irreversible/destructive operation outside the loop's own commits (force-push of a shared
   branch, `git rm` on nodes, rewriting published history), or spend on a provider/scale the owner did not name. Bank those.

**Scope creep is the failure mode, not idleness** — never invent goals to fill a budget.

## Editing the engine — one commit
Edit the file in place · run its tests · `git commit` · `python3 extensions/agi/bin/grid.py commit --all`.
A new file is written directly under `extensions/`, `skills/` or `src/`; `level3.py` (via `git ls-files`) or
`write.py create build … --payload` gives it a node. **Never `grid.py checkout`** — it silently reverted another
agent's uncommitted work twice (`goal:g4.1`). `stitch.py --from-grid --grid-version N --out DIR` (writes OUT) survives.

## The two rules this project has already paid for
- **NEVER create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`**: `driver.sh` prefers
  `<project-root>/bin/*.py` over the engine's, and a stale shadow copy once wiped `nodes/` (H0/H0b, 29k nodes). No `bin/` there.
- **`snapshot-build-site.py` deletes every `origin: build-site` node it does not re-derive, and resurrects deprecated
  ones whose kit entry exists.** Here it is a permanent no-op (no `build-site.md`: its L18 guard returns). In any OTHER
  project with a live `context/kits/` + `context/plans/build-site.md`, emptying either prunes every build-site node.

## Git grid
`refs/grid/*` — never checked out, not in `git branch`; inspect with `grid.py log|diff|versions|payload|status`.
It versions `node.md` + its payload as ONE version, independent of the rest of the commit. Cadence is graph content:
`.agi/nodes/.geometry/crons.md` (`crons_live` + per-job schedules); `crons.py apply` makes the crontab agree
(re-run every 5 min by grid_sync, chained with `;` not `&&`, so a failed push never stops the heal).
`branch_push` pushes the checked-out branch hourly at :07 — a second automatic writer: never merge-then-hold.
`crons_live: false` = one-edit kill switch (turning it back on takes one manual `crons.py apply`).
**Verify which branch is checked out before trusting any push.**

## Conventions
- **Retire, never delete**: `status: deprecated` + move to `.agi/nodes/deprecated/<type>/`; never `git rm`. A grid ref
  outlives its file; readers that glob a type dir read the retired sibling too, live-first. Watch
  `active_node_count` / `deprecated_node_count`; their sum never drops.
- **Two identifiers**: the **mint id** never changes (grid refs, provenance); the **address** is derived and may (G2.5).
- **A version is a grid commit**, never a second node file: edit in place, then `grid.py commit --all` (G6.3).
- **`THOUGHT` block** (G2.11): body is state, thought is delta — why THIS version differs; rewritten whole; absent =
  empty, never fabricated. The one authored region in a build node; its `BUILD-CONTRACT` is regenerated — never hand-edit.
- **Build nodes have two legal origins** (`goal:s29`): `[mvp]` for a new file, `[build, goal]` for a new version (also
  `[goal, mvp]`, `[goal, idea]`, per `[build].md` `parent_shapes`). A goal alone never mints one.
- **Goal ids MAY be renumbered** (owner 2026-09-23): keep every `mint_id`, re-point every reference in the SAME commit,
  record old → new in the THOUGHT. Retire a goal: `retired` + deprecate its seed node. Details: skill `agi-goal`.
- **`GOALS.md` is derived**: edit the goal node; a hand-edit vanishes at the next `--smoke`.
  `snapshot-goals.py --render --check` exits 0 only on a byte-identical round trip.

| Command | Does |
|---|---|
| `bash extensions/agi/driver.sh --smoke --max-iters 1` | snapshot + render + metrics — the node count must not drop |
| `python3 -m pytest extensions/agi/tests/ -q` | the engine's own suite |
| `python3 extensions/agi/bin/commands.py run verify` | the one verification pass (skill `agi-verify`) |
| `python3 extensions/agi/bin/snapshot-goals.py --render --check` | GOALS.md ⇄ goal nodes byte-identical |
| `python3 extensions/agi/bin/viewport.py --verify` | goal:g2.19 — one render, two readers |
| `python3 extensions/agi/bin/grid.py commit --all` | version every changed node and its payload |
| `python3 extensions/agi/bin/links.py links` | every link resolves; broken must be 0 |
| `python3 extensions/agi/bin/links.py schema` | goal:s31 — nodes violating their type's required list (dry) |
| `python3 extensions/agi/bin/spawn_budget.py status` | goal:g4.8 — live agents vs the tree-wide bound |
| `python3 extensions/agi/bin/provisioning.py status` | goal:g1.11 — per-spawn keys |
| `python3 extensions/agi/bin/envfile.py --check` | goal:g1.8 — required keys present, forbidden absent |
| `python3 extensions/agi/bin/crons.py show` | the crontab the graph declares |
| `python3 extensions/agi/bin/viewport.py --live` / `--emit llm` / `--emit both` | the live graph · what a kid is handed · both from ONE stream |
| `python3 extensions/agi/bin/write.py` | goal:g4.18 — named node operations (skill `agi-node-write`) |
