---
id: hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first
mint_id: e358771243ca44d091202615648b45c7
type: hypothesis
parents:
  - goal:g6.12
next_edges: []
edited_by: belam
scaffold_hash: d918f5038bef9d5d
season: 2
testable_claim: heal watch re-sends the overdue dm for a live agent every comms.overdue_repeat_min (default 30) minutes after the first firing, each occurrence naming elapsed minutes and the pid, and never cuts a replacement for a pid that is still alive.
thought_session: dissolve-legacy-2026-09-19
title: L5 the overdue alarm re fires every thirty minutes after the first
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-overdue-alarm-re-fires-every-thirty-minutes-after-the-first

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
