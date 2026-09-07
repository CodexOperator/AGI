---
id: goal:g13
mint_id: fe31c846128c479d8687ea6b4c042547
type: goal
next_edges:
  - goal:g13.1
  - hypothesis:a00-5b27ca07-438c0a
  - hypothesis:a00-6b4ad6b2-a60b78
confidence: 0.8
edited_by: season.py
goal_id: G13
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: active
tags:
  - goal
  - long-term
thought_session: season
title: One read/write path for nodes — an LLM-native node interface
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

**Three questions this opened, answered by the owner on 2026-09-02.** Each was
a place where a decision this project had already paid for collided with the
marker shape. All three are now binding on the build, and the chain falsifies
them rather than re-opening them:

- **`THOUGHT` stays in the node body.** A node file carries a marker *and*
  exactly one authored region, and they coexist — the marker says where the
  data is, the thought says why this version differs. Nothing migrates,
  `goal:g2.11` is untouched, and the grid keeps versioning thought for free
  because it already snapshots `node.md` per version. The alternatives were a
  third grid tree entry (clean, but thought stops being visible in the working
  tree and every reader grows an entry) and the head of the linked file (which
  puts an authored region inside a file generators rewrite — the exact
  `goal:g2.10` failure mode that left 8,034 fields reading `TODO(model)`).
- **A goal node links to itself.** `link_ref: self` — the body *is* the data,
  stated uniformly rather than as an absent field. `goal:g6.9` stands untouched
  and `GOALS.md` keeps rendering *from* goal bodies. This is deliberately an
  exception with a name instead of a hole: a reader never branches on
  `type == goal`, it resolves `self` like any other link, so the one path in
  and one path out survives the exception intact.
- **A link to a missing file raises where a caller can act, and is counted
  where it cannot.** A single-node read raises `MissingLink`. A bulk corpus
  scan returns a typed sentinel and increments a `broken_links` metric, in the
  same shape as `unevidenced_decisive_verdicts`. This is the goal's founding
  finding applied to itself: the defect was never divergent *parsing*, it was
  divergent *failure semantics*, so the answer is not one behaviour everywhere
  but two behaviours **chosen** — loud where a caller can fix it, survivable
  where one bad node must not kill a scan of 893.

**The scope gate is now open.** The original direction was that nothing here
gets built until the parent and kid tiers are both properly standing, because
this interface is what they will both call and designing it against a
half-built caller is how it acquires a caller-shaped seam. That condition is
met: the manifest race is fixed and verified at eight concurrent agents, two
concurrent parents ran without collision, and the read half landed with the
canonical reader keeping its own contract. **`write.py` is the next thing
built**, with the three answers above as its inputs rather than as questions it
has to stop and ask.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Owner addition, 2026-09-03, and it turns this goal from a direction into a testable end state. The body now names the symmetry -- read and write must treat a build node and a non-build node identically, with the engine choosing whether a body lives in the node or in the payload file and the caller never knowing -- and, more usefully, it names a SUCCESS CRITERION that can be checked rather than argued about: when the agi skill is invoked, exactly two disk-interaction tools exist, render viewport and write. That is falsifiable in a way "one read/write path" was not. A third filesystem tool in the skill is a failure of this goal, visibly, without anyone having to judge whether a path is sufficiently unified. Status stays active: it already was, and the owner confirmed no change is needed. What changed is scope clarity, not commitment. Two things are deliberately left open rather than decided here. First, how a payload-backed body and a node-backed body produce the SAME kind of grid version and session linkage -- if they do not, the unification is cosmetic, and that is a design question this session did not answer. Second, the owner has flagged this as one of the few goals in the tree where fanning out several parallel chains is actually warranted, because the direction is genuinely not obvious. goal:g4.1 records the general rule -- same-target concurrency is for open-ended goals and most goals here are clear-cut -- and this is named as an exception to it. Recorded via note through write.py rather than by editing the node file, after the owner caught me doing the latter earlier in this loop; GOALS.md re-rendered and round-trips byte-identical across 111 goals.
<!-- THOUGHT:END -->

## Agent Notes
### The symmetry this goal is actually asking for (owner, 2026-09-03)

**The read and write paths must treat a build node and a non-build node exactly the same.** That is the shape of the finished thing, and stating it makes the remaining work concrete.

**Read.** The same path that reads a non-build nodes body and renders it also reads a build nodes payload and renders it **as that nodes body**, live, in one coherent render. A reader never branches on whether the body happens to live in the node file or in a file the node points at.

**Write.** The same, in reverse. A write goes either to the linked body section inside the node, or to the linked body section in the payload file. **The engine decides which; the caller never does.** `links.py` already carries the primitive -- `link_ref` generalises `payload_ref` and `self` means the body is its own data -- but `declared: 0` across the corpus: today a node body is still a payload rather than a marker, so the two cases are only *representationally* unified, not behaviourally.

**The end state is a tool budget, and it is the real success criterion.** When the `agi` skill is invoked, exactly **two** disk-interaction tools should be available:

1. **render viewport** -- at a target node section and level of detail, at a target node whole, or at a target graph section at a given zoom level.
2. **write** -- to a new or an existing node.

Everything else an agent needs from the local system it should not have. Non-disk tools -- web access and the like -- are unaffected; this is a limit on filesystem reach, not on capability. An agent that can `cat`, `sed` and `grep` its way around the graph will, and every such path is one the engine cannot version, gate, or attribute.

**Deliberately open: how to organise this against the grid and session tracking.** A payload-backed body and a node-backed body must produce the same kind of grid version and the same session linkage, or the unification is cosmetic. This is named as an open design question rather than a decided one, and the owner has flagged it as a **good candidate for fanning out several parallel chains to explore competing solutions** -- one of the few goals in this tree where the direction is genuinely not obvious yet, which is the condition `goal:g4.1` names for aiming concurrent agents at a single target.