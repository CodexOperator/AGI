---
confidence: 1.0
goal_id: G2.10
goal_kind: subgoal
heading_level: 3
id: "goal:g2.10"
mint_id: 167f314e0512428db94739aaba20ed4d
order: 18
origin: goals-doc
parents:
  - goal:g2
seeds: []
status: complete
tags:
  - goal
  - subgoal
title: "G2.10: A build node cannot hold a thought — the scan wipes its body"
type: goal
---

🔴 **`level3.py` regenerates a build node's entire body on every run. Anything
a model wrote there is destroyed on the next loop iteration.**

Measured 2026-08-27, by writing a value and re-running the scan:

| probe | result |
|---|---|
| prose added to a build node body | **wiped** |
| `why: TODO(model)` filled in with a real value | **wiped** |

And the corpus reads exactly as that predicts:

    why/perf/security fields across 190 build nodes:  8,034
    still reading TODO(model):                        8,034
    ever filled:                                          0

**Zero of 8,034.** That is not neglect. `[build].md` says the contract block
is harness-owned and "a model may fill `why`/`perf`/`security`" — the schema
states a permission the code revokes on the next scan. Any agent that spent a
turn filling one did work that was deleted before it could be read.

## Why this is a G2 goal and not a bug report

**G6.8 argues build nodes belong in the graph precisely because they hold
thought:** *"A code node ties cleanly to thought: it can spawn a hypothesis
about itself, an experiment against itself, or just an idea. That
bidirectionality is what makes it worth being a node rather than a record."*
Half of that is currently false. A build node can be *cited* by a thought; it
cannot *contain* one. Today it is exactly the "record" G6.8 says it is more
than — 190 nodes of mechanically-derived shape with a permanently empty
`why`.

The derived half should keep being derived — that is what makes it trustworthy
and what `stale_contracts` polices. The authored half has to survive. Concretely:
`write_frontmatter` already merges frontmatter with `preserve=`; the body needs
the same treatment — regenerate the mechanical `how`, carry over `why`/`perf`/
`security` and any prose outside the markers.

## This is also why the `@v2` nodes exist, and why they cannot be collapsed yet

> **Superseded 2026-08-27 — kept as the reasoning that set the sequence, not as
> current state.** The migration has since run and the convention is retired;
> see the final section. The five nodes no longer hold the prose described
> below, and they were retired in place rather than deleted.

Five nodes carry `origin: build-version` and an `@v2` id
(`build:bin-grid@v2` and four siblings). They hold **7,000–13,000 characters
of real reasoning each** — why `sanitize()` became injective, what
`migrate-refs` is for — and they survive **only because `level3.py` does not
own their origin and therefore never rewrites them.**

CLAUDE.md's rule is right in general: *a version is a grid commit, not a
second node file.* But the `@v2` file is not redundancy here — **it is the
only durable place a build artifact's reasoning can currently live.**
Verified before proposing removal: v1 and v2 payloads are byte-identical to
the engine for all five, so no bytes would be lost — but ~47,000 characters of
prose would be, with nowhere to put it, because the v1 node's body is wiped on
the next scan.

**So the sequence is forced: fix the wipe, migrate the five bodies into their
v1 nodes, then retire the `@v2` convention.** Collapsing them first would
delete prior art to satisfy a naming rule, which is the trade this project
has repeatedly refused. Pairs with **G6.8**, **G6.3** and **G7**.

Falsifier: fill one `why:` on one build node, run `driver.sh --smoke`, and
read it back.

## Fixed 2026-08-27 — the wipe is closed

`write_frontmatter` gained `preserve_body=`, and the three regenerating
writers (`level3.py`, `snapshot-build-site.py`, `decompose-engine.py` — all
sharing one serializer since **S14**'s residual was collapsed the same day)
now carry the authored region across.

Two named regions instead of one guess: `BUILD-CONTRACT` stays derived and
policed, `THOUGHT` stays authored and preserved. This goal originally asked to
"carry over any prose outside the markers", which is not something a
regenerating writer can identify without guessing which prose was
hand-written; the marked region made preservation mechanical and testable
instead. The general form is **G2.11**.

`why`/`perf`/`security` carry over too, keyed on entry `name` and not on `how`
— `how` embeds the line number, so keying on it would drop a model's rationale
the first time anything above the call site moved.

Falsifier run on the live corpus, both directions, twice:
`nodes/build/bin-grid.md` had one `why:` filled and one `THOUGHT` block
appended, then took two full `level3.py --from-grid` scans. Both survived.
Before the fix the first scan wiped both. Idempotence verified separately,
because a derivation that does not reproduce its own stored value is
**G6.5**'s silent-cron failure: a full scan moved exactly the 4 nodes whose
source had changed and nothing else, and `stitch --verify --from-grid
--strict` reported 0 drift in all four categories.

## Complete 2026-08-27 — the migration ran; the `@v2` convention is retired

The sequence this goal set out is finished. **47,356 characters of reasoning
moved** from the five `origin: build-version` bodies into their v1 nodes'
`THOUGHT` regions, verbatim, each carrying a one-line provenance note naming
where it was authored:

| v1 node | body before → after | THOUGHT |
|---|---|---|
| `build:bin-grid` | 13,113 → 26,399 | 13,284 |
| `build:src-graph-core-identity` | 5,380 → 18,135 | 12,753 |
| `build:bin-stitch` | 6,780 → 14,590 | 7,808 |
| `build:lib-find-root.sh` | 1,161 → 8,755 | 7,592 |
| `build:skills-agi-SKILL.md` | 1,118 → 8,525 | 7,405 |

`nodes_with_thought` 2 → 7, `thought_coverage` 0.003 → 0.009.

**The five `@v2` nodes were retired in place, not deleted** — `status:
deprecated`, files kept, mint ids kept, `supersedes:` edges kept, grid refs
kept. Deletion was offered and explicitly rejected by the owner: a deleted
node's grid ref outlives the file, so removing the five would not shrink the
durable structure, it would decouple it — leaving refs and edges with nothing
live behind them for **G10**'s hypergraph to reconcile later. An orphaned ref
is worse than a marked-dead file. Each retired body is now a tombstone naming
the v1 node its reasoning went to; the original text stays readable through
the node's own ref.

**`node_count` deliberately does not move** (789 before and after). That is
what makes the retirement itself trackable rather than silent: retirement is
now visible as `active_node_count` (784) against `deprecated_node_count` (5),
a metric added alongside this work rather than as a count that quietly drops.
**G7**'s invariant is about silent loss, and a shrinking total is exactly the
shape that hides it.

`status: deprecated` is new for build nodes and is **not yet in
`context/schemas/[build].md`** — nothing rejects it (schema validation runs on
the writer path, not over nodes on disk), but declaring it is a real residual
and belongs to whoever next touches the build schema.

Idempotence verified, because a derivation that does not reproduce its own
stored value is **G6.5**'s silent-cron failure: a full `level3.py` scan over
all 185 discovered engine files reproduced all five v1 files byte-for-byte and
changed nothing corpus-wide. The `THOUGHT` regions sit after the derived
trailer, which is where `splice_thought` re-inserts a carried region — placing
them between `BUILD-CONTRACT:END` and the trailer would have made every scan
rewrite the file and left the graph permanently dirty.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version closes the goal, and the previous one was wrong about the cost of
closing it. It said retiring the `@v2` nodes "deletes 5 nodes and drops the
node count" — that was the only removal shape considered, and it framed the
decision as prior-art-versus-tidiness, needing sign-off because something
would be lost.

Sign-off was sought and the framing turned out to be the mistake. The
owner initially agreed to deletion, then reversed it unprompted on a reason
this node had not weighed: grid refs survive a working-tree delete. That fact
was already known here — it is what earlier made deletion look *safe*,
because nothing is truly lost. Read against G10 it argues the opposite way.
Safety was never the binding constraint; **coupling** was. Deleting a node
whose ref persists does not remove structure, it strands it.

So the count never had to drop, and the sign-off that seemed necessary was for
an operation that should not have been on the table. Recorded because the
error is reusable: this project reasons about deletion by asking what is lost,
and for graph nodes that is the wrong first question — ask what stays behind
without its file. The paired lesson is the metric. Retiring in place makes
`node_count` flat, which would have made the retirement invisible; that is why
`active_node_count` ships with it rather than after it.
<!-- THOUGHT:END -->
