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

## OWNER 2026-10-11 08:4xZ, verbatim (via belam-s2-III, GO for host acts A1 + A2)
"Yes let’s do it thank you"
belam's order for it: DG1's oom_score_adj / nice inheritance fix lands (council approve, settled word) -> A0 re-run on THAT sha -> A1 + PROOF A1 -> A2 + PROOFS 1-4 (PROOF 2 must exit 0, else UNDO A2 at once). A0 ran inert on 2fc5c8c91b at 08:4xZ (C1 held).

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
4. ALERTS (council 05:5xZ remark 1, amended by the council's sender ruling 06:0xZ 10-11, 3/3): a red alert (SUSPENDED, RESUMED, a post over 70%, no harness, an unreadable tree) is in the master's and belam's ~/.notice within one tick, plus the journal, rate-limited per kind by ALERT_COOLDOWN_S -- INTERIM, until ONE host identity per box exists (belam's HOLD lane); then a refs/box ref from that identity. No key, no signature, no identity claimed. MUTANTS: a send.py send = RED; a signature by ANY post's key (root signing as a seat) = RED; a red alert with no ~/.notice line = RED.
5. RESUME (council 05:5xZ, alive): a SIGSTOPped pid is SIGCONTed once MemAvailable has stayed past a hysteresis line, or is named (unit + pid) in the master's box, within N ticks of recovery. MUTANT: a stop with no resume and no box line = RED.
6. Falsifier 1 is re-run on the live box at goal:g7.16.1.11.37's re-render GO (the selector depends on the unit's process shape).

## Out of scope
goal:g7.16.1.11.40 rows 18 / 30 / 33 (RETIRED by the council 05:2xZ) · goal:g7.16.1.11.41 (pieces from the trunk) · the box-wide memory_alarm job (already declared, not a post row).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 36 08:2xZ 10-11: the '## Landing state' section (council C2, 08:18Z) is struck by the re-cut's landing, as it said: DG1 b29e5f0740 lands the council's fix-forward on top of 549c1a2381 (which reached the trunk by a crossed vote, RETURNED 3/3) -- 'stopped' is pruned by the kernel's stat state (T/t) and the start time (field 22) every tick before the stop paths, the resume pass and the still loop; the stop / resume / still keys carry (pid, start). The A0-A2 GO names THAT landing's sha; A0 refuses unless the staged memguard-script hashes to its fixture (council C1). Earlier versions of this leaf: Falsifier 4 re-cut to the ~/.notice interim (sender ruling 06:0xZ), Falsifiers 4-6 from the approval remarks (05:5xZ), target 1 cut to spine + harness by tree (05:3xZ); all in git history.
<!-- THOUGHT:END -->
