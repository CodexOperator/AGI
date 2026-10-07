# .sanctuary / guard: keep a box reachable while it burns

Guard is five layers, installed with one command, that keep a mesh box **reachable**
when its userspace runs out of memory. If it cannot be kept reachable, guard makes
it **reboot itself** instead of staying wedged. The source lives in the agi repo,
`extensions/agi/guard/` (build nodes, goal:g7.16.1.7); `~/work/.sanctuary/guard/`
holds symlinks into it, so every command below works from either path:

| file | what it is |
|---|---|
| `guard/guard-init.sh` | the one command. Idempotent; `--dry-run`, `--status`, `--uninstall` |
| `config:guard` | per-box overrides (docker budget, reserve, which box runs the recovery agent): the ```` ```sh guard.env ```` block of `.agi/nodes/.geometry/guard.md`, keyed by box name. The old `guard/guard.env` is kept as `guard.env.pre-graph-20260930` and read only if the node is missing |
| `guard/guard-env.sh` | the ONE reader of that block (`guard_env_load <node>`), sourced by guard-init, ram-main, ram-tier and session-sweep: only blank lines, `#` comments and `GUARD_<NAME>=<value>` (bare, or single-quoted with the literal `$HOME`) are accepted, anything else exits 1 naming the node and line before any side effect; nothing is evaluated |
| `guard/sanctuary-health` | the watchdog's health check (installed to `/usr/local/sbin`) |
| `guard/sanctuary-watch` | the 2-minute watcher: cap-kill alerts + peer checks (installed to `~/.local/bin`) |

## Why: local-town, 2026-09-25

local-town stopped making progress at 13:58:34Z and stayed wedged for
hours. The kernel was fine: it answered ping and completed TCP handshakes on :22.
sshd never sent a banner, not in 150 s and not in 12 tries. There was no way in and
no way to reboot it remotely. A full port scan found nothing else listening, and
there was no already-authenticated channel to use. It needed the operator's hands.

What makes that possible, and what guard fixes:

- **A box with swap does not run out of memory. It thrashes.** The kernel keeps
  reclaiming just enough to call it progress, so the OOM killer never fires.
  Everything that needs a new page stalls in reclaim, for hours.
- **sshd being unkillable did not help.** Its listener already had
  `oom_score_adj=-1000`, so it was never killed. But answering a login means
  forking a child, forking needs memory, and it stalled like everything else.
  TCP accepts, no banner: exactly what we saw.
- **A cgroup protects nothing by itself; only the limits on it do.**
  `claude-remote-control.service` had its own cgroup, but with `MemoryMin=0`,
  `MemoryLow=0` and `OOMScoreAdjust=200`. The engine's reaper had its own
  cgroup with no limits at all.
- **The engine's own scripts were a load source.** On encryption-town the reaper
  swept 622 worktrees every 30 s with `removed=0` across 2387 passes, about
  3000 process spawns per pass. mem_cap's probe took a deliberate OOM kill on
  every spawn: 1784 kills in 6 days. Both are fixed in `goal:g6.49`. The box had
  also spent 454 s with *every* task stalled on memory (`/proc/pressure/memory`).
  This was measured on encryption-town, not local-town, which could not be
  entered. The cause of local-town's wedge is plausible, not proven.

## The five layers

| # | layer | what it does | lives in |
|---|---|---|---|
| 1 | **systemd-oomd** | Kills the runaway on memory *pressure* (PSI), while there is still time. The kernel's OOM killer waits until there is no progress at all, which under swap never comes. | system |
| 2 | **the way back in** | `user@<uid>` is capped at *RAM − reserve − docker*, so everything the user runs can thrash itself but can never take the memory sshd needs. sshd gets `MemoryMin` (made real by `system.slice`'s own `MemoryMin`) and the top CPU weight within `system.slice`; it stays unkillable the way it always was, by itself. Claude gets `MemoryLow` + CPU weight over its siblings, with the same `MemoryLow` on every ancestor (`user.slice`, `user-<uid>.slice`, `user@`, `app.slice`), because cgroup v2 protection is worth nothing unless the whole chain above has it. | system + user |
| 3 | **the engine fence** | `agi.slice` = `agi-engine.slice` (the little scripts: reaper, alarms, watch: **512M, 128 tasks, no swap**) + `agi-work.slice` (rounds, merge-ups, suites). oomd acts on `agi.slice` at 40 % pressure, before `user@` reaches 50 %, so the engine goes before Claude does. | user |
| 4 | **the watchdog** | If memory stays stalled ≥ 40 % for **5 minutes**, or the health check cannot even start, the box **reboots**. `kernel.panic=10` so a panic reboots instead of hanging, and `kernel.panic_on_oops=1` so a kernel oops (a kernel bug) is turned into that reboot instead of limping on. | system |
| 5 | **the watch** | Every 2 min: alerts if a cap bit here (`agi-engine` hitting its own cap is an **ALARM**: those scripts never get near 512M), and probes every other town. On an outage it has *seen begin*, it can launch **one** recovery Claude. | user |

Layers 1–3 keep the box reachable. Layer 4 is the last resort when they cannot.
Layer 5 tells you.

### How the engine is routed into its slices

systemd applies drop-in directories by **unit-name prefix**, and a same-named file
in a more specific directory wins (tested on this systemd before relying on it):

```
~/.local/share/systemd/user/agi-.service.d/50-sanctuary-guard.conf      -> Slice=agi-work.slice
~/.local/share/systemd/user/agi-agi-.service.d/50-sanctuary-guard.conf  -> Slice=agi-engine.slice
```

So every unit the engine writes (`agi-agi-reaper-*`, `agi-agi-alarms-*` →
engine; `agi-belam-dispatch-*`, `agi-belam-mur-*`, `agi-helper-*` → work) lands
in the right slice **with no change to the engine**. Guard's own units live in
`~/.local/share/systemd/user`, not `~/.config/systemd/user`: `crons.py`'s drift
scan reports every undeclared `*.service` in the latter.

### The oomd quirk that silently dropped the backstop

Found live on encryption-town at install time, and invisible to a read-only
review. Inside a user manager, the root slice (`-.slice`) **is** the
`user@<uid>.service` cgroup. Once `agi.slice` asks oomd to watch it, the user
manager starts reporting its units to oomd, including that root slice with the
default `ManagedOOMMemoryPressure=auto`. oomd reads `auto` as "stop watching this
path", so it dropped the `user@<uid>` 50 % entry PID1 had registered. `agi.slice`
was watched, and the backstop above it was not. Other users on the box (e.g.
`user@1001`) kept theirs, because their managers have nothing to report and
never connect. Guard sets the user manager's own root slice to `kill` at 50 %
(`~/.local/share/systemd/user/-.slice.d/`), so both entries survive. `--status`
checks oomd's real monitored list (`oomctl`, needs sudo), not the config.

**Running units are never restarted.** They move at their next start. The
reaper and alarms move sooner if you pass `--restart-engine` (cheap: `crons.py`
re-arms them anyway).

## Setup

On each box, from the box's own user (the engine's user; `ubuntu` on core-town):

```bash
~/work/.sanctuary/guard/guard-init.sh --dry-run    # read the plan: every file, every command, the sizes
sudo ~/work/.sanctuary/guard/guard-init.sh         # apply
~/work/.sanctuary/guard/guard-init.sh --status     # verify
```

**Roll out in this order:** encryption-town first (reachable, and it runs the
recovery agent), then core-town, then local-town *after* measuring its docker
usage (below), silicon-town whenever. Re-run the script after any change to
`guard/`: it rewrites only what differs and says `unchanged` for the rest.

**local-town first needs its docker budget measured.** llama-server runs in
docker, and containers live in `system.slice`, outside the `user@` cap. On the
box: `docker stats --no-stream`, set `GUARD_DOCKER_BUDGET_local_town` in
config:guard's `guard.env` block above what it shows, dry-run, apply. To cap the running container
too (live, no restart): add `--apply-docker`. It refuses any container already
using ≥ 90 % of the budget, since capping it there would squeeze it at once.

### Sizes (encryption-town, 7854M RAM)

```
user@1000      max 6912M  (7854 − reserve 942)        Claude MemoryLow 1024M (also on user.slice,
                                                      user-1000.slice, user@1000, app.slice)
system.slice   MemoryMin 128M  ->  ssh.service MemoryMin 64M
  agi.slice    max 4838M  (70 % of user@)
    agi-engine max  512M  swap 0, 128 tasks
    agi-work   max 4326M
```

Every number comes from `/proc/meminfo` and config:guard; `--dry-run` prints them
for the box it runs on. `user@` is capped live unless it already holds close to
the high mark in memory it *cannot give back*: anon, shmem, mapped files and
unreclaimable slab. Page cache does not count, because a cap simply trims it. On
encryption-town at install time `memory.current` read 6251M, but only 385M of that
was anon. Only when the hard part is near the mark does the cap wait for the next
boot, via `/run/systemd/system/user@<uid>.service.d/99-sanctuary-guard-defer.conf`
(99- sorts after every other drop-in, and /run is emptied at boot), rather than
squeezing seats that are mid-round.

## Verify

`guard-init.sh --status` checks every layer against the live system, not the
files: oomd active, `user@` actually capped, sshd's weights, which running engine
unit is inside its slice and which moves at next start, the watchdog device
state, whether the health check passes *now*, the timer's next run, the last
five alerts. It also reads the kernel's view (`memory.min`, `memory.low`) to prove
the protection chains are live, not just configured. It ends `all layer checks
passed` (exit 0) or names what failed (exit 1). A layer whose files are absent is
reported as not installed, not as failed. A deferred `user@` cap says so.
Claude's chain is checked link by link: a single ancestor without `memory.low`
fails the check, because one gap makes the whole chain worth nothing.

## Alerts

`~/logs/sanctuary-guard/alerts.log`, one line per event worth a human:

| line | means |
|---|---|
| `ALARM agi-engine.slice hit its own Nx memory cap` | a little script outgrew 512M. They run near 80M: something upstream is wrong. Read from `memory.events.local`, so a kill caused by a limit higher up is not blamed on this slice |
| `ALARM user@<uid> hit its own memory ceiling` | everything this user runs was squeezed; look at what grew |
| `WARN agi-work.slice hit its own memory cap Nx` | a round hit the rounds' cap |
| `OOMD ...` | systemd-oomd killed a cgroup for memory pressure (needs journal access) |
| `OUTAGE <town> (<host> <ip>) is degraded\|down: 3 misses in a row` | *degraded* = pings, no ssh (the livelock shape); *down* = no ping |
| `OUTAGE <town> (<host> <ip>) is ... already was when the watch first saw it` | reported, but no agent: it was down before the watch started |
| `OUTAGE hub gw (<ip>) unreachable from <this host>` | this box's own overlay is down, so every town would look dead: peer checks pause until it is back |
| `RECOVERY agent launched for <town> (unit ...)` | one Claude; never while one for that town still runs, never twice within an hour; its report lands next to the log |
| `RECOVERY launch FAILED for <town>` | systemd-run refused; retried after the same hour, not every 2 min |
| `RECOVERED <town> (<host>) after N min` | it's back; N counts from the first miss. Only outages that were alerted get one (not an asleep silicon-town) |
| `WATCH cannot parse .../hosts.json` | peer checks are OFF until it is fixed; said once, not every run |

`watch.log` has every probe. When the check itself runs and fails, it appends to
`/var/log/sanctuary-health.log`. Three reboot paths leave no line there:

- a check that cannot even start within `test-timeout` (the deepest livelock), and
- the daemon itself dying: read the previous boot, `journalctl -b -1 -u watchdog`
  and `/var/log/watchdog/`;
- a kernel panic or oops (layer 4 sets `kernel.panic_on_oops=1` and
  `kernel.panic=10`): `journalctl -b -1 -k`, or `/var/lib/systemd/pstore` if the
  panic got that far.

**Not alerted, on purpose:** kills inside mem_cap's per-kid scopes (`app.slice`).
A runaway kid dying alone and by name is that cap working, and mem_cap's probe
(`agi-memcap-probe.scope`) dies by SIGKILL on purpose, once per boot.

### The recovery agent

Only on the box with `GUARD_PEERWATCH_CLAUDE_<box>=1` (encryption-town). When it
sees a town go from up to 3 misses, it launches `claude -p` once, in `app.slice`
with a 2G cap and a 1 h limit. The brief carries the owner's rules (mind the
other agents; no new remote heads, no fast-forwards, no force-push; never
`--allow-branch`). If it cannot get a shell it cannot reboot anything. It says
so, waits 15 min to see whether the town's own watchdog brings it back, and
writes its report to `~/logs/sanctuary-guard/recovery-<town>-<ts>.md`. It must
confirm `hostname` before acting on any shell, and it never guesses IPs: the LAN
addresses in hosts.json have drifted, and a guess can land on a healthy box. A new
agent is never launched while one for that town is still running, and never twice
within an hour, so a flapping town cannot stack them.

## Kill switches, from lightest

```bash
sudo touch /etc/sanctuary-guard/watchdog.disable   # the check always passes. Everything else stays on (see below)
sudo systemctl stop watchdog                       # the daemon disarms the device: no reboots at all
systemctl --user stop sanctuary-watch.timer        # no alerts, no peer checks, no agents
sudo ~/work/.sanctuary/guard/guard-init.sh --uninstall   # everything guard wrote, gone
```

The `watchdog.disable` file stops reboots for memory pressure, but not for the
deepest case: if the box cannot even *start* the check for 5 minutes, it still
reboots, because a box that cannot fork a shell script is gone either way. To stop
every reboot, stop the daemon.

Stopping the watchdog is safe. The daemon disarms the device on a clean stop
(softdog has no NOWAYOUT here). Guard masks the package's `wd_keepalive` helper:
its stop/restart dance made the packaged `watchdog.service` fail every restart and
every package upgrade. The device only fires if the daemon dies uncleanly, which
is its job.

## Tuning

All in config:guard (`.agi/nodes/.geometry/guard.md`, its ```` ```sh guard.env ```` block;
edit it through `write.py`), keyed by the BOX name with every non-alphanumeric
turned into `_` (`local-town` -> `_local_town`), then re-run the script. The box
is `GUARD_BOX`, else `/etc/sanctuary-guard/box` (one line), else the hosts.json
town whose `host` is this host, else `hostname -s`. `GUARD_ENV_NODE` points the
script at another node file. Keys:
`GUARD_RESERVE_*`, `GUARD_DOCKER_BUDGET_*`, `GUARD_ENGINE_MAX_*`,
`GUARD_PSI_FULL_*` (the watchdog threshold, default 40 %),
`GUARD_GRACE_*` (seconds after boot it never judges, default 900),
`GUARD_PEERWATCH_CLAUDE_*`. The file documents each one.

Every other memory number the script applies is a cell too (goal:g7.16.1.5.5.5).
Each default is the literal the script used to carry, so a box that sets none of
them gets exactly what it got before. An unset or EMPTY cell takes the default.

| cell | what it sets | default |
|---|---|---|
| `GUARD_OOMD_LIMIT_*` | oomd kill line for user@ + its root slice, % pressure (10..99) | 50 |
| `GUARD_USER_HIGH_PCT_*` | user@ MemoryHigh, % of its MemoryMax (50..99) | 90 |
| `GUARD_AGI_MAX_PCT_*` / `GUARD_AGI_HIGH_PCT_*` | agi.slice max, % of user@'s max / high, % of that max | 70 / 90 |
| `GUARD_ENGINE_HIGH_PCT_*` | agi-engine.slice high, % of `GUARD_ENGINE_MAX` | 75 |
| `GUARD_WORK_HIGH_PCT_*` | agi-work.slice high, % of its max (agi max - engine max) | 90 |
| `GUARD_AGI_OOMD_LIMIT_*` | oomd kill line for agi.slice, % pressure; below user@'s, so the engine dies first | 40 |
| `GUARD_USER_SWAP_PCT_*` / `GUARD_USER_SWAP_CAP_*` | user@ + agi.slice MemorySwapMax = min(swap x PCT/100, CAP) | 50 / 2048M |
| `GUARD_CLAUDE_LOW_DIV_*` / `GUARD_CLAUDE_LOW_CAP_*` | Claude's MemoryLow chain = min(user@ max / DIV, CAP) | 6 / 1024M |
| `GUARD_OOMD_SWAP_USED_PCT_*` / `GUARD_OOMD_PRESSURE_PCT_*` / `GUARD_OOMD_PRESSURE_S_*` | oomd.conf SwapUsedLimit / DefaultMemoryPressureLimit / its duration in seconds | 90 / 60 / 20 |
| `GUARD_SYSTEM_MIN_*` / `GUARD_SSH_MIN_*` | MemoryMin of system.slice / sshd | 128M / 64M |
| `GUARD_ENGINE_SWAP_MAX_*` / `GUARD_RAMDISK_SWAP_MAX_*` | MemorySwapMax of agi-engine.slice / ramdisk.slice (written as 0 or whole MiB) | 0 / 0 |
| `GUARD_USER_MIN_*` | the least user@ may be left with; below it the script refuses | 2048M |
| `GUARD_DOCKER_CAP_HEADROOM_PCT_*` | a container using this % of the docker budget is not capped live | 90 |
| `GUARD_DEFER_PCT_*` | user@'s new cap waits for the next boot when hard use is at or over this % of the new high | 90 |

The script checks every cell as a string before any arithmetic reads it. A
percent or count must be a whole number in its range. A size must be `512M`,
`2G`, `1.5G` or whole MiB: uppercase unit, never negative, never a bare unit.
Anything else is refused by name (`GUARD_<NAME>_<box> must be ...`) and nothing
is written.

## Caveats

- **A watchdog reboot needs tang.** The encrypted farm boxes unlock through tang
  on `gw`. If `gw` is down when the watchdog reboots a box, the box waits at the
  passphrase prompt (dropbear on LAN :2222, `cryptroot-unlock`). That is no worse
  than wedged, but it is not recovered either.
- **Docker is outside the `user@` cap.** The budget subtracts it; only
  `--apply-docker` actually bounds it. A container re-created without `--memory`
  (e.g. llama-server with new flags) is unbounded again.
- **mem_cap's per-kid scopes land in `app.slice`, not `agi-work.slice`.**
  `systemd-run --user --scope` defaults there. They are still bounded by their
  own cap (6G) and by `user@`'s. Moving them into the fence is a one-flag engine
  change (`--slice=agi-work.slice` in `mem_cap.wrap_argv`), for the engine's own
  branch process, not for guard.
- **oomd cannot be told to spare Claude by name.** `ManagedOOMPreference=avoid`
  is honoured only for root-owned cgroups, and everything under `user@` is owned
  by the user. The protection is structural instead: the engine's slice trips
  first at 40 %, and Claude's `MemoryLow` chain makes it the last thing reclaimed.
- **An unprivileged user manager can only raise `OOMScoreAdjust`**, so Claude's
  200 cannot be lowered from its unit. Under guard that matters less: the kernel
  OOM killer is the last line, after oomd and the caps.
- **Guard does not touch sshd's `OOMScoreAdjust`, on purpose.** sshd sets its own
  listener to -1000 and gives every login child back the value it started with.
  Starting sshd at -1000 would make every login shell, and anything run from it,
  unkillable, outside the `user@` cap.
- **sshd's CPU weight ranks it only within `system.slice`.** No IO weight is set:
  no io controller is enabled on these boxes, so it would do nothing.
- **Restarting `claude-remote-control.service` kills every tmux server started
  from a Remote Control session:** they live in its cgroup. Check
  `systemctl --user status claude-remote-control` before restarting it.
- **The watch pauses when the hub is down.** If `gw` does not answer, this
  box's own overlay is down and every town would look dead. It records that once
  and checks nothing else, instead of raising false outages.
- **The system journal may not be readable** by the engine user, so the `OOMD`
  alerts can be silent. The cap alerts come from cgroup counters and are not.

## Uninstall

`sudo guard-init.sh --uninstall` removes every file it wrote and returns every live
value (caps and protection chains) to its default. It stops and disables the
watchdog, which disarms the device, unmasks `wd_keepalive`, restores the original
`/etc/watchdog.conf`, and disables the watch timer. It disables oomd only if guard
was what turned it on. The two packages stay installed but inert:
`/etc/default/watchdog` and debconf are left at `run_watchdog=0`, so the stock
daemon does not start on its own either. To use the stock watchdog without guard
afterwards: `sudo dpkg-reconfigure watchdog`. `softdog` stays loaded
until reboot, disarmed. Engine units already running inside `agi-*.slice` stay
there until they restart.
