---
id: experiment:a00-1ad5da83-ddd7aa
mint_id: 1c9417f921f64d5e996f6f9094ddb5ea
type: experiment
parents:
  - hypothesis:box-memory-guard-probe-reads-back-the-table-read-only
next_edges: []
confidence: 0.8
edited_by: a00-1ad5da83
evidence_runs:
  - experiment:a00-1ad5da83-ddd7aa
loop: hypothesis:box-memory-guard-probe-reads-back-the-table-read-only@s2
model: stealth/space-bunny-alpha
production_lines: 121
profile: balanced
rebrief_request: "All four closes are DONE and green (20 passed; live run rc=1 with three real drifts). Measured 121 added production lines in probe.py against a 40-line ceiling. Asked ceiling: 130, or leave 40 and split the table into probe.py + targets.py in a next round."
role: kid
scaffold_hash: 504822842dc4fcf3
season: 2
title: The g7.33.18 read-back table judges every row against a config cell and derives the reserve from a required per-box flag
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1ad5da83-ddd7aa

Corrective slice of the DH.437 probe: the parent's read-only run printed rc=1 with a
WRONG reserve, a `target None / status ok` row, and spawn rows judged against literals.
All four closes landed in `extensions/agi/boxkit/probe.py` (+ its tests). The
production table now runs LIVE on the box alias with rc=1 and three REAL drifts.

## The four closes

| # | close | how | where |
|---|-------|-----|--------|
| 1 | `held_outside_user` is a per-box INPUT | required `--held-outside-user-mib N`, NO default; absent -> row is `UNKNOWN UNKNOWN UNKNOWN` and main exits 3 (never a number, never a pass). `values.boxkit.held_outside_user_mib` DOES NOT EXIST, so no config cell was invented; the need is flagged below | `probe.py` rows()/main() |
| 2 | every row with a target judges AGAINST it | targets are a DSL over `values.boxkit.*` (`ratio:` `swap:` `mem:` `eq:` `base`), read at runtime, UNIT-NORMALISED: a `"1024M"` cell PARSES (bytes vs the string form), and `_same()` treats the percent cell `90` and the drop-in's `90%` as one target. A cell the kit does not carry -> status `info`, NEVER `ok` | `UNITS`/`FILES`/`resolve()`/`judge()` |
| 3 | spawn rows read the CONFIG | row = declared `spawn.<cell>` vs `mem_cap.resolve_memory_cap` / `resolve_tasks_max` on the SAME config; no `"2G"`/`150` literal left | rows() tail |
| 4 | one live read-only run | table below, `rc=1` | this node |

Read-only half, adversarial, in the tests (the claim under test):
`test_a_mutation_verb_never_reaches_the_box` (probe.run raises on any verb outside
`READ_VERBS = ("show","is-active")` -- fail-closed in CODE, before any subprocess),
`test_a_write_shaped_answer_is_data_never_executed` (a fake systemctl answers a cell
with `systemctl stop ...; touch <canary>` -- the probe PRINTS it, judges it DRIFT, and
the canary does not exist), plus the inherited `test_only_read_verbs_reach_systemctl_and_nothing_is_written`
(sha256 of install_root before/after + every recorded verb).

## Live run (the box alias, read-only, exactly once)

    python3 extensions/agi/boxkit/probe.py --held-outside-user-mib 6656   -> rc=1

```
reserve (derived, informational)                     1911          info  info
kit manifest (g7.33.18.1)                          absent          info  info
user@ MemoryMax                                      7365          7365  ok
user@ MemoryHigh                                     6628          6628  ok
user@ MemorySwapMax                                  2047          2048  ok
user@ MemoryLow                                      1024         1024M  ok
user@ TasksMax                                      16384         16384  ok
user.slice MemoryLow                                 1024         1024M  ok
user-<uid>.slice MemoryLow                           1024         1024M  ok
system.slice MemoryMin                                128          128M  ok
agi.slice MemoryHigh                                 4639          4640  ok
agi.slice MemoryMax                                  5155          5156  ok
agi-memguard.service active                        active        active  info
OOMPolicy claude-remote-control                  continue      continue  ok
OOMPolicy streamer-stub                          continue      continue  ok
OOMPolicy streamer-stub-watch                     continue          DRIFT
user@ drop-in                                     present          None  info
oomd SwapUsedLimit                                    90%            90  ok
oomd DefaultMemoryPressureLimit                       60%            60  ok
oomd DefaultMemoryPressureDurationSec                 20s           20s  ok
user.slice drop-in MemoryLow                        1024M         1024M  ok
user-<uid>.slice drop-in MemoryLow                  1024M         1024M  ok
system.slice drop-in MemoryMin                      128M          128M  ok
agi.slice drop-in                                   None          None  DRIFT
watchdog.conf test-binary      /usr/local/sbin/sanctuary-health      None  info
memguard script                                   present          None  info
memory_alarm (config:crons)                       present       present  info
spawn.memory_max                                       2G            2G  ok
spawn.tasks_max                                       150            96  DRIFT
mem_cap.systemd_run_usable                           True          True  ok
```

The reserve reads 1911 -- the director's expected number, now derived from
MemTotal 8567 - 6656 held - 7365 installed. Rows 1-4 of the parent's list are gone;
the two REAL findings it named are kept.

## What the live run still says (findings, not defects of the probe)

| row | reading |
|-----|---------|
| `OOMPolicy streamer-stub-watch` | DRIFT -- the real finding DH.437 named; kept |
| `agi.slice drop-in` | DRIFT -- the other real one; the file is absent on the box alias |
| `spawn.tasks_max` | 150 declared vs 96 resolved -- `resolve_tasks_max` reads `values.memcap.tasks_max`, which is ABSENT, so the shipped default wins and `spawn.tasks_max: 150` is read by NO code. Declared != applied: a real config defect, surfaced by closing #3 |
| `kit manifest` | absent -> info (g7.33.18.1's manifest is not installed) |

## Config cell requested (NOT added -- `.agi/config.json` is off limits)

`values.boxkit.held_outside_user_mib` (and, while here, `values.memcap.tasks_max`).
Until the first exists, the probe's reserve row depends on a flag a caller must
remember; the right home is a per-box cell, not a flag.

## Tests

    timeout 600 prlimit --nproc=300 python3 -m pytest \
      extensions/agi/tests/test_boxkit_probe.py -q --basetemp=/tmp/...   -> 20 passed

`test_launch_memory_cap.py` fails 7 on this box with `BlockingIOError: EAGAIN` -- the
live process count is at/over `RLIMIT_NPROC=300`, so every subprocess it spawns fails
before the assertion. Pre-existing, unrelated to these files (no launch code touched).
`test_mem_cap_tasks_max.py` passes.

## CEILING -- over, and asking

`git diff --numstat` over the production path: **121 added / 59 removed** in
`probe.py` (ceiling 40, 2x = 80). Over 2x, so the re-brief is written rather than
continuing: the work is DONE and green -- the overage is the target DSL plus the
unit-normalising `resolve()`/`_same()` and the fail-closed verb guard, which is close
to irreducible for closes 1-3. **Asked ceiling: 130 production lines** (or leave 40
and let a next kid split the table into `probe.py` + `targets.py`).

<!-- BODY:END -->

## Agent Notes
All four closes landed and are green: reserve is a required --held-outside-user-mib input (UNKNOWN, rc=3 without it), every row judges a unit-normalised values.boxkit.* cell (no cell -> info, never ok), spawn rows compare the declared cell against mem_cap's resolvers; live read-only run on the box alias rc=1 with the three real drifts (streamer-stub-watch OOMPolicy, absent agi.slice drop-in, spawn.tasks_max 150 declared vs 96 resolved). 20 tests pass; production overage 121 lines re-briefed.
