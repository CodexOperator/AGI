---
id: hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary
mint_id: eed308e46a854e049f168c44dc06bffb
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director-belam
scaffold_hash: 429719d827c6e442
season: 2
testable_claim: "After_join join step greps for the OLD post name at a rotation that also renames the post; the live match after rename is only under the .prev window, so join stays unresolved (measured 605s), pin then refuses, and no automatic reap fires -- the Prime reaped the old chain by pid and killed the stuck wrapper by hand (belam [rule] dm 22:43Z, sensei-director to director-sanctuary HEAD 2 rotation). Fix: after_join join should also match the .prev window (or the renamed target name) at a rename boundary, not only the pre-rename name."
title: L5 after join greps the old post name at a rename boundary
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-after-join-greps-the-old-post-name-at-a-rename-boundary

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted from a [rule] dm sent by belam at 22:43Z, residue 1 of 4 measured live during the sensei-director HEAD 2 rotation to director-sanctuary. Queued for HEAD 3 dispatch in the order belam specified; this is first.
<!-- THOUGHT:END -->
