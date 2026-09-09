---
id: experiment:a00-76bbb729-a84e2a
mint_id: 714307b632624d878a721918e16bb491
type: experiment
parents:
  - hypothesis:l3w4-branch-shared-state
next_edges: []
confidence: 0.6
edited_by: ubuntu
evidence_runs:
  - experiment:a00-76bbb729-a84e2a
loop: hypothesis:l3w4-branch-shared-state@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 39562bffb51fffee
season: 2
title: Worktree shares .env and names the graph fork, built red first
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-76bbb729-a84e2a

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
<Built it, red-first. hypothesis:l3w4-branch-shared-state split out the two isolation leaks at L3.33; I made a real source diff that closes the .env leak and names the graph fork in zoom (the brief's explicit "at minimum name it"). Own code change = 64 insertions / 10 deletions across locations.py, envfile.py, zoom.py + a new test file test_shared_state_worktree.py. DO NOT run git was obeyed; edits are in the main checkout working tree for the director to commit.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted to pending. Body still template placeholder, no experiment summary, no evidence pasted. Claims (shared .env via shared_project_root, zoom naming) lack logs beyond high-level sentence. Code diff unresolved (files edited not reviewed). Need real Experiment/Evidence sections plus paste of failing tests and proof commands before lean can stand.
<!-- THOUGHT:END -->

<EVIDENCE. Red-first: before the fix, all 4 new tests failed (shared_project_root did not exist; zoom refusal read "Fix the graph_core import / target id" instead of naming the fork). After: "4 passed in 0.28s". Full suite: "3 failed, 2018 passed, 1 skipped" -- the 3 failures are in test_sensei.py, the owner's UNTRACKED master-sensei WIP (seats.md fixture lacks dir-g1), independent of this change, same files failing before. My-touched areas (envfile, zoom, locations, dispatch, shared_state): "204 passed". LIVE run quoted verbatim (main checkout = identity, unchanged): $ python3 extensions/agi/bin/envfile.py --what env-file -> /home/ubuntu/work/agi/.env ; $ locations.py --json -> root: .agi. (worktree .env + zoom naming are proven through real git-worktree fixtures in test_shared_state_worktree.py -- those are the live worktree runs).

Parent review pending; reading node now.

REVIEW: Node demoted to pending due to empty body; code diff and tests unreviewed.