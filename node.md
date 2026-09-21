---
id: goal:s30
mint_id: 50c014bec839497aaae0423b3698a709
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S30
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S30: `HANDOFF.md` is replaced each session, so standing content cannot live in it"
---
**Two rules, and the second follows from the first by necessity.**

1. **The director replaces `HANDOFF.md`'s session section wholesale**, on their
   first substantive action — no reading it first, no appending, no asking.
   The one exception is when the user asks to *check* the handoff, which is a
   question about the previous session.
2. **Therefore nothing that is true across sessions may live in it.** Standing
   instructions inside a file the next director deletes are standing
   instructions with a countdown on them.

**Replacing is safe here as a measured property of this file, not a general
licence.** `HANDOFF.md` is `build:HANDOFF.md` with `payload_ref: HANDOFF.md`,
so `grid.py commit --all` versions the payload alongside the node: at the time
of writing, **55 versions, and v40 materialises in full** via `grid.py payload
build:HANDOFF.md --version 40`. Nothing is lost by replacing, so accumulating
charges every future cold session for superseded state and buys nothing — the
principle this repo already applies to itself, that git history is the archive
rather than a to-do list to keep re-adding to.

**The previous rule was the opposite and it was wrong.** "Old sections are
archive and stay" is accumulate-forever; the file reached **1,723 lines with
six session sections, five superseded**, in the document every cold session
opens first.

## What moved, and why it had to

`QUICKSTART.md` — the `bin/*.py` safety rail, cloning and installing on a new
machine, the one-iteration diagram, the glossary. **Keeping it in `HANDOFF.md`
became a live hazard the moment replacement became the default:** the first
director to follow rule 1 correctly would have deleted the install guide along
with the previous session's state. The split is not tidiness, it is removing a
trap that the new rule created.

`README.md` pointed at `HANDOFF.md` as *"Start here on a new machine"* and now
points at `QUICKSTART.md`. `skills/agi/SKILL.md` had no mention of
`HANDOFF.md` at all, which is part of why the convention drifted far enough to
need this goal.

## Falsifier

Delete `HANDOFF.md`'s session section and write a new one. Afterwards: a fresh
session can still bootstrap from zero (`QUICKSTART.md` intact), still knows
what the project is committed to (`GOALS.md` intact), and can still recover any
previous session (`grid.py payload build:HANDOFF.md --version N`). If any of
the three fails, standing content is still leaking into the replaced file.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted after the owner asked whether the director actually had permission to
erase the handoff rather than open the existing one. It did not — the rule I
had landed the day before said the opposite in as many words — and the question
was worth a goal rather than a fix because the two rules are coupled: making
replacement the default silently converts every standing instruction in the
file into something with a deletion date on it.

That coupling is the whole content here. The `QUICKSTART.md` split reads like
housekeeping and is not: it is the second half of a change whose first half
would otherwise destroy the install guide on its first correct application.

The safety argument is measured rather than assumed, and deliberately narrow.
`grid.py versions` was run before the rule was written, not after, because
"the grid keeps it" is exactly the kind of claim that is true of build nodes in
general and would have been worth checking for this one specifically.
<!-- THOUGHT:END -->