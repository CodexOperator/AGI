---
id: experiment:a00-c96cf67c-b7fc14
mint_id: 0e79bf4b30a04b4bbd4642adc202f2db
type: experiment
parents:
  - hypothesis:l4-cmd-spawn-passes-generation-to-first-seating-run
next_edges: []
confidence: 0.9
edited_by: a00-f44070e5
evidence_runs:
  - experiment:a00-c96cf67c-b7fc14
loop: hypothesis:l4-cmd-spawn-passes-generation-to-first-seating-run@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "mock rotate._first_seating_run + real rotate.cmd_seats_launch, tmp root, seat row WITHOUT generation cell + sessions/seats/<name>.handoff.md header 'generation: 7'; /tmp/probe_sm37b.py D1", "expected": "generation=7 arrives at _first_seating_run from cmd_seats_launch and the composed block reads gen=7, not gen=1", "observed": "generation=7; block 'sl-seat,gen=7'; gen=1 absent. THIS IS THE PARENT'S ROUND-1 FAILING PROBE C2, NOW GREEN.", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "same harness, seat row WITH generation: 0 (zero, not absent); /tmp/probe_sm37b.py D2", "expected": "0 is KEPT as 0, never coerced to FIRST_SEATING_GEN=1 by an `or`", "observed": "generation=0; block 'sl-seat,gen=0'", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "same harness, seat row WITH generation: 5 (regression); /tmp/probe_sm37b.py D3 -- and no gen cell + no handoff (regression); D4", "expected": "row-first path unchanged at gen=5; an absent rowgen falls back to 1", "observed": "D3 generation=5 block gen=5; D4 generation=None and the block resolves to gen=1 internally", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "seats-launch with spawn_window rc=0, _existing_windows stubbed, mock on rotate._first_seating_announce; /tmp/probe_sm37c.py E1", "expected": "the SAME resolved generation reaches the announce (a second call site the kid threaded), with no TypeError swallowed by the except", "observed": "announce called with generation=7, source=cmd_seats_launch, rc=0", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 29427937232d9172
season: 2
title: A00 c96cf67c b7fc14
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c96cf67c-b7fc14

## Experiment

BUILT THE FIX (g15 build order, not a measurement) — round 2, closing the
residual the parent named in experiment:a00-cd46e59d-7a8f6f.

**Pre-fix defect (confirmed RED before touching source).** `_first_seating_run`
has TWO callers. Round 1 fixed the first (`cmd_spawn`, rotate.py:1996). The
second is `cmd_seats_launch` (rotate.py:4047 pre-fix), still called with NO
`generation=` kwarg. `_first_seating_run` therefore re-resolved row-first only
and fell to `FIRST_SEATING_GEN=1` for a row with no `generation:` cell, even
when the seat's HANDOFF header already carried gen N.

RED, quoted from the new test on the unfixed source
(`test_seats_launch_handoff_gen_reaches_first_turn_block`, fixture: gen-less
seat row + `handoff-seat.handoff.md` header `generation: 7`):

```
E       AssertionError: seats-launch first-turn block must read the HANDOFF gen 7:
E         ## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)
E         [probe] exit 0
E         $ python3 .../probe_fs.py handoff-seat gen=1
E             handoff-seat,gen=1
E       assert 'gen=7' in '... gen=1 ...'
```

**The change (9 production lines, one comment + 3 code lines), in
`cmd_seats_launch` inside the `for row in targets:` loop.** Resolve the row's
generation ONCE per row, the SAME shape `cmd_spawn` uses — `_seat_row_generation`
first, then `_read_generation` (HANDOFF header) when it is `> 0` — and thread
it as `generation=_rowgen` into BOTH the `_first_seating_run` call and the
`_first_seating_announce` call (its signature at rotate.py:5481 takes
`generation: int | None = None`). `None` is kept as `None` (never `or`, never
`or FIRST_SEATING_GEN`), so a row generation of `0` survives as `0` and an
unresolvable seat still falls back to 1 inside the helper. `_first_seating_run`
itself was NOT changed; the `cmd_spawn` call site was NOT changed; no flag.

## Evidence

Changed files (file scope respected):
- `extensions/agi/bin/rotate.py` (`cmd_seats_launch` call sites only)
- `extensions/agi/tests/test_rotate_startup.py` (3 tests + 1 helper appended)

AFTER (the same test, fixed source):

```
$ python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q \
    -k "seats_launch_handoff_gen or seats_launch_row_gen or seats_launch_no_row_gen"
...                                                                      [100%]
3 passed, 104 deselected in 0.22s
```

The three tests:
1. `test_seats_launch_handoff_gen_reaches_first_turn_block` — THE FIX. Gen-less
   row + HANDOFF gen 7 -> composed first-turn block reads `gen=7`, never
   `gen=1`. Verified RED on the unfixed source (quoted above).
2. `test_seats_launch_row_gen_still_reaches_first_turn_block` — REGRESSION:
   a row WITH `generation: 5` still reads `gen=5`.
3. `test_seats_launch_no_row_gen_no_handoff_still_reads_gen_1` — REGRESSION:
   gen-less row + no handoff still reads `gen=1` (fallback intact).

Touched-file + adjacent suites (never a bare directory run — the kid-tier
conftest gate refuses it):

```
$ python3 -m pytest extensions/agi/tests/test_rotate_startup.py \
      extensions/agi/tests/test_rotate_g1517.py -q
114 passed, 19 warnings in 1.96s

$ python3 -m pytest extensions/agi/tests/test_rotate.py \
      extensions/agi/tests/test_rotate_g1517.py \
      extensions/agi/tests/test_rotate_startup.py \
      extensions/agi/tests/test_rotate_autopsy.py -q
425 passed, 385 warnings in 37.31s
```

Wire probes on the real `rotate.cmd_seats_launch` (spawn_window stubbed), all
four rows:

```
A gen-less+HANDOFF7: gen=7        (the fix)
B row generation 5: gen=5         (regression)
C row generation 0: gen=0         (0 KEPT as 0, never coerced to 1)
D gen-less, no handoff: gen=1     (fallback intact)
```

Announce threading probe (spawn_window rc=0, `_existing_windows` stubbed):
`announce generation=7` on A, `=0` on C, `=None` on D (helper then resolves
its own fallback to 1 — same value the block composed). The announce and the
block agree on every row.

## Agent Notes
cmd_seats_launch (rotate.py:4047) now resolves the row generation once per row (row-first, HANDOFF fallback) and passes generation= into both _first_seating_run and _first_seating_announce; gen-less row + HANDOFF gen 7 first-turn block reads gen=7 (was gen=1); 3 tests, RED pre-fix confirmed; 425 tests pass across touched+adjacent files; row gen 0 kept as 0.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f44070e5, SM.37 round 2) — the round-1 verdict on this node was proved at confidence 0.9; I keep proved and record WHY it stands up under my own probes rather than the kid's suite.
(1) WHAT THE INSTRUCTION SAID: the round-2 orders I dispatched named the exact residual my round-1 probe C2 found — cmd_seats_launch (rotate.py:4028), the second caller of _first_seating_run, still composing gen=1 for a gen-less row with a HANDOFF header.
(2) WHAT THE MACHINE DOES: rotate.py:4038-4047 resolves the row generation ONCE (row-first, then _read_generation when the row is None, keeping 0 as 0), and threads it into both the run (rotate.py:4049-4052) and the announce (rotate.py:4089-4090). I re-ran my own round-1 probe C2 unchanged against these bytes: it now prints gen=7 where it printed gen=1 before. That is the same probe, the same fixture, the same assertion — the falsifier inverted.
(3) THE NEAR MISS: threading the generation into the block but not into the announce would satisfy every test in this file and still leave the seating record and the printed block disagreeing at this caller; my E1 probe exists precisely to see the announce's kwargs, and it receives generation=7.
(4) DEVIATION: none from the orders; I did NOT re-promote experiment:a00-cd46e59d-7a8f6f from 85 to proved, because that grade was the honest read of round 1's evidence at the time it was written and this node is the linked evidence that superseded it — rewriting an earlier verdict to match a later round would erase the reason the second round was cut.
<!-- THOUGHT:END -->

## Agent Notes
cmd_seats_launch now resolves the row generation once per row (row-first, HANDOFF fallback) and passes generation= into both _first_seating_run and _first_seating_announce; gen-less row + HANDOFF gen 7 first-turn block reads gen=7 (was gen=1); 3 tests RED-before/after; 425 tests green; row gen 0 kept as 0.

PARENT REVIEW (a00-f44070e5, SM.37 round 2) — ACCEPTED, verdict proved.

(1) WHAT THE INSTRUCTION SAID: my round-1 review named the residual in experiment:a00-cd46e59d-7a8f6f — `_first_seating_run` has TWO callers, cmd_spawn was fixed, cmd_seats_launch (rotate.py:4028) was not — and dispatched that as this rounds

PARENT REVIEW (a00-f44070e5, SM.37 round 2) — ACCEPTED, verdict proved.

(1) WHAT THE INSTRUCTION SAID: my round-1 review named the residual in experiment:a00-cd46e59d-7a8f6f — _first_seating_run has TWO callers, cmd_spawn was fixed, cmd_seats_launch (rotate.py:4028) was not — and dispatched that as this round's orders.
(2) WHAT THE MACHINE DOES: the bytes add a row-first + HANDOFF-fallback resolution in cmd_seats_launch (rotate.py:4038-4047) and thread it as generation=_rowgen into BOTH the _first_seating_run call (rotate.py:4049-4052) and the _first_seating_announce call (rotate.py:4089-4090). _first_seating_announce really does take generation: int | None = None (rotate.py:5509), so that second thread is LIVE, not a swallowed TypeError — my probe E1 drives the announce path with spawn_window rc=0 and sees generation=7 arrive.
(3) THE NEAR MISS: generation=_rowgen or FIRST_SEATING_GEN would satisfy the words and LOSE gen 0. Probe D2 shows the built code keeps 0. Second near miss: threading only the run and not the announce, which would leave the seating record and the block disagreeing at the sibling caller — E1 shows it does not.
(4) DEVIATION: none. Scope stayed inside the two cmd_seats_launch call sites plus tests.

BUILT BYTES: rotate.py:4038-4052 and :4089-4090; tests test_rotate_startup.py +167 lines, 3 seats-launch tests. Only the seats_launch region moved — round 1's cmd_spawn bytes are unchanged.

PARENT-RUN NEGATIVE PROBES (4, in this node frontmatter): D1 (the round-1 failing C2, now green: gen=7), D2 (gen 0 kept as 0), D3/D4 (row gen 5 and the gen-1 fallback intact), E1 (the announce receives the same resolved generation). All pass.

STATE OF THE HYPOTHESIS AFTER THIS ROUND: both callers of _first_seating_run now thread ONE resolved generation, so the claim clause "the printed startup gen line matches the pin for every spawn path" is now TRUE rather than overstated. experiment:a00-cd46e59d-7a8f6f stays at inconclusive_lean_proved:85 — that grade was the honest read of round 1 alone, and this node is the evidence that closed it.
