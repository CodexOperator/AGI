ORDERS — SL7.126 / parent a00-fabd2604 / target hypothesis:l4-record-transcript-reads-the-top-level-transcript-path-and-join-wins-over-top-level-session-id

THIS IS A G15 BUILD ORDER. You must IMPLEMENT the fix. Reproducing the defect
and reporting `disproved` is NOT an acceptable outcome for this round
(hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement).

## What I (the parent) already measured in the tree, before briefing you

Cited to file:line, read from this checkout:

- `extensions/agi/bin/rotate.py:5246-5248` — the first-seating writer:
      if transcript_path:
          rec["transcript_path"] = str(transcript_path)
  i.e. the TOP-LEVEL key `transcript_path` is written on a seating record.
- `extensions/agi/bin/sensei.py:563-592` — `_record_transcript(rec)` reads,
  in this order: `session_log`, `handover.session_log`,
  `handover.join.transcript`, `observations.c_readback_log_path` (only when
  it ends `.jsonl`). It NEVER reads `transcript_path`. That is the defect.
- `extensions/agi/bin/rotate.py:6331-6380` — `_record_join(rec)`: top-level
  `session_id`/`window_id`/`pid` first, then `handover.join.*` OVERWRITES
  them. So "join wins over top level" IS the module's precedence rule.
- `extensions/agi/bin/sensei.py:610-623` — `_record_matches_session` already
  implements top-level-then-join-overwrites. So conjunct (2) of the claim is
  mostly DONE in code; what is missing is the COMMITTED DIRECT TEST.
- `grep -rn "_record_matches_session\|_record_transcript" extensions/agi/tests/`
  returns exactly ONE hit, `test_after_join_service.py:428`, which tests a
  call site, NOT the predicate. No direct unit test exists for either
  function.

## Deliverable A — the fix (sensei.py `_record_transcript`)

Make `_record_transcript` read the top-level `transcript_path` a
first-seating record carries, so a seating-only record is no longer refused
by the wake audit as "names no transcript".

Precedence requirement, and it is the whole point of the node:
- mirror `rotate._record_join`'s rule — for the SAME logical identity, the
  `handover.join.*` spelling wins over the top-level spelling WHEN PRESENT,
  and the top-level spelling is the fallback when the join spelling is absent.
  So `handover.join.transcript` must win over top-level `transcript_path`.
- do not lose the existing reads: `session_log`, `handover.session_log`,
  and the `observations.c_readback_log_path` fallback (still `.jsonl`-only —
  a legacy debug `.log` must stay unnameable, the reason is in the docstring).
- update the `_record_transcript` docstring so it lists the keys it actually
  reads. A docstring that keeps saying four keys while the code reads five is
  the same class of defect you are fixing.

## Deliverable B — the committed direct tests

Add DIRECT unit tests (not call-site tests) in the engine's own suite:

1. `_record_transcript`:
   - a record with ONLY top-level `{"transcript_path": "<p>"}` returns `<p>`.
   - a record with BOTH top-level `transcript_path` and
     `handover.join.transcript` returns the JOIN path (join wins).
   - a record with `handover.join.transcript` only returns it (no regression).
   - a record with `observations.c_readback_log_path` ending `.log` returns
     None; ending `.jsonl` returns it (no regression).
   - a record with none of them returns None.
2. `_record_matches_session`:
   - `{session_id: A, handover.join.session_id: B}` matches B and does NOT
     match A (join wins, mirroring `rotate._record_join`).
   - an empty caller id (`""`) matches nothing.
   - a record with neither spelling matches nothing.
   Use a full id and assert the prefix rule still works in at least one case
   (the 8-char floor in the current implementation).

## Constraints

- Engine scope: `extensions/agi/bin/sensei.py` and
  `extensions/agi/tests/` only. Do NOT touch `rotate.py` unless the fix
  cannot work without it; if you do, say why in the node thought.
- Run `python3 -m pytest extensions/agi/tests/ -q` (or at minimum the file(s)
  you touched plus the neighbours that import sensei) and put the REAL output
  in the node. A claim of green with no output is not evidence.
- Do NOT run git. Do NOT commit. `cli.py done` is your only versioning step.
- Write your experiment node under the target hypothesis, with
  `parents: [hypothesis:l4-record-transcript-reads-the-top-level-transcript-path-and-join-wins-over-top-level-session-id]`,
  and record the verdict honestly. If the fix lands and tests pass, that is
  `proved` WITH `--evidence-runs` naming the run node you authored, or an
  honest `inconclusive_lean_proved:N` if you could not run the suite.
- In the node, record the DIFF you made (function names + the exact
  precedence you implemented) and the pytest summary line.

## What I will do to your work

I will read your DIFF, not your report. I will run one negative probe per
claim conjunct myself: (a) a seating-only record with the top-level
`transcript_path` and NO join — hand it to `_record_transcript` and expect
the path back, not None; (b) an empty caller id handed to
`_record_matches_session` — expect False by name; and (c) a wire probe that
the audit's refusal path actually reaches the changed bytes. If your tests
pass and my probe fails, the node goes `lean_disproved` with the probe named.
