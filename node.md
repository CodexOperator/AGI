---
id: goal:g6.9
mint_id: f9e21a010143472d8f198d7ea5b10fe0
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
goal_id: G6.9
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - subgoal
thought_session: season
title: "G6.9: `GOALS.md` is rendered from the nodes, not the other way round"
---
**The last hand-authored source in this repo becomes derived, like everything
else.** `nodes/goal/` is currently generated *from* `GOALS.md`, which makes the
document the source of truth and the nodes a projection — the exact arrow
**G6.1** just reversed for engine code, still pointing the wrong way for the
goals themselves. Every property that made the inversion right there is true
here: a goal is a thought, thoughts live in nodes, and a node can be versioned,
zoomed, addressed and linked in ways a heading in a 2,600-line markdown file
cannot.

**What the document becomes: a rendered convenience, not a store.** A flat
human-readable digest of the goal nodes — useful for reading top to bottom, for
`git log`, for a person who wants the whole contract in one scroll. Not
authoritative, and marked as such in its own header so nobody edits it and
expects the edit to survive. The same relationship `context/INJECTION.md`
already has to the graph.

**And it is explicitly the weaker interface.** The real one is the dynamic
hypergraph renderer (**G9.4**, **G10.3**): a viewport a human pans and an agent
queries at the resolution it needs, which is strictly better for both readers
than a linear document is for either. Markdown is what we render *until* that
exists, not the target.

**The hard part is not the renderer, it is `snapshot-goals.py`'s prune.** That
script deletes every `origin: goals-doc` node it does not re-derive on a run —
H0i's shape exactly, and the reason CLAUDE.md carries a standing warning about
emptying a generator input. Inverting the direction means that prune must go
*before* the nodes become the source, not after: for the window where both
exist, a `GOALS.md` that fails to mention a goal must never be able to delete
that goal's node.

**Sequencing, and it is the whole risk:**
1. **Render first, prune never.** Add the node → document renderer and run it
   alongside the existing parser. Diff the rendered document against the
   hand-written one until they agree; that diff is the migration's own test.
2. **Cut the prune.** `snapshot-goals.py` stops deleting, then stops parsing.
3. **Nodes become authoritative.** `GOALS.md` gains a "generated — edit the
   nodes" header, and editing a goal means editing `nodes/goal/<id>.md`.

**Ids are the thing that must survive intact.** Goal ids are never renumbered
(this document's oldest rule), so the renderer's ordering and heading shape
have to be derived from the node's own `goal_id`, never from file order or
from position in the rendered output.

Falsifier: delete a goal's heading from `GOALS.md`, run the loop, and confirm
the goal node is still there and the next render puts the heading back. Until
that holds, the document is still the source and this is not done.

**Done 2026-08-25, and the falsifier ran exactly as pre-registered.** Deleted
`## S12`'s heading from `GOALS.md`, ran the loop: the node survived and the
next render put the heading back. The document is now output.

- `snapshot-goals.py --render` writes `GOALS.md` from `nodes/goal/*` plus
  `doc:goals-preamble`. `--from-doc` is the legacy import, retained for
  bootstrapping a hand-written document into a fresh project. **The bare
  invocation refuses to guess** — one direction prunes and the other cannot, so
  defaulting to either silently is the H0i shape.
- `--render --check` is the migration's own test and stays useful after it:
  **75 goals round-trip byte-identical.** Across 2,800 lines the only
  difference from the hand-written original was a single missing blank line
  after one heading, which the render normalised.
- Each goal node carries `heading_level` and `order`. Neither is inferable —
  depth would be guessed from the id shape, and the S-block deliberately runs
  S11..S17 before S1..S10 because ids are never renumbered.
- `goal_body_cap` is now `0` for this project. **A source of truth cannot be
  capped**, so S12's owner-picks knob got picked by the inversion rather than
  by preference.
- The preamble is `doc:goals-preamble`, `type: doc` and not `type: goal`: it
  has no status, no seeds and nothing to fulfil, and typing it as a goal would
  add a phantom to every count that reads `type == goal`.

**Two real bugs fell out of the round-trip check**, which is the argument for
building the check before the flip rather than after:

- `write_frontmatter` **substituted** a character instead of escaping it —
  `sval.replace('"', "'")`. S13's own title, *"...the string `\"None\"`"*, came
  back out of its node as `'None'`. Silent data loss in the one function that
  touches every node on every run, three lines below where S13 was fixed. Both
  copies of the serializer now emit a proper escaped YAML scalar.
- `snapshot-goals.py`'s prune keyed on `origin: goals-doc` alone, so the
  published (older) engine saw `doc:goals-preamble` — a node it had not written
  and could not produce — and deleted it. **Recovered from the grid**, which
  had it at v1 from the 5-minute cron 19 minutes earlier. The prune now
  requires `type: goal` as well.

That second one is worth keeping as the concrete case for the general rule in
**G6.1**: a generator may delete only what it can produce. It is also the
clearest thing the grid has yet done — the node existed in no commit, no
working tree and no backup, and came back whole.

**The document is the weaker interface and says so in its own banner.** The
real one is the hypergraph viewport (**G9.4**, **G10.3**); markdown is what
gets rendered until that exists, not the target.