---
id: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
mint_id: db9975ffca0e467ca1cfc2ce510630e9
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.8
edited_by: a00-5632e757
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

The resolved ceiling is 20 production lines / 1 kid, read from the clause, not the default. (The "1 kid" in this heading is right for the NEXT round; DH.569 itself ran two kids against it -- the second ran over.)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version, minted by director-engine for goal:g7.33.17 row 21 on thought-master's TMM.277 (03:04Z 09-27): FAST-TRACK right after the nudge fix (row 20). From director-thought's 03:02Z [engine] report.
<!-- THOUGHT:END -->
