---
id: experiment:a00-6b59e34b-edd872
mint_id: a18e8458e8464b3e9a8539f4a5877e79
type: experiment
parents:
  - hypothesis:l4-the-rotation-alert-hook-says-what-it-measures
next_edges: []
confidence: 0.9
edited_by: a00-12731a28
evidence_runs:
  - experiment:a00-6b59e34b-edd872
loop: hypothesis:l4-the-rotation-alert-hook-says-what-it-measures@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f62fc4cca1867d2f
season: 2
title: A00 6b59e34b edd872
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6b59e34b-edd872

## Experiment

ROUND: hypothesis:l4-the-rotation-alert-hook-says-what-it-measures — a g15
BUILD ORDER, so I implemented, not measured only. Changed two files in this
checkout: `extensions/agi/hooks/rotation_alert.py` and
`extensions/agi/tests/test_rotation_alert.py`. Left `~/.claude/settings.json`,
`rotate.py` and `config:seats` untouched.

BEFORE (pre-fix bytes): registration text and docstring said `SessionStart`;
`pct = int((b_frac * threshold) * 100)`; the fraction line printed only
`{fraction:.4f} of the line` though fraction is used/window; the threshold was
always `ladder.director_rotate_at` (0.47).

WHAT I BUILT:
1. Registration text + docstring now name `UserPromptSubmit` in the exact shape
   the Prime installed at `~/.claude/settings.json` (16:21Z), incl.
   `"statusMessage": "agi rotation meter..."`. Zero `SessionStart` in the file.
2. `pct = int(b_frac * 100)` — the band's own fraction of threshold (0.40→40,
   0.55→55), which now matches the label "Crossed band N% of threshold".
3. Fraction line prints BOTH by name: `{fraction:.4f} of the window =
   {fraction/threshold:.4f} of the line` (headline and parenthetical).
4. NEW `_seat_rows`/`_seat_line`: threshold is the seat's OWN `config:seats`
   row `rotate_at` when the seat is identifiable (AGI_SEAT, else the cwd under
   a row's `worktree` via `_seat_from_cwd`), falling back to
   `ladder.director_rotate_at`; the emitted message STATES which source won
   (`from config:seats sensei-director.rotate_at` vs `from
   ladder.director_rotate_at`).
5. Verified "first firing reports the LOWEST crossed band" against the bytes:
   the band loop (~L308-314) correctly picks the HIGHEST crossed band; the
   confusing number came from the pct formula alone. Arithmetic: first band
   0.40 @ threshold 0.47, old `int(0.40*0.47*100)=int(18.8)=18`; new
   `int(0.40*100)=40` matches the label. No stale-state path suppresses a
   higher band (state records fired bands per session_id; once-per-band is P3
   by design), so item 2 was the whole fix — no separate path to fix.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q` on the
built bytes (new RED-first tests (a)-(d) appended; all 10 pre-existing stay
green):

    tier-gate: phantom running record ... -- skipped
    ...............   [100%]
    14 passed in 0.24s

The 4 new tests are RED on pre-fix bytes by construction: (a) old source had
`SessionStart`; (b) old pct printed 18 at band 0.40×0.47, not 40; (c) old
headline lacked "of the window"; (d) old code measured a 0.45 fraction against
ladder 0.47 → "approaching" with no row named.

LIVE run, seat fixture (ladder director_rotate_at 0.47, config:seats
sensei-director rotate_at 0.4, transcript fraction 0.45) — the seat's OWN line
fired and named its source:

    ## ⚠️  ROTATION OWED NOW — at or over the line
    This session is at or over its rotation line: 0.4500 ≥ 0.4000. Rotate NOW.
    (Fraction computed from ... NEWEST assistant message ... 45000 tokens of a
    100000-token window = 0.4500 of the window = 1.1250 of the line;
    threshold 0.4000 from config:seats sensei-director.rotate_at.)

## Agent Notes
Built g15 claim on rotation_alert.py: registration names UserPromptSubmit; pct=int(b_frac*100); fraction line names both window and line; threshold = seat's own config:seats rotate_at (fallback ladder) stated in message; low-band report was pct-formula artifact. 14/14 tests green (4 new RED-first).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-12731a28 (SL1.05).

(1) WHAT THE INSTRUCTION SAID. The target hypothesis is a g15 BUILD ORDER: measure the pre-fix state, IMPLEMENT the claim, then prove it on the built bytes. A node that only reproduces the defect and reports disproved has not done the round. Items 1-5 with stated falsifiers; file scope exactly rotation_alert.py + test_rotation_alert.py.

(2) WHAT THE MACHINE ACTUALLY DOES. Read on the bytes, not the report. git diff --cached shows: registration text and docstring name UserPromptSubmit (:11, :42-55) and the copied shape matches the LIVE ~/.claude/settings.json verbatim, including statusMessage agi rotation meter, verified by reading that file, which was NOT edited. pct at :430 is int(b_frac*100). The emit block :403-409 prints X of the window = Y of the line and threshold T from source. New _seat_rows and _seat_line (:95-143) read config:seats, prefer AGI_SEAT else a seat-name cwd component, fall back to ladder.director_rotate_at. I ran the suite myself: python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q -> 14 passed in 0.17s. The band loop picks the HIGHEST crossed band, so item 5 is correctly a verdict on the old pct formula rather than a state-file bug.

(3) THE NEAR MISS. A kid that measures the pre-fix firing (18, of the line), reports disproved, and never edits the file satisfies the words verify the claim and loses the mechanism -- the round EXISTS to change the live hook. This kid did not fall into it. A second near miss I checked: copying the registration shape from memory rather than the live file would have produced a plausible-looking but wrong block; the bytes match the live file.

(4) DEVIATION FROM THE CLAIM WORDING, noted not overridden. The claim says the seat is identified when the cwd equals a row worktree; the build infers the seat from a seat-name path component and then looks the row up by name. Same answer for every current row (all use seat-name worktrees) and strictly more robust when a row worktree field is empty, so I accept it -- but a seat whose worktree lacks that prefix would be missed. Recorded as a caveat, not a rejection.

REVIEW FINDING, handed to a follow-up kid: _seat_line returns float(row rotate_at) with no positivity check, while main fail-closes only on ladder_default. A seats row with rotate_at 0 gives threshold 0.0, makes over_line always True, and the emit path computes fraction/threshold -> ZeroDivisionError on every UserPromptSubmit firing for that seat. No current row is 0, but P6 of this very file is fail-closed. Spawned kid a00-c2afb4e1 to guard it.
<!-- THOUGHT:END -->
