---
id: hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window
mint_id: e0457c3a9004402b8ef15277466dc97a
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-rotate-self-keeps-the-numeral-window-reaps-fifo-and-records-before-it-terms
next_edges: []
edited_by: sanctuary-director
scaffold_hash: fa269fe6e3d23795
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-12: `_reap_belam_oldest` (rotate.py:3204-3215) returns SKIPPED when the oldest window has no pane pid or no descendants — and then does NOT kill the window, so the chain can stay above five (the owner's cap is on the CHAIN, five windows). CLAIM: on every SKIPPED path the oldest window is still killed by its @id (`tmux kill-window -t @id`), the record says `{reaped: false, skipped: <named reason>, window_killed: true, window_id}`, and a window that no longer exists is recorded as `already gone` (not an error); the reap-by-PID path is unchanged. TESTS: fixtures for (a) no pane pid, (b) pane pid with no descendants, (c) window already gone — each asserts the window line is gone from the fixture window file (or `already gone`), the record fields, and that the chain count after is ≤ five. FALSIFIER: a SKIPPED cap that leaves six windows. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_reap_belam_oldest` ONLY) + test_rotate_handover.py. SERIAL on rotate.py behind hypothesis:l4-the-dry-run-names-the-oldest-it-would-reap. EXCLUDED: everything else."
title: When the Belam cap cannot derive the oldest chain it still kills the oldest window by @id — the chain never stays above five
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-cap-skipped-paths-still-kill-the-oldest-window

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-12: `_reap_belam_oldest` (rotate.py:3204-3215) returns SKIPPED when the oldest window has no pane pid or no descendants — and then does NOT kill the window, so the chain can stay above five (the owner's cap is on the CHAIN, five windows). CLAIM: on every SKIPPED path the oldest window is still killed by its @id (`tmux kill-window -t @id`), the record says `{reaped: false, skipped: <named reason>, window_killed: true, window_id}`, and a window that no longer exists is recorded as `already gone` (not an error); the reap-by-PID path is unchanged. TESTS: fixtures for (a) no pane pid, (b) pane pid with no descendants, (c) window already gone — each asserts the window line is gone from the fixture window file (or `already gone`), the record fields, and that the chain count after is ≤ five. FALSIFIER: a SKIPPED cap that leaves six windows. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (`_reap_belam_oldest` ONLY) + test_rotate_handover.py. SERIAL on rotate.py behind hypothesis:l4-the-dry-run-names-the-oldest-it-would-reap. EXCLUDED: everything else.
