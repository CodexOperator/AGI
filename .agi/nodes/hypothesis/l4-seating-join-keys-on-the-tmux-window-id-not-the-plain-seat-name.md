---
id: hypothesis:l4-seating-join-keys-on-the-tmux-window-id-not-the-plain-seat-name
mint_id: b35460f7117f4ac4a221ec1ae455a69a
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
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
