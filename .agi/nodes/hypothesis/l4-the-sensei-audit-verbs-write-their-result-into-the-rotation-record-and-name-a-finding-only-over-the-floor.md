---
id: hypothesis:l4-the-sensei-audit-verbs-write-their-result-into-the-rotation-record-and-name-a-finding-only-over-the-floor
mint_id: 410761f28bdf4e1c9f91043204d016c6
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 4b946183cccdeebd
season: 2
testable_claim: "OWNER 13:5xZ via belam XXIII (doc:l4-owner-decisions, 4db48fbbe): rotation announces to the Sensei only; the Sensei dms the Prime ONLY on a finding (a floor breach with a structural cause, or a failed key verification); a GREEN audit stays in the rotation record. MEASURED 2026-09-16 14:0xZ: no rotation record carries an audit key (belam.20260916T114647Z.json and every other); sensei.py writes only draft files (:1993); every audit result today lived in drafts + dms. CLAIM, one kid, sensei.py + its tests only, rotate.py untouched: (1) rotate-out-audit and wake-audit, after resolving their window, write their result INTO the audited rotation record under one top-level key `audit` = {out|wake: {calls, a, b, c, d, floor, excess, transcript, window_start, window_end, audited_at, audited_by}} - read-modify-write of that key only, every other key byte-identical (a test diffs the record before/after with the key removed), idempotent (a re-run replaces its own side), `--no-record` opts out (dry read); (2) the verb prints the one line the owner wants: `green <post> <side> --record <stamp> <calls> (floor N)` when excess is 0, else `FINDING <post> <side> --record <stamp> excess <n> over floor <N>` on stdout and exit 0 either way - the dm to the Prime stays a Sensei act, never sent by the verb; floors from the ladder (wake 0, out 1); (3) `rotate.py status --post S --record latest` shows the audit key as part of the record it prints. Falsifier: a record byte differs outside the audit key after a run; a re-run grows the record; a wake with excess 0 prints anything but green. Every printed line names the record stamp, never a generation."
thought_session: dissolve-legacy-2026-09-19
title: L4 the sensei audit verbs write their result into the rotation record and name a finding only over the floor
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-sensei-audit-verbs-write-their-result-into-the-rotation-record-and-name-a-finding-only-over-the-floor

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Amended after the SL7.133 review (belam 14:36Z, wf_d412f952-ff6) - the earlier "(4) No deviation" was FALSE: two deviations landed. (a) FLOORS: the kid wrote AUDIT_FLOOR as a module constant copied from the owner verbatim, a second copy of config:rotations floor_wake/floor_out that _read_rotations already hands both verbs - the claim said "floors from the ladder"; ruled: read the cells (SL7.134 b). (b) CALLS DEFINITION: audit.calls is the window count each verb already computed (out = calls after the last real act; wake = calls before the first (d)), not a new measurement - the claim did not say which. Also carried to SL7.134: the STARTED-record rewrite drops a wake audit written before the outcome (rotate.py preserve list), the write-back lands in the SHARED sessions dir so the Sensei commits the audited record by exact path in the same turn (ruling on g17.1), and the verb should commit it itself. Landed 7db33b255; first live write-back thought-master --record 20260916T110753Z out FINDING excess 9 over floor 1, committed 834cdf010.
<!-- THOUGHT:END -->
