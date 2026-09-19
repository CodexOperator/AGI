---
id: hypothesis:l5-a-message-that-did-not-land-tells-its-sender-so-at-once
mint_id: 2cd10ca30e384ce3910544d959d190ea
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 9c348932855bfe62
season: 2
testable_claim: "(1) MEASURED: send.py send nudges the target pane on every send; when the seat row's pid registry (~/.claude/sessions/<pid>.json) or the pane capture reads busy the nudge is COALESCED and NOTHING retries it -- only a later send to the same seat 're-fires' it; on core-town no cron sweeps stale nudges (mail_poll is the remote-box reader, gated to local-town, and consumes inboxes, so it is not the retry). Every send to director-sanctuary 23:0xZ-02:0xZ printed `nudge: coalesced (pane busy (registry))`; the owner saw no nudge surface there while director-thought's (idle more often) did. (2) SEND OUTPUT: a send whose nudge was not typed prints one plain line `[undelivered-yet] <to> -- pane busy; the sweep retries, you hear [undelivered] after T min` instead of the coalesce jargon; a typed nudge prints `[delivered] <to>`. (3) RETRY: `send.py wake --all-local` sweeps every local row whose inbox has unread or whose nudge marker is stale, types the nudge when the pane is idle, no-ops when busy; a KNOWN cron job `nudge_sweep` (every 2 min, box: every box by default) runs it -- rendered by crons.py like mail_poll, declared in the cron node. (4) NOTIFY THE SENDER: each undelivered nudge is recorded with its send ts + sender; when the sweep finds it still untyped T minutes later (ladder cell, default 10) it dms the SENDER one line `[undelivered] <to> <send ts> '<first 80 chars>' -- pane busy <N> min` (once per message, never per sweep) and marks it notified; when the nudge finally lands, one `[delivered-late] <to> <send ts>` line closes it. The sender's own pane is nudged by that dm, so the sender learns at the deadline, never from tasks not getting done. (5) BRIEF (template half, by SM): §2 gains the line 'a send that prints [undelivered-yet] has NOT reached the pane; wake it with send.py wake <seat> or wait for the sweep; [undelivered] in your inbox names your own line that never landed'. (6) TESTS (red-first, test_send*.py + test_crons.py): busy registry -> [undelivered-yet] + a record; wake --all-local types it once the fixture pane is idle and prints [delivered-late]; T min stale -> exactly one [undelivered] dm to the sender, none on the next sweep; crons.py show renders nudge_sweep on every box; help-smoke green. FILE SCOPE: extensions/agi/bin/send.py (send output, wake --all-local, the undelivered record + notice), extensions/agi/bin/crons.py (KNOWN_JOBS += nudge_sweep), .agi/nodes/.geometry/crons.md (cadence row), .agi/nodes/.geometry/ladder.md (T cell), tests. CEILING 36 production lines (three conjuncts)."
title: "SM.136 (OWNER 02:0xZ 09-19 in the SM pane: dms to director-sanctuary never surfaced while director-thought's did; 'we need to make sure that that is automatically notified to you so that you know, oh, wait, that message didn't deliver'; g15): a nudge coalesced on a busy pane is retried until it lands, and a message not typed into its pane within T minutes dms its SENDER an [undelivered] line at once"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-message-that-did-not-land-tells-its-sender-so-at-once

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SCOPE += (7) CRON BOX GATES (owner 02:1xZ): a cadence with no box runs on EVERY box (crons.py already treats absent as all) and that is the documented DEFAULT in [cron].md; a box list is the exception and must say why in a sibling why_box field (mail_poll: the remote-box reader); the node's grid_sync and branch_push rows drop their box lists now (grid_sync keeps mirror_towns; both jobs are idempotent per box) and crons.py audit flags a gated KNOWN job without why_box; write.py set on a dotted config key writes NESTED (measured 2b0ea2284: dotted keys landed flat) or refuses by name. Ceiling +10 -> 46. Ships in the SAME batch, same residue rule.
