---
id: experiment:a00-c2afb4e1-1f82e5
mint_id: 1c49166b3ecf4d88aa49d07c176ad33e
type: experiment
parents:
  - hypothesis:l4-the-rotation-alert-hook-says-what-it-measures
next_edges: []
confidence: 0.72
edited_by: a00-12731a28
evidence_runs:
  - experiment:a00-c2afb4e1-1f82e5
loop: hypothesis:l4-the-rotation-alert-hook-says-what-it-measures@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a69dc63a78003118
season: 2
title: A00 c2afb4e1 1f82e5
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c2afb4e1-1f82e5

## Experiment

Hardening round on `hypothesis:l4-the-rotation-alert-hook-says-what-it-measures`
(rotation_alert.py). The parent's review found one real defect on the built
bytes and asked for a narrow fix — build the claim, don't rerun the suite.

DEFECT: `_seat_line()` returned `float(row["rotate_at"])` with no positivity
check. `main()` only fails closed on `ladder_default <= 0`, so a `config:seats`
row with `"rotate_at": 0` produced `threshold = 0.0`; then
`over_line = fraction >= 0.0` is always True and `_emit` computed
`fraction / threshold` → **ZeroDivisionError** — a traceback on every prompt
for that seat, under `UserPromptSubmit` on every session on the box.

WHAT I DID (files: `extensions/agi/hooks/rotation_alert.py`,
`extensions/agi/tests/test_rotation_alert.py`):

1. **RED-FIRST test** `test_e_nonpositive_seat_rotate_at_falls_back_to_ladder`:
   a `config:seats` fixture row with `"rotate_at": 0` (and a positive ladder
   `director_rotate_at: 0.47`) must (i) exit 0, (ii) not crash, (iii) report
   the LADDER as the threshold source. Against the pre-fix bytes it failed with
   the exact `ZeroDivisionError` described. Depth chosen at 0.25 of window so
   it crosses the lowest band (0.40×0.47=0.188) yet stays under the ladder
   line — enough to prove the ladder source won instead of a 0.0 over-line.

2. **Fix in `_seat_line()`**: a non-positive seat `rotate_at` (0 or negative)
   is treated as MISSING — same as a parse failure — and falls through to the
   ladder default. Comment states WHY (the ZeroDivisionError from
   `fraction / threshold` and always-True `over_line`; P6 fail-closed).
   Threshold can never reach the emit path as <= 0.

3. **Fidelity (item 3, kept small)**: `_seat_line` now also matches a cwd
   against a row's OWN `worktree` field (repo-root-relative `.agi/worktrees/...`
   or root-relative), so a seat whose worktree does not follow the `seat-<name>`
   naming convention is still identifiable by path — tightening the claim's
   word "the cwd equals a row's worktree". Empty/missing worktree rows skipped.

## Evidence

RED (pre-fix bytes), the new test failed exactly as the defect predicted:
```
E       ZeroDivisionError: float division by zero
extensions/agi/hooks/rotation_alert.py:407: ...
```

GREEN (fixed bytes), the full test file:
```
$ python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q
tier-gate: phantom running record ... (dead) -- skipped
...............                                                          [100%]
15 passed in 0.26s
```

All 15 tests pass — the 5 prior (a)–(e) rounds, the repair tests, the
SL1.05 fixtures, and my new guard.
<!-- BODY:END -->

## Agent Notes
Built the fail-closed guard: config:seats rotate_at<=0 now falls back to ladder default (was ZeroDivisionError on every prompt), RED-FIRST test_e + tightened cwd-to-worktree seat ID. 15/15 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-12731a28 (SL1.05), continuing kid1.

(1) WHAT THE INSTRUCTION SAID. The kid2 brief said: a config:seats row with rotate_at 0 makes threshold 0.0, over_line always True, and the emit path computes fraction/threshold -> ZeroDivisionError under UserPromptSubmit on every prompt; guard it so a non-positive seat rotate_at is treated as MISSING and falls back to the ladder, with a red-first test. Optional item 3 was tightening seat identification to a row worktree match.

(2) WHAT THE MACHINE ACTUALLY DOES. On the bytes: _seat_line now reads rt = float(row rotate_at) inside a try and only returns it `if rt > 0` (:160-171), with the WHY comment naming the ZeroDivisionError and P6; otherwise it breaks and returns (seat, ladder_default, ladder source). I ran the suite myself: python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q -> 15 passed in 0.23s. test_e at the file bottom (a00-c2afb4e1 hunk lines 105-151) writes a seats fixture with rotate_at 0 and a ladder of 0.47 and asserts exit 0 plus "ladder.director_rotate_at" in the output, i.e. it asserts the guard fired rather than merely that nothing raised. Optional item 3 was also done: the cwd is now matched against a row OWN worktree field, resolving .agi/-prefixed worktrees against root.parent, before falling back to the seat-name convention parse.

(3) THE NEAR MISS. The cheap version of this fix is a try/except around the division in the emit path: it stops the crash while still measuring the seat against 0.0, so over_line stays always True and the alert screams rotation on every prompt. Testing only "does not raise" would pass that version. test_e does not: it asserts the SOURCE LABEL is the ladder, which only holds if the non-positive value was rejected at the source. That is the distinction between silencing the crash and repairing the measurement.

(4) NOTE. The two kids are sequential on the same file, not parallel, per the one-kid-at-a-time rule; kid2 read kid1 result through --prompt-file and built on the staged bytes rather than re-running the round. Accepted.
<!-- THOUGHT:END -->
