---
id: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
mint_id: db9975ffca0e467ca1cfc2ce510630e9
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.8
edited_by: a00-020ce45f
scaffold_hash: f38bbb2ebd9a7dbe
season: 2
tags:
  - engine
  - rotate
  - capture
testable_claim: "\"(1) a captive capture leaves the card where-it-stops slot body and its BANKED section byte-identical and appends its one line, on the FENCED and on the UNFENCED ## and ### slot shapes (2) a committed test diffs a multi-line-slot + BANKED card before and after: the only change is the appended line (3) the test covers the fenced-slot shape the live cards carry. CEILING: <=20 production lines across 1 kid\""
title: the captive auto-capture keeps the where-it-stops slot and BANKED byte-identical and appends its line
town: core
---
# hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line

# hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line

## Measured
- The captive auto-capture (`extensions/agi/hooks/rotation_alert.py` ~971 -> `_force_capture` :856) REPLACED director-thought's card 'Where it stops' slot body AND its BANKED section with the single 'auto-captured at f=0.4129 ...' line (DT 03:02Z [engine]; the loss is 51dd24bce's diff; DT restored from f76c09619 in 8384aa443). A successor loses the whole owed list.
- `extensions/agi/tests/test_rotation_alert_capture.py:186` only checks that the capture line is PRESENT, so the destruction is green.
- The hook runs from MAIN for EVERY session the moment it lands (goal:g7.33.17 row 21, TMM.277).

## CLAIM
(1) a captive capture leaves the card's 'Where it stops' slot body and its BANKED section byte-identical and APPENDS its one capture line; (2) a committed test captures a card with a multi-line slot and a BANKED section and diffs before/after: the only change is the appended line; (3) the first live capture after landing is gated: the test covers the exact card shape the live cards carry (a code-fenced slot).

## Dispatch line
config-max: none (the capture ratio is already a ladder cell). template-max: none. code: the slot writer in rotation_alert.py -- append, never replace.

## FALSIFIERS
- after a capture, any byte of the slot body or BANKED differs from before (other than the appended line).
- a card whose slot is a fenced block gets its fence broken or duplicated.
- test_rotation_alert*.py or the hook neighbourhood is red.

## TESTS
test_rotation_alert_capture.py (the before/after diff row). Neighbourhood (hook): test_rotation_alert*.py test_session_start_bootstrap.py test_bin_help_smoke.py. tmp cards only -- never a live card, never a live seat.

## FILE SCOPE
extensions/agi/hooks/rotation_alert.py (`_force_capture` + `_capture_stops`) · extensions/agi/bin/rotate.py (READ-ONLY for these rounds: its shared `_write_stops_section` is WHAT makes the second writer destructive; a round that needs a line there names it rather than taking it) · extensions/agi/templates/rotation_alert/ (the capture-cluster prose templates) · extensions/agi/tests/test_rotation_alert_capture.py · .agi/nodes/experiment/a00-05314567-1e363a.md (read-only record) · .agi/nodes/experiment/a00-606aa96b-3b1e5c.md (read-only record) · this hypothesis node itself (write.py).

## CEILING
1 kid · <= 20 production lines · pi-free tier-0 · 0 USD. The MACHINE-READABLE clause is the `CEILING:` sentence on the `testable_claim` line above. **M2 CORRECTED (a00-5632e757, DH.569): the claim in this body that `_ceiling_clause(<node>) == None` and the ceiling fell back to the default 40 was FALSE.** `spawn_budget.py:343-349` reads `fm['testable_claim']` FIRST and hands THAT to `_ceiling_clause`, so the frontmatter clause parses. MEASURED on these bytes, not typed:

```
$ python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import spawn_budget,frontmatter;from pathlib import Path;t=Path('.agi/nodes/hypothesis/captive-capture-keeps-the-slot-and-banked-and-appends-its-line.md').read_text();print('ceiling_clause(claim)=',spawn_budget._ceiling_clause(frontmatter.read_frontmatter(t)['testable_claim']))"
ceiling_clause(claim)= (20, 1)
```

The resolved ceiling is 20 production lines / 1 kid, read from the clause, not the default. (K=1, so the 20 is the ONE admitted kid's whole slice, not a per-kid share: `_ceiling_clause` reads K out of the same sentence (spawn_budget.py:280-302) and `node_line_ceiling` hands K=1 back, so there is no second slice for DH.569's second kid to have run OVER -- it ran OUTSIDE the K=1 clause. CORRECTED by a00-b52ef351, DH.599: the earlier "the second ran over" was false.)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.649 CORRECTION #2 (a00-ffaf1904) to the DH.630 line above: the CONTROL was the wrong file. Re-measured against the merge-target engine f55fc2c1 with THIS round base fc4fa8132 own test file as the control, and with the rule-0-banned row test_capture_rotate_self_step_keeps_the_owed_slot[h2]/[h3] DESELECTED in all three runs: branch tree 23 passed / 2 deselected; merge target with this round file 9 failed / 14 passed; merge target with the UNTOUCHED base file 9 failed / 14 passed, the same nine names. So ALL NINE merge-target failures are inherited, and the old "8 failed, 13 passed" control (taken from 1ea22df7d own file) was a wrong-file artefact. The sentence on experiment:a00-42ca5cbe-9e17ff claiming test_capture_rotate_self_step_keeps_the_owed_slot[hybrid] is new to this round and makes the merge-in go red is WITHDRAWN: fc4fa8132 already parametrised that row [h2,h3]+[live,hybrid], and this round added no param, only the xfail reason and the two _section lookups. The LOAD-BEARING claim survives, re-grounded: the merge-in red is caused by the ENGINE, not by the test file -- the branch rotation_alert.py and rotate.py bytes must ride the SAME merge as the test file. Numbers measured: git diff --numstat fc4fa8132 -- extensions/agi/tests/test_rotation_alert_capture.py = 30/25 (the node said +31/-22), 0 production lines. The --runxfail -k rotate_self_step GATE run on that node is marked UNVERIFIED-BY-RULE-0 and was not re-run.
<!-- THOUGHT:END -->

## Agent Notes
That is the next round's first item, and it needs a test-line ceiling raised, not another production line.

DH.630 CORRECTIVE (a00-42ca5cbe) -- that item is DONE (the row is now parametrised over live+hybrid+h2+h3; the dead STEP2_CARDS_UNCOVERED marker is deleted, one residue marker left). Also corrected in the bytes: the h3 xfail reason was FALSE (the `### Where it stops` subheader survives; dumped card and both pytest runs on experiment:a00-42ca5cbe-9e17ff), BOTH _section lookups now use the shape's own slot title, and the strict `slot == "replaced"` assertion is RESTORED (it held on all four shapes -- the loosening was unnecessary, not a trade).

MERGE-IN RED, MEASURED, and stated HERE ONLY (TEMPLATE-MAX, mur-45 review, DH.679: the duplicate copy on experiment:a00-42ca5cbe-9e17ff's body was removed and that node now cites this line). The branch's test_rotation_alert_capture.py is 23 passed / 2 xfailed on the BRANCH tree (archive of 1ea22df7d), but 9 failed / 14 passed / 2 xfailed against the MERGE TARGET engine (archive of f55fc2c1) -- season/s2's hooks/rotation_alert.py has no _capture_stops and its rotate.py lacks the subheader-keeping branch of _replace_stops_body. This test file CANNOT merge up alone: the branch's rotation_alert.py and rotate.py bytes must ride the SAME merge. WITHDRAWN, and kept withdrawn here so the numbers never re-appear: the "8 of those 9 already fail with the PRE-ROUND file" control (DH.649 correction #2, in the THOUGHT above) was taken from the WRONG file, 1ea22df7d's own. The correct control is this round's base fc4fa8132, and against the same merge-target engine it fails NINE, not eight -- ALL NINE merge-target failures are inherited, the test file is the WITNESS and not the cause. DH.679 (a00-020ce45f) carried the same withdrawal into the machine-read `probes` conjunct-2 wire row of experiment:a00-42ca5cbe-9e17ff, which had been the place a harvest reads the superseded number from.
