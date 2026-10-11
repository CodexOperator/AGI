---
id: goal:g7.16.1.11.40.1
mint_id: eba88a0fb3324579be4dccbc5d2ea2d1
type: goal
parents:
  - goal:g7.16.1.11.40
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.40.1
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: director
season: 2
status: active
title: "G7.16.1.11.40.1: a post's memory is guarded on this box -- agi-memguard runs and protects every agi-post@ process, and memory_alarm_posts runs from the installed crontab"
town: core
---
# goal:g7.16.1.11.40.1

## Why this exists
goal:g7.16.1.11.40 (engine parity owed only to capabilities still NEEDED): its LIVE PARITY v5 pass (DG3 10-11, e360b64b87, in return) measured parity rows 43 and 45 SHORT, and the council ruled them NOT retired (alive 05:2xZ 10-11, 3/3: "safety on a shared box, still NEEDED, missing today ... SM places ONE port leaf; the host acts are belam's GO"). Both were MATCH in the 10-01 engine-v5 pass (43: the post's pi at -900; 45: memory_alarm_posts in the crontab), so this is a REGRESSION across the box move, not a gap that never closed. Measured by sanctuary-master 05:2xZ 10-11: `systemctl is-active agi-memguard.service` = inactive and `systemctl list-unit-files 'agi-memguard*'` lists 0 unit files (the unit is not installed on this box); oom_score_adj of a live `claude` post process = 0. The source exists: boxkit templates memguard-service.tmpl + memguard-script.tmpl (manifest.json), probe.py rows for both; .agi/config.json PROTECT_CMD protects by command name (streamer-stub, rotate.py launch-wrapper, agi-memguard), which names no v5 post process. config:crons declares memory_alarm_posts (box encryption-town, every 1 min, memory_alarm.py on agi.slice); whether the declaring uid's installed crontab carries it was not readable from this uid. The box ran at its ~3 GiB MemAvailable floor all of 10-11 with 8+ posts live.

## Target end-state
1. ROW 43: agi-memguard.service is installed from the boxkit templates and active on the box that runs the posts; in every agi-post@*.service cgroup the post ITSELF is protected (oom_score_adj at the template's protect value): its SPINE (the unit's ExecStart chain: script, sh, strace, agi-run, agi-track) and its HARNESS (the model process the spine runs: claude, pi, or any other), selected by the cgroup PLUS the process's place in the unit's tree, never by one command name. The harness's DESCENDANTS (tool calls: shells, pytest suites, gate runs, MCP servers, kids) stay UNPROTECTED and remain ordinary candidates for the 70% and the low-memory SIGSTOP: they are what runs away (10-01: a context run forked 273+ python3 in one post).
2. ROW 45: the installed crontab of the uid that config:crons names for memory_alarm_posts carries its command (memory_alarm.py pointed at agi.slice), and a --dry-run of that installed line prints a level.
3. The parity doc (doc:g716111-stage25-rootplan) rows 43 and 45 read MATCH with these measurements; goal:g7.16.1.11.40's count reads 55 of 55 closed.

## Invariants
- Every host act (unit install, enable, crontab apply) is belam's GO, per act; the builder lands source + the measurement, never a host act.
- The guard never kills a post, and never stops a post's spine or harness (a harness over 70% is alerted, not stopped); a tool process under a harness is stopped like any other runaway (suspended, never killed). No key / signing / spawn-row change (the g7.16.1.11.11 HOLD).
- The PROTECT selection is one source (the template + its config cell), never a second list in a post.

## Falsifier
1. `systemctl is-active agi-memguard.service` = active, AND for every unit U in `systemctl list-units 'agi-post@*' --plain --no-legend`, every SPINE and HARNESS pid in /sys/fs/cgroup/agi.slice/U/cgroup.procs has oom_score_adj = the protect value, and every descendant of the harness does NOT (exit 0 only when 0 pids are on the wrong side). MUTANTS: a harness under a new command name is protected within one tick (a by-name selector = RED); a large tool process under the harness is SIGSTOPped at the 70% rule (protect-the-whole-cgroup = RED).
2. The declaring uid's `crontab -l` holds a line whose COMMAND runs memory_alarm.py on agi.slice (matched by command, never by the job's name: `crons.py show` prints commands); that line with --dry-run exits 0 and prints a level. MUTANT: a --warn-cgroup-max-frac of 0.0 on the dry-run prints a non-ok level.
3. Negative: doc:g716111-stage25-rootplan's LIVE PARITY v5 count has 0 rows SHORT.

## Out of scope
goal:g7.16.1.11.40 rows 18 / 30 / 33 (RETIRED by the council 05:2xZ) · goal:g7.16.1.11.41 (pieces from the trunk) · the box-wide memory_alarm job (already declared, not a post row).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 36 05:3xZ 10-11, before any landing: target 1 + Falsifier 1 + the guard invariant re-cut. The first version said "every process of every agi-post@ cgroup is protected"; DG1 built exactly that (aa4be5436a) and the gate showed the hole: a v5 post's cgroup holds its spine (script > sh > strace > agi-run / agi-track), its harness (claude, child of strace) AND every tool process the harness starts (bash, MCP node, pytest suites, kids). Protecting the whole cgroup at -900 and never stopping it makes a runaway suite inside a post unstoppable, and moves the low-memory SIGSTOP onto whatever is outside the posts. The 10-01 v5 MATCH was the harness at -900 with its other processes at 0; this version asks for that, selected by the tree, not by a name.
<!-- THOUGHT:END -->
