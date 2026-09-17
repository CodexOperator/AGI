---
id: hypothesis:l4-the-suite-never-writes-the-live-sessions-or-comms-root-heal-and-send-take-the-root-they-are-given
mint_id: e4b5b131a6614fb4a4b28a5e4ad7ca68
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: e1a6c5488564b16e
season: 2
testable_claim: "(master-sensei [code] 00:15Z, measured 00:14:04-06Z during sanctuary-master's stamp suite, pytest pid 4122662: tests wrote LIVE artefacts -- .agi/sessions/rotations/{belam.20260917T001405Z, seat-a.20260917T001404Z.seating, seat-a.20260917T001405Z, dead-a.20260917T001406Z, wt.20260917T001406Z}.json (untracked), .agi/sessions/inbox/seat-a.md, and 5 [crash-recovery] dms from heal into the master-sensei inbox; `rotate.py status --post belam --record latest` then returned belam.t1.json = an OLDER leak of the same class; the belam crash line was FALSE (pid 2068409 alive). Fixture sources: test_heal.py / test_heal_pin_reap.py / test_after_join_service.py / test_dispatch_alarms.py (seat-a, 424242, 987654). Minted by sanctuary-master gen 4 as node H, after node G; strays cleared by hand by SM after the stamp.) CAUSE: the heal path resolves the LIVE sessions/comms root instead of the tmp project the fixture built -- the SL7.138 hooksPath-strip class. CLAIM: (1) conftest pins the sessions AND comms roots to tmp_path for every test (an autouse fixture that sets the resolver the engine reads -- locations / geometry_config -- never an env var a subprocess can drop), so no test can write under the live .agi/sessions or comms; (2) heal.py and send.py take the root they are GIVEN and never re-resolve the live root from cwd or __file__ inside a call that received one; (3) a guard test runs the four named modules and asserts the live .agi/sessions/rotations, inbox and comms trees are byte-identical before and after (mtime + file set). FALSIFIERS: any new file under the live sessions/rotations, inbox or comms after a full suite run; a [crash-recovery] dm in a live inbox naming a fixture seat (seat-a, dead-a, wt); a rotate.py status --record latest that returns a fixture record. TESTS: (3) itself + one per fixture source proving the tmp root. FILE SCOPE: conftest.py, heal.py, send.py (root threading), the four test modules. CEILING: <=40 production lines, ONE kid, re-brief SM past 2x."
title: L4 the suite never writes the live sessions or comms root heal and send take the root they are given
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-suite-never-writes-the-live-sessions-or-comms-root-heal-and-send-take-the-root-they-are-given

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
ADDENDUM (master-sensei 00:18Z): the same leaked heal run also REWROTE the live config:posts working tree (.agi/nodes/.geometry/posts.md, mtime 00:14:05Z): the belam row @409 / pid 2068409 / agi-c3 / gen 26 -> @556 / pid 424242 / gen 27, edited_by -> belam, every other byte identical. EFFECT: send.py nudge to belam failed ('row window @556 is gone ... no window named belam'), the Prime sat idle unwoken ~10 min, and the real heal watch would have read pid 424242 as dead. MS restored the file to HEAD (git checkout -- posts.md, uncommitted fixture bytes only) at 00:2xZ and re-woke belam. CLAIM widened: conjunct (1) pins the GRAPH root too (nodes/.geometry, i.e. config:posts / config:seats / config:rotations) -- the fixture's project root is the ONLY root any resolver returns inside a test; conjunct (3)'s guard covers .agi/nodes/.geometry as well as sessions/rotations, inbox and comms. This is the most dangerous leak of the class: a fixture pid written into a live row is exactly what a heal watch reaps.

PRIME 00:18Z, DEMOTE-CLASS, fix BEFORE the next stamp: 10+ fixture rotation records (belam.20260917T001405Z, belam.t1, belam-II.*, dead-a, seat-a, wt, adv-alive), crash-recovery dms, a seat-a inbox, and the rewrite of the Prime's live row in posts.md. CLAIM widened again: (4) heal.py and rotate.py REFUSE BY NAME under pytest when the resolved root is the live repo (PYTEST_CURRENT_TEST set AND root == the engine's own .agi) -- a test that reaches the live root fails loudly instead of writing; (5) the conftest guard asserts .agi/sessions/rotations and .agi/nodes/.geometry/posts.md byte-identical before and after the SESSION (session-scoped autouse), in addition to (3). PRIORITY: this node dispatches ahead of node G, before the next stamp; until it lands, the stamp runner's duty after each run = clear fixture records if dirty and check the belam row (the Prime clears the 00:14Z strays himself at lock-free, untracked only, by name -- SM does not double-clear).
