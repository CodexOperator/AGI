---
id: hypothesis:l4-a-kid-reports-to-its-parent-and-the-seat-hears-one-dm-per-round
mint_id: 8d3313bb78824f3fa6c36c27c480aad3
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: f463238b1ee1ba18
season: 2
testable_claim: "goal:g15 (Prime XXI 08:0xZ 2026-09-14; MEASURED: three kid dms to belam within 17 min of dispatching L4.367/L4.368 from the Prime pane — a00-3588e734 07:46Z, a00-dcbb83a2 07:55Z, a00-5573f9e5 07:59Z, each `iter=… agent=… node=experiment:… verdict=…` — because a kid completion line is sent to AGI_SEAT, the DISPATCHING seat, and every nudge wakes a Claude Code pane = one paid turn under the owner 3%/48 h budget, owner 03:0xZ on goal:g14): CLAIM: a kid completion line goes to its PARENT (appended to the round manifest under the kid entry and to the parent inbox), never to the dispatching seat; the seat receives exactly ONE dm per round, from the parent at harvest — accepted/demoted/failed counts, node ids, branch tip — and `send.py send <seat>` from a kid (AGI_TIER=kid) is refused with one line unless the target is its own parent; the parent prompt and the kid prompt name this shape in one sentence each; a fixture proves N kids -> 0 seat dms + 1 parent dm with the asserted shape, on a fake tmux (no live pane is ever nudged by a test); rounds already live keep their behaviour. FALSIFIERS: a kid can still reach any seat by dm; a parent harvest produces more than one seat dm; the seat dm lacks the branch tip. RE-CUT as L4.372 (Prime XXI 14:3xZ 2026-09-14) after the pi review of the first parent branch season2/loops/hypothesis-l4-a-kid-reports-to-i-a00-90dc20b6 @47f1a2c9d (DEMOTED, not merged; START from that tip, keep experiment:a00-b10115c9-316b73, and fix): (R1) the central clause is unproven in the LIVE topology — the parent row lives only in the dispatcher manifest (MAIN .agi/sessions/iter-L4.369/manifest.json) while kid rows live in the parent worktree manifest; cli.py:550-558 _alarm_dispatcher_on_done reads _session_root() only and returns at row is None, so the parent branch (:583-595) never runs and the seat hears ZERO dms — measured: the L4.369 parent itself finished 14:0xZ with no seat dm; (R2) the fixture tests/test_kid_reports_to_parent.py:183-192 puts parent and kids in ONE manifest and cannot fail — drive the real cli.py done with the parent row in a separate dispatcher manifest and assert exactly one seat dm; (R3) the harvest unions both manifests (cli.py:506-507) so kid counts are never zero; (R4) the cli.py:569 kid report write takes the manifest lock dispatch holds (_manifest_lock, dispatch.py:762/812); (R5) send --room (send.py:4830/4851) is gated for AGI_TIER=kid like the dm paths."
title: A kid reports to its parent; the dispatching seat hears one dm per round (Prime XXI 2026-09-14, measured under the 3% CC budget)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-kid-reports-to-its-parent-and-the-seat-hears-one-dm-per-round

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.67 harvest observation (sensei-director, e4ce8a5df): the rounds own completion dm named its PARENT branch (season2/loops/hypothesis-l4-the-harvest-comple-a00-fb310b81) as the tip, but that branch was empty -- HEAD identical to the dispatching seats pre-dispatch commit, no kid work merged into it. The actual commits, including the done: commit, were on the KID branch instead (season2/loops/hypothesis-l4-the-harvest-comple-a00-8b7abc41). Harvested from the kid branch once found; content fully intact, nothing lost. Distinct from the SM.66/SM.67 iter-dir class of bug -- this is the reported branch NAME in the completion line being stale/wrong, not the dm failing to send. Flagged by SM for tracking here, not yet reproduced a second time.
