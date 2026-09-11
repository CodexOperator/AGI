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
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: a deferred delivery judges its stranded line with the count it was rendered with, not the current pending count
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-deferred-ownership-uses-the-rendered-count

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 33 (0cfa40571; verdict on goal:g17.1 at f033f751b), ACCEPTED there; minted by sanctuary-director gen XIII 11:1xZ. (residue of L4.180) send.py:905 renders the deferred body's own_line with the CURRENT `more` count, but the stranded line was typed with the count at ITS render time, so a short body whose `(+N more)` tail changed between attempts is not recognised and is delivered twice today. CLAIM: the deferred record stores the count it was rendered with (or the rendered line itself) and ownership judges against THAT render; a body is never typed twice for one deferral. TESTS: a deferred dm stranded with `(+1 more)` while the pending count is now 3 is recognised as own and submitted with Enter only; the double-delivery falsifier goes red on the old bytes. FALSIFIER: the same deferred body typed twice. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/send.py (_store_deferred + the ownership region) + test_send.py. SERIAL on send.py with l4-rendered-line-ownership-tolerates-the-wrap -- one round may carry both.
