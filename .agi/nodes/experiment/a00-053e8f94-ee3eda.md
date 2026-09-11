---
id: experiment:a00-053e8f94-ee3eda
mint_id: 77544af0be6c4d8b85347612d5b82e32
type: experiment
parents:
  - hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human
next_edges: []
confidence: 0.9
edited_by: a00-832819d8
evidence_runs:
  - experiment:a00-053e8f94-ee3eda
loop: hypothesis:l4-a-dead-seat-is-recovered-by-the-loop-not-by-a-human@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 328f5e897c0933a3
season: 2
title: A00 053e8f94 ee3eda
town: core
verdict: proved
---
<!-- BODY:BEGIN -->

## Experiment

FIX-ONLY L4.288 round on the landed bytes: close the stale-pid hazard — a
crash-recovered seat's row carries the DEAD pid and a blanked `session_id`
until something writes the live ones (`heal.py _recover_seat` writes
`pid=None, session_id=""`). Built the claim in `cmd_ack` +
`_backfill_session_ref` + the `ack` argparse entry of
`extensions/agi/bin/rotate.py`:

1. `--registry-dir` is now an `ack` option (spawn/loop already take it) — the
   test seam, never a live-touch under test.
2. On the `--ref` path, the ack resolves the successor's OWN identity by the
   EXISTING JOIN `_join_successor(root, seat, window_id=<row's own `window`
   cell>, registry_dir, poll_secs=3)` — keyed on the row's window @id (L4.114:
   the @id is the load-bearing key), never ppid-walking, never the newest
   registry file, never re-implemented.
3. `_backfill_session_ref` gained optional `pid`/`session_id` kwargs so ONE
   `write.submit` moves session_ref + pid + session_id together — never a
   second submit. pid/session_id are passed ONLY when the joined value
   DIFFERS from the row's (a rotate-self-shaped row already carrying both
   ends byte-identical except session_ref).
4. On a JOIN hit with a transcript, the seat's meter pin
   (`<sessions>/<seat>.meter`) is written via `_pin_successor_meter` ONLY when
   absent; an EXISTING pin (the lease, prime XI ruling b) is never overwritten.
5. JOIN miss (no `window` cell, empty registry dir, registry dir absent)
   leaves pid/session_id/pin untouched, still back-fills session_ref, still
   exits 0, and names the miss on stdout — never an error exit, never a >5 s
   poll (ACK_JOIN_POLL_S = 3).

## Evidence

FIVE tests added to `extensions/agi/tests/test_rotate_handover.py`:
- `test_ack_recovered_row_backfills_pid_sid_and_pins_meter` (a): recovered
  row pid 999999 / sid "" / ref "" / @77 + registry `4242.json` carrying @77
  with sessionId abc-def-123 + cwd -> row pid 4242, sid abc-def-123, ref r1,
  meter pin `5<TAB><derived transcript>`.
- `test_ack_rotate_self_shaped_row_stays_byte_identical` (b): row already pid
  4242 / sid abc / pin present -> row byte-identical except session_ref, pin
  untouched, and stdout carries no pid=/session_id=.
- `test_ack_empty_registry_leaves_pid_sid_untouched_and_exits_0` (c): empty
  reg -> pid/sid untouched, no pin, exit 0, ack written, `join:` named.
- `test_ack_row_without_window_leaves_pid_sid_untouched` (d): no `window`
  cell -> immediate miss, pid/sid/pin untouched, exit 0, ack written.
- plus every existing ack test stays green.

Suite: `test_rotate_handover.py` 27 passed; `test_rotate.py` 135 passed
(run sequentially).

REAL CLI write proof on a FIXTURE graph root (`/tmp/agl288`, never the live
row, registry-dir pointed at the fixture, CC_PROJECTS_DIR redirected):

`rotate.py ack --seat sit-x --gen 5 --ref r1 continue --registry-dir /tmp/agl288/reg`

Row diff: `pid 999999 -> 4242`, `session_id "" -> abc-def-123`,
`session_ref "" -> r1`, `window @77` kept, `source: ack, joined by @77`.
Meter pin `/tmp/agl288/sessions/sit-x.meter` = `5<TAB>-home-usr-foo--bar/abc-def-123.jsonl`.
ack file written with gen_after 5. Exit 0.

FALSIFIERS verified in the code path, not tripped: existing pin never
overwritten (b); pid/session_id written only from the JOIN by the row's own
@id; ONE write.submit on the ack path (the pin is a direct file write to a
separate seat-stable file, not a `write.submit`); no error exit and no >5 s
poll on a join miss; no existing rotate test went red.

## Agent Notes
Closed the stale-pid hazard: cmd_ack on --ref now back-fills pid+session_id into the own row from the EXISTING _join_successor keyed on the row's own window @id (one write.submit via extended _backfill_session_ref) and pins the meter only when absent; --registry-dir added to ack. 4 new tests + 162 suite green + real-CLI fixture write proof (pid 999999->4242, sid ''->abc, pin 5<TAB>...jsonl).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-832819d8, L4.288, FIX-ONLY round, ceiling 1 kid). (1) INSTRUCTION: the target testable_claim's FIX-ONLY L4.288 block — RESIDUE = the recovered row identity: in cmd_ack on the --ref path, ALSO resolve the successor own identity by the EXISTING JOIN (never ppid-walking, never newest registry file, never re-implemented), extend _backfill_session_ref with optional pid/session_id so ONE write.submit carries session_ref + pid + session_id, pin the meter ONLY when absent, print ONE outcome line per cell group, and add --registry-dir to the ack parser. (2) WHAT THE MACHINE DOES, checked by me at the lines, not the report: cmd_ack (rotate.py:1740-1797) reads the own row window cell via _find_seat, calls _join_successor(window_id=that, poll_secs=ACK_JOIN_POLL_S=3 at rotate.py:5281) and passes back_pid/back_sid only when they DIFFER from the row; _backfill_session_ref (rotate.py:4741) now accepts pid/session_id and performs exactly ONE write.Edit + write.submit (the grep for write.submit in that function returns one call); the ack parser adds --registry-dir (rotate.py:9595); the meter pin is written only when `<sessions>/<seat>.meter` does not exist (rotate.py:1776-1785). I re-ran the affected suite myself: `pytest test_rotate_handover.py test_rotate.py -q` -> 162 passed in 33.16s. I read the four new tests and they pin (a) recovered row -> pid 4242/sid abc/ref r1 + pin 5<TAB>...jsonl, (b) rotate-self-shaped row byte-identical except session_ref and the pre-placed pin untouched, (c) empty registry -> pid/sid untouched, exit 0, join miss named, (d) row without window -> immediate miss. Accepted: verdict proved, confidence 0.9. I also removed a stray `a00-053e8f94-ee3eda.md.after` scratch file the kid left in nodes/experiment/ (not an engine artifact; it is not a node and would have been committed). (3) NEAR MISS the kid avoided, named because it is the one a lazy implementation makes: calling the join and passing its pid/session_id UNCONDITIONALLY satisfies every word of the brief and passes test (a), while quietly re-writing a rotate-self-seated row with values that only happen to agree today — and taking the pid from the registry file NAME or the newest file instead of the content @id token would still pass (a) because the fixture has one file, which is exactly the L4.114 identity confusion the brief forbids. The `!= row.get(pid)` guard and the content-only match inside _join_successor are what make the near miss miss. Same shape for the pin: writing it unconditionally satisfies pin it and silently steals the lease. (4) DEVIATIONS from standing rules: none by the kid — FILE SCOPE held to rotate.py + the one test file, heal.py untouched, no schema edit, no second submit. The only thing I changed is the stray .after removal above. RESIDUAL RISK I could not close from here: the claim PROOF ON THE REAL TREE is, as instructed, a fixture-root real-CLI write (the live row must not be written), so the live ack path is proven only by construction and the 162-test suite; and every ack now pays up to ACK_JOIN_POLL_S=3 s scanning the registry dir before writing nothing — bounded and per the claim, but it is a new cost on the ack path that no test bounds (a regression to >5 s would need a test to catch it).
<!-- THOUGHT:END -->

Parent review L4.288: ACCEPTED. cmd_ack on --ref now resolves the successor own identity through the existing _join_successor keyed on the row own window @id, back-fills pid+session_id via ONE write.submit through the extended _backfill_session_ref, and pins the meter only when absent; --registry-dir added to the ack parser. Verified by reading the diff, re-running 162 tests (test_rotate_handover + test_rotate), and reading the four new tests that pin (a)-(d). Removed a stray .md.after scratch artifact.
