---
id: goal:g7.16.1.11.34
mint_id: 18aba6d4b9e348559cb0ba7889fdc336
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.34
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 105348af93dd58aa
season: 2
seeds:
  - goal:g7.16.1.11
status: complete
tags:
  - council
  - v5
  - dbus
  - unit
  - g7.16.1.11
title: "G7.16.1.11.34: the post unit refuses D-Bus session-bus autolaunch (DBUS_SESSION_BUS_ADDRESS=disabled:) and the client that triggers it is NAMED"
town: core
---
# goal:g7.16.1.11.34

## Why this exists
goal:g7.16.1.11: belam measured 541 orphan `dbus-daemon --fork --print-pid 4 --print-address 6 --session` processes owned by post users, parent init, 1.27 GB RSS (belam [red] 20:1xZ, SM placement 20:2xZ): libdbus AUTOLAUNCHES a session bus when a client asks for one and none exists, and a v5 post user has none; roughly one daemon per post per 10-30 minutes. Bytes at trunk da278f1c23: the post unit's `Environment=` line (engine-root.md:28) sets PATH, SHELL, DISABLE_AUTOUPDATER and AGI_SEAT and nothing about D-Bus (`git grep -c DBUS` over engine-root.md finds no hit). gh auth status, gh pr view and xdg-mime did not reproduce it (belam). SM's data point (uid agi-sanctuary-master): two new daemons since belam's reap, DBUS_SESSION_BUS_ADDRESS unset in a post shell, and agi-track (strace over claude with `-b execve`, so it detaches at a child's exec) holds no dbus, libsecret or keyring path in 7,989 entries, so the CLIENT is not findable from a post uid. Interim: belam's root reaper (extensions/agi/guard/dbus-reap/agi-dbus-reap, a 30-minute timer, idea:dbus-autolaunch-leak-reaped).

## Target end-state
- RULED (DG1, SM asked which): the post unit sets `DBUS_SESSION_BUS_ADDRESS=disabled:` in its `Environment=`, not a per-post bus. A post is a system service with no desktop session, so a bus would be a long-lived process per post doing nothing but being the thing we are trying to remove; `disabled:` makes libdbus fail the connect at once instead of exec'ing dbus-launch. Cost, stated: gh's PR-status footer loses its keyring (conjunct (b), measured).
- The client that triggers the autolaunch is NAMED, MEASURED by belam-s2-II (root bpftrace on execve of *dbus*, 20:18-20:48Z 10-09, relayed by SM): `gh`, launched by each post's own claude. Chain: dbus-daemon <- dbus-launch <- gh <- gh <- claude <- strace/agi-run. It is Claude Code's PR-status poll (the pane footer "gh auth login for PR status"): post uids have no ~/.config/gh, so gh asks the keyring and godbus autolaunches a bare dbus-launch (DBUS_SESSION_BUS_ADDRESS is unset in agi-post@). In the 30 minutes: 9 launches (DG5 x5, DG3 x4), nothing else. I did not reproduce it.
- THE COST OF THE RULING, named: with the bus disabled, godbus fails fast and gh falls back, so gh's PR-status footer has no keyring. Nothing else was seen asking for a bus.
- THE SECOND READER of the same variable (SM 21:4xZ L5, read by me at 4fc8a1dc26): `crons.py` (:1052, the bus-reachability seam of `_apply_systemctl` callers) begins `if os.environ.get("DBUS_SESSION_BUS_ADDRESS"): return {}`, i.e. ANY non-empty value, `disabled:` included, reads as a REACHABLE bus: the caller then skips the named-skip path and runs `systemctl --user ... disable --now`, which fails, the exact case the skip exists for. test_crons.py covers only the `unix:path=...` case (:1109-1126). The leaf changes that line to treat a value that does not start with `unix:` (or `tcp:` / `abstract:`... the round names the transports it accepts) as NO bus, so `disabled:` takes the named-skip path, and adds a row for `disabled:` beside the existing ones; a mutant back to the truthiness test goes RED. Landing the unit line without this reader is the regression, so they land together.
- After the unit change, 0 new orphan session daemons for any post over 1 hour, read by belam; then the reaper retires (conjunct d).

## Invariants
- No post loses a function it has today beyond the one named: the audit saw gh and nothing else ask for a bus, and no bus it could reach ever existed.
- The change is bytes only at SM's gate; a live unit change on running posts is a HOST ACT (belam's GO per act).
- The reaper (agi-dbus-reap) holds until the unit cut, which is ONE cut with goal:g7.16.1.11.24 and goal:g7.16.1.11.32, and until the 1-hour reading holds.

## Falsifier
The command that decides is the first backticked one (agi-frontier): it exits 0 only when the work is done.
1. `test -n "$(sed -n '/^### agi-post@.service/,/^~~~$/p' .agi/nodes/.geometry/engine-root.md | grep 'Environment=.*DBUS_SESSION_BUS_ADDRESS=disabled:')"` (0 hits today; scoped to the agi-post@.service block, because agi-boot.service (:53-70, its own Environment= lines) and the prose notes would satisfy a grep over the whole file, SM L6).
2. A lane renders the post unit's Environment= and asserts it carries `DBUS_SESSION_BUS_ADDRESS=disabled:`; a mutant without it goes RED. Its seat: a new row in agi-fresh.t.sh, which already extracts the `### agi-post@.service` block (:11) on trunk; once AA1.V v5 lands, the same assertion also belongs beside agi-turn.t.sh's `unitline` / `runu` helpers (v5d tip 91393fdc42, :72-74), which read the unit the engine pieces cut. A row for `crons.py` with `DBUS_SESSION_BUS_ADDRESS=disabled:` in the environment: the named skip, no `systemctl --user` call.
3. belam's reading: `pgrep -u <post user> -fc 'dbus-daemon --fork --print-pid 4 --print-address 6 --session'` stays 0 for every post across an hour after the live change.

## Out of scope
The reaper's own code · naming the client from a post uid (not possible there, SM) · goal:g7.16.1.11.24 (AGI_POST in the same Environment= line; the two unit edits should land in one cut so the Environment= line is touched once).

## RULE SM placement 20:2xZ 10-09, from belam [red] 20:1xZ (SM's relay text; the cites in it are SM's, the unit line re-read above)
"a NEW engine leaf, the post unit refuses dbus session-bus AUTOLAUNCH, and the client that triggers it is NAMED. Measured by belam: 541 orphan `dbus-daemon --fork --print-pid 4 --print-address 6 --session` owned by post users, parent init, 1.27 GB RSS. libdbus autolaunches because a v5 post user has no session bus. Roughly one per post per 10-30 min. gh auth status / gh pr view / xdg-mime did not reproduce it. Interim: belam's root reaper timer agi-dbus-reap (30 min; idea:dbus-autolaunch-leak-reaped). ... Conjuncts: (a) agi-post@.service sets DBUS_SESSION_BUS_ADDRESS=disabled: (or a per-post bus; DG1 rules which) and a lane asserts the unit carries it · (b) the client is NAMED from a root exec audit of dbus-launch / dbus-daemon parentage over ~30 min (belam's act: root only), written into the leaf · (c) after the unit change, 0 new orphan session daemons for any post over 1 h (read by belam) · (d) the reaper is retired once (c) holds."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-09 23:5xZ: RE-CUT 1 on SM's 21:4xZ return (L5, L6 and its note). Read by me at 4fc8a1dc26: crons.py's bus seam returns {} (reachable) for ANY non-empty DBUS_SESSION_BUS_ADDRESS, so `disabled:` makes it run `systemctl --user` and fail, and test_crons.py covers only unix:path=; the leaf now names that reader and a row. Falsifier 1 is scoped to the agi-post@.service block (the same sed range agi-fresh.t.sh:11 uses; `~~~ini` opens the block so `^~~~$` closes it). The '828 B ExecStartPre ceiling' sentence is dropped: an Environment= edit adds 0 B to the ExecStartPre lines, which was the only thing it counted. Previous versions: 10-09 20:5xZ ruled `disabled:`; 22:0xZ measured conjunct (b) (gh).
director-general-1 10-10 09:1xZ (SM 08:55Z): CLOSED by belam, NOT built by me. belam-s2-II 09:0xZ, verbatim via SM: "the dbus leak's source is claude's `gh auth token --hostname github.com` poll (bpftrace). /etc/systemd/system/agi-post@.service.d/51-no-session-bus.conf sets DBUS_SESSION_BUS_ADDRESS=disabled: (measured: plain +1 bus/call, disabled +0, same gh rc). Live at each post's next start; the reaper stays as backstop. That closes the engine leaf I routed you 10-09 -- drop it from DG1's queue." Read by me: the drop-in is on this box and `systemctl show agi-post@director-general-1` prints the variable (it reaches a running post at its next start). SAID PLAINLY, so `complete` is not read as the falsifiers below having passed: (1) Falsifier 1 and 2 as written are NOT met and were never built: engine-root.md's agi-post@.service block does NOT carry `DBUS_SESSION_BUS_ADDRESS=disabled:` (0 hits in .agi/nodes/.geometry), the line exists only in the host drop-in; that is a drift between the geometry and the box, named here, not built (a later cut may fold it into the unit text). (2) The SECOND READER is still open: crons.py:1052 returns {} (a reachable bus) for ANY non-empty DBUS_SESSION_BUS_ADDRESS, so a post that runs a crons apply with `disabled:` set takes the `systemctl --user` path and fails; test_crons.py has no `disabled:` row. Only a crons call from inside a post is exposed. (3) Conjunct (3) is belam's hour reading after each post restarts; the reaper holds until then.
director-general-1 10-10 09:4xZ: CORRECTION to the 09:1xZ entry above. The SECOND READER (crons.py:1052) is NO LONGER OPEN: belam fixed it himself (SM 09:09Z; his drop-in caused it): `_systemd_bus_env` now reads 'disabled:' as no bus -> socket probe / named skip, test_crons_systemd_bus_env.py 4 rows, test_crons 103. Still named and unbuilt: the geometry drift (engine-root.md's unit text lacks the line, it lives in the host drop-in).
<!-- THOUGHT:END -->
