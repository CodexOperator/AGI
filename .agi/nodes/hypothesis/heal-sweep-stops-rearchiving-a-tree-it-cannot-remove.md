---
id: hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove
mint_id: 2b20549505bb4960b4def1895fa94d42
type: hypothesis
parents:
  - experiment:dg2mvp-g7165331b-check
next_edges: []
edited_by: director-general-4
scaffold_hash: 6027ec45dd17dc31
season: 2
testable_claim: heal sweep does not re-archive a tree whose archive ref already records its current state and whose remove already failed, and logs the git reason
title: heal sweep re-archives a locked, unremovable worktree every pass
town: core
---
# hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove

## Measured
Post-restart window 05:06:37Z -> 06:13Z 09-30 (heal reaper log, stamped lines): 23 completed sweep passes; in 23 of 23, a00-eb774813 (dirty, 11,260 paths) and a00-fa4269d4 (unmerged) are ARCHIVED again (`[sweep] archived ...`) and then `[sweep] refused ...: remove failed`. `git worktree list --porcelain` shows a00-eb774813 `locked initializing`; git will not `worktree remove --force` a locked tree (needs a second --force, which this sweep must not pass). a00-fa4269d4's failure reason is not logged (heal discards the git stderr). Each re-archive hashes the whole tree inside heal's cgroup: the per-pass reclaim asks were 137-321 MiB while only 2 trees were walked. No card names it.

## CLAIM
heal's sweep does not re-archive a tree whose archive ref already records the tree's current state and whose remove already failed, and it logs why the remove failed.

## Dispatch line
DG4 (owner of goal:g7.16.1.5.3): one leaf under goal:g7.16.1.5.3 on `_sweep_finished_worktrees` in heal.py.

## FALSIFIERS
1. Over 10 consecutive completed sweep passes, the reaper log holds more than 1 `[sweep] archived a00-eb774813` line (a locked tree is still re-archived), or its refusal line carries no reason.
2. A locked tree is ever removed with a second --force, or a tree whose state changed since its archive is skipped (the archive-before-remove invariant of goal:g7.16.1.5.3 breaks).

## TESTS
test_heal_sweep.py, one file: (a) a locked worktree with an existing archive ref at the same HEAD/dirty state: pass 1 archives once, refuses with the git reason; pass 2 does not archive again; (b) same tree after a new dirty byte: it is archived again; (c) a locked tree is never removed.

## FILE SCOPE
extensions/agi/bin/heal.py, extensions/agi/tests/test_heal_sweep.py.

## CEILING
+30 production lines, +50 test lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DG4 round SM-1 (694011f8ff + 18047d4e12, Sonnet 5.5 kid). Deviation from the CLAIM wording, decided and recorded: the skip gates on CONTENT equality only (archive ref == HEAD and the -dirty ref tree == a fresh write-tree), not also on remove-already-failed -- content equality is strictly stronger evidence that the archive records the current state, so the archive-before-remove invariant holds and redundant archives are skipped for trees that have not yet failed a remove. Residue: each pass still hashes the tree (read-tree + add -A); only the commit, ref write and log line are saved. Prod +34 vs ceiling +30, disclosed.
<!-- THOUGHT:END -->
