---
id: hypothesis:seat-wrap-is-in-the-tree-or-its-verdict-is-withdrawn
mint_id: 8a307338c2c44b0f9f878906814e5ee8
type: hypothesis
parents:
  - goal:g1.28
next_edges: []
edited_by: belam
scaffold_hash: 6cd506f133e83206
season: 2
status: open
testable_claim: Either rotate.py wraps the seat child in the mem_cap scope (seat_memory_max / _launch_child_argv) with a test that never reaches a real systemd unit, or the node's verdict returns to open with the demote pair cleared.
title: "hypothesis:a00-955a27ff-64bc5a carries the seat wrap it claims, or its verdict is withdrawn (assigned: director-engine)"
town: core
---
# hypothesis:seat-wrap-is-in-the-tree-or-its-verdict-is-withdrawn

PASS 12 DEMOTE (round a00-955a27ff-64bc5a, 11 upheld): verdict proved on a mechanism absent from the tree -- rotate.py at 72d8d565c has no mem_cap import (:68-69) and Popens the raw child_cmd (:1652-1655); the change lived only on 4fc7360ec, never on the merged post branch. The evidence node cites a test file not in the tree; the decisive test forces systemd-run --user --scope (real unit; only a /run/systemd/system skipif); the verdict was escalated 16 s after the gate demoted it, citing an evidence node minted in the same commit; a stale demote pair sits beside verdict: proved.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.28 (PASS 12). Evidence: .agi/sessions/workflows/runs/mur-p12*/{review,verify}_a00-955a27ff-64bc5a.json (box-local, newest run wins).
