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

## CORRECTIVE DH.563 -- closes mur-director-engine-25 DH.540-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-clean-kid-worktrees-p-a00-c6a30652 tip 357c4b4f2 (branch de-base-563; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. sweep CLI stdout omits the new listed class (heal.py:2017) and no test covers the printed line
2. 2. skip cache no longer saves the git subprocess; the ~5-subprocesses claim at heal.py:1438-1444 is now false
3. 3. node a00-58634208 still claims owner=post / '? when there is none' and shows owner=sensei-director, falsified by its own shipped test
4. 4. two irreconcilable census absolutes reported as agreement (a00-feabefa7: Evidence 3/20 vs parent review 11/20 'agrees')
5. 5. B5 dropped — no committed test for the post-worktree and detached-HEAD gates
6. 6. ignored-directory collapse — the exemption is decided by a directory NAME (heal.py:1289)
7. 7. test budget +121 vs ceiling 80
8. 8. stale mechanism wording in heal.py's own docstring and in two node citations
9. 9. merge commit 357c4b4f2 lands kid- and parent-authored node bytes on a TMM.268 basis that is UNVERIFIED here
10. DEAD READ, and it falsifies a landed node plus the parent's own probe: `_sweep_dirty_owner` returns `str(rec.get("post") or agent_id)` (heal.py:1462), but NO production agent.json has a `post` key — dispatch.py:2940+ builds `agent_record` with `id`, `dispatched_by`, `spawned_by_agent`, `role`, `base_branch`… and `grep -rn '"post":' extensions/agi/bin/*.py` finds only migrate_channel records and cli.py `kind: post`; a real record (.agi/sessions/iter-DH.531/a00-422d2648/agent.json) has no `post`. So the sweep can NEVER name an owning post: the LIST conjunct 'grouped by the owning post (from the round's agent.json)' of hypothesis:clean-kid-worktrees-prune-and-dirty-ones-harvest-or-list is unmet, a00-58634208:51/54 asserts a value the code cannot produce, and the DH.533 parent review at a00-58634208:123 cites 'owner=post-probe-1 read from the round agent.json' from a fixture that invented the key. The available fields are `dispatched_by` / `spawned_by_agent`; either read one or correct the node and the probe claim.
11. A GREEN TEST THAT DOES NOT TEST THE BRANCH IT NAMES: test_heal_sweep_dryrun_census.py:68-69 writes the fixture record as {"agent_id": …, "post": "sensei-director"}, but the code matches on `rec.get("id")` (heal.py:1461). The record therefore never matches and the assertion at :88-90 (`owner=a00-dirty02`) passes through the FALLBACK branch, while the comment directly above it claims 'The OWNER is the tree's own id: a round dir holds SEVERAL seats' records and the first is not it'. No committed test exercises the id-match path at all; the two behaviours are indistinguishable in the suite.
12. STALE CONFIG CELL: .agi/config.json `values.core.worktree_sweep.report_line_note` still reads 'verdict in {removed, refused, kept}'. This diff introduces the `listed` verdict (heal.py:1676, :1752), so the note cell that documents the line format is now wrong, and it is the one place a reader looks for the vocabulary. The cell was not touched by this diff, so the staleness is inherited but caused here.
13. SUMMARY FORMAT NEVER GOT THE TEMPLATE CELL: the hypothesis's dispatch line puts 'the report's line format' in a cell; the per-tree line is (report_line, heal.py:1581) but the per-pass summary is a literal in two places that already disagree (heal.py:1752 with `listed`, :2017 without). One format, two literals, divergent — that duplication is the mechanism behind defect 1.
14. PRODUCTION STATUS CALL LACKS `--no-optional-locks`: the kid's own census (a00-feabefa7 Evidence) used `status --no-optional-locks` with the reason 'a read that cannot refresh an index', but the shipped call at heal.py:1653 is plain `git status --porcelain --ignored`. Combined with defect 2 (now unconditional for every unchanged tree), every 30 s pass takes an index-refreshing status in every leaseless kid worktree — a write-capable read in a pass documented as a census.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_heal_sweep.py test_heal_sweep_dryrun_census.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/heal.py · extensions/agi/tests/test_heal_sweep.py · extensions/agi/tests/test_heal_sweep_dryrun_census.py · .agi/nodes/experiment/a00-067371e8-ce5067.md · .agi/nodes/experiment/a00-58634208-49794c.md · .agi/nodes/experiment/a00-feabefa7-10df7b.md · .agi/nodes/experiment/a00-ffcc01b0-99604b.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 357c4b4f2 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.563: mur-director-engine-25 DH.540-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
