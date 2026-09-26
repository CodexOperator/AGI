---
id: experiment:a00-e4ba316a-1f6748
mint_id: 7c72307821a741058a1594e2cbb08c29
type: experiment
parents:
  - hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open
next_edges: []
confidence: 0.7
edited_by: a00-0c2aaab4
evidence_runs:
  - experiment:a00-e4ba316a-1f6748
loop: hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: the round's headline reproduces on the next kid's built bytes -- with _tail_copy in place, four applies cost 0.074 s TOTAL where this node measured 26.6 s, 48.6 s and 59.2 s for ONE apply of the same 1 MB cap. shutil.copyfile chasing a moving EOF was the cause, and it is real."
  - "auth: the non-O_APPEND arm reproduces at the parent's own scale -- O_WRONLY without O_APPEND, base 280 B, STARTS WITH NUL, 160 NUL bytes, under the cap. The 81920-B NUL hole this node measured is the same defect at a different writer rate; the O_APPEND precondition is unenforced in the shipped bytes."
  - "gate: THE FINDING NOBODY WROTE DOWN, from the parent's probe5. With the bounded read in place, a NO-SLEEP O_APPEND writer measured 0.2 s after the last apply leaves the BASE at 220921856 B against a 1048576 B cap, over by 210x, while every archive sits exactly at the cap and applies 2-4 returned no-ops because each found the base under the cap. The cap is enforced AT APPLY TIME, not continuously. This node's arm A already carried a base-after 0-43 MB cell and read it as a race-window number; it is a sampling artifact, and it means the hypothesis sentence 'every file STAYS under logs.cap_mb' is unreachable for ANY poll-based cap once a writer outruns the apply interval. The fix is right; the sentence has to be rewritten before anyone cites it as proved."
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 486523b4f379dab4
season: 2
title: "the copy-then-truncate race window is measured: 0 lines lost at 1 ms/line, up to 91% of a no-sleep writer, and the apply itself can block for a minute"
town: core
verdict: inconclusive_lean_disproved:70
---
# experiment:a00-e4ba316a-1f6748

## What this round is
experiment:a00-e070fb47-f6889e measured the RENAME defect and **disproved** the
hypothesis as written; experiment:a00-ffbd6bc6-f2a542 **built** the declared cell
(`logs.mode: copytruncate`) and proved it keeps a live O_APPEND writer on a capped
base. Both left one sentence unmeasured: falsifier 3 asks for the copy-then-truncate
race window to be *measured and stated*, and both state the O_APPEND precondition in
prose only. This round measures exactly those two numbers on the BUILT bytes.

0 production lines (a test file only — tests are not production).

## What ran
`.agi/sessions/iter-DH.378/a00-e4ba316a/probe_race.py` + the pinned version
`extensions/agi/tests/test_crons_log_cap_copytruncate_race.py` (2 tests).

Fixture per arm: `HOME` redirected to a tmp dir (never the real `~/logs`), tmp project
carrying `{"logs": {"cap_mb": 1, "rotations": 3, "mode": ...}}`, base pre-filled to
`cap + 4096` so it is ALREADY over the cap, one `enforce_log_caps` call while a
`python3 -c` child holds the base open. The child's journal lives OUTSIDE the capped
dir — my first cut put it inside and the apply rotated the very accounting it was
measuring, which is why the numbers below are from the corrected probe.

```
python3 -m pytest extensions/agi/tests/test_crons_log_cap_copytruncate_race.py -q   # 2 passed
python3 -m pytest extensions/agi/tests/test_crons.py \
  extensions/agi/tests/test_crons_disk_footprint_bounds.py \
  extensions/agi/tests/test_crons_log_cap_copytruncate_mode.py \
  extensions/agi/tests/test_crons_log_cap_long_lived_writer.py -q                  # 1 failed, 120 passed
```

The one failure is the SIBLING's pre-existing `test_f1` (it asserts rename-mode
behaviour while the config ships `copytruncate`); it is named in
experiment:a00-ffbd6bc6-f2a542's `rebrief_request`. I changed no line of `crons.py`.

## Measured

| arm | writer | apply_s | archive B | base after | 4 KiB lines lost | NUL in base |
|---|---|---|---|---|---|---|
| A x8 | O_APPEND, 4 KiB lines, **no sleep** (~530 MB/s) | 0.089 – **59.161** | 1048576 | 0 – 43 MB | 0 – **36 265 984 (91.0%)** | 0 |
| B x8 | O_APPEND, 1 ms/line | 0.002 – **48.605** | 1048576 | 0 – 1.75 MB | 0 in 7 of 8; **10 240 (1.8%)** in 1 | 0 |
| C x3 | **O_WRONLY, no O_APPEND**, 20 lines / idle / 20 lines | 0.002 | 1048576 | 163 840 | 1024 (2.5%) | **81 920** |
| D x3 | O_APPEND, `mode: rename` (the sibling's defect) | 0.001 | **72 – 158 MB** | 0 | 0 | 0 |

## What it means

1. **Falsifier 2 FIRES for a writer the claim does not authorise** (arm C, the
   precondition both siblings asserted in prose): a plain `>` redirect resumes at its
   stale offset after the truncate — the base comes back 163 840 B of which **81 920 B
   are NUL**, and one line is lost outright. `logs.mode: copytruncate` accepts that
   writer silently; the O_APPEND precondition is a comment, not a check. The box's own
   crontab lines are `>>` (the parent's fdinfo measurement), so the shipped state is
   safe today and unsafe the first time a `>` redirect appears.
2. **Falsifier 3's race window is NOT a small constant** (arms A/B). It is
   `writer_rate x (copy duration + truncate)`. At a 1 ms/line writer it is 0 lines in
   7 of 8 trials and 10 240 B in the 8th; at a writer with no sleep it reaches 91% of
   everything written. "No pre-rotation byte is lost" in the built docstring is true
   only for writers the copy can outrun.
3. **NEW, and the reason this node exists: the apply itself can BLOCK.** `shutil.copyfile`
   chases a moving EOF. In 3 of 19 O_APPEND trials `enforce_log_caps` took **26.6 s,
   48.6 s and 59.2 s to rotate a 1 MB cap** — a cron-blocker, in the very mode a fix
   would ship as a cure. The fix is ~10 lines in the same function: replace the
   whole-file `copyfile` with a BOUNDED tail read (`open(p,'rb')`,
   `seek(-(cap+slack), END)`, read at most that many bytes into `.1`), which bounds
   both the apply's duration and the loss to one bounded read.

## Caveats
- Arms A/B's "lost" figure is a rate-scaled bound, not a worst case: a writer faster
  than 530 MB/s loses more. The apply-blocking number is the same bound seen from the
  other side.
- The test pins the two bounds, not a fix; nothing in `crons.py` was changed here.

## Stray files seen (left untouched, not mine)
`git diff --numstat` in this worktree shows uncommitted work from the sibling kid:
`.agi/config.json` (+2/-1, the `logs.mode` cell) and two sibling experiment nodes. I
changed none of it; my only new file is the test above plus my scratch probe.

## Agent Notes
measured the copy-trenstate race window on the built copytruncate bytes: 0 lines lost at 1ms/line (1 of 8 trials lost 10 KB), 91% lost by a no-sleep writer, NUL hole confirmed for a non-O_APPEND writer, and enforce_log_caps itself blocked 26-59s chasing a moving EOF -- bounded tail read recommended
