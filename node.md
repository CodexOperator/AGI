---
id: idea:dbus-autolaunch-leak-reaped
mint_id: ce0222a9b25c4311a46372ca7af3c609
type: idea
parents:
  - goal:g7.16.1.11.7
next_edges: []
model: claude-opus-5-5
role: prime_director
scaffold_hash: cc4e5bfc70c20ba8
season: 2
title: "post users leak autolaunched session buses (541, 1.27 GB on 10-09): a 30-minute root reaper stops the orphans until the unit refuses autolaunch"
town: core
---

# idea:dbus-autolaunch-leak-reaped

MEASURED 2026-10-09 20:0xZ on encryption-town: 541 `dbus-daemon --syslog --fork --print-pid 4 --print-address 6 --session` processes owned by the v5 post users (agi-belam 117, DG3 66, DG1 66, TM 45, DG4 39, ...), every one re-parented to init, holding 1.27 GB RSS together on a 7.8 GB box. That is libdbus AUTOLAUNCH: a post user has no session bus (no user manager), so a client started from the post's claude process (its environment = claude's child env: CLAUDE_CODE_BRIDGE_SESSION_ID, blanked GH_TOKEN/GITHUB_TOKEN, no Bash-tool SHLVL) spawns a private bus that outlives it. Cadence ~1 per post per 10-30 min (one every 30 min while idle). The exact client is NOT yet identified: `gh auth status`, `gh pr view` with the daemon's environment and `xdg-mime` (absent) did not reproduce it.

Interim (belam, on the owner's "make sure all our guards ... are set"): a root timer every 30 min stops only those buses -- owner agi-*, parent 1, --session + --print-pid, older than 30 min; belam's desktop and login buses are never touched. The first manual pass stopped 538.

Root fix (council, via SM): the post unit sets a session-bus address that refuses autolaunch (e.g. DBUS_SESSION_BUS_ADDRESS=disabled: or a per-post bus), and the client that autolaunches is named.

Files (extensions/agi/guard/dbus-reap/): agi-dbus-reap (installed /usr/local/sbin), agi-dbus-reap.service + .timer (installed /etc/systemd/system, OnBootSec=10min, OnUnitActiveSec=30min). Journal tag: agi-dbus-reap.
