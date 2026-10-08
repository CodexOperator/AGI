---
id: hypothesis:l4-rotate-card-writes-the-post-card-wholesale-and-commits-it-by-path-in-one-call
mint_id: f17f81f422e2432ba592ea06cbc20885
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: 0337313c258833a5
season: 2
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (17:25Z; records sanctuary-director 153415Z: 4 Edits, 162402Z: 3 Edits, director-thought 171903Z: 3 Edits + Read, then git add + commit by hand -- F26 says one wholesale Write and three rotations today ignored it: a fact never beats the habit, the tool must perform the step). CLAIM: a verb `rotate.py card --post <post> [--file F | stdin]` writes the post's quorum card (`<sessions>/quorum/<post>.md`, own worktree copy first per _own_card_path) WHOLESALE from the given bytes and commits it by exact path (`git commit -o -m <msg> -- <card>`, message `<post> card: <first heading or --msg>`) in the SAME call; it refuses by name under MERGE_HEAD or a live suite lock in that tree (the audit commit helper's rule), prints the commit sha, and touches the post's last-act stamp exactly as a card write should NOT (the card write is the act that satisfies the captive, never one that re-stales it: INTERNAL_ENV set for the call); an empty body or a body without the `## ` where-it-stops heading is refused by name (the stops-slot gate would refuse later anyway -- refuse early). FALSIFIERS: a card write that leaves the file uncommitted; a commit under MERGE_HEAD or a live lock; a partial (Edit-style) write; a call that re-stales the post's own captive; an empty/heading-less body accepted. TESTS (<=5, fixture repo + fixture sessions): stdin body -> file bytes identical + one commit touching only the card; --file F same; MERGE_HEAD present -> refusal, no commit, file untouched; live lock -> refusal; heading-less body -> refusal by name. FILE SCOPE: rotate.py (one subparser + one function reusing _own_card_path and the audit commit helper), test_rotate*.py. CEILING: <=30 production lines, 1 kid -- re-brief SM past 2x. Template half (master-sensei): the brief clause beside card-write-LAST reads 'the final card is one call: rotate.py card'; F30 tweak waits on this verb."
thought_session: dissolve-legacy-2026-09-19
title: L4 rotate card writes the post card wholesale and commits it by path in one call
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-card-writes-the-post-card-wholesale-and-commits-it-by-path-in-one-call

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
