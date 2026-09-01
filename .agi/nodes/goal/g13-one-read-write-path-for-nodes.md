---
confidence: 0.8
goal_id: G13
goal_kind: long-term
heading_level: 2
id: "goal:g13"
mint_id: fe31c846128c479d8687ea6b4c042547
next_edges:
  - hypothesis:a00-5b27ca07-438c0a
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

**Measured, superseding this goal's own first estimate.**
`hypothesis:a00-5b27ca07-438c0a` counted the read side rather than listing it
from memory, and the shape is sharper than "seven modules each re-implement
parsing": it is **five parsers in two stacks** —
`graph_core.persistence.frontmatter.load_node_file` (used by `zoom.py`,
`dispatch.py`, `dashboard.py`, `backfill-mint-ids.py`) against four ad-hoc
`split("---", 2)` readers in `bin/` (`post_wire`, `metrics`, `stitch`, and
`snapshot-goals`, whose loader `level3.py` reuses). `grid.py` was wrongly on
the first list: it reads git objects, a different job. The five agree on
frontmatter for **847/847** nodes and disagree on **847/847** bodies by
exactly two deterministic rules (a leading blank line, a trailing newline).

So the read-side defect is not divergent parsing, it is **divergent failure
semantics**: malformed input raises, returns `{}`, returns `None`, or is
silently swallowed depending on which of the five you reached; duplicate ids
resolve first-wins in one stack and last-wins in the others. Both are latent
today (0 malformed, 0 duplicates) and neither is chosen — they are four
accidents. A reader that stops seeing a retired node fails quietly and in its
own way, which is the failure mode `CLAUDE.md` already documents for the
live-first deprecated glob.

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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version replaces the read-path paragraph with a measurement. The first
version listed seven modules from memory and was wrong twice — `grid.py` reads
git objects rather than node files, and `level3.py` has no parser of its own —
and it named the wrong defect: the parsers agree, their failure semantics do
not. The correction came from the goal's own first hypothesis, which is the
chain working as intended, and is exactly why a long-term goal is not allowed
to seed a design brief before one exists (`goal:s22`).

Minted as a long-term goal at the owner's direction, having been intended "for
a while" and only becoming statable once `goal:g4.6` showed what unification
actually costs: one config entry and one file.

Deliberately NOT seeded with an mvp. The owner's instruction is that a
long-term goal earns its design brief through a full
hypothesis -> experiment -> verdict chain first, and this is the first goal
held to that rule — see `goal:s22`, which makes the rule mechanical rather than
remembered. Writing a design brief here now would be the exact shortcut s22
exists to close, in the goal that motivated closing it.
<!-- THOUGHT:END -->
