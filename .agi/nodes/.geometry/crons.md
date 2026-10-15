---
id: cron:crons
mint_id: dc4da698f3f94dbc83a0c2233b2a8b94
type: cron
parents:
  - goal:g2.25
cadences:
  grid_sync:
    every_mins: 30
    enabled: true
  town_mirror:
    every_mins: 5
    enabled: true
  evidence_enforce:
    every_mins: 30
    enabled: false
    box: encryption-town
    why_box: "edits node files on MAIN, and MAIN lives on encryption-town (local-town is parked, owner 04:2xZ 10-09; belam decision 19:5xZ 10-09): evidence_gate demotes an unbacked verdict in place; the grid_sync commit step used to run it, so grid_sync off would stop it (goal:g7.16.1.11.13.1)"
    cmd: python3 {repo_root}/extensions/agi/bin/evidence_gate.py enforce --root {root}
  crons_apply:
    every_mins: 5
    enabled: true
    cmd: python3 {repo_root}/extensions/agi/bin/crons.py apply --unit-dir $HOME/.config/systemd/user
  branch_push:
    schedule: 7 * * * *
    enabled: false
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
    enabled: false
  maint_gc:
    schedule: 41 4 * * *
    enabled: true
    box: encryption-town
    why_box: the object store is encryption-town's (MAIN moved there 10-09); gc on any other box would repack a store this job does not own
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
    box: encryption-town
    why_box: "belam's crontab reads every uid's files and writes the town node; a v5 uid reads only its own (goal:g3.8, AA1.S)"
    user: agi-belam
    why_user: "goal:g7.16.1.11.42 option E (belam 15:1xZ 10-11, council 3/3 15:07Z): the board commit is made in the Prime's OWN uid, the hand agi-at and agi-turn already sign with (agi-belam's git signs every commit, committer belam@agi), on posts/belam in a job-owned clone, never ~/t; uid belam keeps only graph_metrics_land, an ff that makes no commit. crons.py apply installs this line through `crontab -u agi-belam` (apply --sudo)"
    log: ~/logs/board_job.log
    cmd: python3 {repo_root}/extensions/agi/bin/board_job.py commit --main {repo_root} --post belam --job metrics_cell --work ~/board-work -- python3 {repo_root}/extensions/agi/bin/metrics_cell.py @WROOT@ town:local-maxxing metrics_line --actor belam -- python3 {repo_root}/extensions/agi/bin/success_metrics.py --line {root}
  graph_metrics_land:
    schedule: 28 * * * *
    enabled: false
    box: encryption-town
    why_box: "MAIN lives on encryption-town; this is uid belam's ONE step of the board job: git merge --ff-only posts/belam into MAIN, only when every commit in MAIN..posts/belam is the job's own (goal:g7.16.1.11.42 C6); it makes no commit"
    cmd: python3 {repo_root}/extensions/agi/bin/board_job.py land --main {repo_root} --post belam
  memory_alarm:
    every_mins: 1
    enabled: true
    box: encryption-town
    user: agi-belam
    why_box: "reads this box's own /proc and user@ cgroup (OWNER 04:0xZ 09-26, after the 03:20Z memory livelock: raise a climb toward exhaustion before the box wedges); every threshold lives here, none in code"
    cmd: python3 {repo_root}/extensions/agi/bin/memory_alarm.py --root {root} --warn-avail-mib 2048 --crit-avail-mib 1024 --warn-psi-some-avg60 30 --crit-psi-full-avg60 20 --warn-cgroup-max-frac 0.95 --warn-slab-mib 1536 --repeat-mins 15 --clear-margin-frac 0.8 --clear-hold-mins 3
  memory_alarm_posts:
    every_mins: 1
    enabled: true
    box: encryption-town
    user: agi-sanctuary-master
    why_box: same reader as memory_alarm, pointed at the SYSTEM agi.slice where the pi-engine posts (agi-post@*) live; reads this box's cgroup, so it runs on this box only (stage-2.5 rootplan C3, parity row 45). It OWNS the alarm to belam (goal g7.16.1.11.20.2, ONE SPOOL PER SENDING SEAT, it only appends a line to sanctuary-master's spool, and the alarm_drain row below signs and box-sends it; sanctuary-master is the sender because box refuses self-mail and belam is adjacent only to the level below) and the user@ job above passes no box flags, so one alarm is one message
    cmd: python3 {repo_root}/extensions/agi/bin/memory_alarm.py --root {root} --warn-avail-mib 2048 --crit-avail-mib 1024 --warn-psi-some-avg60 30 --crit-psi-full-avg60 20 --warn-cgroup-max-frac 0.95 --warn-slab-mib 1536 --repeat-mins 15 --clear-margin-frac 0.8 --clear-hold-mins 3 --alarm-seat sanctuary-master --alarm-to belam --alarm-job memory_alarm_posts --alarm-spool-max 500 --cgroup /sys/fs/cgroup/agi.slice --state {root}/sessions/memory-alarm-posts.json
  alarm_drain:
    every_mins: 1
    enabled: true
    box: encryption-town
    user: agi-sanctuary-master
    why_box: the SENDING seat's drain (goal g7.16.1.11.20.2 council 3/3 21:3xZ, one spool per sending seat) runs in sanctuary-master's own uid on the box where its post tree and its key live, so the seat's key signs and root signs nothing; it box-sends every line of the seat's ~/alarm.spool exactly once (an Alarm-id trailer is searched in the seat's own out-ref before each send), and a send that fails stays spooled with one notice line
    cmd: python3 {repo_root}/extensions/agi/bin/alarm_spool.py drain --seat sanctuary-master --max-tries 60
  alarm_drain_belam:
    every_mins: 1
    enabled: true
    box: encryption-town
    user: agi-belam
    why_box: the SENDING seat's drain for belam's spool (goal g7.16.1.11.20.2 council 3/3 21:3xZ, one spool per sending seat) runs in belam's own uid on the box where its post tree and key live; the root agi-quiet-watch unit only appends a plain line to belam's ~/alarm.spool and never signs, this row signs and box-sends it to sanctuary-master (belam to SM is inside the matrix) exactly once
    cmd: python3 {repo_root}/extensions/agi/bin/alarm_spool.py drain --seat belam --max-tries 60
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
goal:g7.16.1.11.20.2 C1 (owner 21:1xZ-21:2xZ 10-11 via belam: "Pressure alarm should use new mail system also" · "All alarms"; SM 21:30Z, council 3/3 A-AMENDED: ONE SPOOL PER SENDING SEAT, a seat's key signs only in the seat's own uid): memory_alarm_posts runs as `user: agi-sanctuary-master` and passes `--alarm-seat sanctuary-master --alarm-to belam --alarm-job memory_alarm_posts --alarm-spool-max 500` instead of `--notify belam`: it only APPENDS a plain line to sanctuary-master's spool (no key, no box). The new row `alarm_drain` (every minute, user agi-sanctuary-master) runs `alarm_spool.py drain` in that uid: the seat's own key signs `box send belam` (subject `[alarm <job>]`, trailers Alarm-job and Alarm-id), exactly once, a failed send stays spooled with a ~/.notice line. WHY SM sends: box refuses self-mail and mails only adjacent levels, so belam can be mailed only by the post one level below; sender and reader are the two cells on the posts row and the seat on the drain row (a council flip is those lines). The user@ row stays agi-belam: it reads the cgroup of the uid it runs as and sends nothing. nudge_sweep (`send.py wake --all-local`, the old nudge retry) is now enabled: false: nothing has written the old inbox/comms/room paths since 10-09 and agi-boxwake@ wakes on box mail; belam's sweep-log check rides SM's digest. SLAB (goal:g7.16.1.11.40.1.1 target 3b, council 3/3 23:32Z): both memory_alarm rows gain `--warn-slab-mib 1536` and a cgroup's kernel slab (memory.stat) at or over it WARNs by name through the same spool path, repeat 15 min, cleared below 0.8 of it after the hold; NO drop is taken (drop_caches is the box owner's). 1536 MiB is 30 percent of agi.slice's memory.high (5120): above the post-drop baseline (130 MiB, a normal working set sits well under 500) and well below tonight's 2713, so it fires with the slice still ~2 GB short of MemoryHigh, not at it. Both drain rows carry `--max-tries 60` (a cell, none in code): an hour of failed minute passes dead-letters the line to alarm.spool.dead with ONE ~/.notice line, so an unreachable reader never holds the spool or a retry for ever. C2 adds `alarm_drain_belam` (user agi-belam, every minute): agi-quiet-watch (root) no longer signs; it appends ONE plain line to belam's spool by runuser, and this row signs and box-sends it to sanctuary-master as belam. Previous version's thought: goal:g7.16.1.11.20.2 TARGET 4 (belam 20:0xZ 10-11, DG1): both memory_alarm rows gain `--clear-margin-frac 0.8 --clear-hold-mins 3`. Why: the alarm FLAPPED (WARN 20:02:01Z -> CLEARED 20:03:02Z, WARN 20:04:02Z -> CLEARED 20:06:01Z, WARN 20:15:02Z at 10.8 against a line of 10): it cleared on the FIRST tick whose reading fell under the SAME line it raised at, and avg60 hovering at that line raises and clears every few minutes. A raised alarm is now held against a CLEAR line (PSI and cgroup-fill lines x 0.8: some avg60 10 -> 8; MemAvailable lines / 0.8: 2048 -> 2560 MiB) and clears only after 3 minutes below it, unbroken (any tick back over the line restarts the hold). Both values live here, none in code; margin 1 / hold 0 restores the old first-tick clear. Previous version's thought: goal:g7.16.1.11.13.1 (DG1 order 17:22Z, rows test_crons_flip_successors.py c3a114bd3a by DG2; re-cut 10-10 on the trunk 38e1270456 with SM's 21:4xZ A1-A4): turning `grid_sync.enabled` false must stop ONLY the grid, but two things rode on its cron line: (1) the on-disk evidence demotion (the grid_sync commit step ran the on-disk evidence gate) and (2) the town MIRROR (`mirror_towns: true` on the grid_sync cell). This version gives each a job of its own: `evidence_enforce` (every 30, box encryption-town because it edits node files on MAIN and MAIN lives there; a generic `cmd` cell: `evidence_gate.py enforce --root {root}`, the GRAPH root) and `town_mirror` (every 5, any box, a KNOWN job: crons.py renders one guarded push per declared town, byte for byte as before). `mirror_towns` is gone from the grid_sync cell and crons.py REFUSES a node that still carries it, by name (ignoring it would lose the mirror silently). Neither new job names grid.py, so the E2b0 writer list does not move. grid_sync's own line is unchanged. CADENCE 30, not 5 (A1, SM measured: one dry pass over MAIN = 134 s at load 8 and can pass 300 s at E's throttled load 16-50; overlapping runs are two writers on MAIN's node files plus heat, the pathology belam cut for grid_sync 5 -> 30): the lock is INSIDE `evidence_gate.py enforce` (a non-blocking flock, a held lock prints one `[busy]` line, rc 0), so the cron AND the manual verb both refuse to overlap. The build around the cells: `evidence_gate.py enforce` keeps the suite-lock deferral the grid_sync commit step had (a live foreign pid defers the tick, rc 0, nothing rewritten; it commits NOTHING: an in-place edit the next by-path commit versions); the three migrate verbs refuse `--write` by name while grid_sync is retired; with grid_sync retired the rendered mail_poll line fetches `+refs/heads/*:refs/remotes/origin/*` only, because a plain `fetch origin` also fetched the clone's grid refspec; grid_retired() is SILENT for a project with no crons node and NAMES an invalid one. Builder: director-general-3. Previous version's thought: belam-s2-I 20:0xZ 10-09: grid_sync every 5 -> 30 min. MEASURED on encryption-town: one `grid.py commit --all` run takes > 6 min (only 6 completions logged all day), so the */5 runs overlapped and queued on .grid.lock, holding a core at ~20% non-stop while the CPU package sat at 91°C with 153 powerclamp idle injections (thermal throttling). Grid commit is being retired (owner 01:3xZ 10-08: "We don't need the grid commit work we're retiring grid commit"); a slower cadence loses no version (each run versions everything changed since the last). Previous version's thought: belam-s2-I 19:4xZ 10-09: box local-town -> encryption-town for maint_gc, graph_metrics, memory_alarm, memory_alarm_posts. Why: MAIN, the Prime and every post moved to encryption-town 10-08/09 and the owner parked local-town ("Local town will remain down for the foreseeable future", 04:2xZ 10-09), so _on_this_box refused all four and E had no memory alarm, no hourly metrics line and no gc. Kept on local-town (= off): mail_poll (the hub reader; owner 04:0xZ: "Hub is old design") and prime_merge (the Prime's session CHECK covers it; the cron would start a PASS unattended). Previous version's thought: goal:g7.16.1.11.13 E2a (hypothesis g716111-aa3-the-crontab-applier-survives-grid-syncs-retirement, V3; DG1 cut, belam [rule] 05:1xZ 10-08, SM RE5/RE6): this version adds ONE cell, `cadences.crons_apply` (every_mins 5, enabled, NO `box` and so no `why_box`, cmd `crons.py apply --unit-dir $HOME/.config/systemd/user`), so the crontab self-heal no longer lives only in the tail of grid_sync's line and retiring grid_sync cannot lose it. It is boxless on purpose: it renders on every box, AGI_BOX unset included. grid_sync's own apply step STAYS until the switch round (E2b0 and after), so there is no gap. The 'self-reapply property' prose now names crons_apply instead of grid_sync as what runs the applier. The earlier thought (goal:g7.16.1.4.1.2: only engine_push still carries an enabled of its own, publish_engine is gone) is unchanged and lives in the body's kill-switch paragraph. Builder: director-general-3 (DG4 silent, DG1 08:32Z).
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
