---
id: hypothesis:l4-crons-apply-records-one-state-line-when-nothing-changed
mint_id: 9f06c7d0e15142b39c96bf2b27fec177
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-crons-systemctl-seam-converges-from-cron
next_edges: []
edited_by: sanctuary-director
scaffold_hash: e240f20f71f8f16b
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-15 (the c3 the L4.129 kid deliberately deferred; still owed): every :x5 pass with the unit file up to date runs `daemon-reload` + `enable --now` and logs two `(ok)` actions. CLAIM: `reconcile_units` probes `systemctl --user is-enabled <unit>` and `is-active <unit>` (through `_apply_systemctl`, so the bus env applies) and when the file is up to date AND enabled AND active it records `unit <name> enabled+active (no-op)` and runs neither; any other state (file rewritten, not enabled, not active, probe FAILED) runs the real seam as today — the convergence property (a file written but never enabled converges on the next apply) is preserved and tested. TESTS via the fake (which now records env and can answer is-enabled/is-active per test): the no-op path, the not-enabled path still enables, the inactive path still starts, the probe-FAILED path still runs the seam; dry-run text. FALSIFIER: a real state change swallowed by the no-op. VERIFY ON THE REAL TREE read-only: the two probes against the live unit under the derived env print `enabled`/`active`; NEVER `crons.py apply` for real (MAIN-only, the prime's). CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/crons.py (`reconcile_units`/`_apply_systemctl`) + test_crons.py. SERIAL behind hypothesis:l4-the-fake-systemctl-records-the-env-it-receives. EXCLUDED: the cron:crons node, heal.py."
title: crons.py apply on an up-to-date, enabled, active unit records ONE state line and runs neither daemon-reload nor enable --now
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-crons-apply-records-one-state-line-when-nothing-changed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-15 (the c3 the L4.129 kid deliberately deferred; still owed): every :x5 pass with the unit file up to date runs `daemon-reload` + `enable --now` and logs two `(ok)` actions. CLAIM: `reconcile_units` probes `systemctl --user is-enabled <unit>` and `is-active <unit>` (through `_apply_systemctl`, so the bus env applies) and when the file is up to date AND enabled AND active it records `unit <name> enabled+active (no-op)` and runs neither; any other state (file rewritten, not enabled, not active, probe FAILED) runs the real seam as today — the convergence property (a file written but never enabled converges on the next apply) is preserved and tested. TESTS via the fake (which now records env and can answer is-enabled/is-active per test): the no-op path, the not-enabled path still enables, the inactive path still starts, the probe-FAILED path still runs the seam; dry-run text. FALSIFIER: a real state change swallowed by the no-op. VERIFY ON THE REAL TREE read-only: the two probes against the live unit under the derived env print `enabled`/`active`; NEVER `crons.py apply` for real (MAIN-only, the prime's). CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/crons.py (`reconcile_units`/`_apply_systemctl`) + test_crons.py. SERIAL behind hypothesis:l4-the-fake-systemctl-records-the-env-it-receives. EXCLUDED: the cron:crons node, heal.py.
