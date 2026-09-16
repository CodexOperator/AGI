---
id: hypothesis:l4-seating-join-keys-on-the-tmux-window-id-not-the-plain-seat-name
mint_id: b35460f7117f4ac4a221ec1ae455a69a
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: 23d19d053688e7ab
season: 2
testable_claim: "The seating join currently keys on the plain seat name, so a spawn using a custom launch name (for example --name director-sanctuary) leaves the row empty (Prime gen 21, measured 2026-09-16 06:35-06:39Z). Claim: the join should resolve by the @id tmux returns, so --name may legally differ from the seat name -- this is the precondition the owner 2026-09-14 16:1xZ GUI rename to director-sanctuary and director-thought needs."
title: L4 seating join keys on the tmux window id not the plain seat name
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-seating-join-keys-on-the-tmux-window-id-not-the-plain-seat-name

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Defect still reproducible: the window is created with `-n name` (args.name) but both join sites look it up by `seat` (args.seat) through a list-windows name-match; the @id tmux prints via -P -F is captured into proc and never returned, so --name != seat yields window_id None and an empty row. Only post-mint touch (e85a1a797, SM.243) adds more name-keyed calls. EVIDENCE: MEASURED: rotate.py:1821 `name = args.name`, :1857 `seat = getattr(args,"seat")`, :1600-1603 new-window -n name -P -F #{window_id}, :1614-1619 returns rc only (stdout discarded), :2137-2138 `_successor_window_id(seat, ...)`, :6021 same in first-seating join, :10715-10745 matches `name.strip() == seat`; `git log 9eaf028d0..HEAD -S_successor_window_id -- rotate.py` = e85a1a797 only, whose diff adds `_successor_window_id(new_name Never rounded at close (owner 14:1xZ).
