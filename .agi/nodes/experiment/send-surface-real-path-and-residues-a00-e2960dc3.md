---
id: experiment:send-surface-real-path-and-residues-a00-e2960dc3
mint_id: 1bbf3fadd7c8491ca7ebc745240343ea
type: experiment
parents:
  - hypothesis:a00-e2960dc3-29c33b
next_edges: []
edited_by: a00-e2960dc3
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: fdec345eee60c2f6
season: 2
thought_session: dh.25-g7.31.4.2
title: "DH.25 residue closure: real-path foreign refusal plus corrected-path greps"
town: core
---
<!-- BODY:BEGIN -->
# experiment:send-surface-real-path-and-residues-a00-e2960dc3

## Experiment

Closes the three PRIMARY residues a MUR verify named against the DH.21
accept of `goal:g7.31.4.2`. No production code changed; the claim is proved
on the bytes the tests already exercise.

- **R1** — the DH.21 experiment node cited a gitignored `grep.txt` for runs
  the file did not contain. Fixed in place: the measured command+output
  transcripts now sit INLINE in that node's body, and it cites the node and
  the committed test file, never a session file.
- **R2** — the quoted production grep named `extensions/agi/skills`, which
  does not exist (skills lives at repo-root `skills/`), so its exit 2 measured
  nothing. Re-measured below on the CORRECT paths.
- **R3** — conjunct 2 was proven only against a stub of `send._nudge_window`.
  Added a runnable test that calls the REAL `send.send_dm` with the REAL
  `send._nudge_window` and REAL `send._nudge_target`: only the tmux/capture
  layer (`_window_id_listed`, `_leave_copy_mode`, `_capture_pane`,
  `_send_keys`, `_registry_status`) is faked. It asserts a foreign-box peer is
  refused by name with zero keystrokes typed, and a local peer is reached by
  the same call with the same result shape.

## Evidence

**New test — real path, only tmux faked** (`-q`):

```
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest \
    extensions/agi/tests/test_send_surface_ssh_or_not.py -q
....                                                                     [100%]
4 passed in 0.74s
```

**Same suite plus the two guard suites (parity with the DH.21 run):**

```
$ PYTHONPATH=/tmp/pytestenv python3 -m pytest \
    extensions/agi/tests/test_send_surface_ssh_or_not.py \
    extensions/agi/tests/test_box_guard.py \
    extensions/agi/tests/test_send.py -q
........................................................................ [ 21%]
........................................................................ [ 42%]
........................................................................ [ 63%]
........................................................................ [ 84%]
....................................................                     [100%]
340 passed, 11 warnings in 35.24s
```

(The 11 warnings are the pre-existing `datetime.utcnow()` deprecation from
`node_writer.py:1276` in `test_send.py`; unrelated to this claim. 339 -> 340
is the one new test.)

**The real path, measured in the test's own assertions:**

```
# foreign-box peer (box local-town, this box core-town):
#   send_dm(...) -> Path written; stderr: "nudge: far-seat is a FOREIGN box row
#   (box local-town); refusing as a target"; typed == []
# local peer:
#   send_dm(...) -> Path written; typed == [('agi-rc:@111', ('[nudge: sender]: hi local',)),
#                                          ('agi-rc:@111', ('Enter',))]
# both: same parent dir, one block each with ts/from/to + text.
```

**R2 greps, correct paths, real exit codes:**

```
$ grep -rn "is_ssh" extensions/agi/bin extensions/agi/src skills
exit=1        # zero hits: production paths are clean

$ grep -rn "is_ssh" extensions/agi/bin extensions/agi/src skills --include='*.py'
exit=1        # zero hits, .py only

$ grep -rn "is_ssh" extensions/agi/tests/test_send_surface_ssh_or_not.py
extensions/agi/tests/test_send_surface_ssh_or_not.py:3:transport chosen engine-internally, zero `is_ssh` in the caller bodies.
extensions/agi/tests/test_send_surface_ssh_or_not.py:78:# conjunct 4: no `is_ssh` in the caller-facing send/nudge bodies (source bytes).
extensions/agi/tests/test_send_surface_ssh_or_not.py:79:def test_no_is_ssh_in_caller_facing_send_bodies():
extensions/agi/tests/test_send_surface_ssh_or_not.py:87:        assert "is_ssh" not in (ast.get_source_segment(src, fn) or ""), fn.name
exit=0
```

`is_ssh` occurs only in the new test file, which must name the string to
assert it is absent from `send.py`'s caller-facing bodies — that is not a
production path. Production paths (`extensions/agi/bin`, `extensions/agi/src`,
repo-root `skills/`) are measured separately and are zero.

## Evidence files

- Test: `extensions/agi/tests/test_send_surface_ssh_or_not.py`
  (`test_real_path_refuses_foreign_box_and_reaches_local`)
- Corrected in place: `.agi/nodes/experiment/send-surface-ssh-or-not-a00-dd757e64.md`

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.25 corrective round: prior round accepted with three evidentiary residues. R1 closed by moving the measured transcripts inline into the node body and dropping the gitignored session pointer; R2 closed by re-measuring on the existing paths (extensions/agi/bin, extensions/agi/src, repo-root skills) after the bogus extensions/agi/skills path exited 2; R3 closed by a committed runnable test that stubs neither _nudge_window nor _nudge_target. No production code touched (production_lines 0), only the test file grew 37 lines.
<!-- THOUGHT:END -->
