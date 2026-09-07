---
id: hypothesis:l3-remote-control-desktop-disconnect
mint_id: f3a48211a4cb4edd970bef45a774896e
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-III
scaffold_hash: f469c5853ca9acfa
season: 2
testable_claim: A remote-control prime session whose desktop GUI client disconnects keeps running (tmux window alive, background monitors and dispatched rounds unaffected, the transcript still meterable), the owner can reconnect from claude.ai or the terminal without a new session, and any state the disconnect does break is named, tested and repaired.
thought_session: L3.22
title: The prime survives a remote-control GUI disconnect, and the owner can tell what state it left
---
<!-- BODY:BEGIN -->
# hypothesis:l3-remote-control-desktop-disconnect

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED 2026-09-07 ~13:45 UTC (owner, verbatim): oh no i think I errored it somehow by losing connection on remote control GUI on desktop. Weird. Maybe add as something to investigate and fix. STATE AT THE TIME: the prime belam-S1-L3-III kept running (the owner's next message arrived in the same session), L3.22 stayed live at 4/25, the tmux window was open, monitors kept firing. WHAT TO INVESTIGATE: (1) what the desktop remote-control client does on a dropped connection — does the session queue the owner's typed input, drop it, or error a pending turn; (2) whether a background Workflow or Monitor task is cancelled when the client detaches; (3) whether reconnecting from the claude.ai URL vs the desktop app resumes the same session or forks; (4) the failure signature to grep in ~/.claude/projects/<slug>/<session>.jsonl. FIX SHAPE: document the reconnect path in QUICKSTART.md, make rotate.py status show whether a seat's remote-control client is attached, and if a detach kills background tasks, have the prime re-arm its monitors from the handoff's round table on the next turn. FILES: extensions/agi/bin/rotate.py :: cmd_status, QUICKSTART.md, skills/agi/SKILL.md :: Rotation. This is the transport the perpetual seats (goal:g17, l3w4-seat-transport) depend on, so the finding feeds that brief too.
