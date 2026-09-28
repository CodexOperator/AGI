---
id: hypothesis:a-test-that-writes-a-project-root-resolves-it-from-tmp-path-never-from-inherited-agi-env
mint_id: ee9eda3c8dd94667a88a273904c1259b
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: f8a5b9667b432cfa
season: 2
testable_claim: The test that rewrote a post worktree's config.json and made a nodes/nodes self-loop at 05:03Z 09-28 is named by a scratch-tree repro under a dummy AGI_* env, and after the fix it leaves that scratch tree byte-identical.
title: A test that writes a project root resolves it from tmp_path, never from inherited AGI_* env (TMM.322 leak)
town: core
---
# hypothesis:a-test-that-writes-a-project-root-resolves-it-from-tmp-path-never-from-inherited-agi-env

# hypothesis:a-test-that-writes-a-project-root-resolves-it-from-tmp-path-never-from-inherited-agi-env

## Measured
- 05:03Z 09-28, director-engine post worktree: a pytest run from a shell carrying the seat's AGI_POST / AGI_SEAT left (a) `.agi/config.json` rewritten -- workflows.review / drafting / deep-search `provider: pi-free` -> PAID `pi`, a `drafting.model` deepseek slug added, a `mint.storage_categories` block added -- and (b) a `.agi/nodes/nodes` self-loop. thought-master verified it contained, 0 spend (TMM.322).
- The leaked bytes are NOT a fixture literal: `git grep storage_categories -- extensions/` is empty at 230bf04de, so a test wrote an OLDER / FOREIGN config version over the live tree instead of into its tmp_path.
- Detached systemd units carry no AGI_* (`systemctl --user show-environment` has none); a seat's interactive shell does -- the leak needs the inherited env.

## CLAIM
The test that wrote it is NAMED (file::test, reproduced in a scratch tmpfs worktree with a dummy AGI_* env, the transcript pasted), and fixed so that a test which writes a project root (config.json, nodes/) resolves that root from tmp_path -- never from inherited AGI_* env, cwd, or a git ref of the live tree. Re-running the named test under the same dummy env leaves the scratch tree byte-identical (git status empty).

## Dispatch line
config-max: none (no cell carries a test's root) · template-max: the TESTS line of every brief already scrubs AGI_POST/AGI_SEAT (TMM.322) -- keep, cite · code: the named test's (or its fixture's) root resolution -- the only code.

## FALSIFIERS
- no test reproduces the write under a dummy AGI_* env in a scratch worktree (then say so with the transcript, and name the next suspect: a non-test writer);
- after the fix, the named test under the dummy env still changes any byte of the scratch tree;
- the fix changes a production resolver's behaviour for a real seat.

## TESTS
The named test file + its neighbourhood + test_bin_help_smoke.py, run ONLY in a scratch worktree under /dev/shm (git worktree add --detach), TMPDIR + --basetemp under /dev/shm, with a DUMMY AGI_POST/AGI_SEAT (never a live post name); never in a post worktree or MAIN.

## FILE SCOPE
The named test file and, only if the root resolution lives there, its conftest/fixture · the kid's own node. No production file without naming it OUTSIDE first.

## CEILING
1 kid · 0 production lines · <= 30 test lines net · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. QUEUED behind the EG.9 chain (TMM.322 (1)).
