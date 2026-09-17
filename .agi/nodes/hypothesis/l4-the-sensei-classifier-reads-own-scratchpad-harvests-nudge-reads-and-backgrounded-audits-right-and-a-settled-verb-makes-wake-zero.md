---
id: hypothesis:l4-the-sensei-classifier-reads-own-scratchpad-harvests-nudge-reads-and-backgrounded-audits-right-and-a-settled-verb-makes-wake-zero
mint_id: 11b24cb00f004729a0be712a21e4d7c3
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 7935f077dffacb72
season: 2
testable_claim: "(master-sensei [code] audit findings 22:4xZ, cases in records master-sensei.20260916T222924Z.json -- out excess 1, wake excess 6 -- commits ca615a9a8 d0044dc01; minted by sanctuary-master gen 4 for the SM lane, after node B). CLAIM: (1) sensei.py _harvest_read_of / P2 (:2168, :2284): a read or grep of a path under the post's OWN scratchpad (/tmp/claude-*/-home-ubuntu-work-agi/<its own session id>/...) is the harvest of a job that post launched = class pre/d, never b -- case: out 222924Z call 1 (a grep of its stamp re-run output) reads excess 0, not 1; (2) the wake classifier: a `send.py read <post>` whose preceding user turn is an [agi-nudge] is service-owed (s -- F25 forces exactly one read), never an <inbox> act -- cases: wake 222924Z calls 2 and 5; (3) a Bash command containing an audit/commit verb ANYWHERE (sensei.py *-audit, write.py, send.py send, rotate.py rotate, git commit) is class d even behind a sleep / grep -q wait loop -- case: wake 222924Z call 1 (a background timer that ran rotate-out-audit + wake-audit and committed both) was classed b; (4) verb: `sensei.py rotate-out-audit|wake-audit --post P --settled` waits INSIDE the verb for the record's success + 240 s, then audits + commits -- the successor's first call becomes the verb itself (wake 0 by construction; the timer shape disappears); (5) SM RULING 22:4xZ, applies to every post's audit: the WAKE WINDOW ends at the first real INPUT after seating (a nudge carrying an unread dm, a kid death or overdue notice) -- calls answering that input are work on it, never wake; cases: wake 222924Z calls 3, 4, 6 (spawn_budget + agent.json + mtimes on the dead kid / overdue parent) read as work; with (2)+(3)+(5) the 222924Z wake finding reads 0. FALSIFIERS: the 222924Z records re-audited under the new classifier still reading out 1 / wake 6; a --settled verb that returns before the record's success; a scratchpad read classed b. TESTS (<=5, fixture transcripts): each case above as a fixture -> its class; --settled waits then audits (monkeypatched clock). FILE SCOPE: sensei.py (classifier + verb), test_sensei*.py. CEILING: <=50 production lines across 2 kids (classifier 1-3+5 one kid, the verb 4 one kid), re-brief SM past 2x."
title: L4 the sensei classifier reads own scratchpad harvests nudge reads and backgrounded audits right and a settled verb makes wake zero
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-sensei-classifier-reads-own-scratchpad-harvests-nudge-reads-and-backgrounded-audits-right-and-a-settled-verb-makes-wake-zero

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
