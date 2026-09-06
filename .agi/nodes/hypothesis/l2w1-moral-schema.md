---
id: hypothesis:l2w1-moral-schema
mint_id: e41e9049da6643e38f64dc235ed9d62a
type: hypothesis
parents:
  - goal:g12
next_edges: []
edited_by: director
scaffold_hash: f5f18d094ff521d1
testable_claim: A [moral].md schema exists such that the spawn gate accepts a moral node with an empty parents list and links.py schema reports no violation for it
thought_session: agi-master-2026-09-06
title: "L2 wave 1: l2w1-moral-schema"
---
# hypothesis:l2w1-moral-schema

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: .agi/context/schemas/[moral].md (new), only this file. Copy the frontmatter layout of [vision].md. name: moral. fields: title (str); axis (str, one of vertical, lateral, crossing, dynamics, form); grounded_in (str: moral:faith for four of them, the sentinel word Source for faith only, never a parent edge); season_introduced (int); edited_by (str, owner). validation.required: [id, type, mint_id, title, axis, grounded_in, season_introduced, edited_by]; regex on axis. spawn: allowed_parents [], min_parents 0, max_parents 0. Body text after the frontmatter: the only parentless type (goal:g12); hand-edited only, cap 5 (caps live on the ladder node); body regions in this order ESSENCE (owner's verbatim text, never regenerated), QUESTION, IN PRACTICE, VIOLATED WHEN, REFERENCE; and that write.py will refuse moral:* unless --actor owner (wave 2 builds that refusal, do not build it here). VERIFY: links.py schema shows no new violations; commands.py run tests green; python3 extensions/agi/bin/write.py create moral probe --set axis=vertical --set grounded_in=Source --set season_introduced=1 --set edited_by=owner --dry-run prints SPAWN-GATE APPROVED, and you do not create it for real; if the gate refuses because [shape].md parentless_types does not yet list moral (a parallel kid changes it), report exactly that and mark the claim inconclusive rather than editing [shape].md. One new test asserting a parentless moral passes the gate, red before the file exists, green after. Section 3. REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Edit only the file or files named here. Do not commit, do not push, do not run grid.py. If git status shows files you did not create, report them and never touch them. Design source, read the named section before editing: .agi/context/season-ladder-and-morals-brief.md
