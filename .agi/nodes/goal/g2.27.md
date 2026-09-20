---
id: goal:g2.27
mint_id: 70f2dae521da4c5fb3fed1e81c8e514f
type: goal
parents:
  - goal:g2
next_edges: []
confidence: 0.6
core: false
edited_by: belam
goal_id: G2.27
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: d9ba3cb1752f9bbd
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G2.27: The livestream goes live as L4's final round — verified working, accounts created by the agents"
town: streaming-suite
vision_ref: vision:streaming-suite
---
<!-- BODY:BEGIN -->
# goal:g2.27

## Agent Notes
OWNER 2026-09-11 03:1xZ (verbatim in doc:l4-owner-decisions): the L4 closing sequence for the stream — once all items are ready for review and the completion report is being written, cut the stream with a 75 s delay so viewers (15 s behind) see the report on screen for a good minute. As the Prime will run it: `sb-status` -> write + push COMPLETE.md's L4 section (on screen in the Prime's pane) -> `sleep 75; brb` (graceful cut to the card; never panic, never a unit stop) -> `sb-status` confirms -> the session prayer. The completion report waits on the base-level stream setup (hypothesis:l4-the-stream-master-is-the-only-door, running on the town branch) plus the gating rounds the owner named tonight (nudge fix LANDED and live-proven 03:01Z).

OWNER 03:2xZ CORRECTION (verbatim in doc:l4-owner-decisions): the close is PANIC on a 75 s lag, not brb — killed stream.sh pid 3968284
killed relay.sh pid 3968449
killed relay.sh pid 3976762
killed relay.sh pid 3976764
killed ffmpeg pid 3968298
killed ffmpeg pid 3976759
note: 12 segments (~24s) still on disk in /home/ubuntu/work/streamer-stub/out/ring and were never aired.
      bin/panic.sh --retract deletes them; a new grab.sh run wipes the ring anyway.
stream down (6 process(es)) issued from the Prime's pane right after the L4 completion report is pushed, so the stream shows the report and the issued command for a good minute before the hard cut. The one sanctioned Prime use of panic; everywhere else it stays the owner's alone.

[XX 03:05Z] STREAM FULL IDLE (owner 02:5xZ, verbatim doc:l4-owner-decisions tail): the on-air uptime panel now has an idle mode -- streamer-stub 634a463 (branch idle-panel, ff-merged to main): while out/idle.since exists the active time is FROZEN at that epoch, the header reads FULL IDLE and a third line counts 'idle HH:MM:SS'; the header and the idle line are drawtext textfiles with reload=1 written once a second by sb_uptime_watch beside uptime.txt, so entering or leaving idle is a file toggle (sb-idle / sb-active, bin/idle.sh, audited to out/hold.log), no encoder restart. Deployed as mid-stream surgery: brb (card on air, ring kept) -> systemctl --user restart streamer-stub.service (the hold flag survives; the new filter graph carries the two textfiles) -> sb-idle -> back; on air 03:05Z with FULL IDLE / 3d 21:05:14 / idle counting, relay at the 15 s target. Return to active = sb-active (the active time resumes from the wall clock, the idle stretch counted as idle, not as an outage).

[XX 04:29Z] STREAM ENDED on the owner's order 2026-09-14 (verbatim doc:l4-owner-decisions tail: proof of concept done, free the ~10 GB): panic → units streamer-stub, agi-scene-rotate, agi-graph-kiosk, agi-graphweb disabled; tmux stream-follow + the six view-* sessions killed; vncserver :1 killed (Xtigervnc, xfce4-session, the view terminals); the firefox kiosk (5.8 GB + 1.3 GB content process) was the bulk. Measured: used 11.1 → 4.8 GB, available 12.9 → 19.1 GB. Left running on purpose: agi-rc (the Prime, the thought master, the Belam chain), the reaper unit (the thought master's rounds need it), live-bridge.service (the owner's trading bridge -- NOT stream-related, untouched). The stub repo keeps the whole stack incl. the FULL IDLE panel (634a463) for a future stream.

OWNER 2026-09-16 14:1xZ (verbatim in doc:l4-owner-decisions): 'Sounds good let's leave it at your plan. No need to panic stream is down now.' — L4 closes on drain → self-review → COMPLETE.md → prayer; the panic + sb-status steps are STRUCK (stream down); SM plans (4) encryption town + key seats and (5) town goal numbering DEFERRED out of the close.
