---
id: goal:g1.5
mint_id: 67a1f5899e6243c6ac470ca5d2a8e758
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.5
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G1.5: `init` leaves nothing to install by hand"
---
**Setting up a project is currently two manual steps and a memory test.** The
cron half of this is now largely satisfied; the other two are not:

- `grid.py init` — adds the `refs/grid/*` fetch refspec to origin. Skip it and a
  fresh clone silently has no version history; nothing warns, the grid is simply
  absent. **Not done.**
- Cron setup — was `grid.py cron install`, the two-cadence sync (5-minute
  snapshot + grid push, hourly D1 push); that subcommand is retired in
  practice on this project. `bin/crons.py apply` now renders a single managed
  crontab block from `nodes/.geometry/crons.md` (**G10.2**), and the S2
  branch-verification requirement below is implemented, not merely demanded.
  What is still missing is the *init* half: nothing yet calls `crons.py apply`
  as part of bringing a fresh project up, so a new clone still needs someone to
  remember to run it once.
- The project scaffold itself — `agi-tree.config.json`, `nodes/`, `context/` —
  is **L18 action 2** and does not exist at all. `cli.py scaffold` scaffolds a
  node, not a project. **Not done.**

This is G1's invariant failing on G1's own setup path: repeated mechanical
steps, most of them still not a named command, none carrying a written reason
for staying manual. The failure mode is silent in both directions — an
uninitialised grid and an unapplied cron declaration both look exactly like a
working project until the day you need the history.

What has to exist: one command that takes a directory to a running project —
config written from a schema (**L17**) rather than by hand, `nodes/` and
`context/` scaffolded, grid refspec configured, `crons.py apply` run, and the
whole thing idempotent so re-running it on a live project is safe and does
nothing.

**Verify the cron the way S2 had to be verified — now actually implemented.**
`bin/crons.py` re-resolves the branch via `git symbolic-ref` on every apply,
rather than capturing it once at install time, because agi-tree's own work
once sat on a stale `iter24-extend-300hop` branch while a cron pushed `master`
and published nothing, silently, indefinitely. Because the `*/5` job re-runs
`crons.py apply`, that check now happens every 5 minutes rather than once at
install, and `crons_live: false` in the node is a single-edit kill switch. This
clause of the goal is satisfied; `init` and scaffolding are not.

Pairs with **G8.1** — whatever the distribution shape turns out to be
(drop-in clone, skill package, installer), this is the command it has to end in.

Falsifier: clone the repo to an empty machine, run the one command, and check
that `git fetch` brings the grid down and the crontab shows the managed
`agi-crons` block with all four jobs. If either needs a second command, this
is not done.

## Agent Notes
L1.09 (2026-09-03): the cavekit build-site's `hyp:graph-core-r10` -- one command that turns an empty directory into a valid graph root (skeleton, a minimal example node and schema, idempotent re-run, one summary of created paths) -- is the scaffolding half this goal already owes; recorded here rather than as a new goal, and the hypothesis is deprecated with its cohort (goal:s18).