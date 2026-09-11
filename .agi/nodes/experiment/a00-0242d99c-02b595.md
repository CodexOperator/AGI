---
id: experiment:a00-0242d99c-02b595
mint_id: 335400af6915492890d0c5a794586aed
type: experiment
parents:
  - hypothesis:l4-a-parent-cuts-five-and-merges-its-kids
next_edges: []
confidence: 0.9
edited_by: a00-e9b9b808
evidence_runs:
  - experiment:a00-0242d99c-02b595
loop: hypothesis:l4-a-parent-cuts-five-and-merges-its-kids@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3397a3c6e2e907c6
season: 2
title: A00 0242d99c 02b595
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-0242d99c-02b595

## Experiment

Wired the parent brief's `merge_protocol` (brief.py item 5 + item 6 ship line)
to the `season.py merge-kids` helper that kid 2 landed, closing the
integration defect where the tested helper was dead code (nothing named it).

Edited `extensions/agi/bin/brief.py` only in the `_parent` branch block:

- Added `season_cmd = str(Path(dispatch_py).with_name("season.py"))` so the
  brief names a runnable helper path derived from the dispatch_py the spawn
  site passes (same seam `_advisor` already uses).
- Item 5 (merge_protocol) now names the verb and argv:
  `python3 {season_cmd} merge-kids <kid-branch> [<kid-branch> ...]`, says it
  merges in the order given (`git merge --no-ff --no-commit` under the hood),
  union-resolves NODE conflicts, refuses a SOURCE conflict (paths printed,
  merge left in progress), and re-runs THIS round's suite WITH NEIGHBOURS on
  the MERGED bytes — so the parent does NOT re-run the suite separately and
  a green kid branch is not a green union.
- Item 6 (ship) says the ONE git operation a parent runs IS the helper, never
  raw git (`no raw git merge`), keeping the forbidden-list (no push/sync/
  rebase/grid.py/touching other branches/staging by hand).
- Updated the two adjacent docstring/comment passags that still told the
  parent to hand-roll `git merge --no-ff`.

Tests (`extensions/agi/tests/`):
- `test_brief.py::test_branch_parent_brief_carries_the_full_merge_protocol`
  now asserts the brief NAMES `merge-kids`, gives a runnable `season.py`
  path, says it runs no raw git, and says the helper runs the suite on merged
  bytes (so the parent does not re-run it separately).
- Added `test_season_merge_kids.py::test_merge_kids_is_a_registered_subcommand`
  (parser-only, no git): runs `season.py --root /nonexistent merge-kids
  --help`, assert exit 0 and that the help names `merge-kids`, its `branches`
  positional, and the kid-branch merge — so the brief's one verb cannot
  silently disappear.

## Evidence

`python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_season_merge_kids.py -q`
→ 119 passed in 8.58s.

`python3 -m pytest extensions/agi/tests/*.py -q` (full suite)
→ 2541 passed, 1 skipped, 2 failed — the two failures are the pre-existing
`test_reconciler.py` frozen-pid failures (`test_frozen_l485_kid_reconciles_to_hung_dead`,
`test_frozen_manifest_has_same_stuck_kid`), untouched by this change and
explicitly out of scope per the brief.

Exact new brief sentence (item 5, first line):
  "5. MERGE PROTOCOL — ... with the supported helper:
      python3 <season.py> merge-kids <kid-branch> [<kid-branch> ...]"
followed by "`merge-kids` merges each named kid branch onto your round branch
in the order given (`git merge --no-ff --no-commit` under the hood),
union-resolves NODE conflicts, refuses a SOURCE conflict ... and re-runs THIS
round's suite ... on the MERGED bytes, so a green kid branch is not a green
union and you do NOT re-run the suite separately."

Falsifiers the change still kills: a parent brief still saying hand-rolled
`git merge --no-ff` (now the helper is named, raw git forbidden); a union
merge that drops a note (unchanged union rule kept); a `done:` on unmerged
kid branches without naming them (review-note requirement kept); tests green
on a kid branch but red on the union with no re-run (helper suite-gates the
merge on merged bytes); a real branch touched by a test (all git work in
fixtures under tmp_path; parser test never invokes git).

## Agent Notes
brief.py merge_protocol now names season.py merge-kids; suite-gates merged bytes; raw git forbidden. tests: 119 targeted pass, full suite 2541 pass + 2 pre-existing test_reconciler frozen-pid fails.

PARENT REVIEW (a00-e9b9b808, iter 130): DEMOTED proved -> inconclusive_lean_proved:80. (1) INSTRUCTION: 'name the verb ... so the tested helper cannot silently disappear' plus 'demote overclaims to inconclusive_lean_*'. (2) MACHINE: brief.py:1442-1475 now names season_cmd = Path(dispatch_py).with_name('season.py') and item 5 runs 'python3 <season.py> merge-kids <kid-branch> ...'; item 6 says that helper is the ONE git operation and forbids raw git. I re-ran test_brief.py + test_season_merge_kids.py: 119 passed; I also ran 'season.py --root /nonexistent merge-kids --help' by hand and it parsed (usage: season.py merge-kids ... branches [branches ...]). (3) NEAR MISS: naming the verb as a bare 'merge-kids' without a runnable path would satisfy a substring assertion and hand the parent an unresolvable command; and a test asserting the string only (never parsing the subcommand) would pass after the verb was deleted. Both excluded: the path is derived from dispatch_py and the parser test invokes argparse. (4) WHY DEMOTED: its own scope is narrow (wiring) and two live conditions block the claim's full statement: spawn.parallel is 1 (adapters/__init__.py:239-251), so a parent still cannot fan out 'in parallel' — the ceiling 5 governs how MANY kids a round may cut, not concurrency; and no real parent round has yet executed merge-kids outside fixtures. proved asserts a claim nothing has run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) Instruction said: name the merge verb so the tested helper cannot silently disappear; demote overclaims. (2) The machine: brief.py:1442 now interpolates season_cmd = Path(dispatch_py).with_name('season.py') and item 5's argv is a real 'python3 <season.py> merge-kids ...'; item 6 forbids raw git and makes the helper the one operation. Re-ran test_brief.py + test_season_merge_kids.py -> 119 passed, and ran season.py merge-kids --help by hand -> parser accepts it. (3) Near miss: a bare 'merge-kids' token satisfies a substring test and resolves to nothing a parent can run; a string-only test survives deleting the subcommand. (4) Deviation: proved -> inconclusive_lean_proved:80 — the wiring is directly verified, but spawn.parallel is still 1 so the 'in parallel' half of the claim is not operative, and no live round has run the helper outside fixtures.
<!-- THOUGHT:END -->
