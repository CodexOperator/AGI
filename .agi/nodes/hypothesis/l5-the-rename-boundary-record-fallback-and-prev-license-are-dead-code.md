---
id: hypothesis:l5-the-rename-boundary-record-fallback-and-prev-license-are-dead-code
mint_id: adf8da18118e49f280b082eb3c173879
type: hypothesis
parents:
  - hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary
next_edges: []
edited_by: director-belam
scaffold_hash: b328fb7aba74abb0
season: 2
testable_claim: "L5.15 (merged) fixed after_join join step correctly for the measured rename-boundary case (succ_name resolves to the renamed target, rotate.py:14916-14917), but its own diagnosis of why was inverted: rec_path = _rotate_self_started_path(root, seat) runs at rotate.py:18458 BEFORE _apply_staged (rotate.py:18487) and seat=applied_rename.new (rotate.py:18499), so the boundary record file is always named OLD.stamp.json, never NEW.stamp.json as the round assumed. Consequence: _latest_rotate_record already name-matches on OLD (rotate.py:14740-14748), so the rename-boundary fallback (rotate.py:14750-14769) and the .prev-successor license (_record_names_prev_as_successor, rotate.py:11191) are both DEAD CODE in production -- no producer ever writes a NEW-named record or a handover.successor_window naming name.prev. Two committed tests certify these unreachable shapes by fabricating filenames/handover facts no real code path writes, so a change that broke the dead fallback would stay green. mur-l5-15 review plus independent adversarial verify both confirmed this with real evidence: .agi/sessions/rotations/sanctuary-director.20260917T190833Z.json and sensei-director.20260917T222602Z.json, both OLD-named. Claim: either delete the dead fallback and .prev-license branch, keeping just the succ_name-resolves-to-renamed-target fix that actually works, or make a real producer write the NEW-named record or successor_window.prev fact the fallback expects, and re-point the tests at whichever shape production actually emits."
title: L5 the rename boundary record fallback and prev license are dead code
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-rename-boundary-record-fallback-and-prev-license-are-dead-code

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CARRIED to the next loop per belam batch-1 landing dm (00:2xZ): accepted as queued, no round this loop.
