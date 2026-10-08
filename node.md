---
id: experiment:a00-2028b756-c4d94a
mint_id: fbe96d75fef74acca19a2c0a5511818d
type: experiment
parents:
  - hypothesis:l3w4-branch-parent-commits
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-2028b756-c4d94a
loop: hypothesis:l3w4-branch-parent-commits@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 665e76fc0a888d3e
season: 2
title: parent owns the worktree commit in cmd_done
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2028b756-c4d94a

## Experiment

Second half of hypothesis:l3w4-branch-parent-commits, per the hook pin of
2026-09-08 (quorum-3/dir-g1): wired the worktree auto-commit into the parent's
one finishing action rather than a new code path — `cli.py cmd_done` (`--owns`
/`--node-id`). The merge-up REFUSAL half was already landed and tested
(experiment:a00-aa35aab2-58d44f); I did not touch `cmd_merge_up`'s zero-ahead
logic.

**Change.** Added `_auto_commit_worktree(root, agent_id, node_id, owns,
verdict)` to `extensions/agi/bin/cli.py` and call it at the end of `cmd_done`,
right before the final status print. Logic (from the pin):

- `checkout = locations.source_root(root)`; `common = locations.git_common_root(root)`;
  checkout's own toplevel via `git -C checkout rev-parse --show-toplevel`.
  No-op (return None) unless root resolves inside a **linked worktree** — i.e.
  `common != checkout-toplevel` — with a non-empty `git status --porcelain`.
- In the worktree-only case: `git add -A` then `git commit -m "<agent_id> done:
  <node_id or owns[0]> verdict=<verdict>"`, with `-c user.email=agi@local -c
  user.name=agi` so it works where no repo-local identity is set.
- On add/commit failure: loud named `ERR: worktree commit ... failed` to
  stderr; the verdict already written is never discarded (same principle
  `cmd_done` applies a few lines above when the schema-fill step fails).
- Never commits in the MAIN checkout or outside git — that is the goal:g4.1
  hazard (`git add -A` in a shared tree sweeps up siblings' uncommitted work).

**Verification — red-first, three tests in `extensions/agi/tests/test_cli.py`:**

1. `test_done_auto_commits_parent_worktree` — a real git main checkout on
   `season/s1` (base commit), plus a linked worktree holding the loop branch
   `loop/slug-abc12345@s2`. Wrote the kid's node UNCOMMITTED in the worktree,
   ran `cli.cmd_done` resolving root to the worktree graph. Asserted the
   branch lands at `rev-list --count season/s1..<branch>` == 1 with a clean
   worktree; then ran `season.py merge-up <branch>` and asserted it exits 0.
2. `test_done_does_not_commit_main_checkout` — the guard: `done` from the
   main checkout leaves main at exactly base (count == 1) with a sibling's
   uncommitted write intact.
3. `_auto_commit_worktree` no-ops cleanly outside git (the other cmd_done
   tests are unaffected).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_cli.py -q` → 11 passed
  (includes the three new tests above, red-first under the old code).
- Full suite `python3 -m pytest extensions/agi/tests/ -q` → **2107 passed,
  1 skipped**.
- The worktree branch that previously reached merge-up at zero commits (and
  was REFUSED, or worse green-merged as nothing) now arrives at base+1 with a
  clean tree and merge-up merges it green.

## Agent Notes
Wired parent worktree auto-commit into cmd_done (cli.py). _auto_commit_worktree: no-op outside a linked worktree; in a worktree, add+commit the kid's uncommitted node write on acceptance. Three new tests in test_cli.py; full suite 2107 passed. merge-up half already landed (a00-aa35aab2).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
parent a00-5b0cb060 crashed silently before reviewing (pid dead, output.log only the model-not-found warning, cli.py done never called). alive reviewed in its place: diffed cli.py by hand, confirmed _auto_commit_worktree guards main checkout and non-git correctly, ran full suite independently (2111 passed, 1 skipped). Accepted as proved.
<!-- THOUGHT:END -->
