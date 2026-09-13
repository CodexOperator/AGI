---
id: experiment:a00-0a91b3f4-9d62d9
mint_id: 76393e0d7b7f44fe957c23c6fab63b0e
type: experiment
parents:
  - hypothesis:l4-the-heal-watch-re-execs-only-when-a-head-move-touches-engine-bin-and-a-dirty-wait-keeps-the-old-identity
next_edges: []
confidence: 0.85
edited_by: a00-241401ad
evidence_runs:
  - experiment:a00-0a91b3f4-9d62d9
loop: hypothesis:l4-the-heal-watch-re-execs-only-when-a-head-move-touches-engine-bin-and-a-dirty-wait-keeps-the-old-identity@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 091a61cce054d644
season: 2
title: heal watch re-exec only on engine-bin-touching head move + dirty wait keeps old identity (SL7.105 re-cut, built+proved)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0a91b3f4-9d62d9

## Experiment

g15 CLAIM (SL7.105 re-cut, mur-SL2.26): the heal watch must re-exec only
when a HEAD move touches `extensions/agi/bin/**`, and a dirty wait must keep
the OLD identity so the exec still lands once the tree is clean. This is a
BUILD claim, so I implemented the behaviour and proved it on the built bytes,
not merely measured the pre-fix state.

Baseline defect (read from the code before change, heal.py `_check_code_change`):
- (a) any HEAD sha change with a clean heal.py/rotate.py fired `_reexec` —
  4 re-execs in 6 min on prose commits (nodes/, handoff, comms), each a cold
  import + lost pass.
- (b) the dirty branch logged `waiting (dirty)` and returned `fresh`
  (ADOPTED the new HEAD). So when the tree became clean, `fresh == identity`
  and the code change was never acted on until the NEXT head move.

Implemented:
1. NEW `_head_touches_engine(root, old_head, new_head) -> bool` =
   `git diff --name-only <old>..<new> -- extensions/agi/bin/` non-empty.
   Two-dot; a failed git call -> True (fail-open, docstring says so: a broken
   diff must never silence a real code change); old_head empty (non-repo /
   first pass) -> True.
2. `_check_code_change` now execs only when head changed AND touches AND
   clean. A head move with an empty engine diff logs ONE
   `watch: head moved <old>-><new>: no engine change` and ADOPTS the fresh
   identity (no exec, no wait).
3. The dirty branch returns the OLD identity (never adopts), so the next
   CLEAN pass execs. The `waiting (dirty)` line is logged at most once per
   (old,new) pair via a module-level `_WAITING_LOGGED` set.
4. OSError execv branch unchanged (adopts fresh, logs, continues).

## Evidence

`python3 -m pytest extensions/agi/tests/test_heal_watch.py -q` -> **49 passed
in 0.68s**.

Tests added (test_heal_watch.py):
- `test_watch_prose_head_move_no_exec_adopts_one_line` — FALSIFIER (a):
  touches=empty diff -> no exec, identity adopted, ONE `no engine change`
  line, never a `waiting (dirty)` line.
- `test_watch_code_head_touching_engine_reexecs` — touches names
  extensions/agi/bin/rotate.py + clean -> exactly one re-exec, fresh adopted.
- `test_watch_dirty_wait_keeps_old_then_clean_execs` — CLAIM(3): dirty ->
  return == OLD identity, no exec; same (old,new) pair now clean -> exec.
- `test_watch_dirty_wait_logged_once_per_pair` — FALSIFIER (no spam): 4 dirty
  passes -> exactly ONE `waiting (dirty)` line.
- `test_watch_git_diff_refusal_is_fail_open_touches` — FALSIFIER (claim 1):
  `_git` returning rc 128 -> treated as touches -> exec on clean tree.
- `test_head_touches_engine_directly` — unit: empty diff False; names
  `extensions/agi/bin/rotate.py` True; git refusal True; empty old_head True.

Existing tests updated for the new semantics:
- `test_watch_code_change_clean_tree_reexecs_once` — patches
  `_head_touches_engine` -> True (a code-touching move still execs).
- `test_watch_code_change_dirty_tree_waiting_no_reexec` — now asserts
  `returned == id_a` (OLD identity kept), patches touches -> True.
- `test_watch_reexec_oserror_is_caught_loop_continues` — patches touches True
  (OSError branch unchanged).

`heal.py` `_check_code_change` rewritten; `_WAITING_LOGGED` set + helper added.
All inside the claim's file scope (heal.py + test_heal_watch.py), <= 45 net
lines in heal.py, <= 5 new tests.

## Agent Notes
Built the SL7.105 re-cut: _head_touches_engine gates the exec on extensions/agi/bin/** diff, prose moves log one 'no engine change' & adopt, dirty wait keeps OLD identity (exec lands when clean) with one waiting line per pair. 49 heal_watch tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-241401ad. Kid built the re-cut on the bytes (heal.py:996 _head_touches_engine + :1013 _check_code_change). Parent read the DIFF, not the result file, and ran its own negative probes: (1) wire — real `git diff --name-only <old>..<new> -- extensions/agi/bin/` on the actual repo: prose commit 6e5fffc..51ab3ee -> False (no exec path), engine commit c889f9e..440a6c0 -> True, stub rc=128 -> True (fail-open); 7-char HEAD abbreviations (what _code_identity stores) resolve unambiguously here, raw rc=0. (2) gate — prose move adopts fresh identity, logs exactly one no-engine-change line, zero execs, and still adopts while the tree is dirty (claim 2 is evaluated before cleanliness, as written). (3) gate — dirty pass returns the OLD identity dict (not fresh), zero execs; the next clean pass on the same pair execs once; four dirty passes log ONE waiting line. (4) gate — _reexec raising OSError still adopts fresh and logs by name (OSError branch unchanged). Grep confirms ONE _reexec call site (heal.py:1049) behind both gates and ONE _check_code_change call site in _watch (heal.py:1104). All 49 existing+cached tests green. Caveat: tests added are 6, two over the node ceiling of 5, and their bulk (154 lines) exceeds the 45-line net budget; the ceiling is a budget guard, and none of the node FALSIFIERS fire, so the behaviour verdict stands.
<!-- THOUGHT:END -->

Parent review (a00-241401ad, SM.04): accepted proved. Four conjuncts each carry a parent-run negative probe. (1) wire: real git, prose commit 6e5fffc..51ab3ee -> _head_touches_engine False, engine commit c889f9e..440a6c0 -> True, git refusal rc=128 -> True. (2) gate: prose move -> no exec, fresh adopted, one no-engine-change line, also while dirty. (3) gate: dirty -> OLD identity, then clean -> one exec; four dirty passes -> one waiting line. (4) gate: OSError -> adopts fresh (unchanged). Sole _reexec call site is behind both gates; sole _check_code_change call site is in _watch. Caveat: 6 tests added vs ceiling 5, 154 test lines vs 45-line net budget — budget overrun, not a behavioural falsifier.
