---
id: cron:crons
mint_id: dc4da698f3f94dbc83a0c2233b2a8b94
type: cron
parents:
  - goal:g2.25
cadences:
  grid_sync:
    every_mins: 5
    enabled: true
    mirror_towns: true
  crons_apply:
    every_mins: 5
    enabled: true
    cmd: python3 {repo_root}/extensions/agi/bin/crons.py apply --unit-dir $HOME/.config/systemd/user
  branch_push:
    schedule: 7 * * * *
    enabled: true
  mail_poll:
    every_mins: 5
    enabled: true
    box: local-town
    why_box: "the remote-box reader: mail_poll consumes inboxes fetched from the hub"
    cmd: git -C {repo_root} fetch -q origin && python3 {engine_root}/extensions/agi/bin/send.py read --box-local --peek >> {log} 2>&1; python3 {engine_root}/extensions/agi/bin/rotate.py migrate --receive >> {log} 2>&1
  engine_push:
    schedule: 47 * * * *
    enabled: false
  nudge_sweep:
    every_mins: 2
    enabled: true
  maint_gc:
    schedule: 41 4 * * *
    enabled: true
    box: local-town
    why_box: the object store is the local box's; gc on any other box would repack a store this job does not own
    cmd: git -C {repo_root} gc --quiet
  prime_merge:
    schedule: 13 */4 * * *
    enabled: true
    box: local-town
    why_box: the Prime's town->season2/main merge routine runs where the Prime and the town trunk live (owner 01:2xZ 09-21, goal:g5; every 4 hours, owner 09-23 15:0xZ); inert until extensions/agi/bin/prime_merge.py lands (director-engine round)
    cmd: test -f {repo_root}/extensions/agi/bin/prime_merge.py && PI_BIN=$HOME/.npm-global/bin/pi python3 {repo_root}/extensions/agi/bin/prime_merge.py tick --root {root}
  graph_metrics:
    schedule: 23 * * * *
    enabled: true
    box: local-town
    why_box: "belam's crontab reads every uid's files and writes the town node; a v5 uid reads only its own (goal:g3.8, AA1.S)"
    cmd: python3 {repo_root}/extensions/agi/bin/metrics_cell.py {root} town:local-maxxing metrics_line --actor belam -- python3 {repo_root}/extensions/agi/bin/success_metrics.py --line {root}
  memory_alarm:
    every_mins: 1
    enabled: true
    box: local-town
    why_box: "reads this box's own /proc and user@ cgroup (OWNER 04:0xZ 09-26, after the 03:20Z memory livelock: raise a climb toward exhaustion before the box wedges); every threshold lives here, none in code"
    cmd: python3 {repo_root}/extensions/agi/bin/memory_alarm.py --root {root} --warn-avail-mib 2048 --crit-avail-mib 1024 --warn-psi-some-avg60 10 --crit-psi-full-avg60 20 --warn-cgroup-max-frac 0.95 --repeat-mins 15 --notify belam
  memory_alarm_posts:
    every_mins: 1
    enabled: true
    box: local-town
    why_box: same reader as memory_alarm, pointed at the SYSTEM agi.slice where the pi-engine posts (agi-post@*) live; reads this box's cgroup, so it runs on this box only (stage-2.5 rootplan C3, parity row 45)
    cmd: python3 {repo_root}/extensions/agi/bin/memory_alarm.py --root {root} --warn-avail-mib 2048 --crit-avail-mib 1024 --warn-psi-some-avg60 10 --crit-psi-full-avg60 20 --warn-cgroup-max-frac 0.95 --repeat-mins 15 --notify belam --cgroup /sys/fs/cgroup/agi.slice --state {root}/sessions/memory-alarm-posts.json
crons_live: true
edited_by: a00-b465ec27
season: 1
services:
  agi-alarms-sanctuary-master:
    enabled: true
    exec_start: /usr/bin/python3 {repo_root}/extensions/agi/bin/rotate.py alarms --holder sanctuary-master --root {root}
    restart: on-failure
    working_directory: "{repo_root}"
  agi-reaper:
    enabled: true
    exec_start: /usr/bin/python3 {repo_root}/extensions/agi/bin/heal.py watch --root {repo_root} --poll-s 30
    restart: on-failure
    working_directory: "{repo_root}"
    environment:
      AGI_REAPER_LOG: "{logs}/agi-reaper-agi-2f118e6f.log"
status: active
tags:
  - geometry
  - cron
  - structural
thought_session: season
title: Cron cadence declaration
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g7.16.1.11.13 E2a (hypothesis g716111-aa3-the-crontab-applier-survives-grid-syncs-retirement, V3; DG1 cut, belam [rule] 05:1xZ 10-08, SM RE5/RE6): this version adds ONE cell, `cadences.crons_apply` (every_mins 5, enabled, NO `box` and so no `why_box`, cmd `crons.py apply --unit-dir $HOME/.config/systemd/user`), so the crontab self-heal no longer lives only in the tail of grid_sync's line and retiring grid_sync cannot lose it. It is boxless on purpose: it renders on every box, AGI_BOX unset included. grid_sync's own apply step STAYS until the switch round (E2b0 and after), so there is no gap. The 'self-reapply property' prose now names crons_apply instead of grid_sync as what runs the applier. The earlier thought (goal:g7.16.1.4.1.2: only engine_push still carries an enabled of its own, publish_engine is gone) is unchanged and lives in the body's kill-switch paragraph. Builder: director-general-3 (DG4 silent, DG1 08:32Z).
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
a change to where things live on disk while four crons (then) independently
read and wrote that same disk on their own timers. `grid_sync` snapshotting
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
installed (today: `grid_sync`, `branch_push` and the bounded-footprint jobs
named at the end of this body; `engine_push` stays out regardless,
because its own `enabled` is `false`, and `publish_engine` no longer exists —
its cadence was removed with publish-engine.sh (goal:g7.16.1.4.1.1);
see "Two cadences the migration made meaningless" below). This is the
opposite of the previous section: `false` overrides every job's own flag to
off, `true` defers to each job's own flag.

## The self-reapply property

`crons_apply` runs every 5 minutes, and what it runs is the applier
(`crons.py apply`) that reconciles the real scheduled-job table against this
node. It is a cadence of its own, with no `box` key (so no `why_box`): it
renders on every box, and retiring `grid_sync` no longer takes the self-heal
with it. `grid_sync`'s own last step still runs the same applier until the
switch round removes it. So editing
`cadences` or `crons_live` here and letting the graph get committed is
usually the whole change: within 5 minutes the running schedule matches what
this node says, with no command typed against the schedule itself. The one
edge case worth naming, because it is where that stops being automatic: the
kill-switch above removes `crons_apply` and `grid_sync` along with the other
jobs, so once it has run, nothing on this machine is left to notice the *next*
edit. Setting the boolean back on therefore needs one manual re-run of the
applier to install that first round of lines — after which `crons_apply` is
live again and every later edit resumes self-applying as usual.

## Two cadences the migration made meaningless

`goal:g11` landed, so two of the four cadences now describe work that no
longer exists. `engine_push` stays disabled in `cadences:` above rather than
deleted — a declaration that records what was retired is more useful than
one that quietly forgets.

`publish_engine` ran `publish-engine.sh` to carry bytes from the graph repo
into the engine repo. There is one repo now; the payload IS the source file,
so there is nothing to publish and the four gates guard a boundary that is gone. Its cadence and the script itself were removed by goal:g7.16.1.4.1.1 (this node grid history keeps the declaration).

`engine_push` pushed the engine repo. It is the same repo `branch_push`
already pushes, so leaving both enabled would have pushed the same branch
twice an hour, ten minutes apart, for no reason.

What survives is the pair that was never about the boundary: `grid_sync`
(every 5 minutes, snapshot + push refs/grid/*) and `branch_push` (hourly).
The grid is not the publish pipeline — it versions node.md and its payload
together as one atomic version, which plain git does not — so G11 does not
touch it.

## The two bounded-footprint jobs (conjuncts 1 and 2)

`maint_gc` is the DECLARED object-store maintenance. It exists because the
grid versions through plumbing, which never runs `gc --auto`, so nothing
repacked `.git/objects` on its own — the store grew until a human ran one
`git gc` by hand. Cadence, box scope and the command are all declared in
this node's `cadences:`, not written into `crons.py`.

Conjunct (2) — every file in the logs dir under a declared cap with a
declared number of rotations — is not a cron line at all but two config
cells, `logs.cap_mb` and `logs.rotations` in `.agi/config.json`, enforced by
`crons.py` on every apply. The cron log and the reaper log share one cap.

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
