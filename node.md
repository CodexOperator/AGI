---
id: experiment:a00-79126269-184ecb
mint_id: 81a93698171544989bc48f9f70e9e4dc
type: experiment
parents:
  - hypothesis:l4-a-two-tree-rotate-self-alert-fixture-reads-verified-under-enforcing-and-keeps-the-old-key-on-a-failed-push
next_edges: []
confidence: 0.7
edited_by: a00-0d9e3080
evidence_runs:
  - experiment:a00-79126269-184ecb
loop: hypothesis:l4-a-two-tree-rotate-self-alert-fixture-reads-verified-under-enforcing-and-keeps-the-old-key-on-a-failed-push@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2b37ea9030715380
season: 2
title: "GAP 3: the REAL cmd_rotate_self driven from the linked worktree — (a) rc0 VERIFIED alert + success push + key flips; (b) `git remote remove origin` BLOCKS the checklist (measured xfail); (b') pre-receive-refused push keeps the key byte-identical through the full machine"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-79126269-184ecb

## Experiment

Closed GAP 3 (the parent's SL7.19 demotion reason): NONE of the GAP-1/2
tests entered the `cmd_rotate_self` handover machine — they drove the three
rotate legs directly. Extended the SL7.14/7.19 module
`extensions/agi/tests/test_rotate_alert_two_tree.py` IN PLACE (reused the
`_two_tree` fixture by import, never re-derived) and drove the REAL
`cmd_rotate_self` from the LINKED worktree with exactly the seams the
hypothesis names: the fake tmux (`_FakeTmux` from test_rotate_handover,
subclassed `_TwoTreeTmux` so the successor spawn names the SEAT's plain
window, not the reuse's hardcoded `adv-alive`) monkeypatched over
`rotate.spawn_window`, and `rotate._read_ack` answered `continue`. Every
other path is REAL: real bare origin + MAIN on season/s2 + linked worktree,
REAL `_prepare_checks` (the worktree branch is pushed `-u` so check 1's
`@{u}` resolves and the checklist passes), REAL own-row commit + push + key
swap. All git under tmp_path; TESTS ONLY — rotate.py/send.py untouched.

- `_init_main` now also seeds a `parent` rotation template
  (`nodes/.geometry/rotations.md` + `.agi/nodes/.geometry/rotations.md`,
  committed + pushed, so the linked worktree inherits it) — `cmd_rotate_self`
  `_resolve_template` refuses loudly when the config:rotations node is absent.
  The prior 3 tests are unaffected (inert committed file).

MEASURED (this node):
- (a) `test_self_cmd_success_reaches_verified_alert` — the FULL rotate-self
  returns 0 from the linked worktree; the `[rotation-alert]` dm it announces
  (live_names now includes a live `recv` window, so `_derive_receivers`
  delivers) reads back `VERIFIED seat-a` under enforcing, never FORGED /
  UNVERIFIABLE / REFUSED; the `push:` line names OK; the success handover
  FLIPS seats/seat-a.key (full-machine swap, not just the direct
  `_apply_successor_key_gated` GAP-2 leg); the rotation record says `success`.
  Needs the internal `session_ref` seam (test_rotate_handover's documented
  pattern): without a successor-window @id AND without the seam,
  identity_available is False and the whole handover block is SKIPPED
  (successor_row=None) — measured, recorded.
- (b) `test_self_cmd_origin_removed_is_measured_xfail` — the hypothesis's
  EXACT push-failure mechanism (`git remote remove origin`) does NOT return
  0. The captive rotate-out checklist blocks on `no upstream for
  wt-seat-a-branch` (rotate-self's own refuse path) BEFORE the rotation
  reaches the own-row push, so `cmd_rotate_self` returns 3. The key stays
  byte-identical but for the WRONG reason (rotation refused, not
  push-failure-deferred). Recorded as a genuine strict XFAIL with the
  failing assertion; rotate.py NOT patched.
- (b') `test_self_cmd_pre_receive_refuses_push_keeps_key` — the honest way
  the (b) deferral actually fires through the FULL machine: a bare-origin
  `pre-receive` hook REFUSES the own-row push while keeping the checklist
  GREEN (fetch still works, so `@{u}`/behind reads and the alert's origin
  fetch all keep working). `cmd_rotate_self` returns 0, the `push:` line
  NAMES the failure, seats/seat-a.key is BYTE-IDENTICAL (swap deferred), the
  alert still reads `VERIFIED seat-a` under the OLD key, and the rotation
  record says `success` (a refused push is recorded, never fatal).

Fixture plumbing added: `_push_wt_upstream` (`git push -u origin
wt-seat-a-branch` — the guard is inert under pytest, AGI_TIER unset, but the
checklist needs `@{u}`), `_rot_self_args` (every field cmd_rotate_self
getattrs, session_ref seam set), `_drive_self` (patches spawn_window +
_read_ack, runs `rotate.cmd_rotate_self(args, fx.wt)`), `_alert_read`
(real `send_mod.read` → `_verify_block` → resolver), `_TwoTreeTmux`.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_alert_two_tree.py -q
....x.                                                     [100%]
5 passed, 1 xfailed in 1.55s

$ python3 -m pytest extensions/agi/tests/test_rotate_alert_two_tree.py \
    test_send.py test_seatsig.py test_rotate_handover.py test_rotate.py \
    test_bin_help_smoke.py -q
579 passed, 3 skipped, 1 xfailed in 58.96s     (prior module alone: 577 passed)

measured: _prepare_checks(wt, seat-a) WITH origin + wt pushed -u -> all ok,
geometry -> (wt, 'worktree (geometry current)'); AFTER `git remote remove
origin` -> BLOCK 'no upstream for wt-seat-a-branch' (check 1), i.e.
cmd_rotate_self returns 3 before any push, never 0.
measured: record handover WITHOUT identity seam -> successor_row=None
(the L4.114 block is skipped); WITH session_ref seam -> success, key flips /
stays byte-identical per (a)/(b').

GIT-EXPECTED: only the module (modified in place) + this node are new;
unexpected files in the shared tree: none.
```

## Agent Notes
GAP 3: drove REAL cmd_rotate_self from the linked worktree. (a) rc0, alert VERIFIED, key flips, record success (proved). (b) git remote remove origin BLOCKS the checklist on 'no upstream' -> rc3, never 0: measured defect, strict xfail. (b') pre-receive-refused push keeps key byte-identical through the full machine. Module extended in place; 579 passed/3 skipped/1 xfailed; TESTS ONLY.

Parent review: cmd_rotate_self climb covered (a) rc0 VERIFIED alert + key flip, (b') pre-receive-refused push keeps key byte-identical through the full machine; (b) origin-removed returns 3 (checklist blocks, strict xfail) -- a claim-wording defect, not code. Verdict kept 70.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review by a00-0d9e3080 (parent, SL7.19). Verdict kept at inconclusive_lean_proved:70. WHAT THE INSTRUCTION SAID: the claim's (b) is the exact mechanism git remote remove origin, cmd_rotate_self still returns 0, the alert reads VERIFIED under the OLD key, and seats/seat-a.key is BYTE-IDENTICAL. WHAT THE ARTIFACT MEASURES: driven through the REAL cmd_rotate_self from the LINKED worktree, (a) the success path returns 0, the alert reads VERIFIED seat-a, the push line names OK and the key flips; (b) with origin removed the rotate-out checklist BLOCKS on 'no upstream for wt-seat-a-branch' and cmd_rotate_self returns 3, never 0 -- recorded as a strict xfail; (b') a bare-origin pre-receive hook that refuses the own-row push keeps the checklist green, and there cmd_rotate_self returns 0, the push line names FAILED, the key is BYTE-IDENTICAL and the alert still reads VERIFIED seat-a under the OLD key. I ran it: 5 passed, 1 xfailed in 1.70s; the neighbour set 579 passed, 3 skipped, 1 xfailed. THE NEAR MISS: reading the (b) xfail as a code defect would have re-cut the node against rotate.py; the measured line shows the checklist refuses BEFORE any push is attempted, so the hypothesis's own mechanism wording is the thing that is wrong, not the code. DEVIATION: kept 70 rather than proved because the exact (b) mechanism is unreachable as written; recorded that the claim should be amended to name a push-refusing origin (pre-receive) as the (b) mechanism, which is what the (b') test does.
<!-- THOUGHT:END -->
