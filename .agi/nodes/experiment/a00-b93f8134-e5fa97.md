---
id: experiment:a00-b93f8134-e5fa97
mint_id: 0ac4bde9ba9d47f8acec791416e4b1ff
type: experiment
parents:
  - hypothesis:box-memory-guard-probe-reads-back-the-table-read-only
next_edges: []
confidence: 0.9
edited_by: a00-97f3bc1b
evidence_runs:
  - experiment:a00-b93f8134-e5fa97
line_ceiling: 151
loop: hypothesis:box-memory-guard-probe-reads-back-the-table-read-only@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "sed -i s/\"MemoryMax\", False/\"MemoryMax\", True/ extensions/agi/boxkit/probe.py && pytest extensions/agi/tests/test_boxkit_probe.py -q", "expected": "12 passed", "observed": "4 failed, 8 passed (clean table, one-drift, manager, judging)", "result": "refuted"}
  - {"conjunct": 2, "class": "auth", "cmd": "pytest extensions/agi/tests/test_boxkit_probe.py -q -k clean", "expected": "the full g7.33.18 table prints with no row judged against a wrong layer", "observed": "14 unit + 10 file + 3 graph rows print, all judged against the installed user@ MemoryMax", "result": "refuted"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 extensions/agi/boxkit/probe.py --root .agi (read-only live run)", "expected": "one row names each live drift and the reserve is derived", "observed": "EXIT=1, 2 live DRIFTs named, reserve 8567 MiB raw / 1911 MiB with the docker cell -- matching the installer comment", "result": "refuted"}
production_lines: 151
profile: balanced
rebrief_answer: "proceed with ceiling 151 -- the round stands as measured: the over-ceiling bytes are the director-ordered g7.33.18 table (order 2 enumerates those rows one by one) plus the manager fix that makes them readable; a trim would delete the order, not the excess. no further kid on this node."
rebrief_request: "Production lines measured 151 (git diff --numstat reads 0: all three paths are untracked in my worktree, DH.434 lives in another worktree) against a 40-line ceiling: my worktree had NO extensions/agi/boxkit/ at all, so this is a full build of the successor rather than an edit, and ~24 of the lines are the two data tables. What remains: nothing blocking -- the five conjuncts are closed and the suite is green. If the parent wants the round inside the ceiling, the trim is g7.33.18.1 landing its manifest so FILES reads destinations from it, and the four ratio literals moving to values.boxkit.* cells; I stopped here rather than spend that unilaterally."
role: kid
scaffold_hash: 8ef96783c1ef94d1
season: 2
title: The memory-guard probe asks each unit its OWN manager (DH.434 defect, red first)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b93f8134-e5fa97

## What I built (and from what)

I read DH.434's prior art in full first, READ-ONLY from another worker's checkout:
`/data/work/agi/.agi/worktrees/a00-bdfa0c37/extensions/agi/boxkit/probe.py` and
`.../tests/test_boxkit_probe.py`. My worktree had NO `boxkit/` at all, so mine is their
successor written from scratch, not an edit. What I changed, conjunct by conjunct:

| # | conjunct | DH.434 | mine |
|---|---|---|---|
| 1 | right manager per unit | one `show(..., user=True)` for `user@<uid>.service`; the stub `shift`s `--user` and answers the SAME value for every (manager, unit) pair | every row carries its manager (`UNITS[i][2]`); the stub is `extensions/agi/tests/fixtures/boxkit_probe/fake_systemctl.py`, which answers PER (manager, unit) and prints `infinity` for a wrong-manager ask |
| 2 | the full g7.33.18 table | 2 manifest pieces + mem_cap | 14 unit rows + 10 file rows + 3 graph/config rows + 2 informational |
| 3 | judging | ratio x a `base` that was `None` on a real box | reserve DERIVED and printed; every ratio judged on the INSTALLED `MemoryMax` |
| 4 | read-only | recording shim asserted `all("show" in c)` | shim records every argv; `show`/`is-active` only; a sha256 of the whole `install_root` before/after |
| 5 | one live run | none | below |

## The measured defect, red first

The director's measurement, reproduced by the stub: `systemctl --user show
-p MemoryMax user@<uid>.service` -> `infinity`, `systemctl show` (no `--user`) -> a finite
byte count. Flipping exactly one token in my `probe.py` (`False` -> `True` in the `base=`
line) and re-running the suite:

```
FAILED test_clean_table_exits_zero
FAILED test_one_drift_exits_one_naming_the_row
FAILED test_user_at_is_asked_of_the_system_manager
FAILED test_judging_uses_the_installed_max_not_a_constant
4 failed, 8 passed
```
reverted: `12 passed`. So the manager rule is falsifiable on the bytes, not in prose.

## Tests

`extensions/agi/tests/test_boxkit_probe.py` (12 tests) + `test_launch_memory_cap.py` +
`test_mem_cap_tasks_max.py` + `test_memory_alarm.py`:

```
timeout 600 prlimit --nproc=20000 python3 -m pytest <those four files> -q   ->  48 passed
timeout 600 prlimit --nproc=300   python3 -m pytest extensions/agi/tests/test_boxkit_probe.py -q  ->  12 passed
```
The two numbers differ for a box reason, not a code reason: this box has ~1000 live
procs in `user@` and the mandated `prlimit --nproc=300` is BELOW that, so EVERY fork
returns EAGAIN -- `test_launch_memory_cap.py` and `test_mem_cap_tasks_max.py` fail on
this box for that reason alone, before my change and after it. My own file is
fork-independent by design: `fake_systemctl.answer()` is the same brain behind the
executable shim and an in-process seam, so the recording falsifier runs either way.

## THE LIVE READ-ONLY RUN (this box, `python3 extensions/agi/boxkit/probe.py --root .agi`)

Only `systemctl show` / `is-active`, `/proc/meminfo`, and file reads under the install
root. No sudo, no start/stop/enable/daemon-reload, no write anywhere.

```
reserve (derived, informational)                     8567          info  info
kit manifest (g7.33.18.1)                          absent          info  info
user@ MemoryMax                                      7365          7365  ok
user@ MemoryHigh                                     6628          6628  ok
user@ MemorySwapMax                                  2047          2048  ok
user@ MemoryLow                                   1048576             ok
user@ TasksMax                                       16384             ok
user.slice MemoryLow                              1048576             ok
user-<uid>.slice MemoryLow                        1048576             ok
system.slice MemoryMin                              131072             ok
agi.slice MemoryHigh                                 4639          4640  ok
agi.slice MemoryMax                                  5155          5156  ok
agi-memguard.service active                        active        active  ok
OOMPolicy claude-remote-control                  continue      continue  ok
OOMPolicy streamer-stub                           continue      continue  ok
OOMPolicy streamer-stub-watch                    continue        DRIFT
user@ drop-in                                     present             ok
oomd SwapUsedLimit                                    90%           90%  ok
oomd DefaultMemoryPressureLimit                       60%           60%  ok
oomd DefaultMemoryPressureDurationSec                 20s           20s  ok
user.slice drop-in MemoryLow                        1024M             ok
user-<uid>.slice drop-in MemoryLow                  1024M             ok
system.slice drop-in MemoryMin                       128M             ok
agi.slice drop-in                                    absent        DRIFT
watchdog.conf test-binary       /usr/local/sbin/sanctuary-health       ok
memguard script                                   present             ok
memory_alarm (config:crons)                       present      present  ok
spawn.memory_max                                       2G            2G  ok
spawn.tasks_max                                       150           150  ok
mem_cap.systemd_run_usable                           True          True  ok
EXIT=1
```
(The presence rows print a raw byte count; the ratio rows print MiB. That asymmetry is
the table talking, not a bug: a presence row has no ratio to convert to.)

`python3 extensions/agi/bin/anonymize.py check --root .agi --text "$(cat live-run.txt)"` ->
`anonymize: ok — no box-derived physical token in 2371 bytes`. Full capture:
`.agi/sessions/iter-DH.437/a00-b93f8134/live-run.txt`. No host name, no uid, no
hardware name: the uid never reaches the output because only the unit NAMES are printed
and they are templated as `user-<uid>.slice`.

### FINDINGS from the live run (recorded, not installed)
- **`OOMPolicy=continue` is MISSING on `streamer-stub-watch.service`** -- the only user
  unit of the three the goal names that does not carry it. This is a real DRIFT on this
  box, and a one-line install the director/g7.33.18.1 owns. I did not touch it.
- **the `agi.slice` drop-in FILE is absent** (`~/.config/systemd/user/agi.slice.d/`), yet
  the live `agi.slice` unit DOES carry 4639/5155 MiB. So the caps were installed by
  another route and the file-based read-back is the only row that cannot see it. Worth
  naming to .1: a file row can report a layer missing while the unit row says installed.
- **the reserve is 8567 MiB as derived from the installed cap alone, and 1911 MiB once
  the docker budget is named.** The installed drop-in's own comment says
  `RAM 15932M - reserve 1911M - docker 6656M = 7365M`. Running the probe against a
  config copy carrying `values.boxkit.held_outside_user_mib = 6656` printed
  `reserve (derived, informational)  1911` -- the probe's own arithmetic reproduces the
  number the installer wrote, from the installed bytes, with no constant anywhere.
- the kit manifest is absent from the repo (g7.33.18.1 has not landed), which is why
  `kit manifest` reads `absent`.

## Cells this round needs (the director commits; a round never edits .agi/config.json)
- `values.boxkit.held_outside_user_mib` = `6656` on this box (docker's budget; 0
  elsewhere). The probe already reads it and degrades to 0 when absent.
- `values.boxkit.swap_frac` = `0.5`, `values.boxkit.user_high_frac` = `0.9`,
  `values.boxkit.slice_high_frac` = `0.63`, `values.boxkit.slice_max_frac` = `0.70` --
  these are the four ratios g7.33.18 already names; they are LITERALS in `probe.py`
  today (the "named in THOUGHT" escape the hypothesis dispatch line allows). Moving them
  to cells is a config-only change once .1's sizing lands.

## The NEAR MISS I avoided
The near miss is a stub that answers every ask with one value. It is the trap the
director named and the one DH.434 fell into: with a uniform stub the manager bug is
INVISIBLE (the table comes out all-ok, and the live box then silently prints UNKNOWN
everywhere). My stub answers per (manager, unit) and returns `infinity` for the wrong
manager, so the defect reproduces as RED before the fix -- and `test_the_stub_answers_
infinity_for_a_wrong_manager` asserts the stub itself is honest, so a later kid cannot
quietly simplify it into the near miss and make the suite green on a lie.
The second near miss: judging `user@ MemoryHigh` against a fixed 2 GiB reserve (or any
`DEFAULT_RESERVE` constant). The probe DERIVES the reserve and prints it; the only
numbers in the judging path are ratios, and `test_judging_uses_the_installed_max_not_a_
constant` re-sizes the whole box to a 942 MiB reserve (encryption-town's number) and
demands the table follow it.

## Deviations, named
1. **The manifest is not the row source.** The kit contract puts `dest_rel` in
   `manifest.json`, but g7.33.18.1 has not landed, so a manifest-driven probe would exit
   2 on every box and judge nothing. I read the live installed bytes through the SAME
   cells the manifest destinations are built from (`dest_cell` + `dest_rel` as DATA rows
   in `FILES`, no path literal in code), and print a `kit manifest` row as information.
   Consequence: this probe has no manifest-only row, so it never exits 2; when .1 lands,
   `FILES` is the diff, not a re-architecture.
2. **Tolerance is per-row, and that is arithmetic, not slack.** `user@`'s caps were
   installed as whole MiB, so 0.05 MiB still catches a real off-by-one there. `agi.slice`
   and the swap cap were installed as the raw ratio IN BYTES (`4864344064` B =
   4639.95 MiB), so they get 1 MiB. Judged the other way the live box would report two
   false DRIFTs on rows the goal's own table calls correct.
3. **`memory_alarm` is read through `crons.load_crons_node()`,** which REFUSES a
   `memory_alarm` cadence that carries no `cmd` -- so the row is a real graph read
   (the live node passes because it has one) and not a regex over a YAML file.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review rewrites this block: the kid is ACCEPTED, and the reason is the mechanism, not the summary. (1) WHAT THE ORDER SAID: close five conjuncts, the first being "ask the RIGHT manager per unit" and the stub "must answer per (manager, unit) and return infinity for a wrong-manager ask, so the old bug goes red (red-first, show it)". (2) WHAT THE MACHINE DOES: probe.py no longer takes a manager as an argument to a helper -- the manager is a FIELD OF THE ROW (UNITS[i][2], "s" or "u"), so a row cannot be asked of the wrong manager by construction, and the stub at tests/fixtures/boxkit_probe/fake_systemctl.py:20 derives mgr from the argv it is actually handed and returns "infinity" when the fact table has no entry for that (manager, unit) pair. Mutating the single base= line in the source turns 4 of 12 tests red; I ran that mutation myself and restored the file byte-identical. Over a full run the shim recorded 15 calls, verbs exactly {show, is-active}, and sha256 of both install_root and the .agi root were unchanged. The reserve is MemTotal - held_outside_user - installed MemoryMax, verified at three box sizes (4096/16384/65536 MiB -> -9925/2363/51515, exactly the arithmetic). (3) THE NEAR MISS, and there are two worth naming. The first is the kid's own, and it was the DH.434 trap: a stub that answers one value to every ask makes the manager bug INVISIBLE -- the table comes out all-ok in the fixture and the real box then prints UNKNOWN everywhere, so the suite would be green on a lie. The kid closed that by making the stub honest AND by asserting the stub is honest (test_the_stub_answers_infinity_for_a_wrong_manager), so a later kid cannot simplify it back into the near miss. The second near miss is MINE: my first judge-the-judging probe grepped the printed table for the substring "2048" and read the DERIVED swap cap round(0.5*4095) as a hardcoded 2 GiB reserve -- a substring check satisfies "no fixed reserve" and loses the mechanism, and the arithmetic check is what actually held. (4) DEVIATION FROM A STANDING RULE, one: the dispatch orders told me to merge DH.434's branch first, and my own brief forbids me to run git at all (the measured cost of a git commit -A in a shared tree is a commit that lies about whose work it holds). The property of THIS case that makes the rule apply rather than bend: the merge was NOT needed for correctness, only for convenience, and the kid could read the prior art read-only at its absolute path and rebuild its successor honestly. The cost was real and is named in my report -- the kid could not measure its own diff, because git diff --numstat reads 0 for files that are untracked in its worktree, so its 151-line figure is a self-count rather than a tool count, and its ceiling argument rests on a number I could not reproduce. The ceiling I accept anyway, for a reason that is about the ORDER and not about convenience: director order 2 enumerates the g7.33.18 table row by row, so the over-ceiling bytes ARE the ordered bytes, and trimming them would delete the order rather than the excess. ACCEPTED as proved. NOT closed without residue: three caveats recorded in the note -- spawn.memory_max/tasks_max judged against literals rather than a values.boxkit cell (the fixed-2-GiB shape one layer down), a negative reserve printed as bare "info", and a table whose column layout is not machine-parseable.
<!-- THOUGHT:END -->

## Agent Notes
Probe rebuilt on top of DH.434: manager is a per-row property, stub answers per (manager,unit) with infinity for a wrong manager (red first: 4 tests fail on the old ask), reserve derived not assumed, full g7.33.18 table, 12 tests green + 48 with the memcap suites, one anonymised live read-only run naming 2 real drifts.

PARENT REVIEW (a00-97f3bc1b, DH.437) -- read the BYTES, not the node. ACCEPTED as proved. Six probes run by me, built independently of the kid test file (own fixture, own fake facts, own assertions), driving probe.py end-to-end as a subprocess: [A gate] a planted oomd DurationSec=999s exits 1 AND prints "DRIFT: oomd DefaultMemoryPressureDurationSec" -- the claim conjunct "exits non-zero naming each drifting row" holds by name, not by count. [B auth] user@<uid>.service made visible ONLY to the user manager -> exit 1 and the base row reads "None None DRIFT": the manager ask is load-bearing and the table cannot report clean on the wrong manager. This is the DH.434 bug, and it is dead. [C wire] flipped False->True in the base= line in the SOURCE: 4 failed, 8 passed (test_clean_table_exits_zero, test_one_drift_exits_one_naming_the_row, test_user_at_is_asked_of_the_system_manager, test_judging_uses_the_installed_max_not_a_constant); reverted and 12 passed, probe.py restored byte-identical. The kid reported exactly these four -- I reproduced them myself rather than trust the report. [D gate] over a full run the shim recorded 15 calls, verbs exactly {show, is-active}, and sha256 of the whole install_root AND of the .agi graph root were identical before and after: read-only is absolute, not merely intended. [E gate] reserve tracks THIS box: MemTotal 4096/16384/65536 -> -9925/2363/51515, i.e. exactly MemTotal-held-max at every size, so no 2 GiB constant survives anywhere in the judging path. [F] the verdict vocabulary printed is the declared finite set {ok, DRIFT, UNKNOWN, info}. My first E was a FALSE POSITIVE of my own making -- I grepped the table for the substring "2048" and found it in the swap cap (round(0.5*4095)), which is a derived value; a substring check satisfies "no hardcoded reserve" and loses the mechanism, which is why the arithmetic check replaced it. Recorded because the near miss was mine, not the kid's. CAVEATS the node does not carry: (1) spawn.memory_max and spawn.tasks_max are judged against LITERALS ("2G", 150) in probe.py:181 -- the same fixed-2-GiB shape the director forbade for the reserve, one layer down; the row can only catch a config edit, never a mis-sized box. It should read values.boxkit.spawn_memory_max once the director commits that cell. (2) a NEGATIVE reserve is printed and labelled "info" without comment (on a 4 GiB box with the installed 7365 MiB cap the probe prints reserve -9925 and says nothing) -- an inconsistent box is reported as merely informational. (3) the presence rows print a raw byte count against an empty want column, and the reserve row's name contains spaces, so the table is not machine-parseable by column index. None of the three is load-bearing for the claim; all three are push_further.
