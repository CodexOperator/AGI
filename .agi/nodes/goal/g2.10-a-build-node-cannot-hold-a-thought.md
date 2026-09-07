---
id: goal:g2.10
mint_id: 167f314e0512428db94739aaba20ed4d
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.10
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
title: "G2.10: A build node cannot hold a thought — the scan wipes its body"
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

Idempotence verified, because a derivation that does not reproduce its own
stored value is **G6.5**'s silent-cron failure: a full `level3.py` scan over
all 185 discovered engine files reproduced all five v1 files byte-for-byte and
changed nothing corpus-wide. The `THOUGHT` regions sit after the derived
trailer, which is where `splice_thought` re-inserts a carried region — placing
them between `BUILD-CONTRACT:END` and the trailer would have made every scan
rewrite the file and left the graph permanently dirty.

## Residual closed 2026-08-28 — retirement is declared, and has an address

`status: deprecated` is now declared in `context/schemas/[build].md`, as an
**optional** field: absent means live, and it is deliberately not in `required`,
since adding it there would invalidate 185 nodes to express a default.

**A retired node now moves to `nodes/deprecated/<type>/`** — the same per-type
split, one level down. That changes its **address**, which is derived and
expected to change on regroup, and never its **mint id**, so every grid ref and
provenance link keeps resolving (**G2.5**). Git recorded all five as renames.

Readers that walk `nodes/` recursively needed nothing — `metrics.py`,
`grid.py`, `snapshot-goals.py`, `evidence_gate.py`, `snapshot-build-site.py`
and the rest already `rglob`. **Four globbed a single type directory and would
have silently stopped seeing retired nodes**, which is how a deprecation turns
into a deletion nobody authorised:

| reader | why it matters |
|---|---|
| `stitch.py` | a retired node still **claims** its `payload_ref`; dropping it turns the engine file into an `orphan_files` report — drift, refused publish |
| `level3.py` | must rewrite a node **where it lives**, or a scan re-mints it at the live address and one id exists in two files |
| `node_writer.py` | an edge pointing at a retired node has to keep resolving |
| `zoom.py` | display enrichment; a node with no title reads as corruption, not retirement |

All four now read live directory first, then the retired sibling. **The order
is load-bearing** wherever a reader takes the first hit: a live node must win
over a retired namesake, and that has its own test.

Verified: `node_count` 790, `active_node_count` 785, `deprecated_node_count` 5 —
**identical before and after the move**, which is the property that says the
regroup is an addressing change and nothing else. `stitch --verify --from-grid`
reports the same 191 nodes, 5 version chains, 0 orphans, 0 drift. A full scan
reports 0 nodes created and 0 pruned. Tests 794 → 800.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version closes the residual the last one named, and the interesting part is
that the residual was two things wearing one name.

The declaration gap was the small half: a status the code honoured and the
schema did not mention. Real, but a one-line fix.

The half that was not written down is that **`status: deprecated` had no
address.** Five nodes sat in `nodes/build/` marked dead, indistinguishable by
location from the 185 live ones, and every future reader would have had to know
to check a field. Giving retirement a directory is what makes it structural
rather than advisory — and it is the form the owner asked for, per type, so
`nodes/deprecated/goal/` and the rest already have their shape when the first
goal retires.

What the move surfaced is worth more than the move. Four readers globbed a
single type directory, and **each would have failed differently and quietly**:
`stitch.py` by reporting the retired node's engine file as an orphan and
refusing the publish; `level3.py` by re-minting the node at its old address, so
one id lived in two files; `node_writer.py` by failing to resolve edges into it;
`zoom.py` by rendering it untitled. Only the first is loud. The others degrade
into something that looks like ordinary corruption later, with no link back to
the retirement that caused it.

That is the same lesson as the last version, one layer down. Deleting a node
strands its grid ref; hiding a node from a reader strands whatever that reader
was responsible for. In both cases the node "still exists" and the damage is in
what stopped pointing at it. **When retiring anything here, the question is not
whether the thing survives — it is which readers stop seeing it, and what each
of them silently concludes from the absence.**

Previous thought on this node: why deletion was offered, agreed, then reversed.
One grid version back — `grid.py diff goal:g2.10 --back 1`.
<!-- THOUGHT:END -->