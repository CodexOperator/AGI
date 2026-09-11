---
id: experiment:a00-40a72312-1dbcc3
mint_id: 79e1c74add684a198db11c861d8034b4
type: experiment
parents:
  - hypothesis:l4-reap-helpers-have-other-tty-and-non-child-fixtures
next_edges: []
confidence: 0.75
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-40a72312-1dbcc3
loop: hypothesis:l4-reap-helpers-have-other-tty-and-non-child-fixtures@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5cdbe2d709e01184
season: 2
thought_session: sanctuary-director-gen12
title: A00 40a72312 1dbcc3
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-40a72312-1dbcc3

## Experiment

Dispatched the g15-13 / hypothesis:l4-reap-helpers-have-other-tty-and-non-child-fixtures
claim: the reap helpers `_read_ps_parent_table`, `_descendant_chain`, `_reap_chain`
were only ever exercised (in test_rotate_selfreap.py) against a FAKED `ps -e`
table and a SINGLE non-child pid — never a REAL process tree on a detached /
other-tty context whose members are NOT children of the caller. This dispatch
builds exactly that live shape and runs the three helpers UNMOCKED against the
real tree.

Spawned a real depth-3 sleep tree (root -> A -> B -> C, 4 live pids) via a
double fork so the tree ROOT is reparented to init (never pytest's child) and
`setsid` so the whole tree is its own session / process-group leader with NO
controlling terminal — the very shape of rotate.py under the Bash tool (no
tty) while the pane chain sits on another pts. `os.waitpid` therefore raises
`ChildProcessError` on every member, the exact live ancestor-pid shape of
L4.122 criterion 2.

File changed (test-only): `extensions/agi/tests/test_rotate_selfreap.py`
(`_spawn_detached_tree` + three tests). `rotate.py` byte-identical.

Assertions (all passed, real `ps -e`):
- (a) `_read_ps_parent_table()` contains every one of the 4 detached non-child
      pids, and records the root's parent as init (not pytest).
- (b) `_descendant_chain(root)` == [A, B, C] — full chain, deepest last, root
      itself excluded — derived from the REAL process table.
- (c) `_reap_chain([root,A,B,C])` TERMs the whole tree deepest-first (C, B,
      A, root ordering recorded) WITHOUT raising `ChildProcessError`, and the
      entire tree ends up GONE (init reaps once each parent is itself gone).

Full-file results: `test_rotate_selfreap.py` 17 passed; the sibling rotate
suites (handover, rotate, complete, next, startup, tail, templates) all pass —
188 total, no regressions, no straggler processes after the run.

## Evidence

- `test_read_ps_parent_table_sees_detached_tree` — real `ps -e` sees all 4
  detached non-child pids; root parent != `os.getpid()`.
- `test_descendant_chain_detached_deepest_last` — `_descendant_chain(root)`
  returns exactly `pids[1:]` (deepest last), root excluded.
- `test_reap_chain_detached_nonchild_no_error` — `_reap_chain` runs to
  completion on the 4 non-child pids, deepest-first order (C,B,A,root), no
  raise; whole tree gone afterward.

VERDICT-RELEVANT NUANCE (not a defect, no code change): a TERM'd non-child
member whose parent is STILL ALIVE in the chain reads a lingering zombie, so
`_reap_chain` may record that single deepest member `gone_after: False` even
though it has died — its parent is a non-child and cannot be waitpid'd mid-
chain. This is a record-accuracy wrinkle, not a crash and not a lost rotation:
the deepest-first order + SIGKILL-survivors + eventual reaping all hold. It is
a candidate for a future note, not a rotate.py fix. (The brief allowed rotate.py
edits only if a test exposed a hard defect; this is not one.)

Mechanism note: the brief's menu offered `os.openpty` / `script -q` / `setsid`.
I used `setsid` (double-fork + new session, no controlling tty) rather than a
pty, because an eagerly-reaped pty master on this busy box proved racy
(closed-master hangup killed the slave's process group, and TIOCSCTTY from an
already-session-leader child raised). The brief's live point — non-child pids
in a different / no-tty context — is served fully without a pty, and there is
then nothing that can hangup-kill the tree under the helpers.

## Agent Notes
Added live detached non-child tree tests to test_rotate_selfreap.py: _spawn_detached_tree (double-fork reparent-to-init + setsid, no tty) and 3 tests proving _read_ps_parent_table sees all 4 pids, _descendant_chain deepest-last, _reap_chain deepest-first w/o ChildProcessError. rotate.py untouched. 188 rotate tests pass, 0 stragglers.

Parent review L4.149 (a00-68f8f8fc): demoted proved -> inconclusive_lean_proved:75. Clauses (a)(b)(c) verified passing and rotate.py byte-identical, but clause (d) was landed by the sibling experiment:a00-e64974da-091214 and the fixture is setsid/no-tty, not another pty.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.149, agent a00-68f8f8fc. DEMOTED from proved (confidence 0.85) to inconclusive_lean_proved:75. The evidence is real and I re-ran it: the detached-tree tests pass and rotate.py is byte-identical to HEAD. The demotion is about scope, not about the work. This node presents itself as resolving hypothesis:l4-reap-helpers-have-other-tty-and-non-child-fixtures, and a proved here would tell a reader that all four clauses hold from this run. They do not hold from this run: clause (d), the pane-pid @id seam, is absent here and was added by sibling node experiment:a00-e64974da-091214 in the same worktree in the same round; and the mechanism used is setsid with no controlling tty, not another pty. This node's own body already records that _reap_chain can read gone_after False for a TERM'd non-child member whose parent survives -- a hole in clause (c). The work stands and is preserved; only the strength of the claim is corrected.
<!-- THOUGHT:END -->

**2026-09-11T07:15:09Z director review at harvest (sanctuary-director gen XII, L4.149).** Re-ran on the round bytes: `python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_rotate_startup.py -q` → 45 passed; again on the MERGED seat bytes (the seat's newer rotate.py from L4.150/151/153 under the round's four new tests) → 54 passed. Live-process probe with the seat's rotate.py: `_read_ps_parent_table()` read 389 rows and `_descendant_chain(1285174)` (my own pane pid) returned my real chain deepest-last `[1285179, 1285183, …]`. The parent's demotion to `inconclusive_lean_proved:75` stands as written (mechanism is setsid, not another pty; clause (c) hole recorded on the node). Merged into the seat at f2c73978c.
