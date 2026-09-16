---
id: hypothesis:l4-the-sensei-audit-verbs-write-their-result-into-the-rotation-record-and-name-a-finding-only-over-the-floor
mint_id: 410761f28bdf4e1c9f91043204d016c6
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 4b946183cccdeebd
season: 2
testable_claim: "OWNER 13:5xZ via belam XXIII (doc:l4-owner-decisions, 4db48fbbe): rotation announces to the Sensei only; the Sensei dms the Prime ONLY on a finding (a floor breach with a structural cause, or a failed key verification); a GREEN audit stays in the rotation record. MEASURED 2026-09-16 14:0xZ: no rotation record carries an audit key (belam.20260916T114647Z.json and every other); sensei.py writes only draft files (:1993); every audit result today lived in drafts + dms. CLAIM, one kid, sensei.py + its tests only, rotate.py untouched: (1) rotate-out-audit and wake-audit, after resolving their window, write their result INTO the audited rotation record under one top-level key `audit` = {out|wake: {calls, a, b, c, d, floor, excess, transcript, window_start, window_end, audited_at, audited_by}} - read-modify-write of that key only, every other key byte-identical (a test diffs the record before/after with the key removed), idempotent (a re-run replaces its own side), `--no-record` opts out (dry read); (2) the verb prints the one line the owner wants: `green <post> <side> --record <stamp> <calls> (floor N)` when excess is 0, else `FINDING <post> <side> --record <stamp> excess <n> over floor <N>` on stdout and exit 0 either way - the dm to the Prime stays a Sensei act, never sent by the verb; floors from the ladder (wake 0, out 1); (3) `rotate.py status --post S --record latest` shows the audit key as part of the record it prints. Falsifier: a record byte differs outside the audit key after a run; a re-run grows the record; a wake with excess 0 prints anything but green. Every printed line names the record stamp, never a generation."
title: L4 the sensei audit verbs write their result into the rotation record and name a finding only over the floor
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-sensei-audit-verbs-write-their-result-into-the-rotation-record-and-name-a-finding-only-over-the-floor

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by master-sensei gen 8 at 14:0xZ on the owner rotation-pings order relayed 13:59Z. (1) INSTRUCTION: "a green audit stays in the rotation record; audit dms to the Prime ONLY on a finding". (2) MECHANISM: today the verbs (SL7.130/131) resolve and classify but write nothing back - the record is where the owner wants the green result, and it has no audit key; the record writer is a JSON file under .agi/sessions/rotations/, committed by the rotate wrapper, so an audit write lands in the next grid/branch push like any record field. (3) NEAR MISS: the verb sending the Prime dm itself - satisfies "only on a finding" and loses the Sensei judgement of structural cause; ruled out: the verb names the finding, the Sensei decides the dm. (4) No deviation; the floors are the ladder numbers.
<!-- THOUGHT:END -->
