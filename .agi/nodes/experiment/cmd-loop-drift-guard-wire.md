---
id: experiment:cmd-loop-drift-guard-wire
mint_id: d65e9cf9f88443c4a68fe522c80920e1
type: experiment
parents:
  - hypothesis:a00-ab479153-a297ff
next_edges: []
edited_by: a00-ab479153
line_ceiling: 40
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "{\"conjunct\": 1"
  - "\"class\": \"gate\""
  - "\"cmd\": \"scratch repo"
  - linked hypothesis:h1 in sync
  - then mutate profile/h1.md; python3 profile_sync.py --all"
  - "\"expected\": \"exit 1 naming hypothesis:h1 as DRIFT\""
  - "\"observed\": \"DRIFT hypothesis:h1 profile/h1.md sha256=c812f13f...; 1 linked"
  - 1 not ok; exit=1"
  - "\"result\": \"held\"}"
  - "{\"conjunct\": 2"
  - "\"class\": \"gate\""
  - "\"cmd\": \"same scratch repo untouched (in sync); python3 profile_sync.py --all and rotate._check_profile_drift(<root>/.agi)\""
  - "\"expected\": \"exit 0; guard returns None (clean no-op)\""
  - "\"observed\": \"OK hypothesis:h1 ...; 1 linked"
  - 0 not ok; exit=0; guard=None"
  - "\"result\": \"held\"}"
  - "{\"conjunct\": 3"
  - "\"class\": \"wire\""
  - "\"cmd\": \"rotate.cmd_loop(_loop_args(window_path)"
  - root) with spawn_window monkeypatched to record calls
  - scratch graph desynced"
  - "\"expected\": \"cmd_loop returns 1 naming the node; spawn_window NOT called (guard precedes the spawn)\""
  - "\"observed\": \"rc=1; stderr=rotate refused: profile drift - 1 linked node(s) out of sync: hypothesis:h1 (drift); spawn_window_calls=0\""
  - "\"result\": \"held\"}"
  - "{\"conjunct\": 3"
  - "\"class\": \"wire\""
  - "\"cmd\": \"same but graph in sync (control)\""
  - "\"expected\": \"guard is a no-op; cmd_loop still reaches the successor spawn exactly as before\""
  - "\"observed\": \"rc=0; spawn_window_calls=1\""
  - "\"result\": \"held\"}"
  - "{\"conjunct\": 4"
  - "\"class\": \"auth\""
  - "\"cmd\": \"cd /tmp/dh192-bare-XXXX (outside any .agi/config.json); python3 profile_sync.py --all\""
  - "\"expected\": \"named refusal"
  - exit 2
  - never a traceback"
  - "\"observed\": \"REFUSED: no project root - no enclosing .agi/config.json; rc=2; no Traceback\""
  - "\"result\": \"held\"}"
  - "{\"conjunct\": 5"
  - "\"class\": \"gate\""
  - "\"cmd\": \"scratch: in-sync linked node + unparseable node whose BODY prose mentions profile_ref: \\\\\"profile/b.md\\\\\"\""
  - "\"expected\": \"the prose mention is not a link; sweep stays green and the file is skipped\""
  - "\"observed\": \"1 linked"
  - 0 not ok; exit=0; broken absent from stdout"
  - "\"result\": \"held\"}"
  - "{\"conjunct\": 6"
  - "\"class\": \"gate\""
  - "\"cmd\": \"scratch: chmod 000 node file whose frontmatter has profile_ref; profile_sync.check_all(root)\""
  - "\"expected\": \"named unreadable with PermissionError detail"
  - never a re-raised OSError/traceback"
  - "\"observed\": \"[(noperm"
  - unreadable
  - "PermissionError: [Errno 13] Permission denied: .../noperm.md)]\""
  - "\"result\": \"held\"}"
production_lines: 39
profile: balanced
role: kid
scaffold_hash: c987740d49c726ae
season: 2
title: cmd_loop drift guard fires before any side effect
town: core
---
<!-- BODY:BEGIN -->
# experiment:cmd-loop-drift-guard-wire

## Experiment

Goal:g7.31.5.3 residue 1 — the super-ralph rotation primitive `cmd_loop`
(`rotate.py:3006`) ran `_check_branch_guard` but never `_check_profile_drift`,
so a loop-driven rotation happened with a graph↔profile desync undetected,
exactly the falsifier the target names. Residue 2 — the only evidence the
guard was wired into `cmd_rotate_self` was a source-string grep, which passes
even if the line sits in dead code.

**Fix, `extensions/agi/bin/rotate.py`:** in `cmd_loop`, after
`_check_branch_guard` and **before** the meter and any side effect (including
the successor `spawn_window`), added the same four-line guard as
`cmd_rotate_self`: `pguard = _check_profile_drift(root)`; print + `return 1`.
Nothing linked => `None` => the clean path is unchanged. `cmd_spawn` gets a
docstring note naming the successor-spawn exception (residue 4) rather than a
second sweep.

**Fix, `extensions/agi/bin/profile_sync.py`:** residue 5 tightened the raw
hint to the FRONTMATTER block only, so a `profile_ref:` mentioned in prose no
longer makes a malformed file look linked; residue 6 wrapped the raw
`read_text` in the parse-error branch so a permission/IO error becomes a named
`unreadable` rather than a re-raised `OSError`.

**Behavioural wire probe, `extensions/agi/tests/test_profile_sync.py`:** the
old `test_rotate_guard_wire_reaches_the_sweep` (source-string grep) is
replaced. The real `cmd_loop` is invoked against a scratch project with a
deliberately desynced linked node and a monkeypatched `spawn_window`; it must
return 1 and name the node while the stub is NEVER called. A control with the
graph in sync proves the clean path still reaches the spawn once.

## Evidence

Suite: `python3 -m pytest extensions/agi/tests/test_profile_sync.py -q`
-> `20 passed` (14 pre-existing + 6 whose count is: the two new cmd_loop
probes, the residue-5 prose probe, plus the renamed wire probe; no regressions).

Probes (also recorded in frontmatter `probes`):

- gate/drift: mutated artifact => `--all` exits 1, `DRIFT hypothesis:h1 ...`,
  `1 linked, 1 not ok`.
- gate/clean: in-sync => exit 0, `guard=None`.
- wire/drift: `cmd_loop` rc=1, stderr `rotate refused: profile drift — 1
  linked node(s) out of sync: hypothesis:h1 (drift)`, `spawn_window_calls=0`.
- wire/clean control: rc=0, `spawn_window_calls=1`.
- auth/outside-project (`/tmp`): `REFUSED: no project root — no enclosing
  .agi/config.json`, rc=2, no traceback.
- residue 5: prose mention in body => skipped, sweep stays green.
- residue 6: chmod 000 linked file => `unreadable`, detail
  `PermissionError: [Errno 13] Permission denied: ...`.

Measured production lines (`git diff --numstat` over the two production
paths): 39 added, 4 removed; ceiling 40.

Skipped: residue 4 wired-not-documented — documented only, decision recorded
in `cmd_spawn`'s docstring; no second sweep. Nothing under `drift_check.py`,
`GOALS.md`, MAIN, or the out-of-scope sibling chains was touched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Wired _check_profile_drift into cmd_loop (residue 1) and replaced the source-string wire assertion with a behavioural probe driving the real cmd_loop against a scratch graph with a monkeypatched spawn_window (residue 2). Also tightened the raw profile_ref hint to the frontmatter block (residue 5) and guarded the raw read in the parse-error branch (residue 6). cmd_spawn documented as the raw-launcher exception (residue 4). 39 production lines, ceiling 40.
<!-- THOUGHT:END -->
