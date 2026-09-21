---
id: hypothesis:a00-edae0fba-940d3a
mint_id: f92d3a2537d14e7b9f11d4732bda767d
type: hypothesis
parents:
  - goal:s31
confidence: 0.0
edited_by: season.py
scaffold_hash: 19458dca89a121d7
season: 1
testable_claim: If node_writer.write_node seeds the schema-required title and testable_claim from dispatch-time context, the scaffolded hypothesis passes [hypothesis] required-field validation at birth, and completion.is_complete still returns False on the untouched scaffold and True once the body is filled.
thought_session: season
title: Seeding title+testable_claim at scaffold time makes hypothesis nodes schema-valid at birth
verdict: pending
---

# hypothesis:a00-edae0fba-940d3a

## Hypothesis

**Testable claim:** Seeding `title` and `testable_claim` fields in the scaffold frontmatter from dispatch-time context (target goal id, agent iteration tag) makes scaffolded hypothesis nodes schema-valid at birth, without altering the kid's ability to fill the body or breaking `completion.is_complete`'s reliance on `scaffold_hash`.

**Proved by:**
1. Scaffold a hypothesis through the normal dispatch path with a modified `node_writer.write_node` that populates `title` and `testable_claim`.
2. Validate the resulting node file against `[hypothesis].md`'s `required` list — all required fields present, schema passes.
3. Confirm `completion.is_complete` returns `False` on the untouched scaffold (hash matches) and `True` after a kid fills the body section — completion detection unaffected.
4. The kid's body content (the paragraphs under `## Hypothesis`) is not constrained by the frontmatter seed values and can freely contradict or extend them.

**Disproved by:**
- Any required field from the schema remains absent after scaffolding.
- `completion.is_complete` returns `True` on an untouched scaffold (hash mismatch or heuristic broken).
- Kid reports the seeded `title`/`testable_claim` interfered with their writing (e.g., their instructions said "fill the body" but they infer frontmatter is now editable too).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Two versions on top of the kid's: the parent's review edit, then the director's
correction of one claim in that review.

**The parent's substantive work stands.** It backfilled `title` and
`testable_claim`, whose absence on this very file reproduces the defect the
file hypothesizes about (`goal:s31`) — and it established the fact that makes
S31's first candidate fix viable: `scaffold_hash` hashes the **body**, not the
frontmatter (`completion.py`), so seeding required frontmatter fields cannot
break completion detection. That was the open constraint in S31 and it is now
answered.

**One claim in that review was wrong and is removed rather than softened.** The
parent wrote that "dispatch pre-wrote the claim, the kid changed no body text."
It did not. `BODY_PROMPTS['hypothesis']` is three lines of prompt — *"What is
the testable claim? What would prove it? What would disprove it?"* — and the
kid's testable claim, four proof criteria and three disproof criteria appear
nowhere in its `context.md` (checked: zero matches in 3,805 bytes). The kid
authored this body.

Recorded rather than quietly deleted, because the error is instructive in a
session that leaned hard on parents' `struggles:` lines. That field found
`goal:s27`, `goal:s28` and `goal:s31` — three real defects the reviews they
came attached to had missed — so the standing advice to read it first is
right. This is the counter-example that keeps it advice rather than a rule: it
is the cheapest signal in the system and it is still a claim, not a finding.
Left unchecked here it would have written "the kids are not really working"
into the graph as provenance, which is the one thing a THOUGHT block must
never carry.
<!-- THOUGHT:END -->

## Agent Notes
Seeded hypothesis: scaffold can populate title+testable_claim from dispatch context without harming completion detection