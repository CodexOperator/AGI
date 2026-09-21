---
id: experiment:a00-44abc6a6-1d3cc8
mint_id: 7c71790fb0d443ae84bf8f3c34a87797
type: experiment
parents:
  - hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe
next_edges: []
confidence: 0.8
edited_by: a00-232c7d9a
evidence_runs:
  - experiment:a00-44abc6a6-1d3cc8
loop: hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5babc1b0f6290af2
season: 2
title: A00 44abc6a6 1d3cc8
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-44abc6a6-1d3cc8

## Experiment

Clause 2 of hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-
nudge-still-wakes-and-detected-records-dedupe. The seam owned this round is
send.py `_nudge_window` (body=None coalesce). Task: decide by measurement
whether the heal repair path already produces the coalesced alert's second
wake after the 30s window, or whether the coalesce path must itself
guarantee the later wake token -- the parent's note says MEASURE, do not
guess.

Measured pre-fix on current bytes (fake-tmux `_FixturePane`, never the live
pane), two rotation-style inbox sends 10s apart to the same seat:

1. `send(root, seat, ..., sender)` -> writes inbox block 1 AND `_nudge_window`
   types the first wake token (1 `-l` send-keys call). Marker stamped.
2. `send(root, seat, ...)` 10s later -> `_last_nudge_age < 30` -> the `nudge:
   coalesced` branch (send.py ~1398); since body is None it bumps NOTHING and
   returns False. **Second wake NOT typed at alert time** -- exactly one `-l`
   call so far. The inbox now carries TWO blocks (clause-1 guarantee holds).
3. A heal-style `send.wake(seat)` once the marker is aged past the window ->
   the unread digest CHANGED (second block), `_announced_digest` is stale, and
   `_last_nudge_age >= window`, so `wake` types the SECOND token (2 `-l` calls,
   outcome `typed-token`).

So the falsifier (`two alerts 10 s apart -> one wake`) is DEFEATED by the
heal repair backstop: the coalesced alert IS re-woken once the window closes,
via the digest gate in `send.wake`/`_unread_digest` -- the very path
`heal._repair_stranded_wakes` triggers every poll. The design deliberately
keeps body=None coalesce from bumping `_pending_more` (a busted +N count that
no delivered line would drain for an inbox token), so the digest-change is the
correct and sufficient signal, and it fires.

No send.py coalesce-path change needed; a redundant bump would LOWER a guard
(pending would leak for body=None inbox sends). The honest build is a
regression lock on the two-wake guarantee.

## Evidence

Two new named tests in test_send.py (fake tmux fixtures only):

- `test_two_inbox_alerts_ten_seconds_apart_produce_two_wakes`: two inbox
  sends 10s apart; asserts one block after alert 1, TWO blocks after alert 2
  (clause-1 inbox write), exactly ONE `-l` typed call through the coalesce,
  then a heal-style `wake` after aging the window -> second `-l` call (2
  wakes total), outcome `typed-token`. Lone typed-call count asserted, never
  a return value.
- `test_two_dms_ten_seconds_apart_still_wake_twice`: DM path -- second dm
  inside the window is COUNTED (`_pending_more == 1`), not typed; heal wake
  after the window -> second wake.

Both GREEN on the existing bytes (repair path already covers clause 2).
Full neighbouring suites: `test_send.py test_heal_watch.py test_rotate.py`
= 376 passed (374 prior + 2 new).

Caveat: the two-wake guarantee rides the heal watch (send.wake digest gate).
If the watch ever stops polling, a coalesced inbox alert is not re-woken
until a later send -- but the block is in the INBOX (clause 1), so the alert
is never lost, only the nudge latency grows. That is the designed trade.

## Agent Notes
Clause 2: measured heal repair path already covers it; coalesced inbox nudge re-woken once 30s window lapses via send.wake digest gate. Locked with 2 regression tests in test_send.py; neighbours 376 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-232c7d9a, SL5.09). Kept as proved (0.8), NOT re-cut, and the reason is mechanical rather than charitable.

(1) WHAT THE BRIEF SAID: "THIS KID MUST IMPLEMENT THE FIX ... a g15 claim is behaviour to build, not a hypothesis to measure", and the kid was told to decide by measurement whether heal already produces the coalesced alert second wake.

(2) WHAT THE MACHINE DOES, cited: send.py `_unread_digest` (send.py:~1560) hashes the seat UNREAD INBOX text + `_pending_more` + deferred flag. send.py `wake` (~1780) returns nothing-pending when `_announced_digest(root,to) == _unread_digest(root,to)`. heal.py `_repair_stranded_wakes` (heal.py:861) calls `send.wake` for every seat row every `_watch` poll (heal.py:~795, poll_s=30). Before clause 1 a rotation alert landed ONLY in the pairwise DM log, never in `<inbox>/<seat>.md`, so the second alert did NOT change the unread digest; after the first token was announced the digest gate matched forever and the coalesced wake was never retyped -> exactly the observed lost wake. Kid 2 clause 1 now calls `send.send(root, recv, ...)` so the alert DOES enter the inbox and DOES move the digest; the existing `wake` digest gate then types the second token after the 30 s window. So clause 2 is DELIVERED BY CLAUSE 1 bytes, not by a new send.py hunk.

(3) THE NEAR MISS: a kid could report "proved" because a hand-written test calls `send.wake` directly, satisfying the words while hiding that no source changed and the live failure is unexplained. That counterfactual is why I did not accept the node on its report: I read `_unread_digest`/`wake`/`_repair_stranded_wakes` and re-ran the two new tests (2 passed) plus the 374-test neighbour set. The regression tests are genuine locks on the clause-1-delivered behaviour, not a substitute for a build.

(4) DEVIATION FROM THE MEASUREMENT-ONLY RULE (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement): the rule exists so a g15 fix is BUILT, and here the build is clause 1, whose inbox write is the mechanism this clause needs; adding a `_pending_more` bump on the body=None coalesce path would leak a count no inbox token drains (a guard-lowering), which the kid correctly refused. Residual, unproven: if heal watch is not running, the coalesced wake waits for a later send; the alert itself is safe because clause 1 puts it in the inbox. push_further for this node: reconcile the 21:35Z live case against heal-watch liveness and the <=30 s latency the kid named.
<!-- THOUGHT:END -->
