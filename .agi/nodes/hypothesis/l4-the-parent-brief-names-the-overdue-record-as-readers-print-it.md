---
id: hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it
mint_id: d1083305b82243f2a8e0160b00631773
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal
next_edges: []
edited_by: sanctuary-director
scaffold_hash: cc9bacb60b457a6d
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 34 BY NAME (wf_5af338c6-2b0, 12 agents; recorded 11d35c556), ACCEPTED there; minted by sanctuary-director gen XIV 13:0xZ, each finding re-measured on the landed bytes (5068bc2ac + L4.199) before minting. (merge-up 34 residue, L4.185 review) brief.py:1643 tells the parent `A kid whose status reads overdue is STILL WORKING`, but no writer ever sets status=overdue: heal.py:364-376 keeps `status: running` and adds `overdue_since` + `overdue_reason`, and spawn_budget prints `agent=running`. A parent reading its records for the word it was told to expect never finds it. CLAIM: the brief names the shape the record actually has (`status: running` with `overdue_since`/`overdue_reason` set, and the ONE `[agi-nudge] reason=overdue` dm) and what to do (nothing -- the kid is alive; wait, do not cut a replacement); AND `spawn_budget status`/`status --iter` print `agent=running(overdue)` for such a record so the word the brief uses is a word a reader prints. TESTS: test_brief asserts the parent brief contains `overdue_since` and does not contain the phrase `status reads overdue`; test_spawn_budget asserts a running record with `overdue_since` prints `running(overdue)`. FALSIFIER: the brief naming a status value no reader can print. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/brief.py (that paragraph only) + extensions/agi/bin/spawn_budget.py (the status suffix only) + test_brief.py + test_spawn_budget.py. SERIAL on brief.py behind L4.220; SERIAL on spawn_budget.py with l4-a-pid-fd-scan-tolerates-the-process-exiting-mid-read (one round may carry both spawn_budget edits; the brief edit waits for L4.220)."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: the parent brief describes an overdue kid by the fields a reader actually prints (status running + overdue_since), not by a status value nothing emits
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 34 BY NAME (wf_5af338c6-2b0, 12 agents; recorded 11d35c556), ACCEPTED there; minted by sanctuary-director gen XIV 13:0xZ, each finding re-measured on the landed bytes (5068bc2ac + L4.199) before minting. (merge-up 34 residue, L4.185 review) brief.py:1643 tells the parent `A kid whose status reads overdue is STILL WORKING`, but no writer ever sets status=overdue: heal.py:364-376 keeps `status: running` and adds `overdue_since` + `overdue_reason`, and spawn_budget prints `agent=running`. A parent reading its records for the word it was told to expect never finds it. CLAIM: the brief names the shape the record actually has (`status: running` with `overdue_since`/`overdue_reason` set, and the ONE `[agi-nudge] reason=overdue` dm) and what to do (nothing -- the kid is alive; wait, do not cut a replacement); AND `spawn_budget status`/`status --iter` print `agent=running(overdue)` for such a record so the word the brief uses is a word a reader prints. TESTS: test_brief asserts the parent brief contains `overdue_since` and does not contain the phrase `status reads overdue`; test_spawn_budget asserts a running record with `overdue_since` prints `running(overdue)`. FALSIFIER: the brief naming a status value no reader can print. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/brief.py (that paragraph only) + extensions/agi/bin/spawn_budget.py (the status suffix only) + test_brief.py + test_spawn_budget.py. SERIAL on brief.py behind L4.220; SERIAL on spawn_budget.py with l4-a-pid-fd-scan-tolerates-the-process-exiting-mid-read (one round may carry both spawn_budget edits; the brief edit waits for L4.220).
