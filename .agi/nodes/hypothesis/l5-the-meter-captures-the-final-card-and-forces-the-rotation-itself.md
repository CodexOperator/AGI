---
id: hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself
mint_id: 184e3105aaef43ba80159b8431a9901b
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: ccff74b1e9263af5
season: 2
testable_claim: "(1) rotation_alert.py (the UserPromptSubmit meter hook): at f >= director_rotate_at, OR when a `rotate now` line from the seat's rotated_by holder or the owner sits unread/unacted in its inbox, the hook's additional context is an IMPERATIVE block -- 'ROTATE NOW: (a) write the card wholesale now, (b) run python3 extensions/agi/bin/rotate.py rotate; nothing else this turn' -- not a number and a band. (2) FORCE: the hook's existing background rotate-self path (goal:g15.25 line 4) stops waiting on the card-age captive forever: when the card is still stale N minutes (ladder cell, default 10) after the imperative first fired, the hook CAPTURES the final card itself -- `rotate.py handoff` (the driven §0 writer) refreshes the state block and writes the where-it-stops slot from measured state (last acts, live rounds, unread, the trunk tip, 'auto-captured at f=<f> after <N> min without a self-rotate') -- commits it by path, then runs rotate-self --force --stops <that line>; the predecessor is reaped as today (F1). The captured card is marked AUTO-CAPTURED in its header so the successor knows it was not authored. (3) IDLE BELOW THE LINE: `rotate.py alarms --holder <post>` (timer-driven, not prompt-driven) dms `rotate now` to a held seat at f >= director_rotate_at as today AND when the seat has been idle (no act: no card write, no send, no dispatch, no landing -- last_act.py) for >= M minutes (ladder cell, default 20) at f >= 0.85 x director_rotate_at; the dm is a nudge, the nudge is a prompt, the prompt makes (1) fire; alarms runs as a detached user unit per master (systemd-run --user, --working-directory + --root), declared in the cron node's services: table. (4) MEASURED trigger: director-sanctuary gen 6 sat idle at the prompt from ~01:20Z to 01:5xZ at f=0.444 (94% of 0.47) with its card written; the owner asked three times; the hook never fired (no prompt while idle, f below the line) and the alarms loop was not running (no holder unit). (5) TESTS (red-first, test_rotation_alert*.py + test_rotate.py): a payload at f >= line prints the imperative block; an unread 'rotate now' from the holder prints it below the line; a stale card N minutes after the first imperative -> handoff captures + rotate-self --force invoked with the generated stops line (subprocess recorded, nothing real spawned under AGI_HOOK_NO_SPAWN); alarms --once dms a held seat idle >= M min at 0.85 x line and stays silent for a working seat at the same f; the card written by the driven writer carries AUTO-CAPTURED and a non-empty stops line. FILE SCOPE: extensions/agi/hooks/rotation_alert.py, extensions/agi/bin/rotate.py (alarms + handoff), extensions/agi/bin/last_act.py (read only), .agi/nodes/.geometry/ladder.md (two cells), .agi/nodes/.geometry/crons.md (services: row), tests. CEILING 40 production lines (four conjuncts)."
title: "SM.135 (OWNER 01:5xZ 09-19 in the SM pane, verbatim: 'Can the meter automatically prompt the agent to self rotate or something' / 'It must capture and force final card update'; measured: director-sanctuary idle 25 min at f=0.444 with the card written, third owner ask; g15.25): the meter mechanism prompts the rotation, and when the post does not rotate in bounded time it captures the final card itself and forces rotate-self"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
