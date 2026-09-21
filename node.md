---
id: hypothesis:l4-kill-switch-without-a-bus-is-a-named-skip
mint_id: 8ed18f36ec1f4c2a85e7be6540a98d32
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-crons-systemctl-seam-converges-from-cron
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 42fca51d79b0fce3
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-17: crons.py:556 — kill switch (crons_live:false / service disabled) + unit file present + no user bus SKIPS `disable --now` SILENTLY: the unit stays running with no line saying so. CLAIM: that path records `unit <name> present, no user bus: disable --now SKIPPED (unit may still be running)` — one named line, the file is still removed (or not — state which, with the reason: removing the file while the unit runs leaves a running unit systemd no longer knows; the review's expectation is a NAMED skip, choose and justify), daemon-reload skipped for the same reason with its own line. TESTS via the fake: kill switch + present + no bus → the named line, no FAILED; kill switch + present + bus → real disable. FALSIFIER: the silent path still exists (no line). CEILING: 1 kid. FILE SCOPE: crons.py (the kill-switch branch ONLY) + test_crons.py. SERIAL behind hypothesis:l4-crons-apply-records-one-state-line-when-nothing-changed. EXCLUDED: everything else."
title: crons.py kill switch with the unit present and no bus records a NAMED skip, never a silent one
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-kill-switch-without-a-bus-is-a-named-skip

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-17: crons.py:556 — kill switch (crons_live:false / service disabled) + unit file present + no user bus SKIPS `disable --now` SILENTLY: the unit stays running with no line saying so. CLAIM: that path records `unit <name> present, no user bus: disable --now SKIPPED (unit may still be running)` — one named line, the file is still removed (or not — state which, with the reason: removing the file while the unit runs leaves a running unit systemd no longer knows; the review's expectation is a NAMED skip, choose and justify), daemon-reload skipped for the same reason with its own line. TESTS via the fake: kill switch + present + no bus → the named line, no FAILED; kill switch + present + bus → real disable. FALSIFIER: the silent path still exists (no line). CEILING: 1 kid. FILE SCOPE: crons.py (the kill-switch branch ONLY) + test_crons.py. SERIAL behind hypothesis:l4-crons-apply-records-one-state-line-when-nothing-changed. EXCLUDED: everything else.
