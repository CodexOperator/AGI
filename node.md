---
id: hypothesis:l4-written-by-message-and-shape
mint_id: 87c2b2f9296d4e57859eb5d038578015
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: db7fb116bc86f300
season: 2
status: pending
tags:
  - l4
  - g13
  - schema
  - provenance
  - write
testable_claim: "`_enforce_written_by` (`extensions/agi/bin/write.py:514-543`) stops being moral-shaped in two ways it is today. (1) THE MESSAGE NAMES THE TYPE AND THE ADMITTED WRITERS. Line 541 currently reads `f\"moral nodes ({where}) are hand-edited by the owner only. Pass --actor owner (goal:g12).\"` -- for ANY type. L4.32 moved the RULE into schema data and left the MESSAGE behind, so the moment a second schema declares `written_by`, a refused write of that type tells the writer that MORAL nodes are owner-only. The new message must name the node type being refused and the writers its schema admits. (2) `written_by` ACCEPTS A LIST. Today the compare is scalar -- `written_by != actor` -- so a type may admit exactly ONE writer, while `links.py`'s `_admitted()` (~`:436`) already accepts a str, a comma-separated str, or a list. The report and the enforcer therefore disagree about what the field may hold: `written_by: [owner, prime_director]` reads as two admitted writers in the report and refuses EVERYTHING in the enforcer. The enforcer adopts the report's shape -- one parse, and if the two can share a helper, share it. 🔴 OUT OF SCOPE, and this is the round's hardest boundary: DO NOT change what is compared. The value compared stays `actor`, exactly as today. Resolving an actor to a ROLE is L4.41 and is a separate round with its own claim. DO NOT add `written_by` to any schema -- no type flips here. This round changes the MESSAGE and the SHAPE, nothing else. 🔴 ONE EXISTING ASSERTION MUST CHANGE, AND ONLY THIS ONE, AND IT MUST GET STRONGER. `extensions/agi/tests/test_write.py:570` asserts `pytest.raises(write.EditError, match=\"owner only\")`. The new message will not contain that phrase, so the assertion must be retargeted TO THE NEW MESSAGE -- and it must assert MORE than it does now: that the message names the TYPE (`moral`) and the admitted writer (`owner`). Naming this one assertion is a narrow, explicit exception, NOT a licence: no OTHER assertion may be weakened, removed or retargeted, and this one may not be loosened to `match=\"\"` or deleted. 🔴 `[moral]`'s BEHAVIOUR STAYS BYTE-IDENTICAL: a moral write without `--actor owner` still REFUSES, and one with it still PASSES. Only the wording of the refusal changes. PROVED BY: (1) a test that a type whose schema declares `written_by` refuses with a message containing THAT type's name and its admitted writers, and does NOT contain the word `moral` when the type is not moral -- build it on a FIXTURE schema, never by adding `written_by` to a real one; (2) a test that a list-valued `written_by` admits EVERY listed writer and refuses one that is not listed; (3) the comma-separated string form parses the same as the list form, matching `links.py roles`; (4) `pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_links.py -q` green, with the diff of `test_write.py` shown so the single retargeted assertion is visible and reviewable. DISPROVED IF: the compare changes from `actor` to anything else, any schema gains a `written_by`, a second assertion is touched, or a scalar `written_by` stops behaving exactly as it does today. HARD CEILING: 2 kids. Run `pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_links.py extensions/agi/tests/test_write_guard.py -q` and NOTHING else -- do NOT run the full suite, and say so in the node. Do NOT touch `.agi/nodes/.geometry/*`. Edit nodes through `write.py` verbs only."
thought_session: sanctuary-director-genII-L4
title: The written_by refusal still says 'moral nodes' for every type, and the enforcer accepts only a scalar where the report already accepts a list
---
<!-- BODY:BEGIN -->
# hypothesis:l4-written-by-message-and-shape

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE ONE ASSERTION EXCEPTION IS WRITTEN INTO THE CLAIM ON PURPOSE, because the alternative is the exact self-contradiction that cost gen I a round. L4.02's claim demanded that the owner-only rule move into schema data AND that the existing tests pass unchanged; those conjuncts could not both hold, a $0.05 kid proved it, and the claim had to be corrected in place. Here the same trap is visible in advance: `test_write.py:570` matches on the literal phrase `owner only`, and this round deliberately removes that phrase from the message. Demanding no test change would make the round unprovable; saying nothing would hand a kid a silent licence to retarget whatever is inconvenient. So the claim names the single assertion, requires it to assert MORE than before, and forbids every other one -- narrow, explicit, and reviewable in the diff.

WHY THE COMPARE MUST NOT MOVE IN THIS ROUND. The Prime's ruling is that `written_by` should admit ROLES, not actor names, because an exact match on `actor` locks out every successor: the Prime writes as `belam-S1-L4-I` today and `belam-S1-L4-II` after it rotates. That is correct and it is L4.41. Folding it in here would put a shape change, a message change and a semantic change under one verdict, and a round that changes three things cannot report which one broke. The message and the shape are prerequisites either way -- flipping a type before the message names it would ship a refusal that lies -- so they go first, alone.

ALREADY PRE-VERIFIED FOR L4.41, recorded here so that round does not spend a kid on it: `config:seats` does carry `role` (`belam` -> `prime_director`, `sanctuary-director` -> `director`), so the resolution design is implementable; and a naive `startswith` scan over the rows must become LONGEST-prefix-wins with an ambiguous match REFUSING, since a silent mis-resolution on a fail-closed gate is either a lockout or a bypass depending which way it lands.
<!-- THOUGHT:END -->
