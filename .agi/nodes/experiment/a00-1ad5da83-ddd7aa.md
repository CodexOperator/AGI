---
id: experiment:a00-1ad5da83-ddd7aa
mint_id: 1c9417f921f64d5e996f6f9094ddb5ea
type: experiment
parents:
  - hypothesis:box-memory-guard-probe-reads-back-the-table-read-only
next_edges: []
confidence: 0.8
edited_by: a00-58736bab
evidence_runs:
  - experiment:a00-1ad5da83-ddd7aa
line_ceiling: 130
loop: hypothesis:box-memory-guard-probe-reads-back-the-table-read-only@s2
model: stealth/space-bunny-alpha
probes:
  - "auth: probe.run() refuses set-property x2, restart, daemon-reload, edit, stop BY NAME, no subprocess spawned (PASS)"
  - "gate: no --held-outside-user-mib -> reserve row UNKNOWN and rc!=0 (PASS); held present -> reserve falls by exactly the held delta and MemTotal-held-user@MemoryMax closes within 0.01 MiB (PASS)"
  - "wire: values.boxkit.MEM_LOW 1024M->2048M and USER_TASKS 16384->1024 each MOVE their row, so the cell drives it live (PASS)"
  - "wire: recording systemctl shim saw 15 calls, verbs exactly {show, is-active}, zero files changed under install_root or the graph root (PASS)"
  - "gate: spawn.tasks_max is judged against mem_cap.resolve_tasks_max, which reads values.memcap.tasks_max -- ABSENT on this box -- so the row DRIFTs 150 vs 96; that is a TRUE finding (spawn.tasks_max is read by no code) which the kid itself reported, and the one probe of mine whose expectation was wrong"
production_lines: 121
profile: balanced
rebrief_answer: proceed with ceiling 130
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

PARENT REVIEW DH.439 (a00-58736bab). I read the DIFF (7be9634ca..391b04181), not the result file, and ran 8 of my own negative probes (probes.py in my session dir: read-only, throwaway fixture, no real systemctl, no claude). ACCEPTED as proved.

MECHANISM, in the four parts.

(1) WHAT THE ORDERS SAID: "held_outside_user is a per-box INPUT, absent -> the reserve row is UNKNOWN, never a number"; "every row with a known target judges against it ... a row the kit has no target for prints info, never ok"; "spawn rows read spawn.memory_max / spawn.tasks_max from the config -- the cell IS the target"; "never a write"; "no host name".

(2) WHAT THE MACHINE ACTUALLY DOES, cited to the bytes and to artifacts I BUILT AND RAN:
- probe.py run() raises ValueError("probe.py refuses a non-read systemctl verb") on any verb outside READ_VERBS=("show","is-active") BEFORE subprocess is reached. PROBE A/auth: 6 mutation verbs (set-property x2, restart, daemon-reload, edit, stop) all refused BY NAME, zero subprocesses spawned (I replaced probe.subprocess.run with a raiser to prove no spawn). Fail-closed in code, not in a reviewer's good intentions.
- probe.py rows() carries held_outside_user_mib=None; without it the reserve row is the literal tuple UNKNOWN/UNKNOWN/UNKNOWN. main() returns 3 on any UNKNOWN, 1 on any DRIFT, and prints "DRIFT: <row>" / "UNKNOWN: <row>" under each offending row. PROBE B/gate: absent -> UNKNOWN and rc != 0; present -> the value FALLS by exactly the held delta, and MemTotal - held - user@MemoryMax closes to within 0.01 MiB against the box's own readings. The director's 8567 is now 1911.
- Targets are a DSL (base | ratio:cell | swap:cell | mem:cell | eq:cell | lit:v | None) resolved at runtime from values.boxkit.*, normalised through as_mib(); a missing cell returns info=True, so judge() can only return info or DRIFT, never ok. PROBE C/wire: flipping values.boxkit.MEM_LOW 1024M -> 2048M moved user.slice MemoryLow ok -> DRIFT; USER_TASKS 16384 -> 1024 moved user@ TasksMax ok -> DRIFT. The cells drive the rows LIVE; a literal would not have moved.
- PROBE D/wire-readonly: a recording systemctl shim saw 15 calls, verbs exactly {show, is-active} (plus the --user manager flag), and a full mtime+size snapshot of install_root and the graph root before/after showed ZERO files changed. The probe reaches only mem_cap._read_cached_probe (a read) and never mem_cap.systemd_run_usable, which would have spawned a 256 MiB scope AND written the probe cache.
- LIVE, read-only, once, re-run BY ME: python3 extensions/agi/boxkit/probe.py --held-outside-user-mib 6656 -> rc=1, 31 rows, three DRIFT lines named, and the table matches this node's recorded table value for value. No host name anywhere.

(3) THE NEAR MISS, as a counterfactual: leaving the sizing constants in the UNITS tuple (as DH.437 did) satisfies "prints the table" and loses the claim -- every row would still read ok against a number nobody configured, which is exactly the target=None/status=ok defect the director named. Symmetrically, calling systemctl through a bare subprocess.run satisfies "only systemctl show" in prose and loses it in the machine: nothing in the code would stop a future row asking for set-property.

(4) No standing rule deviated from.

ONE CORRECTION TO MY OWN PROBE, recorded because a probe that fails for its own reason is not evidence: my E/wire-spawn expectation (that the row should track spawn.tasks_max and stay ok) was wrong. mem_cap.resolve_tasks_max reads values.memcap.tasks_max, which is ABSENT from the live config, so the shipped default 96 wins while spawn.tasks_max declares 150. The row DRIFTs, and that DRIFT is a TRUE finding, not a false alarm -- spawn.tasks_max is read by no code. The kid named this itself, in the live table and in the findings table, and requested the values.memcap.tasks_max cell without touching .agi/config.json. I confirm it independently: probe.py:242 compares spawn.tasks_max against mem_cap.resolve_tasks_max(cfg_all); mem_cap.py:65 reads ((cfg or {}).get("values") or {}).get("memcap") or {}).get("tasks_max"); the live config's values.memcap carries only probe_cache_dir_name and probe_cache_file.

REBRIEF ANSWERED: rebrief_request -> rebrief_answer "proceed with ceiling 130", line_ceiling 130. 121 measured production lines for a four-way corrective (target DSL + unit normalisation + fail-closed verb guard) is over the 40 default, but it is one file and one coherent table; splitting probe.py into probe.py + targets.py is the better follow-up and is left to the next round rather than forced now. Answer line DM'd to the director in this round's single harvest line.

CAVEATS carried forward, not refutations: (a) the reserve row depends on a flag no config cell holds, so a caller who forgets --held-outside-user-mib gets rc=3 UNKNOWN -- fail-closed and correct, but the probe has no memory of the per-box input until values.boxkit.held_outside_user_mib exists. (b) The test recipe in my own orders (timeout 600 prlimit --nproc=300) is BROKEN on this box: it makes 7 unrelated tests in test_launch_memory_cap.py and test_mem_cap_tasks_max.py fail with BlockingIOError EAGAIN; the same 18 pass without the prlimit. The kid diagnosed this correctly and named it; the defect is in the recipe, not in the kid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-58736bab, DH.439) -- the parent's edit on top of the kid's proved node. The kid's four closes are ACCEPTED: the read-only guard is fail-closed in code (run() raises on any systemctl verb outside READ_VERBS before subprocess is reached, so no future row can reach a mutation verb), every row with a target judges against a unit-normalised values.boxkit.* cell, a row with no cell can only print info, and the reserve is a required per-box input whose absence is UNKNOWN with a non-zero exit. I re-ran the live read-only probe myself: rc=1, 31 rows, three named DRIFTs, the table matching this node value for value, no host name. WHY THIS VERSION DIFFERS FROM THE KID'S: it adds the parent's own negative probes (auth/gate/wire), the one probe of mine that was WRONG and why (I expected spawn.tasks_max to track its own cell; it is judged against mem_cap.resolve_tasks_max, which reads values.memcap.tasks_max -- absent on this box, so 150 vs 96 is a TRUE finding the kid itself reported, not a defect I caught), the answered re-brief, and the broken prlimit test recipe from the parent's own orders.
<!-- THOUGHT:END -->
