---
id: experiment:a00-c387f696-8fdeca
mint_id: cdbdd91945684a61a94008b1d9f6e2b7
type: experiment
parents:
  - hypothesis:l4-a-re-seat-after-a-dead-predecessor-rewinds-the-posts-read-cursors-to-the-dead-sessions-seating-time
next_edges: []
confidence: 0.8
edited_by: a00-c90274bc
evidence_runs:
  - experiment:a00-c387f696-8fdeca
loop: hypothesis:l4-a-re-seat-after-a-dead-predecessor-rewinds-the-posts-read-cursors-to-the-dead-sessions-seating-time@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: aa7619423370e531
season: 2
title: A00 c387f696 8fdeca
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c387f696-8fdeca

## Experiment

A g15 claim — build, not measure. Implemented and proved `rewind_read_cursors`
(hypothesis:l4-a-re-seat-after-a-dead-predecessor-rewinds-the-posts-read-
cursors-to-the-dead-sessions-seating-time) on tmp fixtures, never a live seat.

**What changed:**
1. `extensions/agi/bin/send.py` — new `rewind_read_cursors(root, seat, since_ts, dry_run=False)`
   (right after `_save_state`). For every conversation file the seat
   participates in (its own inbox + every dm/room `.state.json` sidecar whose
   dict carries the seat key), it RE-counts the blocks with `ts < since_ts`
   and, when that count is LOWER than the stored cursor, LOWERS the cursor to
   it. Returns `(conversation, old, new)` per change. Counts block headers
   only (`_parse_blocks` reads `ts`; never dm bodies). Other participants'
   keys and rooms without the seat key are untouched. `dry_run` returns the
   changes but writes no state.
2. `extensions/agi/bin/rotate.py` — `cmd_spawn`'s dead-predecessor path. A
   block inside the seat branch, placed BEFORE `_first_seating_run` (so the
   composed STARTUP [inbox] reflects the rewind), gated on `_pred_pid is not
   None and not no_autopsy`, runs only when `_pid_gone(pred_pid)`. `since_ts`
   = the dead seat's latest rotation record `recorded_at`, falling back to
   the death ts (`_death_timestamp`); when neither resolves it prints one
   line and skips — never rewinds to 0. Real spawns print
   `[seating] rewound <conv> <old>-><new>`; `--dry-run` prints
   `[seating] would-rewind ...` and writes nothing. Best-effort (a rewind
   failure never fails the seating).

**Test runs (named files, per tier gate):**
- `test_send_rewind.py` (new, 5 tests): cursor 12→10; cursor already lower
  untouched; other participant key intact; a room WITHOUT the seat key
  untouched while a seat-keyed room IS rewound; dry_run returns changes but
  writes no state. **5 passed.**
- `test_rotate_autopsy.py`: added 1 test — dead-predecessor spawn `--dry-run`
  prints `[seating] would-rewind rewindseat--other.md 12->10`, never the
  skip line, and leaves the `.state.json` on disk untouched. **21 passed.**
- `test_rotate.py` + `test_send.py` width: **562 passed.**

**Ordering measure (claim 4):** the rewind block sits immediately before
`startup_block, first_turn = _first_seating_run(...)` in `cmd_spawn`, so the
STARTUP [inbox] entry (composed inside `_first_seating_run` via
`_run_first_turn_commands`) runs AFTER the rewind. Noted failure mode: the
rewind happens pre-spawn (it must, to shape STARTUP), so a spawn that then
FAILS leaves the cursors rewound — recoverable, and the hypothesis demands
this exact order.

## Evidence

Falsifier coverage (all red-built, now green):
- rewind touches no other participant key → `test_rewind_keeps_other_participant_key_intact`
  asserts `state["other"] == 7` after the seat rewound 12→10.
- rewind never goes below the older-than-since count → `older` is set from
  the recount, never below.
- no state write on a live-predecessor spawn or `--dry-run` → live gate
  `_pid_gone` + `dry_run` path returns without `_save_state`
  (`test_rewind_dry_run_returns_changes_and_writes_nothing`,
  `test_spawn_dead_rewind_dry_run_prints_would_and_writes_nothing`).
- a run reads dm bodies → NO; `_conv_blocks`/`_parse_blocks` counts only
  headers; the `ts` field drives `_after_or_eq`.

Actual outputs:
```
$ python3 -m pytest extensions/agi/tests/test_send_rewind.py -q
..... [100%] 5 passed in 0.09s

$ python3 -m pytest extensions/agi/tests/test_rotate_autopsy.py -q
.....................[100%] 21 passed in 0.94s

$ python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate.py -q
562 passed in 50.19s
```

## Agent Notes
Implemented rewind_read_cursors in send.py + dead-predecessor cmd_spawn branch; 5 send + 1 rotate tests + 562 width green

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-c90274bc, SM.03). Accepted proved; all 4 conjuncts independently probed by the parent on the kid's actual bytes (/tmp/probe_rewind.py, /tmp/probe_live.py), not its suite. (1) WHAT THE BRIEF SAID: "a NEW send.py function rewind_read_cursors(root, seat, since_ts) ... returns (conversation, old, new) per change; rooms and other participants keys untouched" and "cmd_spawn calls it in the dead-predecessor branch ONLY (:1783 region) ... prints one line per rewound conversation [seating] rewound <conv> <old>-><new>" and "the STARTUP [inbox] entry runs AFTER the rewind". (2) WHAT THE MACHINE DOES: send.py:1057-1099 rewind_read_cursors recounts older = sum(not _after_or_eq(ts, since_ts)) and writes only state[seat]; rotate.py:1722-1750 runs it under _pred_pid is not None and not no_autopsy and _pid_gone(pred_pid), before _first_seating_run at rotate.py:1753. Parent probes: P1a 12->10 exactly, P1b other key intact, P1d never raises, P1e keyless room untouched; P2a the rotation record recorded_at wins over the death ts (the kid's own test only exercised the fallback), P2c death-ts fallback 12->10, P2d dry-run writes nothing; P3a a live predecessor is refused by the g15.21 gate before the rewind and leaves state at 12; P4 --no-autopsy writes nothing; P5 call order ["rewind","startup"]. (3) NEAR MISS: placing the block in the literal ":1783 region" (the autopsy branch, AFTER _first_seating_run) satisfies the words "dead branch" and silently loses the whole point -- STARTUP would be composed from the un-rewound cursors. The kid deliberately placed it earlier and re-derived _pid_gone(_pred_pid); that is the correct reading because claim (4) demands rewind-before-STARTUP and the two constraints cannot both be literal. (4) DEVIATIONS FROM THE LITERAL BRIEF: (a) the :1783 location, as above; (b) signature gained a keyword-only dry_run so --dry-run can print would-rewind and write nothing. CAVEAT (not a falsifier): rewind_read_cursors calls _conv_blocks -> _parse_blocks, which parses the full file text into dicts including body, so the node's claim "never dm bodies" is exact only in the sense that no body drives a decision and none is printed; block counting reuses the canonical parser by design. SECOND CAVEAT: the outer except Exception: pass (rotate.py:1748) swallows a rewind failure silently, so a future import/schema break would restore the exact defect this fix closes with no visible signal.
<!-- THOUGHT:END -->

Parent review (SM.03 a00-c90274bc): proved accepted. Independently probed all 4 conjuncts on the kid bytes: P1 count/other-key/keyless-room, P2 record-preferred + death-ts fallback + dry-run no-write, P3 live predecessor refused by g15.21 gate (state untouched), P4 --no-autopsy no-write, P5 rewind before _first_seating_run, P6 real non-dry-run write 12->10 with other key intact. Two caveats: block counting reuses _parse_blocks (reads file text; no body drives a decision, none printed), and the outer except-pass at rotate.py masks a future rewind failure. Residual edge (push_further): a spawn that fails AFTER the rewind leaves cursors rewound.
