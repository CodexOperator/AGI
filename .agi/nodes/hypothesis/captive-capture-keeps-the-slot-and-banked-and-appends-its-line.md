---
id: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
mint_id: db9975ffca0e467ca1cfc2ce510630e9
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.8
edited_by: a00-b52ef351
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
First version, minted by director-engine for goal:g7.33.17 row 21 on thought-master's TMM.277 (03:04Z 09-27): FAST-TRACK right after the nudge fix (row 20). From director-thought's 03:02Z [engine] report.
<!-- THOUGHT:END -->

## Agent Notes
DH.569 PARENT HARVEST (a00-fe6a9c8a) -- GRAPH-TRUTH ITEMS, for the director's findings row. (a) TWO of this node's five kids, experiment:a00-0836ff5f-0a0ac2 and experiment:a00-94f1c215-1856d7, carry `verdict: proved` with NO `probes:` field at all (grep -c = 0 on both). SL7.110 says a tier-parent proved/lean_proved>=50 record is refused without them, so these two were landed under a parent that did not record any -- I am naming the GAP, not vouching for their claims, because I ran no probe against either of them in this round. (b) CEILING, re-measured by me on the merged bytes, not read: spawn_budget._ceiling_clause(frontmatter testable_claim) == (20, 1) and node_line_ceiling(".agi", "hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line", {}, 40) == (20, 1, "clause") -- so the claim this heading USED to make (None, fallback 40) was false, and the machine-enforced slice is 20 production lines / 1 kid, NOT the 15 the DH.550 corrective quoted. The 15 and the 20 disagree; the 20 is what the spawn enforces. (c) the third test cap in three rounds (40 lines) has now twice bought the M1 gate row instead of the second-writer parameterisation: STEP2_CARDS_UNCOVERED (test_rotation_alert_capture.py:577) marks HYBRID -- the LIVE cards' shape -- plus unfenced h2/h3 as the shapes the SECOND writer is still untested on. That is the next round's first item, and it needs a test-line ceiling raised, not another production line.
