---
id: goal:s35
mint_id: 2e11d8bd74be4ca0a1755ad3240ae405
type: goal
parents:
  - goal:g15
next_edges: []
confidence: 1.0
edited_by: director
goal_id: S35
goal_kind: short-term
heading_level: 2
origin: goals-doc
scaffold_hash: eb5531b880f23924
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S35: Schemas are nodes, and they live under nodes/"
---
# goal:s35

## Agent Notes
**Owner decision, 2026-09-05: schemas ARE nodes.** They sit in
`.agi/context/schemas/` because that is where they were first written, not
because anything about them is context. They are the most load-bearing
documents in the graph — every spawn is checked against one — and they are the
only such documents with no mint id, no version history in the grid, no
provenance, and no place in any count of what this project knows.

**No payload. The schema node IS the file** — unlike a build node, which is a
node *pointing at* bytes elsewhere, a schema's frontmatter and its prose are the
whole artifact. That is why this is not simply "give each schema a build node".

### Why it is worth doing, concretely

- **They get grid history.** Today `[goal].md` was widened to let a goal name
  the build node that produced it, and there is no `grid.py log` for that change
  — only the repo commit. Every other consequential document in this project has
  a per-node version chain; the ones that govern all the others do not.
- **They get a `THOUGHT` block.** The reasoning behind a schema revision is
  exactly the reasoning most worth keeping, and it currently lives in prose that
  the next revision overwrites.
- **They stop being invisible.** `node_count`, `links.py`, `viewport.py` and the
  injected map all read `nodes/`. Seventeen schemas are outside every one of
  them.

### The migration, in the order that keeps it safe

The hazard is that **every reader globs `nodes/<type>/*.md`**, so the moment a
file lands there it is a node whether or not it looks like one. A move-first
migration therefore breaks `links.py`, `metrics.py` and `stitch.py` in one step,
against files that have no `id:` and no `mint_id:`.

1. **Write `[schema].md`** — the meta-schema. What a schema node must carry:
   `id: schema:<name>`, `type: schema`, `mint_id`, `title`, `tags`, plus the
   schema keys it already has (`name`, `fields`, `validation`, `spawn`).
2. **Add node frontmatter to all 17 files, in place, still under
   `context/schemas/`.** `mint_id` via `backfill-mint-ids.py`, never invented by
   hand (`goal:s14`). Nothing reads them as nodes yet, so this step cannot break
   a reader.
3. **Teach `schema_registry` to resolve either location**, nodes-first, context
   as fallback. Six non-test modules reach the directory today
   (`schema_registry/loader.py`, `cli.py`, `node_writer.py`, `evidence_gate.py`,
   `spawn_gate.py`, `dispatch.py`) plus five test files.
4. **Move them** to `.agi/nodes/schema/`, one commit. `active_node_count` rises
   by 17 — a rise is legal, a drop is the thing that is never allowed.
5. **Verify, then drop the fallback** in a later commit, not the same one.

### The falsifier

`links.py schema` reports zero violations for `type: schema` itself; a spawn
checked against a moved schema produces the identical decision to one checked
before the move; and `grid.py versions schema:goal` returns a version chain.
**The count check is the sharp one:** node counts may only rise across this
migration, and the rehearsal must be run before the real cut — `goal:g11`'s
migration was rehearsed four times against exactly this invariant.

### Not in scope

`agent_session.md`, `[overview].md`, `[shape].md` and `[config].md` are in the
same directory but are not node-type schemas. They move too — they are equally
nodes — but their `type:` is decided during step 1, not assumed here.