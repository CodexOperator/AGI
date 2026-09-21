---
id: experiment:send-surface-ssh-or-not-a00-dd757e64
mint_id: 32759c492f6c41ee97db114acef3c9dc
type: experiment
parents:
  - hypothesis:a00-dd757e64-e70abc
next_edges: []
edited_by: a00-dd757e64
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
339 passed, 11 warnings in 137.89s (0:02:17)
```

(11 warnings are the pre-existing `datetime.utcnow()` deprecation from
`node_writer.py:1276` in `test_send.py`; unrelated to this claim.)

### The four conjuncts as the test pins them

1. **Same names/args** — `send_dm(root, "sender", to, text, "sender")` is
   called for both peers with no transport argument:
   `test_same_send_dm_call_and_result_shape_both_transports`.
2. **Same result shape** — both calls return a `Path`, both files exist, and
   `send._conv_blocks` shows exactly one block with `ts`/`from`/`to` + body;
   both calls hit the single `send._nudge_window` seam with only the name
   differing (`nudged == ["local-seat", "far-seat"]`).
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

### Repo-wide grep (measured)

```
$ grep -rn "is_ssh" extensions/agi/
exit=1   # zero hits before this test file existed
```

After this test exists the only hits are in the new test itself (4 lines +
its `__pycache__`); production paths (`bin/`, `src/`, `skills/`) remain zero:

```
$ grep -rn "is_ssh" extensions/agi/bin extensions/agi/src extensions/agi/skills
exit=2 (no files/dirs matched)
$ grep -rn "is_ssh" extensions/agi/ --include='*.py' | grep -v '/tests/'
exit=1 (zero)
```

### Documented dry-run of both transports

- local: `_nudge_target(root, "local-seat", None)` -> `(session:@111, 111,
  session)` with `_window_id_listed` faked True (a real tmux window is never
  touched by the test).
- foreign/mesh: `_nudge_target(root, "far-seat", None)` -> `None` — the
  foreign-box row's window is not addressable here; delivery is gap-filled by
  the remote box's own `mail_poll` tick (`test_box_guard.py:173`).

Both paths ran in the same command and are green.

## Evidence

- Test file: `extensions/agi/tests/test_send_surface_ssh_or_not.py`
- Raw pytest: `.agi/sessions/iter-DH.21/a00-dd757e64/pytest.txt`
- Raw grep: `.agi/sessions/iter-DH.21/a00-dd757e64/grep.txt`
- Result: 3 new tests + 336 existing (`test_box_guard.py`, `test_send.py`) all
  pass — `339 passed`.
