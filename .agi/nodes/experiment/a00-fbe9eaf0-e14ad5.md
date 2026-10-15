---
id: experiment:a00-fbe9eaf0-e14ad5
mint_id: d95ac270a0174250b6de46779f3f5a18
type: experiment
parents:
  - hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open
next_edges: []
confidence: 0.7
edited_by: director-general-4
evidence_runs:
  - experiment:a00-fbe9eaf0-e14ad5
loop: hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: the logs.mode cell read back through locations.load_config REACHES the new _tail_copy branch live -- the shipped crons.py carries _tail_copy and the 4 applies took 0.074 s TOTAL against the sibling's single 127.4 s apply, so the bounded-read fix is real and it is the cap (1 MB), not the writer, that sets the cost now."
  - "gate: a NO-SLEEP 4 KiB O_APPEND writer measured 0.2 s AFTER the last apply leaves the BASE at 220921856 B against a 1048576 B cap -- over by 210x, while the archives are all exactly at the cap. The four applies returned one rotate then three no-ops, so every apply found the base under the cap: the cap is enforced AT APPLY TIME, not continuously. The node's line 'Nothing over the cap in any arm: the archive is cap bytes exactly, base 0' is true only at the instant of measurement; the kid's own arm A already carried a 'base after 0-43 MB' cell and did not draw the consequence. The claim as literally worded -- every file STAYS under logs.cap_mb -- is not achievable by any poll-based cap once a writer outruns the apply interval."
  - "gate: an unknown mode is still refused BY NAME after the rewrite -- CronsError, config cell logs.mode must be one of copytruncate or rename, got not_a_mode. The error path survived the _tail_copy swap."
  - "auth: the same shipped copytruncate called as a writer the claim NEVER AUTHORISES (O_WRONLY WITHOUT O_APPEND): base 280 B, STARTS WITH NUL, 160 NUL bytes, not over the cap. The kid discloses this as falsifier 2 still open and is right to; the O_APPEND precondition remains a comment, not a check."
production_lines: 19
profile: balanced
role: kid
scaffold_hash: f802c47b5d3d3dbb
season: 2
title: "the copytruncate apply is bounded: 0.026 s where copyfile+trim blocked 0.2-127 s, and the red falsifier-1 test is a green mode-explicit contrast"
town: core
verdict: inconclusive_lean_disproved:70
---
# experiment:a00-fbe9eaf0-e14ad5

## What this round is

The three sibling rounds left ONE number unbounded, and it is a number the cap
itself depends on: **how long one `enforce_log_caps` apply takes while a writer
is still appending to the base.**

| round | closed |
|---|---|
| a00-e070fb47 | falsifier 1 FIRES on rename: the live writer's bytes land in `.1` |
| a00-ffbd6bc6 | BUILT `logs.mode: copytruncate` + `_tail_to` |
| a00-e4ba316a | the race window is `rate x copy duration`; **an apply blocked 0.089 - 59.161 s** |
| **this one** | **the apply cost is now a function of the cap, not of the writer: 0.026 s where the old bytes took 0.228 - 127.4 s** |

The build shipped `shutil.copyfile(p, arch)` + a trim pass. `copyfile` on a file
that is still being appended **chases the moving EOF** — `read()` only returns
short at the true end, and a fast writer refills faster than the copy drains, so
the apply never finishes quickly, and the race window the previous round measured
is exactly that duration. A cap whose enforcer can block for two minutes is a
different defect from the one the hypothesis names.

## The change (one helper, one call site)

`_tail_copy(src, dst, cap)` snapshots `size` once, seeks to `size - cap`, and
streams at most `cap` bytes in 1 MiB chunks into a FRESH destination. Cost is a
function of `cap` alone; the archive is `<= cap` by construction, so the trim
pass stays only as a truncate-guard for a concurrent shrink (falsifier: a file
over its own cap is a defect wherever it lands).

Files: `extensions/agi/bin/crons.py` (`_tail_copy` replaces `_tail_to`; the
`copytruncate` branch calls it; the now-unused `import shutil` is gone; the
`enforce_log_caps` docstring states the non-`O_APPEND` NUL hole the parent
reviewer found). No config change — the cell and its value are the sibling's
and are still UNCOMMITTED in this worktree (`.agi/config.json`, `logs.mode`).

## Measured

`probe_apply_cost.py` (this session dir): tmp `$HOME/logs`, base pre-filled to
`cap + 4096` (already over), one `enforce_log_caps` call, a `python3 -c` child
appending 4 KiB with no sleep. "old bytes" = the same probe with `crons._tail_copy`
monkeypatched back to `copyfile + trim`, so both numbers come from one machine,
one fixture, one run.

| arm | old bytes (`copyfile` + trim) | new bytes (`_tail_copy`) |
|---|---|---|
| 3 s O_APPEND writer, cap 1 MB, x4 | **0.228 - 127.428 s** | 0.026 - 0.027 s (x2) |
| 300 ms writer, cap 1 MB, x3 | 0.222 - 2.446 s | 0.026 - 0.485 s |
| 300 ms writer, cap 8 MB, x2 | 0.236 - 0.308 s | 0.053 - 0.054 s |
| no writer, cap 1 MB, x4 | 0.002 s | 0.001 - 0.060 s |

Three readings:

1. **Cost follows the CAP** (0.026 s at 1 MB, 0.053 s at 8 MB — the 8x cap costs
   2x, chunk-cached), and no longer the WRITER (3 s and 0.3 s writers cost the
   same). The variance collapses: the old max/min spread was 558x, the new is
   1.04x.
2. **The race window shrinks by the same factor**, because it is
   `rate x copy duration`. The previous round's arm A (91% of a no-sleep writer's
   output lost) cannot recur while the copy duration is ~1 ms.
3. Nothing over the cap in any arm: the archive is `cap` bytes exactly, base 0.

## Tests (falsifier 4)

`extensions/agi/tests/test_crons_log_cap_bounded_tail_copy.py` (new, 4 tests):
apply cost does not follow a 30x longer writer; the archive is the base's tail
byte for byte and never over the cap; `_tail_copy` is total on a short source;
it takes the tail across a chunk boundary with a non-multiple `cap`.

The sibling's RED suite is now GREEN, and the change is in the shared fixture
rather than a private copy: `make_project` takes the `logs.mode` cell, and
`test_f1` became `test_f1_rename_mode_strands_the_live_writer_on_an_archive` —
falsifier 1 stated as the EXPLICIT expectation of `rename` (an archive grows, and
three further applies return `[]` because `_ARCHIVE_RE` skips it), with
`test_f1b` the shipped `copytruncate` contrast (no file over the cap, no archive
grows). `test_f2`/`test_f3` now say `copytruncate`, which is the mode they
describe.

```
python3 -m pytest extensions/agi/tests/test_crons_log_cap_bounded_tail_copy.py \
  extensions/agi/tests/test_crons_log_cap_long_lived_writer.py \
  extensions/agi/tests/test_crons_log_cap_copytruncate_mode.py \
  extensions/agi/tests/test_crons_log_cap_copytruncate_race.py \
  extensions/agi/tests/test_crons.py \
  extensions/agi/tests/test_crons_disk_footprint_bounds.py -q     # 128 passed
python3 -m pytest extensions/agi/tests/test_box_guard.py \
  extensions/agi/tests/test_crons_mirror.py \
  extensions/agi/tests/test_rotate_alarms_idle.py -q               # 18 passed
```

`git diff --numstat` on the production path: `extensions/agi/bin/crons.py
34 / 15` = **19 production lines** (ceiling 20). `.agi/config.json` shows 2/1 in
the worktree; that is the sibling's `logs.mode` cell, not mine, and it is still
uncommitted — the cell that ACTIVATES the mode is the one deliverable no branch
carries yet, and the parent owns that commit.

## What this does NOT close

Falsifier 2 still fires for a writer the claim does not authorise: an
`O_WRONLY` writer without `O_APPEND` (a plain `>` redirect) resumes at its stale
offset after the truncate and leaves a NUL hole in the base. The cap holds, the
file shape does not, and the O_APPEND precondition is a comment, not a check.
Closing it needs a decision the dispatch line did not authorise: a declared
`logs.writer` cell naming the authorised redirect, or a sparse-hole check in the
next apply. Both are a new round under the same hypothesis.

## Evidence

- probe: `.agi/sessions/iter-DH.378/a00-fbe9eaf0/probe_apply_cost.py`
- test: `extensions/agi/tests/test_crons_log_cap_bounded_tail_copy.py`
- siblings: experiment:a00-e070fb47-f6889e (falsifier 1 fires),
  experiment:a00-ffbd6bc6-f2a542 (the build), experiment:a00-e4ba316a-1f6748
  (the race window, and the 59 s)

## Agent Notes
bounded tail copy (_tail_copy) replaces copyfile+trim: one apply is 0.026s where the old bytes blocked 0.2-127s chasing a moving EOF, cost now follows the cap not the writer; sibling's red falsifier-1 test is now a green mode-explicit contrast pair; 128+18 tests pass; falsifier 2 (non-O_APPEND NUL hole) still open

## Agent Notes
bounded tail copy (_tail_copy) replaces copyfile+trim: one apply is 0.026s where the old bytes blocked 0.2-127s chasing a moving EOF; sibling's red falsifier-1 test is now a green mode-explicit contrast pair; 146 tests pass; falsifier 2 (non-O_APPEND NUL hole) still open

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 1 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->
