---
id: hypothesis:a00-edae0fba-940d3a
mint_id: f92d3a2537d14e7b9f11d4732bda767d
type: hypothesis
parents:
  - goal:g7.33.10.1
confidence: 0.0
edited_by: belam
evidence_runs:
  - experiment:dg2close-a00-edae0fba-940d3a-check
scaffold_hash: 19458dca89a121d7
season: 1
testable_claim: If node_writer.write_node seeds the schema-required title and testable_claim from dispatch-time context, the scaffolded hypothesis passes [hypothesis] required-field validation at birth, and completion.is_complete still returns False on the untouched scaffold and True once the body is filled.
thought_session: season
title: Seeding title+testable_claim at scaffold time makes hypothesis nodes schema-valid at birth
verdict: disproved
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
Moved from goal:s31 to goal:g7.33.10.1 because its disproved claim (seed testable_claim at scaffold) is the evidence g7.33.10.1 cites that the fix is the lift at done, not seeding, which leaves only the pre-gate corpus open. goal:g7.33.10.1 is the live leaf the council re-homed retired s31 into, and its body cites this node by id. Owner, verbatim: "Move all hypotheses under all retired s goals to be patented by appropriate nested g-goals". Parenthood only (owner: "The regime doesn't need a goal. We're just adjusting parenthood"): mint_id, body and verdict unchanged.
<!-- THOUGHT:END -->

## Agent Notes
Seeded hypothesis: scaffold can populate title+testable_claim from dispatch context without harming completion detection
