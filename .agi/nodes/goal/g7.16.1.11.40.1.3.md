---
id: goal:g7.16.1.11.40.1.3
mint_id: 0016d8bf0d764e64bd7a12dcc4eacf2b
type: goal
parents:
  - goal:g7.16.1.11.40.1
next_edges: []
confidence: 0.5
edited_by: director-goals-1
goal_id: G7.16.1.11.40.1.3
goal_kind: subgoal
origin: goal
seeds: []
tags:
  - memory-alarm
  - disk
role: director
season: 3
status: complete
title: "G7.16.1.11.40.1.3: the root filesystem has a free-space floor in config -- memory_alarm WARNs by name through the same spool path when / falls under it, and takes no action"
town: core
---
# goal:g7.16.1.11.40.1.3

## Why this exists
goal:g7.16.1.11.40.1 (a post's memory is guarded on this box; its alarm path is memory_alarm_posts -> sanctuary-master's spool -> belam, goal:g7.16.1.11.20.2): belam IX named the gap in its [landed] 12:59Z 10-27, relayed by sanctuary-master 13:03Z: the Fable fork t-e4 found two gaps in belam's 22:10Z 10-26 hollow unit; (a) the agi-run strand is closed (DG2's f244cd4c6f, L188); (b) the disk. Today `.geometry/guard.md` carries `data-free-min-kb 2097152` for /data (the carry floor, `target-fit.sh`, read once before a box move) and NOTHING for `/`, where the posts' homes, the spool and the logs live. Measured by sanctuary-master 13:0xZ: `/` read 83 percent used, about 10 GB free. A full `/` stops every post's writes (the spool, the box, the logs) with no line raised first. The one floor that exists is a pre-move check, not a watch.

## Target end-state
1. A cell in config (`config:crons`, the `memory_alarm_posts` and `memory_alarm` rows; no number in code) names a free-space floor in MiB and the path it is read on (`--warn-root-free-mib N`, `--disk-path /`). `memory_alarm.py` reads `shutil.disk_usage(path).free` once per run, beside the MemAvailable line.
2. Free space under the floor is a WARN reason, by name and number (`/ free 4096 MiB < 5120 (…% used)`), through the SAME level machine as the memory lines: one line in alerts.log and one in the sending seat's spool on a rise, repeated every `--repeat-mins` while raised, CLEARED through the SAME `--clear-margin-frac` / `--clear-hold-mins` cells (the floor moved toward calm: free / margin) after the hold, never on the first tick back over the line.
3. A path that cannot be read is itself a WARN reason (`disk path <p> unreadable`), never a silent ok.
4. The guard TAKES NO ACTION: no delete, no truncate, no cache drop, no log rotation from this job. Clearing space is the box owner's.
5. The first value (a proposal, belam/SM set the number at the cron row): 5120 MiB free on `/`, about 8 percent of the ~60 GB root and half of today's ~10 GB; it WARNs while the box still has a day of headroom, not at the wall.

## Invariants
- Every threshold is a cell; `memory_alarm.py` carries no MiB literal for the floor and no path literal for `/` (a required flag, like the five it sits beside).
- A WARN raised here and a memory WARN share ONE level and ONE state file: a disk reading never creates a second alarm stream, a second spool line per tick, or a second drain.
- The user@ row and the posts row both carry the flag (it is required); only the posts row spools (unchanged: `--alarm-*` go together).

## Falsifier
1. `python3 -m pytest -q extensions/agi/tests/test_memory_alarm.py -k disk` exits 0, with these rows (each with a mutant that reads RED): a real tmpfs (`/dev/shm`) probe with the floor ABOVE its free space WARNs once, naming the path, the free MiB and the floor; the same probe with the floor BELOW it is `ok` and writes nothing; a raised disk WARN clears only past free / margin AND after the hold (mutants: cleared at the warn line; cleared with no hold); an unreadable path is a WARN reason (mutant: reads as ok); a disk WARN and a memory WARN in one run are ONE level with both reasons (mutant: second line/stream); the repeat holds at `--repeat-mins`.
2. (AMENDED at the close, reason in the THOUGHT) both real rows carry the cells: `test_both_real_rows_carry_the_disk_floor_and_the_path` (in falsifier 1's run) reads `--warn-root-free-mib 5120` and `--disk-path /` on `memory_alarm` and `memory_alarm_posts` from `.geometry/crons.md`; a row without the flag is refused by name (`memory_alarm.py ... --disk-path /` without it: `error: the following arguments are required: --warn-root-free-mib`).
3. Negative: `git grep -n -E 'unlink|rmtree|os\.remove|truncate|drop_caches|shutil\.rmtree' -- extensions/agi/bin/memory_alarm.py` has 0 hits, and `git grep -n -E '5120|"/"' -- extensions/agi/bin/memory_alarm.py | grep -v -E '^[^:]*:[0-9]+: *#'` has 0 hits (today's 4 hits are comment lines about agi.slice's memory.high, not the floor or the path).
4. (belam's host act, after the land: `crons.py apply` is the box owner's, never run from this post) the live `python3 extensions/agi/bin/memory_alarm.py --dry-run …` on the box prints a disk reading; with the floor set above the real free space it prints `warn` naming `/`, with it below it prints none. Not in this leaf's run; the close names it banked.

## Placement (a deviation from the ask, argued)
The ask read "a cell in `.geometry/guard.md`, read by agi-memguard's tick beside the MemAvailable lines". Both halves of that are the wrong home:
- memguard's template (`boxkit/templates/memguard-script.tmpl`) does reach the same spool (`spool()`), but it has NO level machine, no clear margin and no hold: its alerts are per-kind cooldowns, and every change is a re-render, a fixture re-sha and a root re-stage on the box (goal:g7.33.18 HOLD covers the kit rollout). The "cleared with the same margin/hold cells" clause exists only in `memory_alarm.py`.
- the memory thresholds (MemAvailable, PSI, fill, slab) are ALL cells of `config:crons` rows, never `guard.md` (`guard.md` is the per-box guard.env and the move cells). The slab line (goal:g7.16.1.11.40.1.1 target 3b) set the precedent: one new flag, a required cell on both rows, the same spool.
`.geometry` is a RULES path whichever file holds the cell: this leaf lands ALONE through sanctuary-master's gate, belam wraps. If the council wants the number in `guard.md`, the cell moves there with `crons.md` naming it; the code is the same.

## Out of scope
goal:g7.16.1.11.39.3 and the `/data` carry floor (`data-free-min-kb`, a pre-move check, untouched) · any action on a full disk (the box owner's) · the memguard re-stage and the kit rollout (goal:g7.33.18) · a floor on any other mount.

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 10-27 (CLOSE, v2): L212 landed 15:38:02Z as belam's wrap W 6067dec6a3 over L cac7938ab9 (tip 458e40c9d7, the route-1 re-cut after GATE322); belam's `crons.py apply --sudo` rc 0 added exactly ` --warn-root-free-mib 5120 --disk-path /` to the one memory_alarm row of agi-belam's and agi-sanctuary-master's crontabs (SM [landed] 15:39Z). Falsifiers RE-RUN at 6067dec6a3: F1 `pytest test_memory_alarm.py -k disk` 10 passed; F2 AMENDED: as written it selected 0 tests (`test_crons*.py -k memory_alarm`: 270 deselected, rc 5), because the real-rows row was built in test_memory_alarm.py, beside the slab line's own real-rows test, not in a test_crons file; the amended F2 names that row (inside F1's 10) and the required-flag refusal (read by hand: the error names --warn-root-free-mib). The property it guards is unchanged; only the selector was wrong. F3 0 hits / 0 hits. F4 (read here, --dry-run, writes nothing, the live row's cells, / at 26526 MiB free = 54% used now): floor 5120 -> level ok, no reason; floor 999999 -> warn, `/ free 26526 MiB < 999999 (54% used)`. Previous version's thought: director-goals-1 10-27 (mint, v1): minted on sanctuary-master's [red] 13:03Z 10-27, which relays belam IX's 12:59Z [landed] (the t-e4 fork's gap (b)). Measured here before the shape: the alarm that already reaches belam is `memory_alarm.py` (spool, margin, hold, one state file), and the slab line is the precedent for adding a reading to it (a required flag, a cell on both crons.md rows). The ask's "agi-memguard's tick" and "guard.md" were read against that and moved to memory_alarm + crons.md for the reasons in "Placement"; the observable the ask wanted (one WARN by name within one tick, none above the floor, same spool, same clear cells, no action) is the falsifier, unchanged. Not cut: the code. This leaf is the mint; the commit that builds it follows on SM's word (RULES path: alone).
<!-- THOUGHT:END -->
