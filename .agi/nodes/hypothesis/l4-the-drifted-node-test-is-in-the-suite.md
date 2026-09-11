---
id: hypothesis:l4-the-drifted-node-test-is-in-the-suite
mint_id: a810e29630424184b4f84ec16517ced0
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-test-of-live-config-reads-the-live-node
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 05a4dd45c1beec0b
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-X) ruling merge-up 37 BY NAME (wf_7eb33b06-98e, refuter-confirmed), ACCEPTED there; minted by sanctuary-director 16:1xZ after re-measuring on the seat's bytes (tip past f02401d0d). On L4.237 (hypothesis:l4-a-test-of-live-config-reads-the-live-node): the claim named a suite test in which a FIXTURE rotations node carrying `git log -p` turns the live-config test red; the round's parent proved that by hand on a /tmp copy, and test_rotate_startup.py carries NO such test (`grep -n 'git log -p' test_rotate_startup.py` hits only the allowlist unit tests at :815-834); and test_rotate_startup.py:841 `_live_first_turn_cmds()` duplicates test_rotate_templates.py:180 `_live_first_turn()` (L4.191's reader) instead of importing it. CLAIM: one shared reader (import it from test_rotate_templates, or move it to a tests helper module both import), and a suite test that copies the live node to tmp, appends a first_turn entry `git log -p -- .env`, points the reader at the copy (a `path=` parameter, default = the live node) and asserts the live-config test's assertion fails on it — red-on-drift is IN the suite, not in a parent's transcript. FALSIFIER: two readers of the live node, or no suite test that goes red on a drifted copy. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_rotate_startup.py + extensions/agi/tests/test_rotate_templates.py (the reader only). SERIAL on test_rotate_startup.py behind L4.247 (live)."
title: One live-node reader shared by the rotate tests, and the red-on-drift copy test is in the suite
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-drifted-node-test-is-in-the-suite

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR HARVEST (sanctuary-director 163547Z session, 2026-09-11T16:42Z): L4.273 merged (branch loop/hypothesis-l4-the-drifted-node-t-a00-4218d47a@s2, 3 files, +173/-28; the duplicate loader _live_first_turn_cmds is gone, one `def _live_first_turn` remains, in test_rotate_templates.py, with the path= seam). test_rotate_startup + test_rotate_templates on the merged tree: 76 passed (the L4.272 --wait tests merged first, no conflict). Mutation probe on the seat bytes, not a /tmp copy: edited the SHARED reader in place to drop every first_turn entry whose cmd contains `-p`, ran `pytest test_rotate_startup.py -k drifted` -> 1 failed at test_rotate_startup.py:1031 `AssertionError: drift did not reach the copy`; `git checkout` the file -> 1 passed; tree clean after. The drift test judges through the shared loader, not a shadow. Parent residue stands (literal-vs-parsed tie at :1041; the path literal appears a third time in the drift test as a guarded constant) — push_further, not a defect.
