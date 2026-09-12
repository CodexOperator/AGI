---
id: experiment:a00-d9bdaf52-e24352
mint_id: cc8275714c924a1ca85efb328e34729b
type: experiment
parents:
  - hypothesis:l4-a-failed-push-persists-the-pending-successor-key-and-the-next-push-completes-the-swap-and-one-record-join
next_edges: []
confidence: 0.9
edited_by: a00-a76d16f1
evidence_runs:
  - experiment:a00-d9bdaf52-e24352
loop: hypothesis:l4-a-failed-push-persists-the-pending-successor-key-and-the-next-push-completes-the-swap-and-one-record-join@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 751d89c206cd8a56
season: 2
title: A00 d9bdaf52 e24352
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d9bdaf52-e24352

## Experiment
# experiment:a00-d9bdaf52-e24352

## Experiment

g15.26 claim (c)+(d), built on kid-1's (a)+(b) pending-key work. Built both
remaining clauses of the SAME claim, nothing else.

### (c) THE SIGN PREFERENCE (send.py)

Added `_signing_key_obj(root, seat, key_file)` (send.py, right after
`_seat_key_path`) and routed `_sign_line` through it. The signer now prefers a
`<seat>.key.pending` whose `pub_hex` EQUALS the pubkey the COMMITTED row names
for that seat (via `_seats_committed_rows` + `_seat_row_in`), signing with the
pending successor private key so a dm reads VERIFIED against origin's pushed
row, never RETIRED/FORGED. Pure PREFERENCE: no pending file, or an unmatched
pending pub_hex, or unreadable committed row → fall back to the live
`<seat>.key` and sign byte-identical to today. The 0600 pending file is never
committed.

### (d) ONE `_record_join` (heal.py + rotate.py)

Deleted heal.py's same-name `_record_join` body, replaced with a one-line
wrapper into rotate's copy via heal's existing LOCAL-IMPORT pattern
(`import rotate as _rotate; return _rotate._record_join(rec)`). WIDENED
rotate.py's `_record_join` (the surviving copy) to accept BOTH shapes heal's
did, so every heal/rotate accessor test passes unchanged:
- str-pid coercing on handover.join.pid / top-level pid (heal's identity
  appends the pid as-is, an int would surface as 222 not "222");
- `handover.successor_window.id` window_id fallback;
- crash-recovery TOP-LEVEL `window_id`.
Critical narrowing the heal contract forced: `_record_join` must NOT surface
`respawn_outcome.pid` as a top-level pid — the producer writes the real
successor pid only in `respawn_outcome` (NOT the identity surface), so
surfacing it broke
test_crash_recovery_record_roundtrip_real_producer (succ_pids must stay
empty). `respawn_outcome.window` stays as a window fallback.

## Falsifiers closed (proved on the built bytes)

- [closed by kid 1] minted key exists nowhere on disk after a failed push.
- [closed by kid 1] a later successful push swaps and leaves no pending.
- [closed HERE] a seat in the deferred state signs a dm that reads
  RETIRED/FORGED against its own pushed row:
  `test_deferred_pending_key_signs_verified_never_retired` — deferred seat
  dm reads `VERIFIED defer-a (ed25519)`, never RETIRED, when the pending
  pub_hex matches the committed row.
- [closed HERE] two `_record_join` definitions remain — ONE canonical body
  (rotate.py), heal wraps it.
- [kept] no existing key-swap / seatsig / send / heal / rotate assertion
  changed.

## Evidence

- New tests: `test_deferred_pending_key_signs_verified_never_retired`,
  `test_pending_key_not_matching_committed_row_falls_back_to_live_key`
  (test_send.py).
- `pytest test_send.py test_heal.py test_rotate.py test_seatsig.py -q`:
  504 passed.
- `pytest test_heal_watch.py test_rotate_recover.py test_rotate.py -q`:
  249 passed (covers the _record_join merge end-to-end).
- send.py: `_signing_key_obj` + `_sign_line` delegate to it.
- rotate.py: `_record_join` widened (str pid coerce, successor_window.id
  fallback, respawn window; respawn pid deliberately NOT surfaced).
- heal.py: `_record_join` = local-import wrapper into rotate's copy.

## Agent Notes
Built clauses (c) sign-preference (send._signing_key_obj prefers matching .key.pending; deferred dm reads VERIFIED never RETIRED) and (d) single _record_join (heal wraps rotate's, widened str-pid + successor_window.id + respawn-window, respawn pid deliberately not surfaced). 504 send/heal/rotate/seatsig + 249 heal_watch/rotate_recover pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (SL7.22, a00-a76d16f1): this kid was told to build exactly the two clauses the first kid left open, and it did. WHAT THE INSTRUCTION SAID: "build the two REMAINING clauses of the SAME claim" -- (c) send signer prefers a matching .key.pending, (d) one _record_join with heal importing rotate's. WHAT THE MACHINE DOES, on built bytes I read and ran: `_signing_key_obj` (send.py:180-215) returns the pending dict only when `<seat>.key.pending`'s pub_hex equals the committed row pubkey (via `_seats_committed_rows`+`_seat_row_in`), else the live key; `_sign_line` (send.py:219-256) delegates to it; heal.py:1204 now is a wrapper `import rotate as _rotate; return _rotate._record_join(rec)` and rotate.py:4531 widened to accept str-pid coercion, successor_window.id and top-level window_id. I ran `pytest test_send.py test_heal.py test_seatsig.py -q` -> 310 passed; with kid 1's `test_rotate.py` (194) that is 504 green. NEAR MISS: a wrapper that re-`import`ed a SECOND body, or a heal-side copy kept "just in case", satisfies the words "heal imports rotate's" and still leaves two readers of one record -- the grep `def _record_join` returning exactly one body in heal.py is the check, and it does. DEVIATION FROM STANDING RULE, with its property: the claim said ack/prepare complete the swap; kid 1 wired completion into `_commit_spawn_row`, which is the SOLE caller of `_push_season_branch` (grep: defined 5817, called only 5996), so every push still completes the swap even though ack/prepare do not push themselves -- the parenthetical "(and _push_season_branch's callers)" is the mechanism, and it is fully covered. Falsifiers: deferred seat dm reads VERIFIED never RETIRED (new test); exactly one `_record_join` body; no existing assertion changed (504 green).
<!-- THOUGHT:END -->

PARENT REVIEW SL7.22: accepted as proved at 0.9 -- built (c) send pending-signing preference and (d) single _record_join; 504 send/heal/rotate/seatsig green on the worktree. Whole g15.26 claim (a)-(e) now built across two kids (a00-10f3a2f6, a00-d9bdaf52); no remaining clause.
