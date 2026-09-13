---
id: hypothesis:l4-the-after-join-dm-is-one-line-per-entry-detail-only-on-refusal-or-nonzero-record-named-by-graph-address
mint_id: 4514cf88d9e2441b8e8df78ce7deae72
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 4033b459d6ab2935
season: 2
testable_claim: "goal:g15.25 SM.01 (intake: master-sensei 22:4xZ; owner 22:3xZ verbatim in doc:l4-owner-decisions: wordy/redundant input text is a cut). The SHAPE is already DECLARED — config:rotations director template `delivery` (rotations.md:69, landed 47b8af755): one line per entry, label + exit; detail only on REFUSED or non-zero; the record named as the graph address (`rotate.py status --record latest`), never a filesystem path — and the CODE does not do it. MEASURED on season2/main @9f7715132: `_compose_after_join_dm` rotate.py:11293-11384 emits for EVERY entry `[label] status` + `$ cmd` + every output line (per-command byte_cap) regardless of rc; the over-budget branch (dm_byte_cap, DEFAULT_AFTER_JOIN_DM_BYTE_CAP=4000 :9487) already keeps label+status per entry but closes with `full output: {record_path}` — a filesystem path; one call site :11781 passes record_path. CLAIM — rewrite the composer so that: (1) an entry with rc==0, not refused, not timed out = EXACTLY one line `[label] exit 0` — no `$ cmd`, no output; (2) REFUSED = one line `[label] REFUSED — <reason>`; (3) non-zero or TIMEOUT = `[label] exit N|TIMEOUT (>Ns)` + `$ cmd` + the output (per-command cap, as today) — detail stays where it is needed; (4) the tail names the record as its graph address `python3 extensions/agi/bin/rotate.py status --post <seat> --record latest` — never record_path (param stays accepted for the call site, never printed); (5) the captive `ack … diff` line + its gen rule (SL7.74) UNCHANGED; (6) the over-budget branch keeps rule 1-4 and the `… [trimmed N bytes] …` marker, its `full output:` line becomes the same graph address. FALSIFIERS: a zero-exit entry that still prints `$ cmd` or output; a refusal whose reason is dropped; any absolute or relative filesystem path in the composed dm; a non-zero entry whose output is dropped; the captive line altered; a change outside the composer. TESTS (test_after_join_service.py: update the two composer tests :2390 :2409, add <= 4): rc0 -> one line, no `$`; rc1 -> cmd + output present; refused -> one line carrying the reason; record_path given -> its string ABSENT, graph address PRESENT; over-budget -> label lines + graph address, no path. FILE SCOPE: rotate.py `_compose_after_join_dm` only (+ its docstring), test_after_join_service.py. CEILING: <= 40 lines net in rotate.py, <= 6 tests; after_join nbhd green. TEMPLATE-FIRST note for master-sensei (not this round): the prime template `delivery` (rotations.md:113) lacks the SHAPE sentence the director line carries — one template edit, after this lands the code reads the same for both."
title: "the after_join dm is one line per entry (label + exit), detail only on REFUSED / non-zero, the record named by its graph address never a path — the code half of the shape the director template declared 22:3xZ (owner: wordy outputs are a cost)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-after-join-dm-is-one-line-per-entry-detail-only-on-refusal-or-nonzero-record-named-by-graph-address

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM review by name (SL2#28 @d22584a70): ACCEPT. In-process probe of _compose_after_join_dm with rc0/rc2/REFUSED/TIMEOUT entries + record_path=/home/ubuntu/x.json: rc0 = one line, no $ cmd; rc2 keeps cmd+output; REFUSED one line with reason; no filesystem path in either the normal or the over-budget (cap 1500, 20 entries) body; record named by rotate.py status --post <seat> --record latest; captive ack line intact. 134 tests green across the #28 files.
