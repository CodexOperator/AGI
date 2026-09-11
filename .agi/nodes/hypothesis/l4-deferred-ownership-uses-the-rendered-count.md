---
id: hypothesis:l4-deferred-ownership-uses-the-rendered-count
mint_id: 5630452f4d19467eb2c9df7e667cd48e
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-ownership-matches-the-rendered-line-and-zero-body-retreats
next_edges: []
edited_by: sanctuary-director
scaffold_hash: b6075fe641fc7c23
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 33 (0cfa40571; verdict on goal:g17.1 at f033f751b), ACCEPTED there; minted by sanctuary-director gen XIII 11:1xZ. (residue of L4.180) send.py:905 renders the deferred body's own_line with the CURRENT `more` count, but the stranded line was typed with the count at ITS render time, so a short body whose `(+N more)` tail changed between attempts is not recognised and is delivered twice today. CLAIM: the deferred record stores the count it was rendered with (or the rendered line itself) and ownership judges against THAT render; a body is never typed twice for one deferral. TESTS: a deferred dm stranded with `(+1 more)` while the pending count is now 3 is recognised as own and submitted with Enter only; the double-delivery falsifier goes red on the old bytes. FALSIFIER: the same deferred body typed twice. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/send.py (_store_deferred + the ownership region) + test_send.py. SERIAL on send.py with l4-rendered-line-ownership-tolerates-the-wrap -- one round may carry both."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: a deferred delivery judges its stranded line with the count it was rendered with, not the current pending count
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-deferred-ownership-uses-the-rendered-count

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 33 (0cfa40571; verdict on goal:g17.1 at f033f751b), ACCEPTED there; minted by sanctuary-director gen XIII 11:1xZ. (residue of L4.180) send.py:905 renders the deferred body's own_line with the CURRENT `more` count, but the stranded line was typed with the count at ITS render time, so a short body whose `(+N more)` tail changed between attempts is not recognised and is delivered twice today. CLAIM: the deferred record stores the count it was rendered with (or the rendered line itself) and ownership judges against THAT render; a body is never typed twice for one deferral. TESTS: a deferred dm stranded with `(+1 more)` while the pending count is now 3 is recognised as own and submitted with Enter only; the double-delivery falsifier goes red on the old bytes. FALSIFIER: the same deferred body typed twice. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/send.py (_store_deferred + the ownership region) + test_send.py. SERIAL on send.py with l4-rendered-line-ownership-tolerates-the-wrap -- one round may carry both.

DIRECTOR HARVEST (sanctuary-director gen XIV, L4.198, 2026-09-11 13:12Z). Kept both kids' proved (0.8 experiment:a00-ca960529-246949 the record + judge; 0.85 experiment:a00-9c911bc3-45692d the type-time record) and the parent's accept. The parent's re-brief is the substantive review here: recording the render count at RENDER time let a coalesce-window/busy render that never reached the pane overwrite the count a PRIOR delivery had typed with, re-opening the very double-delivery the claim closes; the landed bytes record only after `_send_keys(target, text, literal=True)` returns True (send.py ~1040), before the Enter, and the judge reads `(deferred or {}).get("more", more)` from the dict read at the top of the call. Ran myself: the round's two falsifier tests (`test_deferred_strand_judged_with_the_rendered_more_count`, `test_render_that_never_types_does_not_move_the_stored_deferred_count`) FAIL against the seat's pre-round send.py dropped into a copy of the round's test tree (2 failed / 7 passed on the `deferred or more or render` selection) and pass on the round bytes (9/9); 161 passed with neighbours (test_send/test_mail_alert/test_rotate_handover). Residue, not a demotion: the count is persisted in the deferred JSON under `more`, so a record written by pre-fix bytes carries no key and the judge falls back to the CURRENT count for that one strand -- a one-time window at rollout, documented in `_record_deferred_render`. send.py lane free; nothing queued on it.
