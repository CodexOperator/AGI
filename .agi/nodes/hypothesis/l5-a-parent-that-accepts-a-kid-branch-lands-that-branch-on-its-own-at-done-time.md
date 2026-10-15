---
id: hypothesis:l5-a-parent-that-accepts-a-kid-branch-lands-that-branch-on-its-own-at-done-time
mint_id: e53df3d9bd854fd08e10cebebbfd4cc1
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 0537f39fa1dd09e8
season: 2
testable_claim: "(1) cli.py _auto_commit_worktree (~L2136, the one-hand-one-path hook wired by hypothesis:l3w4-branch-parent-commits) today commits only the parent's OWN dirty worktree at done-time; when the accepted artefact is a KID's separate --branch worktree the parent's tree is clean, nothing is committed, and the parent branch reads exactly its fork point. (2) MEASURED (director-sanctuary 23:59Z, SM.125 parent a00-7bbd1556 iter 129): DM said accepted=3, parent tip d7e42300b = its fork point, zero commits ahead; each kid's work (a00-0604d6ec / a00-cb24707f / a00-a2fdcdc5) sits only on its own branch; the parent's review was real (4 adversarial probes in its THOUGHT, kid3's 17 + 93 tests reproduced) -- the harness lost the harvest, not the agent; the SM.125 harvest went by hand as an orphan-kid round, the expensive route this hook exists to remove. (3) FIX: at cmd_done --owns <node>, when the owned node's agent id was dispatched under its own --branch (resolved from that iteration's manifest.json branch/worktree fields, the same manifest cmd_done already reads), the finishing action runs git merge --no-ff <kid-branch> into the parent's own checkout before committing its own direct edits; a kid dispatched without --branch, or a merge that conflicts, leaves today's path byte-identical and names the conflict (never a partial merge). (4) TESTS (red-first, test_cli.py beside the l3w4 test): two sibling --branch kid worktrees each with one real commit, parent worktree clean, cmd_done --owns <kid-B-node-id> -> the parent's branch lands at base+1 carrying kid B's commit (today: base+0); --owns <kid-A> then <kid-B> -> base+2; a kid without --branch -> unchanged from today; a conflicting kid branch -> refused by name, parent branch untouched. FILE SCOPE: extensions/agi/bin/cli.py (_auto_commit_worktree + the manifest lookup), extensions/agi/tests/test_cli.py. CEILING 14 production lines."
thought_session: dissolve-legacy-2026-09-19
title: "SM.130 (director-sanctuary [red] 23:59Z, SM.125 harvest; g15): cmd_done --owns merges an accepted kid's own --branch into the parent's checkout, so a multi-kid parent that picks a winner never finishes at base+0 -- the second cause of the zero-commit-branch symptom after l3w4-branch-parent-commits"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-parent-that-accepts-a-kid-branch-lands-that-branch-on-its-own-at-done-time

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
