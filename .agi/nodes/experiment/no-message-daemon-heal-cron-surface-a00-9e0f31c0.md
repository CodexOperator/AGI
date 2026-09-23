---
id: experiment:no-message-daemon-heal-cron-surface-a00-9e0f31c0
mint_id: 2978564bc0464684baa32135d318ff6d
type: experiment
parents:
  - hypothesis:a00-9e0f31c0-b143d1
next_edges: []
edited_by: a00-9e0f31c0
evidence_runs: experiment:no-message-daemon-heal-cron-surface-a00-9e0f31c0
line_ceiling: 40
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: bb4b7d319eb8a3af
season: 2
title: "Message transport is a one-shot send.py tick: heal/cron surface adds no new daemon for g7.31.4"
town: core
---
<!-- BODY:BEGIN -->
# experiment:no-message-daemon-heal-cron-surface-a00-9e0f31c0


## Experiment

Four-part test of C1 (falsifier 3 of `goal:g7.31.4`: no NEW message daemon /
router on the heal/cron surface for this goal). All commands read-only; no
production code changed. One durable guard test added
(`extensions/agi/tests/test_no_message_daemon.py`, tests are not production).

### 1. Enumerate the heal/cron surface, mechanically

`crons.py show` (run from the main checkout — the worktree refuses `show`/`audit`
by design, see Struggles), the only `send.py` occurrences in the whole rendered
crontab are the ONE-SHOT `nudge_sweep` tick:

```
$ cd /data/work/agi && python3 extensions/agi/bin/crons.py show | grep -nE 'send\.py|daemon|router|mail|nudge|wake'
12:  */2 * * * * cd /data/work/agi/.agi && python3 .../send.py wake --all-local >> .../agi-crons-agi-3fbc6951.log 2>&1
22:  */2 * * * * cd /data/work/agi/.agi && python3 .../send.py wake --all-local >> .../agi-crons-agi-3fbc6951.log 2>&1
project: /data/work/agi
crons_live: True
status: up to date
```

`crons.py audit` — the only units on this box not declared by the crons node
are dispatch/mur workflow units and desktop/claude-remote-control; none is a
message transport:

```
$ cd /data/work/agi && python3 extensions/agi/bin/crons.py audit
crons: audit found 9 undeclared item(s):
  unit: agi-belam-mur-dt65-lean.service (not declared by this node)
  ... (agi-belam-mur-*/agi-belam-dispatch-*/agi-helper-suite-seat/belam-desktop/claude-remote-control)
```

The declared persistent surface in `.agi/nodes/.geometry/crons.md`
(`services:` table) is exactly TWO units, neither a message transport:

```
services:
  agi-alarms-sanctuary-master:  exec_start: .../rotate.py alarms --holder sanctuary-master ...
  agi-reaper:                   exec_start: .../heal.py watch --root {repo_root} --poll-s 30
```

`KNOWN_JOBS` (`crons.py:92`) is
`("grid_sync", "branch_push", "publish_engine", "engine_push", "mail_poll", "nudge_sweep")`;
the generic `cmd` job path is `crons.py:616` (renders any declared `cmd`).
The live node declares no generic `cmd` job except `prime_merge`, whose command
is `test -f .../prime_merge.py && ... prime_merge.py tick` — a one-shot tick,
not a loop, and it names no message transport.

Live `systemctl --user` units matching `agi` (30 files) — the two declared
services plus dispatch/mur workflow units; the transport-word filter is empty:

```
$ systemctl --user list-unit-files --all | grep -iE 'message|router|mail|send|daemon|dispatcher'
(no output)
$ systemctl --user list-unit-files --all | grep -iE 'agi' | grep -E 'agi-(agi-reaper|agi-alarms)'
agi-agi-alarms-sanctuary-master-3fbc6951.service
agi-agi-reaper-3fbc6951.service
```

Live process table — the only long-running agi engine processes are the two
pre-existing services; the message transport is a TRANSIENT cron tick
(`send.py wake --all-local`, etimes 4 s at sample time, gone by the next):

```
$ ps -eo pid,ppid,etimes,args | grep -E 'extensions/agi/bin/(send|heal|crons|grid|rotate)\.py'
1038317 1417 32118  rotate.py alarms --holder sanctuary-master --root /data/work/agi/.agi
1038539 1417 32109  heal.py watch --root /data/work/agi --poll-s 30
2963853 2963850   4  send.py wake --all-local          <- one-shot cron tick, not resident
...
$ ps -eo pid,etimes,comm,args | awk '$3=="daemon" || $3 ~ /router/ || $3 ~ /message/'
(no output)
```

Daemon-construction primitives in the message transport's own bytes — the only
`while True` in `send.py` is a FILESYSTEM WALK (`_in_git_repo`, `send.py:3144`),
not a serve loop; `heal.py`'s loop is the pre-existing reaper service:

```
$ grep -nE 'fork|daemonize|setsid|serve_forever|socket\.|listen\(|while True' \
      extensions/agi/bin/send.py extensions/agi/bin/heal.py extensions/agi/bin/crons.py
extensions/agi/bin/send.py:3148:    while True:              # _in_git_repo walk, returns on .git
extensions/agi/bin/heal.py:1525:    while True:              # _watch: the agi-reaper service
extensions/agi/bin/crons.py:655-656: "Type=simple", "Restart=..."   # the unit RENDERER; the service table above is the only input
```

### 2. Classify every persistent hit before/after by git history

The goal boundary: `goal:g7.31.4` node minted 2026-09-21 04:09Z, falsifier
`.3` at 04:18Z. Every persistent service/cadence predates it:

```
$ git log -1 --format='%h %ci %s' f0f792479   # services: table + agi-reaper
f0f792479 2026-09-11 01:07:11 -0400 UNIT INSTALLED (Prime, merge-up 27 ...): cron:crons services table agi-reaper = heal.py watch ...
$ git log -1 --format='%h %ci %s' 41126d4a2   # mail_poll
41126d4a2 2026-09-18 18:49:34 -0400 ... SM.117b cells ... mail_poll on local-town
$ git log -1 --format='%h %ci %s' 2b0ea2284   # nudge_sweep
2b0ea2284 2026-09-18 22:10:32 -0400 cron:crons cadences.nudge_sweep (core-town, every 2 min): send.py wake per live post
$ git log --format='%h %ci %s' -- .agi/nodes/goal/g7.31.4.md | tail -1
86994e298 2026-09-21 04:09:56 +0000 mint goal:g7.31 umbrella + g7.31.1–.5 (grok-bot pane spine)
```

`agi-reaper` (2026-09-11) and `mail_poll`/`nudge_sweep` (2026-09-18) are
ancestors of HEAD and predate the goal — pre-existing, by name and date, not
new. `agi-reaper` is the round reaper (`heal.py watch`), `agi-alarms` is
`rotate.py alarms`; neither routes messages. No service/cadence line was added
at or after 2026-09-21.

### 3. Wire probe — the transport needs no daemon

`send.py`'s real path with the tmux seam faked (the model of
`experiment:send-surface-ssh-or-not-a00-dd757e64`); no message-daemon process
was live at any point (the `ps` sample above shows none):

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q \
    -k test_real_path_refuses_foreign_box_and_reaches_local
1 passed, 6 deselected in 12.58s
```

That test drives real `send_dm` -> real `_nudge_window` -> real `_nudge_target`
(stubbing only tmux/capture): the dm record lands in the recipient inbox
(`_conv_blocks` reads it back), the local peer's pane nudge is typed, the
foreign-box peer is refused by name with zero keystrokes. No daemon exists to
route it.

### 4. Negative control — the detection is not vacuous

Durable guard `extensions/agi/tests/test_no_message_daemon.py` scans the LIVE
surface (the crons node's `services:` + the lines `render_managed_lines`
actually emits + the declared generic `cmd` jobs) and `send.py`'s bytes. It
flags a line only when it is BOTH a message transport (`send.py|router|
message|mail`) AND persistent (`--poll|--serve|--daemon|serve_forever|setsid|
while True|Restart=`), and it asserts the scan FIRES on a synthetic service row
and on a synthetic generated `cmd` job rendered through the real renderer:

```
$ python3 -m pytest extensions/agi/tests/test_no_message_daemon.py -q
3 passed in 22.27s
```

The negative control is the near-miss rule-out: the live surface legitimately
names `send.py` twice (`read --box-local`, `wake --all-local`); a scan that
flagged any `send.py` would be wrong, and a scan that returned nothing because
it keyed the wrong word would certify nothing. Synthetic state was in-memory
only (a dict handed to `render_managed_lines`); nothing was installed or
reverted on disk.

## Evidence

All transcripts inline above; no session file is leaned on. Conclusion: C1
holds on the built bytes — the surface declares two pre-existing persistent
services (reaper, alarms), none a message transport, and every message path is
a one-shot `send.py` tick plus a file inbox.

- Guard test: `extensions/agi/tests/test_no_message_daemon.py` (3 tests,
  production lines 0 — tests are excluded from the ceiling).
- Wire probe: `test_send_surface_ssh_or_not.py::test_real_path_refuses_foreign_box_and_reaches_local`.
- Production paths changed: NONE.
## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Measured the live surface and dated every persistent service/cadence to commits that predate the goal mint (f0f792479 2026-09-11, 41126d4a2 / 2b0ea2284 2026-09-18 vs goal mint 2026-09-21). Added a durable guard test with a real negative control rather than leaving production_lines at zero with nothing that fails if a daemon is ever added.
<!-- THOUGHT:END -->
