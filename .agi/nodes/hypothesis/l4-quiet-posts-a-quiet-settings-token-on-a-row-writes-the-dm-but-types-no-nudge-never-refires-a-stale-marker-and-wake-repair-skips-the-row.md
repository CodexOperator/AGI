---
id: hypothesis:l4-quiet-posts-a-quiet-settings-token-on-a-row-writes-the-dm-but-types-no-nudge-never-refires-a-stale-marker-and-wake-repair-skips-the-row
mint_id: 3f93148b81c143718e8f23d8afbee68f
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 68c504b933f33808
season: 2
testable_claim: "(sanctuary-master gen 5, 03:2xZ; OWNER ruling (B) 03:1xZ via belam gen 27, verbatim in doc:l4-owner-decisions: QUIET POSTS -- the NEXT named round after SM.80 lands, before SM.70; the Prime then sets the token on thought-master + director-thought, whose rotation alerts are already silent via config:rotations.) CLAIM: (1) a `settings` cell on a config:posts row carrying the token `quiet` (SETTINGS_ALIASES gains \"quiet\": {\"quiet\": True}; tokens compose with `ultracode`, so the cell is a space-separated token list or a JSON object and rotate._normalize_settings reads both the same way) makes `send.py send <post>` WRITE the dm/inbox exactly as today and exit 0, but type NO tmux nudge (no send-keys, no copy-mode cancel, no pending/deferred nudge file) and NEVER re-fire a stale marker for that row (the stale-marker re-fire path is skipped by name for a quiet row, not suppressed by a marker write); (2) heal.py `_repair_stranded_wakes` (the watch pass's seat-wake repair, and send.wake it calls) SKIPS a quiet row by name -- no typed space, no Enter, no capture-pane of that pane; (3) `send.py status <post>` (or `whois`) prints `quiet` for such a row so an operator can see why a nudge never came; (4) a NON-quiet row keeps every nudge/re-fire/wake behavior byte-for-byte (the falsifier: run the existing nudge + wake tests unchanged). FALSIFIERS: a quiet row that receives a send-keys of any kind; a stale marker on a quiet row that re-fires; a wake-repair pass that touches a quiet row's pane; any change to a non-quiet row's behavior; a settings cell 'ultracode quiet' that stops enabling ultracode. TESTS: one per conjunct (send quiet -> inbox written, tmux fake untouched; stale marker on a quiet row -> no re-fire; wake repair skips; status shows quiet; a non-quiet row still nudges) + the existing nudge/wake suites unchanged. FILE SCOPE: bin/send.py (nudge path + status), bin/heal.py (_repair_stranded_wakes), bin/rotate.py (SETTINGS_ALIASES + _normalize_settings token list), tests. CEILING: <=35 production lines, ONE kid, re-brief SM past 2x. Every pytest with --basetemp under /tmp. The config half (setting quiet on the two rows) is the Prime's write after landing, never the kid's."
thought_session: dissolve-legacy-2026-09-19
title: L4 quiet posts a quiet settings token on a row writes the dm but types no nudge never refires a stale marker and wake repair skips the row
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-quiet-posts-a-quiet-settings-token-on-a-row-writes-the-dm-but-types-no-nudge-never-refires-a-stale-marker-and-wake-repair-skips-the-row

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM REVIEW (sanctuary-master gen 5, 05:1xZ, by name, PRE-HARVEST -- the director rotated at its line before merging): ACCEPT inconclusive_lean_proved:85 on the loop branch tip c89c2563f (season2/loops/hypothesis-l4-quiet-posts-a-quie-a00-f0ed4b5b; 2 kids accepted). Diff read: rotate.SETTINGS_ALIASES gains quiet and _normalize_settings merges a token list (quiet composes with ultracode); send._row_is_quiet reads the row's settings; _nudge_window returns before typing for a quiet row (the stale-marker re-fire lives there, so it is skipped by name); send.wake prints 'wake <post>: quiet-skip' and returns False; heal._repair_stranded_wakes continues past a quiet row; status prints ' quiet' after the post name; the dm/inbox write is untouched (`if nudge and not _row_is_quiet`). 52 insertions / 11 deletions across send.py 28, rotate.py 29, heal.py 6 against the 35 ceiling -- ~1.2x on insertions-only after the docstrings, disclose at harvest. Tests: test_send_quiet.py (7: quiet writes inbox + no nudge, wake never re-fires a stale marker, wake-repair skips, status shows quiet only for a quiet row, a NON-quiet row still nudges, dm to a quiet row types nothing, normalize composes quiet+ultracode) + the existing send/heal/rotate suites: 663 passed / 0 failed in a throwaway detached worktree of the tip with a /tmp basetemp (removed after). merge-tree gate of c89c2563f on HEAD: clean. SUCCESSOR / director: merge --no-ff on the post branch, harvest line, merge-up by SHA; then the Prime writes `settings: quiet` (composing with any ultracode) on thought-master + director-thought -- the config half is his, never the kid's.
