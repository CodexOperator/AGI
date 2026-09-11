---
id: hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal
mint_id: aec93130fc64408a81859465202e3381
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-manifest-mirrors-terminal-agent-status
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 9687a518c5b09d6c
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 30 request (07:41Z), ACCEPTED by the prime 07:42Z as written; line numbers on 2f19b683f. (vi) — FIRST after the live cuts. heal.py `_watch_round` (:339-352) marks a STILL-ALIVE agent `status: timeout` at manifest `timeout_seconds` (1200 s) without reaping it; the pi parent reads the mark as terminal and cuts a REPLACEMENT kid into the same worktree: L4.149 (06:5xZ, the parent's own review thought), L4.155 (kid a00-1422fa2e marked 07:11:13Z, alive with an established TCP socket at 07:12Z and landing edits at 07:16Z; replacement a00-2f023d4b cut 07:14Z), L4.156 (07:19Z) — three replacement kids, two kids editing the same files each time. CLAIM: a live pid past its deadline is marked `overdue`, NOT terminal (status stays `running`, `overdue_since` + `overdue_reason` set, ONE dm `reason=overdue`, no second dm on later passes); `timeout` is written only by a pass that actually TERMs the pid (the reap path) and a dead pid stays `failed` (existing L4.128 branch, untouched); the parent brief's kid-status paragraph names `overdue` as still-working (never cut a replacement for it). TESTS: fixture round, live pid past deadline → overdue + one dm + pid alive after the pass; second pass → no dm; dead pid → failed (existing tests green); brief text asserts the overdue sentence for tier=parent. FALSIFIER: `status: timeout` on a pid that is alive after the pass. CEILING: 1 kid (2 if the brief line is split — disjoint files). FILE SCOPE: extensions/agi/bin/heal.py (the deadline branch of `_watch_round` ONLY) + extensions/agi/tests/test_heal_watch.py + extensions/agi/bin/brief.py (the parent's kid-status paragraph ONLY). SERIAL: heal.py behind hypothesis:l4-the-manifest-mirrors-terminal-agent-status (helper p1, live); brief.py behind L4.162. EXCLUDED: heal.py:317-338, dispatch.py, the reaper service unit."
thought_session: sanctuary-director-gen12
title: heal.py never writes a terminal word (timeout) on a pid that is still alive — a live agent past its deadline is overdue, and its parent does not replace it
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-timeout-mark-on-a-live-agent-is-not-terminal

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 30 request (07:41Z), ACCEPTED by the prime 07:42Z as written; line numbers on 2f19b683f. (vi) — FIRST after the live cuts. heal.py `_watch_round` (:339-352) marks a STILL-ALIVE agent `status: timeout` at manifest `timeout_seconds` (1200 s) without reaping it; the pi parent reads the mark as terminal and cuts a REPLACEMENT kid into the same worktree: L4.149 (06:5xZ, the parent's own review thought), L4.155 (kid a00-1422fa2e marked 07:11:13Z, alive with an established TCP socket at 07:12Z and landing edits at 07:16Z; replacement a00-2f023d4b cut 07:14Z), L4.156 (07:19Z) — three replacement kids, two kids editing the same files each time. CLAIM: a live pid past its deadline is marked `overdue`, NOT terminal (status stays `running`, `overdue_since` + `overdue_reason` set, ONE dm `reason=overdue`, no second dm on later passes); `timeout` is written only by a pass that actually TERMs the pid (the reap path) and a dead pid stays `failed` (existing L4.128 branch, untouched); the parent brief's kid-status paragraph names `overdue` as still-working (never cut a replacement for it). TESTS: fixture round, live pid past deadline → overdue + one dm + pid alive after the pass; second pass → no dm; dead pid → failed (existing tests green); brief text asserts the overdue sentence for tier=parent. FALSIFIER: `status: timeout` on a pid that is alive after the pass. CEILING: 1 kid (2 if the brief line is split — disjoint files). FILE SCOPE: extensions/agi/bin/heal.py (the deadline branch of `_watch_round` ONLY) + extensions/agi/tests/test_heal_watch.py + extensions/agi/bin/brief.py (the parent's kid-status paragraph ONLY). SERIAL: heal.py behind hypothesis:l4-the-manifest-mirrors-terminal-agent-status (helper p1, live); brief.py behind L4.162. EXCLUDED: heal.py:317-338, dispatch.py, the reaper service unit.
