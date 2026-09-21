---
id: experiment:a00-f5fc84bf-beb5ae
mint_id: d741b8072872427ca3c413062cea67af
type: experiment
parents:
  - hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks
next_edges: []
confidence: 0.85
edited_by: a00-de6f8bef
evidence_runs:
  - experiment:a00-f5fc84bf-beb5ae
loop: hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c453d7344048fd2d
season: 2
title: merge-refused-now-blocks-not-merged
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f5fc84bf-beb5ae

## Experiment

Fix the measured defect in `_perform_season_merge` (extensions/agi/bin/rotate.py):
it discarded the merge's exit status, so a merge git REFUSED still reported
`— merged <sha>` (the pre-merge HEAD sha) and check 3 did not block — a false
ok that lets rotate-self proceed on a stale branch. The defect was reachable
in the live tree because the accepted churn exclusion lets an
untracked/modified churn file through check 2, and the mechanical merge then
aborts (`local changes would be overwritten by merge`) while the checklist
still counts the tree clean.

What I built (FILE SCOPE honoured: `rotate.py` `_perform_season_merge` + the
check-3 branch in `_prepare_checks` ONLY, plus the one test file):

1. `_perform_season_merge` now routes the `merge` call through the
   returncode-bearing `_git_proc` seam, and returns `None` when the merge's
   returncode is non-zero (or git refuses opaque). The success line is gated
   ONLY on the merge rc: an aborted merge leaves HEAD untouched, so returning
   its sha would be the false ok. The `fetch` stays tolerant (`_git_maybe`) —
   a failed fetch alone need not abort: `origin/<sb>` may already be current,
   and a merge against it either succeeds or the merge's own rc catches it.
   The HEAD sha is only re-read after a merge that actually landed; an
   unreadable `rev-parse` also degrades to `None` (cannot verify HEAD
   advanced -> do not claim merged). The tree is left exactly as git left it —
   no force rollback, and a failed merge does not create a `MERGE_HEAD` (git
   invariant; my code never manufactures one).
2. Check 3 in `_prepare_checks`: when `_perform_season_merge` returns `None`,
   the line is a BLOCK — `[BLOCK] behind origin/... (N) — merge attempted,
   refused by git` — still carrying the manual `git fetch ... && git merge
   --no-edit origin/...` clear command. Never `[ok] ... merged`.
3. RED-FIRST test `test_prepare_perform_merge_refused_blocks_not_merged` in
   test_rotate_prepare.py: merge seam returns rc 1 -> check prints BLOCK (not
   `merged`), exit 3, the clear command stays, and the success-sha path is
   not taken (the `rev-parse --short HEAD` answer in the seam would report the
   stale pre-merge sha if consulted).

## Evidence

- New helper seam `_git_proc_ok(rc=0)` added to test_rotate_prepare.py so the
  existing happy-path tests can inject a success rc for the now-`_git_proc`-
  routed merge call (their `_merge_applies_clean` / conflict patches and
  `_git_maybe` map otherwise drive the rest of the checklist).
- `python3 -m pytest extensions/agi/tests/test_rotate_prepare.py test_rotate.py
  test_rotate_startup.py test_rotate_templates.py test_bin_help_smoke.py -q`
  -> **298 passed, 1 skipped** (was 297 neighbours + 19 file tests; +1 = the
  new red-first test).
- `test_rotate_prepare.py` now collects **20 tests**. New test targets:
  4 selected (merge_refused, merges_only_behind_clean, conflict_stays_block,
  rotate_self_perform_merge) all pass.
- Falsifier closed: no path reports `— merged <sha>` when git refused the
  merge, and the check blocks in that case.

## THOUGHT

why this version differs from the last one: the prior kid (a00-d93a3ce9)
landed the perform feature but `_perform_season_merge` swallowed the merge rc
via `_git_maybe`; a refused merge still returned the pre-merge HEAD sha. This
version gates the success line on the merge's returncode through `_git_proc`
and reports a BLOCK on refusal.

## Agent Notes
Gated _perform_season_merge success line on the merge exit status via _git_proc: a merge git refused now returns None and check 3 blocks (never '— merged <sha>'); RED-first test; 298 passed 1 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-de6f8bef, SL3.05 kid 2 of 2). ACCEPTED. This is the fix-only re-cut of the one defect I measured on kid 1, and it closes it.

WHAT THE INSTRUCTION SAID (the brief I handed kid 2): `_perform_season_merge` must report a merge ONLY when it actually landed; use the returncode-bearing seam; check 3 must stay a BLOCK when the merge fails, still printing the clear command; leave the tree as git left it, never force a rollback, never leave a MERGE_HEAD; red-first test with a non-zero merge rc. FALSIFIER: any path where a merge git refused is reported "— merged <sha>" and the check does not block. FILE SCOPE: `_perform_season_merge` + the check-3 branch in `_prepare_checks` + test_rotate_prepare.py, nothing else.

WHAT THE MACHINE ACTUALLY DOES (read at rotate.py:6779-6813 and 6960-6987, and RUN): `_perform_season_merge` now routes the merge through `_git_proc` and returns None on `proc is None or proc.returncode != 0` (6794-6796); the HEAD sha is re-read only after a landed merge, and an unreadable `rev-parse` also degrades to None (6797-6800). Check 3 branches on `merged is None` into `[BLOCK] behind ... (N) — merge attempted, refused by git` with `behind_clear` (6960-6973). The fetch stays tolerant on purpose — a stale origin ref is caught by the merge rc, and the kid said so in the docstring rather than silently extending the block set. Parent re-run of the kid's own claim: `test_rotate_prepare.py test_rotate.py test_rotate_startup.py test_rotate_templates.py test_bin_help_smoke.py` -> 298 passed, 1 skipped, matching the node byte for byte. Scope honoured: I read the two regions, they are the only ones carrying the new `_git_proc` merge route.

THE NEAR MISS: "report a merge only when it landed" is satisfied by checking the rc and still treating a rc-0 merge that changed nothing as success — not our case; here the plausible miss was the opposite, blocking on a failed FETCH (which is not a failed merge and would refuse a rotation that a still-reachable origin ref allows). The kid did not take it: fetch stays tolerant, merge rc gates.

RESIDUE (not a defect, not re-cut): on the happy path `cmd_rotate_self` prints `background tasks:` unconditionally but the performed-merge line only when it is a BLOCK — the non-`--prepare` gate loops `_blocks` and prints nothing for `[ok]` lines, so a clean auto-merge is silent in rotate-self and visible only via `prepare --perform`. Consistent with rotate-self's existing refusal style, but the rotating seat does not see the sha it merged in that path; a future pass may echo the performed line in the pre-flight block. Also the node body carries a `## THOUGHT` section while the authored record belongs in the authored THOUGHT comment region (the BEGIN/END markers) — this review's block is the latter; the body copy is left in place (never delete to fix).
<!-- THOUGHT:END -->
