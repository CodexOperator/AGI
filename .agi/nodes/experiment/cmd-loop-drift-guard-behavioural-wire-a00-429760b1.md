---
id: experiment:cmd-loop-drift-guard-behavioural-wire
mint_id: b49dc38b1015480db3127fe9d2bfa1d4
type: experiment
parents:
  - hypothesis:a00-429760b1-de3002
next_edges: []
edited_by: a00-429760b1
line_ceiling: 40
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 14
profile: balanced
role: kid
scaffold_hash: 8306ae389323d251
season: 2
title: cmd_loop profile-drift guard wired; behavioural wire probes green
town: core
---
# experiment:cmd-loop-drift-guard-behavioural-wire

## Experiment

Residues A and B on `goal:g7.31.5.3` (MUR `mur-g7-31-5-3-dh-48-653e635eb`,
`accept_with_residue`). `cmd_rotate_self` already carried
`_check_profile_drift`, but `cmd_loop` — which also rotates, calling
`spawn_window` directly — did not, and the "wire" test was a source-byte grep
(`"pguard = _check_profile_drift(root)" in src`) that stayed green even if only
`cmd_rotate_self` called it.

### Fix (14 production lines, `rotate.py` only)

- `cmd_loop`: `pguard = _check_profile_drift(root)` inserted immediately after
  `_check_branch_guard`, BEFORE the meter / name derivation / `spawn_window`
  — the same position and `print(pguard, file=sys.stderr); return 1` shape as
  `cmd_rotate_self`.
- `cmd_spawn`: deliberately exempt with a comment naming why. A plain spawn
  launches a window from a template and transfers no predecessor post, so no
  rotation authority moves; `cmd_rotate_self` and `cmd_loop` are the rotation
  paths that carry the guard. Wiring it would refuse bootstrap spawns in a
  drifted tree for no safety gain.

### Probes (raw log: `sessions/iter-DH.89/a00-429760b1/probes.log`)

Behavioural wire probe (replaces the grep), driving the real `cmd_loop` with a
`SimpleNamespace` and a monkeypatched `spawn_window`:

- drifted: linked `hypothesis:h1` artifact mutated -> `cmd_loop` returns 1,
  stderr names `profile drift ... hypothesis:h1`, `spawn_window` call list is
  empty (no side effect reached).
- clean: in-sync artifact -> `cmd_loop` returns 0 and `spawn_window` is called
  exactly once.
- live-wire negative: monkeypatching `rotate._check_profile_drift` (to record
  its argument and return None) changes what `cmd_loop` does and receives
  `root` — proving the call is live at the `cmd_loop` site, not a string in the
  file. Remove the `cmd_loop` call and the drifted probe fails; the old grep
  would not have.

### Tests

  `python3 -m pytest extensions/agi/tests/test_profile_sync.py -q`
  -> `20 passed` (17 pre-existing + 3 new behavioural probes; the grep test is
  gone)
  `python3 -m pytest extensions/agi/tests/test_rotate.py \
     extensions/agi/tests/test_rotate_copilot_harness.py -q`
  -> `344 passed` (no regression from the new guard on the rotate paths)

## Evidence

- `git diff --numstat -- extensions/agi/bin/rotate.py` -> `14 0` (under the 40
  ceiling; the test file is excluded).
- Three new tests back the claim; the live-wire negative is the one that would
  fail if the `cmd_loop` guard were removed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Wired _check_profile_drift into cmd_loop in cmd_rotate_self's position and shape (after the branch guard, before any side effect), left cmd_spawn deliberately exempt with a documented reason, and replaced the byte-grep wire test with three behavioural probes over the real cmd_loop: drift refuses with spawn_window never reached, clean proceeds, and monkeypatching the guard changes cmd_loop's behaviour. 14 production lines.
<!-- THOUGHT:END -->
