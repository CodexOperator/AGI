---
id: hypothesis:l4-quiet-posts-a-quiet-settings-token-on-a-row-writes-the-dm-but-types-no-nudge-never-refires-a-stale-marker-and-wake-repair-skips-the-row
mint_id: 3f93148b81c143718e8f23d8afbee68f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 68c504b933f33808
season: 2
testable_claim: "(sanctuary-master gen 5, 03:2xZ; OWNER ruling (B) 03:1xZ via belam gen 27, verbatim in doc:l4-owner-decisions: QUIET POSTS -- the NEXT named round after SM.80 lands, before SM.70; the Prime then sets the token on thought-master + director-thought, whose rotation alerts are already silent via config:rotations.) CLAIM: (1) a `settings` cell on a config:posts row carrying the token `quiet` (SETTINGS_ALIASES gains \"quiet\": {\"quiet\": True}; tokens compose with `ultracode`, so the cell is a space-separated token list or a JSON object and rotate._normalize_settings reads both the same way) makes `send.py send <post>` WRITE the dm/inbox exactly as today and exit 0, but type NO tmux nudge (no send-keys, no copy-mode cancel, no pending/deferred nudge file) and NEVER re-fire a stale marker for that row (the stale-marker re-fire path is skipped by name for a quiet row, not suppressed by a marker write); (2) heal.py `_repair_stranded_wakes` (the watch pass's seat-wake repair, and send.wake it calls) SKIPS a quiet row by name -- no typed space, no Enter, no capture-pane of that pane; (3) `send.py status <post>` (or `whois`) prints `quiet` for such a row so an operator can see why a nudge never came; (4) a NON-quiet row keeps every nudge/re-fire/wake behavior byte-for-byte (the falsifier: run the existing nudge + wake tests unchanged). FALSIFIERS: a quiet row that receives a send-keys of any kind; a stale marker on a quiet row that re-fires; a wake-repair pass that touches a quiet row's pane; any change to a non-quiet row's behavior; a settings cell 'ultracode quiet' that stops enabling ultracode. TESTS: one per conjunct (send quiet -> inbox written, tmux fake untouched; stale marker on a quiet row -> no re-fire; wake repair skips; status shows quiet; a non-quiet row still nudges) + the existing nudge/wake suites unchanged. FILE SCOPE: bin/send.py (nudge path + status), bin/heal.py (_repair_stranded_wakes), bin/rotate.py (SETTINGS_ALIASES + _normalize_settings token list), tests. CEILING: <=35 production lines, ONE kid, re-brief SM past 2x. Every pytest with --basetemp under /tmp. The config half (setting quiet on the two rows) is the Prime's write after landing, never the kid's."
title: L4 quiet posts a quiet settings token on a row writes the dm but types no nudge never refires a stale marker and wake repair skips the row
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-quiet-posts-a-quiet-settings-token-on-a-row-writes-the-dm-but-types-no-nudge-never-refires-a-stale-marker-and-wake-repair-skips-the-row

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
