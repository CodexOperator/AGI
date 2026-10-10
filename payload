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
| io | `/proc/pressure/io` avg60 · `/proc/diskstats` inflight · `Writeback` in meminfo | read io off memory PSI (2 % memory while io ~88 %) |
| disk | `df -B1M <the exact path>` FIRST | assume one fs: `/` (`/tmp`, `/home`) and `/data` (repo, every worktree) are DIFFERENT |
| load | `/proc/loadavg` field 1 | gate on load alone: a dispatch gate is load1 AND io avg60 AND (disk free, key cap x live < balance) |

UNITS: every cgroup number in MiB = bytes / 1048576. A figure ~4.9 % above its own row is MB mislabelled.
VmHWM includes file-backed pages (torch libs, the safetensors mmap) the cgroup books as cache: read VmHWM AND the
hard rise; before claiming a kill frees MiB, read the scope's `memory.stat` anon vs file.

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

`pgrep -f <pattern>` matches the waiter's own argv and the claude processes' prompts: a loop on it never ends.
Wait on a PID found by comm + cwd.

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

## 5 · Your own long jobs
- `run_in_background` jobs sit in `run-*.scope` units that systemd-oomd kills in a memory spike — silently, no output.
  A long job runs in foreground chunks (`timeout 540`), resumable, logging each decision to a file.
- A suite or gate tree goes on tmpfs (`/dev/shm/<gate>` + its own `TMPDIR`), removed after; stopping it = every pid whose cwd is the gate path.

## 6 · Never print
| source | carries | read it as |
|---|---|---|
| `journalctl` lines | the HOST NAME (field 4) | cut to the message |
| `~/logs/memory-alarm-alerts.log` | the host name (field 2) | `cut -d' ' -f1,3-` |
| `systemctl show -p Description`, `/proc/<pid>/cmdline`, `ps -ef`, `pgrep -a` | argv — keys (the stream relay's) | `-p ActiveEnterTimestamp`, comm, cwd |
| `~/.claude/sessions/<pid>.json`, transcript events | machine-id, account / org uuids | named fields only |
| a suite's E-lines | fixture keys | filter on `key|priv` |
A slip onto a live stream: `brb` at once, then ONE `[red]` to the Prime.
