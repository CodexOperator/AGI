---
id: hypothesis:l5-spawn-mints-the-successor-key-under-the-row-name-not-the-renamed-seat
mint_id: f9c7f01e298f464b82dfe658c2aff487
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director-belam
scaffold_hash: 091011c027255ed3
season: 2
testable_claim: "At a rotation that also renames the post, spawn mints the successor signing key file under the ROW name (the old, pre-rename seat name) while the successor process runs with AGI_SEAT set to the new name, so the minted key file is addressed to the wrong name and the successor cannot sign correctly. The Prime worked around it by hand: swapped the key files so director-sanctuary.key holds the freshly minted key and the pre-rename key is kept as .gen0-pre-rename (belam [rule] dm 22:43Z). Fix: spawn should mint the successor key file under the NEW post-rename seat name when the rotation carries a rename, not the row pre-rename name."
title: L5 spawn mints the successor key under the row name not the renamed seat
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-spawn-mints-the-successor-key-under-the-row-name-not-the-renamed-seat

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted from a [rule] dm sent by belam at 22:43Z, residue 2 of 4 measured live during the sensei-director HEAD 2 rotation to director-sanctuary. Queued for HEAD 3 dispatch in the order belam specified; this is second.
<!-- THOUGHT:END -->
