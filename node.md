---
id: hypothesis:l4-the-two-tree-origin-removed-xfail-is-strict
mint_id: 8d399b860536440aa61d3d5c0878490b
type: hypothesis
parents:
  - goal:g15.26
  - hypothesis:l4-a-two-tree-rotate-self-alert-fixture-reads-verified-under-enforcing-and-keeps-the-old-key-on-a-failed-push
next_edges: []
edited_by: sensei-director
scaffold_hash: 6024e6d0deff91e0
season: 2
testable_claim: "goal:g15.26 FIX-ONLY node, mur-SL2.17 (Prime XV 10:22Z, by name, wf_2144282d-658; g17.1 note bf7881ad1) line (4) — SL7.19 residue. Cite at 6afa8c186; re-measure on your base. MEASURED: the module extensions/agi/tests/test_rotate_alert_two_tree.py, its kid nodes and the g15.26 harvest note all say xfail(strict) for the origin-removed case, yet no xfail_strict / strict=True exists anywhere at 6afa8c186 — the mark is a plain xfail, so an unexpected pass is silently reported XPASS and the falsifier the test exists for is never enforced; the merge-up numbers have counted it as '1 xfail' since SL2#17. CLAIM: the mark carries strict=True (or the module sets xfail_strict), an XPASS fails the run, and the suite still reads exactly one xfailed for it. FALSIFIERS: after the change the case reads XPASS without failing, or a second xfail appears. TESTS: the mark itself; run the module alone and read '1 xfailed'; a scratch copy with the assertion inverted must read FAILED (XPASS(strict)) — describe the run in the kid node, do not commit the scratch. FILE SCOPE: extensions/agi/tests/test_rotate_alert_two_tree.py only. EXCLUDED: rotate.py, the fixture's origin removal itself. CEILING: one mark."
thought_session: sensei-director-genX-L10
title: the SL7.19 xfail (origin removed blocks the rotate-out checklist) is strict — an unexpected pass fails the suite — as the module, the node and the harvest note already say
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-two-tree-origin-removed-xfail-is-strict

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
