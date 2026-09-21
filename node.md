---
id: hypothesis:l4-a-nudge-cancels-copy-mode-and-re-fires-on-a-stale-marker
mint_id: f241328f9d4f4d69890e16bc9fb6f5f1
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: fcbc26930ef59317
season: 2
testable_claim: "goal:g15 (Prime XXI 14:1xZ 2026-09-14; MEASURED: the thought-master pane @366 sat in tmux copy mode (#{pane_in_mode}=1) from ~07:02Z to 14:1xZ and swallowed every nudge keystroke; its nudge marker .agi/sessions/inbox/thought-master.nudge stood since 02:44Z because the post never ran send.py read, and send.py types nothing while a marker stands, so the Prime lap-1 dm of 07:43Z queued silently for 6 h; recorded on goal:g17.1): CLAIM: (1) the nudge path in send.py reads #{pane_in_mode} for the target window before typing and, when set, sends `-X cancel` first (measured from a fake tmux fixture that records the key sequence: cancel precedes the nudge line iff in_mode); (2) a standing marker older than the post last-read stamp (or older than N minutes, N from config with a default of 30) is STALE — the nudge re-fires and the marker is re-stamped, with one log line naming the re-fire; a fresh marker still suppresses (no double-typing into a live turn); (3) `send.py status <post>` prints marker age, pending count, in_mode, and last-read, so a director sees a stalled post in one line; (4) the fixture proves the four cases: no marker, fresh marker, stale marker, copy mode; no live pane is touched by a test; the suite stays green under the ceiling. FALSIFIERS: a stale marker still suppresses; cancel is sent when not in copy mode (a spurious Escape into a live prompt); a fresh marker double-types."
title: A nudge cancels copy mode and re-fires on a stale marker (Prime XXI 2026-09-14; the 6-hour stall of the figure-eight)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-nudge-cancels-copy-mode-and-re-fires-on-a-stale-marker

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
