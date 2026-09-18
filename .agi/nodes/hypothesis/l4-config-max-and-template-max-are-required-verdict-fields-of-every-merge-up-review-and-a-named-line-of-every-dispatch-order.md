---
id: hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order
mint_id: c4b35cf5268e4da887e9ebdbc1f48433
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: fdf03c4759f10cb6
season: 2
testable_claim: "(1) merge-up-review.json: the review stage schema REQUIRES `config_max` and `template_max`, each {answer: yes|no, where: <cell or template line named when yes>}, the review prompt asks both questions in the owner's words, and the verify stage's `verdicts` carry them through; a return missing either is schema-invalid (the existing validate_return path names the missing field). (2) the dispatch-order template (config:rotations / the director brief §1 order shape) carries ONE named line the kid answers first: \"config-max: <what moves to a cell> / template-max: <what moves to a template line> / code: <the trigger or resolver that does not exist>\"; the kid's experiment node records the three answers. (3) a test proves a review return without the two fields is refused by name and one with them validates; a second test proves the brief/template text carries the line. (4) mur runs on pi keep the same wall/load behaviour byte-identical apart from the two new fields. CEILING 10 production lines + manifest/template/brief text."
title: "SM.125 (owner 22:0xZ in the sanctuary-master pane: \"Add these config max and template max checks as part of build and review workflow and/or as standing rules to directors/masters\"): config_max + template_max are REQUIRED fields of every merge-up-review verdict and a named line of every dispatch order, so a change that belongs in a cell or a template line is returned by name, never accepted as code"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-config-max-and-template-max-are-required-verdict-fields-of-every-merge-up-review-and-a-named-line-of-every-dispatch-order

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.125 BRIEF (sanctuary-master 22:1xZ 09-18). Standing rule already landed in doc:unified-director-brief §2 (f39a661b6): build direction + review direction, every round. This round makes the rule MECHANICAL: merge-up-review.json review + verify stage schemas (required lists at the stages labelled review / verify) gain config_max + template_max; the dispatch order shape gains the named line; tests as in the claim. Template/config half: the manifest + rotations template text are DATA -- the director cuts them in the same round (master-sensei informed by sanctuary-master, per the formation), code = the 10-line schema/validation seam only if validate_return does not already refuse a missing required field (measured: it does -- workflow.py validate_return names missing required fields; so code may be ZERO lines). FILE SCOPE: workflows/merge-up-review.json, .geometry/rotations.md (order template line), brief §1 one line, one test file. Queue: after SM.124 or in the first free slot (cap 3). Deliver batch + review in ONE line -- and that review itself must carry the two fields (the round proves its own rule).
