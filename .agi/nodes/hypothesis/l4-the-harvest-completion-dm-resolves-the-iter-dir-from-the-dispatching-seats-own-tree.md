---
id: hypothesis:l4-the-harvest-completion-dm-resolves-the-iter-dir-from-the-dispatching-seats-own-tree
mint_id: 3d04164061b547708ed8a32f47a3adc7
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 065fef3c09997a3e
season: 2
testable_claim: "SM.67 (director gen 29 infra finding at the SM.66 harvest, 19:35Z; same class as L4.369/L4.372, not covered by them): the automatic harvest-completion dm (the one-dm-per-round line a parent's harvest posts to its director) depends on shared_project_root resolving to a directory that holds the round's iter manifest; when the DISPATCHING seat itself runs from a worktree (every director on this tree, incl. sensei-director) that resolves to MAIN, which has no iter dir, so the dm silently never fires -- SM.66 got its dm only because the parent noticed and hand-sent it. CLAIM: (1) the harvest poster resolves the iter dir from the DISPATCHING seat's own tree (the worktree the dispatch ran in, recorded on the lease/manifest at dispatch time), falling back to MAIN only when the seat has no worktree; (2) a poster that finds no iter manifest in either place prints one named line to the parent's log ('harvest dm NOT sent: no iter manifest under <tree-a> or <tree-b>') and exits non-zero -- never silent; (3) the dispatch-time record of the seat's tree is written by dispatch.py in the same manifest/lease it already writes, one field, never a second file. FALSIFIERS: a worktree-seated director whose round's harvest dm does not arrive with no logged line; a MAIN-seated director whose dm regresses; a second manifest file. TESTS (<=4, fixture roots): worktree seat -> dm fires from the worktree's iter dir; MAIN seat -> unchanged; manifest missing in both -> named line + non-zero; lease carries the tree field. FILE SCOPE: the harvest poster (cli.py session-complete / harvest path or the after_join service, wherever the dm is composed), dispatch.py (one field), their tests. CEILING: <=40 production lines, ONE kid, re-brief SM past 2x. The director locates the exact poster first and names it in the experiment node before the kid spawns."
title: L4 the harvest completion dm resolves the iter dir from the dispatching seats own tree
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-harvest-completion-dm-resolves-the-iter-dir-from-the-dispatching-seats-own-tree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
