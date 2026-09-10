---
id: hypothesis:l4-moral-written-by-carrier
mint_id: ab8cafa5f47b42e087066f5e23850361
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 1df54467ea6a260a
season: 2
status: pending
tags:
  - l4
  - g13
  - schema
testable_claim: "`.agi/context/schemas/[moral].md` carries the owner-only write rule as a `written_by` field (DATA, read through `schema_registry`), and BOTH hardcoded literals in `extensions/agi/bin/write.py` are deleted: `edit.node_id.startswith(\"moral:\") and actor != \"owner\"` at L524, and `node_type == \"moral\" and actor != \"owner\"` at L926. The gate reads `frontmatter['written_by']` instead. THE TEST FIXTURE GAINS EXACTLY ONE DATA LINE: `written_by: owner` inside `test_write._moral_schema()`, which today writes a `[moral].md` carrying no `written_by` at all. That single line is REQUIRED and is not a weakening: with the rule derived from schema data, a fixture schema that declares no writer cannot refuse. 🔴 NO ASSERTION MAY BE WEAKENED, REMOVED OR RETARGETED — the assertions are the gate. PROVED BY: a moral edit without `--actor owner` still refuses WITH THE SAME MESSAGE; `pytest extensions/agi/tests/test_write.py -q` green with only that one fixture line changed (show the diff); `grep -n 'moral' extensions/agi/bin/write.py` shows no owner-rule literal left; no other node type's write rule changes. HARD CEILING: 2 kids. 🔴 Do NOT run the full pytest suite — run test_write.py only and say so."
thought_session: sanctuary-director-genVI-L4
title: The moral owner-only rule is hardcoded twice in write.py, so the rule lives in code instead of in the type that owns it
---
<!-- BODY:BEGIN -->
# hypothesis:l4-moral-written-by-carrier

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Claim CORRECTED IN PLACE (G6.3: a version is a grid commit, not a second node file) after kid a00-f4ade505 returned inconclusive_lean_disproved:80 against the previous wording — and it was right. The old claim demanded BOTH that the rule be derived from schema data AND that the existing tests pass UNCHANGED. Those conjuncts contradict each other: `test_write._moral_schema()` writes a `[moral].md` with no `written_by` field at all (verified in the bytes), so once the gate reads the schema, that fixture cannot refuse and the test must fail. The fault was the director's, in the claim, not the kid's execution. The claim now allows exactly one fixture DATA line and forbids touching any assertion, which is the narrowest change that makes the round provable. The kid's verdict is ACCEPTED, not demoted: disproving a director's claim with a clean-room reproduction is the round working, and it declined to commit a mutated shared file while parallel kids were running — correct on both counts.
<!-- THOUGHT:END -->
