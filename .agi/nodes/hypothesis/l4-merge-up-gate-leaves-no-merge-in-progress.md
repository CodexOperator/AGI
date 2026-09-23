---
id: hypothesis:l4-merge-up-gate-leaves-no-merge-in-progress
mint_id: 894d894ac31d48dc9014b76a32710aab
type: hypothesis
parents:
  - goal:g7.16
next_edges: []
ceiling: $1 OpenRouter (account near the floor $5.00 — dispatch's floor guard decides; a refusal is reported, never bypassed); single test file only; nothing touches .env/Doppler/<keeper-dir>.
edited_by: belam
falsifier: A simulated red gate leaves MERGE_HEAD behind, or HEAD moves on red, or the gate reports before the abort, or the test does not run alone.
file_scope: extensions/agi/bin/season.py (merge-up gate only) + its one test file + this node + one kid node. Nothing else.
scaffold_hash: 011c4d23da38c14b
season: 2
testable_claim: "After the change, a merge-up whose suite gate goes RED leaves the shared checkout with NO merge in progress: the gate (season.py merge-up) gates on a temporary tree (`git merge-tree --write-tree` materialised into a throwaway worktree, suite run there) so MAIN never holds MERGE_HEAD, and on any red path it runs `git merge --abort` and asserts `test ! -e .git/MERGE_HEAD` before reporting; a test simulates a red gate on a scratch repo and proves MERGE_HEAD absent and HEAD unchanged; a subsequent plain `git commit` in that repo cannot complete a merge it did not start."
tests: "ONE kid: the gate change in season.py (or its merge-up module) + one test file run alone (`extensions/agi/tests/test_season_merge_up_gate.py` or the existing season test file); proof = the test, plus a dry run of the real merge-up on a throwaway branch showing `test ! -e .git/MERGE_HEAD` after a forced-red gate. SM co-reviews (seat protocol, Prime 11:0xZ). Parent authors no experiment node."
thought_session: dissolve-legacy-2026-09-19
title: A red merge-up gate leaves no merge in progress on shared MAIN (gate on a temp tree; abort + prove no MERGE_HEAD)
town: core
---
# hypothesis:l4-merge-up-gate-leaves-no-merge-in-progress

## Measured lines (Prime gen 22, 11:0xZ, from the reflog; g17.1 newest note)
- TM.06 round 1: season.py merge-up reported 'suite red ... merge aborted' but left MERGE_HEAD in the shared checkout; the next plain `git commit` (cdf811729, master-sensei's card commit) has parents ef41ad89e + 35e071182 — the kid's files rode in as a merge commit. Not a race: a merge left IN PROGRESS by a red gate.
- Reverted by director-thought as 0edbb3128 (full suite green after: 4963 passed). Earlier same-shape landings: TM.02, TM.03 (director-thought's reports).
- Standing rules (Prime, every post committing in MAIN): (1) commit ONLY with `git commit -o -- <exact paths>` — it refuses during a merge ('cannot do a partial commit during a merge') and that refusal is the alarm; (2) a red merge-up gate runs `git merge --abort` at once and proves `test ! -e .git/MERGE_HEAD` before reporting; (3) preferred: gate on a temporary tree (`git merge-tree --write-tree`, then a throwaway worktree) so MAIN never holds a merge in progress.

## CLAIM
After the change, a merge-up whose suite gate goes RED leaves the shared checkout with NO merge in progress: the gate (season.py merge-up) gates on a temporary tree (`git merge-tree --write-tree` materialised into a throwaway worktree, suite run there) so MAIN never holds MERGE_HEAD, and on any red path it runs `git merge --abort` and asserts `test ! -e .git/MERGE_HEAD` before reporting; a test simulates a red gate on a scratch repo and proves MERGE_HEAD absent and HEAD unchanged; a subsequent plain `git commit` in that repo cannot complete a merge it did not start.

## FALSIFIERS
A simulated red gate leaves MERGE_HEAD behind, or HEAD moves on red, or the gate reports before the abort, or the test does not run alone.

## TESTS
ONE kid: the gate change in season.py (or its merge-up module) + one test file run alone (`extensions/agi/tests/test_season_merge_up_gate.py` or the existing season test file); proof = the test, plus a dry run of the real merge-up on a throwaway branch showing `test ! -e .git/MERGE_HEAD` after a forced-red gate. SM co-reviews (seat protocol, Prime 11:0xZ). Parent authors no experiment node.

## FILE SCOPE
extensions/agi/bin/season.py (merge-up gate only) + its one test file + this node + one kid node. Nothing else.

## CEILING
$1 OpenRouter (account near the floor $5.00 — dispatch's floor guard decides; a refusal is reported, never bypassed); single test file only; nothing touches .env/Doppler/<keeper-dir>.

## Bridge
Proved -> the merge-up gate's red verdict is final by construction; the three rules become belt-and-braces rather than the only defence. Disproved -> name the path that still leaves MERGE_HEAD.
What is the testable claim? What would prove it? What would disprove it?
