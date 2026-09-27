---
id: hypothesis:clean-kid-worktrees-prune-and-dirty-ones-harvest-or-list
mint_id: 913004c875fd47f38641fd969fa9af5f
type: hypothesis
parents:
  - goal:g7.31.3.3
  - hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram
next_edges: []
edited_by: director-engine
scaffold_hash: 4f16fd6ce0dbde55
season: 2
testable_claim: a clean non-live kid worktree whose branch resolves to HEAD is removed with the branch kept; a dirty one commits its write-logged node edits on its kid branch and lists every other dirty path per owner; dry-run is the default; post worktrees are never touched
title: "Clean non-live kid worktrees prune (branch kept) and dirty ones harvest-or-list, dry-run first (owner sweep question 04:4xZ; assigned: director-engine)"
town: local-maxxing
---
# hypothesis:clean-kid-worktrees-prune-and-dirty-ones-harvest-or-list

## Measured
OWNER 04:4xZ 09-27 asked "How is the 92 unharvested worktree sweep going". Director census 04:4xZ: 78 dirty non-live kid worktrees (58 node-only, 20 code); nobody sweeps them. The prune that exists (heal.py _sweep_finished_worktrees ~1524, gates ~1591/1600/1617 unmerged, ~1624 dirty) removes almost nothing: its ancestry base is `base_branch` from the round's agent.json (heal.py:1146 _sweep_worktree_base) -- the branch the round was CUT from -- while a kid's commits land on its PARENT's loop branch and reach the cut branch only at a merge-up, so a finished clean kid reads 'unmerged'. Measurements disagree: a00-f7651b92 says 0/48 (post base), a kid node 2/60, the DH.529 parent's 10-tree probe 6/10 on the engine base. Removing a CLEAN worktree loses no commit while its branch ref exists (`git worktree remove` keeps the branch).

## CLAIM
(1) A kid worktree that is clean, non-live, and whose branch ref exists is prunable (`git worktree remove`, branch kept); the ancestry gate is replaced by 'the branch ref resolves to HEAD', and post worktrees are never touched. (2) A dirty non-live kid worktree is HARVEST-OR-LIST: each uncommitted node file whose bytes == its last write-log sha is committed on the kid branch naming its actor (TMM.268); every other dirty path (unlogged node, code, config) is LISTED in one report grouped by the owning post (from the round's agent.json), never deleted; `--dry-run` is the DEFAULT and prints the census (counts per class + per owner) before anything moves. (3) A RANDOM-sample re-measure (seeded, >= 20 trees) of the old gate vs the new rule is pasted on the kid node, settling 0/48 vs 2/60 vs 6/10.

## Dispatch line
config-max: the dry-run default and the sample size are cells (values.core.worktree_sweep.{dry_run_default, sample_n}) / template-max: the report's line format next to the cell / code: the new prune predicate + the harvest-or-list pass (the trigger that does not exist)

## FALSIFIERS
a dirty or live worktree removed · a post worktree touched · an unlogged edit committed · a removed worktree whose branch did not resolve to its HEAD · the sweep acting without --dry-run first by default · a literal path (use locations.worktrees_root)

## TESTS
one new test file on tmp repos only: clean+branch -> removed and branch kept; clean+no branch -> kept; dirty logged node -> committed on the kid branch; dirty code -> listed under its owner, untouched; live -> untouched; dry-run default moves nothing; plus test_heal*.py test_worktrees_dir_cell.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp). NEVER run the real sweep against the live worktrees dir.

## FILE SCOPE
extensions/agi/bin/heal.py (the sweep predicate + one harvest-or-list function) · .agi/config.json (values.core.worktree_sweep only; if the round gate refuses it, write the exact diff on the kid node) · one new test file · the kid's own node

## CEILING
HARD CAP: 2 kids (1: prune predicate + random re-measure, 2: harvest-or-list + dry-run report) · <= 45 production lines · <= 100 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. BASE: cut from the DH.529 loop tip c93decfda.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version (director-engine): slice 2 of the DH.499 split. OWNER 04:4xZ 09-27, verbatim: "How is the 92 unharvested worktree sweep going". The unmerged gate measures against the cut branch, not where kid work lands; a clean tree with a live branch ref loses nothing on removal, so the gate becomes that. Dirty trees never lose a byte: logged node edits commit (TMM.268), the rest is listed per owner.
<!-- THOUGHT:END -->
