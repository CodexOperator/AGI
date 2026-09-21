---
id: experiment:send-surface-ssh-or-not-a00-dd757e64
mint_id: 32759c492f6c41ee97db114acef3c9dc
type: experiment
parents:
  - hypothesis:a00-dd757e64-e70abc
next_edges: []
edited_by: a00-e2960dc3
evidence_runs: experiment:send-surface-ssh-or-not-a00-dd757e64
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f371b16508b966ff
season: 2
title: Same send_dm call and result shape for a local and a foreign-box peer; transport stays engine-internal
town: core
---
<!-- BODY:BEGIN -->
# experiment:send-surface-ssh-or-not-a00-dd757e64

## Experiment

Built `extensions/agi/tests/test_send_surface_ssh_or_not.py` (a surface-
invariance test) and ran it with the two existing guard suites. No production
code was changed — the test passed on the built bytes, so no engine edit was
needed or made.

**Command** (naming files explicitly, kid-tier gate honoured):

```
PYTHONPATH=/tmp/pytestenv python3 -m pytest \
  extensions/agi/tests/test_send_surface_ssh_or_not.py \
  extensions/agi/tests/test_box_guard.py \
  extensions/agi/tests/test_send.py -q
```

### Raw output (tail)

```
340 passed, 11 warnings in 35.24s
```

(11 warnings are the pre-existing `datetime.utcnow()` deprecation from
`node_writer.py:1276` in `test_send.py`; unrelated to this claim. 340 = the 3
original tests + 1 added in DH.25 that exercises the REAL nudge path.)

### The four conjuncts as the test pins them

1. **Same names/args** — `send_dm(root, "sender", to, text, "sender")` is
   called for both peers with no transport argument:
   `test_same_send_dm_call_and_result_shape_both_transports`.
2. **Same result shape** — both calls return a `Path`, both files exist, and
   `send._conv_blocks` shows exactly one block with `ts`/`from`/`to` + body;
   both calls hit the single `send._nudge_window` seam with only the name
   differing (`nudged == ["local-seat", "far-seat"]`). NOTE: that test
   monkeypatches `_nudge_window`, so it proves the seam is reached, not what
   the real seam does. The REAL path is closed by
   `test_real_path_refuses_foreign_box_and_reaches_local` (DH.25), which
   stubs neither `_nudge_window` nor `_nudge_target` and asserts the foreign
   box is refused by name with zero keystrokes typed, the local peer typed
   (`agi-rc:@111`), and the same Path/block shape for both.
3. **Engine-internal transport** — `send._nudge_target(root, "local-seat",
   None)` is a tuple, `send._nudge_target(root, "far-seat", None)` is `None`
   (`test_transport_decision_is_engine_internal`). The refuse is at `send.py`'
   `_nudge_target`'s `boxes.row_is_local` guard; the remote gap-fill is the
   `mail_poll` cron (`crons.py:588`) proved by
   `test_box_guard.py:173` (`test_mail_poll_one_tick_through_bare_hub`), which
   also ran green in this command.
4. **Zero `is_ssh` in caller bodies** — `test_no_is_ssh_in_caller_facing_send_
   bodies` reads `extensions/agi/bin/send.py` source bytes and asserts the
   string is in none of `send_dm`, `send_room`, `_nudge_target`,
   `_nudge_window`, `_announce_nudge` (AST function-source segments).

### Repo-wide grep (measured, CORRECT paths)

The DH.21 body quoted `extensions/agi/skills`, which does not exist — skills
lives at repo-root `skills/`. That path was why the run exited 2 and the
`skills/` third of "production paths remain zero" was never measured. Re-run
with the real paths:

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

The string occurs ONLY in the new test file, which must name it to assert its
absence from `send.py`'s caller-facing bodies — not a production path.
Production paths (`extensions/agi/bin`, `extensions/agi/src`, repo-root
`skills/`) are zero.

### Documented dry-run of both transports

- local: `_nudge_target(root, "local-seat", None)` -> `(session:@111, 111,
  session)` with `_window_id_listed` faked True (a real tmux window is never
  touched by the test).
- foreign/mesh: `_nudge_target(root, "far-seat", None)` -> `None` — the
  foreign-box row's window is not addressable here; delivery is gap-filled by
  the remote box's own `mail_poll` tick (`test_box_guard.py:173`).

Both paths ran in the same command and are green.

## Evidence

All transcripts are INLINE in this node (above); no session file is leaned on.

- Test file: `extensions/agi/tests/test_send_surface_ssh_or_not.py`
  (4 tests: the 3 conjunct tests plus `test_real_path_refuses_foreign_box_and_
  reaches_local`, which drives the REAL `send_dm` -> REAL `_nudge_window` ->
  REAL `_nudge_target` with only the tmux/capture layer faked).
- Result: `340 passed, 11 warnings in 35.24s` over this file plus
  `test_box_guard.py` and `test_send.py`.
- DH.25 residue closure: `experiment:send-surface-real-path-and-residues-a00-e2960dc3`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.25 in-place correction. The DH.21 body quoted an exit=1 grep and an exit=2 production grep from a gitignored grep.txt that did not contain those runs, and named extensions/agi/skills (nonexistent; skills is repo-root). Both replaced with inline measured transcripts on the correct paths, and conjunct 2 now points at the new real-path test rather than resting on the _nudge_window stub. Result count updated 339 -> 340.
<!-- THOUGHT:END -->
