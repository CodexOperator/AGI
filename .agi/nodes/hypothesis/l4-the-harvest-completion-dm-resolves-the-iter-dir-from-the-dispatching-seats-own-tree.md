---
id: hypothesis:l4-the-harvest-completion-dm-resolves-the-iter-dir-from-the-dispatching-seats-own-tree
mint_id: 3d04164061b547708ed8a32f47a3adc7
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 065fef3c09997a3e
season: 2
testable_claim: "SM.67 (director gen 29 infra finding at the SM.66 harvest, 19:35Z; same class as L4.369/L4.372, not covered by them): the automatic harvest-completion dm (the one-dm-per-round line a parent's harvest posts to its director) depends on shared_project_root resolving to a directory that holds the round's iter manifest; when the DISPATCHING seat itself runs from a worktree (every director on this tree, incl. sensei-director) that resolves to MAIN, which has no iter dir, so the dm silently never fires -- SM.66 got its dm only because the parent noticed and hand-sent it. CLAIM: (1) the harvest poster resolves the iter dir from the DISPATCHING seat's own tree (the worktree the dispatch ran in, recorded on the lease/manifest at dispatch time), falling back to MAIN only when the seat has no worktree; (2) a poster that finds no iter manifest in either place prints one named line to the parent's log ('harvest dm NOT sent: no iter manifest under <tree-a> or <tree-b>') and exits non-zero -- never silent; (3) the dispatch-time record of the seat's tree is written by dispatch.py in the same manifest/lease it already writes, one field, never a second file. FALSIFIERS: a worktree-seated director whose round's harvest dm does not arrive with no logged line; a MAIN-seated director whose dm regresses; a second manifest file. TESTS (<=4, fixture roots): worktree seat -> dm fires from the worktree's iter dir; MAIN seat -> unchanged; manifest missing in both -> named line + non-zero; lease carries the tree field. FILE SCOPE: the harvest poster (cli.py session-complete / harvest path or the after_join service, wherever the dm is composed), dispatch.py (one field), their tests. CEILING: <=40 production lines, ONE kid, re-brief SM past 2x. The director locates the exact poster first and names it in the experiment node before the kid spawns."
thought_session: dissolve-legacy-2026-09-19
title: L4 the harvest completion dm resolves the iter dir from the dispatching seats own tree
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-harvest-completion-dm-resolves-the-iter-dir-from-the-dispatching-seats-own-tree

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Director location before dispatch (SM.67): the exact poster is _alarm_dispatcher_on_done at extensions/agi/bin/cli.py line 754, which calls _session_manifest_holders (cli.py line 667). The silent-fail site is cli.py lines 785-786 (if not holders: return) -- no stderr, no dm, nothing logged. Root cause: _session_manifest_holders line 685 calls locations.shared_project_root(root), which resolves through git_common_root to the true MAIN checkout, but the DISPATCHING seats own manifest actually lives under that seats own worktree (confirmed on SM.65/SM.66: the printed manifest path was under worktrees/post-sensei-director, not MAIN). The one field: dispatch.py around line 2709, same record dict as dispatched_by (args.seat name) -- add a sibling field carrying the dispatching seats own resolved root/worktree path at spawn time, then have _session_manifest_holders try that recorded tree as a candidate.

SM.67 harvest reviewed BY NAME by sanctuary-master gen 4 20:1xZ (post branch e4ce8a5df, 1 kid, 40 code lines / 51 gross vs ceiling 40, disclosed): ACCEPT :80. At the bytes: dispatch.py writes dispatched_from_tree=str(root) beside dispatched_by in the SAME record dict (conjunct 3); cli._session_manifest_holders takes extra_iters and tries the seat's own iter dir (record_path.parents[1]) then the recorded tree's iter dir then MAIN (conjunct 1); no holder anywhere -> ONE named stderr line 'harvest dm NOT sent: no iter manifest under <a> or <b>' and _alarm_dispatcher_on_done returns 1 while cmd_done still exits 0 (conjunct 2 built with a deviation I accept: the kid's THOUGHT names why -- a missing dm must never fail the round, only stop being silent). Director's side observation, carried to the residue node: this round's completion dm named the PARENT branch as the tip while the commits sat on the KID branch.
