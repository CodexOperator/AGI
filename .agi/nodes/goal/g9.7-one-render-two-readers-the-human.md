---
id: goal:g9.7
mint_id: 3f9c1a4e7d2b48c5b1e0a6f83c5d7e21
type: goal
parents:
  - goal:g9
confidence: 1.0
edited_by: season.py
goal_id: G9.7
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: season
title: "G9.7: One render, two readers: the human viewport and the LLM's context are the same view"
---
**Stated by the owner, 2026-09-02, and it is a constraint on `goal:g9.4`
rather than a feature beside it:** *"I want it to be the same view as you'd
want to present to an LLM, so we can iterate on it as I use it to start
observing things more graphically."*

**The invariant.** The viewport a human pans across and the context a kid is
spawned with are **one render at two grains**, not two renderers that happen to
agree. Whatever `zoom.py` hands an agent is what the terminal draws, and the
terminal is where a human tunes it.

## Why this is the load-bearing half of legibility, not a nicety

`goal:g9` says a system whose state only agents can read cannot be evaluated,
corrected, or handed to anyone else. This goal says the converse is worse:
**two views drift, and the one nobody watches is the one agents actually
read.** Today `INJECTION.md` caps its ASCII map at 200 lines and truncates
silently — a human has never looked at what a kid is handed, because no
instrument pointed there. The dashboard (`goal:g9.1`, built) shows a human
metrics and health; it does not show a human *what the agents are seeing*.

**The mechanism that makes it hold rather than a rule someone remembers.** The
same argument `goal:g1.9` makes about briefs — a brief that restates a rule
enforced elsewhere is a hand-maintained copy of a contract — applies to views.
A viewport that re-derives the graph is a second reader with its own failure
semantics, which is precisely the defect `goal:g13` was written about. So the
viewport must consume `goal:g13`'s read path, not its own.

**Consequence, and it is the payoff the owner named.** Tuning the view for a
human tunes it for every agent in the same edit. The human becomes the
feedback loop on agent context quality — which no one currently is.

## Ordering, decided with the owner

This is why the viewport comes **after** the unification and not beside it.
Building it against today's several overlapping ASCII renderers would mint the
second reader this goal exists to forbid. `goal:g9.4` already absorbs the
renderer unification (A2) and says to do it *as part of* the viewport, because
the viewport requirement is what tells you what the unified renderer needs to
do. This goal adds the other end of that: **and the unified renderer's other
consumer is the spawn path.**

## Three axes the owner selected, and one they did not

Selected: **space** (pan/zoom a window across a graph bigger than the screen),
**time** (step through iterations and grid versions), **live** (agents rendered
where they are working, moving as they move). Not selected: stepping a chain
node-by-node — recorded here so a later reader does not re-propose it as an
oversight.

Each axis has to answer the same question twice: *what does a human see, and
what would an agent be handed at this position?* An axis that only answers one
of those has failed this goal even if it works.

## Falsifier

Change what the renderer emits — a level, a cap, a field — and both the
terminal viewport and the next kid's injected context change in the same
commit, with nothing edited by hand. If a human can tune the view and an
agent's context is unaffected, there are two renderers and this goal is not
met.

Second, behavioural: a human watching the viewport during a live run should be
able to say why a kid went where it went, from what the viewport showed. If
explaining a kid's behaviour requires opening `INJECTION.md` separately, the
view is not the one agents read.

## Relations

- **Constrains `goal:g9.4`** — the viewport is the deliverable; this is the
  invariant it must satisfy.
- **Depends on `goal:g13`** — the unified read path is the single reader both
  consumers call. Blocked until g13's read half stands.
- **Sibling of `goal:g1.9`** — one brief assembled by the engine; this is one
  view rendered by the engine. Same argument, different artefact.
- **Feeds `goal:g8`** (forkability) through `goal:g9`: a fork needs to see
  what it inherited.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted 2026-09-02 from the owner's session brief, because it is a commitment
and commitments belong in a goal node rather than in `HANDOFF.md`, which the
next director deletes.

The reason it is its own goal rather than a paragraph appended to `goal:g9.4`
is that it is falsifiable on its own and g9.4 is not changed by it. g9.4 says
build a pannable viewport; it would be satisfied by a viewport with its own
private renderer. This goal says the renderer must be shared with the spawn
path, and that claim survives even if the viewport's UI is thrown away and
rebuilt. Folding them would lose the distinction that makes either checkable —
the same reason `goal:g13` records for staying separate from `goal:g1.9`.

Filed `active` rather than `horizon` because it is scheduled: phase C of this
session's plan, iterations 6-8. Its parent `goal:g9` stays `horizon`, which is
correct and deliberate — `goal:s26` forbids a long-term goal being `complete`
while a child is live, not a child being active under a horizon parent.

The "not selected" paragraph exists because an unrecorded rejection reads as an
oversight to the next reader, who then re-proposes it. The owner chose three of
four axes deliberately.
<!-- THOUGHT:END -->