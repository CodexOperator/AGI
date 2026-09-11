---
id: hypothesis:l4-the-fake-systemctl-records-the-env-it-receives
mint_id: cafbd0947b1c460a97458ed986416db1
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-crons-systemctl-seam-converges-from-cron
next_edges: []
edited_by: sanctuary-director
scaffold_hash: e6dcf974659c1343
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-14: `test_crons.py`'s `fake_systemctl` records argv only; deleting `env=merged` at crons.py:485-486 (the L4.129 bus-env merge) leaves 62/62 green — the mutation survives, so the fix is unprotected. CLAIM: the fake records the environment it was invoked with (XDG_RUNTIME_DIR, DBUS_SESSION_BUS_ADDRESS and whether they came from the caller or the fallback), the L4.129 tests assert on it, and the mutation (delete `env=merged`) turns at least one test RED (paste the mutation run, then restore byte-identical). FALSIFIER: the mutation still green. TESTS ONLY — crons.py byte-identical. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_crons.py ONLY. Cut FIRST in the crons queue (g15-15 and g15-17 build on the recorded env). EXCLUDED: crons.py edits."
title: The test fake for systemctl records the ENV it receives so the bus-env merge cannot be deleted unnoticed
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-fake-systemctl-records-the-env-it-receives

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-14: `test_crons.py`'s `fake_systemctl` records argv only; deleting `env=merged` at crons.py:485-486 (the L4.129 bus-env merge) leaves 62/62 green — the mutation survives, so the fix is unprotected. CLAIM: the fake records the environment it was invoked with (XDG_RUNTIME_DIR, DBUS_SESSION_BUS_ADDRESS and whether they came from the caller or the fallback), the L4.129 tests assert on it, and the mutation (delete `env=merged`) turns at least one test RED (paste the mutation run, then restore byte-identical). FALSIFIER: the mutation still green. TESTS ONLY — crons.py byte-identical. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_crons.py ONLY. Cut FIRST in the crons queue (g15-15 and g15-17 build on the recorded env). EXCLUDED: crons.py edits.
