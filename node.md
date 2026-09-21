---
id: hypothesis:l4-links-roles-report
mint_id: 73d3f7d68f00435aa2928a6ac959fda9
type: hypothesis
parents:
  - goal:g13
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 905c6a3bc6ffcc03
season: 2
status: pending
tags:
  - l4
  - g13
  - provenance
  - schema
  - report
testable_claim: "`links.py roles` is a THIRD dry report beside `links` and `schema`, and it reports the COVERAGE GAP as well as the violations -- because today the gap IS the finding. MEASURED FIRST, so the claim is not built on a guess: 214 of 1830 nodes carry a `role:` in frontmatter (170 kid, 38 parent, 6 director, stamped by `node_writer._pick(\"role\", \"AGI_ROLE\")` at `:728`), and EXACTLY ONE schema in `.agi/context/schemas/` declares `written_by:` -- `[moral].md`. So a report that only listed violations would print a near-empty list and read as a clean bill of health, when the truth is that almost nothing is CHECKABLE yet. THE REPORT MUST PRINT BOTH HALVES: (a) for every node type, whether its schema declares `written_by:` at all, so the unchecked types are VISIBLE and counted; (b) for the types that do declare one, every node whose recorded writer is not admitted, named with its node id and the writer found. The recorded writer is read from what already exists -- frontmatter `role:`, and `edited_by:` -- and where a node records no writer the report says UNRECORDED rather than guessing or skipping silently. IT CHANGES NOTHING: no node is written, no schema is edited, no `--fix` is added. It is the third `action` choice at `links.py:294` and it follows `_schema_report`'s shape (`:334`) -- dry by default and loudly so. PROVED BY: (1) `python3 extensions/agi/bin/links.py roles` runs on this corpus and PRINTS its output -- paste it, do not describe it -- showing the per-type declared/undeclared census and any violations; (2) `git status --porcelain` is byte-identical before and after the run -- SHOW BOTH; (3) a test in `extensions/agi/tests/` builds a fixture corpus with a schema declaring `written_by: owner` and one node recorded against a different writer, and asserts the report NAMES that node and still writes nothing; (4) `python3 extensions/agi/bin/links.py links` and `links.py schema` print exactly what they printed before -- the existing two actions are untouched. DISPROVED IF: the report writes anything, the violations half is present but the coverage half is not, an unrecorded writer is silently skipped or filled with a guess, or `links` and `schema` change their output. HARD CEILING: 2 kids. Run `pytest extensions/agi/tests/test_links.py -q` plus whatever test file you add, and NOTHING else -- do NOT run the full suite, and say so in the node. Do NOT touch `.agi/nodes/.geometry/*`. Edit nodes through `write.py` verbs only."
thought_session: sanctuary-director-genII-L4
title: Only one schema declares who may write its type, so a violations-only role report would read as a clean bill of health
---
<!-- BODY:BEGIN -->
# hypothesis:l4-links-roles-report

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THIS CLAIM CORRECTS MY OWN EARLIER FINDING, and the correction is worth more than the round. When I opened as gen II I told the prime that `doc:l4-plan` had L4.05 and L4.06 as siblings and that L4.05 was really downstream of L4.06, because 'L4.05 has no data source -- the write-log carries no actor, role or seat'. The prime accepted that and recorded it in `goal:g17.1` and in the plan's dependency graph.

The conclusion was right and HALF THE EVIDENCE WAS WRONG. It is true that the write-log carried no writer, and L4.06 fixed that. But L4.05 never had to read the write-log: 214 nodes already carry `role:` in their own frontmatter, stamped at mint by `node_writer._pick("role", "AGI_ROLE")` (`:728`). I did not check that before asserting the absence, and a count I could have taken in one grep would have shown it.

THE REAL BOTTLENECK IS THE OTHER SIDE OF THE JOIN. A role report compares a node's recorded writer against what its TYPE admits, and exactly one schema -- `[moral].md` -- declares `written_by:` at all. So the report is thin today not for want of writers but for want of RULES to check them against. That reframes the round rather than cancelling it: the coverage gap is the finding, and a report that hides it behind an empty violations list would actively mislead. Hence both halves in the claim.

It also means L4.05's true prerequisite is L4.09 (flipping `warn` to `refuse` per type, which is where more schemas gain a declared writer), not L4.06 -- and L4.09 is owner-go. That is a dependency correction to a dependency correction, and it is banked for the prime rather than acted on: this round builds the report that MEASURES the gap, which is exactly the input such a decision needs.
<!-- THOUGHT:END -->
