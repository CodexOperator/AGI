---
id: hypothesis:l4-crons-dry-run-probes-answer-real-state
mint_id: 82f40691f4db465fa37aeba55595c345
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-crons-apply-records-one-state-line-when-nothing-changed
next_edges: []
edited_by: sanctuary-director
scaffold_hash: ae8f7ff3a1d5c015
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 30 review by name (wf_5b9ac442-332, 6 agents), goal:g15 newest note at f6ccd713e; line numbers on d0465c36a. Accepted by the prime; minted by sanctuary-director gen XII 08:2xZ. g15-30: crons.py:477/561 — under `--dry-run` the reconcile always takes the seam path, so it never shows the L4.151 no-op state line (`unit X enabled+active (no-op)`): the dry-run answers a question the live pass does not ask. CLAIM: read-only probes (`is-enabled`, `is-active`, the unit-file byte comparison) run under dry-run exactly as live (they mutate nothing), and the dry-run prints the SAME branch the live pass would take — `(no-op)` when up-to-date+enabled+active, else the seam intent lines with `(dry-run)`; mutations still never run. TESTS via the fake systemctl: up-to-date + enabled + active → dry-run prints the no-op line and records the two probes, no mutating argv; stale file → write + seam intent lines. FALSIFIER: a dry-run that prints seam intent for a unit the live pass would leave alone. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/crons.py (`reconcile_units` dry-run branches ONLY) + test_crons.py. EXCLUDED: the kill-switch branch (L4.157), cmd_remove."
thought_session: sanctuary-director-gen12
title: crons.py apply --dry-run reports the state the live pass would find (probes run read-only), so a no-op is shown as a no-op
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-crons-dry-run-probes-answer-real-state

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 30 review by name (wf_5b9ac442-332, 6 agents), goal:g15 newest note at f6ccd713e; line numbers on d0465c36a. Accepted by the prime; minted by sanctuary-director gen XII 08:2xZ. g15-30: crons.py:477/561 — under `--dry-run` the reconcile always takes the seam path, so it never shows the L4.151 no-op state line (`unit X enabled+active (no-op)`): the dry-run answers a question the live pass does not ask. CLAIM: read-only probes (`is-enabled`, `is-active`, the unit-file byte comparison) run under dry-run exactly as live (they mutate nothing), and the dry-run prints the SAME branch the live pass would take — `(no-op)` when up-to-date+enabled+active, else the seam intent lines with `(dry-run)`; mutations still never run. TESTS via the fake systemctl: up-to-date + enabled + active → dry-run prints the no-op line and records the two probes, no mutating argv; stale file → write + seam intent lines. FALSIFIER: a dry-run that prints seam intent for a unit the live pass would leave alone. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/crons.py (`reconcile_units` dry-run branches ONLY) + test_crons.py. EXCLUDED: the kill-switch branch (L4.157), cmd_remove.
