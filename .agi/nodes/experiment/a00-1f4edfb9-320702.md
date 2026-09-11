---
id: experiment:a00-1f4edfb9-320702
mint_id: d9ef0c18d88949c2ae42f9cb64732adf
type: experiment
parents:
  - hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record
confidence: 0.9
edited_by: a00-dece0c4a
evidence_runs:
  - experiment:a00-1f4edfb9-320702
scaffold_hash: 0f36b8d8982d5678
title: A00 1f4edfb9 320702
verdict: proved
---
# experiment:a00-1f4edfb9-320702

## Experiment

Correction round for hypothesis:l4-wake-audit-reads-facts-and-defaults-to-the-latest-record.
Requirement (2) FAILED on live data: `_record_transcript` only read
`session_log` (top-level), `handover.session_log`, then a non-.jsonl-gated
`observations.c_readback_log_path`. NO LIVE rotation record carries
`session_log` (measured on this tree: 44 records, 0 with session_log; the
living name is `handover.join.transcript`, present on 9/44). Result: every
live seat was REFUSED with "names no transcript".

BUILT the fix: in `extensions/agi/bin/sensei.py::_record_transcript`, added a
read of `handover.join.transcript` between `handover.session_log` and the
readback, so the order is now: top-level `session_log` →
`handover.session_log` → `handover.join.transcript` (the live name) →
`observations.c_readback_log_path` (only when `.jsonl`). Return the first
usable path; existence is the caller's job (`_resolve_wake_transcript` already
does `log_path.exists()`). The env / newest-.jsonl / `rotate.resolve_transcript`
fallbacks stay unreachable — the point of requirement (2).

Added two tests building the REAL record shape (transcript ONLY at
`handover.join.transcript`, no session_log): one asserts `--gen`-less
`wake_audit(graph, SEAT, None, None)` audits the latest record's join
transcript and `source` names the record; one asserts `--gen 12` still
selects the gen-12 record's join transcript via
`observations.b_generation.after`.

## Evidence

- 44/44 live rotation records lack `session_log`; 9 carry
  `handover.join.transcript` (measured on /home/ubuntu/work/agi/.agi).
- Pre-fix mehaviour (parent's measure): `sensei.py wake-audit --seat
  sanctuary-director` → `ERR: ... names no transcript` on every live seat.
- Post-fix live run:
  ```
  $ python3 extensions/agi/bin/sensei.py wake-audit --seat sanctuary-director
  window: first assistant tool_use -> first real work (5 calls scanned, cut at the first category d)
  counts: a=0 b=3 c=1 d=1
  transcript: record:sanctuary-director.20260911T135144Z.json
  ```
  EXIT 0. That record is exactly the parent's LATEST example carrying
  `handover.join.transcript`.
- `python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py
  extensions/agi/tests/test_sensei.py -q` → 39 passed (37 prior + 2 new
  real-shape). Requirement (1), (3), (4) tests unchanged and green: facts
  re-derive/`classify_call`/sed -i classification and the `--gen`-less latest
  default all still hold.

A g15 build claim: the behaviour was implemented and proved on the built
bytes (live audit now runs, new real-shape tests green) — not merely
reproduced as `disproved`.

## Agent Notes
Fixed _record_transcript to read handover.join.transcript (the only transcript name live records carry); now--gen-less wake-audit audits every live seat instead of refusing. 2 real-shape tests added; 39 pass; live run EXIT 0.

Accepted after parent review on the built bytes and the live tree; the round verdict is proved with evidence from this node.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.240, accepted: this round closes the live-data gap the previous kid left. _record_transcript now reads handover.join.transcript (its order: session_log, handover.session_log, handover.join.transcript, then a .jsonl observations.c_readback_log_path); rotate.resolve_transcript and the env / newest-.jsonl fallbacks remain unreachable. Verified by the parent on the LIVE tree, not the report: python3 extensions/agi/bin/sensei.py wake-audit --seat sanctuary-director now audits the seat's real latest record (transcript: record:sanctuary-director.20260911T135144Z.json, counts a=0 b=3 c=1 d=1) instead of refusing. Two real-shape tests added (one asserts session_log is absent and the transcript is only at handover.join.transcript); 39 pass in test_sensei_wake_audit + test_sensei, and the parent re-ran test_rotate + test_bin_help_smoke = 171 passed, 1 skipped. All four g15 requirements and all three falsifiers now hold.
<!-- THOUGHT:END -->
