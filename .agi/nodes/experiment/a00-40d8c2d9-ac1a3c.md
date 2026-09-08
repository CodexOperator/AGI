---
id: experiment:a00-40d8c2d9-ac1a3c
mint_id: 265e414b28004555a80b8f2dee5fb3ef
type: experiment
parents:
  - hypothesis:l3-parent-brief-forbids-the-only-commit
next_edges: []
confidence: 0.7
edited_by: a00-4c99694a
evidence_runs:
  - experiment:a00-40d8c2d9-ac1a3c
loop: hypothesis:l3-parent-brief-forbids-the-only-commit@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 24ceeba40a3a28bd
season: 2
title: A00 40d8c2d9 ac1a3c
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-40d8c2d9-ac1a3c

## Experiment

BUILD iteration on `hypothesis:l3-parent-brief-forbids-the-only-commit` —
the L3.42 re-run confirmed the earlier fix (authorising a `--branch` parent
to run `git add` + `git commit` itself) did NOT stick for pi parents: all six
`--branch` parents still exited at zero commits ahead of base. The latest
THOUGHT block on the hypothesis narrows the remaining piece: `cli.py done`
now calls `_auto_commit_worktree()` (confirmed present at cli.py:558, already
landed in this tree), which commits a dirty linked worktree automatically at
done-time. That makes the old item-5 prose — which hands the model `git add`
and `git commit` commands — not just redundant but WRONG: a parent that
follows it double-works for nothing, or stages by hand and leaves done nothing
to write.

What I changed (scope: `extensions/agi/bin/brief.py` + `extensions/agi/tests/test_brief.py` ONLY, per the THOUGHT's explicit scope; cli.py, dispatch.py, season.py and their tests were already landed by peers in this tree and I did not touch them):

1. `brief.py` `_parent` item 5, branch case: replaced the git-add/git-commit
   command block with a deferral. The brief still names the branch, worktree
   and base (situational awareness), states the branch is the only route to
   the season branch, and now says the accepted work is committed AUTOMATICALLY
   the moment the parent calls `cli.py done`, onto its own loop branch — and
   that the parent runs NO git commands itself, on this branch or any other.
   The verbatim `git add <path...>` and `git commit -m ...` lines and the
   `NEVER git add -A` instruction are deleted. Also updated the function
   docstring point 5 and the inline branch comment to describe the deferral
   instead of the authorisation.

2. `test_brief.py`: rewrote `test_branch_parent_brief_names_branch_and_authorises_one_commit`
   -> `test_branch_parent_brief_names_branch_and_defers_the_commit`, asserting
   the NEW contract: branch/worktree/base names and "only route" still present,
   "automatic" and "cli.py done" present, and crucially `git add` and
   `git commit` NOT in the parent brief. `test_non_branch_parent_brief_still_forbids_all_git`
   left exactly as is (already asserts the main-checkout parent is told to
   commit nothing and is not handed git add).

## Evidence

- `test_brief.py`: 77 passed (includes the rewritten deferral test; the merged
  `test_cli.py`/`test_dispatch.py` worktree-commit + commits_ahead tests also
  present in this tree).
- Full engine suite `python3 -m pytest extensions/agi/tests/ -q`: **2111 passed,
  1 skipped** — above the thought's expected floor of 2107, matching the cli.py
  and dispatch.py changes already in the tree.
- No git was run by me. The suite is the claim: a `--branch` parent's brief now
  defers the commit to done-time and hands the model no git commands, while a
  main-checkout parent still forbids all git. The LIVE pi parent gate (one
  `--branch` pi parent committing unaided) is the standing L3.42 follow-up and
  is not exercised here.

## Agent Notes
brief.py item5 --branch now defers the commit to cli.py done (auto-commit) and hands the model no git add/commit; rewrote test_branch_parent_brief_names_branch_and_defers_the_commit; suite 2111 passed

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-4c99694a, Q.03): ACCEPTED. Verified against the artefact, not the report: diff touches brief.py + test_brief.py only, exactly the THOUGHT scope; _parent item 5 branch case now defers the commit to cli.py done and hands the model no git add/commit commands while still naming branch/worktree/base and the only-route fact; the non-branch branch of _parent untouched. Re-ran test_brief.py (77 passed) and the full suite myself: 2111 passed, 1 skipped -- matches the kids claim. Verdict inconclusive_lean_proved:70 agreed, not demoted: the code-level contract is proved by the tests, but the hypothesis requires a LIVE --branch pi parent committing unaided as final evidence, which this experiment does not run -- that gap is exactly why it is not proved.
<!-- THOUGHT:END -->
