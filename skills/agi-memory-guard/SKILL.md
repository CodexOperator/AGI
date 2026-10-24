---
name: agi-memory-guard
description: >
  Read, find, stop and free on the shared box without making it worse: memory, io, disk and load
  readings in one unit, finding a process by comm + cwd (never argv), orphan and stage scopes,
  stopping a round so nothing relaunches or keeps billing, freeing disk on the RIGHT mount, and
  what never to print while doing it. Use whenever a post checks box pressure, gates a round on
  memory / io / disk, stops a runaway or orphan, or frees space.
---

# agi-memory-guard — the box is shared: measure, then touch

Source of truth for thresholds: the config cells (`values.local_maxxing.*`, `spawn.memory_max`) and
`/var/log/agi-memguard.log` — never a number from memory. Owner 2026-09-27 19:22Z: the traps live here, not on cards.

## 1 · Read the box — one pass, named fields only
| axis | read | never |
|---|---|---|
| memory | `/proc/meminfo` MemAvailable · `/proc/pressure/memory` · `user@<uid>.service/memory.current` vs `memory.high` | quote a swarm's min without `/var/log/agi-memguard.log` (SPIKE / SUSPENDED lines are the truth) |
| slab | `agi.slice/memory.stat` slab + slab_reclaimable vs `memory.current` and `memory.high` | gate on anon+shmem alone: a slice AT MemoryHigh with small anon = kernel slab (dentry/inode cache from file walks), reclaim swaps the posts' anon; MemAvailable box-wide stays high (belam 23:1xZ 10-11: 5104/5120 MiB, anon 1638, slab 2713; goal:g7.16.1.11.40.1.1) |
| io | `/proc/pressure/io` avg60 · `/proc/diskstats` inflight · `Writeback` in meminfo | read io off memory PSI (2 % memory while io ~88 %) |
| disk | `df -B1M <the exact path>` FIRST | assume one fs: `/` (`/tmp`, `/home`) and `/data` (repo, every worktree) are DIFFERENT |
| load | `/proc/loadavg` field 1 | gate on load alone: a dispatch gate is load1 AND io avg60 AND (disk free, key cap x live < balance) |
| load, hot box | `thermal_zone` temp WITH loadavg | read load alone on E: powerclamp idle injection inflates it (91C, load 16-50, belam 10-10); count `ps -C dbus-daemon` per user (the reaper keeps it low); one heavy lane at a time |

UNITS: every cgroup number in MiB = bytes / 1048576. A figure ~4.9 % above its own row is MB mislabelled.
VmHWM includes file-backed pages (torch libs, the safetensors mmap) the cgroup books as cache: read VmHWM AND the
hard rise; before claiming a kill frees MiB, read the scope's `memory.stat` anon vs file.
A cgroup `file` figure can be SHMEM (a RAM disk) that reclaim cannot free: read `memory.stat` shmem before calling file pages
reclaimable (DG4; `heal.py` now nets shmem out).

## 2 · Find the process — comm + cwd, never argv
```
for p in /proc/[0-9]*: comm · readlink cwd · PPid · State · /proc/<p>/io rchar/wchar · etime
scopes: /sys/fs/cgroup/user.slice/user-<uid>.slice/user@<uid>.service/app.slice/run-*.scope/cgroup.procs
```
| shape | means |
|---|---|
| PPid = systemd, the tool call that started it is gone | an ORPHAN (a recursive grep over MAIN read 25.7 GB in D state for 4 h) |
| a lone `pi` in its own `run-*.scope`, cwd a director worktree | a workflow STAGE — it outlives its runner unit and keeps billing its key |
| a sampler / relaunch in a round worktree after the round stopped | it OUTLIVES the stop (ppid 1, appends per sample, no fd held) |
| a seat's cgroup | per PROCESS (`/proc/<pid>/cgroup`): a heal respawn can land in `session-N.scope`, outside user@'s cap |

One exception, the guard (`agi-memguard`, goal:g7.16.1.11.40.1): it reads a post unit's argv only as the exact tail equality between that unit's tracer and its child, to tell the harness from its tools; never a pattern, never printed.

`pgrep -f <pattern>` matches the waiter's own argv and the claude processes' prompts: a loop on it never ends.
Wait on a PID found by comm + cwd.
`pkill -f <script>` is the same trap (it matches your OWN command line and kills the shell): `pgrep -x sh -a`, kill by pid (DG4). A background runner that waits on MemAvailable must STOP, not run anyway, when the wait ends: it was about to run beside the gate (DG4, 09:33Z).
Find by `pgrep -x <comm>` (+ cwd), never `-f`. A test that kills its own sleeps starts them under `setsid` and kills with `pkill -g <its own pgid>` (DG1 gen 23).

## 3 · Stop — nothing relaunches, nothing keeps billing
```
systemctl --user stop run-<id>.scope   (the runner unit AND every stage scope whose members' cwd is the round's)
 ─▶ re-list by cwd in the round's worktrees ─▶ stop the lease's agent_pid + the orphan `cli.py wait` pair
 ─▶ read user@ memory.current yourself ─▶ spend: every minted key's usage flat over ≥ 2 min (reporting lags ~1 min)
```
- A director's SIGTERM can miss a kid's relaunch (one grew to 4.9 GiB after the stop): the re-list is not optional.
- A write-bound stall drains its Writeback for minutes after the writer stops: never re-clear on "it did not ease in 2 min".
- A prose NO MODEL LOAD in a brief does not bind a pi kid: under a model hold dispatch no round that can reach a model script.
- A model slot claimed by talk fails: a box-wide flock or nothing.

## 4 · Free disk — the full mount, lossless first
```
df the path ─▶ size ONE level (`du -xm --max-depth=1 <mount-dir>` in the background: /tmp has thousands of entries)
 ─▶ candidate = old (mtime > 24 h, nothing newer inside) AND 0 processes with a cwd or open fd in it
 ─▶ regenerable scratch (test basetemps, fixture logs) = delete · anything else = list for its owner
```
Worktrees live on `/data`: removing one frees nothing on `/`. A kid worktree is lossless to remove only when HEAD
is reachable from another ref AND `status --porcelain --ignored` shows nothing but caches — its ignored round
records (manifests, trajectories) are data: move them to `.agi/sessions/harvest-<date>/<wt>/` first; plain
`git worktree remove`, never `--force`. Never a recursive grep / find over MAIN's `.agi/` (every worktree checkout).
- dispatch holds when the RAM disk is >= the guard line (60 %): remove finished RAM round worktrees with `git worktree remove`; never bare
  `git worktree prune` (DG3 dispatch hold, `dispatch.py`).

## 5 · Your own long jobs
- `run_in_background` jobs sit in `run-*.scope` units that systemd-oomd kills in a memory spike — silently, no output.
  A long job runs in foreground chunks (`timeout 540`), resumable, logging each decision to a file.
- A suite or gate tree goes on DISK (`~/gate/<gate>` + its own `TMPDIR` there; tmpfs only while the slice has room, see the scratch rule below), removed after; stopping it = every pid whose cwd is the gate path.
- ONE full suite on the box at a time, on disk; SM's gate first; others run targeted rows; start only when MemAvailable >= the box's floor (6 GB; encryption-town 3 GB: no RAM disk, no stream stack, a gate tree is ~150 MB of tmpfs -- owner 10-09), memory PSI avg10 < 5 and io PSI avg60 < 50; each run removes its /dev/shm tree at its end (belam [rule] 18:4xZ 10-08: two tmpfs suites at once = box PSI full avg60 34.8%, the watchdog reboots at 40% for 5 min).
- starting a gate suite: assert the MemAvailable floor + PSI in the SAME command that starts it (exit if below); remove your finished
  /dev/shm trees BEFORE starting; never prune another's (SM gen 31 06:01Z: FULL at 2.7 GB under E's 3 GB floor).
- a Bash call that prints "moved to the background" keeps running: stop it at once with TaskStop unless wanted; use foreground `timeout`
  chunks; never a recursive search over `.agi/` (SM gen 31: `grep -rl` over `.agi/` 19:00-21:01Z, io storm).
- a run with a wall-time cap: start the cap clock AFTER the box / suite-window wait, never before (DT1: t0 before it burned the cap on a 31 min wait).
- briefing a compute subagent: say ONE process, no pools, `ulimit -v` (>= 4000000 for `import torch`), a PSI start gate; an unforbidden
  subagent fans out (thought-master 19:4xZ, near-reboot).

**Scratch is DISK, never /dev/shm, while the slice is full (belam's box-resource rule, 14:2xZ 10-11; every post).** tmpfs pages are charged to agi.slice: a RAM-disk basetemp or gate tree pushes EVERY post into reclaim and swap (SM's full suite 12:4xZ: mem PSI full 20, swap 0.9 GB; DG2's /dev/shm/dg2 1 GB at 14:2xZ: the alarm flapped). While `cat /sys/fs/cgroup/agi.slice/memory.current` is above 4600 MiB: no test or lane scratch on /dev/shm -- basetemp, TMPDIR and gate trees on a /data dir, NEVER your home or /tmp: every post home (/var/lib/agi/*) and /tmp sit on the 60 GB ROOT disk (belam [red] 17:0xZ 10-11: SM's ~/gate full suite, 3.6 GB basetemp, took / from 71% to 82% at +0.35 GB/min; stopped at 24%, removed). A post uid cannot write /data today: ask belam for a dir before the first suite; `nice -n 10`; ONE lane at a time; ONE heavy suite on the box at a time (say so in the box before a full pytest; start only at agi.slice anon + shmem < 3500 MiB (`memory.stat`) AND MemAvailable >= 2.5 GB AND mem PSI full avg60 < 2, read in the command that starts it; stop it yourself at mem PSI full avg60 > 10). The START test is never `memory.current`: it counts page cache + kernel memory the kernel reclaims under pressure, so it sits near High while only anon + shmem are hard (belam [rule] 16:2xZ 10-11: a 4600 MiB start test on memory.current kept SM's queued suite waiting at 5111 MiB with anon 2589). Clean your /dev/shm entries when done.

## 6 · Never print
| source | carries | read it as |
|---|---|---|
| `journalctl` lines | the HOST NAME (field 4) | cut to the message |
| `~/logs/memory-alarm-alerts.log` | the host name (field 2) | `cut -d' ' -f1,3-` |
| `systemctl show -p Description`, `/proc/<pid>/cmdline`, `ps -ef`, `pgrep -a` | argv — keys (the stream relay's) | `-p ActiveEnterTimestamp`, comm, cwd |
| `~/.claude/sessions/<pid>.json`, transcript events | machine-id, account / org uuids | named fields only |
| a suite's E-lines | fixture keys | filter on `key|priv` |
A slip onto a live stream: `brb` at once, then ONE `[red]` to the Prime.

## Traps moved from cards (owner 10-10: one sweep, then a rule)
- a test run while agi.slice is near its high -> the run is itself a dentry walker: hand it to a peer or run it on a small archive (alive gen 11-12)
- an alarm line you propose -> test it on a stressed fixture AND on a real quiet reading first (alive gen 12: the fill line was vacuous, then noisy)
- a load or rate cited for an hour -> measure it for THAT hour, or name whose number it is (alive gen 12)
- an A/B decision line -> it carries a MINIMUM EFFECT SIZE above the reading's resolution, or it passes on noise (alive gen 12, the vfs_cache_pressure A/B)
- a `sudo find` over /data/work or /var/lib/agi outlived its tool timeout and filled the dentry slab (14:12Z 10-21 warn) -> never walk those trees with find; kill a timed-out walk (belam gen II)
- scratch-worktree harness runs, one after another, put 2.2 GiB of dentry slab on agi.slice and tripped MemoryHigh (21:37Z 10-21, belam trap 121) -> run harnesses ONE at a time; at a slab warn: `sync; echo 2 | sudo tee /proc/sys/vm/drop_caches`, then read memory.stat back
