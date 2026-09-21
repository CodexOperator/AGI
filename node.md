---
id: goal:g2.11
mint_id: 684604b774304d6aba522fc661a30bfd
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: season.py
goal_id: G2.11
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
title: "G2.11: Every node version carries the thought that produced it"
---
**`body` is state; `thought` is delta.** The body says what a node asserts
*now*. The thought says why *this version* differs from the last one. They
accumulate differently, they are rewritten on different schedules, and
collapsing them into one field loses the second — which is what the corpus
did until 2026-08-27.

The two halves of a node body are now named regions:

| region | owner | lifetime |
|---|---|---|
| `BUILD-CONTRACT` | the harness | rewritten every scan, policed by `stale_contracts` |
| `THOUGHT` | whoever authored the version | carried across every rewrite |

**G2.10 is the special case; this is the general one.** G2.10 measured a build
node's body being wiped on every scan and fixed the writer. But the question
it exposes is not about build nodes: *where does the reasoning behind a change
live, for any node?* For a build node the answer used to be "nowhere" — the
body is 100% derived contract, so there was no slot at all. For an idea or a
hypothesis the body **is** argument, so it looks like the answer is "the body"
— but that body is the cumulative case being made, rewritten in place as the
argument matures. It is not a record of what changed on 2026-08-19 and why.

## Why per-version, and why that needs no new machinery

The grid already snapshots `node.md` once per version. So a thought written
into the body is, without one line of new plumbing, **the thought that was
current at that version** — `grid.py log` becomes a changelog of reasoning and
`grid.py diff` shows how the reasoning moved, not just how the prose did.

That is the whole argument for putting it in the body rather than inventing a
third grid tree entry beside `node.md` and `payload`. The cheap thing and the
right thing coincide here, which is rare enough to say out loud.

## Three decisions, each with the alternative that was rejected

- **A marked body block, not a frontmatter field.** `write_frontmatter`
  flattens newlines (`str(v).replace("\n", " ")`), so multi-line prose in
  frontmatter is destroyed silently by the one function that writes every node
  on every run. That function has already produced two corpus-wide data-loss
  bugs (**S13**, and the null round-trip in **S14**). Prose does not go there.
- **Marked, not positional.** "Any prose outside the contract block" — G2.10's
  original phrasing — is not something a regenerating writer can identify
  without guessing which prose was hand-written. A marker makes preservation
  mechanical and testable.
- **Absent means empty.** Adding the field churned **0 of 786** nodes. No
  backfill pass, no mass rewrite, no `thought: ""` on every node. Existing
  nodes acquire a thought when someone next has one, and the graph is
  honest in the meantime about not knowing why most of it was written.

## Stripped from injected context, deliberately

Renderers must **not** carry thought blocks into `GOALS.md`, `INJECTION.md` or
`zoom.py`'s kid context. This is the design ethic applied directly: thought is
**provenance you zoom into**, not weight every reader carries forever. A
thought written once would otherwise be injected into every session for the
rest of the project's life — the exact "heavier pack" the ethic exists to
refuse.

The trap this creates and which must be handled: `snapshot-goals.py --render
--check` asserts a byte-identical `nodes -> GOALS.md -> nodes` round trip. If
render strips thought, the round trip loses it and `--check` fails. The
comparison has to exclude the thought region, not the strip be abandoned.

## What is deliberately not built here

**The automatic variant.** A thought could be a *link to the chat that
produced the version* rather than prose an agent writes by hand. That is
already argued, in two places: **G2.7** (the finest zoom is the chat that
produced the version) and **G10.1** (chats are thoughts, so chats are nodes),
including the hard part — a chat that produces nothing has no owner and
vanishes. This goal deliberately does not restate them; it builds the manual
half, which works today, and reserves `thought_session:` in frontmatter as the
short scalar those goals can populate later. Two sources of truth about one
mechanism is how the injected context once ended up teaching the opposite of
the skill (H3b).

**Retro-fill from chat history.** Existing nodes have empty thoughts. Filling
them from session transcripts is possible but is G10.1's problem, not this
one's, and it should not be done by inventing plausible reasoning after the
fact — a fabricated thought is worse than an absent one, because it reads as
evidence.

Falsifier: fill one `why:` and one `THOUGHT` block on a build node, run
`driver.sh --smoke` and a full `level3.py` scan, and read them back. Run twice.
Both must survive both passes. (Run 2026-08-27 on `nodes/build/bin-grid.md`:
both survived; before the fix, both were wiped by the first scan.)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version of this goal, and the first thought in the graph — so it is also
the demonstration that the mechanism works.

The idea arrived from the user as "add a `thought` field to each node, unless
`body` already covers it for build nodes." Checking that premise is what
produced the shape above: for build nodes `body` does not cover it at all (the
body is 100% derived contract, and G2.10 had just measured 8,034 authored
fields being wiped unread), while for idea/hypothesis nodes `body` *looks*
like it covers it but does not — that body is the cumulative argument, not a
record of what changed in this version. `body` is state, `thought` is delta.
That distinction is the whole goal and it came from testing the user's own
caveat rather than accepting it.

Three alternatives were live and two were rejected on evidence, not taste. A
frontmatter field dies to `write_frontmatter`'s newline flattening — the same
function behind S13 and S14's corpus-wide corruptions. A third grid tree entry
beside `node.md` and `payload` is the purest design, and would keep thought out
of readers by construction, but it needs an authoring surface and new plumbing;
the body block gets per-version storage free because the grid already snapshots
`node.md` per version. Purity lost to the fact that the cheap option was also
sufficient.

What I am least sure of: whether "rewritten from scratch each version" survives
contact with agents who will be tempted to append instead. If thoughts start
accumulating, this becomes a second body and the distinction collapses. Worth
measuring later — average thought length over versions is the tell.
<!-- THOUGHT:END -->

## Complete 2026-08-27

The mechanism ships and is verified end to end: the block survives every
regenerating writer, readers strip it, the grid versions it per node version,
`thought_coverage` reports it, and it is declared in all 14 active schemas plus
`CLAUDE.md` and `SKILL.md`.

**Coverage is 2 of 788 and that is not an incomplete goal — it is the design.**
Absent means empty by construction; the alternative is fabricating reasoning
for 786 nodes after the fact, which this goal explicitly forbids because a
made-up thought reads as evidence. Nodes acquire a thought when someone next
has one. Recovering real reasoning from stored sessions is **G10.1**'s
problem, not a residual of this one.