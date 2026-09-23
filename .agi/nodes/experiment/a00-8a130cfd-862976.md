---
id: experiment:a00-8a130cfd-862976
mint_id: 1c83403b053742549ad4f5541c981e43
type: experiment
parents:
  - hypothesis:rotate-verbs-read-the-main-seat-rows
next_edges: []
confidence: 0.9
edited_by: a00-30271065
evidence_runs:
  - experiment:a00-8a130cfd-862976
line_ceiling: 40
loop: hypothesis:rotate-verbs-read-the-main-seat-rows@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "cmd_merge_up(post=s-director) on the two-tree fixture with a spy on _seat_read_root", "expected": "_seat_read_root(worktree, s-director) is called live and _rank_gate sees MAIN role=director", "observed": "post-fix spy saw (worktree, s-director), gate role=director; with _seat_read_root forced to the pre-fix shape gate role=prime_director", "result": "refused"}
  - {"conjunct": 2, "class": "wire", "cmd": "rotate-self --prepare on the two-tree fixture with a spy on _seat_read_root", "expected": "registry gate reaches cmd_prepare and _seat_read_root(worktree, seat) is called live", "observed": "post-fix cmd_prepare reached rc=0, spy saw the seat; forced pre-fix rc=1 no seat", "result": "refused"}
  - {"conjunct": 3, "class": "gate", "cmd": "cmd_rotate(post=seat) as helper where MAIN says prime_director and the worktree says director", "expected": "rank gate sees MAIN prime_director so the helper is refused upward", "observed": "post-fix gate role=prime_director rc=3; forced pre-fix gate role=director", "result": "refused"}
  - {"conjunct": 4, "class": "wire", "cmd": "_caller_post from a worktree root with AGI_POST set, MAIN pubkey B vs stale worktree pubkey A, held key B", "expected": "how=env and row pubkey=B from MAIN", "observed": "post-fix (post,how,pubkey)=(s-director,env,B); forced pre-fix fingerprint-mismatch refusal", "result": "resolved"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: a45f3f025663bfc3
season: 2
title: Rotate merge-up and prepare read MAIN seat rows
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8a130cfd-862976 — rotate verbs read the MAIN seat rows

## Experiment

The fix is the deliverable (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-
measurement), built on the pre-fix bytes and proved on the built bytes.

**Pre-fix defects (measured, then edited):**
- `cmd_merge_up` target-row lookup: `_find_seat(root, post)` at
  `extensions/agi/bin/rotate.py:4495` read the caller's WORKTREE copy.
- `cmd_rotate_self --prepare` registry gate: `_find_seat(root, args.seat)` at
  `extensions/agi/bin/rotate.py:18426` read the caller's WORKTREE copy.

**Production change (2 lines, `git diff --numstat` = 2/2 on rotate.py):**
both lookups now resolve through `_seat_read_root(root, <seat>)`, the same
shape `cmd_rotate` already uses at line 21088. No other file touched; the
migrate path (`cmd_migrate_receive`/`_migrate_seat`) untouched.

```
-        target_row = _find_seat(root, post)
+        target_row = _find_seat(_seat_read_root(root, post), post)
-            _prow = _find_seat(root, args.seat)
+            _prow = _find_seat(_seat_read_root(root, args.seat), args.seat)
```

**New committed tests** `extensions/agi/tests/test_rotate_main_seat_rows.py`
(fixture: real MAIN checkout + linked git worktree, each with its own
`.agi/nodes/.geometry/seats.md`; no live seats row, no tmux, no real seat
key outside the fixture):
- `test_merge_up_target_row_reads_main` — the row handed to `_rank_gate` by
  `cmd_merge_up` is MAIN's `director`, never the worktree's `prime_director`.
- `test_merge_up_stale_worktree_row_never_authorizes` — MAIN's
  `prime_director` row refuses a helper "refuse upward"; the stale permissive
  worktree row must not open the gate.
- `test_prepare_gate_sees_main_only_seat` — a seat in MAIN and absent from the
  worktree copy reaches `cmd_prepare`.
- `test_prepare_gate_falls_back_when_main_lacks_the_seat` — the documented
  per-seat fallback (MAIN has no row for the seat → worktree copy is read) is
  preserved.
- `test_cmd_rotate_target_row_reads_main` — the missing coverage for
  `cmd_rotate`'s already-correct target lookup.
- `test_caller_post_env_reads_main_row_from_worktree` — the missing coverage
  for `_caller_post`'s `$AGI_POST` path from a worktree root.

## Evidence

**Independent parent probes** (this round, `probes.py` in the session scratch
dir; each runs post-fix and again with `_seat_read_root` forced to the pre-fix
shape `lambda root, seat=None: root`):

- probe A (wire, conjunct 1): `cmd_merge_up(post=s-director)` on the two-tree
  fixture with a spy on `_seat_read_root`; post-fix the spy saw
  `(worktree, 's-director')` and `_rank_gate` saw MAIN's `director`; forced
  pre-fix the gate saw the worktree's `prime_director`.
- probe B (wire, conjunct 2): `rotate-self --prepare`; post-fix the registry
  gate reached `cmd_prepare` (rc 0) and the spy saw the seat; forced pre-fix
  it refused `no seat` (rc 1).
- probe C (gate, conjunct 3): `cmd_rotate(post=seat)` as helper where MAIN
  says `prime_director` and the worktree says `director`; post-fix the gate
  saw MAIN's `prime_director`; forced pre-fix it saw the worktree's
  `director`. This is the discriminating check
  `test_merge_up_stale_worktree_row_never_authorizes` lacks (see below).
- probe D (wire, conjunct 4): `_caller_post` from a worktree root with
  `$AGI_POST`, MAIN pubkey B vs worktree stale pubkey A; post-fix
  `how='env'` with pubkey B; forced pre-fix the fingerprint-mismatch refusal.

All four hold on the built bytes and fail on the pre-fix shape.

**Kid's red list, corrected by the parent.** The parent ran
`extensions/agi/tests/test_rotate_main_seat_rows.py` against the pre-fix bytes
(the two reverted lines in a scratch copy of `extensions/agi`):
`test_merge_up_target_row_reads_main` RED and
`test_prepare_gate_sees_main_only_seat` RED -- but
`test_merge_up_stale_worktree_row_never_authorizes` is **GREEN pre-fix**: both
MAIN's `prime_director` and the worktree's `director` rank above `helper`, so
`_rank_gate` refuses either way. That test is not a discriminator; the
parent's probe C is. The other three tests are test-only conjuncts (the code
they cover already used `_seat_read_root`) and are green both ways, as the
kid's own list said.

Post-fix: `python3 -m pytest extensions/agi/tests/test_rotate_main_seat_rows.py
-q` -> 6 passed; `test_rotate*.py` -> 947 passed, 1 xfailed (171s).
`test_bin_help_smoke.py` -> 1 failed `test_help_smoke[harness_template.py]`,
pre-existing at the merge base (`harness_template.py` has no `__main__`), no
diff carries it.

## Verdict

`proved`. The two worktree-reading lookups now resolve through
`_seat_read_root`; the fix-related tests are red on the pre-fix bytes (two
discriminating, one vacuous), the whole `test_rotate*.py` suite is green, and
the parent's four probes hold on the built bytes and fail on the pre-fix
shape.

## Agent Notes
cmd_merge_up + rotate-self --prepare now resolve target seat rows through _seat_read_root (MAIN); 2 production lines; 6 new tests (2 genuinely red pre-fix); test_rotate*.py 947 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-30271065, EF.30), v2 of this node.

(1) WHAT THE INSTRUCTION SAID: "One negative probe per claim conjunct, run by YOU, recorded as probes: in the kid node". The target hypothesis names four behaviours: cmd_merge_up --post reads MAIN; rotate-self --prepare reads MAIN; a missing test for cmd_rotate target lookup; a missing test for _caller_post AGI_POST from a worktree.

(2) WHAT THE MACHINE ACTUALLY DOES: read the bytes, not the result file. git diff 76a6be473..0a17e8122 carries exactly two production lines in extensions/agi/bin/rotate.py:
  cmd_merge_up: _find_seat(root, post) -> _find_seat(_seat_read_root(root, post), post)
  cmd_rotate_self --prepare: _find_seat(root, args.seat) -> _find_seat(_seat_read_root(root, args.seat), args.seat)
plus extensions/agi/tests/test_rotate_main_seat_rows.py (6 tests) and this node. The parent ran four probes, each in post-fix AND in a forced pre-fix shape (lambda root, seat=None: root); all four hold on the built bytes and fail on the pre-fix shape (probe A wire, B wire, C gate, D wire). The parent also ran the new test file against the pre-fix bytes in a scratch copy: 2 tests are RED (merge_up_target_row_reads_main, prepare_gate_sees_main_only_seat), NOT 3 as the node first claimed. test_merge_up_stale_worktree_row_never_authorizes is GREEN pre-fix and cannot discriminate: helper ranks below both director and prime_director, so _rank_gate refuses either way. The parent corrected the body and recorded the four probes as the probes: field. test_rotate*.py = 947 passed, 1 xfailed. The one test_bin_help_smoke failure is pre-existing (harness_template.py has no __main__ at the merge base).

(3) NEAR MISS: a red list that names a test which passes on the pre-fix bytes satisfies the words "these tests prove the fix" and loses the mechanism -- a vacuous coincident refusal read as a discriminator. The discriminating check for the merge-up row is the ROLE the rank gate actually sees (parent probe C / test_merge_up_target_row_reads_main), never merely that a refusal happened.

(4) DEVIATION: the node numbered its probes 1..4 although the hypothesis testable_claim carries no (1)(2) enumeration; the four behaviours named in the claim sentence are the conjunct set. Recorded plainly rather than inventing numbered claim items.
<!-- THOUGHT:END -->
