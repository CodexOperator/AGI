---
confidence: 0.8
goal_id: G13
goal_kind: long-term
heading_level: 2
id: "goal:g13"
mint_id: fe31c846128c479d8687ea6b4c042547
next_edges:
  - goal:g13.1
  - hypothesis:a00-5b27ca07-438c0a
  - hypothesis:a00-6b4ad6b2-a60b78
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - long-term
title: One read/write path for nodes — an LLM-native node interface
type: goal
---

**One way in and one way out of the graph.** Every operation an agent performs
on a node — create it, create the file behind it, edit it in place, read it,
read its history — should go through a single interface, turn-by-turn and
guardrailed, rather than through whichever of a dozen call sites happened to be
nearest. The shape wanted is **vim-like, not chat-like**: a small set of
composable operations, a locked sequence, and guardrails that make an illegal
move *unavailable* rather than merely discouraged.

**Today the write half is partly unified and the read half is not unified at
all.** `node_writer.write_node` is the one gated write routine and four callers
use it — `cli.py scaffold`, `cli.py done`, `post_wire`, `dispatch`. Three
generators sit outside it deliberately (`snapshot-goals.py`,
`snapshot-build-site.py`, `level3.py`), owning their own frontmatter keys and a
`preserve=` merge the routine has no notion of. There is no reading equivalent.

**The read-side defect is not divergent parsing — it is divergent failure
semantics.** Every parser in the tree agrees on frontmatter for every node in
the corpus; what differs is what each does when a node is malformed or an id
is duplicated. Malformed input raises, is silently skipped per-file, returns
`{}` with the whole file as its body, returns `None`, or vanishes from a dict,
depending which reader you happened to reach. None of those was chosen. They
are accidents that agree only because the corpus currently contains nothing
that would tell them apart.

**The count belongs to the chain, not to this goal — and this goal will stop
guessing at it.** Successive nodes have said seven, five, four and ten,
because the honest answer depends on where you draw the boundary: bulk corpus
readers and single-node readers are different populations, and only the first
is what a unified `parse_node` would replace. A goal that restates its chain's
measurements becomes the hand-maintained second copy this project keeps paying
for (`goal:s17`), so the number lives in the chain and nowhere else. Read it
there.

A reader that stops seeing a retired node fails quietly and in its own way,
which is the failure mode `CLAUDE.md` already documents for the live-first
deprecated glob — the same defect class, already observed.

**`goal:g4.6` is what made this legible.** One spawn path turned out to be a
config entry plus one adapter file, not a rewrite. The same argument applies
one layer down: a harness is to spawning what a node interface is to writing.
Both replace "N call sites that agree by convention" with "one call site that
agrees by construction".

**Three debts it would pay, each already recorded elsewhere.** First,
`thought_session:` is reserved in frontmatter and nothing writes it —
`goal:g2.7` and `goal:g10.1` want the chat that produced a version linked to
that version, the finest grain of the LOD axis, and `dispatch.py` knows the
harness session path at spawn time and drops it on the floor. On 2026-09-01 a
kid wrote `bin/completion.py` in full and died before recording anything; its
204 KB transcript was the only account of that design and was recovered by
comparing file mtimes. A write path that stamps the session once is the
difference between provenance and forensics. Second, a node's mint id and its
address are two identifiers (`goal:g2.5`), and every reader resolving one by
hand is a place they can be conflated. Third, `dispatch._node_type_for`'s
private step table and the `[<type>].md :: spawn` blocks that `spawn_gate`
actually enforces are two definitions of one fact, and they already disagree.

**What would falsify it.** A new node operation can be added and every existing
caller gains it without editing more than one file. Changing the verdict
taxonomy or the chain grammar changes what agents may write in the same commit
with nothing edited by hand. A retired node stays resolvable through the
interface with no caller knowing about `deprecated/`.

**Sibling, not duplicate, of `goal:g1.9`** — that goal is about what an agent
is *told*, this one about what an agent may *do*; merging them would lose the
distinction that makes either checkable. **Feeds `goal:g10`**, the hypergraph:
G10 is the structure, this is the aperture onto it.

## The shape, from the owner's board (2026-09-02)

**Three modules, and two of them are helpers.** `render.py` — possibly named
`engine.py` — owns every read and every write. `read.py` and `write.py` are its
helpers and nothing else calls them. **Exactly one path in, exactly one path
out**, which is the invariant at the top of this goal restated as a file
listing rather than as an intention. The owner's summary is the acceptance
test: *"`read.py` and `write.py` is all you need to develop moving forward."*

Two entry conditions reach the same destination, and naming both is what makes
the interface complete rather than a read API with a write API bolted on:

- **Code does not exist yet.** `snapshot-goals.py` runs, node bodies update,
  the node renders. This is today's generator direction, and it is the half
  that already works.
- **Code exists.** `read.py` reads it into a rendered node; `write.py` writes
  the rendered node back to node data, and back out to the code itself. The
  loop `read -> render -> write -> render` closes, and every arrow on it is
  one of the two helpers.

## A node body is a marker, not a payload

**The load-bearing consequence, and the one that changes what a node file
*is*.** A node body is not stored data. It is the **live-linked, live-streamed
content of the file the node points at**, resolved through the IO map
(`goal:g2.2`) at read time. What is stored on disk is a blank field or an empty
marked line — a placeholder that tells the read operation *where the body goes*,
nothing more.

Three things follow, each already half-true somewhere in this repo:

1. **`payload_ref` is the prototype.** A build node already links a file rather
   than copying it, and `grid.py` already versions node and payload as one
   tree. This generalizes that from one node type to every node type, so it is
   a widening of a proven mechanism rather than a new one.
2. **`goal:g2.2` gains the linkage itself.** Which file a node is linked to
   becomes IO-map content — declared and configured, not hardcoded per type.
3. **Propagation becomes deterministic, and the write path is what runs it.**
   With the link declared, a rename or a reference update is one traversal:
   the map (`goal:g2.2`) names every place the fact appears, `write.py` edits
   them as a kid or parent finishes its node. **The map owns the links; this
   goal owns the traversal.** No model retypes a reference — including the
   schema prose restated in `CLAUDE.md` and `SKILL.md`, whose links are to
   marked *regions* rather than whole files.

**Three questions this opens and deliberately does not answer.** Each must be
settled before any of it is built, and each is cheap to state now and expensive
to discover later:

- **Where does `THOUGHT` live?** It is authored, durable, and today it lives in
  the body. If the body is a marker, thought needs a home — and frontmatter is
  ruled out already, because `write_frontmatter` flattens newlines and would
  destroy it silently.
- **What is a goal node's linked file?** `goal:g6.9` established that
  `GOALS.md` is rendered *from* goal node bodies. A live-linked body points the
  arrow the other way. One of the two has to give, and G6.9 was paid for.
- **What does a link to a missing file do?** A deprecated node whose file is
  gone must not fail quietly — that is precisely the divergent-failure-semantics
  defect this goal was written about, reappearing inside its own fix.

**Scope, at the owner's direction: nothing here is built this session.** The
read and write paths are not to be touched until the parent and kid tiers are
both properly standing, because this interface is what they will both call and
designing it against a half-built caller is how it acquires a caller-shaped
seam.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version records the owner's board, and the board answers a question the
previous version could only pose. v3 said "one way in and one way out" and then
described the current mess; it had no picture of what the unified thing looks
like. Now there is one: three modules, two of them helpers, and a summary
sentence that doubles as an acceptance test — if you need a third thing to
develop against, the seam is wrong.

The genuinely new claim is that a node body is a marker rather than data. That
was not in any previous version and it is not a detail: it converts this goal
from "route the existing calls through one door" into "change what a node file
holds". It is also the reason the goal now names `goal:g2.2` as load-bearing
rather than adjacent — the IO map stops being a contract annotation and becomes
the linkage table the read path resolves through.

The three open questions are recorded unanswered on purpose. Each one is a
place where an existing, paid-for decision collides with the new shape —
`THOUGHT`'s home, `goal:g6.9`'s render direction, and this goal's own founding
finding about failure semantics. Writing them down now costs three paragraphs;
discovering the second one mid-migration would cost the `GOALS.md` round trip.

Scope note added at the owner's direction: not this session. The interface is
what parents and kids will both call, and it should not be designed while only
one of those callers exists.

Still no mvp seeded, and still for `goal:s22`'s reason — a board is not a
design brief, and this goal earns one through a hypothesis -> experiment ->
verdict chain like every other. Recording the shape does not shortcut that; it
gives the chain something specific to falsify.
<!-- THOUGHT:END -->
