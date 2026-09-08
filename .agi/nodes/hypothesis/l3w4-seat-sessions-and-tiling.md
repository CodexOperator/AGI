---
id: hypothesis:l3w4-seat-sessions-and-tiling
mint_id: e254cbdf45a84cb99bbfda36769e2e37
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-XI
scaffold_hash: 45218ed64ae7a1e1
season: 2
testable_claim: "After the change, one command brings up a live background remote-control session for every non-ephemeral seat in config:seats exactly the way Belam's own session is brought up — same head, same model and effort from the seat row, same CLAUDE_CODE_WORKFLOWS gate — and each one answers a read-back; rotate.py status lists every seat as attached with a real session id rather than no_pin; and a separate tiling step arranges the corresponding terminals on the X :1 desktop automatically, re-tiling when a seat is added or rotated. Three red-first tests fail today and pass after: a dry run resolves one launch command per non-ephemeral seat row from seats.md with that row's model and effort, a seat with session_kind fire-and-forget is excluded, and the tiler computes a full-screen partition for N windows with no overlap and no gaps."
thought_session: belam-S1-L3-XI
title: Every non-ephemeral seat gets its own remote-control session, and the desktop tiles them
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-seat-sessions-and-tiling

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD IT. Your artefact is a DIFF; if git diff --stat is empty you are not done. OWNER ASK, 2026-09-07 ~23:3x UTC, verbatim: 'make sure that all of the non-ephemeral roles get their own remote-control background sessions the way Belam does and that separately on the actual desktop screen all the sessions get tiled automatically. I want to start livestreaming this process from the remote box'. WHY IT IS TWO THINGS IN ONE BRIEF: they share a trigger (a seat comes up or rotates) and they are useless apart — sessions with no tiling cannot be watched, tiling with no sessions has nothing to show. WHAT EXISTS. rotate.py spawn_window is ALREADY the single launch path for spawn and loop (experiment:a00-716d4b22-b2db4e, L3.24) and it is what brings up a Belam; brief.py assembles the head per tier; config:seats carries harness, model, effort, settings, session_kind and pin_ref per seat, and session_kind already distinguishes remote-control from tty from fire-and-forget. So the launcher and the registry both exist and nothing joins them: today only the prime is ever spawned this way, by hand, one at a time. Do not write a second launcher — extend the one that works. WHAT IS MISSING AND IS THE REAL WORK: bringing up N sessions is not N times bringing up one. Each needs its own pin file so rotate.py meter reads ITS transcript and not the prime's (that exact bug is trap 0c and it has bitten twice), its own comms identity so send.py routes to it, and a read-back that confirms the window exists — never trust a printed success, because rotate.py loop reported a successful rotation and spawned no window at all (L3.32, fixed at L3.33 but confirm by tmux capture-pane anyway). THE TILING is genuinely separate and should stay a separate command that reads the live window list rather than being wired into spawn: the desktop is X display :1, the terminals are what the livestream will show, and the tiler's only job is a full-screen partition with no overlap and no gaps that re-runs when the set of seats changes. Prefer whatever WM control the box already has over adding a dependency. LIVESTREAM CONSTRAINT, and it is a real requirement not a nicety: whatever is on that screen is public. No pane may render a secret. Check what your layout exposes before you call it done.

BUILD IMPERATIVE (added by belam-S1-L3-IX; standing until `hypothesis:l3-brief-build-imperative-missing` lands it in `brief.py`'s kid template, after which this paragraph is redundant rather than wrong).

YOUR ARTEFACT IS A DIFF. An empty `git diff --stat` at the end means you are NOT done. This brief is an instruction to BRING A STATE ABOUT, not a question about whether that state holds today. Measuring the present, confirming the defect and stopping is NOT a result here — it was measured six times in this loop, decisively at L3.34 where four independent parents returned four honest red-first baselines with zero lines of code between them. Diagnose, then FIX, then prove it with a test that is RED before your change and GREEN after. A fix you tried that turned out to be wrong or impossible, stated plainly with the measurement that shows why, is a real result. Silence about the code is not.

TWO STANDING PROHIBITIONS FOR EVERY WAVE-4 SEAT BRIEF: (1) do not write to `.agi/nodes/.geometry/seats.md` — the Sanctuary Master owns that registry, and a seat that installs its own row is the exact failure this separation exists to prevent (it happened twice at L3.36 and both rows were dropped). If your seat needs a row, STATE THE ROW YOU WANT IN YOUR NODE BODY as a request to her. (2) Do not start, populate or run any real seat: the owner's standing gate (HANDOFF.md §6 item 47, verbatim "once we verify that perpetual seats work well and fully let's just stop there for a bit before we start them running") means BUILD the mechanism, PROVE it live, then STOP.

YOU HOLD A BRANCH — READ THIS BEFORE ANYTHING ELSE (Belam XI, L3.43, 2026-09-08). You were dispatched with `--branch`, so you are in your own git worktree on your own `loop/...@s2` branch. **COMMIT YOUR KID'S WORK TO THAT BRANCH BEFORE YOU EXIT.** From inside your worktree:

    git add -A
    git commit -m "L3.43 <your agent id>: <what landed>"

MEASURED TWICE NOW, INCLUDING THE ROUND IMMEDIATELY BEFORE THIS ONE: every `--branch` parent so far has exited with its branch at ZERO commits ahead, `season.py merge-up` then merged an empty branch and REPORTED GREEN, and a human had to harvest the work by hand from inside the worktree. A round that ends with your branch empty has produced nothing as far as every automated reader is concerned. You are the live proof that this can work — see `hypothesis:l3-parent-brief-forbids-the-only-commit`.

Do NOT push. Do NOT merge. Do NOT touch `season/s2`. The director merges. Commit locally on your own branch, that is all.

Run on pi/OpenRouter. Your kid: `python3 extensions/agi/bin/dispatch.py . L3.43 --target <this node> --level small --tier kid --harness pi`. Do NOT run `workflow.py run` for any reason this round.
