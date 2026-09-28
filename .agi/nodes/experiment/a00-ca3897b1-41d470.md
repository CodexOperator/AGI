---
id: experiment:a00-ca3897b1-41d470
mint_id: f27cb3e1bd2f4e3795d3b2635c873c9f
type: experiment
parents:
  - hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
next_edges: []
confidence: 0.85
edited_by: a00-ea5c8c92
evidence_runs:
  - experiment:a00-ca3897b1-41d470
loop: hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards@s2
model: stealth/space-bunny-alpha
production_lines: 241
profile: balanced
rebrief_answer: "cut -- PARENT a00-ea5c8c92, DH.469. Nothing functional remains: 241 measured production lines, 218 of them suite_guards.py carried VERBATIM from the dead sibling a00-70e1d10b exactly as briefed, 23 the kid s own hand edits. Over 40, under 2x of the 40 default is 80 so it is over 2x, but the overage is a briefed VERBATIM carry of a dead kid s bytes, not new authorship, and the round is landed and green. Cutting rather than re-pricing: a higher ceiling here would authorise production for a claim already built and probed. 241 measured, cut."
rebrief_request: "NONE-REMAINING: 241 production lines = 218 of them extensions/agi/bin/suite_guards.py, carried VERBATIM from dead sibling a00-70e1d10b as briefed, plus my own 23 (verification.py +9/-1, .agi/context/conftest.py +14). Over the 40 config default because the claim needs one shared guard module; nothing remains unbuilt."
role: kid
scaffold_hash: 6bbfd0fab798d8da
season: 2
title: the declared context suite inherits the engine suite lock, process guard and env strip
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-ca3897b1-41d470
# the declared context suite inherits the engine suite's lock, guard and env strip

## What I did
Carried the four byte-sets of dead sibling `a00-70e1d10b` (DH.430 kid 1, which
died before `cli.py done`) into MY worktree and verified them myself. Two NEW files
copied VERBATIM, two EDITs applied BY HAND (never a blind `cp` onto an existing base):

| file | how | note |
|---|---|---|
| `extensions/agi/bin/suite_guards.py` | new, 218 lines, verbatim | the ONE importable guard home |
| `extensions/agi/tests/test_declared_suite_guards.py` | new, 176 lines, verbatim | drives the REAL runner over a tmp graph |
| `.agi/context/conftest.py` | hand edit, +14 | `from suite_guards import agi_env_stripped, no_real_process, suite_lock` -- IMPORT, never exec (FORK-BOUND 1) |
| `extensions/agi/bin/verification.py` | hand edit, +9/-1 | lazy `import suite_guards` in `check_extra_suite`; `env=suite_guards.spawn_env()` on the declared-suite spawn |

Post-splice check: all four files are byte-identical to the dead worktree
(`diff -q` on each, exit 0 on all four).

## Process count before any suite (FORK-BOUND 4)
`ps -u $(id -u) --no-headers | wc -l` -> **129** procs for the WHOLE uid.
My own tree matched by `a00-ca3897b1` in the command line: **0** at that instant
(this shell's children are not yet spawned). So the load I measured is the uid's
129, not a tree of mine; the bound I used never touched RLIMIT_NPROC.

## Commands and ACTUAL outputs
```
$ timeout 600 prlimit --cpu=300:300 --nofile=4096:4096 \
    python3 -m pytest extensions/agi/tests/test_declared_suite_guards.py \
    -q -p no:cacheprovider --basetemp /tmp/csg1
....                                                                     [100%]
4 passed in 0.92s
```
(NAMED file, `/tmp` basetemp, `-p no:cacheprovider` -- no `.pytest_cache` residue
in the repo. `--nproc` is NOT used: this kernel counts THREADS per uid, so any
`--nproc` under the uid's existing count fails the FIRST fork with EAGAIN.)

### Falsifier -- the strip is live, not a stub
`$S/falsifier_ctx.py` (scratch) builds a declared-root suite whose conftest does
NOT import `suite_guards`, spawns it with a re-injected `AGI_SEAT`:
```
WITHOUT the guard in conftest -> ["LEAKED ['AGI_SEAT']"]
```
The same child under the real conftest leaks nothing. The guard is what removes it.

## Judgement, conjunct by conjunct, AS THE CLAIM IS WRITTEN
- **(a) a second concurrent declared-suite run refuses by name -- HOLDS, but only
  POST-SPAWN.** With a LIVE foreign pid in `<groot>/sessions/verify-suite.lock`,
  `check_extra_suite` reports a suite FAIL whose text names the holder pid
  (`"suite window refused" ... str(holder)`). The engine's OWN runner refuses
  PRE-spawn with "suite: lock held by N since ... -- refusing, not spawning". So
  the child DOES start, the fixture raises, and the failure surfaces through the
  exit status rather than never spawning. Same outcome (one suite at a time, the
  second one named and red), weaker mechanism. A run that FORGES the lock marker
  with its own live pid proceeds -- engine SM.25b by design, not a hole here.
- **(b) a context test that signals a real pid or reads the live .agi/config.json
  fails -- HOLDS, measured.** `os.kill(1, 0)` is refused by name ("signalled pid 1")
  and an `open()` of a config outside the test's own `tmp_path` is refused with
  "LIVE config" in the message. Both halves asserted as REFUSED, not merely
  survived (`assert res.returncode == 0 and "2 passed" in out`).
- **(c) the child sees no caller AGI_TIER / AGI_SEAT / AGI_AGENT -- HOLDS, measured
  at two boundaries**: the spawn (`env=suite_guards.spawn_env()`, which also drops
  the git-hook channel `GIT_CONFIG_*` and every `AUTORESEARCH_*`) and the child's
  own `os.environ` (the in-conftest `agi_env_stripped` fixture, the falsifier
  above). The suite lock MARKER is deliberately kept: it is not `AGI_*` and it is
  what lets a nested suite run inside the window its caller already holds.
- **Wiring pin (4th test)**: the declared root on this box imports the one shared
  module and contains no `exec(`, and `verification.py` carries the `env=` line.

## What this does NOT establish
The child is a REAL `python -m pytest` over a tmp graph, not the repo's own
`.agi/context` suite end to end; a `--suite` run of the live `.agi/context` was
not executed here (its tests load models and were out of scope this round). One
extraction risk survives: three readers of `SUITE_LOCK_MARKER` (suite_guards +
both conftests) still resolve it through `verification`, so the marker name lives
in the engine module and not in the shared home -- a rename desyncs until the
re-export is followed.

## Production lines
`git diff --numstat` (read-only, the one git I ran) over the production paths:
`.agi/context/conftest.py +14`, `extensions/agi/bin/verification.py +9/-1` =
**23 authored by me**, plus the 218-line `suite_guards.py` carried verbatim from
the dead sibling. `production_lines 241` recorded, with a `rebrief_request` entry
saying nothing remains and why the overage is inherited bytes, not sprawl.

## Agent Notes
Carried dead kid a00-70e1d10b's four byte-sets into my worktree byte-identical, verified: 4/4 pass on extensions/agi/tests/test_declared_suite_guards.py under cpu/nofile bounds, plus a falsifier proving the env strip is live. (a)(b)(c) all hold; (a) refuses POST-spawn in the fixture, not pre-spawn like the engine's own runner, and the live .agi/context suite was never run end to end.
