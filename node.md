---
id: config:guard
mint_id: 275ccb3bf7af4b198b50c21e0a2b6f59
type: config
parents:
  - goal:g7.16.1.7
  - goal:g7.16.1.5.1
next_edges: []
edited_by: belam
locations: {}
season: 2
title: config:guard -- the sanctuary guard's per-box settings (was ~/work/.sanctuary/guard/guard.env)
---
<!-- BODY:BEGIN -->
# config:guard

The ONE cell for the sanctuary guard's per-box settings (goal:g7.16.1.7: "the
guard is in the graph ... guard.env as a .geometry config node keyed by box
class, never by host name"). `extensions/agi/guard/guard-init.sh` reads the
fenced block below (opened by the line ```` ```sh guard.env ````, closed by a bare fence)
and evaluates it as bash, exactly as it used to source `guard.env`. The file it
replaces is kept on the box as `~/work/.sanctuary/guard/guard.env.pre-graph-20260930`
and is read only when this node is missing.

- **Key = the BOX name**, never the host name: `GUARD_<SETTING>_<box>` with every
  non-alphanumeric of the box turned into `_` (`local-town` -> `local_town`).
  guard-init.sh resolves the box as `GUARD_BOX`, else `/etc/sanctuary-guard/box`
  (one line), else the hosts.json town whose `host` is this host, else `hostname -s`.
- `GUARD_ENV_NODE=<path>` points guard-init.sh at another copy of this node.
- After an edit: `guard-init.sh --dry-run` on the box, then `sudo guard-init.sh`.
  The why, the layers and the kill switches: `extensions/agi/guard/GUARD.md`.

```sh guard.env
# guard.env: per-BOX overrides for guard-init.sh (evaluated as bash; this block is config:guard).
# Key = the box name (GUARD_BOX, else /etc/sanctuary-guard/box, else the hosts.json town
# whose host is this host) with every non-alphanumeric turned into _ (local-town -> local_town).
# Sizes: 512M, 2G, 1.5G, or a bare number of MiB. Anything unset uses the default.
#
#   GUARD_RESERVE_<box>            memory kept OUT of user@<uid> for sshd + system.
#                                  default: max(768M, 12% of RAM)
#   GUARD_DOCKER_BUDGET_<box>      memory set aside for docker containers. They live in
#                                  system.slice, so the user@ cap does NOT bound them;
#                                  this subtracts them from it. default: 0
#   GUARD_ENGINE_MAX_<box>         cap for the little engine scripts. default: 512M
#   GUARD_PSI_FULL_<box>           watchdog trips when every task is stalled on memory
#                                  >= this % of the last minute, for 5 min. default: 40
#   GUARD_GRACE_<box>              seconds after boot the watchdog never judges. default: 900
#   GUARD_PEERWATCH_CLAUDE_<box>   1 = the first outage of another town launches ONE
#                                  recovery claude. Set it on ONE box only. default: 0
#
# Re-run guard-init.sh on a box after changing its lines. Never key a line by host name.

# --- encryption-town: 8G, no docker ----------------------------
# Always on, and the only box with Doppler: it runs the recovery agent.
GUARD_PEERWATCH_CLAUDE_encryption_town=1

# --- local-town: 16G + llama-server in docker ---------------------
# llama-server (host network, port 8080) partially offloads 9B-35B models to
# host RAM. 8G is a STARTING POINT, not a measurement: the box was unreachable
# when this was written. Once it is back: `docker stats --no-stream`, then tune.
# 16G - 1.9G reserve - 8G docker leaves ~5.6G for belam's seats and rounds.
GUARD_DOCKER_BUDGET_local_town=0

# --- core-town: 23G, docker for the stream -----------------------------
# Unmeasured. Set a budget after `docker stats --no-stream` on the box.
# GUARD_DOCKER_BUDGET_core_town=4G

# --- silicon-town: 6G Lima VM, ephemeral ---------------------------
# Defaults fit. Its watchdog only ever reboots the VM, never the laptop.

# owner 2026-09-29 22:4xZ option (b), set by belam-S2-L5-XVIII: oomd waits for 85% pressure, the watchdog reboots only at 60% full stall, user@ throttles at 95% of its max
GUARD_PSI_FULL_local_town=60
GUARD_OOMD_LIMIT_local_town=85
GUARD_USER_HIGH_PCT_local_town=95

# owner 2026-09-30 01:3xZ option B, set by belam-S2-L5-XIX (goal:g7.16.1.5.1 + .5.2; scripts ram-main.sh + session-sweep.sh):
#   GUARD_RAM_MAIN_<box>                 MAIN, whose working files move to the RAM disk under the SAME path. empty = off
#   GUARD_RAM_DIR_<box>                  the tmpfs mount (fstab). default: /mnt/agi-ram
#   GUARD_RAM_SYNC_MIN_<box>             RAM -> disk sync of MAIN's working files, minutes. default: 10
#   GUARD_AGI_SESSIONS_ARCHIVE_<box>     /data home of idle .agi/sessions/iter-* dirs (a symlink stays behind)
#   GUARD_CLAUDE_PROJECTS_ARCHIVE_<box>  /data home of idle ~/.claude/projects/<dir> (the 09-28 convention)
#   GUARD_SWEEP_IDLE_MIN_<box>           an iter dir untouched this long moves. default: 120
#   GUARD_SWEEP_PRESSURE_PCT_<box>       tmpfs use at/above this -> the pressure idle age. default: 60
#   GUARD_SWEEP_PRESSURE_IDLE_MIN_<box>  default: 20
#   GUARD_SWEEP_CLAUDE_IDLE_MIN_<box>    a Claude project dir untouched this long moves. default: 1440
GUARD_RAM_MAIN_local_town=/data/work/agi
GUARD_RAM_DIR_local_town=/mnt/agi-ram
GUARD_RAM_SYNC_MIN_local_town=10
GUARD_AGI_SESSIONS_ARCHIVE_local_town='/data/home-$USER/agi-sessions'
GUARD_CLAUDE_PROJECTS_ARCHIVE_local_town='/data/home-$USER/claude-projects'
GUARD_SWEEP_IDLE_MIN_local_town=120
GUARD_SWEEP_PRESSURE_PCT_local_town=60
GUARD_SWEEP_PRESSURE_IDLE_MIN_local_town=20
GUARD_SWEEP_CLAUDE_IDLE_MIN_local_town=1440
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g7.16.1.5.1 + .5.2 (belam-S2-L5-XIX 01:3xZ 09-30): nine cells for the owner option B -- MAIN working files on the RAM disk under its own path (ram-main.sh) and the idle-session sweep to /data homes (session-sweep.sh). Paths use $USER, never a literal home, so the anonymize gate holds. goal:g7.16.1.5.1 added as a parent: the owner, 01:3xZ: the goal can parent the new versions of all relevant .geometry nodes.
<!-- THOUGHT:END -->
