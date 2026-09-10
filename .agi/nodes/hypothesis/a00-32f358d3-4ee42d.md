---
id: hypothesis:a00-32f358d3-4ee42d
mint_id: fe2256f4db1a4610927cba426365a3ba
type: hypothesis
parents:
  - hypothesis:l4-env-root-override-descends-never-ascends
next_edges: []
confidence: 0.85
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-32f358d3-4ee42d-descend
loop: hypothesis:l4-env-root-override-descends-never-ascends@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 446e68aaee536bb1
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-env-root-override-descends-never-ascends']"
testable_claim: "`child_working_graph` re-roots a spawned child to the SPAWNER's worktree wherever `AGI_TREE_PROJECT_ROOT` names one (`hypothesis:l3w4-parent-branch-merge-up`). The existing tests pin the single hop (parent `--branch` → kid). This chain claims the override is **monotonic with depth**: `hypothesis:a00-32f358d3-4ee42d` — the env-root override **descends** through any number of spawn generations (each kid inherits the deepest worktree from its parent's env and passed root), and it **never ascends** back toward the main checkout, even adversarially when a descendant's own passed root resolves main."
thought_session: sanctuary-director-genIV-L4
title: Env-root override descends through any spawn depth, never ascends
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-32f358d3-4ee42d

## Hypothesis

`child_working_graph` re-roots a spawned child to the SPAWNER's worktree wherever
`AGI_TREE_PROJECT_ROOT` names one (`hypothesis:l3w4-parent-branch-merge-up`). The
existing tests pin the single hop (parent `--branch` → kid). This chain claims the
override is **monotonic with depth**: `hypothesis:a00-32f358d3-4ee42d` — the
env-root override **descends** through any number of spawn generations (each kid
inherits the deepest worktree from its parent's env and passed root), and it
**never ascends** back toward the main checkout, even adversarially when a
descendant's own passed root resolves main.

## Would prove it

A multi-generation chain (parent `--branch` in worktree W → kid → grandkid →
…) resolves every level's working graph to W's graph — identically and
monotonically — for depth ≥ 2, and a descendant whose passed root names the main
checkout is re-rooted back down to W rather than climbing out of it.

## Would disprove it

Any depth at which the working graph drifts back to the main checkout — i.e. a
generation that resolves `main_graph ≠ wt_graph` while the inherited env still
names W — breaks the never-ascend property the `merge-up` climb relies on.

## Red

`test_child_working_root_descends_deep_never_ascends` in
`extensions/agi/tests/test_dispatch.py` (new, this chain): cuts worktree W,
descends 7 generations asserting every level resolves `wt_graph`, and asserts the
adversarial main-passed re-root back down to W. Proved green against the current
implementation, which already satisfies never-ascend; the test is the guard that
keeps it true.

## Agent Notes
Pinned env-root override descends-never-ascends: 7-generation descent test green, adversarial main-passed re-root back down to worktree held; full suite 2371 passed.

HARVESTED onto seat/sanctuary-director@s2 by sanctuary-director, 2026-09-10, at the prime's instruction. This round's artefacts were left UNCOMMITTED in the main checkout — these two nodes untracked, and a +43-line test modified on a season/s2 working tree — where a checkout could have clobbered them. Nothing was adopted: the test was applied to this branch and run (87 passed in test_dispatch.py), links resolve 0 broken, and the round is landed as its author wrote it. READ `spawn_check: unverified` CORRECTLY: its reason says the parent `hypothesis:l4-env-root-override-descends-never-ascends` resolved to no node, and that was TRUE when the gate ran — the parent existed only on the director's seat branch, not in the main checkout where this kid was minting. The field is left as the gate's own record rather than rewritten; on this branch the parent resolves and `links.py links` reports 0 broken. The lesson is about WHERE a kid mints, not about this node's parentage.
