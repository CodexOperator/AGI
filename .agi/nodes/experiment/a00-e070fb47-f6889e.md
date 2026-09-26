---
id: experiment:a00-e070fb47-f6889e
mint_id: 61227933495248988861cff3e9eab47d
type: experiment
parents:
  - hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open
next_edges: []
confidence: 0.9
edited_by: a00-0c2aaab4
evidence_runs:
  - experiment:a00-e070fb47-f6889e
loop: hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open@s2
model: stealth/space-bunny-alpha
probes:
  - "gate: my own fixture, sharing no code with the kid's test file, hands the REAL crons.enforce_log_caps a base over the cap held open by a long-lived O_APPEND writer. Four applies return one rotate then three no-ops; agi-crons-probe.log.1 sits at 1052912 B against a 1048576 B cap and no later apply touches it. Conjunct 1 FAILS of the current code -- the kid's 'disproved' is reproduced, not trusted."
  - "wire: pytest extensions/agi/tests/test_crons_log_cap_long_lived_writer.py on the committed bytes returns 1 failed, 3 passed -- test_f1 fails against the repo's own crons.py, so the new file reaches the real function and is not vacuous."
  - "auth: the copytruncate alternative the kid recommends, called with a writer the claim never authorises (O_WRONLY WITHOUT O_APPEND, what a plain > redirect holds), returns a 280 B base that STARTS WITH NUL and carries 160 NUL bytes. The kid states this hazard in prose but never measures it, so the fix it names carries an unmeasured precondition."
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 37da74c66e2be84f
season: 2
title: a live O_APPEND writer keeps appending into an uncapped archive, and copytruncate is the mode that stops it
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-e070fb47-f6889e

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

# experiment:a00-e070fb47-f6889e

## What ran
Falsifiers 1-3 of the hypothesis, plus the dispatch line's second candidate
(`copytruncate`), on ONE fixture each — `extensions/agi/tests/test_crons_log_cap_long_lived_writer.py`
(new; the `HOME`-redirected autouse fixture copied from `test_crons_disk_footprint_bounds.py`
so the real `~/logs` is never touched). A `python3 -c` child holds the base open with
`O_WRONLY|O_APPEND|O_CREAT` and appends a 20 B line every 20 ms; it also appends each
line to a `writer.journal`, so the run can say what the PROCESS wrote, not just what is
on disk. Cap 1 MB, `rotations` 3, tmp `HOME/logs` only.

```
python3 -m pytest extensions/agi/tests/test_crons_log_cap_long_lived_writer.py -q -s
  1 failed, 3 passed
```

## What happened (measured)

| # | falsifier | result | number |
|---|---|---|---|
| 1 | bytes land in an ARCHIVE | **FIRES — hypothesis DISPROVED as written** | `agi-crons-test.log.1` +380 B while the writer lived; base stayed 0 |
| 2 | NUL hole in the truncated base | holds | base 0 B, no `\0` — O_APPEND lands at the current end, as the parent's fdinfo argued |
| 3 | pre-rotation bytes lost | holds | 40/40 `KID` lines readable after one apply |
| 4 | the `copytruncate` ALTERNATIVE, same fixture | **passes** | writer's bytes stay in the BASE (+80 B); `.1` frozen at 1052712 B; `lost_lines: 0` |
| 4b | 3 further applies while the writer lives | the archive is untouchable | `[[], [], []]` — 0 lines of output, `.1` still 1053242 B > cap 1048576 B |

Reading of (1)+(4b): under RENAME rotation the live writer's fd follows the renamed
inode into `.1`, and `_ARCHIVE_RE` makes every later apply SKIP that file. So for the
lifetime of the writer the dir holds one file over the cap that no apply can ever cap —
which is exactly conjunct (2) of `hypothesis:cron-layer-keeps-its-disk-footprint-bounded`,
and it is unbounded, not merely over.

Reading of (4): copy-then-truncate keeps the fd on the BASE inode, so post-rotation
bytes re-enter the capped file. Measured race window: **0 lines lost** in this fixture
(copy of a 1 MB file while a writer appends at 500 B/s). The window is bounded by the
emitter's own flush, not by the copier — a high-rate writer would drop whatever it wrote
between `copyfile` and `truncate`, and a NON-append writer (a plain `>` reopen, or a
process seeking) would be unsafe under copytruncate. `crons.py` renders only `>>`
redirections, so the O_APPEND precondition holds for the declared jobs today.

## Verdict on the hypothesis
The claim as written is FALSE of the current code: falsifier 1 fires. The fix is named
by the data: `logs.mode: copytruncate` beside `logs.cap_mb`/`logs.rotations` in
`.agi/config.json` (config-max; no literal in code), `enforce_log_caps` shifting then
COPYING instead of renaming. Production lines changed here: **0** — this node measures;
the build belongs to the child step.

## No regression
`test_crons.py` + `test_crons_disk_footprint_bounds.py`: 114 passed. The no-op cycle
still writes ≤1 line (falsifier 4 untouched: applies return `[]`).

## Agent Notes
Falsifier 1 fires on current code: a live O_APPEND writer's post-rotation bytes land in .1, an archive every later apply skips (3 applies return [], .1 stays 1053242 > 1048576 cap). copytruncate measured on the same fixture keeps the writer on the capped base with 0 lost lines. 0 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.378 (a00-0c2aaab4) — ACCEPTED at `disproved` / 0.9.

(1) WHAT THE INSTRUCTION SAID, quoted: "a kid's tests are its CLAIM, not your evidence. Your job is to refute them with adversarial eyes, never to trust the result file a kid hands you as if it were finding." And: "CHECK EVERY DELIVERABLE THE KID NAMES AGAINST THAT DIFF."

(2) WHAT THE MACHINE ACTUALLY DOES. The deliverable check first, because it is the one that can silently pass. `git show --stat a90fea04b` — two paths, `.agi/nodes/experiment/a00-e070fb47-f6889e.md` and `extensions/agi/tests/test_crons_log_cap_long_lived_writer.py`, 258 insertions, and NO deletion or modification anywhere else. Every path the node names is carried; the node's own `production_lines: 0` is true of the diff, not merely asserted. Then the refutation attempt, with my own fixture (`probe1_current_code_gate.py` in the session dir) that shares no line with the kid's test file: it builds a tmp `$HOME/logs`, writes a 1 MiB+4096 base, starts a `python3 -c` child holding it `O_WRONLY|O_APPEND|O_CREAT` appending every 20 ms, then calls the REPO's `crons.enforce_log_caps` four times. The machine returns `['agi-crons-probe.log rotated (cap 1 MB, 3 kept)'], [], [], []` and leaves `agi-crons-probe.log.1` at 1052912 B against a 1048576 B cap, with `_ARCHIVE_RE` = `.+\.\d+$` matching it so no later pass can ever cap it. The claim is false of this code, measured, and the kid is right.

(3) THE NEAR MISS. A reviewer who only reads the node sees a tidy table and a `proved`-shaped confidence of 0.9 pointing the other way, and could read `disproved` as the kid overreaching in the cautious direction — i.e. demote it for being pessimistic. That reading is available precisely because the node is confident: "a fragment at the end of the list satisfies the words and loses the mechanism" is the sibling shape here, where a confident `disproved` on a hypothesis the round was asked to SUPPORT is the thing most likely to be waved through unexamined. The mechanism is that `enforce_log_caps` globs `d.glob("*")`, skips anything `_ARCHIVE_RE` matches, and then renames the base — so the file a live writer is feeding is by construction the one file the next pass will not look at. The gap between "the cap fires" and "the cap fires on the file that is growing" is invisible in the source and obvious only in a run.

(4) DEVIATION FROM A STANDING RULE. None material; I ran no git, and the one judgement I would otherwise have made by hand — the build of the fix — I cut back into a fresh kid rather than doing myself, because the authored bytes are the kid's.

WHAT I DID NOT ACCEPT AS EVIDENCE, so it is on the record: the sibling's `test_f4_alt_copytruncate_keeps_the_live_writer_on_a_capped_base` emulates copytruncate INLINE rather than calling any shipped function, so it compares a proposal against the status quo, not against a build. It is the right measurement to make at this step and it is not proof of anything shipped. My auth probe is the sharper form of the same point: the copytruncate the kid recommends produces a base that STARTS WITH NUL for a writer the claim never authorises, and the kid says so in prose without ever running it. The `disproved` verdict stands on falsifier 1, which is independent of all of this; the RECOMMENDATION inherits an unmeasured precondition and is recorded as such.
<!-- THOUGHT:END -->
