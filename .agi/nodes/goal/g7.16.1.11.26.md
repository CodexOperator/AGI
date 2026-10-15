---
id: goal:g7.16.1.11.26
mint_id: 38562cf6531c4287acc81e22cef3e40a
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G7.16.1.11.26
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 6d8d44cb8bf9ad4d
season: 2
seeds:
  - goal:g7.16.1.11
status: horizon
tags:
  - council
  - v5
  - guard
  - e
  - g7.16.1.11
title: "G7.16.1.11.26: config:guard carries _encryption_town lines (belam supplies the values) so guard layer 5 sanctuary-watch can be installed on E; no RAM_* line applies"
town: core
---
# goal:g7.16.1.11.26

## Why this exists
goal:g7.16.1.11: guard layer 5 (extensions/agi/guard/sanctuary-watch, installed by guard-init.sh:655 layer5()) is NOT installed on E (belam's E root audit 04:1xZ, card-belam.md:85). It is held because its peers still list local-town (down) and `GUARD_PEERWATCH_CLAUDE_encryption_town=1` would launch a recovery claude per L outage; belam's order is "first config:guard E lines (DG1 leaf) + /etc/sanctuary-guard/box = encryption-town, then sudo guard-init.sh". The block that holds the lines, .agi/nodes/.geometry/guard.md, carries 19 `_local_town` keys over :86-129 (SM's relayed ":86-117" was short): DOCKER_BUDGET, PSI_FULL, OOMD_LIMIT, USER_HIGH_PCT, RAM_MAIN, RAM_DIR, RAM_SYNC_MIN, AGI_SESSIONS_ARCHIVE, SWEEP_PAIRS, TIER_HOT, TIER_COLD, TIER_DIRS, SWEEP_IDLE_MIN, SWEEP_PRESSURE_PCT, SWEEP_PRESSURE_IDLE_MIN, SWEEP_CLAUDE_IDLE_MIN, RAM_WORKTREES, RAM_WT_HOLD_PCT, ENGINE_MAX; and exactly ONE `_encryption_town` key, :79 PEERWATCH_CLAUDE, under the header at :77 "encryption-town: 8G, no docker". E has no RAM disk, so no RAM_* line applies.

## Target end-state
- guard.md carries an `_encryption_town` line, with the value belam supplies as a box fact, for each of the 4 keys guard-init.sh actually reads for a box and that carry no path, RAM or docker fact: PSI_FULL (guard-init.sh:216), OOMD_LIMIT (:217), USER_HIGH_PCT (:218), ENGINE_MAX (:230). With PEERWATCH_CLAUDE (:79 today) the wanted set is those 5.
- The other 15 local keys get NO E line, and a one-line comment in the E block names them not applicable: RAM_MAIN, RAM_DIR, RAM_SYNC_MIN, RAM_WORKTREES, RAM_WT_HOLD_PCT (E has no RAM disk), DOCKER_BUDGET (no docker), AGI_SESSIONS_ARCHIVE, SWEEP_PAIRS, TIER_HOT, TIER_COLD, TIER_DIRS (paths), and the four SWEEP_IDLE_MIN, SWEEP_PRESSURE_PCT, SWEEP_PRESSURE_IDLE_MIN, SWEEP_CLAUDE_IDLE_MIN, which are INERT on E: only session-sweep.sh reads them, and its :22 exits "off" unless RAM_MAIN and AGI_ARCH are set (both N/A on E); SWEEP_PRESSURE_PCT is a RAM-disk fact; guard-init.sh reads none of the four (belam may still name a value).
- `GUARD_BOX=encryption-town` makes guard-init.sh --dry-run exit 0 and print layer 5 with PEER_CLAUDE as the E line says. (guard-init.sh reads a missing key silently: `hostvar` at :189 defaults, and its only missing-cell warning, :699, needs docker; so a missing E line is not a warning guard-init.sh emits. session-sweep.sh:22 does echo "cells unset ... off" for the N/A case.)
- OPEN FOR BELAM, not decided here: which towns are E's peers (extensions/agi/guard/sanctuary-watch builds the peer list at :79-89 from hosts.json, probes with ping and ssh at :99-103; :76 is the missing-hosts.json exit; the header at :13 says it checks every other town) and whether PEERWATCH_CLAUDE stays 1 on E while a listed peer is down.

## Invariants
- Never key a line by host name (guard.md's own rule): the box key is the town, `_encryption_town`.
- The values are belam's box facts: no `_local_town` value is copied to an E line unless belam says so, and each E value's source is in the THOUGHT.
- This leaf installs nothing: layer 5 is installed by `sudo guard-init.sh` on E (root, belam's), after the lines land and /etc/sanctuary-guard/box reads encryption-town.

## Falsifier
The command that decides is the FIRST backticked one (agi-frontier, engine-post.md:170-173, runs it and prints "met" on exit 0), so it exits 0 ONLY WHEN THE WORK IS DONE.
1. Positive, fails today (1 of the 5 named keys): `test $(sed -n '/guard[.]env: per-BOX/,/^[[:punct:]]\{3\}$/p' .agi/nodes/.geometry/guard.md | grep -oE '^GUARD_(PEERWATCH_CLAUDE|PSI_FULL|OOMD_LIMIT|USER_HIGH_PCT|ENGINE_MAX)_encryption_town=' | sort -u | wc -l) -eq 5` (scoped to the `sh guard.env` fence that guard_env_load reads (guard-init.sh:172-181), from its first comment line to the closing bare fence, and counting DISTINCT keys: five lines in the THOUGHT block, or one key five times, can no longer make it green, SM B5; the range avoids a literal backtick because agi-frontier splits the Falsifier on them).
2. `bash extensions/agi/tests/guard-env.t.sh` exits 0 (its s-c3 rows read every `GUARD_*_encryption_town` assignment through each script's own cell()), and `GUARD_BOX=encryption-town bash extensions/agi/guard/guard-init.sh --dry-run` exits 0 on the lines landed here.
3. Negative: `test -z "$(git grep -n -E '^GUARD_(DOCKER_BUDGET|RAM_[A-Z_]*|AGI_SESSIONS_ARCHIVE|SWEEP_[A-Z_]*|TIER_[A-Z_]*)_encryption_town' -- .agi/nodes/.geometry/guard.md)"` (the 15 N/A keys have no E line), and `test -z "$(git grep -n -E '^GUARD_[A-Z_]*_encryption_town=.*(/mnt/|/data/work/agi|[$]HOME)' -- .agi/nodes/.geometry/guard.md)"` (no E value is a local-town path, except one belam names for E, listed in the THOUGHT).

## Out of scope
Installing layer 5 or running guard-init.sh (root, belam's) · the hub route (goal:g7.16.1.11.25) · item (5), the egress watchdog, already graphed by belam (6a830b2fbf) · editing the peer list in hosts.json.

## RULE SM placement 04:3xZ 10-09, from belam [owner] 04:2xZ (the text below is SM's relay; its cites are SM's: its ":86-117" is short, the local-town span is :86-129, and the sanctuary-watch peer list is :79-89, not :76)
"(B) config:guard E LINES before guard layer 5 (sanctuary-watch) is installed: .agi/nodes/.geometry/guard.md carries per-box keys _local_town (:86-117: DOCKER_BUDGET, PSI_FULL, OOMD_LIMIT, USER_HIGH_PCT, RAM_*, SWEEP_PAIRS, TIER_HOT) and only ONE _encryption_town key (:79 PEERWATCH_CLAUDE); E has no RAM disk (no RAM_* lines apply). A build leaf; the values are belam's (box facts)."

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-10 02:5xZ: RE-CUT 3 on SM's 01:3xZ return (B5). F1 was `git grep -c` over the whole guard.md: five `_encryption_town` lines in the THOUGHT block, or one key repeated five times, made it green. It now reads the guard.env fence only (the range is the block's first comment line to the closing bare fence, written with a [[:punct:]] class so the command holds no backtick) and counts distinct keys. Same wanted set as re-cut 2 (PEERWATCH_CLAUDE + PSI_FULL, OOMD_LIMIT, USER_HIGH_PCT, ENGINE_MAX); everything else carried. Previous versions: re-cut 2 10-09 06:3xZ, re-cut 1 05:5xZ.
<!-- THOUGHT:END -->
