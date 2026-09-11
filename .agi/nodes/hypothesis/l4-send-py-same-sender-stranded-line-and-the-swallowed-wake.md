---
id: hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake
mint_id: 3737045155144ec7ba794c0b3092389d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-nudge-carries-the-dm-body-inline
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 54c2f3dd7bd3a2cf
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-21: send.py:809 — a stranded pane line from the SAME sender counts as 'ours', so a new same-sender dm is neither typed into the pane nor deferred (lost until the next wake); :741 — when a deferred dm is delivered, the inbox send's OWN wake is swallowed; `_NUDGE_LINE_MAX=95` is model-derived, not measured; the two busy-defer tests (:511, :747) still use the synthetic pane. CLAIM: (a) the type/defer decision treats a stranded line from the same sender exactly like a foreign one; (b) delivering a deferred dm and the current send each produce a wake (or ONE combined nudge that names both), none swallowed; (c) `_NUDGE_LINE_MAX` is set from a measurement on a live 104-column pane (the capture and the arithmetic in a comment next to the constant); (d) tests :511 and :747 run on the real capture fixture (hypothesis:l4-the-busy-pane-fixture-is-a-real-capture). TESTS: capture-based, one per clause; a same-sender stranded line + new dm -> typed or deferred, never dropped; deferred delivery + fresh send -> two wakes (or one naming both). FALSIFIER: a same-sender dm still silently dropped, or a wake lost. CEILING: 2 kids (a+b / c+d, disjoint regions). FILE SCOPE: extensions/agi/bin/send.py + extensions/agi/tests/test_send.py. EXCLUDED: everything else."
thought_session: sanctuary-director-gen12
title: "send.py: a same-sender stranded line is not 'ours', a deferred delivery never swallows the current send's wake, and the nudge width is measured on a pane"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-send-py-same-sender-stranded-line-and-the-swallowed-wake

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-21: send.py:809 — a stranded pane line from the SAME sender counts as 'ours', so a new same-sender dm is neither typed into the pane nor deferred (lost until the next wake); :741 — when a deferred dm is delivered, the inbox send's OWN wake is swallowed; `_NUDGE_LINE_MAX=95` is model-derived, not measured; the two busy-defer tests (:511, :747) still use the synthetic pane. CLAIM: (a) the type/defer decision treats a stranded line from the same sender exactly like a foreign one; (b) delivering a deferred dm and the current send each produce a wake (or ONE combined nudge that names both), none swallowed; (c) `_NUDGE_LINE_MAX` is set from a measurement on a live 104-column pane (the capture and the arithmetic in a comment next to the constant); (d) tests :511 and :747 run on the real capture fixture (hypothesis:l4-the-busy-pane-fixture-is-a-real-capture). TESTS: capture-based, one per clause; a same-sender stranded line + new dm -> typed or deferred, never dropped; deferred delivery + fresh send -> two wakes (or one naming both). FALSIFIER: a same-sender dm still silently dropped, or a wake lost. CEILING: 2 kids (a+b / c+d, disjoint regions). FILE SCOPE: extensions/agi/bin/send.py + extensions/agi/tests/test_send.py. EXCLUDED: everything else.
