---
id: experiment:a00-f918d3e3-15d035
mint_id: aa78c74eb5204258ba3f23d0f9d26f3a
type: experiment
parents:
  - hypothesis:rotate-self-registry-gate-reads-main-and-the-wrapper-restores-signals
next_edges: []
confidence: 0.85
edited_by: a00-63193a20
evidence_runs:
  - experiment:a00-f918d3e3-15d035
loop: hypothesis:rotate-self-registry-gate-reads-main-and-the-wrapper-restores-signals@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "MAIN+worktree fixture with DISAGREEING rows (MAIN role=director, worktree role=helper); cmd_rotate_self(--closeout) with _closeout_form_json capturing the role argument", "expected": "gate resolves through _seat_read_root and reads MAIN's row: role_read='director'", "observed": "post-fix role_read='director'; with _seat_read_root forced to return root (simulated pre-fix cfg_root) role_read='helper' and the probe FAILS", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "unique sentinel handler installed for SIGHUP/SIGTERM/SIGPIPE; cmd_rotate_self with _commit_rotation_record raising inside the shield window; assert getsignal identity; same probe against cmd_rotate_self.__wrapped__ (functools.wraps exposes the UNDECORATED pre-fix bytes)", "expected": "decorated call restores the exact prior handler OBJECTS on the exception path; pre-fix bytes leak SIG_IGN on all three", "observed": "decorated: leaked=none exact-restore=True; undecorated: leaked=['SIGHUP','SIGTERM','SIGPIPE']", "result": "held"}
production_lines: 28
profile: balanced
role: kid
scaffold_hash: 1f1df5bda8723cfd
season: 2
title: Rotate-self gate reads the writer's row; signal shield restored in a finally
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f918d3e3-15d035

**Verdict in one line: the fix is BUILT and both claims are PROVED by a new
test file that is red on the pre-fix bytes and green on the built ones.**

## What changed (production, 28 added lines, rotate.py)

```
(1) gate   18649  -row = _find_seat(cfg_root, seat)
                  +row = _find_seat(_seat_read_root(root, seat), seat)
                  the SAME resolution the --prepare branch uses (:18591);
                  one resolution, no second copy of the helper

(2) shield new @_restore_signals_on_exit (rotate.py:11264) wraps
           cmd_rotate_self (:18547): snapshot SIGHUP/SIGTERM/SIGPIPE
           BEFORE the call, restore in a finally on EVERY exit path
           (normal return, early return, raise). The success-path
           _restore_shield_signals(_shield_old) at :20413 is kept.
```

## The one deviation, and why it is the same guarantee

A literal `try:` re-indent around the 155-line shield window
(rotate.py 20232-20386) would add ~155 production lines — 4x the 40-line
ceiling and past the 2x done-refusal at 80. The decorator's `finally` runs
on exactly the same set of exit paths (the window has NO early return
between the shield install and the success return) while costing 22 lines.
The guarantee is try/finally on every way out, at the function boundary
instead of the block boundary.

## Proof — `extensions/agi/tests/test_rotate_self_registry_and_shield.py`

| test | pre-fix | post-fix |
|---|---|---|
| `test_nonprepare_gate_sees_main_only_seat` | RED, rc=1 `no seat` | green, rc=0 |
| `test_shield_restored_on_exception_inside_window` | RED, `SIGHUP is SIG_IGN` | green |
| `test_nonprepare_gate_falls_back_when_main_lacks_the_seat` | green (fallback) | green |

The gate test builds a REAL MAIN checkout + linked worktree (`_make`, the
`test_rotate_main_seat_rows.py` fixture): the seat exists in MAIN, the
worktree copy does not; `--closeout` (with `_closeout_form_json` stubbed)
is the post-gate seam. The shield test drives the full fixture rotate-self,
patches `_commit_rotation_record` to raise INSIDE the window, and asserts
`signal.getsignal` is byte-identical to before the call — restoring in the
test's own `finally` too, so a pre-fix run cannot poison the runtime.

RED verification: the two production edits were temporarily reverted
(edit, not git) and the file re-run — 2 failed, 1 passed, the two failures
exactly the two residues. Fix restored, then:

```
env -u TMUX -u TMUX_PANE python3 -m pytest \
  test_rotate_self_registry_and_shield.py test_rotate_selfreap.py \
  test_rotate_tail.py test_rotate_handover.py \
  test_rotate_launch_wrapper.py test_rotate_g1517.py \
  test_rotate_prepare.py test_rotate_main_seat_rows.py test_rotate.py -q
=> 510 passed, 771 warnings in 171.37s
```

The shared worktree already carried the `_caller_post` `_seat_read_root`
fix at :18041 (EF.30); EF.68 closes the rotate-self gate that was left
outside it. `production_lines: 28` (`git diff --numstat HEAD` → `28 1
rotate.py`).

## Evidence

- `git diff --numstat HEAD` → `28	1	extensions/agi/bin/rotate.py`
- new-test run post-fix: `3 passed`
- new-test run pre-fix: `2 failed, 1 passed`
- named-file suite post-fix: `510 passed`
- no live tmux/process/rotate-self-run was touched; own-chain derive stays
  refused under `PYTEST_CURRENT_TEST`, so no real TERM ever fires.

## Agent Notes
built both fixes in rotate.py (gate reads _seat_read_root; new _restore_signals_on_exit decorator = try/finally on every exit path for the shield); new test_rotate_self_registry_and_shield.py red on pre-fix bytes, green post-fix; 510 named-file tests pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW EF.68 (a00-63193a20), accepted proved. (1) Instruction: one parent-run negative probe per claim conjunct, recorded as probes in the kid node, and the kid delivers a fix whose new test file is red on the pre-fix bytes. (2) Machine: git diff 15251fdc28..2709119cda carries rotate.py +28/-1, the new test file, and the node; the gate now reads _find_seat(_seat_read_root(root, seat), seat) and cmd_rotate_self is wrapped by _restore_signals_on_exit, whose functools.wraps finally restores the snapshot. My two probes (recorded above) pass and each discriminates: the disagreeing-row fixture reads director post-fix and helper when _seat_read_root is forced to return root; the sentinel probe shows decorated leaked=none while __wrapped__ leaks all three signals. New test file re-run by me: 3 passed in 0.63s. (3) Near miss: a probe that only asserts latest_restore is not SIG_IGN would pass on a decorator that reset to SIG_DFL and never restored a custom prior handler; my probe installs unique handler objects and asserts identity, so that near miss is excluded. (4) Deviation accepted: the kid used a function-boundary decorator instead of re-indenting the 155-line window in try/finally. The window has no early return between the shield install at :20258 and the success restore at :20413, so the decorator finally covers the same exit set including raises; my exception probe proves the guarantee empirically on the changed bytes. Caveat: the node testable_claim still says launch wrapper signal reset at ~19991/~20145 while the director orders scoped the R5 leak to the cmd_rotate_self shield; a later reader should not look for a launch-wrapper change.
<!-- THOUGHT:END -->

PARENT EF.68 review: ACCEPTED proved. Diff 15251fdc28..2709119cda read byte-for-byte: rotate.py gate now _find_seat(_seat_read_root(root, seat), seat) (one resolution, same as --prepare) and cmd_rotate_self is wrapped by _restore_signals_on_exit (functools.wraps + finally). Two parent probes recorded above, both held and both discriminate vs the pre-fix bytes; new test file re-run by the parent 3 passed in 0.63s. Zero demotions.
