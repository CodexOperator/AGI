---
cadences:
  grid_sync: {every_mins: 5, enabled: true}
  branch_push: {schedule: "7 * * * *", enabled: true}
  publish_engine: {schedule: "37 * * * *", enabled: false}
  engine_push: {schedule: "47 * * * *", enabled: false}
crons_live: true
id: "cron:crons"
mint_id: dc4da698f3f94dbc83a0c2233b2a8b94
parents:
  - goal:g10.2
status: active
tags:
  - geometry
  - cron
  - structural
title: "Cron cadence declaration"
type: cron
---

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g11 landed, so two of the four cadences now describe work that no longer
exists, and both are disabled rather than deleted — a declaration that records
what was retired is more useful than one that quietly forgets.

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

Turning these off is a two-line edit to a node, applied within five minutes by
the job that re-reads this file. That is the property this node was created
for, used for the first time on a real change.
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

## `crons_live: true` is the kill-switch for the goal:g11 repo migration

`goal:g11` moves the graph inside the repo it builds — a change to where
things live on disk while four crons are independently reading and writing
that same disk on their own timers. `grid_sync` snapshotting mid-move,
`branch_push` pushing a half-moved branch, `publish_engine` publishing
against a graph commit that the move has not settled yet, `engine_push`
committing an engine tree mid-shuffle — any one of the four racing the move
is a way to corrupt it. `crons_live: true` is the single flip that removes
every managed line at once, so the migration can run with nothing else
touching the tree, and `crons_live: true` is the equally single flip that
brings all four back when it is safe. One boolean rather than four
independent toggles is what makes "is it safe to move yet" a single fact
instead of a four-way coincidence to verify by hand.

## The self-reapply property

`grid_sync` itself runs every 5 minutes, and what it runs is the applier
that reconciles the real scheduled-job table against this node. So editing
`cadences` or `crons_live` here and letting the graph get committed is the
whole change: within 5 minutes the running schedule matches what this node
says, with no command typed against the schedule itself. The one edge case
worth naming is `crons_live: true` — the job that would re-apply the new
state is itself one of the four lines removed, so turning cadences back on
takes one manual re-run of the applier once, not a wait for a cadence that
no longer exists.

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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 minted this node parentless and added `cron` to `[shape].md :: parentless_types`
alongside `goal:long-term`, `goal:short-term` and `idea` — treating "describes the
graph's own shape" as equivalent to "has no lineage." That conflated two different
claims. `idea` and the two goal roots are parentless because there is genuinely
nothing upstream of them in the content graph. This node is not like that: it
exists *because* `goal:g10.2` ("The graph describes its own geometry") asks for
`.geometry/` nodes to exist and says plainly that such a node is "subject to
every rule other nodes obey." Declaring it parentless was declaring it exempt from
the one rule (has-a-parent) that G10.2 itself insists still applies. v2 sets
`parents: [goal:g10.2]` — the goal that made this node necessary is its parent,
the same way any other node's parent is the thing that motivated it. This also
means the node now participates in chain depth and `outcome_coverage` like any
other node, which is what "subject to every rule" actually requires rather than
a stated intention.
<!-- THOUGHT:END -->
