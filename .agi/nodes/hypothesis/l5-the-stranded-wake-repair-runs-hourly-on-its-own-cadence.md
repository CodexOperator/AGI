---
id: hypothesis:l5-the-stranded-wake-repair-runs-hourly-on-its-own-cadence
mint_id: a492a95e16854ffc894b78709cc70c46
type: hypothesis
parents:
  - goal:g6.12
next_edges: []
edited_by: belam
scaffold_hash: c5114d4a233f48dc
season: 2
testable_claim: "OWNER 2026-09-17 14:1xZ (verbatim in doc:l5-owner-decisions): the L5 director was nudged constantly while its parents and kids were live. MEASURED: heal.py _watch calls _repair_stranded_wakes -> send.wake for every non-quiet row on every 30 s poll, and every kid dm moves the unread digest, so clause (1) one-token-per-state re-fires each poll. CLAIM: (1) the repair runs on its own cadence comms.wake_repair_every_s (send.py _COMMS_DEFAULTS, default 3600; heal._wake_repair_due, first pass after a watch start always due); (2) the reaper, after_join performer and round watch keep the 30 s poll untouched; (3) comms.nudge_stale_after_minutes 30 -> 60 so a standing marker re-fires hourly too; (4) one fixture test pins the cadence. Landed by the PRIME as a direct write on the owner order (deviation from the small-fix rule: 11 production lines, not test-only), tests heal/send 89 green, reaper unit restarted on the committed bytes."
thought_session: dissolve-legacy-2026-09-19
title: "L5: the stranded-wake repair runs hourly on its own cadence, never on the 30 s heal poll"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-stranded-wake-repair-runs-hourly-on-its-own-cadence

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
