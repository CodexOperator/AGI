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

## CORRECTIVE DH.540 -- closes mur-director-engine-22 DH.533-k1 + DH.533-k2 (verify: DEMOTE x2; every unrefuted residue + missed item batched here)
BASE      CUT FROM season2/loops/hypothesis-clean-kid-worktrees-p-a00-fbd128d3 tip dedc18720 (branch de-base-540). No merge. Never rebase.
KID A -- safety (extensions/agi/bin/heal.py sweep path only):
A1. heal.py:1637-1639 judges dirt from `git status --porcelain`, so IGNORED files are invisible and `git worktree remove` deletes them -> a tree with any ignored or untracked byte is NEVER removed (use --ignored); one test: an ignored file keeps the tree.
A2. heal.py:1643-1648 unguarded json.loads(agent.json) + report.format can raise into the persistent watch loop -> a bad agent.json or a bad report_line cell yields a named line, never an exception; one test each.
A3. heal.py:1643 owner = the lexicographically FIRST agent.json under the tree -> owner = the tree's own agent id (its directory name, a00-*), `?` otherwise.
A4. heal.py:1642 + :1713 count the LIST case into `refused` -> the pass summary prints listed=<n> apart from refused=<n>.
A5. the dirty LIST path never writes _SWEEP_SKIP, so every dirty tree is re-listed every 30 s pass -> list a tree once per dirty set.
A6. heal.py:1941 -> :1680: dry_run_default also silently disables _sweep_bring_home -> bring-home keeps its behaviour at the base f71d1915b; the cell gates ONLY the prune.
KID B -- cells, docs, tests, nodes:
B1. heal.py:1533-1543 reads the worktree_sweep cells only inside `if grace_min is None` -> read them unconditionally.
B2. heal.py:1152 _sweep_worktree_base docstring still says 'no base => NOT removed' -> state the rule the code applies.
B3. heal.py:1584 pre-resolve loop is dead work and :1597's eager default resolves the base twice per tree -> delete the dead loop, resolve lazily.
B4. test_heal_sweep.py:211 asserts the CODE FALLBACK literal -> build the expected line from the cell's report_line.
B5. committed tests (tmp repos) for two gates that rest only on parent probes: a POST worktree is never touched by this sweep; a detached-HEAD kid tree is kept.
B6. nodes via write.py: experiment:a00-067371e8-ce5067 says the round gate did not refuse the config write (the director landed it, dedc18720) and generalises 'strict SUPERSET of OLD' past its three sample rows -> correct both; experiment:a00-58634208-49794c says worktree_sweep 'was a pair of dead cells' (none existed at the base) -> correct.
B7. NEVER touch .agi/config.json: write on your node the FINAL verdict set the code emits; the director rewrites report_line_note and removes the unread sample_n cell at landing.
DEMOTED (no work): M3 armed-off -- the cell IS the ordered switch (config-max); first-3-paths -- a note; the ceiling -- g7.33.19 row 17.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_heal_sweep.py test_heal_sweep_dryrun_census.py test_heal_sweep_prune_predicate.py + test_heal*.py test_worktrees_dir_cell.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp); tmp repos only, NEVER the real sweep, never a live worktree
FILE SCOPE extensions/agi/bin/heal.py (sweep + bring-home seam only) · the three sweep test files · experiment:a00-067371e8-ce5067 · experiment:a00-58634208-49794c (write.py) · the kids' own nodes
CEILING   HARD CAP: 2 kids (A, B) · heal.py net <= 40 lines over the ROUND BASE dedc18720 (measure with git diff --numstat dedc18720) · <= 80 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.540: mur-22 DH.533-k1/k2 verify DEMOTE x2 -- the dirty gate misses ignored bytes (worktree remove deletes them), the watch loop can raise, the dry-run cell also silences bring-home, plus cells/docs/tests/node text; batched into ONE corrective, 2 kids; M3 + first-3-paths demoted with reasons.
<!-- THOUGHT:END -->
