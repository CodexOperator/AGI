---
id: hypothesis:l4-a-kid-reports-to-its-parent-and-the-seat-hears-one-dm-per-round
mint_id: 8d3313bb78824f3fa6c36c27c480aad3
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: f463238b1ee1ba18
season: 2
testable_claim: "goal:g15 (Prime XXI 08:0xZ 2026-09-14; MEASURED: three kid dms to belam within 17 min of dispatching L4.367/L4.368 from the Prime pane — a00-3588e734 07:46Z, a00-dcbb83a2 07:55Z, a00-5573f9e5 07:59Z, each `iter=… agent=… node=experiment:… verdict=…` — because a kid completion line is sent to AGI_SEAT, the DISPATCHING seat, and every nudge wakes a Claude Code pane = one paid turn under the owner 3%/48 h budget, owner 03:0xZ on goal:g14): CLAIM: a kid completion line goes to its PARENT (appended to the round manifest under the kid entry and to the parent inbox), never to the dispatching seat; the seat receives exactly ONE dm per round, from the parent at harvest — accepted/demoted/failed counts, node ids, branch tip — and `send.py send <seat>` from a kid (AGI_TIER=kid) is refused with one line unless the target is its own parent; the parent prompt and the kid prompt name this shape in one sentence each; a fixture proves N kids -> 0 seat dms + 1 parent dm with the asserted shape, on a fake tmux (no live pane is ever nudged by a test); rounds already live keep their behaviour. FALSIFIERS: a kid can still reach any seat by dm; a parent harvest produces more than one seat dm; the seat dm lacks the branch tip."
title: A kid reports to its parent; the dispatching seat hears one dm per round (Prime XXI 2026-09-14, measured under the 3% CC budget)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-kid-reports-to-its-parent-and-the-seat-hears-one-dm-per-round

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
