---
id: experiment:a00-b13be0c7-c5cab1
mint_id: 9b43db66158a4e83ac603e13fda12b2b
type: experiment
parents:
  - hypothesis:l4-the-sensei-classifier-reads-own-scratchpad-harvests-nudge-reads-and-backgrounded-audits-right-and-a-settled-verb-makes-wake-zero
next_edges: []
confidence: 0.8
edited_by: a00-b13be0c7
evidence_runs:
  - experiment:a00-b13be0c7-c5cab1
line_ceiling: 50
loop: hypothesis:l4-the-sensei-classifier-reads-own-scratchpad-harvests-nudge-reads-and-backgrounded-audits-right-and-a-settled-verb-makes-wake-zero@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 34
profile: balanced
role: kid
scaffold_hash: 69dc0f6c019270d3
season: 2
title: rotate.py prepare/rotate-self check-2 scopes dirty-tree to own paths and never re-asks --stops on a retry
town: core
verdict: proved
---
# experiment:a00-b13be0c7-c5cab1

SM.84 ITEM 7 — rotate.py prepare gate / rotate-self check-2 dirty-tree scoping
to the post's own paths, and no --stops re-ask on a retry after a refused
rotation. (A separate kid owns ITEM 6, sensei.py out-window — not touched.)

## What the measurements said

Two live measurements this round, both a false dirty-tree REFUSAL on FOREIGN
dirt in MAIN:

- master-sensei 00:19Z (prepare gate): refused on cron-owned comms + rotation
  records, other posts' cards, HANDOFF.md, nodes the post never touched; then
  a retry treated the where-it-stops slot as STALE and demanded --stops.
- belam 00:31Z (rotate-self check 2): refused three times on three foreign
  paths, including another post's UNTRACKED node draft in shared MAIN.

## Root cause found (measured, not assumed)

g15.25/SM.40 had already made foreign dirt NON-blocking on a MAIN post — BUT
only when the merge touch-set (`git diff --name-only HEAD...origin/<sb>`) was
MEASURABLE. On a MAIN post whose `origin/<sb>` ref is absent locally (the gate
runs NO fetch, so a MAIN checkout that has never fetched its retire target
reads unmeasurable), it fell back to blocking on EVERY dirty path. Proven by
probe: with foreign tracked paths and an unmeasured touch-set, prepare rc=3
`[BLOCK] dirty tree: HANDOFF.md, ... (touch-set unmeasured)`; with the
touch-set measurable-empty the same paths passed rc=0 as `foreign dirt`.

Clamp C: rotate-self writes the where-it-stops slot + commits `rotate-out gen
N->N+1` (stop_commit) BEFORE the prepare checklist. A checklist REFUSAL leaves
that commit behind un-completed; a bare retry then read it as a fresh
predecessor block and demanded --stops.

## What changed (rotate.py, 34 production lines, ceiling 50)

1. `_prepare_checks` check 2 partition: when `_touch is None and _main_post`,
   block on the rotating post's OWN paths only (own card, via the SM.40 owner
   guess) and name every other non-churn path `foreign dirt (merge target
   unmeasured)` on a never-blocking line — never a refusal. git's own
   overwrite refusal still protects a dirty tracked file a real merge touches.
   The `(touch-set unmeasured)` suffix now only prints when there are actual
   own-path blockers. The foreign-dirt line says `(not in the merge)` when the
   touch-set resolved, `(merge target unmeasured)` when it could not.

2. `_stops_slot_is_stale`: a slot is a PREDECESSOR's stale block only after
   the generation ADVANCED. When the seat's CURRENT measured generation still
   equals the commit subject's starting `N` (the rotate-out never completed),
   return None — the seat is resuming after a blocked attempt, so the retry
   proceeds bare, no `--stops` demand (F23).

## Tests

- New: `test_prepare_check2_sm84_dt_foreign_dirt_and_untracked_draft_pass`
  (DT 00:18Z + 00:26Z): MAIN + unmeasurable touch, cron comms + rotation
  record + HANDOFF + another post's card + another post's untracked node
  draft -> rc 0, churn named, foreign named, no BLOCK.
- New: `test_prepare_check2_main_post_touch_unmeasured_scopes_own_paths`
  (replaces the obsolete all-dirt-blocks fallback test): foreign passes as
  info; the rotating post's OWN card still BLOCKS.
- New: `test_retry_after_blocked_rotate_out_not_stale` (F23): card committed
  `rotate-out gen 4->5`, row still gen 4 -> bare retry DELEGATES, no --stops.
- Old proxy tests `test_rotate_self_refuses_on_dirty_with_same_line`,
  `test_rotate_self_still_refuses_with_window_path_set`,
  `test_rotate_self_unpushed_plus_dirty_refuses_no_push` moved to WORKTREE
  seats so their 'own dirt blocks' intent no longer depends on the old MAIN
  unmeasurable-touch fallback.

## Evidence / result

Probe (before): Scenario B/C2 (foreign tracked / untracked drafts, touch
unmeasurable) rc=3 BLOCK. After fix: rc=0, `[ok] foreign dirt (merge target
unmeasured): ...` on both. Full rotate suite: 885 passed, 1 xfailed, 0 failed.
prepare+verb: 78 passed.

Raw output, screenshots, logs.

## Agent Notes
ITEM7: prepare/rotate-self check-2 scopes dirty-tree to the post's own paths on a MAIN post even when touch-set is unmeasurable (foreign dirt named info, never a block); _stops_slot_is_stale no longer fires after an uncompleted rotate-out, so a retry never re-asks --stops. 34 prod lines, 885 rotate tests green.
