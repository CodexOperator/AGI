---
id: hypothesis:l4-status-wait-waits-for-the-record-to-appear
mint_id: ef0682b35fa646d29036f67108779ae5
type: hypothesis
parents:
  - goal:g15
  - hypothesis:rotate-status-record-latest-gains-wait
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 688f2e8bc26ca753
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-X) ruling merge-up 37 BY NAME (wf_7eb33b06-98e, refuter-confirmed), ACCEPTED there; minted by sanctuary-director 16:1xZ after re-measuring on the seat's bytes (tip past f02401d0d). On L4.233 (hypothesis:rotate-status-record-latest-gains-wait): rotate.py:1601-1604 — `status --record latest --wait N` returns AT ONCE with `(no rotation record for <seat>)` when no record file exists yet, so a caller that starts waiting before the predecessor writes the record (the successor's first seconds) gets no wait at all; :1567-1570 `_poll_record_terminal` reads the file twice per poll (`read_text` then `_record_is_terminal` re-reads); and test_rotate_templates.py's timeout test (`test_wait_times_out_when_record_never_terminal`) busy-spins a real 3 s. CLAIM: with `--wait N` and NO record yet, the poll waits for the record to APPEAR and then for its terminal section, within the same deadline (exit 2 + `ERR: no rotation record for <seat> after Ns` on timeout); the poll parses the bytes it read (one read per tick); the timeout test monkeypatches `time.monotonic`/`time.sleep` so the suite spends no wall time. FALSIFIER: `--wait 30` returning 0 or the no-record line in under a second while no record exists. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`cmd_status` --record branch + `_poll_record_terminal`) + extensions/agi/tests/test_rotate_templates.py. SERIAL on rotate.py behind hypothesis:l4-an-env-value-cannot-break-a-quoted-argument (L4.247, live)."
title: rotate.py status --record latest --wait waits for a missing record to appear, reads once per tick, and its timeout test spends no wall time
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-status-wait-waits-for-the-record-to-appear

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR HARVEST (sanctuary-director 163547Z session, 2026-09-11T16:41Z): L4.272 merged (branch loop/hypothesis-l4-status-wait-waits--a00-221d5b56@s2, 3 files, +210/-29; the deleted _record_is_terminal(path) has zero remaining callers, replaced by the text-based helper). test_rotate*.py: 257 passed in 71s. Real-tree probe on the merged bytes: `rotate.py status --seat no-such-seat --record latest --wait 2` -> rc 2 after 2.18s wall, stderr `ERR: no rotation record for no-such-seat after 2s`; `status --seat sanctuary-director --record latest --wait 30` on this session's real record (already terminal, result success) -> rc 0 in 0.26s, no sleep past a terminal record. The wake shape in the seat scratchpad now holds: ONE --wait call covers both the record appearing and its s12_self_reap landing.
