---
confidence: 1.0
goal_id: G1.5
goal_kind: subgoal
id: "goal:g1.5"
origin: goals-doc
parents:
  - goal:g1
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G1.5: `init` leaves nothing to install by hand"
type: goal
---

**Setting up a project is currently three manual steps and a memory test.** The
commands all exist and none of them are called by anything:

- `grid.py init` — adds the `refs/grid/*` fetch refspec to origin. Skip it and a
  fresh clone silently has no version history; nothing warns, the grid is simply
  absent.
- `grid.py cron install` — the two-cadence sync (5-minute snapshot + grid push,
  hourly D1 push). Skip it and the crash-recovery window is not ≤5 minutes, it
  is however long since someone last remembered.
- The project scaffold itself — `agi-tree.config.json`, `nodes/`, `context/` —
  is **L18 action 2** and does not exist at all. `cli.py scaffold` scaffolds a
  node, not a project.

This is G1's invariant failing on G1's own setup path: three repeated mechanical
steps, none of them a named command, none carrying a written reason for staying
manual. The failure mode is silent in both directions — an uninitialised grid
and an uninstalled cron both look exactly like a working project until the day
you need the history.

What has to exist: one command that takes a directory to a running project —
config written from a schema (**L17**) rather than by hand, `nodes/` and
`context/` scaffolded, grid refspec configured, crons installed, and the whole
thing idempotent so re-running it on a live project is safe and does nothing.

**Verify the cron the way S2 had to be verified.** `grid.py cron install` must
confirm which branch is actually checked out, because agi-tree's own work once
sat on a stale `iter24-extend-300hop` branch while a cron pushed `master` and
published nothing, silently, indefinitely. An installer that writes a crontab
line without that check just automates the same failure faster.

Pairs with **G8.1** — whatever the distribution shape turns out to be
(drop-in clone, skill package, installer), this is the command it has to end in.

Falsifier: clone the repo to an empty machine, run the one command, and check
that `git fetch` brings the grid down and `crontab -l` shows both cadences. If
either needs a second command, this is not done.
