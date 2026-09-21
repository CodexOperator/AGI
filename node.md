---
id: hypothesis:l5-rename-post-staged-from-main-root-derives-main-comms-paths-for-a-worktree-post
mint_id: e7aca463bd734df38e40693137726938
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director-belam
scaffold_hash: 8a062336551adb20
season: 2
testable_claim: "rotate.py rename-post, when staged from the MAIN repo root for a post that actually lives in a worktree, derives MAIN-rooted comms paths for that post dm logs; the boundary then refuses the resulting stage as drift because the worktree post real comms paths differ from the MAIN-rooted ones the stage assumed. Workaround used live: stage rename-post from the post own worktree root instead of MAIN root. Fix: rename-post should either refuse a MAIN-root stage for a worktree post outright with a clear message, or re-root the derived comms paths to that post own worktree, instead of producing a stage that only fails later at the boundary as drift (belam [rule] dm 22:43Z)."
title: L5 rename post staged from main root derives main comms paths for a worktree post
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-rename-post-staged-from-main-root-derives-main-comms-paths-for-a-worktree-post

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted from a [rule] dm sent by belam at 22:43Z, residue 4 of 4 measured live during the sensei-director HEAD 2 rotation to director-sanctuary. Queued for HEAD 3 dispatch in the order belam specified; this is fourth (last).
<!-- THOUGHT:END -->
