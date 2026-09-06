---
id: hypothesis:l2w3-brief-heads
mint_id: bc3274360640428ca1f245d1aa8e97ff
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: a962cd579d85089b
testable_claim: brief.py has a director and a prime_director tier, and every tier's brief begins with the prayers and readings in the ladder node's read_order for that role, sourced from moral:faith's REFERENCE region at run time rather than copied into code
thought_session: agi-master-2026-09-06
title: "L2 wave 3: l2w3-brief-heads"
---
# hypothesis:l2w3-brief-heads

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: extensions/agi/bin/brief.py plus tests; dispatch.py only if the tier map needs the two new names. Section 4.5, Reading order by role, and the ladder node's read_order field. RULE: brief.assemble(tier=...) prepends a head built from .agi/nodes/moral/faith.md: parse its REFERENCE region by the section headings it carries (4.1 the four prayers, 4.2 words of Jesus, 4.3 the Tao, 4.4 carried sayings, plus the soul-mind-body paragraph from the ESSENCE or IN PRACTICE region of the morals as the brief names it) and emit, in the ladder's read_order for that role, only the parts that role reads: kid gets the four prayers and nothing else; parent adds words of Jesus and soul-mind-body; director adds Tao 1 and 56 and the five axes (one line per moral: name, axis, question); prime_director adds the carried sayings. Prayers always first, before the map, before the target. The Church Slavonic is copied byte for byte from the node; attributions (God through the prophet, Paul) stay as written. TIERS: add director and prime_director assemblers; a director's job text is: hold the lens for the goals it owns, dispatch parents through dispatch.py --tier parent, never do kid work, judge each parent's report through the lens above (season.py judge), write HANDOFF.md live, rotate at the ladder's director_rotate_at through rotate.py; prime_director adds: master is yours alone, merge never rebase, grid commit --all only on master, self-rotate. Keep each job text under twenty lines. VERIFY red-first: the kid head contains the four prayers and not the Tao; the director head contains Tao 1; a missing moral:faith node raises a named error rather than an empty head; suite green. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs to cli.py done), every verify command with its actual output in the body. Engine files are edited in place; a new engine file goes directly under extensions/agi/bin/. Suite via python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md
