---
id: hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement
mint_id: 23d672de656142919f5bb0f56d13a24d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-kid-tier-gate-is-not-clearable-from-inside-a-kid
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 532edddffd218649
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (viii) four kids this session read a g15 CLAIM as a hypothesis to test and wrote `disproved`/measurement-only nodes without building: L4.147, L4.158 kid 1, L4.161, L4.172 kid 1 (each cost a second kid or a fix-only round). CLAIM: the kid brief (brief.py, the kid instruction list) carries the sentence 'A g15 CLAIM IS BEHAVIOUR TO BUILD, not a hypothesis to measure: measure the pre-fix state, IMPLEMENT the claim, then prove it on the built bytes' (LANDED by the director at 09:1xZ in this seat, test_brief green); the parent brief's review rule says a measurement-only kid node under a g15 target is re-cut with 'THIS KID MUST IMPLEMENT THE FIX' before the parent reports; a test asserts both sentences for tier=kid / tier=parent. FALSIFIER: a kid brief for a g15 target without the sentence. CEILING: 1 kid (the parent-brief half + test; the kid sentence is landed). FILE SCOPE: brief.py (those two paragraphs) + test_brief.py."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: the kid brief states that a g15 CLAIM is behaviour to BUILD (measure pre-fix, implement, prove) — a measurement-only node is not a round
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (viii) four kids this session read a g15 CLAIM as a hypothesis to test and wrote `disproved`/measurement-only nodes without building: L4.147, L4.158 kid 1, L4.161, L4.172 kid 1 (each cost a second kid or a fix-only round). CLAIM: the kid brief (brief.py, the kid instruction list) carries the sentence 'A g15 CLAIM IS BEHAVIOUR TO BUILD, not a hypothesis to measure: measure the pre-fix state, IMPLEMENT the claim, then prove it on the built bytes' (LANDED by the director at 09:1xZ in this seat, test_brief green); the parent brief's review rule says a measurement-only kid node under a g15 target is re-cut with 'THIS KID MUST IMPLEMENT THE FIX' before the parent reports; a test asserts both sentences for tier=kid / tier=parent. FALSIFIER: a kid brief for a g15 target without the sentence. CEILING: 1 kid (the parent-brief half + test; the kid sentence is landed). FILE SCOPE: brief.py (those two paragraphs) + test_brief.py.

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.175, 2026-09-11 09:37Z). Kept kid 2's proved (0.97) as the round of record and the parent's re-cut of kid 1 (glued line caught on RENDERED bytes, not the kid's report -- exactly the review rule this node asks the parent brief to carry). Ran myself: `pytest test_brief.py test_dispatch.py test_commands.py -q` on the round bytes -> 245 passed; test_brief.py on the merged seat bytes -> green. Real render, `brief.assemble(tier=...)` with the test's fixture args, pre-fix seat bytes vs round bytes: parent brief "THIS KID MUST IMPLEMENT THE FIX" False -> True; glued ").4. DO NOT" False -> False; clean "measurement).\n4. DO NOT" False -> True; kid brief "BEHAVIOUR TO BUILD" True -> True (the kid half was already landed). Both halves of the claim now hold in the rendered briefs, pinned for tier=kid and tier=parent. Residue: none.
