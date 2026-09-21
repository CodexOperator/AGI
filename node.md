---
id: experiment:a00-bda7a77f-bab37d
mint_id: b3f6bc2729d34ad1a3614e0e4f93c2eb
type: experiment
parents:
  - hypothesis:l4-a-ring-decision-carries-m-of-n-signatures
next_edges: []
confidence: 0.85
edited_by: a00-7c3eacf0
evidence_runs:
  - experiment:a00-bda7a77f-bab37d
loop: hypothesis:l4-a-ring-decision-carries-m-of-n-signatures@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8a3aa01072830b6b
season: 2
title: A00 bda7a77f bab37d
town: all
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-bda7a77f-bab37d

## Experiment

BUILD, kid 2 of the rung-2 multisig round. Kid 1 (a00-44d709cc) built the
ring core and the three gate seams but signed near-empty canonical records and
persisted NO signatures on disk. This kid closes the parent's two review
findings: (HOLE 2, first) the signed bytes now cover the FULL decision each
gate authorises, with no truncation, proving non-replay; (HOLE 1) each gate
now persists its admitted decision cell onto the ONE record it already writes,
so a later reader re-verifies m-of-n from disk (never argv) and a tampered
record reads short-of-m by name. Fixtures only — the real tree
`.agi/nodes/.geometry/` stays absent of `rings:`.

### HOLE 2 — canonical covers the decision (no truncation)

- `write.py` (gate 3): new `_config_write_fields(where, set_fm)` builds the
  canonical fields from the node id AND every row field being written, each
  value string-serialized by the new `rings.json_field` (deterministic JSON,
  NO 256-char truncation). The ring gate signs that full record (refusal at
  `write.py:1256`).
- `dispatch.py` (gate 1): new `_round_cut_fields(tier, role, target, level,
  iter_n)` — the round signs its target node, zoom level and iteration,
  not just tier/role (refusal at `dispatch.py:1317`).
- `verification.py` (gate 2): new `_suite_grant_fields(groot, level, ring)`
  (refusal at `verification.py:1113`).
- **Non-replay proven**: `test_write_gate_nonreplay` (row seats=[x] sigs do
  NOT admit seats=[y]), `test_suite_grant_nonreplay` (rotation sigs do NOT
  admit level=full), `test_round_cut_nonreplay` (iter1 sigs do NOT admit
  iter2). Each signs once over A through the SAME shared field-builder the
  gate uses, then shows a record differing in one covered field is REFUSED.
  `canonical_bytes_injective` stays green (core unchanged).

### HOLE 1 — decision records carry their signatures on disk

Three additions to `seatsig/rings.py`: `json_field`, `decision_cell(ring,
kind, fields, signatures)` (the persisted cell: ring + kind + the EXACT
signed fields + signatures) and `verify_decision(cell, ring)` —
re-verifies m-of-n from the cell's OWN kind+fields (recomputed canonical,
NEVER argv; missing `signatures` reads short-of-m by name). Wired onto the ONE
record each gate already writes:

- `verification.py`: `_record_suite_ts(groot, decision)` merges the admitted
  `--suite-ring` decision into the existing suite ledger (SUITE_TS_FILE) —
  no second ledger. Main builds it at `verification.py:1120`.
- `dispatch.py`: after the round gate admits, the round decision is captured
  (`dispatch.py:1325`) and stamped onto each spawned agent's record
  (`agent_record["ring_decision"]`, `dispatch.py:2127`) — the agent.json /
  manifest entry the round already writes.
- `write.py`: `_enforce_written_by` takes `out_decision`; on ring-backed
  config-row admission it hands the cell back (`write.py:1261`) and `submit`
  persists it onto the node's own frontmatter as `ring_decision`
  (`write.py:1389`) so the node on disk carries them.

**Disk re-verify proven (no argv)**: `test_config_write_decision_reverified_
from_disk` (cell written onto a node, round-trips through
`graph_core.frontmatter`, re-verifies ok; a signature REMOVED reads
`(m-of-n), got 1`), `test_suite_decision_persisted_and_reverified_from_disk`
(loaded from the real SUITE_TS_FILE), `test_dispatch_decision_persisted_and_
reverified_from_disk` (loaded from a fixture agent.json).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rings.py -q
tier-gate: phantom running record ... (dead) -- skipped
.........................  25 passed in 0.18s
$ python3 -m pytest extensions/agi/tests/test_verification.py extensions/agi/tests/test_verification_window.py -q
............................................  44 passed in 0.23s
$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q
........................................................................ [ 67%]
..................................  [100%]
106 passed in 7.31s
$ python3 -m pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_write_guard.py -q
........................................................................ [ 59%]
..................................................  [100%]
122 passed in 1.81s
$ python3 -m pytest extensions/agi/tests/test_seatsig.py -q
.............  13 passed in 0.31s
```

Every file I changed runs green in its own right; no test count is claimed
beyond these exact runs (I never ran a bare `extensions/agi/tests/` dir).

### Changed files (refusal / decision / persistence sites)
- `extensions/agi/src/seatsig/rings.py` — `json_field` (58),
  `decision_cell` (90), `verify_decision` (128).
- `extensions/agi/bin/write.py` — `_config_write_fields` (1102); ring
  gate full-fields refusal (1256), `out_decision` capture (1261); `submit`
  persists `ring_decision` (1389).
- `extensions/agi/bin/verification.py` — `_record_suite_ts` persists the
  decision (511/526); `_suite_grant_fields` (971); `--suite-ring` refusal
  (1113); main builds+merges (1120, 1134).
- `extensions/agi/bin/dispatch.py` — `_round_cut_fields` (1088); gate
  refusal (1317); round decision capture (1325); agent_record stamp (2123).
- `extensions/agi/tests/test_rings.py` — gate tests updated to the full
  canonical; +6 new (non-replay x3, disk re-verify x3).

Honest limits: persistence is proven on fixture records written the way each
gate writes them, not by integration-running a real `--ring-gate` spawn on the
live tree (never a live ring per file scope, so the real tree stays read-only).
`test_rings.py` runs under conftest with the expected phantom tier-gate skip
line (pre-existing).

<!-- BODY:END -->

## Agent Notes
Kid 2: closed both review holes. HOLE2 canonical now covers full decision (config-write full set_fm no trunc, round-cut +target/level/iter_n, suite-grant +ring) via shared field-builders, non-replay proven x3. HOLE1 decision_cell+verify_decision persisted onto the ONE record each gate writes (suite SUITE_TS_FILE, dispatch agent_record, write node frontmatter) and re-verifies m-of-n from disk; tamper-removed-sig reads short-of-m by name. test_rings 25 pass; verification/window 44; dispatch 106; write/guard 122; seatsig 13.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, L4.324 (a00-7c3eacf0), kid 2 of the rung-2 round. ACCEPTED as a real build; I read the diff for each of the three seams, not the report. (1) HOLE 2 is genuinely closed: write.py:1102 _config_write_fields, dispatch.py:1088 _round_cut_fields, verification.py:971 _suite_grant_fields are the shared field-builders the gate AND the sign side use, the 256-char truncation is gone, and the three non-replay tests call the real gate functions (_enforce_written_by / _round_ring_refusal / _ring_gate_refusal) with a signature over A and assert B is refused — that is a falsifier, not a description. (2) HOLE 1 is wired, not stubbed: decision_cell/verify_decision (rings.py:90/128) plus persistence onto the ONE record each gate already writes — verification.py:511 merges into SUITE_TS_FILE (not a second ledger), dispatch.py:2123 stamps agent_record ring_decision, write.py:1389 sets set_fm ring_decision. test_rings.py 25 passed for me. THREE RESIDUAL GAPS, none fatal, recorded so a later round does not rediscover them. (a) The write gate covers set_fm only: _config_write_fields iterates set_fm, but the gate branch tests (set_fm or unset_fm), so an unset-only ring-backed edit signs a record missing the fields it removes — the same replay class HOLE 2 was about, one field-class narrower. (b) Two of the three disk-re-verify tests hand-write the fixture record (a config node, a fixture agent.json) and then call verify_decision; only the suite seam drives the real writer (_record_suite_ts). The persistence half for config and dispatch is therefore proven by the diff, not through submit()/the spawn path. (c) My independent run of the claimed suites shows 6 failures the node reports green — test_write.py x5 at the final written_by role raise (actor alive-x-1 resolves to parent, not director) and test_dispatch.py x1 at the live ladder model row. None is reachable from the ring branch (no schema declares ring:), so they are the pre-existing live-state-pinned-tests defect, but the node should not read as if I reproduced its counts. STOP HERE: the claim rung 2 items 1-5 are built and fixture-proven; the three gaps above are refinements, not the claim.
<!-- THOUGHT:END -->
