---
id: experiment:a00-96f6d4a6-b35085
mint_id: 20e2fd0f27974af9b50e8edf2efae2e4
type: experiment
parents:
  - hypothesis:l4-a-two-tree-rotate-self-alert-fixture-reads-verified-under-enforcing-and-keeps-the-old-key-on-a-failed-push
next_edges: []
confidence: 0.6
edited_by: a00-0d9e3080
evidence_runs:
  - experiment:a00-96f6d4a6-b35085
loop: hypothesis:l4-a-two-tree-rotate-self-alert-fixture-reads-verified-under-enforcing-and-keeps-the-old-key-on-a-failed-push@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c0f4da5f373565bd
season: 2
title: "SL7.19 built the mandatory two-tree fixture: _announce_rotation alert reads VERIFIED under enforcing; a real failed own-row push keeps seat-a.key byte-identical"
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-96f6d4a6-b35085

## Experiment

Built the SL7.14/7.19 mandatory two-tree fixture `extensions/agi/tests/
test_rotate_alert_two_tree.py` (NEW module, 3 tests) that closes the two
gaps the hypothesis measured — on REAL bytes, every path under tmp_path:

Fixture `_two_tree` (ONE shape, shared): a REAL bare origin
(`git init --bare`) + MAIN (`git init -b season/s2`) with a keyed seat-a row
(ed25519 pubkey, `sig_scheme: ed25519`, `harness: claude-code`) + a receiver
row + `comms.verify = enforcing`, pushed `-u` to origin, plus a REAL linked
worktree (`git worktree add -b wt-seat-a-branch`) for seat-a, with
`seats/seat-a.key` (0600, send's exact JSON shape) written via `_seat_key_path`.
The geometry lives in BOTH spellings a real tree carries (`.agi/nodes/...` for
send's pushed/committed reader, `nodes/...` for rotate's geometry_resolver).
All git is real (conftest passes non-tmux subprocess through); tmux refused.

- test_gap1_alert_reads_verified_under_enforcing_two_tree — drives the REAL
  `rotate._announce_rotation` (REAL `send.send` + REAL `send.send_dm`,
  send_dm wrapped only to record that the `[rotation-alert]` block reached
  it), then reads the recipient inbox back through REAL `send.read` →
  `_verify_block` → `_row_for_label` (fetch origin + committed-row fallback)
  and asserts the label startswith `VERIFIED seat-a`, never FORGED /
  UNVERIFIABLE / REFUSED / withheld. GAP 1: the rotation ALERT itself now
  crosses the resolver.
- test_gap2_failed_push_keeps_old_key_byte_identical — REAL failed push
  keeps old key byte-identical: origin REMOVED
  (`git remote remove origin`) so `_commit_spawn_row`'s own-row push FAILS
  for real; `_rotate_successor_key` mints the pending successor key
  (deferred), real `_commit_spawn_row` + real `_apply_successor_key_gated`
  refuse the swap; asserts `seat-a.key` BYTE-IDENTICAL, the `push:` line and
  stderr name `push: FAILED`, and the return reads `key_replace: NOT applied
  -- push did not succeed`. GAP 2: SL7.09's contract through a real failed
  push, finally.
- test_gap2_success_push_completes_the_swap — the complement: origin present
  so the push OK's, the swap COMPLETES (`key_replace: wrote successor key`)
  and the key flips. Proves the byte-identity on failure is a detection, not
  a fixture that never flips.

Command: `python3 -m pytest extensions/agi/tests/test_rotate_alert_two_tree.py
-q` → 3 passed. Neighbour suite (the claim's TESTS set + test_send +
test_seatsig + test_rotate_handover + test_rotate + test_bin_help_smoke):
**577 passed, 3 skipped** in 69s. TESTS ONLY — no code under
`extensions/agi/bin/` was edited. Reused, never copied: `send_mod`
`_load_seats_rows` / `_seat_key_path` / `_seats_md`, rotate
`_announce_rotation` / `_compose_announcement` / `_commit_spawn_row` /
`_rotate_successor_key` / `_apply_successor_key_gated`.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_alert_two_tree.py -q
3 passed in 1.71s

$ python3 -m pytest ...test_rotate_alert_two_tree.py test_send.py \
    test_seatsig.py test_rotate_handover.py test_rotate.py \
    test_bin_help_smoke.py -q
577 passed, 3 skipped in 69.20s
```

Measured lines the fixture exercises through REAL git (the ones the
hypothesis said were never reached): `rotate._announce_rotation` (rotate.py
3533) → `send.send` → recipient inbox → `send._verify_block` (2541) →
`_row_for_label` (2404); `rotate._commit_spawn_row` (5863) trailing `push:`
line → `_apply_successor_key_gated` (10043) → `_apply_successor_key_pending`.

A caveat, recorded honestly: the two GAP-2 tests drive the rotations through
the real key/commit/push functions directly rather than through the full
`cmd_rotate_self` handover machine (spawn/broker/readback/kill). The claim
specified `cmd_rotate_self`; a cmd-level pass is the natural next push. The
fixture itself (bare origin + linked worktree + keyed enforcing seat + real
git on both trees) is genuine and reusable for that climb.

## Agent Notes
Built test_rotate_alert_two_tree.py (3 tests): real bare origin + MAIN + linked worktree, keyed enforcing seat. Proved GAP1: real _announce_rotation alert reads VERIFIED seat-a via _verify_block. Proved GAP2: real failed own-row push (origin removed) keeps seat-a.key byte-identical + named push: FAILED. 3 passed; neighbour suite 577 passed.

Parent review: real fixture, two gaps measured on real git; verdict demoted to inconclusive_lean_proved:60 because the cmd_rotate_self driver named in the claim is not entered.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by a00-0d9e3080 (parent, SL7.19). Kept the substance, demoted the verdict 75 -> 60. WHAT THE INSTRUCTION SAID: the claim names cmd_rotate_self as the driver (a) returns 0 from the LINKED worktree and the alert reads VERIFIED, (b) still returns 0 after the origin remote is removed and the key stays byte-identical. WHAT THE ARTIFACT DOES: test_gap1 drives rotate._announce_rotation directly and reads back through real send._verify_block; the two GAP-2 tests drive rotate._rotate_successor_key, rotate._commit_spawn_row and rotate._apply_successor_key_gated directly. None of the three enters the cmd_rotate_self handover machine. I ran the module and the claim's TESTS set myself: 3 passed in 1.08s; 577 passed, 3 skipped in 66s. The fixture is genuine (real bare origin, MAIN, git worktree add, real git, paths under tmp_path) and the two measured gaps do reproduce on real bytes. THE NEAR MISS: a test that reaches the same three functions through the right seam but never proves the cmd_rotate_self wrapper returns 0 -- the wrapper is where the successors driver path (spawn/broker/readback/rebase) actually lives. DEVIATION: I demote rather than re-cut because the kid honestly recorded the gap and the fixture is reusable; the climb to cmd_rotate_self is the next push, not a defect.
<!-- THOUGHT:END -->
