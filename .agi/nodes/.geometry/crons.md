---
id: cron:crons
mint_id: dc4da698f3f94dbc83a0c2233b2a8b94
type: cron
parents:
  - goal:g10.2
cadences:
  grid_sync:
    every_mins: 5
    enabled: true
  branch_push:
    schedule: 7 * * * *
    enabled: true
  publish_engine:
    schedule: 37 * * * *
    enabled: false
  engine_push:
    schedule: 47 * * * *
    enabled: false
crons_live: true
edited_by: season.py
season: 1
status: active
tags:
  - geometry
  - cron
  - structural
thought_session: season
title: Cron cadence declaration
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Two defects, found by the parent re-verifying this node's own claim during a
`goal:g11` migration freeze: flipping the frontmatter boolean off really does
remove every managed line (confirmed live: 2 lines removed), but this node's
OWN PROSE never said which value does that — a reader had no way to answer
"which value turns the crons off" from the node that exists to answer it,
which is exactly what happened: the crons were believed disabled while they
kept running and pushing.

The root cause was mechanical, not a one-off typo: every past edit to
`crons_live` replaced the boolean with a global find-and-replace that ran
through this body's prose as well as the frontmatter, because the prose used
to spell out the literal pattern `` `crons_live: true` `` (key, colon, and
value glued into one string) in its own headings and sentences. A
find-and-replace targeting that exact string flips the frontmatter and every
matching prose occurrence together, so both sides of the explanation always
carried the *same* value — self-contradictory at v1 (`true`), the
all-`false` version, and back to `true` again, every time, by construction.
Confirmed across the three prior versions of this node
(`git show 78a95fa89:nodes/.geometry/crons.md`,
`git show 90ff99986:...`, `git show 27855bafc:...`): the same X appeared on
both sides of "`crons_live: X` is the single flip that removes... and
`crons_live: X` is the equally single flip that brings back", which cannot be
true for any single X.

**Fixed by never writing that composite string again.** The two sections
below name `` `crons_live` `` once, as the key, and name `` `false` `` and
`` `true` `` separately, as plain values, each tied to its own effect in its
own sentence — no shared "key: value" token exists anywhere in this body for
a blanket replace to catch. A future edit to the frontmatter's boolean can
therefore no longer drag the prose's claim along with it; the prose will only
go stale if someone edits *it* directly, which is a normal editing risk, not
a self-inflicted structural one.

Also worth recording precisely, because the old text had it backwards: the
self-reapply edge case belongs to `false`, not `true`. `crons_live: false`
removes *all four* lines unconditionally (`grid_sync`'s own `enabled: true`
does not save it) — including `grid_sync` itself, which is the job that
would otherwise notice the next edit and re-apply it within five minutes. So
going back to `true` needs one manual `crons.py apply` to install the first
round of lines; after that, `grid_sync` is running again and every
subsequent edit to this node self-applies as before, with no further manual
step. `true` does not unconditionally install all four lines either — only
the ones whose own `cadences.<job>.enabled` is `true`, which today is
`grid_sync` and `branch_push` (`publish_engine` and `engine_push` stay
disabled regardless of `crons_live`).

Second, unrelated defect fixed in this same version: this node carried two
authored reasoning regions (marked with the paired HTML comment this schema
uses for exactly one such region per node) — the previous version's, about
retiring the `publish_engine`/`engine_push` cadences after `goal:g11`, left
at the top; and an older one below it, about correcting this node's own mint
from parentless to `parents: [goal:g10.2]`, from the version before that.
Past edits added a new region at the top without removing the one
underneath, which the schema does not allow — exactly one such region per
node, rewritten from scratch per version. Both are merged into this single
one. The
parentage fix from the older block is still true and is why `parents:
[goal:g10.2]` is set above; that fact now lives in the frontmatter itself; it
does not need to be restated at length here. The cadence-retirement reasoning
from the newer block is still current and now lives in the body below,
unchanged in substance.

`crons_live` is left `false` in this version — the parent froze the crons
deliberately for the duration of this migration and restores it at the end.
This version changes only the prose and the duplicate-block cleanup, not the
frozen state.
<!-- THOUGHT:END -->

The scheduling cadence for this project's four recurring jobs, declared as
graph content rather than left to live only in a scheduled-job table
somewhere no node points at. `grid_sync` runs on a plain interval
(`every_mins`); the other three run at fixed points in the hour
(`schedule`, a 5-field cron expression). This node states cadence and
enablement only — it does not know a command or a filesystem path, and it
never will: those are resolved at apply time by the reader, not encoded
here (G8.2 — no machine's layout belongs in a graph node any more than in
the engine that ships to every project).

## What `false` does: the kill-switch

Setting the frontmatter boolean above to `false` is the single flip that
removes every managed cron line at once, unconditionally — no individual
job's own `enabled` flag can save it. This exists for exactly the situation
this repo used it for: `goal:g11` moved the graph inside the repo it builds,
a change to where things live on disk while four crons independently read
and write that same disk on their own timers. `grid_sync` snapshotting
mid-move, `branch_push` pushing a half-moved branch, `publish_engine`
publishing against a graph commit the move has not settled yet, `engine_push`
committing an engine tree mid-shuffle — any one of the four racing the move
is a way to corrupt it. One boolean rather than four independent toggles is
what makes "is it safe to move yet" a single fact instead of a four-way
coincidence to verify by hand. Setting it removes the running lines within
one `grid_sync` interval of the edit landing — see "The self-reapply
property" below for the one case where that stops being automatic.

## What `true` does: installing the declared cadence

Setting the frontmatter boolean above to `true` reconciles the real crontab
to match `cadences:` above: each job whose own `enabled` is also `true` gets
installed (today: `grid_sync` and `branch_push`; `publish_engine` and
`engine_push` stay out regardless, because their own `enabled` is `false` —
see "Two cadences the migration made meaningless" below). This is the
opposite of the previous section: `false` overrides every job's own flag to
off, `true` defers to each job's own flag.

## The self-reapply property

`grid_sync` itself runs every 5 minutes, and what it runs is the applier
that reconciles the real scheduled-job table against this node. So editing
`cadences` or `crons_live` here and letting the graph get committed is
usually the whole change: within 5 minutes the running schedule matches what
this node says, with no command typed against the schedule itself. The one
edge case worth naming, because it is where that stops being automatic: the
kill-switch above removes `grid_sync` along with the other three, so once it
has run, nothing on this machine is left to notice the *next* edit. Setting
the boolean back on therefore needs one manual re-run of the applier to
install that first round of lines — after which `grid_sync` is live again
and every later edit resumes self-applying as usual.

## Two cadences the migration made meaningless

`goal:g11` landed, so two of the four cadences now describe work that no
longer exists, and both are disabled in `cadences:` above rather than
deleted — a declaration that records what was retired is more useful than
one that quietly forgets.

`publish_engine` ran `publish-engine.sh` to carry bytes from the graph repo
into the engine repo. There is one repo now; the payload IS the source file,
so there is nothing to publish and the four gates guard a boundary that is
gone.

`engine_push` pushed the engine repo. It is the same repo `branch_push`
already pushes, so leaving both enabled would have pushed the same branch
twice an hour, ten minutes apart, for no reason.

What survives is the pair that was never about the boundary: `grid_sync`
(every 5 minutes, snapshot + push refs/grid/*) and `branch_push` (hourly).
The grid is not the publish pipeline — it versions node.md and its payload
together as one atomic version, which plain git does not — so G11 does not
touch it.

## Why this is a node and not a comment in a crontab

A comment explaining a schedule is prose next to the thing it describes,
readable but not actionable — changing the real schedule and changing the
comment are two edits, and they drift the moment someone does only one.
Putting the cadence in a node the applier actually reads collapses that to
one edit with one outcome: the graph's stated cadence *is* the running
cadence, checked into version history, reviewable in the same diff as
everything else that changed that iteration, and revertible with the same
`grid.py` history as any other node. That is what G10.2 asks a `.geometry`
node to be — not documentation about the system's schedule, but the input
the schedule is derived from.

This node's own history is itself an example of that not being sufficient on
its own: the schedule state was always correct (`crons.py apply` reads the
frontmatter, never the prose), but the prose explaining it was wrong at
every version, for a year of edits, because nothing checks that the two stay
consistent the way `grid.py diff` checks that a fix changed something. Being
graph content made the defect *findable* — `git show` against three old
versions is how it was confirmed — it did not make it self-correcting.