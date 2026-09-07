---
id: hypothesis:l3w4-seat-sessions-and-tiling
mint_id: e254cbdf45a84cb99bbfda36769e2e37
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: 45218ed64ae7a1e1
season: 2
testable_claim: "After the change, one command brings up a live background remote-control session for every non-ephemeral seat in config:seats exactly the way Belam's own session is brought up — same head, same model and effort from the seat row, same CLAUDE_CODE_WORKFLOWS gate — and each one answers a read-back; rotate.py status lists every seat as attached with a real session id rather than no_pin; and a separate tiling step arranges the corresponding terminals on the X :1 desktop automatically, re-tiling when a seat is added or rotated. Three red-first tests fail today and pass after: a dry run resolves one launch command per non-ephemeral seat row from seats.md with that row's model and effort, a seat with session_kind fire-and-forget is excluded, and the tiler computes a full-screen partition for N windows with no overlap and no gaps."
title: Every non-ephemeral seat gets its own remote-control session, and the desktop tiles them
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-seat-sessions-and-tiling

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD IT. Your artefact is a DIFF; if git diff --stat is empty you are not done. OWNER ASK, 2026-09-07 ~23:3x UTC, verbatim: 'make sure that all of the non-ephemeral roles get their own remote-control background sessions the way Belam does and that separately on the actual desktop screen all the sessions get tiled automatically. I want to start livestreaming this process from the remote box'. WHY IT IS TWO THINGS IN ONE BRIEF: they share a trigger (a seat comes up or rotates) and they are useless apart — sessions with no tiling cannot be watched, tiling with no sessions has nothing to show. WHAT EXISTS. rotate.py spawn_window is ALREADY the single launch path for spawn and loop (experiment:a00-716d4b22-b2db4e, L3.24) and it is what brings up a Belam; brief.py assembles the head per tier; config:seats carries harness, model, effort, settings, session_kind and pin_ref per seat, and session_kind already distinguishes remote-control from tty from fire-and-forget. So the launcher and the registry both exist and nothing joins them: today only the prime is ever spawned this way, by hand, one at a time. Do not write a second launcher — extend the one that works. WHAT IS MISSING AND IS THE REAL WORK: bringing up N sessions is not N times bringing up one. Each needs its own pin file so rotate.py meter reads ITS transcript and not the prime's (that exact bug is trap 0c and it has bitten twice), its own comms identity so send.py routes to it, and a read-back that confirms the window exists — never trust a printed success, because rotate.py loop reported a successful rotation and spawned no window at all (L3.32, fixed at L3.33 but confirm by tmux capture-pane anyway). THE TILING is genuinely separate and should stay a separate command that reads the live window list rather than being wired into spawn: the desktop is X display :1, the terminals are what the livestream will show, and the tiler's only job is a full-screen partition with no overlap and no gaps that re-runs when the set of seats changes. Prefer whatever WM control the box already has over adding a dependency. LIVESTREAM CONSTRAINT, and it is a real requirement not a nicety: whatever is on that screen is public. No pane may render a secret. Check what your layout exposes before you call it done.
