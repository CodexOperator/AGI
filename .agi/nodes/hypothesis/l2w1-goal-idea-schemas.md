---
id: hypothesis:l2w1-goal-idea-schemas
mint_id: 110d23d222b44631935ac21f27b4b227
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: 5a5d1533a7a514f6
testable_claim: "[goal].md lets a long-term goal name a vision parent and [idea].md accepts goal or vision parents and carries authors, with GOALS.md still round-tripping byte-identical"
thought_session: agi-master-2026-09-06
title: "L2 wave 1: l2w1-goal-idea-schemas"
---
# hypothesis:l2w1-goal-idea-schemas

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILES: .agi/context/schemas/[goal].md and [idea].md, both, nothing else. [goal].md: variant long-term allowed_parents [build, goal, vision], min_parents 0 with a comment that parentless long-term goals are grandfathered season 1 and new ones name a vision or goal parent; variant short-term: add the comment that every S goal is parented on goal:g15, done 2026-09-06, 35 of 35. [idea].md: spawn.allowed_parents [goal, vision]; min_parents 1; max_parents 2; add field authors (list of agent ids; for a co-authored memo idea every listed author is required, see goal:g12.2 and section 2 Ideas as memos); pre-existing parentless ideas are grandfathered. VERIFY: links.py schema same or fewer violations for goal and idea; python3 extensions/agi/bin/snapshot-goals.py --render --check must print round-trip byte-identical; commands.py run tests green with one new or updated test per file. Section 2. REPORT: write one experiment node whose parents is this hypothesis, with a verdict on the testable claim; evidence_runs must be a list of node ids, your own experiment node counts once it exists; list every verify command and its actual output in the body. Edit only the file or files named here. Do not commit, do not push, do not run grid.py. If git status shows files you did not create, report them and never touch them. Design source, read the named section before editing: .agi/context/season-ladder-and-morals-brief.md

AMENDMENT 2026-09-06 after round 1: the [shape].md kid already set [goal].md long-term and short-term min_parents to 1 and [idea].md min_parents to 1, with grandfather comments, because parentless_types is now [moral] and the gate refuses an empty parents list for any other type regardless of min_parents. Keep min_parents 1 on both goal variants; do not revert to 0. Your remaining work on [goal].md is allowed_parents [build, goal, vision] for long-term and the goal:g15 comment on short-term; on [idea].md it is allowed_parents [goal, vision], max_parents 2, and the authors field. Run git diff on both files first and build on what is there.
